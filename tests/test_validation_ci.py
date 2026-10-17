"""Validate execution accounting without invoking live clients or engines."""

import io
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import validation_ci


class ValidationRuntimeTests(unittest.TestCase):
    def report(self, function, kind="checks", test_id=None):
        case = unittest.FunctionTestCase(function)
        if test_id:
            case.id = lambda: test_id
        suite = unittest.TestSuite([case])
        return validation_ci.unittest_report(suite, kind, io.StringIO())

    def test_success_reports_actual_count(self):
        result = self.report(lambda: None)
        self.assertEqual((result["status"], result["testsRun"]), ("passed", 1))
        self.assertEqual(
            result["counts"],
            {"errors": 0, "failures": 0, "skipped": 0, "expected_failures": 0},
        )

    def test_empty_selection_is_failure(self):
        result = validation_ci.unittest_report(
            unittest.TestSuite(), "checks", io.StringIO()
        )
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["selection_error"], "No tests selected")

    def test_expected_platform_skip_is_partial_with_reason(self):
        def windows_only():
            raise unittest.SkipTest("Windows junction behavior requires Windows")

        result = self.report(
            windows_only, test_id=next(iter(validation_ci.PLATFORM_SKIPS))[0]
        )
        self.assertEqual(result["status"], "partial")
        self.assertEqual(
            result["skipped"][0]["reason"], "Windows junction behavior requires Windows"
        )
        self.assertTrue(result["skipped"][0]["id"])

    def test_other_test_cannot_borrow_platform_skip_reason(self):
        def unrelated():
            raise unittest.SkipTest("Windows junction behavior requires Windows")

        self.assertEqual(self.report(unrelated)["status"], "failed")

    def test_missing_dependency_skip_fails(self):
        def missing_dependency():
            raise unittest.SkipTest("PowerShell 7.2+ unavailable")

        result = self.report(missing_dependency)
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["counts"]["skipped"], 1)
        self.assertEqual(len(result["unexpected_skips"]), 1)

    def test_blender_never_accepts_skipped_execution(self):
        def unavailable():
            raise unittest.SkipTest("Windows junction behavior requires Windows")

        self.assertEqual(self.report(unavailable, "blender")["status"], "failed")

    def test_errors_and_assertions_record_ids_and_details(self):
        def error():
            raise RuntimeError("fixture error")

        def failure():
            raise AssertionError("fixture assertion")

        result = validation_ci.unittest_report(
            unittest.TestSuite(
                [unittest.FunctionTestCase(error), unittest.FunctionTestCase(failure)]
            ),
            "checks",
            io.StringIO(),
        )
        self.assertEqual(result["status"], "failed")
        self.assertEqual(
            (
                result["testsRun"],
                result["counts"]["errors"],
                result["counts"]["failures"],
            ),
            (2, 1, 1),
        )
        self.assertIn("fixture error", result["errors"][0]["traceback"])
        self.assertTrue(result["failures"][0]["id"])

    def test_discovery_automatically_includes_new_modules(self):
        class NamedCase(unittest.TestCase):
            def __init__(self, name):
                super().__init__()
                self.name = name

            def id(self):
                return self.name

        names = [
            "test_future.New.test_method",
            "test_scene_blender_integration.Real.test_method",
            "test_low_poly_blender_integration.Real.test_method",
        ]

        def discovered(directory, pattern):
            return unittest.TestSuite(
                [
                    NamedCase(name)
                    for name in names
                    if name.startswith(Path(pattern).stem + ".")
                ]
            )

        modules = [Path(name.split(".")[0] + ".py") for name in names]
        with (
            patch.object(Path, "glob", return_value=modules),
            patch.object(unittest, "TestLoader") as loader,
        ):
            loader.return_value.discover.side_effect = discovered
            self.assertEqual(
                [
                    case.id()
                    for case in validation_ci.cases(
                        validation_ci.selected_suite("checks")
                    )
                ],
                names[:1],
            )
            self.assertEqual(
                [
                    case.id()
                    for case in validation_ci.cases(
                        validation_ci.selected_suite("blender")
                    )
                ],
                sorted(names[1:]),
            )

    def test_plans_use_real_report_flags_and_new_home(self):
        output = Path("/evidence")
        for check, script in [
            ("codex-discovery", "check_codex_skills.py"),
            ("claude-discovery", "check_claude_skills.py"),
            ("fern-install", "check_fern_install.py"),
        ]:
            command = validation_ci.command_plan(check, output, 42)[0]
            self.assertIn("scripts/" + script, command)
            self.assertIn("--report", command)
        install = validation_ci.command_plan("fern-install", output, 42)[0]
        self.assertIn("--home", install)
        self.assertEqual(install[-2:], ["--timeout", "42"])

    def test_unittest_child_can_import_repository_packages(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "scripts").mkdir()
            (root / "tests").mkdir()
            (root / "scripts" / "__init__.py").write_text("", encoding="utf-8")
            (root / "scripts" / "helper.py").write_text(
                "VALUE = 42\n", encoding="utf-8"
            )
            (root / "scripts" / "validation_ci.py").write_text(
                "import unittest\n"
                "suite = unittest.defaultTestLoader.discover('tests')\n"
                "result = unittest.TextTestRunner().run(suite)\n"
                "raise SystemExit(not result.wasSuccessful())\n",
                encoding="utf-8",
            )
            (root / "tests" / "test_import.py").write_text(
                "import unittest\n"
                "from scripts import helper\n"
                "class ImportTest(unittest.TestCase):\n"
                "    def test_value(self):\n"
                "        self.assertEqual(helper.VALUE, 42)\n",
                encoding="utf-8",
            )
            environment = os.environ.copy()
            environment.pop("PYTHONPATH", None)
            for check in ("checks", "blender"):
                with self.subTest(check=check):
                    command = validation_ci.command_plan(check, root, 42)[-1]
                    result = subprocess.run(
                        command,
                        cwd=root,
                        env=environment,
                        text=True,
                        capture_output=True,
                        timeout=30,
                    )
                    self.assertEqual(
                        result.returncode, 0, result.stdout + result.stderr
                    )
                    self.assertIn("Ran 1 test", result.stderr)

    def test_latest_upgrade_targets_only_selected_client(self):
        self.assertEqual(
            validation_ci.latest_command("codex-discovery")[-1], "@openai/codex@latest"
        )
        self.assertEqual(
            validation_ci.latest_command("claude-discovery")[-1], "claude-agent-sdk"
        )
        with self.assertRaises(ValueError):
            validation_ci.latest_command("checks")

    def test_missing_prerequisite_fails_before_tests(self):
        with (
            patch.object(validation_ci.shutil, "which", return_value=None),
            patch.object(validation_ci, "execute") as execute,
        ):
            result = validation_ci.run("checks", Path("/evidence"), 3)
        self.assertEqual(result["status"], "failed")
        self.assertIn("PowerShell", result["error"])
        execute.assert_not_called()

    def test_missing_child_report_never_passes(self):
        with (
            tempfile.TemporaryDirectory() as temporary,
            patch.object(validation_ci, "execute", return_value={"status": "passed"}),
        ):
            result = validation_ci.run("codex-discovery", Path(temporary), 3)
        self.assertEqual(result["status"], "failed")
        self.assertIn("error", result)

    def test_structured_skip_survives_process_success(self):
        with (
            tempfile.TemporaryDirectory() as temporary,
            patch.object(validation_ci, "prerequisites"),
            patch.object(validation_ci, "execute", return_value={"status": "passed"}),
        ):
            output = Path(temporary)
            (output / "unittest.json").write_text(
                json.dumps(
                    {
                        "status": "partial",
                        "testsRun": 1,
                        "skipped": [
                            {
                                "id": "fixture",
                                "reason": "Windows junction behavior requires Windows",
                            }
                        ],
                    }
                )
            )
            result = validation_ci.run("checks", output, 3)
        self.assertEqual(result["status"], "partial")
        self.assertTrue(any("Windows junction" in limit for limit in result["limits"]))

    def test_empty_agent_selection_never_calls_model(self):
        with patch.object(validation_ci.fern_ci, "run_behavior") as run_behavior:
            result = validation_ci.run("agent-behavior", Path("/evidence"), 3)
        self.assertEqual(result["status"], "failed")
        run_behavior.assert_not_called()


if __name__ == "__main__":
    unittest.main()
