"""Render README discovery results from source-matched client report artifacts."""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START = b"<!-- agent-support:start -->"
END = b"<!-- agent-support:end -->"
CLIENTS = {"codex": "Codex", "claude-code": "Claude Code"}
SYMBOLS = {"passed": "&#9989;", "failed": "&#10060;", "unknown": "&mdash;"}


def source_hashes(root):
    """Match both probe hash formats without importing either client SDK."""
    directory = root / "skills"
    if not directory.is_dir() or directory.is_symlink():
        raise ValueError("Source skill tree is missing or linked")
    sources = {}
    for skill in sorted(directory.iterdir()):
        if not skill.is_dir():
            continue
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", skill.name):
            raise ValueError("Invalid source skill name")
        entry = skill / "SKILL.md"
        if not entry.is_file():
            raise ValueError("Source skill is missing SKILL.md")
        digest = hashlib.sha256()
        paths = sorted(skill.rglob("*"), key=lambda p: p.relative_to(skill).as_posix())
        for path in [skill, *paths]:
            if path.is_symlink():
                raise ValueError("Source skill contains a link")
            if path.is_file():
                digest.update(path.relative_to(skill).as_posix().encode() + b"\0")
                digest.update(hashlib.sha256(path.read_bytes()).digest())
        data = entry.read_bytes()
        parts = data.decode("utf-8").split("---", 2)
        if len(parts) != 3 or parts[0]:
            raise ValueError("Source skill has invalid frontmatter")
        sources[skill.name] = {
            "source_sha256": digest.hexdigest(),
            "skill_sha256": hashlib.sha256(data).hexdigest(),
            "body_sha256": hashlib.sha256(parts[2].encode()).hexdigest(),
        }
    if not sources:
        raise ValueError("Source skill tree is empty")
    return sources


def valid_run_url(value):
    return isinstance(value, str) and bool(
        re.fullmatch(
            r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/actions/runs/[0-9]+",
            value,
        )
    )


def version_label(client, value):
    """Only publish recognized version text, never arbitrary report strings."""
    patterns = {
        "codex": r"codex-cli [0-9]+\.[0-9]+\.[0-9]+(?:[-+][A-Za-z0-9.-]+)?",
        "claude-code": r"[0-9]+\.[0-9]+\.[0-9]+(?:[-+][A-Za-z0-9.-]+)? \(Claude Code\)",
    }
    if isinstance(value, str) and re.fullmatch(patterns[client], value):
        return f"`{value}`"
    return "unknown version"


def report_results(path, client, channel, revision, run_url, sources):
    unknown = {name: "unknown" for name in sources}

    def warn(reason):
        print(f"{CLIENTS[client]}: {reason}", file=sys.stderr)

    try:
        report = json.loads(path.read_bytes())
    except (OSError, ValueError):
        warn("report missing or unreadable; results unknown")
        return unknown, "unknown version"
    if not isinstance(report, dict) or report.get("client") != client:
        warn("invalid report client; results unknown")
        return unknown, "unknown version"
    version = version_label(client, report.get("client_version"))
    if report.get("channel", channel if not run_url else None) != channel:
        warn("channel mismatch; results unknown")
        return unknown, version
    reported_revision = report.get("source_revision")
    if reported_revision != revision and (reported_revision is not None or run_url):
        warn("source revision mismatch; results unknown")
        return unknown, version
    if run_url and report.get("run_url") != run_url:
        warn("CI run mismatch; results unknown")
        return unknown, version
    status = report.get("status")
    complete = report.get("scan_completed")
    if (
        not isinstance(status, str)
        or status not in {"passed", "failed"}
        or (
            (run_url is not None or "scan_completed" in report)
            and not isinstance(complete, bool)
        )
    ):
        warn("invalid report completion; results unknown")
        return unknown, version
    if complete is False or (complete is not True and status != "passed"):
        warn("scan incomplete; results unknown")
        return unknown, version
    rows = report.get("skills")
    if not isinstance(rows, list) or any(
        not isinstance(row, dict) or not isinstance(row.get("name"), str)
        for row in rows
    ):
        warn("invalid skill entries; results unknown")
        return unknown, version
    grouped = {}
    for row in rows:
        grouped.setdefault(row["name"], []).append(row)
    for name in sources:
        matches = grouped.get(name, [])
        if len(matches) != 1:
            if matches:
                warn(f"{name}: duplicate entries; result unknown")
            continue
        row = matches[0]
        if not isinstance(row.get("status"), str) or row["status"] not in {
            "passed",
            "failed",
        }:
            continue
        keys = ("source_sha256",)
        if client == "claude-code":
            keys += ("skill_sha256", "body_sha256")
        if any(row.get(key) != sources[name][key] for key in keys):
            warn(f"{name}: source hash mismatch; result unknown")
            continue
        unknown[name] = row["status"]
    return unknown, version


def render_support_block(reports, revision, channel="pinned", run_url=None, root=ROOT):
    """Render the selected channel from current source and report provenance."""
    if not isinstance(revision, str) or not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("Revision must be a full lowercase 40-character SHA")
    if channel not in {"pinned", "latest"}:
        raise ValueError("Channel must be pinned or latest")
    if run_url is not None and not valid_run_url(run_url):
        raise ValueError("Run URL must be a GitHub Actions run HTTPS URL")
    sources = source_hashes(root)
    results, versions = {}, {}
    for client in CLIENTS:
        path = reports / f"agent-support-{client}-{channel}" / "agent-support.json"
        results[client], versions[client] = report_results(
            path, client, channel, revision, run_url, sources
        )
    lines = [
        "",
        "",
        "| Skill | Codex | Claude Code |",
        "| --- | --- | --- |",
    ]
    for name in sources:
        cells = [SYMBOLS[results[client][name]] for client in CLIENTS]
        lines.append(f"| [{name}](skills/{name}/README.md) | {' | '.join(cells)} |")
    revision_label = "Tested source commit" if run_url else "Source base commit"
    lines.extend(
        [
            "",
            "&#9989; discovery passed; &#10060; discovery failed; &mdash; unknown.",
            f"Channel: `{channel}`. Versions:",
            f"Codex {versions['codex']}; Claude Code {versions['claude-code']}.",
            f"{revision_label}: `{revision}`.",
        ]
    )
    if run_url:
        lines.append(f"Evidence: [CI run]({run_url}).")
    else:
        lines.append("Evidence: local discovery; hosted CI not run.")
        lines.append("Local evidence covers the current working tree.")
    lines.extend(["", ""])
    return "\n".join(lines)


def update_readme(reports, readme, revision, channel="pinned", run_url=None, root=ROOT):
    """Replace only the unique marked block; return whether bytes changed."""
    original = readme.read_bytes()
    if original.count(START) != 1 or original.count(END) != 1:
        raise ValueError("README must contain one pair of support table markers")
    start, end = original.index(START) + len(START), original.index(END)
    if start > end:
        raise ValueError("README support table markers are reversed")
    block = render_support_block(reports, revision, channel, run_url, root)
    rendered = original[:start] + block.encode("ascii") + original[end:]
    if rendered == original:
        return False
    readme.write_bytes(rendered)
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reports", type=Path, required=True)
    parser.add_argument("--readme", type=Path, default=ROOT / "README.md")
    parser.add_argument("--revision", required=True)
    parser.add_argument("--channel", choices=("pinned", "latest"), default="pinned")
    parser.add_argument("--run-url")
    args = parser.parse_args(argv)
    try:
        update_readme(
            args.reports, args.readme, args.revision, args.channel, args.run_url
        )
    except (OSError, UnicodeError, ValueError):
        print(
            "Support table: invalid input or source; README unchanged", file=sys.stderr
        )
        return 2
    contents = args.readme.read_bytes()
    block = contents.split(START, 1)[1].split(END, 1)[0]
    print(block.decode("ascii").strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
