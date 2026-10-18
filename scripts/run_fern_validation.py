"""Run Fern validation in Docker without exposing host homes or source mounts."""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIRECTORIES = {"skills", "docs", "examples", "scripts", "tests", ".github"}
SOURCE_FILES = {
    "AGENTS.md",
    "README.md",
    "CHANGELOG.md",
    "LICENSE",
    ".gitignore",
    ".markdownlint-cli2.jsonc",
    "package.json",
    "package-lock.json",
    "requirements-dev.txt",
    "requirements-agent-ci.txt",
    "ruff.toml",
}
EXCLUDED_PARTS = {
    ".git",
    ".venv",
    "node_modules",
    "__pycache__",
    ".ruff_cache",
    ".codex",
    ".agents",
    ".claude",
    ".aws",
    ".ssh",
}
SECRET_NAMES = {"auth.json", "credentials", "credentials.json", ".netrc", ".npmrc"}


class LaunchError(Exception):
    """A host prerequisite or container operation failed."""


def allowed_source(relative, *, all_public=False):
    """Allow public source trees and explicit root metadata only."""
    parts = relative.parts
    if parts == (".agents", "plugins", "marketplace.json"):
        return True
    return (
        bool(parts)
        and (
            all_public
            or (len(parts) == 1 and relative.name in SOURCE_FILES)
            or (len(parts) > 1 and parts[0] in SOURCE_DIRECTORIES)
        )
        and not any(
            part.lower() in EXCLUDED_PARTS
            or part.lower() in SECRET_NAMES
            or part.lower().startswith(".env")
            or part.lower().endswith((".pem", ".key", ".pyc", ".pyo"))
            for part in parts
        )
    )


def stage_source(root, destination, *, all_public=False):
    """Copy indexed/unignored source files, never the checkout's Git database."""
    listing = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    for name in set(os.fsdecode(listing.stdout).split("\0")) - {""}:
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts:
            raise LaunchError("Git returned a path outside the source checkout")
        if not allowed_source(relative, all_public=all_public):
            continue
        source = root / relative
        if not source.exists():
            continue  # Indexed files can have pending deletions.
        if any(path.is_symlink() for path in [source, *source.parents]):
            raise LaunchError(f"Source symlinks are not supported: {relative}")
        if not source.resolve().is_relative_to(root.resolve()) or not source.is_file():
            raise LaunchError(f"Source is not a regular checkout file: {relative}")
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)


def validate_options(args, root, environment):
    output = args.output.expanduser().resolve()
    if output.exists():
        raise LaunchError("--output must name a new, nonexistent directory")
    if output.is_relative_to(root.resolve()):
        raise LaunchError("--output must be outside the source checkout")
    if args.timeout <= 0:
        raise LaunchError("--timeout must be positive")
    if args.suite != "behavior" and (args.model or args.case):
        raise LaunchError("--model and --case apply only to the behavior suite")
    if args.suite == "behavior":
        if not args.model or not args.model.strip():
            raise LaunchError("Behavior validation requires an explicit --model")
        if not (environment.get("CODEX_API_KEY") or environment.get("OPENAI_API_KEY")):
            raise LaunchError(
                "Behavior validation requires CODEX_API_KEY or OPENAI_API_KEY"
            )
    return output


def container_deadline(args, source):
    if args.suite == "checks":
        slots = 10
    elif args.suite == "install":
        slots = 1
    else:
        spec = json.loads((source / "examples/behavior-smoke.json").read_text("utf-8"))
        cases = [case for case in spec["cases"] if case["skill"] == "setup-fern"]
        if args.case:
            cases = [case for case in cases if case["id"] in args.case]
        slots = sum(len(case["turns"]) + 1 for case in cases)
    return max(1, slots) * args.timeout + 300


def launch(
    args,
    root=ROOT,
    *,
    dockerfile="scripts/fern-ci/Dockerfile",
    entrypoint="scripts/fern_ci.py",
    entrypoint_args=None,
    target=None,
    deadline=None,
    label="Fern",
    all_public=False,
):
    environment = os.environ.copy()
    output = validate_options(args, root, environment)
    if shutil.which("docker") is None:
        raise LaunchError(
            "Docker is required; install and start Docker before validation"
        )
    if args.suite == "behavior":
        environment["CODEX_API_KEY"] = (
            environment.get("CODEX_API_KEY") or environment["OPENAI_API_KEY"]
        )
    else:
        environment.pop("CODEX_API_KEY", None)
    environment.pop("OPENAI_API_KEY", None)
    revision = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    output.mkdir(parents=True)
    evidence = output / "evidence"
    evidence.mkdir()
    image = "fern-validation:" + uuid.uuid4().hex
    container = "fern-validation-" + uuid.uuid4().hex
    record = {
        "suite": args.suite,
        "source_revision": revision,
        "source_snapshot": "working tree public source (indexed and unignored files)",
        "model": args.model,
        "cases": args.case,
        "status": "failed",
        "exit_code": 1,
    }
    created = False
    built = False

    def docker(arguments, log_name, timeout=120, check=True):
        with (output / log_name).open("ab") as log:
            result = subprocess.run(
                ["docker", *arguments],
                env=environment,
                stdout=log,
                stderr=subprocess.STDOUT,
                timeout=timeout,
                check=False,
            )
        if check and result.returncode:
            raise LaunchError(f"Docker operation failed; see {log_name}")
        return result

    try:
        with tempfile.TemporaryDirectory(prefix="fern-docker-context-") as temporary:
            context = Path(temporary)
            stage_source(root, context, all_public=all_public)
            manifest = {
                path.relative_to(context).as_posix(): hashlib.sha256(
                    path.read_bytes()
                ).hexdigest()
                for path in sorted(context.rglob("*"))
                if path.is_file()
            }
            (output / "source-manifest.json").write_text(
                json.dumps(manifest, indent=2) + "\n", encoding="ascii"
            )
            deadline = deadline or container_deadline(args, context)
            build_options = ["--target", target] if target else []
            docker(
                [
                    "build",
                    "--file",
                    str(context / dockerfile),
                    "--tag",
                    image,
                    *build_options,
                    str(context),
                ],
                "docker-build.log",
                timeout=1200,
            )
            built = True
        command = [
            "create",
            "--name",
            container,
            "--init",
            "--security-opt",
            "no-new-privileges",
            "--pids-limit",
            "512",
            "--memory",
            "4g",
            "--env",
            f"SOURCE_REVISION={revision}",
        ]
        if args.suite == "behavior":
            command.extend(["--env", "CODEX_API_KEY"])
        arguments = entrypoint_args
        if arguments is None:
            arguments = [
                "--suite",
                args.suite,
                "--output",
                "/evidence",
                "--timeout",
                str(args.timeout),
            ]
            if args.model:
                arguments.extend(["--model", args.model])
            for case in args.case:
                arguments.extend(["--case", case])
        command.extend([image, "python", entrypoint, *arguments])
        # A fixed generated name also permits cleanup if create fails midway.
        created = True
        docker(command, "docker-create.log")
        docker(["start", container], "docker-start.log")
        try:
            docker(
                ["wait", container],
                "docker-wait.log",
                timeout=deadline,
            )
        except subprocess.TimeoutExpired:
            record["error"] = "Container exceeded the host deadline"
            docker(["kill", container], "docker-cleanup.log", check=False)
            raise LaunchError(record["error"]) from None
        wait_output = (output / "docker-wait.log").read_text(encoding="utf-8").strip()
        try:
            exit_code = int(wait_output)
        except ValueError:
            raise LaunchError(
                "Docker returned an invalid container exit status"
            ) from None
        record["exit_code"] = exit_code
        record["status"] = "passed" if exit_code == 0 else "failed"
    except (LaunchError, OSError, subprocess.SubprocessError) as error:
        record["error"] = str(error)
    finally:
        if created:
            # Keep untrusted container artifacts away from host log paths.
            try:
                docker(["logs", container], "container.log", check=False)
            except (OSError, subprocess.SubprocessError) as error:
                record["log_collection_error"] = str(error)
            try:
                copied = docker(
                    ["cp", f"{container}:/evidence/.", str(evidence)],
                    "docker-copy.log",
                    check=False,
                )
                if copied.returncode:
                    record["evidence_copy_failed"] = True
                    record["exit_code"] = record["exit_code"] or 1
                    record["status"] = "failed"
            except (OSError, subprocess.SubprocessError) as error:
                record["cleanup_error"] = str(error)
                record["status"] = "failed"
                record["exit_code"] = record["exit_code"] or 1
            finally:
                try:
                    removed = docker(
                        ["rm", "--force", container], "docker-cleanup.log", check=False
                    )
                    if removed.returncode:
                        raise LaunchError(
                            "Container cleanup failed; see docker-cleanup.log"
                        )
                except (LaunchError, OSError, subprocess.SubprocessError) as error:
                    record["container_cleanup_error"] = str(error)
                    record["status"] = "failed"
                    record["exit_code"] = record["exit_code"] or 1
        if built:
            try:
                docker(["image", "rm", image], "docker-cleanup.log", check=False)
            except (OSError, subprocess.SubprocessError) as error:
                record["image_cleanup_error"] = str(error)
        secret = environment.get("CODEX_API_KEY")
        if secret:
            for log in output.glob("*.log"):
                log.write_bytes(
                    log.read_bytes().replace(secret.encode(), b"[REDACTED]")
                )
        (output / "launcher.json").write_text(
            json.dumps(record, indent=2) + "\n", encoding="utf-8"
        )
    print(f"{label} {args.suite}: {record['status']}; evidence: {output}")
    return 0 if record["exit_code"] == 0 else 1


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--suite", choices=("checks", "install", "behavior"), required=True
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model")
    parser.add_argument("--case", action="append", default=[])
    parser.add_argument("--timeout", type=int, default=600)
    args = parser.parse_args(argv)
    try:
        return launch(args)
    except (LaunchError, OSError, subprocess.SubprocessError) as error:
        print(f"Fern validation: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
