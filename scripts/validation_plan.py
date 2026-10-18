"""Select repository validation by evidence layer and actual changed paths."""

import json
import os
import subprocess
from pathlib import Path

if __package__ in {None, ""}:
    from skill_packages import skill_packages
else:
    from .skill_packages import skill_packages

ROOT = Path(__file__).resolve().parents[1]
CHECKS = (
    "checks",
    "codex-discovery",
    "claude-discovery",
    "fern-install",
    "blender",
    "agent-behavior",
)
LAYERS = ("pr", "affected", "full")
ENGINE_TESTS = {
    "test_scene_blender_integration.py",
    "test_low_poly_blender_integration.py",
}


def git(root, *arguments):
    return subprocess.run(
        ["git", *arguments], cwd=root, capture_output=True, check=True
    ).stdout


def changed_paths(root, base):
    """Include working-tree edits and unignored additions, plus both rename paths."""
    if base.startswith("-"):
        raise ValueError("--base must be a Git revision, not an option")
    revision = git(root, "rev-parse", "--verify", base + "^{commit}").decode().strip()
    names = git(root, "diff", "--no-renames", "--name-only", "-z", revision, "--")
    names += git(root, "ls-files", "--others", "--exclude-standard", "-z")
    return revision, sorted(set(os.fsdecode(names).split("\0")) - {""})


def test_inventory(root):
    modules = sorted(path.name for path in (root / "tests").glob("test_*.py"))
    return {
        "checks": [name for name in modules if name not in ENGINE_TESTS],
        "blender": [name for name in modules if name in ENGINE_TESTS],
    }


def affected_skills(paths, packages, root):
    """Shared harness/dependency changes conservatively select every package."""
    if paths is None:
        return sorted(packages)
    shared = (
        "scripts/",
        "tests/",
        "examples/",
        ".github/",
        "requirements",
        "package",
    )
    if any(
        path.startswith(shared)
        or path in {"AGENTS.md", "ruff.toml", ".markdownlint-cli2.jsonc"}
        for path in paths
    ):
        return sorted(packages)
    selected = set()
    for path in paths:
        collection = None
        parts = Path(path).parts
        if path == ".agents/plugins/marketplace.json":
            collection = "fern"
        elif (
            len(parts) == 4
            and parts[0] == "skills"
            and parts[2:] == (".codex-plugin", "plugin.json")
        ):
            collection = parts[1]
        if collection:
            selected.update(
                name
                for name, package in packages.items()
                if package.relative_to(root).parts[:2] == ("skills", collection)
            )
            continue
        for name, package in packages.items():
            relative = package.relative_to(root).as_posix()
            if path == relative or path.startswith(relative + "/"):
                selected.add(name)
            elif path.startswith("skills/") and path.endswith("README.md"):
                if relative.startswith(path.rsplit("/", 1)[0] + "/"):
                    selected.add(name)
        # A deleted/moved package can disappear from current discovery. Keep
        # removals conservative instead of silently assigning no runtime checks.
        if path.startswith("skills/") and not any(
            path.startswith(package.relative_to(root).as_posix() + "/")
            for package in packages.values()
        ):
            selected.update(packages)
    return sorted(selected)


def make_plan(layer, *, root=ROOT, base=None, cases=None, checks=None, latest=False):
    root = Path(root).resolve()
    if layer not in LAYERS:
        raise ValueError(f"Unknown validation layer: {layer}")
    if layer == "pr" and (cases or latest):
        raise ValueError("Case selection and latest clients require affected/full")
    if base and layer != "affected":
        raise ValueError("--base applies only to the affected layer")
    if checks and set(checks) - set(CHECKS):
        raise ValueError("Unknown check selection")
    packages = skill_packages(root)
    spec = json.loads((root / "examples/behavior-smoke.json").read_text("utf-8"))
    definitions = spec["cases"]
    known = {case["id"]: case for case in definitions}
    if len(known) != len(definitions):
        raise ValueError("Behavior case IDs must be unique")
    if cases and set(cases) - known.keys():
        raise ValueError("Unknown behavior case selection")
    missing = {case["skill"] for case in definitions} - packages.keys()
    if missing:
        raise ValueError(f"Behavior cases reference missing skills: {sorted(missing)}")
    base_sha, paths = changed_paths(root, base) if base else (None, None)
    selected = affected_skills(paths, packages, root)
    if cases:
        if len(set(cases)) != len(cases):
            raise ValueError("Behavior case IDs must be unique")
        case_skills = {known[item]["skill"] for item in cases}
        selected = sorted(set(selected) | case_skills) if base else sorted(case_skills)
    chosen = [
        case
        for case in definitions
        if (case["id"] in cases if cases else case["skill"] in selected)
    ]
    requested = ["checks"] if layer == "pr" else []
    if layer != "pr":
        if layer == "full":
            requested.append("checks")
        if selected:
            requested += ["codex-discovery", "claude-discovery"]
        if any(name in selected for name in ("setup-fern", "maintain-skills")):
            requested.append("fern-install")
        if any(
            packages[name].relative_to(root).parts[1] == "blender" for name in selected
        ):
            requested.append("blender")
        if chosen:
            requested.append("agent-behavior")
    if checks:
        if layer == "pr" and set(checks) != {"checks"}:
            raise ValueError("The pr layer runs only checks")
        if set(checks) - set(requested):
            raise ValueError(
                "Requested check is not applicable to the selected changes"
            )
        requested = [check for check in requested if check in checks]
    entries = []
    for check in requested:
        channels = (
            ["pinned", "latest"]
            if (check.endswith("-discovery") and (latest or layer == "full"))
            else ["pinned"]
        )
        for channel in channels:
            entries.append(
                {
                    "id": check + ("-latest" if channel == "latest" else ""),
                    "check": check,
                    "channel": channel,
                    "cases": [case["id"] for case in chosen]
                    if check == "agent-behavior"
                    else [],
                    "model_required": check == "agent-behavior",
                }
            )
    by_skill = {}
    for case in chosen:
        by_skill.setdefault(case["skill"], []).append(case["id"])
    uncovered = [name for name in selected if name not in by_skill]
    manual = []
    for group, reason in (
        (
            "godot",
            "Real Godot import/build/editor and project-specific runtime acceptance",
        ),
        ("blender", "Visual quality, rig usability, and live-editor acceptance"),
        ("image-generation", "Real image inputs/outputs and visual acceptance"),
    ):
        names = [
            name
            for name in selected
            if packages[name].relative_to(root).parts[1] == group
        ]
        if names:
            manual.append(
                {"scope": group, "skills": names, "status": "not_run", "reason": reason}
            )
    if "setup-fern" in selected:
        manual.append(
            {
                "scope": "native-host",
                "skills": ["setup-fern"],
                "status": "not_run",
                "reason": "Effective project config, native custom-agent/instruction loading, Windows migration and Codex Cloud publication/new-task discovery require host evidence",
            }
        )
    fern_skills = [
        name
        for name in selected
        if packages[name].relative_to(root).parts[:2] == ("skills", "fern")
    ]
    if fern_skills:
        manual.append(
            {
                "scope": "fern-plugin",
                "skills": fern_skills,
                "status": "not_run",
                "reason": "Codex plugin cache loading and fresh-host marketplace installation require separate host evidence from standalone skill installation and discovery",
            }
        )
    if "commit" in selected:
        manual.append(
            {
                "scope": "live-git",
                "skills": ["commit"],
                "status": "not_run",
                "reason": "Live staging, hooks, signing and intermediate-commit checks use the documented manual fixture",
            }
        )
    return {
        "schema_version": 1,
        "layer": layer,
        "source_revision": git(root, "rev-parse", "HEAD").decode().strip(),
        "selection": "changed paths" if base else "all current packages",
        "base_revision": base_sha,
        "changed_paths": paths,
        "selected_skills": selected,
        "checks": entries,
        "test_modules": test_inventory(root),
        "behavior_matrix": [
            {"skill": name, "cases": ids} for name, ids in sorted(by_skill.items())
        ],
        "behavior_coverage": {
            "available_cases": len(definitions),
            "selected_cases": len(chosen) if layer != "pr" else 0,
            "skills_without_cases": uncovered,
            "limits": "Synthetic copied-skill tasks, not general skill quality or native trigger coverage",
        },
        "manual_evidence": manual if layer != "pr" else [],
    }
