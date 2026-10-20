"""Plan and run layered repository validation in disposable Docker containers."""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

if __package__ in {None, ""}:
    import check_docker_context
    import run_fern_validation as docker_launcher
    from validation_plan import CHECKS, LAYERS, ROOT, make_plan
else:
    from . import check_docker_context
    from . import run_fern_validation as docker_launcher
    from .validation_plan import CHECKS, LAYERS, ROOT, make_plan


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="ascii", newline="\n")


def aggregate(results):
    statuses = {result["status"] for result in results}
    if statuses - {"passed", "partial", "not_run"}:
        return "failed"
    if not statuses:
        return "not_run"
    return "passed" if statuses == {"passed"} else "partial"


def deadline(entry, timeout, root):
    if entry["check"] == "agent-behavior":
        definitions = json.loads(
            (root / "examples/behavior-smoke.json").read_text("utf-8")
        )["cases"]
        turns = sum(
            len(case["turns"]) + 1
            for case in definitions
            if case["id"] in entry["cases"]
        )
        return max(1, turns) * timeout + 300
    return timeout * (12 if entry["check"] == "checks" else 2) + 300


def run_check(entry, args, output, root):
    is_agent = entry["model_required"]
    if is_agent and not args.run_agent:
        return {
            "id": entry["id"],
            "status": "not_run",
            "reason": "Model execution was not requested; use --run-agent with --model and a CI API credential",
            "cases": entry["cases"],
        }
    if is_agent and (
        not args.model
        or not (os.environ.get("CODEX_API_KEY") or os.environ.get("OPENAI_API_KEY"))
    ):
        return {
            "id": entry["id"],
            "status": "failed",
            "reason": "Requested agent behavior requires --model and CODEX_API_KEY or OPENAI_API_KEY",
            "cases": entry["cases"],
        }
    options = argparse.Namespace(
        output=output,
        suite="behavior" if is_agent else "checks",
        model=args.model if is_agent else None,
        case=entry["cases"],
        timeout=args.timeout,
    )
    arguments = [
        "--check",
        entry["check"],
        "--output",
        "/evidence",
        "--timeout",
        str(args.timeout),
        "--channel",
        entry["channel"],
    ]
    if is_agent:
        arguments += ["--model", args.model]
        for case in entry["cases"]:
            arguments += ["--case", case]
    result = {"id": entry["id"], "status": "failed", "evidence": output.name}
    try:
        if entry["check"] == "docker-context":
            host_report = check_docker_context.run(root, output, args.timeout)
            code = int(host_report.get("status") != "passed")
        else:
            code = docker_launcher.launch(
                options,
                root=root,
                dockerfile="scripts/validation-ci/Dockerfile",
                entrypoint="scripts/validation_ci.py",
                entrypoint_args=arguments,
                target="engines" if entry["check"] == "blender" else "core",
                deadline=deadline(entry, args.timeout, root),
                label="Repository validation",
                all_public=True,
            )
        report = output / "evidence/summary.json"
        if not report.is_file():
            result["reason"] = "Check did not produce the required summary.json"
        else:
            data = json.loads(report.read_text("utf-8"))
            if not isinstance(data, dict):
                raise ValueError("Check report must be an object")
            if data.get("check") != entry["check"]:
                raise ValueError("Report does not match the requested check")
            result["status"] = data.get("status", "failed") if code == 0 else "failed"
            result["summary"] = str(Path(output.name) / "evidence/summary.json")
            result["limits"] = data.get("limits", [])
            if entry["check"] == "docker-context":
                hashes = data.get("source_hashes")
                if not isinstance(hashes, dict) or not hashes:
                    raise ValueError("Docker context report requires source hashes")
                result["source_hashes"] = hashes
            if result["status"] not in {"passed", "partial", "failed", "not_run"}:
                result["status"] = "failed"
                result["reason"] = "Check returned an unknown result status"
            if result["status"] == "not_run":
                result["status"] = "failed"
                result["reason"] = "An explicitly selected check did not run"
        result["exit_code"] = code
    except (
        ValueError,
        OSError,
        subprocess.SubprocessError,
        docker_launcher.LaunchError,
        check_docker_context.ContextError,
    ) as error:
        result["status"] = "failed"
        result["reason"] = str(error)
    return result


def markdown_summary(summary):
    lines = [
        f"## Validation: {summary['layer']} ({summary['status']})",
        "",
        f"Source revision: `{summary['source_revision']}`. Working-tree hashes are in container source manifests or the host check's source_hashes.",
        "",
        "| Check | Status | Evidence / reason |",
        "| --- | --- | --- |",
    ]
    for item in summary["checks"]:
        detail = item.get("reason", item.get("summary", ""))
        lines.append(
            f"| {item['id']} | {item['status']} | {str(detail).replace('|', '/').replace(chr(10), ' ')} |"
        )
    if not summary["checks"]:
        lines += [
            "",
            "No checks apply to this selection; no validation pass is claimed.",
        ]
    gaps = summary["behavior_coverage"]["skills_without_cases"]
    if gaps and summary["layer"] != "pr":
        lines += [
            "",
            "Skills without automated behavior cases: " + ", ".join(gaps) + ".",
        ]
    if summary["manual_evidence"]:
        lines += ["", "Manual evidence remains **not run**:"]
        lines += [
            f"- {item['scope']}: {item['reason']}"
            for item in summary["manual_evidence"]
        ]
    lines += [
        "",
        "A successful command is scoped to the executed checks. It does not certify omitted model, host, engine, visual, or human acceptance.",
    ]
    return "\n".join(lines) + "\n"


def run(args, root=ROOT):
    root = Path(root).resolve()
    output = args.output.expanduser().resolve()
    if output.exists() or output.is_relative_to(root) or root.is_relative_to(output):
        raise ValueError(
            "--output must be a new directory outside and not containing the checkout"
        )
    if args.timeout <= 0:
        raise ValueError("--timeout must be positive")
    if args.model and not args.run_agent:
        raise ValueError("--model requires --run-agent")
    plan = make_plan(
        args.layer,
        root=root,
        base=args.base,
        cases=args.case,
        checks=args.check,
        latest=args.latest,
    )
    if args.run_agent and not any(item["model_required"] for item in plan["checks"]):
        raise ValueError("--run-agent selected no applicable behavior cases")
    output.mkdir(parents=True)
    write_json(output / "plan.json", plan)
    if args.plan_only:
        print(f"Validation plan: {output / 'plan.json'}; no checks executed")
        return 0
    results = []
    snapshot = None
    scoped_hashes = {}
    deterministic_failure = False
    for entry in plan["checks"]:
        directory = output / entry["id"]
        if deterministic_failure:
            result = {
                "id": entry["id"],
                "status": "not_run",
                "reason": "Deterministic checks failed; fix the candidate before expensive validation",
                "cases": entry["cases"],
            }
        else:
            result = run_check(entry, args, directory, root)
        current_hashes = result.get("source_hashes", {})
        manifest = directory / "source-manifest.json"
        if manifest.is_file():
            current = json.loads(manifest.read_text("utf-8"))
            current_hashes = current
            if snapshot is None:
                snapshot = current
                write_json(output / "source-manifest.json", snapshot)
            elif current != snapshot:
                result["status"] = "failed"
                result["reason"] = (
                    "Source changed between check snapshots; rerun a stable candidate"
                )
        if any(
            path in scoped_hashes and scoped_hashes[path] != digest
            for path, digest in current_hashes.items()
        ):
            result["status"] = "failed"
            result["reason"] = (
                "Source changed between check snapshots; rerun a stable candidate"
            )
        scoped_hashes.update(current_hashes)
        results.append(result)
        if entry["check"] == "checks" and result["status"] == "failed":
            deterministic_failure = True
        print(f"{entry['id']}: {result['status']}", flush=True)
    summary = {
        **plan,
        "checks": results,
        "status": aggregate(results),
        "coverage_status": "incomplete"
        if plan["manual_evidence"]
        or (args.layer != "pr" and plan["behavior_coverage"]["skills_without_cases"])
        or any(item["status"] != "passed" for item in results)
        else "complete_for_selected_checks",
    }
    write_json(output / "summary.json", summary)
    text = markdown_summary(summary)
    (output / "summary.md").write_text(text, encoding="ascii", newline="\n")
    print(f"{args.layer}: {summary['status']}; evidence: {output}")
    return int(summary["status"] == "failed")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--layer", choices=LAYERS, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--base",
        help="Affected-layer Git base; includes local staged/unstaged additions",
    )
    parser.add_argument("--check", choices=CHECKS, action="append", default=[])
    parser.add_argument("--case", action="append", default=[])
    parser.add_argument("--latest", action="store_true")
    parser.add_argument("--run-agent", action="store_true")
    parser.add_argument("--model")
    parser.add_argument("--plan-only", action="store_true")
    parser.add_argument("--timeout", type=int, default=600)
    args = parser.parse_args(argv)
    try:
        return run(args)
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        print(f"Validation: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
