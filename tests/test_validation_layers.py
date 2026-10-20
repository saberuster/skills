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

import yaml

from scripts import run_validation, validation_plan
from scripts.check_markdown_links import check_markdown_links


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

    def test_plugin_manifest_changes_select_only_their_collection(self):
        for path, expected in (
            (".agents/plugins/marketplace.json", ["setup-fern"]),
            ("skills/fern/.codex-plugin/plugin.json", ["setup-fern"]),
            ("skills/blender/.codex-plugin/plugin.json", ["reference-scene"]),
        ):
            with (
                self.subTest(path=path),
                mock.patch.object(
                    validation_plan, "changed_paths", return_value=("base", [path])
                ),
            ):
                plan = self.plan(base="main")
            self.assertEqual(plan["selected_skills"], expected)

    def test_fern_plugin_host_evidence_remains_not_run(self):
        with mock.patch.object(
            validation_plan,
            "changed_paths",
            return_value=("base", [".agents/plugins/marketplace.json"]),
        ):
            plan = self.plan(base="main")
        plugin = next(
            item
            for item in plan["manual_evidence"]
            if item["scope"] == "fern-plugin-host"
        )
        self.assertEqual(plugin["skills"], ["setup-fern"])
        self.assertEqual(plugin["status"], "not_run")
        self.assertIn("Windows", plugin["reason"])
        self.assertIn("fern-plugin", {item["check"] for item in plan["checks"]})

    def test_docker_context_selected_only_for_affected_filtering_inputs(self):
        for path, expected in (
            ("scripts/fern-ci/Dockerfile.dockerignore", True),
            ("scripts/validation-ci/Dockerfile.dockerignore", True),
            ("scripts/run_fern_validation.py", True),
            ("scripts/check_docker_context.py", True),
            (".agents/plugins/marketplace.json", True),
            ("skills/fern/setup-fern/SKILL.md", False),
            ("scripts/unrelated.py", False),
            ("docs/plugins.md", False),
        ):
            with (
                self.subTest(path=path),
                mock.patch.object(
                    validation_plan, "changed_paths", return_value=("base", [path])
                ),
            ):
                checks = {item["check"] for item in self.plan(base="main")["checks"]}
                self.assertEqual("docker-context" in checks, expected)

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

    def test_ci_model_shards_gate_exact_cases_on_same_invocation_preflight(self):
        workflows = validation_plan.ROOT / ".github/workflows"
        for filename in ("validation-runtime.yml", "validation-full.yml"):
            jobs = yaml.load(
                (workflows / filename).read_text("ascii"), Loader=yaml.BaseLoader
            )["jobs"]
            steps = jobs["behavior"]["steps"]
            step = next(item for item in steps if "CASES" in item.get("env", {}))
            script = step["run"].split("python - <<'PY'\n", 1)[1].rsplit("\nPY", 1)[0]
            # Runtime jobs keep their independent schedule; only model shards
            # repeat the cheap checks against their own immutable checkout.
            runtime = jobs.get("runtime", jobs.get("extended"))
            self.assertNotIn("behavior", runtime.get("needs", []))
            for preflight in ("failed", "passed", "partial"):
                with self.subTest(workflow=filename, preflight=preflight):
                    guide = self.root / "guide.md"
                    guide.unlink(missing_ok=True)
                    (self.root / "README.md").write_text("[Guide](guide.md)\n")
                    if preflight != "failed":
                        guide.write_text("Guide\n")
                    output = Path(self.temporary.name) / f"{filename}-{preflight}"
                    seen = []
                    real_run = run_validation.run

                    def check(entry, args, folder, source):
                        seen.append(entry["check"])
                        if entry["check"] == "checks":
                            findings = check_markdown_links(source)
                            self.assertEqual(bool(findings), preflight == "failed")
                            status = "failed" if findings else preflight
                        else:
                            self.assertEqual(entry["check"], "agent-behavior")
                            self.assertEqual(entry["cases"], ["reflect-one"])
                            status = "passed"  # Dispatch stub, not a model trial.
                        return {"id": entry["id"], "status": status}

                    def dispatch(command):
                        self.assertEqual(
                            command[:2], [sys.executable, "scripts/run_validation.py"]
                        )
                        with mock.patch.object(
                            run_validation,
                            "run",
                            side_effect=lambda args: real_run(args, self.root),
                        ):
                            return run_validation.main(command[2:])

                    with (
                        mock.patch.dict(
                            os.environ,
                            {
                                "MODEL": "fixture",
                                "CASES": '["reflect-one"]',
                                "RUNNER_TEMP": str(output),
                            },
                        ),
                        mock.patch.object(subprocess, "call", side_effect=dispatch),
                        mock.patch.object(
                            run_validation, "run_check", side_effect=check
                        ),
                        self.assertRaises(SystemExit) as exit_result,
                    ):
                        exec(compile(script, filename, "exec"), {})
                    self.assertEqual(
                        exit_result.exception.code, int(preflight == "failed")
                    )
                    summary = json.loads(
                        (output / "behavior-evidence/summary.json").read_text()
                    )
                    self.assertEqual(
                        [item["id"] for item in summary["checks"]],
                        ["checks", "agent-behavior"],
                    )
                    self.assertEqual(summary["behavior_coverage"]["selected_cases"], 1)
                    if preflight == "failed":
                        self.assertEqual(seen, ["checks"])
                        blocked = summary["checks"][-1]
                        self.assertEqual(blocked["status"], "not_run")
                        self.assertEqual(blocked["cases"], ["reflect-one"])
                        self.assertIn("Deterministic checks failed", blocked["reason"])
                        self.assertEqual(summary["status"], "failed")
                        self.assertEqual(summary["coverage_status"], "incomplete")
                    else:
                        self.assertEqual(seen, ["checks", "agent-behavior"])


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

    def test_host_context_check_bypasses_container_and_requires_valid_report(self):
        with (
            tempfile.TemporaryDirectory() as temporary,
            mock.patch.object(run_validation.docker_launcher, "launch") as launch,
            mock.patch.object(run_validation.check_docker_context, "run") as host,
        ):
            output = Path(temporary) / "context"
            valid = {
                "check": "docker-context",
                "status": "passed",
                "source_hashes": {"filter": "a" * 64},
            }
            for payload, expected in (
                (valid, "passed"),
                ({**valid, "status": "not_run"}, "failed"),
                ({**valid, "source_hashes": {}}, "failed"),
                ({**valid, "check": "checks"}, "failed"),
                ([], "failed"),
            ):
                run_validation.write_json(output / "evidence/summary.json", payload)
                host.return_value = valid
                result = run_validation.run_check(
                    self.entry("docker-context"),
                    self.options(output),
                    output,
                    Path(temporary) / "source",
                )
                self.assertEqual(result["status"], expected)
            launch.assert_not_called()

    def test_fern_plugin_uses_container_runtime(self):
        with (
            tempfile.TemporaryDirectory() as temporary,
            mock.patch.object(
                run_validation.docker_launcher, "launch", return_value=0
            ) as launch,
            mock.patch.object(run_validation.check_docker_context, "run") as host,
        ):
            output = Path(temporary) / "plugin"
            run_validation.write_json(
                output / "evidence/summary.json",
                {"check": "fern-plugin", "status": "passed"},
            )
            result = run_validation.run_check(
                self.entry("fern-plugin"), self.options(output), output, Path(temporary)
            )
            self.assertEqual(result["status"], "passed")
            self.assertIn("fern-plugin", launch.call_args.kwargs["entrypoint_args"])
            host.assert_not_called()

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

    def test_broken_reference_blocks_expensive_checks_without_hiding_selection(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "source"
            root.mkdir()
            (root / "README.md").write_text("[Guide](missing.md)\n")
            output = Path(temporary) / "result"
            entries = [
                self.entry(name)
                for name in ("checks", "codex-discovery", "blender", "agent-behavior")
            ]
            plan = {
                "layer": "full",
                "source_revision": "base",
                "checks": entries,
                "manual_evidence": [],
                "behavior_coverage": {"skills_without_cases": []},
            }

            def check(entry, args, folder, source):
                self.assertEqual(entry["check"], "checks")
                findings = check_markdown_links(source)
                self.assertEqual(len(findings), 1)
                self.assertEqual(findings[0].target, "missing.md")
                run_validation.write_json(
                    folder / "evidence/summary.json",
                    {"status": "failed", "reason": findings[0].message},
                )
                return {"id": entry["id"], "status": "failed", "exit_code": 1}

            with (
                mock.patch.object(run_validation, "make_plan", return_value=plan),
                mock.patch.object(
                    run_validation, "run_check", side_effect=check
                ) as run,
            ):
                self.assertEqual(
                    run_validation.run(
                        self.options(output, run_agent=True, model="fixture"), root
                    ),
                    1,
                )
            run.assert_called_once()
            summary = json.loads((output / "summary.json").read_text())
            self.assertEqual(summary["status"], "failed")
            self.assertEqual(summary["coverage_status"], "incomplete")
            self.assertEqual(
                [item["id"] for item in summary["checks"]],
                [item["id"] for item in entries],
            )
            for item in summary["checks"][1:]:
                self.assertEqual(item["status"], "not_run")
                self.assertIn("Deterministic checks failed", item["reason"])
            self.assertEqual(summary["checks"][-1]["cases"], ["one"])
            self.assertTrue((output / "checks/evidence/summary.json").is_file())

    def test_success_partial_and_runtime_failure_do_not_gate_independent_checks(self):
        for first_check, first_status, expected in (
            ("checks", "passed", 0),
            ("checks", "partial", 0),
            ("codex-discovery", "failed", 1),
        ):
            with (
                self.subTest(check=first_check, status=first_status),
                tempfile.TemporaryDirectory() as temporary,
            ):
                root = Path(temporary) / "source"
                root.mkdir()
                output = Path(temporary) / "result"
                plan = {
                    "layer": "full",
                    "source_revision": "base",
                    "checks": [self.entry(first_check), self.entry("blender")],
                    "manual_evidence": [],
                    "behavior_coverage": {"skills_without_cases": []},
                }
                with (
                    mock.patch.object(run_validation, "make_plan", return_value=plan),
                    mock.patch.object(
                        run_validation,
                        "run_check",
                        side_effect=[
                            {"id": first_check, "status": first_status},
                            {"id": "blender", "status": "passed"},
                        ],
                    ) as run,
                ):
                    self.assertEqual(
                        run_validation.run(self.options(output), root), expected
                    )
                self.assertEqual(run.call_count, 2)
                summary = json.loads((output / "summary.json").read_text())
                self.assertEqual(summary["checks"][-1]["status"], "passed")

    def test_host_hashes_detect_drift_against_container_snapshot_in_either_order(self):
        for order in (("checks", "docker-context"), ("docker-context", "checks")):
            with self.subTest(order=order), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary) / "source"
                root.mkdir()
                output = Path(temporary) / "result"
                plan = {
                    "layer": "full",
                    "source_revision": "base",
                    "checks": [self.entry(name) for name in order],
                    "manual_evidence": [],
                    "behavior_coverage": {"skills_without_cases": []},
                }

                def check(entry, args, folder, source):
                    result = {"id": entry["id"], "status": "passed"}
                    if entry["id"] == "docker-context":
                        result["source_hashes"] = {"filter": "b" * 64}
                    else:
                        run_validation.write_json(
                            folder / "source-manifest.json",
                            {"filter": "a" * 64, "unrelated": "c" * 64},
                        )
                    return result

                with (
                    mock.patch.object(run_validation, "make_plan", return_value=plan),
                    mock.patch.object(run_validation, "run_check", side_effect=check),
                ):
                    self.assertEqual(run_validation.run(self.options(output), root), 1)
                summary = json.loads((output / "summary.json").read_text())
                self.assertIn("Source changed", summary["checks"][1]["reason"])


if __name__ == "__main__":
    unittest.main()
