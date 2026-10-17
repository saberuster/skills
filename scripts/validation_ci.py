"""Run repository validation inside a disposable Linux Docker container."""

import argparse
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

if __package__ in {None, ""}:
    import fern_ci
else:
    from . import fern_ci

ROOT = Path(__file__).resolve().parents[1]
CHECKS = (
    "checks",
    "codex-discovery",
    "claude-discovery",
    "fern-install",
    "blender",
    "agent-behavior",
)
BLENDER_MODULES = {
    "test_scene_blender_integration",
    "test_low_poly_blender_integration",
}
PLATFORM_SKIPS = {
    (
        "test_godot_build_regressions.GodotBuildRegressionTests.test_godot_rejects_windows_junction",
        "Windows junction behavior requires Windows",
    )
}


def cases(suite):
    """Flatten discovery without losing import-error test cases."""
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from cases(item)
        else:
            yield item


def selected_suite(kind, root=ROOT):
    selected = unittest.TestSuite()
    for module in sorted((root / "tests").glob("test_*.py")):
        if (module.stem in BLENDER_MODULES) == (kind == "blender"):
            # Select before importing so broken engine-only imports cannot affect
            # the dependency-free suite or hide a Blender import error.
            selected.addTests(
                unittest.TestLoader().discover(str(root / "tests"), pattern=module.name)
            )
    return selected


def unittest_report(suite, kind, stream=None):
    """Report actual execution and reject unexpected skips or empty selections."""
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    skipped = [{"id": test.id(), "reason": reason} for test, reason in result.skipped]
    unexpected_skips = [
        row
        for row in skipped
        if kind != "checks" or (row["id"], row["reason"]) not in PLATFORM_SKIPS
    ]
    errors = [{"id": test.id(), "traceback": detail} for test, detail in result.errors]
    failures = [
        {"id": test.id(), "traceback": detail} for test, detail in result.failures
    ]
    unexpected_successes = [test.id() for test in result.unexpectedSuccesses]
    failed = (
        not result.testsRun
        or not result.wasSuccessful()
        or bool(unexpected_skips)
        or bool(result.expectedFailures)
    )
    return {
        "status": "failed" if failed else "partial" if skipped else "passed",
        "testsRun": result.testsRun,
        "errors": errors,
        "failures": failures,
        "skipped": skipped,
        "unexpected_skips": unexpected_skips,
        "unexpected_successes": unexpected_successes,
        "expected_failures": [
            {"id": test.id(), "traceback": detail}
            for test, detail in result.expectedFailures
        ],
        "counts": {
            "errors": len(errors),
            "failures": len(failures),
            "skipped": len(skipped),
            "expected_failures": len(result.expectedFailures),
        },
        "selection_error": "No tests selected" if not result.testsRun else None,
    }


def command_plan(check, output, timeout):
    """Keep exact delegated interfaces inspectable without launching clients."""
    python = sys.executable
    if check == "checks":
        return [
            [python, "-m", "ruff", "check", "."],
            [python, "-m", "ruff", "format", "--check", "."],
            ["npm", "run", "lint:md"],
            [
                python,
                "-m",
                "scripts.validation_ci",
                "--check",
                check,
                "--unittest-report",
                str(output / "unittest.json"),
            ],
        ]
    if check == "blender":
        return [
            [
                python,
                "-m",
                "scripts.validation_ci",
                "--check",
                check,
                "--unittest-report",
                str(output / "unittest.json"),
            ]
        ]
    if check in {"codex-discovery", "claude-discovery"}:
        client = check.split("-")[0]
        return [
            [
                python,
                f"scripts/check_{client}_skills.py",
                "--report",
                str(output / "discovery.json"),
            ]
        ]
    if check == "fern-install":
        return [
            [
                python,
                "scripts/check_fern_install.py",
                "--home",
                str(Path(tempfile.gettempdir()) / "validation-fern-install-target"),
                "--report",
                str(output / "install.json"),
                "--timeout",
                str(timeout),
            ]
        ]
    raise ValueError(f"No command plan for {check}")


def latest_command(check):
    if check == "codex-discovery":
        return ["npm", "install", "--global", "@openai/codex@latest"]
    if check == "claude-discovery":
        return [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--upgrade",
            "claude-agent-sdk",
        ]
    raise ValueError("The latest channel is only supported by client discovery checks")


def execute(command, output, index, timeout):
    result = fern_ci.run_process(command, ROOT, os.environ.copy(), timeout)
    fern_ci.write_json(output / f"process-{index}.json", result)
    passed = (
        result["returncode"] == 0
        and not result["timed_out"]
        and not result["cleanup_error"]
    )
    return {
        "command": command,
        "status": "passed" if passed else "failed",
        "returncode": result["returncode"],
        "timed_out": result["timed_out"],
        "cleanup_error": result["cleanup_error"],
        "evidence": f"process-{index}.json",
    }


def prerequisites(check):
    if check == "checks" and not shutil.which(os.environ.get("PWSH", "pwsh")):
        raise ValueError("PowerShell 7.2+ is required for Godot helper regressions")
    if check == "blender":
        blender = Path(os.environ.get("BLENDER", ""))
        if not blender.is_file() or not os.access(blender, os.X_OK):
            raise ValueError(
                "BLENDER must name the installed executable; use engines target"
            )


def run(check, output, timeout, channel="pinned", model=None, selected_cases=None):
    summary = {
        "check": check,
        "channel": channel,
        "source_revision": os.environ.get("SOURCE_REVISION"),
        "status": "failed",
        "results": [],
        "limits": [
            "Results describe only executed checks and the recorded source snapshot.",
            "Discovery and scripted regressions do not validate model decisions.",
            "Blender background fixtures do not establish visual or human acceptance.",
        ],
        "model_requests": check == "agent-behavior",
    }
    try:
        prerequisites(check)
        if channel == "latest":
            upgrade = execute(latest_command(check), output, "upgrade", timeout)
            summary["results"].append(upgrade)
            if upgrade["status"] != "passed":
                return summary
        if check == "agent-behavior":
            if not selected_cases:
                raise ValueError("Select at least one agent behavior case explicitly")
            behavior = fern_ci.run_behavior(
                output, model, selected_cases, timeout, all_skills=True
            )
            summary["results"].append(behavior)
            summary["status"] = (
                "passed" if behavior.get("status") == "passed" else "failed"
            )
            return summary
        for index, command in enumerate(command_plan(check, output, timeout), 1):
            summary["results"].append(execute(command, output, index, timeout))
        if any(row["status"] != "passed" for row in summary["results"]):
            return summary
        report_name = (
            "unittest.json"
            if check in {"checks", "blender"}
            else "install.json"
            if check == "fern-install"
            else "discovery.json"
        )
        report = json.loads((output / report_name).read_text(encoding="utf-8"))
        summary["results"].append({"evidence": report_name, **report})
        summary["status"] = (
            report["status"]
            if report.get("status") in {"passed", "partial"}
            else "failed"
        )
        if summary["status"] == "partial":
            summary["limits"].append(
                "Windows junction behavior was not run in this Linux container."
            )
    except Exception as error:
        summary["error"] = fern_ci.redact(str(error))
    return summary


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", choices=CHECKS, required=True)
    parser.add_argument("--output", type=Path, default=Path("/evidence"))
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--channel", choices=["pinned", "latest"], default="pinned")
    parser.add_argument("--model")
    parser.add_argument("--case", action="append", default=[])
    parser.add_argument("--unittest-report", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if (
        sys.platform != "linux"
        or not Path("/.dockerenv").is_file()
        or os.getuid() != 0
        or os.environ.get("FERN_VALIDATION_CONTAINER") != "1"
    ):
        parser.error(
            "This entrypoint requires a disposable root Linux Docker container"
        )
    if args.timeout <= 0 or args.output != Path("/evidence"):
        parser.error("Use /evidence and a positive timeout")
    args.output.mkdir(exist_ok=True)
    if args.unittest_report:
        if (
            args.check not in {"checks", "blender"}
            or args.unittest_report != args.output / "unittest.json"
        ):
            parser.error("Invalid internal unittest report selection")
        report = unittest_report(selected_suite(args.check), args.check)
        fern_ci.write_json(args.unittest_report, report)
        return int(report["status"] == "failed")
    summary = run(
        args.check, args.output, args.timeout, args.channel, args.model, args.case
    )
    fern_ci.write_json(args.output / "summary.json", summary)
    fern_ci.scrub_artifacts(args.output)
    print(f"{args.check}: {summary['status']}", flush=True)
    return int(summary["status"] not in {"passed", "partial"})


if __name__ == "__main__":
    raise SystemExit(main())
