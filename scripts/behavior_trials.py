"""Prepare isolated manual agent trials and record evidence, without model calls."""

import argparse
import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "examples/behavior-smoke.json"


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, value):
    Path(path).write_text(
        json.dumps(value, indent=2) + "\n", encoding="ascii", newline="\n"
    )


def hashes(directory):
    """Include every regular file; reject links instead of following them."""
    result = {}
    for path in sorted(Path(directory).rglob("*")):
        if path.is_symlink() or getattr(path.lstat(), "st_file_attributes", 0) & 0x400:
            raise ValueError(f"Links are not permitted in trial trees: {path}")
        if path.is_file():
            result[path.relative_to(directory).as_posix()] = hashlib.sha256(
                path.read_bytes()
            ).hexdigest()
    return result


def inside(root, relative):
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or path == root.resolve():
        raise ValueError(f"Unsafe fixture path: {relative}")
    return path


def definition_hash(case, spec_path):
    payload = {"case": case, "fixtures": {}}
    for fixture in case.get("fixture_files", {}).values():
        payload["fixtures"][fixture] = hashlib.sha256(
            inside(Path(spec_path).parent, fixture).read_bytes()
        ).hexdigest()
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode("ascii")
    ).hexdigest()


def prepare(output, cases=None, source_root=ROOT, spec_path=SPEC):
    output = Path(output).resolve()
    if output.exists():
        raise ValueError(f"Refusing to overwrite existing run directory: {output}")
    spec = read_json(spec_path)
    selected = [case for case in spec["cases"] if not cases or case["id"] in cases]
    if not selected or (cases and set(cases) - {c["id"] for c in selected}):
        raise ValueError("Unknown or empty case selection")
    source_root = Path(source_root).resolve()
    # A run may never write beneath the source packages it snapshots.
    if output.is_relative_to(source_root / "skills"):
        raise ValueError("Run directory must be outside source skill packages")
    revision = subprocess.run(
        ["git", "-C", str(source_root), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    output.mkdir(parents=True)
    for case in selected:
        trial = output / case["id"]
        workspace = trial / "workspace"
        workspace.mkdir(parents=True)
        source = source_root / "skills" / case["skill"]
        source_hashes = hashes(source)
        if "SKILL.md" not in source_hashes:
            raise ValueError(f"Missing source skill: {source}")
        shutil.copytree(source, workspace / "skill")
        for relative, content in case.get("files", {}).items():
            path = inside(workspace, relative)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8", newline="\n")
        for relative, fixture in case.get("fixture_files", {}).items():
            path = inside(workspace, relative)
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(inside(Path(spec_path).parent, fixture), path)
        if case["id"] == "skills-local-edits":
            write_json(
                workspace / "baseline.json",
                {"format-report": hashes(workspace / "baseline/format-report")},
            )
        write_json(
            trial / "input.json",
            {
                "skill": "skill/SKILL.md",
                "context": case["context"],
                "turns": case["turns"],
                "delivery": "Deliver each turn separately in the same fresh session.",
            },
        )
        write_json(trial / "evaluator.json", case["evaluation"])
        write_json(
            trial / "manifest.json",
            {
                "case": case["id"],
                "prepared_at": datetime.now(timezone.utc).isoformat(),
                "source_path": str(source),
                "source_commit": revision.stdout.strip()
                if revision.returncode == 0
                else None,
                "source_hashes": source_hashes,
                "spec_path": str(Path(spec_path).resolve()),
                "definition_hash": definition_hash(case, spec_path),
                "initial_hashes": hashes(workspace),
            },
        )
        shutil.copytree(workspace, trial / "before")
    return [str(output / case["id"]) for case in selected]


def changes(before, after):
    return [
        {
            "path": path,
            "kind": "added"
            if path not in before
            else "deleted"
            if path not in after
            else "modified",
            "before": before.get(path),
            "after": after.get(path),
        }
        for path in sorted(before.keys() | after.keys())
        if before.get(path) != after.get(path)
    ]


def outside_section(content, heading):
    """Use Markdown heading maps for scope and raw bytes for preservation."""
    tokens = MarkdownIt("commonmark").parse(content.decode("utf-8"))
    headings = [
        (token, tokens[index + 1].content)
        for index, token in enumerate(tokens)
        if token.type == "heading_open"
        and token.tag in {"h1", "h2"}
        and token.level == 0
    ]
    selected = [
        token
        for token, title in headings
        if token.tag == "h2" and title == heading.removeprefix("## ")
    ]
    if len(selected) != 1:
        return None
    offsets = [0]
    for line in content.splitlines(keepends=True):
        offsets.append(offsets[-1] + len(line))
    start_line = selected[0].map[0]
    end_line = next(
        (token.map[0] for token, _ in headings if token.map[0] > start_line),
        len(offsets) - 1,
    )
    start, end = offsets[start_line], offsets[end_line]
    return content[:start], content[end:]


def check_invariants(trial, evaluation, before, after):
    results = []
    delta = changes(before, after)
    for rule in evaluation.get("invariants", []):
        kind = rule["kind"]
        if kind == "unchanged":
            passed = not delta
        elif kind == "only_changes":
            passed = all(item["path"] in rule["paths"] for item in delta)
        elif kind == "changed":
            passed = all(before.get(p) != after.get(p) for p in rule["paths"])
        elif kind == "outside_section_unchanged":
            original = (trial / "before" / rule["path"]).read_bytes()
            current_path = trial / "workspace" / rule["path"]
            current = current_path.read_bytes() if current_path.exists() else b""
            expected = outside_section(original, rule["heading"])
            passed = (
                expected is not None
                and outside_section(current, rule["heading"]) == expected
            )
        elif kind == "no_mutation_commands":
            path = trial / "workspace" / rule["path"]
            commands = (
                [json.loads(line) for line in path.read_text().splitlines()]
                if path.exists()
                else []
            )
            passed = all(not command["mutation"] for command in commands)
        else:
            raise ValueError(f"Unknown invariant: {kind}")
        results.append({"id": rule["id"], "status": "passed" if passed else "failed"})
    return results


def record(trial, transcript_path, assessment_path, runner, model):
    trial = Path(trial).resolve()
    if (trial / "result.json").exists():
        raise ValueError("Result already recorded; prepare a fresh trial for a rerun")
    manifest = read_json(trial / "manifest.json")
    inputs = read_json(trial / "input.json")
    evaluation = read_json(trial / "evaluator.json")
    transcript = read_json(transcript_path)
    assessment = read_json(assessment_path)
    if not isinstance(transcript, dict) or not isinstance(assessment, dict):
        raise ValueError("Transcript and assessment must be JSON objects")
    turns = transcript.get("turns", [])
    if not isinstance(turns, list) or not all(isinstance(turn, dict) for turn in turns):
        raise ValueError("Transcript turns must be a list of JSON objects")
    assessments = assessment.get("criteria", {})
    if not isinstance(assessments, dict):
        raise ValueError("Assessment criteria must be a JSON object")
    complete = len(turns) == len(inputs["turns"]) and all(
        turn.get("request") == request
        and isinstance(turn.get("response"), str)
        and bool(turn["response"].strip())
        for turn, request in zip(turns, inputs["turns"])
    )
    evaluated = []
    for criterion in evaluation["criteria"]:
        supplied = assessments.get(criterion["id"], {})
        if not isinstance(supplied, dict):
            raise ValueError("Each criterion assessment must be a JSON object")
        status = supplied.get("status", "unverified")
        reason = supplied.get("reason", "Not assessed")
        evidence = supplied.get("evidence", [])
        if status not in {"passed", "failed", "unverified"}:
            raise ValueError("Assessment status must be passed, failed, or unverified")
        if (
            not isinstance(assessment.get("evaluator"), str)
            or not assessment["evaluator"].strip()
            or not isinstance(reason, str)
            or not reason.strip()
            or not isinstance(evidence, list)
            or not evidence
            or not all(isinstance(item, str) and item.strip() for item in evidence)
        ):
            status = "unverified"
        evaluated.append(
            {
                "id": criterion["id"],
                "status": status,
                "reason": reason,
                "evidence": evidence,
            }
        )
    before = manifest["initial_hashes"]
    after = hashes(trial / "workspace")
    source = Path(manifest["source_path"])
    drift = changes(
        manifest["source_hashes"], hashes(source) if source.exists() else {}
    )
    current_case = next(
        (
            case
            for case in read_json(manifest["spec_path"])["cases"]
            if case["id"] == manifest["case"]
        ),
        None,
    )
    definition_drift = (
        current_case is None
        or definition_hash(current_case, manifest["spec_path"])
        != manifest["definition_hash"]
    )
    invariants = check_invariants(trial, evaluation, before, after)
    statuses = [item["status"] for item in evaluated + invariants]
    outcome = (
        "failed"
        if "failed" in statuses
        else "unverified"
        if not complete or drift or definition_drift or "unverified" in statuses
        else "passed"
    )
    shutil.copytree(trial / "workspace", trial / "after")
    write_json(trial / "transcript.json", transcript)
    write_json(trial / "assessment.json", assessment)
    result = {
        "case": manifest["case"],
        "runner": runner,
        "model": model,
        "evaluator": assessment.get("evaluator"),
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "outcome": outcome,
        "transcript_complete": complete,
        "source_commit": manifest["source_commit"],
        "source_drift": drift,
        "definition_drift": definition_drift,
        "file_changes": changes(before, after),
        "invariants": invariants,
        "criteria": evaluated,
        "limits": (
            "Semantic scores are evaluator-supplied assessments. Filesystem checks "
            "cover only the trial workspace, not the entire host. Explicit skill "
            "loading only; no host discovery or automatic selection claim."
        ),
    }
    write_json(trial / "result.json", result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    prepare_parser = commands.add_parser("prepare")
    prepare_parser.add_argument("--output", required=True, type=Path)
    prepare_parser.add_argument("--case", action="append", dest="cases")
    record_parser = commands.add_parser("record")
    record_parser.add_argument("--trial", required=True, type=Path)
    record_parser.add_argument("--transcript", required=True, type=Path)
    record_parser.add_argument("--assessment", required=True, type=Path)
    record_parser.add_argument("--runner", required=True)
    record_parser.add_argument("--model", required=True)
    args = parser.parse_args()
    try:
        if args.command == "prepare":
            print(json.dumps(prepare(args.output, args.cases), indent=2))
        else:
            result = record(
                args.trial, args.transcript, args.assessment, args.runner, args.model
            )
            print(json.dumps(result, indent=2))
            return 0 if result["outcome"] == "passed" else 1
    except (ValueError, OSError, KeyError) as error:
        parser.exit(2, f"{error}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
