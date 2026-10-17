"""Check native Windows selection and evidence without running the host suite."""

import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import yaml

from scripts import windows_ci


def case(identity, function=lambda: None):
    test = unittest.FunctionTestCase(function)
    test.id = lambda: identity
    return test


def discovered(extra=()):
    return unittest.TestSuite(
        [case(name) for name in sorted(windows_ci.REQUIRED_CASES)]
        + [case(name) for name in sorted(windows_ci.EXCLUDED_CASES)]
        + list(extra)
    )


class WindowsRegressionTests(unittest.TestCase):
    def selection(self, suite):
        with patch.object(
            windows_ci.validation_ci, "selected_suite", return_value=suite
        ):
            return windows_ci.select_suite()

    def run_fixture(self, suite):
        with (
            tempfile.TemporaryDirectory() as temporary,
            patch.object(windows_ci.sys, "platform", "win32"),
            patch.object(
                windows_ci, "metadata", return_value={"source_revision": "fixture"}
            ),
            patch.object(
                windows_ci.validation_ci, "selected_suite", return_value=suite
            ),
        ):
            output = Path(temporary) / "new-evidence"
            summary = windows_ci.run(output)
            artifacts = {
                name: (output / name).read_text(encoding="utf-8")
                for name in ("summary.json", "summary.md", "unittest.log")
            }
        self.assertEqual(json.loads(artifacts["summary.json"]), summary)
        return summary, artifacts

    def test_selection_keeps_new_portable_modules_and_only_exact_exclusions(self):
        new = "test_future.FutureTests.test_portable"
        similar = next(iter(windows_ci.EXCLUDED_CASES)) + "_portable"
        with patch.object(
            windows_ci.validation_ci,
            "selected_suite",
            return_value=discovered([case(new), case(similar)]),
        ) as selected:
            suite, selection = windows_ci.select_suite()
        selected.assert_called_once_with("checks")
        identities = {item.id() for item in windows_ci.validation_ci.cases(suite)}
        self.assertEqual(identities, windows_ci.REQUIRED_CASES | {new, similar})
        self.assertIn("test_future", selection["selected_modules"])
        self.assertEqual(selection["selection_errors"], [])
        self.assertEqual(len(selection["excluded_cases"]), 7)
        self.assertTrue(all(row["reason"] for row in selection["excluded_cases"]))
        self.assertTrue(all(row["discovered"] for row in selection["excluded_cases"]))

    def test_missing_each_required_identity_fails(self):
        for missing in sorted(windows_ci.REQUIRED_CASES):
            with self.subTest(missing=missing):
                suite = unittest.TestSuite(
                    item
                    for item in windows_ci.validation_ci.cases(discovered())
                    if item.id() != missing
                )
                summary, _ = self.run_fixture(suite)
                self.assertEqual(summary["exit_code"], 1)
                self.assertTrue(
                    any(missing in error for error in summary["selection_errors"])
                )

    def test_stale_exclusion_or_duplicate_identity_fails_selection(self):
        _, selection = self.selection(
            unittest.TestSuite([case(name) for name in windows_ci.REQUIRED_CASES])
        )
        self.assertTrue(
            any("Missing exclusion" in row for row in selection["selection_errors"])
        )
        _, selection = self.selection(
            discovered([case(next(iter(windows_ci.REQUIRED_CASES)))])
        )
        self.assertIn(
            "Duplicate discovered test identities", selection["selection_errors"]
        )

    def test_success_reports_actual_counts_and_evidence(self):
        summary, artifacts = self.run_fixture(discovered())
        self.assertEqual((summary["status"], summary["exit_code"]), ("passed", 0))
        self.assertEqual(
            summary["unittest"]["testsRun"], len(windows_ci.REQUIRED_CASES)
        )
        self.assertEqual(summary["unittest"]["counts"]["skipped"], 0)
        self.assertIn("Native Windows regressions: passed", artifacts["summary.md"])

    def test_import_error_traceback_survives_in_failed_report(self):
        broken = unittest.TestLoader().loadTestsFromName(
            "windows_fixture_missing_module"
        )
        suite = discovered(list(windows_ci.validation_ci.cases(broken)))
        summary, artifacts = self.run_fixture(suite)
        self.assertEqual((summary["status"], summary["exit_code"]), ("failed", 1))
        self.assertEqual(summary["unittest"]["counts"]["errors"], 1)
        self.assertIn("windows_fixture_missing_module", artifacts["unittest.log"])

    def test_runtime_skip_cannot_pass_even_for_linux_allowlisted_junction(self):
        def skip():
            raise unittest.SkipTest("Windows junction behavior requires Windows")

        identity = "test_godot_build_regressions.GodotBuildRegressionTests.test_godot_rejects_windows_junction"
        suite = unittest.TestSuite(
            case(item.id(), skip) if item.id() == identity else item
            for item in windows_ci.validation_ci.cases(discovered())
        )
        summary, _ = self.run_fixture(suite)
        self.assertEqual(summary["status"], "failed")
        self.assertEqual(summary["unittest"]["counts"]["skipped"], 1)

    def test_empty_selection_fails_with_artifacts(self):
        summary, artifacts = self.run_fixture(unittest.TestSuite())
        self.assertEqual(summary["exit_code"], 1)
        self.assertEqual(summary["unittest"]["testsRun"], 0)
        self.assertIn("No tests selected", artifacts["summary.md"])

    def test_assertion_failure_retains_report_and_log(self):
        def fail():
            raise AssertionError("synthetic failure evidence")

        summary, artifacts = self.run_fixture(
            discovered([case("test_future.Case.fail", fail)])
        )
        self.assertEqual(summary["exit_code"], 1)
        self.assertEqual(summary["unittest"]["counts"]["failures"], 1)
        self.assertIn("synthetic failure evidence", artifacts["unittest.log"])
        self.assertIn("Native Windows regressions: failed", artifacts["summary.md"])

    def test_prerequisite_failure_still_writes_evidence(self):
        with (
            tempfile.TemporaryDirectory() as temporary,
            patch.object(windows_ci.sys, "platform", "win32"),
            patch.object(
                windows_ci, "metadata", side_effect=ValueError("PowerShell unavailable")
            ),
        ):
            output = Path(temporary) / "new-evidence"
            summary = windows_ci.run(output)
            self.assertEqual(summary["exit_code"], 1)
            self.assertIn("PowerShell unavailable", (output / "summary.md").read_text())
            self.assertTrue((output / "unittest.log").is_file())

    def test_linux_is_rejected_before_output_or_discovery(self):
        with (
            patch.object(windows_ci.sys, "platform", "linux"),
            patch.object(windows_ci, "fresh_output") as output,
        ):
            with self.assertRaisesRegex(ValueError, "native Windows"):
                windows_ci.run(Path("unused"))
        output.assert_not_called()

    def test_metadata_records_actual_source_and_runner_versions(self):
        with (
            patch.object(windows_ci.shutil, "which", return_value="fixture-pwsh"),
            patch.object(
                windows_ci.platform, "platform", return_value="fixture-windows"
            ),
            patch.object(
                windows_ci.subprocess,
                "run",
                side_effect=[
                    SimpleNamespace(stdout="7.4.6\n"),
                    SimpleNamespace(stdout="fixture-head\n"),
                ],
            ) as command,
            patch.dict(
                windows_ci.os.environ, {"ImageOS": "win25", "ImageVersion": "fixture"}
            ),
        ):
            result = windows_ci.metadata()
        self.assertEqual(result["source_revision"], "fixture-head")
        self.assertEqual(
            result["powershell"], {"path": "fixture-pwsh", "version": "7.4.6"}
        )
        self.assertEqual(result["runner"]["ImageOS"], "win25")
        self.assertEqual(result["runner"]["ImageVersion"], "fixture")
        self.assertEqual(
            command.call_args_list[1].args[0], ["git", "rev-parse", "HEAD"]
        )

    def test_old_powershell_is_rejected_before_test_selection(self):
        with (
            patch.object(windows_ci.shutil, "which", return_value="fixture-pwsh"),
            patch.object(
                windows_ci.subprocess,
                "run",
                return_value=SimpleNamespace(stdout="7.1.0"),
            ),
        ):
            with self.assertRaisesRegex(ValueError, "PowerShell 7.2"):
                windows_ci.metadata()

    def test_workflow_routes_windows_once_per_validation_layer(self):
        workflows = windows_ci.ROOT / ".github/workflows"

        def read(name):
            return yaml.load(
                (workflows / name).read_text(encoding="ascii"), Loader=yaml.BaseLoader
            )

        for name in ("validate.yml", "validation-full.yml"):
            workflow = read(name)
            windows = workflow["jobs"]["windows"]
            self.assertEqual(
                windows["uses"], "./.github/workflows/validation-windows.yml"
            )
            self.assertNotIn("if", windows)
            self.assertNotIn("needs", windows)
        self.assertNotIn("windows", read("validation-runtime.yml")["jobs"])
        workflow = read("validation-windows.yml")
        self.assertEqual(set(workflow["on"]), {"workflow_call", "workflow_dispatch"})
        self.assertEqual(workflow["jobs"]["regressions"]["runs-on"], "windows-2025")
        steps = workflow["jobs"]["regressions"]["steps"]
        self.assertTrue(
            any(
                "python -m scripts.windows_ci --output" in step.get("run", "")
                for step in steps
            )
        )
        upload = next(
            step
            for step in steps
            if step.get("uses", "").startswith("actions/upload-artifact@")
        )
        self.assertEqual(upload["if"], "always()")

    def test_output_must_be_fresh_and_outside_source_tree(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            for invalid in (
                base,
                windows_ci.ROOT / "unused-windows-evidence",
                Path("relative"),
            ):
                with (
                    self.subTest(invalid=invalid),
                    self.assertRaisesRegex(ValueError, "Output"),
                ):
                    windows_ci.fresh_output(invalid)
            output = windows_ci.fresh_output(base / "new")
            self.assertTrue(output.is_dir())


if __name__ == "__main__":
    unittest.main()
