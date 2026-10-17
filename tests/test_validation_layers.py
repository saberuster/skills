"""Layer selection, evidence aggregation, and isolated launcher contracts."""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import run_validation, validation_plan


class LayerPlanTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "source"
        for path in (
            "skills/meta/reflect",
            "skills/blender/reference-scene",
            "skills/fern/setup-fern",
        ):
            package = self.root / path
            package.mkdir(parents=True)
            (package / "SKILL.md").write_text("fixture\n")
        (self.root / "examples").mkdir()
        (self.root / "examples/behavior-smoke.json").write_text(
            json.dumps(
                {
                    "cases": [
                        {"id": "reflect-one", "skill": "reflect", "turns": ["one"]},
                        {
                            "id": "fern-one",
                            "skill": "setup-fern",
                            "turns": ["one", "two"],
                        },
                    ]
                }
            )
        )
        (self.root / "tests").mkdir()
        for name in ("test_new_helper.py", "test_scene_blender_integration.py"):
            (self.root / "tests" / name).write_text("# fixture\n")
        patcher = mock.patch.object(validation_plan, "git", return_value=b"a" * 40)
        patcher.start()
        self.addCleanup(patcher.stop)

    def plan(self, layer="affected", **kwargs):
        return validation_plan.make_plan(layer, root=self.root, **kwargs)

    def test_pr_includes_new_test_modules_but_not_real_engine_modules(self):
        plan = self.plan("pr")
        self.assertEqual([item["check"] for item in plan["checks"]], ["checks"])
        self.assertEqual(plan["test_modules"]["checks"], ["test_new_helper.py"])
        self.assertEqual(
            plan["test_modules"]["blender"], ["test_scene_blender_integration.py"]
        )

    def test_full_selects_runtime_and_both_discovery_channels(self):
        plan = self.plan("full")
        ids = {item["id"] for item in plan["checks"]}
        self.assertEqual(
            ids,
            set(validation_plan.CHECKS)
            | {"codex-discovery-latest", "claude-discovery-latest"},
        )
        self.assertEqual(
            plan["behavior_coverage"]["skills_without_cases"], ["reference-scene"]
        )
        self.assertTrue(plan["manual_evidence"])

    def test_changed_skill_selects_only_its_cases_and_no_unrelated_runtime(self):
        with mock.patch.object(
            validation_plan,
            "changed_paths",
            return_value=("base", ["skills/meta/reflect/SKILL.md"]),
        ):
            plan = self.plan(base="main")
        self.assertEqual(plan["selected_skills"], ["reflect"])
        self.assertEqual(plan["checks"][-1]["cases"], ["reflect-one"])
        self.assertNotIn("blender", {item["check"] for item in plan["checks"]})

    def test_shared_runner_and_removed_package_changes_select_all(self):
        for path in ("scripts/behavior_trials.py", "skills/removed/SKILL.md"):
            with (
                self.subTest(path=path),
                mock.patch.object(
                    validation_plan, "changed_paths", return_value=("base", [path])
                ),
            ):
                self.assertEqual(len(self.plan(base="main")["selected_skills"]), 3)

    def test_docs_only_change_does_not_claim_runtime_pass(self):
        with mock.patch.object(
            validation_plan,
            "changed_paths",
            return_value=("base", ["docs/development.md"]),
        ):
            plan = self.plan(base="main")
        self.assertEqual(plan["checks"], [])
        self.assertEqual(run_validation.aggregate([]), "not_run")

    def test_explicit_cases_narrow_packages_without_a_base(self):
        plan = self.plan("full", cases=["reflect-one"], checks=["agent-behavior"])
        self.assertEqual(plan["selected_skills"], ["reflect"])
        self.assertEqual(plan["checks"][0]["cases"], ["reflect-one"])

    def test_invalid_case_or_inapplicable_check_fails(self):
        for kwargs in (
            {"cases": ["missing"]},
            {"cases": ["reflect-one", "reflect-one"]},
            {"cases": ["reflect-one"], "checks": ["blender"]},
        ):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                self.plan(**kwargs)

    def test_base_diff_keeps_uncommitted_and_untracked_candidate_paths(self):
        with mock.patch.object(
            validation_plan,
            "git",
            side_effect=[
                b"base\n",
                b"skills/old/SKILL.md\0skills/new/SKILL.md\0",
                b"examples/new.json\0",
            ],
        ) as git:
            base, paths = validation_plan.changed_paths(self.root, "main")
        self.assertEqual(base, "base")
        self.assertEqual(len(paths), 3)
        self.assertIn("--no-renames", git.call_args_list[1].args)
        self.assertNotIn("HEAD", git.call_args_list[1].args)


class LayerRunnerTests(unittest.TestCase):
    def test_documented_script_entrypoint_works_from_outside_the_checkout(self):
        with tempfile.TemporaryDirectory() as temporary:
            environment = os.environ.copy()
            environment.pop("PYTHONPATH", None)
            result = subprocess.run(
                [
                    sys.executable,
                    str(Path(run_validation.__file__).resolve()),
                    "--help",
                ],
                cwd=temporary,
                env=environment,
                capture_output=True,
                text=True,
                timeout=30,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("--layer", result.stdout)

    def test_repository_snapshot_preserves_root_docs_and_config_without_credentials(
        self,
    ):
        launcher = run_validation.docker_launcher
        for name in (
            "GUIDE.md",
            ".gitattributes",
            "requirements-new.txt",
            "new-source/public.py",
        ):
            self.assertTrue(launcher.allowed_source(Path(name), all_public=True))
        for name in (
            ".env",
            "new-source/auth.json",
            ".codex/config.toml",
            ".git/config",
        ):
            self.assertFalse(launcher.allowed_source(Path(name), all_public=True))
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "source"
            root.mkdir()
            (root / "GUIDE.md").write_text("Public guide\n")
            (root / ".gitattributes").write_text("* text=auto\n")
            destination = Path(temporary) / "snapshot"
            listing = type("Listing", (), {"stdout": b"GUIDE.md\0.gitattributes\0"})()
            with mock.patch.object(launcher.subprocess, "run", return_value=listing):
                launcher.stage_source(root, destination, all_public=True)
            self.assertEqual((destination / "GUIDE.md").read_text(), "Public guide\n")
            self.assertTrue((destination / ".gitattributes").is_file())

    def options(self, output, **kwargs):
        defaults = dict(
            layer="full",
            output=output,
            base=None,
            case=[],
            check=[],
            latest=False,
            run_agent=False,
            model=None,
            plan_only=False,
            timeout=20,
        )
        defaults.update(kwargs)
        return argparse.Namespace(**defaults)

    def entry(self, check="agent-behavior"):
        return {
            "id": check,
            "check": check,
            "channel": "pinned",
            "cases": ["one"] if check == "agent-behavior" else [],
            "model_required": check == "agent-behavior",
        }

    def test_optional_agent_is_not_run_and_missing_requested_key_fails(self):
        with (
            mock.patch.dict(os.environ, {}, clear=True),
            mock.patch.object(run_validation.docker_launcher, "launch") as launch,
        ):
            args = self.options(Path("unused"))
            result = run_validation.run_check(
                self.entry(), args, Path("unused"), Path("source")
            )
            self.assertEqual(result["status"], "not_run")
            args.run_agent = True
            args.model = "model"
            result = run_validation.run_check(
                self.entry(), args, Path("unused"), Path("source")
            )
            self.assertEqual(result["status"], "failed")
            launch.assert_not_called()

    def test_green_exit_without_evidence_is_not_a_pass(self):
        with (
            tempfile.TemporaryDirectory() as temporary,
            mock.patch.object(run_validation.docker_launcher, "launch", return_value=0),
        ):
            output = Path(temporary) / "check"
            result = run_validation.run_check(
                self.entry("checks"), self.options(output), output, Path(temporary)
            )
            self.assertEqual(result["status"], "failed")

    def test_mismatched_report_fails_and_platform_partial_is_retained(self):
        with (
            tempfile.TemporaryDirectory() as temporary,
            mock.patch.object(
                run_validation.docker_launcher, "launch", return_value=0
            ) as launch,
        ):
            output = Path(temporary) / "check"
            report = output / "evidence/summary.json"
            run_validation.write_json(report, {"check": "blender", "status": "passed"})
            self.assertEqual(
                run_validation.run_check(
                    self.entry("checks"), self.options(output), output, Path(temporary)
                )["status"],
                "failed",
            )
            run_validation.write_json(report, {"check": "checks", "status": "partial"})
            self.assertEqual(
                run_validation.run_check(
                    self.entry("checks"), self.options(output), output, Path(temporary)
                )["status"],
                "partial",
            )
            self.assertEqual(launch.call_args.kwargs["target"], "core")
            self.assertTrue(launch.call_args.kwargs["all_public"])
            self.assertEqual(
                launch.call_args.kwargs["entrypoint"], "scripts/validation_ci.py"
            )

    def test_aggregate_does_not_hide_errors_or_omitted_checks(self):
        for states, expected in [
            (["passed"], "passed"),
            (["passed", "partial"], "partial"),
            (["passed", "not_run"], "partial"),
            (["passed", "error"], "failed"),
            ([], "not_run"),
        ]:
            with self.subTest(states=states):
                self.assertEqual(
                    run_validation.aggregate([{"status": state} for state in states]),
                    expected,
                )

    def test_planning_writes_no_execution_claims_and_never_starts_docker(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "source"
            root.mkdir()
            output = Path(temporary) / "plan"
            with (
                mock.patch.object(
                    run_validation, "make_plan", return_value={"checks": []}
                ),
                mock.patch.object(run_validation, "run_check") as check,
            ):
                self.assertEqual(
                    run_validation.run(self.options(output, plan_only=True), root), 0
                )
            check.assert_not_called()
            self.assertTrue((output / "plan.json").is_file())
            self.assertFalse((output / "summary.json").exists())

    def test_source_drift_between_checks_fails_the_aggregate(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "source"
            root.mkdir()
            output = Path(temporary) / "result"
            plan = {
                "layer": "full",
                "source_revision": "base",
                "checks": [self.entry("checks"), self.entry("blender")],
                "manual_evidence": [],
                "behavior_coverage": {"skills_without_cases": []},
            }

            def check(entry, args, folder, source):
                run_validation.write_json(
                    folder / "source-manifest.json", {"source.py": entry["id"]}
                )
                return {"id": entry["id"], "status": "passed"}

            with (
                mock.patch.object(run_validation, "make_plan", return_value=plan),
                mock.patch.object(run_validation, "run_check", side_effect=check),
            ):
                self.assertEqual(run_validation.run(self.options(output), root), 1)
            summary = json.loads((output / "summary.json").read_text())
            self.assertEqual(summary["status"], "failed")
            self.assertIn("Source changed", summary["checks"][1]["reason"])


if __name__ == "__main__":
    unittest.main()
