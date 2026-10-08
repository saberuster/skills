"""Source-bound table generation with synthetic reports, never client calls."""

import copy
import hashlib
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from scripts.update_agent_support import (
    END,
    START,
    main,
    render_support_block,
    source_hashes,
    update_readme,
)

REVISION = "a" * 40
RUN_URL = "https://github.com/example/skills/actions/runs/123"


class SupportTableTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.reports = self.root / "reports"
        self.readme = self.root / "README.md"
        self.before = b"# Synthetic README\n\nKeep this prose.\n\n" + START
        self.after = END + b"\n\nKeep this suffix too.\n"
        self.readme.write_bytes(self.before + b"\nold table\n" + self.after)
        for name in ("alpha", "beta"):
            source = self.root / "skills" / name / "SKILL.md"
            source.parent.mkdir(parents=True)
            source.write_bytes(
                f"---\nname: {name}\ndescription: Synthetic.\n---\nInstructions.\n".encode()
            )
            (source.parent / "resource.txt").write_bytes(b"Resource.\n")
        hashes = source_hashes(self.root)
        self.codex = self.report("codex", hashes, "codex-cli 0.133.0")
        self.claude = self.report("claude-code", hashes, "2.1.292 (Claude Code)")
        self.write_report(self.codex)
        self.write_report(self.claude)

    def report(self, client, hashes, version):
        return {
            "client": client,
            "client_version": version,
            "channel": "pinned",
            "source_revision": REVISION,
            "run_url": RUN_URL,
            "scan_completed": True,
            "status": "passed",
            "skills": [
                {"name": name, "status": "passed", **values}
                for name, values in hashes.items()
            ],
        }

    def write_report(self, report, channel="pinned", client=None):
        path = (
            self.reports
            / f"agent-support-{client or report['client']}-{channel}"
            / "agent-support.json"
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report), encoding="ascii", newline="\n")
        return path

    def render(self, channel="pinned", run_url=RUN_URL):
        with redirect_stderr(io.StringIO()):
            return render_support_block(
                self.reports, REVISION, channel, run_url, self.root
            )

    def row(self, rendered, name="alpha"):
        return next(line for line in rendered.splitlines() if f"[{name}]" in line)

    def test_mixed_results_survive_overall_failure(self):
        self.codex["status"] = "failed"
        self.codex["skills"][0]["status"] = "failed"
        self.write_report(self.codex)
        rendered = self.render()
        self.assertTrue(self.row(rendered).endswith("| &#10060; | &#9989; |"))
        self.assertTrue(self.row(rendered, "beta").endswith("| &#9989; | &#9989; |"))
        self.assertIn("`codex-cli 0.133.0`", rendered)
        self.assertIn("`2.1.292 (Claude Code)`", rendered)
        self.assertIn(REVISION, rendered)
        self.assertIn(f"[CI run]({RUN_URL})", rendered)

    def test_global_failure_cannot_publish_partial_success(self):
        for status in ("passed", "failed"):
            with self.subTest(status=status):
                self.codex.update(scan_completed=False, status=status)
                self.write_report(self.codex)
                self.assertTrue(
                    self.row(self.render()).endswith("| &mdash; | &#9989; |")
                )
        self.codex.pop("scan_completed")
        self.write_report(self.codex)
        self.assertIn("| &mdash; | &#9989; |", self.row(self.render()))

    def test_missing_client_report_and_missing_or_unchecked_rows(self):
        self.write_report(self.codex).unlink()
        self.claude["skills"] = [{**self.claude["skills"][0], "status": "not_checked"}]
        self.write_report(self.claude)
        rendered = self.render()
        for name in ("alpha", "beta"):
            self.assertTrue(self.row(rendered, name).endswith("| &mdash; | &mdash; |"))

    def test_stale_commit_channel_or_run_fails_closed(self):
        for key, value in (
            ("source_revision", "b" * 40),
            ("source_revision", None),
            ("channel", "latest"),
            ("run_url", RUN_URL + "4"),
            ("client", "other-client"),
            ("scan_completed", "true"),
            ("scan_completed", None),
            ("status", ["passed"]),
            ("status", {"passed": True}),
        ):
            with self.subTest(key=key):
                report = copy.deepcopy(self.codex)
                report[key] = value
                self.write_report(report, client="codex")
                self.assertTrue(
                    self.row(self.render()).endswith("| &mdash; | &#9989; |")
                )

    def test_source_hashes_match_probe_formats(self):
        source = self.root / "skills/alpha"
        (source / "Z-resource.txt").write_bytes(b"Uppercase resource.\n")
        (source / "a-resource.txt").write_bytes(b"Lowercase resource.\n")
        digest = hashlib.sha256()
        for name in ("SKILL.md", "Z-resource.txt", "a-resource.txt", "resource.txt"):
            digest.update(name.encode() + b"\0")
            digest.update(hashlib.sha256((source / name).read_bytes()).digest())
        hashes = source_hashes(self.root)["alpha"]
        self.assertEqual(hashes["source_sha256"], digest.hexdigest())
        self.assertEqual(
            hashes["body_sha256"], hashlib.sha256(b"\nInstructions.\n").hexdigest()
        )

    def test_changed_resource_invalidates_both_clients_package_evidence(self):
        (self.root / "skills/alpha/resource.txt").write_bytes(b"Changed.\n")
        self.assertTrue(self.row(self.render()).endswith("| &mdash; | &mdash; |"))
        source = self.root / "skills/alpha/SKILL.md"
        source.write_bytes(source.read_bytes() + b"Changed instructions.\n")
        self.assertTrue(self.row(self.render()).endswith("| &mdash; | &mdash; |"))

    def test_each_claude_hash_is_required(self):
        for key in ("source_sha256", "skill_sha256", "body_sha256"):
            with self.subTest(key=key):
                report = copy.deepcopy(self.claude)
                report["skills"][0].pop(key)
                self.write_report(report)
                self.assertTrue(
                    self.row(self.render()).endswith("| &#9989; | &mdash; |")
                )

    def test_duplicate_or_unsupported_rows_are_unknown(self):
        for replacement in (
            [self.codex["skills"][0]] * 2 + [self.codex["skills"][1]],
            [
                {**self.codex["skills"][0], "status": "unsupported"},
                self.codex["skills"][1],
            ],
            [
                {**self.codex["skills"][0], "status": ["passed"]},
                self.codex["skills"][1],
            ],
            [
                {**self.codex["skills"][0], "status": {"passed": True}},
                self.codex["skills"][1],
            ],
        ):
            with self.subTest(replacement=replacement):
                report = {**self.codex, "skills": replacement}
                self.write_report(report)
                rendered = self.render()
                self.assertTrue(self.row(rendered).endswith("| &mdash; | &#9989; |"))
                self.assertTrue(
                    self.row(rendered, "beta").endswith("| &#9989; | &#9989; |")
                )

    def test_structurally_invalid_reports_are_unknown_and_not_leaked(self):
        for invalid in ("not JSON", "[]", '{"client":"codex","skills":[null]}'):
            with self.subTest(invalid=invalid):
                path = self.write_report(self.codex)
                path.write_text(invalid, encoding="ascii")
                self.assertTrue(
                    self.row(self.render()).endswith("| &mdash; | &#9989; |")
                )
        report = copy.deepcopy(self.codex)
        report.update(
            client_version="private/token/path", errors=["private/token/path"]
        )
        self.write_report(report)
        self.assertNotIn("private/token/path", self.render())

    def test_latest_artifacts_do_not_replace_pinned_results(self):
        latest = copy.deepcopy(self.codex)
        latest.update(channel="latest", status="failed")
        latest["skills"][0]["status"] = "failed"
        self.write_report(latest, channel="latest")
        self.assertTrue(self.row(self.render()).endswith("| &#9989; | &#9989; |"))
        self.assertTrue(
            self.row(self.render("latest")).endswith("| &#10060; | &mdash; |")
        )

    def test_legacy_reports_only_accepted_locally_with_hash_match(self):
        for report in (self.codex, self.claude):
            for key in ("channel", "source_revision", "scan_completed", "run_url"):
                report.pop(key)
            self.write_report(report)
        self.assertTrue(
            self.row(self.render(run_url=None)).endswith("| &#9989; | &#9989; |")
        )
        self.assertIn(
            "Evidence: local discovery; hosted CI not run.", self.render(run_url=None)
        )
        self.assertTrue(self.row(self.render()).endswith("| &mdash; | &mdash; |"))

    def test_ci_provenance_without_scan_completion_is_unknown(self):
        for report in (self.codex, self.claude):
            report.pop("scan_completed")
            self.write_report(report)
        self.assertTrue(self.row(self.render()).endswith("| &mdash; | &mdash; |"))
        self.assertTrue(
            self.row(self.render(run_url=None)).endswith("| &#9989; | &#9989; |")
        )

    def test_marker_errors_preserve_all_bytes(self):
        for original in (b"No markers\n", START + END + START, END + START, START):
            with self.subTest(original=original):
                self.readme.write_bytes(original)
                with self.assertRaises(ValueError):
                    update_readme(self.reports, self.readme, REVISION, root=self.root)
                self.assertEqual(self.readme.read_bytes(), original)

    def test_invalid_inputs_and_source_preserve_readme(self):
        original = self.readme.read_bytes()
        for kwargs in (
            {"revision": "short"},
            {"channel": "other"},
            {"run_url": "https://github.com.evil.invalid/actions/runs/123"},
            {"run_url": RUN_URL + "?token=synthetic"},
        ):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                update_readme(
                    self.reports,
                    self.readme,
                    root=self.root,
                    **{"revision": REVISION, **kwargs},
                )
            self.assertEqual(self.readme.read_bytes(), original)
        (self.root / "skills/empty").mkdir()
        with self.assertRaises(ValueError):
            update_readme(self.reports, self.readme, REVISION, root=self.root)
        self.assertEqual(self.readme.read_bytes(), original)

    def test_preserves_prose_and_does_not_rewrite_identical_output(self):
        self.assertTrue(
            update_readme(self.reports, self.readme, REVISION, root=self.root)
        )
        updated = self.readme.read_bytes()
        self.assertTrue(updated.startswith(self.before))
        self.assertTrue(updated.endswith(self.after))
        self.assertNotIn(b"\r", updated)
        with patch.object(Path, "write_bytes", side_effect=AssertionError("rewrite")):
            self.assertFalse(
                update_readme(self.reports, self.readme, REVISION, root=self.root)
            )
        self.assertEqual(updated, self.readme.read_bytes())

    def test_cli_prints_only_generated_markdown_for_job_summary(self):
        output = io.StringIO()
        with (
            patch("scripts.update_agent_support.ROOT", self.root),
            patch(
                "scripts.update_agent_support.source_hashes",
                return_value=source_hashes(self.root),
            ),
            redirect_stdout(output),
            redirect_stderr(io.StringIO()),
        ):
            result = main(
                [
                    "--reports",
                    str(self.reports),
                    "--readme",
                    str(self.readme),
                    "--revision",
                    REVISION,
                    "--run-url",
                    RUN_URL,
                ]
            )
        self.assertEqual(result, 0)
        self.assertTrue(output.getvalue().startswith("| Skill | Codex | Claude Code |"))
        self.assertNotIn("Support table updated", output.getvalue())


if __name__ == "__main__":
    unittest.main()
