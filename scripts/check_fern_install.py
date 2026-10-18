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
from urllib.parse import urlsplit, urlunsplit

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
SOURCE_FIELDS = (
    "source",
    "sourceType",
    "sourceUrl",
    "ref",
    "skillPath",
    "skillFolderHash",
)

# Match Skills 1.7.0 src/local-lock.ts, including Node's localeCompare order.
# This hashes the trusted snapshot, never the installer record or installed copy.
FALLBACK_HASH_SCRIPT = r"""
const fs = require('node:fs/promises');
const path = require('node:path');
const crypto = require('node:crypto');
async function filesAt(directory, base = '') {
  const files = [];
  for (const entry of await fs.readdir(directory, { withFileTypes: true })) {
    const relativePath = path.join(base, entry.name);
    if (entry.isDirectory()) {
      if (entry.name !== '.git' && entry.name !== 'node_modules') {
        files.push(...await filesAt(path.join(directory, entry.name), relativePath));
      }
    } else if (entry.isFile()) {
      files.push({
        relativePath: relativePath.replace(/\\/g, '/'),
        fullPath: path.join(directory, entry.name),
      });
    }
  }
  return files;
}
(async () => {
  const root = process.argv[1];
  const files = await filesAt(root);
  files.sort((a, b) => a.relativePath.localeCompare(b.relativePath));
  const hash = crypto.createHash('sha256');
  for (const file of files) {
    hash.update(file.relativePath);
    hash.update(await fs.readFile(file.fullPath));
  }
  process.stdout.write(hash.digest('hex'));
})().catch(error => { console.error(error.message); process.exitCode = 1; });
"""


def skills_cli_fallback_sha256(directory, env=None):
    """Compute the exact pinned installer's fallback from trusted source files."""
    try:
        completed = subprocess.run(
            ["node", "-e", FALLBACK_HASH_SCRIPT, str(directory)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
            timeout=60,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as error:
        raise DiscoveryError(
            f"Could not compute Skills 1.7.0 fallback SHA-256 ({type(error).__name__})"
        ) from error
    digest = completed.stdout.strip()
    if completed.returncode or not re.fullmatch(r"[0-9a-f]{64}", digest):
        reason = (
            f"exit {completed.returncode}"
            if completed.returncode
            else "invalid digest output"
        )
        raise DiscoveryError(
            f"Could not compute Skills 1.7.0 fallback SHA-256 ({reason})"
        )
    return digest


def diagnostic_value(value, field=None):
    """Retain scalar provenance only; drop unknown fields and URL credentials."""
    if value is None or isinstance(value, (bool, int)):
        return value
    if not isinstance(value, str):
        return f"<invalid {type(value).__name__}>"
    if field == "sourceUrl":
        try:
            url = urlsplit(value)
            value = urlunsplit((url.scheme, url.hostname or "", url.path, "", ""))
        except ValueError:
            return "<invalid URL>"
    return value[:512]


def inspect_source_lock(home, expected, env=None):
    """Return parsed data plus sanitized diagnostics, even for invalid locks."""
    diagnostics = {"read_status": "missing", "mismatches": []}
    mismatches = diagnostics["mismatches"]
    try:
        lock_bytes = (home / ".agents/.skill-lock.json").read_bytes()
    except OSError as error:
        diagnostics["read_status"] = (
            "missing" if isinstance(error, FileNotFoundError) else "unreadable"
        )
        mismatches.append(
            {
                "field": "lock",
                "expected": "readable JSON",
                "actual": diagnostics["read_status"],
            }
        )
        return None, None, diagnostics
    diagnostics["sha256"] = hashlib.sha256(lock_bytes).hexdigest()
    try:
        lock = json.loads(lock_bytes)
    except (ValueError, UnicodeError):
        diagnostics["read_status"] = "malformed_json"
        mismatches.append(
            {"field": "lock", "expected": "valid JSON", "actual": "malformed_json"}
        )
        return lock_bytes, None, diagnostics
    diagnostics["read_status"] = "parsed"
    if not isinstance(lock, dict):
        mismatches.append(
            {"field": "lock", "expected": "object", "actual": diagnostic_value(lock)}
        )
        return lock_bytes, None, diagnostics
    diagnostics["version"] = diagnostic_value(lock.get("version"))
    if type(lock.get("version")) is not int or lock["version"] != 3:
        mismatches.append(
            {"field": "version", "expected": 3, "actual": diagnostics["version"]}
        )
    entries = lock.get("skills")
    if not isinstance(entries, dict):
        mismatches.append(
            {
                "field": "skills",
                "expected": "object",
                "actual": diagnostic_value(entries),
            }
        )
        return lock_bytes, None, diagnostics
    diagnostics["package_set"] = sorted(diagnostic_value(name) for name in entries)
    diagnostics["expected_package_set"] = sorted(expected)
    if set(entries) != set(expected):
        mismatches.append(
            {
                "field": "skills",
                "expected": sorted(expected),
                "actual": diagnostics["package_set"],
            }
        )
    diagnostics["records"] = {}
    for name, record in entries.items():
        diagnostics["records"][diagnostic_value(name)] = (
            {
                key: diagnostic_value(record[key], key)
                for key in SOURCE_FIELDS
                if key in record
            }
            if isinstance(record, dict)
            else diagnostic_value(record)
        )
    for name, package in expected.items():
        if name not in entries:
            continue
        record = entries[name]
        if not isinstance(record, dict):
            mismatches.append(
                {
                    "skill": name,
                    "field": "record",
                    "expected": "object",
                    "actual": diagnostic_value(record),
                }
            )
            continue
        source = package["source"]
        provenance = {
            "source": source["repository"],
            "sourceType": "github",
            "sourceUrl": source["url"],
            "ref": source["sha"],
            "skillPath": package["skill_path"],
        }
        for field, value in provenance.items():
            if record.get(field) != value:
                mismatches.append(
                    {
                        "skill": name,
                        "field": field,
                        "expected": value,
                        "actual": diagnostic_value(record.get(field), field),
                        "actual_present": field in record,
                    }
                )
        actual_hash = record.get("skillFolderHash")
        accepted = {"git_tree_oid": package["tree_oid"]}
        if actual_hash == package["tree_oid"]:
            algorithm = "git_tree_oid"
        else:
            try:
                accepted["skills_1_7_0_sha256"] = skills_cli_fallback_sha256(
                    package["path"], env
                )
            except DiscoveryError as error:
                diagnostics.setdefault("diagnostic_errors", []).append(
                    f"{name}: {error}"
                )
            algorithm = (
                "skills_1_7_0_sha256"
                if actual_hash == accepted.get("skills_1_7_0_sha256")
                and actual_hash is not None
                else None
            )
        if algorithm is None:
            mismatches.append(
                {
                    "skill": name,
                    "field": "skillFolderHash",
                    "expected": accepted,
                    "actual": diagnostic_value(actual_hash),
                    "actual_present": "skillFolderHash" in record,
                }
            )
        else:
            diagnostics["records"][name]["hash_algorithm"] = algorithm
    return lock_bytes, entries, diagnostics


@contextlib.contextmanager
def installation_home(target, expected, report, env=None):
    """Capture lock evidence before cleanup without masking the primary failure."""
    with disposable_home(target) as (temporary, home):
        try:
            yield temporary, home
        finally:
            if "source_lock" not in report:
                try:
                    report["source_lock"] = inspect_source_lock(home, expected, env)[2]
                except Exception as error:
                    # Evidence collection must not replace the primary error.
                    report["source_lock"] = {
                        "read_status": "diagnostic_error",
                        "error_type": type(error).__name__,
                    }


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


def verify_installed(home, expected, env=None, report=None):
    lock_bytes, _entries, diagnostics = inspect_source_lock(home, expected, env)
    if report is not None:
        report["source_lock"] = diagnostics
    if diagnostics["mismatches"]:
        fields = ", ".join(
            f"{row['skill']}.{row['field']}" if "skill" in row else row["field"]
            for row in diagnostics["mismatches"]
        )
        raise DiscoveryError(f"Installer source provenance mismatch: {fields}")
    rows = []
    for name, package in expected.items():
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
        source_record = diagnostics["records"][name].copy()
        algorithm = source_record.pop("hash_algorithm")
        rows.append(
            {
                "name": name,
                "sha256": hashes,
                "source_record": source_record,
                "source_hash_algorithm": algorithm,
            }
        )
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
        expected = {}
        env = {}
        with installation_home(home_target, expected, report, env) as (temporary, home):
            report["disposable_home"] = str(home)
            env.update(isolated_environment(home))
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
            report["installed"], before = verify_installed(home, expected, env, report)
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
            repeated, after = verify_installed(home, expected, env, report)
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
