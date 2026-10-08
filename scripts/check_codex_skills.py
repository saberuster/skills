"""Check real Codex skill discovery without credentials or model requests."""

import argparse
import contextlib
import hashlib
import json
import os
import queue
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


class DiscoveryError(RuntimeError):
    """An actionable discovery or protocol failure."""


def package_sha256(directory):
    digest = hashlib.sha256()
    for path in [
        directory,
        *sorted(
            directory.rglob("*"), key=lambda p: p.relative_to(directory).as_posix()
        ),
    ]:
        if path.is_symlink():
            raise DiscoveryError(f"Refusing linked skill source: {path}")
        if path.is_file():
            digest.update(
                path.relative_to(directory).as_posix().encode("utf-8") + b"\0"
            )
            digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def discover_expected(repo_root):
    """Read the existing YAML contract, rather than approximate its parser."""
    expected = {}
    sources = [
        p / "SKILL.md" for p in sorted((repo_root / "skills").iterdir()) if p.is_dir()
    ]
    if not sources:
        raise DiscoveryError("No skills/*/SKILL.md sources found")
    for source in sources:
        source_sha256 = package_sha256(source.parent)
        if not source.is_file():
            raise DiscoveryError(f"{source}: missing source SKILL.md")
        text = source.read_text(encoding="utf-8")
        parts = text.split("---", 2)
        if len(parts) != 3 or parts[0] != "":
            raise DiscoveryError(f"{source}: missing YAML frontmatter")
        try:
            metadata = yaml.safe_load(parts[1])
        except yaml.YAMLError as error:
            raise DiscoveryError(f"{source}: invalid YAML: {error}") from error
        if not isinstance(metadata, dict):
            raise DiscoveryError(f"{source}: frontmatter must be a mapping")
        name, description = metadata.get("name"), metadata.get("description")
        if not isinstance(name, str) or name != source.parent.name:
            raise DiscoveryError(f"{source}: name must match its directory")
        if not isinstance(description, str) or not description.strip():
            raise DiscoveryError(f"{source}: description must be a nonempty string")
        if name in expected:
            raise DiscoveryError(f"Duplicate source skill name: {name}")
        expected[name] = {
            "description": description,
            "source": source,
            "source_sha256": source_sha256,
        }
    return expected


def isolated_environment(home):
    """Pass only executable/OS essentials; never inherit tokens or host settings."""
    allowed = {"PATH", "PATHEXT", "SYSTEMROOT", "WINDIR", "COMSPEC"}
    env = {key: value for key, value in os.environ.items() if key.upper() in allowed}
    for name, child in {
        "HOME": ".",
        "USERPROFILE": ".",
        "CODEX_HOME": ".codex",
        "XDG_CONFIG_HOME": ".config",
        "XDG_DATA_HOME": ".local/share",
        "XDG_CACHE_HOME": ".cache",
        "APPDATA": "AppData/Roaming",
        "LOCALAPPDATA": "AppData/Local",
        "TMP": "tmp",
        "TEMP": "tmp",
        "TMPDIR": "tmp",
    }.items():
        destination = home / child
        destination.mkdir(parents=True, exist_ok=True)
        env[name] = str(destination.resolve())
    return env


@contextlib.contextmanager
def isolated_project(repo_root):
    """Copy all complete packages to a disposable project, outside user discovery."""
    with tempfile.TemporaryDirectory(prefix="skill-discovery-") as temporary:
        root = Path(temporary)
        project, home = root / "project", root / "home"
        destination = project / ".agents/skills"
        destination.mkdir(parents=True)
        # Stop ancestor project discovery before it can reach a real checkout.
        (project / ".git").mkdir()
        for source in sorted((repo_root / "skills").iterdir()):
            if source.is_symlink() or any(p.is_symlink() for p in source.rglob("*")):
                raise DiscoveryError(f"Refusing linked skill source: {source}")
            if source.is_dir():
                shutil.copytree(source, destination / source.name)
        home.mkdir()
        yield project.resolve(), home.resolve()


def executable_command(executable, arguments):
    resolved = shutil.which(str(executable))
    if not resolved:
        raise DiscoveryError(f"Codex executable not found: {executable}")
    if os.name == "nt" and Path(resolved).suffix.lower() in {".cmd", ".bat"}:
        return [os.environ.get("COMSPEC", "cmd.exe"), "/d", "/c", resolved, *arguments]
    return [resolved, *arguments]


class JsonLineProcess:
    """Bounded stdio reads with process-tree cleanup, including timeout failures."""

    def __init__(self, command, cwd, env, timeout):
        self.timeout = timeout
        self.messages = queue.Queue()
        self.stderr = []
        options = {"start_new_session": True} if os.name != "nt" else {}
        self.process = subprocess.Popen(
            command,
            cwd=cwd,
            env=env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            **options,
        )
        self.readers = [
            threading.Thread(target=self._read_stdout, daemon=True),
            threading.Thread(target=self._read_stderr, daemon=True),
        ]
        for reader in self.readers:
            reader.start()

    def _read_stdout(self):
        try:
            for line in self.process.stdout:
                self.messages.put(line)
        except (UnicodeError, OSError) as error:
            self.messages.put(DiscoveryError(f"Cannot read server stdout: {error}"))
        finally:
            self.messages.put(None)

    def _read_stderr(self):
        try:
            for line in self.process.stderr:
                if len(self.stderr) < 100:
                    self.stderr.append(line.rstrip())
        except (UnicodeError, OSError):
            pass

    def send(self, message):
        try:
            self.process.stdin.write(json.dumps(message) + "\n")
            self.process.stdin.flush()
        except (BrokenPipeError, OSError) as error:
            raise DiscoveryError(f"Server closed stdin: {error}") from error

    def line(self, deadline):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise DiscoveryError("Timed out waiting for Codex stdout")
        try:
            message = self.messages.get(timeout=remaining)
        except queue.Empty as error:
            raise DiscoveryError("Timed out waiting for Codex stdout") from error
        if isinstance(message, Exception):
            raise message
        if message is None:
            raise DiscoveryError("Codex exited before returning the expected response")
        return message

    def request(self, request_id, method, params):
        self.send({"id": request_id, "method": method, "params": params})
        deadline = time.monotonic() + self.timeout
        while True:
            line = self.line(deadline)
            try:
                if not line.endswith("\n"):
                    raise ValueError("truncated JSON line")
                message = json.loads(line)
            except ValueError as error:
                raise DiscoveryError(
                    f"Malformed response for {method}: {error}"
                ) from error
            if not isinstance(message, dict):
                raise DiscoveryError(
                    f"Malformed response for {method}: expected object"
                )
            if "id" not in message and isinstance(message.get("method"), str):
                continue  # Notifications do not fulfill the outstanding request.
            if message.get("id") != request_id:
                raise DiscoveryError(
                    f"Unexpected response id while waiting for {method}"
                )
            if "error" in message:
                raise DiscoveryError(f"{method} failed: {json.dumps(message['error'])}")
            if not isinstance(message.get("result"), dict):
                raise DiscoveryError(f"{method}: missing object result")
            return message["result"]

    def close(self):
        # Kill the group even after the wrapper exits: a child may still hold pipes.
        if os.name != "nt":
            try:
                os.killpg(self.process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        elif self.process.poll() is None:
            try:
                subprocess.run(
                    ["taskkill", "/PID", str(self.process.pid), "/T", "/F"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=10,
                    check=False,
                )
            except (OSError, subprocess.TimeoutExpired):
                self.process.kill()
        if self.process.poll() is None:
            self.process.kill()
        self.process.wait(timeout=10)
        for reader in self.readers:
            reader.join(timeout=2)
        for stream in (self.process.stdin, self.process.stdout, self.process.stderr):
            stream.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()


def same_path(actual, expected):
    return (
        isinstance(actual, str)
        and Path(actual).is_absolute()
        and (Path(actual).resolve() == expected.resolve())
    )


def verify_discovery(result, expected, project):
    data = result.get("data")
    if not isinstance(data, list) or len(data) != 1 or not isinstance(data[0], dict):
        raise DiscoveryError("skills/list: expected one project entry in data")
    entry = data[0]
    if not same_path(entry.get("cwd"), project):
        raise DiscoveryError("skills/list: cwd does not match the isolated project")
    if not isinstance(entry.get("errors"), list) or not isinstance(
        entry.get("skills"), list
    ):
        raise DiscoveryError("skills/list: missing skills or errors array")
    global_errors, row_load_errors = [], {name: [] for name in expected}
    for error in entry["errors"]:
        message = f"Codex load error: {json.dumps(error)}"
        attributable = next(
            (
                name
                for name in expected
                if isinstance(error, dict)
                and isinstance(error.get("message"), str)
                and same_path(
                    error.get("path"), project / ".agents/skills" / name / "SKILL.md"
                )
            ),
            None,
        )
        if attributable is None:
            global_errors.append(message)
        else:
            row_load_errors[attributable].append(message)
    failures = global_errors[:]
    records, ignored_system = [], []
    for name, source in expected.items():
        matches = [
            s for s in entry["skills"] if isinstance(s, dict) and s.get("name") == name
        ]
        issues = row_load_errors[name][:]
        expected_path = project / ".agents/skills" / name / "SKILL.md"
        # A duplicate may include a leaked user/global source; inspect every match.
        for found in matches:
            if not same_path(found.get("path"), expected_path):
                global_errors.append(
                    f"{name}: path is not the isolated package SKILL.md"
                )
            if found.get("scope") != "repo":
                global_errors.append(f"{name}: skill is not in repo scope")
        if len(matches) != 1:
            issues.append(f"expected one discovery entry, found {len(matches)}")
        else:
            found = matches[0]
            if not same_path(found.get("path"), expected_path):
                issues.append("path is not the isolated package SKILL.md")
            if found.get("description") != source["description"]:
                issues.append("description differs from source frontmatter")
            if found.get("enabled") is not True:
                issues.append("skill is not enabled")
            if found.get("scope") != "repo":
                issues.append("skill is not in repo scope")
        failures.extend(f"{name}: {issue}" for issue in issues)
        records.append(
            {
                "name": name,
                "source": str(source["source"].relative_to(ROOT))
                if source["source"].is_relative_to(ROOT)
                else str(source["source"]),
                "status": "failed" if issues else "passed",
                "source_sha256": source.get("source_sha256"),
                "issues": issues,
                "discovered": matches,
            }
        )
    for found in entry["skills"]:
        if not isinstance(found, dict) or not isinstance(found.get("name"), str):
            failures.append("skills/list: malformed skill entry")
            global_errors.append("skills/list: malformed skill entry")
        elif found["name"] not in expected:
            if found.get("scope") == "system":
                ignored_system.append(found["name"])
            else:
                failures.append(f"Unexpected non-system skill: {found['name']}")
                global_errors.append(f"Unexpected non-system skill: {found['name']}")
    return records, failures, ignored_system, global_errors


def check_codex(repo_root=ROOT, executable="codex", timeout=30):
    report = {
        "client": "codex",
        "check": "skill discovery via app-server skills/list",
        "behavior": "not_run",
        "client_version": None,
        "scan_completed": False,
        "skills": [],
        "errors": [],
    }
    try:
        expected = discover_expected(repo_root)
        report["skills"] = [
            {"name": name, "status": "not_checked"} for name in expected
        ]
        with isolated_project(repo_root) as (project, home):
            env = isolated_environment(home)
            with JsonLineProcess(
                executable_command(executable, ["--version"]), project, env, timeout
            ) as version_process:
                report["client_version"] = version_process.line(
                    time.monotonic() + timeout
                ).strip()
                if version_process.process.wait(timeout=timeout) != 0:
                    raise DiscoveryError("Codex --version failed")
                if not report["client_version"].startswith("codex-cli "):
                    raise DiscoveryError(
                        "Codex --version returned an unrecognized version"
                    )
            command = executable_command(executable, ["app-server", "--stdio"])
            with JsonLineProcess(command, project, env, timeout) as server:
                try:
                    initialized = server.request(
                        1,
                        "initialize",
                        {
                            "clientInfo": {
                                "name": "skill_discovery_ci",
                                "version": "1.0",
                            }
                        },
                    )
                    if not same_path(initialized.get("codexHome"), home / ".codex"):
                        raise DiscoveryError(
                            "initialize: Codex did not use isolated CODEX_HOME"
                        )
                    report["server_user_agent"] = initialized.get("userAgent")
                    server.send({"method": "initialized"})
                    result = server.request(
                        2, "skills/list", {"cwds": [str(project)], "forceReload": True}
                    )
                    records, failures, ignored, global_errors = verify_discovery(
                        result, expected, project
                    )
                    report.update(
                        skills=records, errors=failures, ignored_system_skills=ignored
                    )
                    for record in records:
                        name = record["name"]
                        source = expected[name]
                        staged_hash = package_sha256(project / ".agents/skills" / name)
                        record["staged_sha256"] = staged_hash
                        if (
                            staged_hash != source["source_sha256"]
                            or package_sha256(source["source"].parent)
                            != source["source_sha256"]
                        ):
                            record["status"] = "failed"
                            record["issues"].append("package changed during discovery")
                            failures.append(f"{name}: package changed during discovery")
                    if os.name == "nt" and any(
                        isinstance(skill, dict) and skill.get("scope") == "user"
                        for skill in result["data"][0]["skills"]
                    ):
                        failures.append(
                            "Windows OS-home skill discovery escaped HOME/USERPROFILE "
                            "isolation; run this probe on Linux in an isolated HOME"
                        )
                        global_errors.append(
                            "Windows OS-home discovery escaped isolation"
                        )
                    report["scan_completed"] = not global_errors
                except DiscoveryError:
                    report["server_stderr"] = server.stderr[:]
                    raise
    except (DiscoveryError, OSError, subprocess.SubprocessError) as error:
        report["scan_completed"] = False
        report["errors"].append(str(error))
    report["status"] = "failed" if report["errors"] else "passed"
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--codex", default="codex", help="Codex executable (default: PATH)"
    )
    parser.add_argument("--report", type=Path, help="Write discovery evidence as JSON")
    args = parser.parse_args(argv)
    report = check_codex(executable=args.codex)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(
            json.dumps(report, indent=2) + "\n", encoding="ascii", newline="\n"
        )
    print(
        f"Codex discovery: {report['status']} ({report['client_version'] or 'unknown version'})"
    )
    for skill in report["skills"]:
        print(f"  {skill['name']}: {skill['status']}")
    for failure in report["errors"]:
        print(f"  ERROR: {failure}", file=sys.stderr)
    print("Behavior not run; no turns or model requests")
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
