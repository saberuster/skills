"""Probe public Fern CLI installation in an explicit disposable Linux home.

This exercises scripted installer mechanics and Codex discovery, not a model's
execution of setup-fern. It does not apply configuration, agents, or instructions.
"""

import argparse
import contextlib
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

try:
    from scripts.check_codex_skills import (
        DiscoveryError,
        JsonLineProcess,
        executable_command,
        isolated_environment,
        package_sha256,
        same_path,
    )
except ModuleNotFoundError:
    from check_codex_skills import (
        DiscoveryError,
        JsonLineProcess,
        executable_command,
        isolated_environment,
        package_sha256,
        same_path,
    )

ROOT = Path(__file__).resolve().parents[1]
SKILLS_VERSION = "1.7.0"
SOURCES = {"saberuster/skills": "main", "cli/cli": "trunk"}


@contextlib.contextmanager
def disposable_home(target):
    """Require an unused temp-root name; create the actual HOME with tempfile."""
    if sys.platform != "linux":
        raise DiscoveryError("Run the install probe in disposable Linux CI or Docker")
    target = Path(target)
    temporary_root = Path(tempfile.gettempdir()).resolve()
    if not target.is_absolute() or target.parent.resolve() != temporary_root:
        raise DiscoveryError("--home must be an unused direct child of the temp root")
    if target.exists() or target.is_symlink():
        raise DiscoveryError("--home must not already exist")
    target = target.resolve()
    if ROOT.is_relative_to(target) or target.is_relative_to(ROOT):
        raise DiscoveryError("--home must be outside the source checkout")
    if target == Path.home().resolve():
        raise DiscoveryError("--home must not be the current user home")
    target.mkdir(mode=0o700)
    try:
        with tempfile.TemporaryDirectory(prefix="profile-", dir=target) as home:
            yield target, Path(home)
    finally:
        # Only this context's exclusively created disposable directory is removed.
        shutil.rmtree(target)


def run(command, cwd, env, timeout, commands):
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        timeout=timeout,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    commands.append(
        {
            "command": command,
            "returncode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
    )
    if completed.returncode:
        raise DiscoveryError(
            f"Command failed ({completed.returncode}): {' '.join(command)}"
        )
    return completed.stdout


def fetch_snapshot(repository, branch, destination, env, timeout, commands):
    url = f"https://github.com/{repository}.git"
    resolved = run(
        ["git", "ls-remote", url, f"refs/heads/{branch}"],
        destination.parent,
        env,
        timeout,
        commands,
    ).splitlines()
    if len(resolved) != 1:
        raise DiscoveryError(f"Could not resolve exactly one {repository} {branch}")
    fields = resolved[0].split()
    if (
        len(fields) != 2
        or not re.fullmatch(r"[0-9a-f]{40}", fields[0])
        or fields[1] != f"refs/heads/{branch}"
    ):
        raise DiscoveryError(f"Invalid resolved ref for {repository}")
    revision = fields[0]
    run(["git", "init", str(destination)], destination.parent, env, timeout, commands)
    run(
        ["git", "fetch", "--depth", "1", url, revision],
        destination,
        env,
        timeout,
        commands,
    )
    run(
        ["git", "checkout", "--detach", "FETCH_HEAD"],
        destination,
        env,
        timeout,
        commands,
    )
    return {"repository": repository, "branch": branch, "sha": revision, "url": url}


def select_packages(snapshot, directories):
    """Discover only the selected subtrees, checking leaf and name boundaries."""
    packages = {}
    for relative in directories:
        directory = snapshot / relative
        if not directory.is_dir():
            raise DiscoveryError(f"Missing required source directory: {relative}")
        files = sorted(directory.rglob("SKILL.md"))
        if not files:
            raise DiscoveryError(f"Empty required source directory: {relative}")
        package_directories = {skill.parent for skill in files}
        for skill in files:
            package = skill.parent
            if any(
                parent in package_directories
                for parent in package.parents
                if parent.is_relative_to(directory)
            ):
                raise DiscoveryError(f"Nested package boundary: {skill}")
            parts = skill.read_text(encoding="utf-8").split("---", 2)
            if len(parts) != 3 or parts[0]:
                raise DiscoveryError(f"Missing YAML frontmatter: {skill}")
            try:
                metadata = yaml.safe_load(parts[1])
            except yaml.YAMLError as error:
                raise DiscoveryError(f"Invalid YAML frontmatter: {skill}") from error
            name = metadata.get("name") if isinstance(metadata, dict) else None
            description = (
                metadata.get("description") if isinstance(metadata, dict) else None
            )
            if (
                name != package.name
                or not isinstance(name, str)
                or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)
                or not isinstance(description, str)
                or not description.strip()
            ):
                raise DiscoveryError(f"Invalid source skill identity: {skill}")
            if name in packages:
                raise DiscoveryError(f"Duplicate selected skill: {name}")
            packages[name] = {
                "path": package,
                "skill_path": skill.relative_to(snapshot).as_posix(),
                "selection": relative,
                "description": description,
                "sha256": package_sha256(package),
            }
    return packages


def parse_install(stdout, selected, repository, revision, home):
    try:
        rows = json.loads(stdout)
    except ValueError as error:
        raise DiscoveryError("Installer did not return valid JSON") from error
    if not isinstance(rows, list) or len(rows) != len(selected):
        raise DiscoveryError("Installer returned incomplete selected skill results")
    seen = set()
    for row in rows:
        if not isinstance(row, dict) or row.get("name") not in selected:
            raise DiscoveryError("Installer returned an unexpected skill")
        name = row["name"]
        if name in seen:
            raise DiscoveryError(f"Installer returned duplicate skill: {name}")
        seen.add(name)
        if (
            row.get("status") != "installed"
            or row.get("source") != repository
            or row.get("ref") != revision
            or row.get("mode") != "copy"
            or row.get("scope") != "global"
            or row.get("agents") != ["Codex"]
            or not same_path(row.get("path"), home / ".agents/skills" / name)
        ):
            raise DiscoveryError(f"Installer result/provenance mismatch: {name}")
    return rows


def verify_installed(home, expected):
    lock_path = home / ".agents/.skill-lock.json"
    try:
        lock_bytes = lock_path.read_bytes()
        lock = json.loads(lock_bytes)
    except (OSError, ValueError) as error:
        raise DiscoveryError("Missing or invalid installer source lock") from error
    entries = (
        lock.get("skills")
        if isinstance(lock, dict) and lock.get("version") == 3
        else None
    )
    if not isinstance(entries, dict) or set(entries) != set(expected):
        raise DiscoveryError("Installer source lock has missing or unexpected skills")
    rows = []
    for name, package in expected.items():
        record = entries[name]
        source = package["source"]
        provenance = {
            "source": source["repository"],
            "sourceType": "github",
            "sourceUrl": source["url"],
            "ref": source["sha"],
            "skillPath": package["skill_path"],
            "skillFolderHash": package["tree_oid"],
        }
        if not isinstance(record, dict) or any(
            record.get(key) != value for key, value in provenance.items()
        ):
            raise DiscoveryError(f"Installer source provenance mismatch: {name}")
        hashes = {}
        for label, directory in {
            "canonical": home / ".agents/skills" / name,
            "source": package["path"],
        }.items():
            if not directory.is_dir() or not (directory / "SKILL.md").is_file():
                raise DiscoveryError(f"Missing {label} package: {name}")
            hashes[label] = package_sha256(directory)
            if hashes[label] != package["sha256"]:
                raise DiscoveryError(
                    f"Installed package byte mismatch ({label}): {name}"
                )
        rows.append({"name": name, "sha256": hashes, "source_record": record})
    directory = home / ".agents/skills"
    if {p.name for p in directory.iterdir()} != set(expected):
        raise DiscoveryError(f"Unexpected installed package set: {directory}")
    # Skills 1.7.0 treats Codex as universal and installs to .agents/skills.
    # A second user copy would invalidate discovery and the intended target.
    codex_directory = home / ".codex/skills"
    if codex_directory.exists() and any(
        path.name != ".system" for path in codex_directory.iterdir()
    ):
        raise DiscoveryError("Unexpected duplicate Codex user skill installation")
    return rows, lock_bytes


def verify_user_discovery(result, expected, project, home):
    data = result.get("data")
    if (
        not isinstance(data, list)
        or len(data) != 1
        or not isinstance(data[0], dict)
        or not same_path(data[0].get("cwd"), project)
    ):
        raise DiscoveryError("skills/list: missing isolated project result")
    entry = data[0]
    if entry.get("errors") != [] or not isinstance(entry.get("skills"), list):
        raise DiscoveryError("skills/list: load errors or missing skills array")
    rows = []
    for name, package in expected.items():
        matches = [
            row
            for row in entry["skills"]
            if isinstance(row, dict) and row.get("name") == name
        ]
        if len(matches) != 1:
            raise DiscoveryError(
                f"skills/list: missing or duplicate user skill: {name}"
            )
        row = matches[0]
        if (
            row.get("scope") != "user"
            or row.get("enabled") is not True
            or row.get("description") != package["description"]
            or not same_path(
                row.get("path"), home / ".agents/skills" / name / "SKILL.md"
            )
        ):
            raise DiscoveryError(f"skills/list: user discovery mismatch: {name}")
        rows.append(row)
    for row in entry["skills"]:
        if (
            not isinstance(row, dict)
            or not isinstance(row.get("name"), str)
            or (row["name"] not in expected and row.get("scope") != "system")
        ):
            raise DiscoveryError("skills/list: unexpected non-system skill")
    return rows


def check_install(home_target, codex="codex", timeout=180):
    report = {
        "check": "scripted Fern public snapshot installation and user discovery",
        "status": "failed",
        "behavior": "not_run",
        "model_requests": False,
        "resource_application": "not_run",
        "skills_cli_version": SKILLS_VERSION,
        "candidate": [],
        "sources": [],
        "commands": [],
        "errors": [],
    }
    try:
        candidate = select_packages(ROOT, ["skills/fern", "skills/meta"])
        report["candidate"] = [
            {"name": name, "path": row["skill_path"], "sha256": row["sha256"]}
            for name, row in candidate.items()
        ]
        with disposable_home(home_target) as (temporary, home):
            report["disposable_home"] = str(home)
            env = isolated_environment(home)
            env.update(
                CI="1",
                DISABLE_TELEMETRY="1",
                DO_NOT_TRACK="1",
                GIT_TERMINAL_PROMPT="0",
                GIT_CONFIG_NOSYSTEM="1",
                GIT_CONFIG_GLOBAL=str(home / ".gitconfig"),
                NPM_CONFIG_USERCONFIG=str(home / ".npmrc"),
                NPM_CONFIG_CACHE=str(home / ".cache/npm"),
            )
            project = temporary / "project"
            project.mkdir()
            (project / ".git").mkdir()
            snapshots = temporary / "snapshots"
            snapshots.mkdir()
            expected = {}
            batches = []
            for repository, branch in SOURCES.items():
                snapshot = snapshots / repository.split("/")[0]
                source = fetch_snapshot(
                    repository, branch, snapshot, env, timeout, report["commands"]
                )
                report["sources"].append(source)
                selections = (
                    ["skills/fern", "skills/meta"]
                    if repository == "saberuster/skills"
                    else ["skills/gh"]
                )
                packages = select_packages(snapshot, selections)
                for name, package in packages.items():
                    if name in expected:
                        raise DiscoveryError(f"Duplicate required source skill: {name}")
                    package["source"] = source
                    package["tree_oid"] = run(
                        [
                            "git",
                            "rev-parse",
                            f"HEAD:{Path(package['skill_path']).parent.as_posix()}",
                        ],
                        snapshot,
                        env,
                        timeout,
                        report["commands"],
                    ).strip()
                    expected[name] = package
                for selection in selections:
                    names = sorted(
                        n for n, p in packages.items() if p["selection"] == selection
                    )
                    batches.append((source, selection, names))
            # npx resolves this exact published version, inside the disposable npm cache.
            cli = ["npx", "--yes", f"skills@{SKILLS_VERSION}"]
            version = run(
                [*cli, "--version"], project, env, timeout, report["commands"]
            ).strip()
            if version != SKILLS_VERSION:
                raise DiscoveryError("Skills CLI did not report the pinned version")
            for source, selection, names in batches:
                url = (
                    f"https://github.com/{source['repository']}/tree/"
                    f"{source['sha']}/{selection}"
                )
                stdout = run(
                    [
                        *cli,
                        "add",
                        url,
                        "--skill",
                        *names,
                        "--agent",
                        "codex",
                        "-g",
                        "--copy",
                        "-y",
                        "--json",
                    ],
                    project,
                    env,
                    timeout,
                    report["commands"],
                )
                parse_install(stdout, names, source["repository"], source["sha"], home)
            report["installed"], before = verify_installed(home, expected)
            report["codex_version"] = run(
                executable_command(codex, ["--version"]),
                project,
                env,
                timeout,
                report["commands"],
            ).strip()
            with JsonLineProcess(
                executable_command(codex, ["app-server", "--stdio"]),
                project,
                env,
                timeout,
            ) as server:
                try:
                    initialized = server.request(
                        1,
                        "initialize",
                        {"clientInfo": {"name": "fern_install_ci", "version": "1.0"}},
                    )
                    if not same_path(initialized.get("codexHome"), home / ".codex"):
                        raise DiscoveryError("Codex did not use isolated CODEX_HOME")
                    server.send({"method": "initialized"})
                    result = server.request(
                        2, "skills/list", {"cwds": [str(project)], "forceReload": True}
                    )
                    report["discovered"] = verify_user_discovery(
                        result, expected, project, home
                    )
                finally:
                    report["server_stderr"] = server.stderr[:]
            # Read-only second verification deliberately avoids timestamp changes
            # caused by reinstall. It reuses the original immutable source snapshots.
            repeated, after = verify_installed(home, expected)
            if repeated != report["installed"] or before != after:
                raise DiscoveryError(
                    "Same-snapshot verification changed content or lock"
                )
            report["same_snapshot"] = {
                "mode": "read_only_verification",
                "content_unchanged": True,
                "lock_bytes_unchanged": True,
                "lock_sha256": hashlib.sha256(after).hexdigest(),
                "reinstall": "not_run",
            }
            report["status"] = "passed"
    except (DiscoveryError, OSError, subprocess.SubprocessError) as error:
        report["errors"].append(str(error))
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--home", type=Path, required=True, help="Unused direct child of the temp root"
    )
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--codex", default="codex")
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args(argv)
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    report = check_install(args.home, args.codex, args.timeout)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(
        json.dumps(report, indent=2) + "\n", encoding="ascii", newline="\n"
    )
    print(f"Fern install mechanics: {report['status']}; model behavior not run")
    for error in report["errors"]:
        print(f"ERROR: {error}", file=sys.stderr)
    return int(report["status"] != "passed")


if __name__ == "__main__":
    sys.exit(main())
