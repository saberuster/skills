"""Exercise host isolation, failure evidence, and Docker cleanup without Docker."""

import argparse
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import run_fern_validation as launcher


class LauncherTests(unittest.TestCase):
    def options(self, output, suite="checks", **kwargs):
        return argparse.Namespace(
            output=output,
            suite=suite,
            model=kwargs.get("model"),
            case=kwargs.get("case", []),
            timeout=30,
        )

    def test_output_cannot_exist_or_contain_source(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "source"
            root.mkdir()
            for output in (root, root / "new"):
                with (
                    self.subTest(output=output),
                    self.assertRaises(launcher.LaunchError),
                ):
                    launcher.validate_options(self.options(output), root, {})

    def test_behavior_requires_explicit_model_and_key(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "source"
            output = Path(temporary) / "evidence"
            for model, env in ((None, {"CODEX_API_KEY": "fake"}), ("model", {})):
                with self.subTest(model=model), self.assertRaises(launcher.LaunchError):
                    launcher.validate_options(
                        self.options(output, "behavior", model=model), root, env
                    )
            self.assertEqual(
                launcher.validate_options(
                    self.options(output, "behavior", model="model"),
                    root,
                    {"OPENAI_API_KEY": "fake"},
                ),
                output.resolve(),
            )

    def test_context_excludes_credentials_caches_and_git_state(self):
        for name in (
            ".git/config",
            "skills/.env",
            "scripts/auth.json",
            "tests/key.pem",
            "docs/.ssh/id_rsa",
            "skills/item/node_modules/a.js",
            "unknown.txt",
        ):
            with self.subTest(name=name):
                self.assertFalse(launcher.allowed_source(Path(name)))
        self.assertTrue(
            launcher.allowed_source(Path("skills/fern/setup-fern/SKILL.md"))
        )
        self.assertTrue(launcher.allowed_source(Path("package-lock.json")))

    def test_staging_copies_working_tree_bytes_without_private_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "source"
            destination = Path(temporary) / "context"
            for relative in ("scripts/public.py", "scripts/auth.json", ".git/config"):
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("working tree bytes", encoding="utf-8")
            listing = b"scripts/public.py\0scripts/auth.json\0.git/config\0"
            with mock.patch.object(
                launcher.subprocess,
                "run",
                return_value=subprocess.CompletedProcess([], 0, stdout=listing),
            ):
                launcher.stage_source(root, destination)
            self.assertEqual(
                (destination / "scripts/public.py").read_text("utf-8"),
                "working tree bytes",
            )
            self.assertFalse((destination / "scripts/auth.json").exists())
            self.assertFalse((destination / ".git").exists())

    def test_deadline_counts_worker_turns_and_independent_evaluations(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "examples").mkdir()
            (root / "examples/behavior-smoke.json").write_text(
                json.dumps(
                    {
                        "cases": [
                            {"id": "one", "skill": "setup-fern", "turns": ["a", "b"]},
                            {"id": "two", "skill": "setup-fern", "turns": ["a"]},
                            {"id": "other", "skill": "another", "turns": ["a"]},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            args = self.options(root / "output", "behavior", model="test")
            self.assertEqual(launcher.container_deadline(args, root), 5 * 30 + 300)
            args.case = ["two"]
            self.assertEqual(launcher.container_deadline(args, root), 2 * 30 + 300)

    def run_mocked(
        self,
        root,
        output,
        *,
        suite="checks",
        fail_wait=False,
        timeout=False,
        fail_operation=None,
    ):
        calls = []

        def run(command, **kwargs):
            calls.append((command, kwargs.get("env", {})))
            if command[0] == "git":
                return subprocess.CompletedProcess(command, 0, stdout="a" * 40 + "\n")
            if command[1] == "wait":
                if timeout:
                    raise subprocess.TimeoutExpired(command, 30)
                kwargs["stdout"].write(b"7\n" if fail_wait else b"0\n")
            if command[1] == "logs" and suite == "behavior":
                kwargs["stdout"].write(b"private-test-key\n")
            return subprocess.CompletedProcess(
                command, int(command[1] == fail_operation)
            )

        options = self.options(
            output, suite, model="test-model" if suite == "behavior" else None
        )
        with (
            mock.patch.dict(
                os.environ, {"OPENAI_API_KEY": "private-test-key"}, clear=True
            ),
            mock.patch.object(launcher.shutil, "which", return_value="docker"),
            mock.patch.object(launcher, "stage_source"),
            mock.patch.object(launcher, "container_deadline", return_value=330),
            mock.patch.object(launcher.subprocess, "run", side_effect=run),
        ):
            result = launcher.launch(options, root=root)
        return result, calls

    def test_container_has_no_host_mounts_or_keys_for_deterministic_checks(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "source"
            output = Path(temporary) / "evidence"
            result, calls = self.run_mocked(root, output)
            self.assertEqual(result, 0)
            create, env = next(item for item in calls if item[0][1] == "create")
            self.assertNotIn("--mount", create)
            self.assertNotIn("--volume", create)
            self.assertNotIn("-v", create)
            self.assertNotIn("--privileged", create)
            self.assertNotIn("CODEX_API_KEY", env)
            self.assertNotIn("OPENAI_API_KEY", env)
            self.assertIn("no-new-privileges", create)
            self.assertTrue((output / "launcher.json").is_file())

    def test_behavior_forwards_key_by_name_without_value_in_arguments(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "source"
            output = Path(temporary) / "evidence"
            result, calls = self.run_mocked(root, output, suite="behavior")
            self.assertEqual(result, 0)
            create, env = next(item for item in calls if item[0][1] == "create")
            self.assertIn("CODEX_API_KEY", create)
            self.assertEqual(env["CODEX_API_KEY"], "private-test-key")
            self.assertNotIn("private-test-key", " ".join(create))
            self.assertNotIn("OPENAI_API_KEY", env)
            self.assertEqual((output / "container.log").read_text(), "[REDACTED]\n")

    def test_failed_container_still_copies_evidence_and_cleans_up(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "source"
            output = Path(temporary) / "evidence"
            result, calls = self.run_mocked(root, output, fail_wait=True)
            self.assertEqual(result, 1)
            operations = [command[1] for command, _ in calls if command[0] == "docker"]
            self.assertLess(operations.index("cp"), operations.index("rm"))
            self.assertIn('"exit_code": 7', (output / "launcher.json").read_text())

    def test_timeout_kills_copies_and_removes_container(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "source"
            output = Path(temporary) / "evidence"
            result, calls = self.run_mocked(root, output, timeout=True)
            self.assertEqual(result, 1)
            operations = [command[1] for command, _ in calls if command[0] == "docker"]
            self.assertLess(operations.index("kill"), operations.index("cp"))
            self.assertLess(operations.index("cp"), operations.index("rm"))

    def test_copy_or_remove_failure_prevents_success(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "source"
            for operation in ("cp", "rm"):
                with self.subTest(operation=operation):
                    output = Path(temporary) / operation
                    result, calls = self.run_mocked(
                        root, output, fail_operation=operation
                    )
                    self.assertEqual(result, 1)
                    operations = [
                        command[1] for command, _ in calls if command[0] == "docker"
                    ]
                    self.assertIn("rm", operations)


if __name__ == "__main__":
    unittest.main()
