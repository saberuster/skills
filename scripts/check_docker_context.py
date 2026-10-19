"""Exercise checked-in Docker context filters with disposable synthetic files."""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import uuid
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
FILTERS = (
    "scripts/fern-ci/Dockerfile.dockerignore",
    "scripts/validation-ci/Dockerfile.dockerignore",
)
MARKETPLACE = ".agents/plugins/marketplace.json"
DECOYS = (
    ".agents/private.txt",
    ".agents/plugins/private.txt",
    ".agents/plugins/marketplace.json.backup",
    ".agents/skills/private/SKILL.md",
    "skills/fixture/.agents/plugins/marketplace.json",
    "docs/fixture/.agents/private.txt",
    "scripts/fixture/.agents/plugins/marketplace.json",
)


class ContextError(Exception):
    """The fixture, Docker operation, or exported filesystem is invalid."""


def source_bytes(root):
    """Read only the public inputs used by this check, rejecting source links."""
    result = {}
    for name in (*FILTERS, MARKETPLACE):
        source = root / name
        if any(item.is_symlink() for item in (source, *source.parents)):
            raise ContextError(f"Source symlinks are not supported: {name}")
        if not source.resolve().is_relative_to(root) or not source.is_file():
            raise ContextError(f"Missing regular public source file: {name}")
        result[name] = source.read_bytes()
    return result


def hashes(inputs):
    return {name: hashlib.sha256(data).hexdigest() for name, data in inputs.items()}


def inspect_archive(archive, expected):
    """Check tar members in place; never extract container files onto the host."""
    found = False
    agent_members = []
    with tarfile.open(archive, "r:*") as exported:
        for member in exported:
            name = member.name
            while name.startswith("./"):
                name = name[2:]
            path = PurePosixPath(name)
            if path.is_absolute() or ".." in path.parts or "\\" in name:
                raise ContextError("Export contains an unsafe filesystem path")
            if ".agents" not in path.parts:
                continue
            normalized = path.as_posix()
            agent_members.append(normalized)
            if normalized in (".agents", ".agents/plugins") and member.isdir():
                continue
            if normalized != MARKETPLACE or not member.isfile() or found:
                raise ContextError(f"Excluded .agents member survived: {normalized}")
            stream = exported.extractfile(member)
            if stream is None or stream.read() != expected:
                raise ContextError("Marketplace bytes changed in the Docker context")
            found = True
    if not found:
        raise ContextError("Public marketplace is missing from the Docker context")
    return {"marketplace_bytes_match": True, "agents_members": agent_members}


def run(root: Path, output: Path, timeout: int) -> dict:
    """Build/export both scratch fixtures and retain their logs and source hashes."""
    root = root.expanduser().resolve()
    output = output.expanduser().resolve()
    if output.exists():
        raise ContextError("--output must name a new, nonexistent directory")
    if output.is_relative_to(root) or root.is_relative_to(output):
        raise ContextError("--output must be outside and not contain the checkout")
    if timeout <= 0:
        raise ContextError("--timeout must be positive")
    output.mkdir(parents=True)
    evidence = output / "evidence"
    evidence.mkdir()
    report = {
        "check": "docker-context",
        "status": "failed",
        "source_hashes": {},
        "fixtures": [],
        "limits": [
            "Synthetic Docker filter coverage; no user profile or real secrets used.",
            "Does not establish plugin loading, skill behavior, or host parity.",
        ],
    }
    environment = os.environ.copy()
    environment.pop("CODEX_API_KEY", None)
    environment.pop("OPENAI_API_KEY", None)

    def command(arguments, directory, record, *, cleanup=False):
        commands = record["cleanup"] if cleanup else record["commands"]
        log = directory / f"{'cleanup' if cleanup else 'command'}-{len(commands)}.log"
        entry = {"command": ["docker", *arguments], "log": str(log.relative_to(output))}
        commands.append(entry)
        try:
            with log.open("wb") as stream:
                process = subprocess.run(
                    entry["command"],
                    cwd=directory,
                    env=environment,
                    stdout=stream,
                    stderr=subprocess.STDOUT,
                    timeout=timeout,
                    check=False,
                )
            entry["exit_code"] = process.returncode
            entry["timed_out"] = False
            if process.returncode:
                raise ContextError(f"Docker operation failed; see {entry['log']}")
        except (OSError, subprocess.SubprocessError, ContextError) as error:
            entry["error"] = str(error)
            entry.setdefault("exit_code", None)
            entry["timed_out"] = isinstance(error, subprocess.TimeoutExpired)
            raise ContextError(entry["error"]) from error

    inputs = None
    try:
        inputs = source_bytes(root)
        report["source_hashes"] = hashes(inputs)
        if shutil.which("docker") is None:
            raise ContextError("Docker is required; install and start Docker")
        for index, filter_name in enumerate(FILTERS):
            directory = output / f"fixture-{index}"
            context = directory / "context"
            context.mkdir(parents=True)
            record = {
                "filter": filter_name,
                "status": "failed",
                "commands": [],
                "cleanup": [],
            }
            report["fixtures"].append(record)
            image = "docker-context-fixture:" + uuid.uuid4().hex
            container = "docker-context-fixture-" + uuid.uuid4().hex
            build_attempted = False
            create_attempted = False
            try:
                files = {MARKETPLACE: inputs[MARKETPLACE]}
                files.update({name: b"synthetic excluded fixture\n" for name in DECOYS})
                files["README.md"] = b"synthetic public fixture\n"
                dockerfile = filter_name.removesuffix(".dockerignore")
                files[dockerfile] = b"FROM scratch\nCOPY . /\n"
                files[filter_name] = inputs[filter_name]
                for name, data in files.items():
                    target = context / name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(data)
                build_attempted = True
                command(
                    [
                        "build",
                        "--file",
                        str(context / dockerfile),
                        "--tag",
                        image,
                        str(context),
                    ],
                    directory,
                    record,
                )
                create_attempted = True
                command(
                    ["create", "--name", container, image, "/never-run"],
                    directory,
                    record,
                )
                archive = directory / "filesystem.tar"
                command(
                    ["export", "--output", str(archive), container], directory, record
                )
                record.update(inspect_archive(archive, inputs[MARKETPLACE]))
                record["status"] = "passed"
            except (ContextError, OSError, tarfile.TarError) as error:
                record["error"] = str(error)
            finally:
                operations = []
                if create_attempted:
                    operations.append(["rm", "--force", container])
                if build_attempted:
                    operations.append(["image", "rm", "--force", image])
                for operation in operations:
                    try:
                        command(operation, directory, record, cleanup=True)
                    except ContextError:
                        record["status"] = "failed"
                        record["cleanup_failed"] = True
        if len(report["fixtures"]) == len(FILTERS) and all(
            item["status"] == "passed" for item in report["fixtures"]
        ):
            report["status"] = "passed"
    except (ContextError, OSError) as error:
        report["error"] = str(error)
    finally:
        if inputs is not None:
            try:
                report["final_source_hashes"] = hashes(source_bytes(root))
                if report["final_source_hashes"] != report["source_hashes"]:
                    raise ContextError(
                        "Public Docker fixture inputs changed during validation"
                    )
            except (ContextError, OSError) as error:
                report["status"] = "failed"
                report["error"] = str(error)
        (evidence / "summary.json").write_text(
            json.dumps(report, indent=2) + "\n", encoding="utf-8"
        )
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=600)
    args = parser.parse_args(argv)
    try:
        report = run(args.source, args.output, args.timeout)
    except (ContextError, OSError) as error:
        print(f"Docker context validation: {error}", file=sys.stderr)
        return 1
    print(f"Docker context validation: {report['status']}; evidence: {args.output}")
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
