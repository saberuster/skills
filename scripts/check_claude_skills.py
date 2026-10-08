"""Check Claude Code skill discovery through initialization, without a model turn."""

import argparse
import hashlib
import importlib.metadata
import json
import os
import shutil
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def expected_skills(root):
    """Read source metadata and content hashes, refusing ambiguous skill names."""
    expected = {}
    for directory in sorted((root / "skills").iterdir()):
        if not directory.is_dir():
            continue
        path = directory / "SKILL.md"
        if not path.is_file():
            raise ValueError(f"Skill directory has no SKILL.md: {directory.name}")
        data = path.read_bytes()
        parts = data.decode("utf-8").split("---", 2)
        if len(parts) != 3 or parts[0]:
            raise ValueError(f"Invalid frontmatter: {path}")
        metadata = yaml.safe_load(parts[1])
        if not isinstance(metadata, dict):
            raise ValueError(f"Invalid metadata: {path}")
        name, description = metadata.get("name"), metadata.get("description")
        if name != path.parent.name or name in expected:
            raise ValueError(f"Invalid or duplicate source skill name: {path}")
        if not isinstance(description, str) or not description.strip():
            raise ValueError(f"Empty source description: {path}")
        ui = path.parent / "agents" / "openai.yaml"
        policy = yaml.safe_load(ui.read_text(encoding="utf-8")).get("policy", {})
        package = hashlib.sha256()
        for relative, digest in file_hashes(path.parent).items():
            package.update(relative.encode("utf-8") + b"\0")
            package.update(bytes.fromhex(digest))
        expected[name] = {
            "description": description,
            "source_sha256": package.hexdigest(),
            "skill_sha256": hashlib.sha256(data).hexdigest(),
            "body_sha256": hashlib.sha256(parts[2].encode("utf-8")).hexdigest(),
            "codex_allow_implicit_invocation": policy.get("allow_implicit_invocation"),
        }
    if not expected:
        raise ValueError("No source skills found")
    return expected


def file_hashes(directory):
    result = {}
    for path in sorted(
        directory.rglob("*"), key=lambda item: item.relative_to(directory).as_posix()
    ):
        if path.is_symlink():
            raise ValueError(f"Skill source contains a symlink: {path}")
        if path.is_file():
            result[path.relative_to(directory).as_posix()] = hashlib.sha256(
                path.read_bytes()
            ).hexdigest()
    return result


def copy_skills(root, project, expected):
    """Copy the complete packages and verify every copied byte."""
    for name in expected:
        source = root / "skills" / name
        hashes = file_hashes(source)
        target = project / ".claude" / "skills" / name
        shutil.copytree(source, target)
        if hashes != file_hashes(target):
            raise ValueError(f"Copied package differs from source: {name}")


def isolated_environment(home):
    """Allow runtime paths, but inherit no credentials, Claude settings or hooks."""
    env = {
        key: value
        for key, value in os.environ.items()
        if key.upper() in {"PATH", "SYSTEMROOT", "WINDIR", "COMSPEC", "PATHEXT"}
    }
    for directory in (home, home / "tmp", home / ".claude"):
        directory.mkdir(parents=True, exist_ok=True)
    env.update(
        HOME=str(home),
        USERPROFILE=str(home),
        CLAUDE_CONFIG_DIR=str(home / ".claude"),
        XDG_CONFIG_HOME=str(home / ".config"),
        XDG_CACHE_HOME=str(home / ".cache"),
        APPDATA=str(home / "AppData" / "Roaming"),
        LOCALAPPDATA=str(home / "AppData" / "Local"),
        TMPDIR=str(home / "tmp"),
        TEMP=str(home / "tmp"),
        TMP=str(home / "tmp"),
        DISABLE_TELEMETRY="1",
        DISABLE_ERROR_REPORTING="1",
        DISABLE_AUTOUPDATER="1",
        CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC="1",
    )
    return env


@contextmanager
def process_environment(env):
    """SDK subprocesses merge os.environ, so scrub the current process as well."""
    previous = os.environ.copy()
    os.environ.clear()
    os.environ.update(env)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(previous)


async def initialization_info(options, client_factory=None):
    """An empty SDK connection only initializes; never send a user prompt."""
    if client_factory is None:
        from claude_agent_sdk import ClaudeSDKClient

        client_factory = ClaudeSDKClient
    async with client_factory(options=options) as client:
        return await client.get_server_info()


async def bounded_initialization(options):
    import anyio

    with anyio.fail_after(60):
        return await initialization_info(options)


def verify_commands(info, expected):
    """Require a unique command and the complete source description per skill."""
    skills = [
        {"name": name, **source, "status": "not_checked"}
        for name, source in expected.items()
    ]
    errors = []
    if not isinstance(info, dict) or not isinstance(info.get("commands"), list):
        return skills, ["Initialization response has no commands list"]
    commands = info["commands"]
    if not commands:
        return skills, ["Initialization commands list is empty"]
    by_name = {}
    for command in commands:
        if (
            not isinstance(command, dict)
            or not isinstance(command.get("name"), str)
            or not command["name"]
            or not isinstance(command.get("description"), str)
        ):
            return skills, ["Malformed initialization command"]
        by_name.setdefault(command["name"], []).append(command)
    for row in skills:
        name = row["name"]
        source = expected[name]
        matches = by_name.get(name, [])
        if len(matches) != 1:
            error = f"Expected one command for {name}, found {len(matches)}"
            row.update(status="failed", errors=[error], command_count=len(matches))
            errors.append(error)
            continue
        actual = matches[0]["description"]
        row["observed_description"] = actual
        # Claude Code 2.1.292 adds this scope label in initialization commands.
        if actual not in (source["description"], source["description"] + " (project)"):
            error = f"Discovered description differs from source: {name}: {actual!r}"
            row.update(status="failed", errors=[error])
            errors.append(error)
        else:
            row["status"] = "passed"
    return skills, errors


def cli_executable(override):
    if override:
        resolved = shutil.which(override)
        if not resolved:
            raise ValueError(f"Claude CLI executable not found: {override}")
        return resolved
    import claude_agent_sdk

    # The pinned official SDK ships a CLI, avoiding a user's installation/config.
    executable = "claude.exe" if sys.platform == "win32" else "claude"
    bundled = Path(claude_agent_sdk.__file__).parent / "_bundled" / executable
    if not bundled.is_file():
        raise ValueError("SDK bundled CLI is missing; supply --claude")
    return str(bundled)


def run_discovery(root, claude, expected, report):
    """Collect live initialization evidence, preserving versions before startup."""
    import anyio
    from claude_agent_sdk import ClaudeAgentOptions

    report["sdk_version"] = importlib.metadata.version("claude-agent-sdk")
    executable = cli_executable(claude)
    with tempfile.TemporaryDirectory(prefix="claude-skill-discovery-") as temporary:
        base = Path(temporary)
        project = base / "project"
        project.mkdir()
        copy_skills(root, project, expected)
        env = isolated_environment(base / "home")
        report["client_version"] = subprocess.run(
            [executable, "--version"],
            cwd=project,
            env=env,
            check=True,
            capture_output=True,
            text=True,
            timeout=15,
        ).stdout.strip()
        options = ClaudeAgentOptions(
            cwd=str(project),
            cli_path=executable,
            setting_sources=["project"],
            tools=[],
            mcp_servers={},
            settings=json.dumps({"disableAllHooks": True}),
            extra_args={"strict-mcp-config": None, "no-session-persistence": None},
            env=env,
        )
        with process_environment(env):
            info = anyio.run(bounded_initialization, options)
        # Initialization must not change even the temporary installed packages.
        for name in expected:
            if file_hashes(root / "skills" / name) != file_hashes(
                project / ".claude" / "skills" / name
            ):
                raise ValueError(f"Package changed during initialization: {name}")
    return info


def check(root, claude=None, discovery_runner=None):
    report = {
        "client": "claude-code",
        "client_version": None,
        "sdk_version": None,
        "status": "failed",
        "scan_completed": False,
        "behavior": "not_run",
        "model_turns": 0,
        "skills": [],
        "errors": [],
        "policy_limitations": [
            "Claude Code does not apply agents/openai.yaml policy; Codex "
            "allow_implicit_invocation is source metadata only. Automatic selection "
            "and explicit-invocation restrictions are not verified by this check."
        ],
    }
    try:
        expected = expected_skills(root)
        report["skills"] = [
            {"name": name, **source, "status": "not_checked"}
            for name, source in expected.items()
        ]
        runner = discovery_runner or run_discovery
        info = runner(root, claude, expected, report)
        report["skills"], report["errors"] = verify_commands(info, expected)
        report["scan_completed"] = all(
            row["status"] in {"passed", "failed"} for row in report["skills"]
        )
        if not report["errors"]:
            report["status"] = "passed"
    except Exception as error:
        report["errors"].append(str(error))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--claude", help="Claude CLI executable (default: SDK bundle)")
    parser.add_argument("--report", type=Path, help="Write JSON discovery evidence")
    args = parser.parse_args()
    report = check(ROOT, args.claude)
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered, encoding="ascii", newline="\n")
    print(rendered, end="")
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
