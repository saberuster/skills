"""Run deterministic regression fixtures on a native Windows CI runner."""

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

from scripts import validation_ci

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_CASES = {
    "test_godot_build_regressions.GodotBuildRegressionTests."
    "test_output_collection_failure_preserves_native_exit_and_evidence": "POSIX inherited-pipe fixture runs in Linux Docker",
    "test_fern_ci.FernRunnerTests."
    "test_negative_control_skill_is_unreadable_to_actual_worker_uid": "Linux container worker UID isolation runs in Linux Docker",
    "test_fern_ci.FernRunnerTests."
    "test_successful_exit_stops_background_writes_before_snapshot": "Linux process-group cleanup runs in Linux Docker",
    "test_fern_ci.FernRunnerTests.test_detached_agent_tools_stop_before_snapshot": "Linux container worker UID and detached-process cleanup run in Linux Docker",
    "test_fern_ci.FernRunnerTests.test_timeout_preserves_partial_evidence_and_terminates": "Linux process-group cleanup runs in Linux Docker",
    "test_fern_ci.FernRunnerTests.test_timeout_closes_pipes_held_by_detached_agent_tool": "Linux container worker UID and detached-process cleanup run in Linux Docker",
    "test_fern_ci.FernRunnerTests."
    "test_agent_invocation_retains_events_and_resumes_with_same_home": "Linux container worker UID and executable shebang fixture run in Linux Docker",
}
REQUIRED_CASES = {
    "test_godot_build_regressions.GodotBuildRegressionTests."
    "test_godot_rejects_windows_junction",
    "test_godot_build_regressions.GodotBuildRegressionTests."
    "test_godot_rejects_directory_and_file_links",
    "test_behavior_trials.BehaviorTrialsTests.test_links_rejected_from_source",
    "test_skill_packages.SkillPackageTests."
    "test_linked_container_is_rejected_before_source_is_read",
    "test_markdown_links.MarkdownLinkTests.test_symlink_escape_is_rejected",
}


def select_suite():
    """Keep every non-engine module and exclude only identified Linux fixtures."""
    discovered = list(validation_ci.cases(validation_ci.selected_suite("checks")))
    identities = [test.id() for test in discovered]
    selected = [test for test in discovered if test.id() not in EXCLUDED_CASES]
    errors = []
    if not selected:
        errors.append("No tests selected")
    if len(identities) != len(set(identities)):
        errors.append("Duplicate discovered test identities")
    for label, expected in (
        ("required", REQUIRED_CASES),
        ("exclusion", EXCLUDED_CASES.keys()),
    ):
        missing = sorted(set(expected) - set(identities))
        if missing:
            errors.append(f"Missing {label} identities: {', '.join(missing)}")
    return unittest.TestSuite(selected), {
        "selected_modules": sorted({test.id().split(".")[0] for test in selected}),
        "selected_cases": [test.id() for test in selected],
        "excluded_cases": [
            {"id": name, "reason": reason, "discovered": name in identities}
            for name, reason in sorted(EXCLUDED_CASES.items())
        ],
        "selection_errors": errors,
    }


def metadata():
    pwsh = shutil.which(os.environ.get("PWSH", "pwsh"))
    if not pwsh:
        raise ValueError("PowerShell 7.2+ is required")
    version = subprocess.run(
        [
            pwsh,
            "-NoLogo",
            "-NoProfile",
            "-Command",
            "$PSVersionTable.PSVersion.ToString()",
        ],
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    ).stdout.strip()
    if tuple(int(part) for part in version.split(".")[:2]) < (7, 2):
        raise ValueError("PowerShell 7.2+ is required")
    revision = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    ).stdout.strip()
    return {
        "source_revision": revision,
        "windows": platform.platform(),
        "python": sys.version,
        "python_executable": sys.executable,
        "powershell": {"path": pwsh, "version": version},
        "runner": {
            name: os.environ.get(name)
            for name in ("RUNNER_OS", "RUNNER_ARCH", "ImageOS", "ImageVersion")
        },
    }


def fresh_output(output):
    """Do not overwrite evidence or write generated files into the source tree."""
    if not output.is_absolute():
        raise ValueError("Output must be an absolute path outside the repository")
    resolved = output.resolve()
    if resolved.is_relative_to(ROOT) or output.exists() or output.is_symlink():
        raise ValueError("Output must be a new directory outside the repository")
    resolved.mkdir(parents=True)
    return resolved


def run(output):
    if sys.platform != "win32":
        raise ValueError("This entrypoint requires native Windows")
    output = fresh_output(output)
    summary = {
        "check": "windows",
        "status": "failed",
        "exit_code": 1,
        "selected_modules": [],
        "selected_cases": [],
        "excluded_cases": [],
        "limits": [
            "Deterministic fixtures only; no real engine or model execution.",
            "These fixtures do not establish native desktop discovery or human acceptance.",
        ],
    }
    with (output / "unittest.log").open("w", encoding="utf-8", newline="\n") as log:
        try:
            summary.update(metadata())
            suite, selection = select_suite()
            summary.update(selection)
            # Run import-error cases as well so their original tracebacks survive.
            report = validation_ci.unittest_report(suite, "windows", stream=log)
            summary["unittest"] = report
            if report["status"] == "passed" and not selection["selection_errors"]:
                summary.update(status="passed", exit_code=0)
        except Exception as error:
            summary["error"] = str(error)
            log.write(f"{type(error).__name__}: {error}\n")
    (output / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    report = summary.get("unittest", {})
    lines = [
        f"## Native Windows regressions: {summary['status']}",
        "",
        f"Exit code: {summary['exit_code']}; tests run: {report.get('testsRun', 0)}; "
        f"counts: {report.get('counts', {})}",
        "",
        "Selected modules: " + (", ".join(summary["selected_modules"]) or "none"),
        "",
        "Source revision: " + summary.get("source_revision", "unavailable"),
        "",
        "Windows: " + summary.get("windows", "unavailable"),
        "Python: " + summary.get("python", "unavailable"),
        "PowerShell: " + json.dumps(summary.get("powershell", {})),
        "Runner image: " + json.dumps(summary.get("runner", {})),
        "",
        *summary["limits"],
        "",
        "Excluded cases (assigned to Linux Docker checks):",
        "",
        *[
            f"- `{row['id']}`: {row['reason']} (discovered: {row['discovered']})"
            for row in summary["excluded_cases"]
        ],
    ]
    for error in summary.get("selection_errors", []) + [summary.get("error")]:
        if error:
            lines.extend(["", "Failure: " + error])
    (output / "summary.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8", newline="\n"
    )
    return summary


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        summary = run(args.output)
    except ValueError as error:
        parser.error(str(error))
    print(f"windows: {summary['status']}", flush=True)
    return summary["exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())
