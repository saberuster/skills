"""Synthetic Claude discovery protocol checks; no CLI or model is called."""

import asyncio
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.check_claude_skills import (
    check,
    copy_skills,
    expected_skills,
    initialization_info,
    isolated_environment,
    main,
    process_environment,
    verify_commands,
)


class CommandTests(unittest.TestCase):
    def setUp(self):
        self.expected = {"test-skill": {"description": "Complete description."}}
        self.command = {"name": "test-skill", "description": "Complete description."}

    def test_unique_complete_description(self):
        result, errors = verify_commands({"commands": [self.command]}, self.expected)
        self.assertEqual(result[0]["status"], "passed")
        self.assertEqual(errors, [])

    def test_observed_project_scope_suffix(self):
        command = {**self.command, "description": "Complete description. (project)"}
        result, errors = verify_commands({"commands": [command]}, self.expected)
        self.assertEqual(result[0]["observed_description"], command["description"])
        self.assertEqual(errors, [])

    def test_malformed_or_empty_info(self):
        for info in (None, {}, {"commands": {}}, {"commands": []}):
            with self.subTest(info=info):
                rows, errors = verify_commands(info, self.expected)
                self.assertEqual(rows[0]["status"], "not_checked")
                self.assertTrue(errors)
        for command in (None, {}, {"name": "test-skill", "description": None}):
            with self.subTest(command=command):
                rows, errors = verify_commands({"commands": [command]}, self.expected)
                self.assertEqual(rows[0]["status"], "not_checked")
                self.assertTrue(errors)

    def test_missing_or_duplicate_skill(self):
        for commands in (
            [{"name": "unrelated", "description": "Other"}],
            [self.command, self.command],
        ):
            with self.subTest(commands=commands):
                rows, errors = verify_commands({"commands": commands}, self.expected)
                self.assertEqual(rows[0]["status"], "failed")
                self.assertTrue(errors)

    def test_truncated_or_different_description(self):
        for description in ("Complete", "Other.", "Complete description. suffix"):
            with self.subTest(description=description):
                rows, errors = verify_commands(
                    {"commands": [{**self.command, "description": description}]},
                    self.expected,
                )
                self.assertEqual(rows[0]["status"], "failed")
                self.assertEqual(rows[0]["observed_description"], description)
                self.assertTrue(errors)

    def test_multiple_failures_and_successes_are_all_reported(self):
        expected = {
            name: {"description": name}
            for name in ("missing", "duplicate", "changed", "ok")
        }
        commands = [
            {"name": "duplicate", "description": "duplicate"},
            {"name": "duplicate", "description": "duplicate"},
            {"name": "changed", "description": "wrong"},
            {"name": "ok", "description": "ok"},
        ]
        rows, errors = verify_commands({"commands": commands}, expected)
        self.assertEqual([row["status"] for row in rows], ["failed"] * 3 + ["passed"])
        self.assertEqual(len(errors), 3)


class ReportTests(unittest.TestCase):
    def test_failure_artifact_keeps_versions_and_skill_matrix_and_exits_nonzero(self):
        expected = {
            "missing": {"description": "Missing skill"},
            "ok": {"description": "Working skill"},
        }

        def runner(root, claude, expected, report):
            report.update(client_version="Claude test", sdk_version="SDK test")
            return {"commands": [{"name": "ok", "description": "Working skill"}]}

        with patch(
            "scripts.check_claude_skills.expected_skills", return_value=expected
        ):
            report = check(Path("unused"), discovery_runner=runner)
        self.assertEqual(report["client_version"], "Claude test")
        self.assertEqual(report["sdk_version"], "SDK test")
        self.assertEqual(report["status"], "failed")
        self.assertTrue(report["scan_completed"])
        self.assertEqual(
            [row["status"] for row in report["skills"]], ["failed", "passed"]
        )
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "report.json"
            with (
                patch("sys.argv", ["check", "--report", str(target)]),
                patch("scripts.check_claude_skills.check", return_value=report),
                patch("sys.stdout", new_callable=io.StringIO),
            ):
                self.assertEqual(main(), 1)
            self.assertEqual(json.loads(target.read_text()), report)

    def test_initialization_failure_keeps_known_versions_and_unchecked_skills(self):
        def runner(root, claude, expected, report):
            report.update(client_version="Claude test", sdk_version="SDK test")
            raise ValueError("Initialization failed")

        with patch(
            "scripts.check_claude_skills.expected_skills",
            return_value={"sample": {"description": "Sample"}},
        ):
            report = check(Path("unused"), discovery_runner=runner)
        self.assertEqual(report["client_version"], "Claude test")
        self.assertEqual(report["skills"][0]["status"], "not_checked")
        self.assertEqual(report["errors"], ["Initialization failed"])
        self.assertFalse(report["scan_completed"])

    def test_malformed_response_is_not_a_completed_scan(self):
        with patch(
            "scripts.check_claude_skills.expected_skills",
            return_value={"sample": {"description": "Sample"}},
        ):
            report = check(Path("unused"), discovery_runner=lambda *args: {})
        self.assertFalse(report["scan_completed"])
        self.assertEqual(report["skills"][0]["status"], "not_checked")


class IsolationTests(unittest.TestCase):
    def test_skill_directory_without_entry_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "skills" / "missing").mkdir(parents=True)
            with self.assertRaisesRegex(ValueError, "has no SKILL.md"):
                expected_skills(root)

    def test_credentials_and_configuration_are_not_inherited(self):
        with tempfile.TemporaryDirectory() as temporary:
            with patch.dict(
                os.environ,
                {"ANTHROPIC_API_KEY": "secret", "CLAUDE_CODE_OAUTH_TOKEN": "secret"},
            ):
                env = isolated_environment(Path(temporary) / "home")
                self.assertNotIn("ANTHROPIC_API_KEY", env)
                self.assertNotIn("CLAUDE_CODE_OAUTH_TOKEN", env)
                with process_environment(env):
                    self.assertNotIn("ANTHROPIC_API_KEY", os.environ)
                    self.assertEqual(os.environ["HOME"], env["HOME"])
                self.assertEqual(os.environ["ANTHROPIC_API_KEY"], "secret")

    def test_complete_copy_is_verified(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "source"
            skill = root / "skills" / "sample"
            (skill / "agents").mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                "---\nname: sample\ndescription: A sample.\n---\nBody.\n"
            )
            (skill / "agents" / "openai.yaml").write_text(
                "policy:\n  allow_implicit_invocation: false\n"
            )
            (skill / "extra.txt").write_text("Complete resource tree.\n")
            expected = expected_skills(root)
            self.assertFalse(expected["sample"]["codex_allow_implicit_invocation"])
            self.assertEqual(len(expected["sample"]["body_sha256"]), 64)
            self.assertEqual(len(expected["sample"]["source_sha256"]), 64)
            project = Path(temporary) / "project"
            copy_skills(root, project, expected)
            self.assertEqual(
                (project / ".claude" / "skills" / "sample" / "extra.txt").read_text(),
                "Complete resource tree.\n",
            )
            (skill / "extra.txt").write_text("Changed resource.\n")
            changed = expected_skills(root)
            self.assertNotEqual(
                expected["sample"]["source_sha256"], changed["sample"]["source_sha256"]
            )
            self.assertEqual(
                expected["sample"]["skill_sha256"], changed["sample"]["skill_sha256"]
            )


class NoPromptTests(unittest.TestCase):
    def test_initialization_uses_only_empty_connect_info_and_disconnect(self):
        events = []
        expected_info = {"commands": [{"name": "sample", "description": "Sample"}]}

        class Client:
            def __init__(self, *, options):
                events.append(("options", options))

            async def __aenter__(self):
                await self.connect()
                return self

            async def connect(self, *args, **kwargs):
                self_args = (args, kwargs)
                events.append(("connect", self_args))

            async def get_server_info(self):
                events.append(("info",))
                return expected_info

            async def __aexit__(self, *args):
                events.append(("disconnect",))

            async def query(self, *args, **kwargs):
                raise AssertionError("Sending a prompt is prohibited")

        result = asyncio.run(initialization_info("options", Client))
        self.assertEqual(result, expected_info)
        self.assertEqual(
            events,
            [("options", "options"), ("connect", ((), {})), ("info",), ("disconnect",)],
        )

    def test_disconnect_runs_when_server_info_fails(self):
        disconnected = []

        class Client:
            def __init__(self, *, options):
                pass

            async def __aenter__(self):
                return self

            async def get_server_info(self):
                raise ValueError("Invalid info")

            async def __aexit__(self, *args):
                disconnected.append(True)

        with self.assertRaises(ValueError):
            asyncio.run(initialization_info(None, Client))
        self.assertEqual(disconnected, [True])


if __name__ == "__main__":
    unittest.main()
