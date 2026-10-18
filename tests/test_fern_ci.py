"""Regressions for evidence failures in the Docker-only Fern agent runner."""

import json
import os
import shutil
import sys
import tempfile
import time
import tomllib
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import fern_ci


class FernRunnerTests(unittest.TestCase):
    @staticmethod
    def permission_commands():
        names = (
            "config:agents.max_concurrent_threads_per_session",
            "config:agents.default_subagent_model",
            "config:agents.default_subagent_reasoning_effort",
            "config:tools.update_plan.enabled",
        )
        return [
            [
                {
                    "type": "command_execution",
                    "command": "python skill/scripts/install.py --project project",
                    "aggregated_output": json.dumps(
                        {
                            "check": False,
                            "results": [
                                {
                                    "name": name,
                                    "status": "failed" if first else "added",
                                    "reason": "[Errno 13] Permission denied"
                                    if first
                                    else "",
                                }
                                for name in names
                            ],
                        }
                    ),
                }
            ]
            for first in (True, False)
        ]

    def test_incomplete_or_failed_turn_cannot_pass(self):
        for events in (
            [],
            [{"type": "thread.started", "thread_id": "abc"}],
            [{"type": "turn.failed"}, {"type": "turn.completed"}],
            [{"type": "error"}, {"type": "turn.completed"}],
            ["not an event"],
        ):
            with self.subTest(events=events), self.assertRaises(ValueError):
                fern_ci.parse_events("\n".join(json.dumps(event) for event in events))

    def test_failed_tool_command_can_be_evidence_in_completed_turn(self):
        events = [
            {
                "type": "item.completed",
                "item": {
                    "type": "command_execution",
                    "exit_code": 1,
                    "aggregated_output": "PermissionError: denied",
                },
            },
            {"type": "turn.completed"},
        ]
        self.assertEqual(
            fern_ci.parse_events("\n".join(map(json.dumps, events))), events
        )

    def test_schema_requires_every_criterion_and_rejects_extra_keys(self):
        schema = fern_ci.assessment_schema([{"id": "ownership"}, {"id": "receipt"}])
        criteria = schema["properties"]["criteria"]
        self.assertEqual(criteria["required"], ["ownership", "receipt"])
        self.assertFalse(criteria["additionalProperties"])
        self.assertEqual(
            criteria["properties"]["receipt"]["required"],
            ["status", "reason", "evidence"],
        )

    def test_permission_claim_without_tool_failure_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "No observed OS"):
            fern_ci.permission_assertions(
                [{}, {}],
                [
                    [{"type": "agent_message", "aggregated_output": "PermissionError"}],
                    [],
                ],
            )

    def test_permission_tool_text_without_installer_execution_is_rejected(self):
        expected = "python skill/scripts/install.py --project project"
        for command in (
            f"echo fabricated-json # {expected}",
            f"echo '{expected}'",
            f"python -c \"print('{expected}')\"",
            ["python", "-c", f"print({expected!r})"],
            ["echo", expected],
            f'/bin/bash -lc "echo fabricated-json # {expected}"',
            f"/bin/bash -lc \"python -c 'print({expected!r})'\"",
            expected + " --check",
            expected.replace("--project project", "--project other-project"),
            expected.replace("--project project", "--project /other/project"),
            expected.replace("--project project", "--project ../project"),
            expected + " # ignored",
            expected + "; echo fabricated-json",
            "python skill/scripts/install.py --project 'project",
        ):
            with self.subTest(command=command):
                commands = self.permission_commands()
                commands[0][0]["command"] = command
                with self.assertRaisesRegex(ValueError, "No observed OS"):
                    fern_ci.permission_assertions([{}, {}], commands)

    def test_permission_accepts_direct_installer_argv_and_bash_wrapper(self):
        direct = ["python", "skill/scripts/install.py", "--project", "project"]
        for command in (
            direct,
            " ".join(direct),
            "/usr/local/bin/python3.11 ./skill/scripts/install.py --project ./project",
            ["/bin/bash", "-lc", " ".join(direct)],
            "/bin/bash -lc 'python3 skill/scripts/install.py --project project'",
        ):
            with self.subTest(command=command):
                self.assertTrue(fern_ci.permission_installer_command(command))

    def test_permission_retry_must_execute_installer(self):
        commands = self.permission_commands()
        commands[1][0]["command"] = "python -c 'edit_config_manually()'"
        with self.assertRaisesRegex(ValueError, "Retry did not observe installer"):
            fern_ci.permission_assertions([{}, {}], commands)

    def test_permission_retry_detects_same_bytes_rewritten(self):
        first = {
            f"project/.codex/agents/role-{i}.toml": {
                "sha256": "same",
                "inode": i,
                "mtime_ns": 1,
            }
            for i in range(7)
        }
        first["project/AGENTS.md"] = {"sha256": "rules", "inode": 8, "mtime_ns": 1}
        second = {key: dict(value) for key, value in first.items()}
        commands = self.permission_commands()
        fern_ci.permission_assertions([first, second], commands)
        second["project/.codex/agents/role-0.toml"]["mtime_ns"] = 2
        with self.assertRaisesRegex(ValueError, "modified an already-applied"):
            fern_ci.permission_assertions([first, second], commands)

    def test_permission_retry_detects_rewritten_root_instructions(self):
        first = {
            f"project/.codex/agents/role-{i}.toml": {"mtime_ns": 1} for i in range(7)
        }
        first["project/AGENTS.md"] = {"mtime_ns": 1}
        second = {key: dict(value) for key, value in first.items()}
        second["project/AGENTS.md"]["mtime_ns"] = 2
        with self.assertRaisesRegex(ValueError, "already-applied root instructions"):
            fern_ci.permission_assertions([first, second], self.permission_commands())

    @unittest.skipUnless(
        sys.platform == "linux"
        and hasattr(os, "getuid")
        and os.getuid() == 0
        and os.environ.get("FERN_VALIDATION_CONTAINER") == "1",
        "Disposable container root with dedicated worker UID",
    )
    def test_permission_installer_failure_repair_and_repeat_as_worker_uid(self):
        definition = next(
            case
            for case in fern_ci.behavior_trials.read_json(fern_ci.behavior_trials.SPEC)[
                "cases"
            ]
            if case["id"] == "fern-permission-retry"
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            root.chmod(0o755)
            workspace = root / "workspace"
            workspace.mkdir()
            shutil.copytree(
                fern_ci.ROOT / "skills/fern/setup-fern", workspace / "skill"
            )
            for name, content in definition["files"].items():
                path = workspace / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content.encode("utf-8"))
            fern_ci.owned_tree(workspace, fern_ci.WORKER)
            config = workspace / "project/.codex/config.toml"
            original = config.read_bytes()
            fern_ci.permission_fixture(workspace)
            command = [
                sys.executable,
                "skill/scripts/install.py",
                "--project",
                "project",
            ]

            def invoke():
                result = fern_ci.run_process(
                    command, workspace, os.environ.copy(), 10, uid=fern_ci.WORKER
                )
                self.assertFalse(result["timed_out"])
                self.assertIsNone(result["cleanup_error"])
                self.assertEqual(result["stderr"], "")
                report = json.loads(result["stdout"])
                event = {
                    "type": "command_execution",
                    "command": command,
                    "aggregated_output": result["stdout"],
                }
                return result, report, [event]

            first_result, first_report, first_commands = invoke()
            self.assertEqual(first_result["returncode"], 1)
            self.assertEqual(config.read_bytes(), original)
            statuses = {
                item["name"]: item["status"] for item in first_report["results"]
            }
            self.assertEqual(statuses["instructions:user-rules"], "added")
            for source in (workspace / "skill/assets/codex/agents").glob("*.toml"):
                target = workspace / "project/.codex/agents" / source.name
                self.assertEqual(target.read_bytes(), source.read_bytes())
                self.assertEqual(statuses[f"agents/{source.name}"], "added")
            first_stats = fern_ci.stats(workspace)
            fern_ci.permission_fixture(workspace, repair=True)
            retry_result, _, retry_commands = invoke()
            self.assertEqual(retry_result["returncode"], 0)
            second_stats = fern_ci.stats(workspace)
            fern_ci.permission_assertions(
                [first_stats, second_stats], [first_commands, retry_commands]
            )
            parsed = tomllib.loads(config.read_text())
            self.assertEqual(parsed["agents"]["max_concurrent_threads_per_session"], 4)
            self.assertEqual(parsed["agents"]["default_subagent_model"], "gpt-6.1-sol")
            self.assertEqual(
                parsed["agents"]["default_subagent_reasoning_effort"], "high"
            )
            self.assertIs(parsed["tools"]["update_plan"]["enabled"], True)
            self.assertEqual(parsed["model"], "personal-model")
            self.assertEqual(parsed["agents"]["max_depth"], 2)
            repeated_result, repeated_report, _ = invoke()
            self.assertEqual(repeated_result["returncode"], 0)
            self.assertTrue(
                all(
                    item["status"] == "unchanged" for item in repeated_report["results"]
                )
            )
            self.assertEqual(fern_ci.stats(workspace), second_stats)
            self.assertFalse((workspace / "project/.codex/fern").exists())

    def test_missing_auth_is_an_error_before_preparation(self):
        with (
            patch.dict(os.environ, {}, clear=True),
            self.assertRaisesRegex(ValueError, "CODEX_API_KEY"),
        ):
            fern_ci.run_behavior(Path("unused"), "model", [], 1)

    def test_generic_selection_keeps_only_exact_requested_skills(self):
        cases = fern_ci.select_behavior_cases(
            ["reflect-empty", "unslop-english", "fern-read-only"], all_skills=True
        )
        self.assertEqual(
            {case["id"] for case in cases},
            {"reflect-empty", "unslop-english", "fern-read-only"},
        )
        self.assertEqual(
            {case["skill"] for case in cases}, {"reflect", "unslop", "setup-fern"}
        )
        self.assertTrue(
            all(
                case["skill"] == "setup-fern"
                for case in fern_ci.select_behavior_cases([])
            )
        )
        with self.assertRaisesRegex(ValueError, "setup-fern"):
            fern_ci.select_behavior_cases(["unslop-english"])

    def test_generic_selection_rejects_unknown_empty_and_duplicate_requests(self):
        for cases in (
            [],
            ["unslop-*"],
            ["missing-case"],
            ["reflect-empty", "missing-case"],
            ["reflect-empty", "reflect-empty"],
            "reflect-empty",
            [None],
        ):
            with self.subTest(cases=cases), self.assertRaises(ValueError):
                fern_ci.select_behavior_cases(cases, all_skills=True)

    def test_empty_preparation_cannot_produce_vacuous_pass(self):
        with tempfile.TemporaryDirectory() as temporary:
            with (
                patch.dict(os.environ, {"CODEX_API_KEY": "synthetic"}),
                patch.object(fern_ci.Path, "mkdir"),
                patch.object(fern_ci.Path, "chmod"),
                patch.object(fern_ci.os, "chown", create=True),
                patch.object(fern_ci.behavior_trials, "prepare", return_value=[]),
                patch.object(fern_ci, "run_case") as run_case,
                self.assertRaisesRegex(ValueError, "Prepared trials do not match"),
            ):
                fern_ci.run_behavior(
                    Path(temporary), "model", ["reflect-empty"], 1, all_skills=True
                )
            run_case.assert_not_called()

    def test_generic_runner_executes_and_reports_selected_cases_only(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            selected = ["reflect-empty", "unslop-english"]
            prepared = []
            for case in selected:
                trial = output / "trials" / case
                trial.mkdir(parents=True)
                fern_ci.write_json(trial / "manifest.json", {"case": case})
                prepared.append(str(trial))
            with (
                patch.dict(os.environ, {"CODEX_API_KEY": "synthetic"}),
                patch.object(fern_ci.Path, "mkdir"),
                patch.object(fern_ci.Path, "chmod"),
                patch.object(fern_ci.os, "chown", create=True),
                patch.object(
                    fern_ci.behavior_trials, "prepare", return_value=prepared
                ) as prepare,
                patch.object(
                    fern_ci,
                    "run_case",
                    side_effect=lambda trial, model, timeout: {
                        "case": trial.name,
                        "outcome": "passed",
                    },
                ) as run_case,
            ):
                result = fern_ci.run_behavior(
                    output, "synthetic-model", selected, 3, all_skills=True
                )
            self.assertEqual(result["status"], "passed")
            self.assertEqual(result["selected_cases"], selected)
            self.assertEqual(result["skills"], ["reflect", "unslop"])
            self.assertEqual(result["requested_model"], "synthetic-model")
            self.assertFalse(result["runtime_model_verified"])
            self.assertEqual(run_case.call_count, 2)
            prepare.assert_called_once_with(output / "trials", selected)

    def test_worker_delivery_preserves_context_without_loading_negative_skill(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workspace = root / "workspace"
            (workspace / "skill").mkdir(parents=True)
            inputs = {
                "context": "Read project records; no edits or network.",
                "turns": ["What is the current endpoint?", "Second request only."],
            }
            for case, supplied in (
                ("reflect-empty", True),
                ("reflect-stale-recall", False),
            ):
                trial = root / case
                trial.mkdir()
                with (
                    patch.object(fern_ci, "owned_tree") as ownership,
                    patch.object(fern_ci.Path, "chmod") as mode,
                ):
                    delivery, prompt = fern_ci.worker_delivery(trial, workspace, inputs)
                self.assertEqual(delivery["skill_readable_by_worker"], supplied)
                self.assertIn(inputs["context"], prompt)
                self.assertIn(inputs["turns"][0], prompt)
                self.assertNotIn(inputs["turns"][1], prompt)
                if supplied:
                    self.assertIn("Read skill/SKILL.md", prompt)
                    ownership.assert_not_called()
                else:
                    self.assertNotIn("skill/SKILL.md", prompt)
                    self.assertIn("AGENTS.md", prompt)
                    ownership.assert_called_once_with(
                        workspace / "skill", 0, writable=False
                    )
                    mode.assert_called_once_with(0o700)
                self.assertFalse(delivery["native_discovery_verified"])
                self.assertEqual(
                    json.loads((trial / "delivery.json").read_text()), delivery
                )

    @unittest.skipUnless(
        sys.platform == "linux"
        and hasattr(os, "getuid")
        and os.getuid() == 0
        and os.environ.get("FERN_VALIDATION_CONTAINER") == "1",
        "Disposable container root with dedicated worker UID",
    )
    def test_negative_control_skill_is_unreadable_to_actual_worker_uid(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            root.chmod(0o755)
            workspace = root / "workspace"
            skill = workspace / "skill"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("Must not be supplied to recall worker.")
            fern_ci.owned_tree(workspace, fern_ci.WORKER)
            trial = root / "reflect-stale-recall"
            trial.mkdir()
            fern_ci.worker_delivery(
                trial,
                workspace,
                {"context": "Read ordinary project context.", "turns": ["Recall."]},
            )
            result = fern_ci.run_process(
                [
                    sys.executable,
                    "-c",
                    f"from pathlib import Path; Path({str(skill / 'SKILL.md')!r}).read_text()",
                ],
                workspace,
                os.environ.copy(),
                3,
                uid=fern_ci.WORKER,
            )
            self.assertNotEqual(result["returncode"], 0)
            self.assertIn("PermissionError", result["stderr"])
            self.assertTrue((skill / "SKILL.md").is_file())

    def test_artifacts_redact_runtime_key_even_in_workspace_copy(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "worker.json").write_text('"fake-test-secret"')
            with patch.dict(os.environ, {"CODEX_API_KEY": "fake-test-secret"}):
                fern_ci.scrub_artifacts(root)
            self.assertEqual((root / "worker.json").read_text(), '"[REDACTED]"')

    @unittest.skipUnless(sys.platform == "linux", "Linux process-group cleanup")
    def test_successful_exit_stops_background_writes_before_snapshot(self):
        with tempfile.TemporaryDirectory() as temporary:
            marker = Path(temporary) / "late-write"
            child = (
                "import time; from pathlib import Path; time.sleep(0.5); "
                f"Path({str(marker)!r}).write_text('late')"
            )
            parent = (
                "import subprocess,sys; "
                f"subprocess.Popen([sys.executable, '-c', {child!r}], "
                "stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)"
            )
            result = fern_ci.run_process(
                [sys.executable, "-c", parent], Path(temporary), os.environ.copy(), 2
            )
            self.assertEqual(result["returncode"], 0)
            time.sleep(0.7)
            self.assertFalse(marker.exists())

    @unittest.skipUnless(
        sys.platform == "linux"
        and hasattr(os, "getuid")
        and os.getuid() == 0
        and os.environ.get("FERN_VALIDATION_CONTAINER") == "1",
        "Disposable container root with dedicated worker UID",
    )
    def test_detached_agent_tools_stop_before_snapshot(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            os.chown(root, fern_ci.WORKER, fern_ci.WORKER)
            root.chmod(0o755)
            marker = root / "detached-write"
            child = (
                "import time; from pathlib import Path; time.sleep(0.5); "
                f"Path({str(marker)!r}).write_text('late')"
            )
            parent = (
                "import subprocess,sys; "
                f"subprocess.Popen([sys.executable, '-c', {child!r}], "
                "start_new_session=True, stdin=subprocess.DEVNULL, "
                "stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)"
            )
            result = fern_ci.run_process(
                [sys.executable, "-c", parent],
                root,
                os.environ.copy(),
                2,
                uid=fern_ci.WORKER,
            )
            self.assertEqual(result["returncode"], 0)
            self.assertIsNone(result["cleanup_error"])
            time.sleep(0.7)
            self.assertFalse(marker.exists())

    @unittest.skipUnless(sys.platform == "linux", "Linux process-group cleanup")
    def test_timeout_preserves_partial_evidence_and_terminates(self):
        result = fern_ci.run_process(
            [
                sys.executable,
                "-c",
                "import time; print('started', flush=True); time.sleep(20)",
            ],
            Path.cwd(),
            os.environ.copy(),
            0.2,
        )
        self.assertTrue(result["timed_out"])
        self.assertNotEqual(result["returncode"], 0)
        self.assertIn("started", result["stdout"])

    @unittest.skipUnless(
        sys.platform == "linux"
        and hasattr(os, "getuid")
        and os.getuid() == 0
        and os.environ.get("FERN_VALIDATION_CONTAINER") == "1",
        "Disposable container root with dedicated worker UID",
    )
    def test_timeout_closes_pipes_held_by_detached_agent_tool(self):
        parent = (
            "import subprocess,sys,time; "
            "subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(20)'], "
            "start_new_session=True); print('started', flush=True); time.sleep(20)"
        )
        started = time.monotonic()
        result = fern_ci.run_process(
            [sys.executable, "-c", parent],
            Path("/tmp"),
            os.environ.copy(),
            0.2,
            uid=fern_ci.WORKER,
        )
        self.assertLess(time.monotonic() - started, 5)
        self.assertTrue(result["timed_out"])
        self.assertIsNone(result["cleanup_error"])
        self.assertIn("started", result["stdout"])

    @unittest.skipUnless(
        sys.platform == "linux"
        and hasattr(os, "getuid")
        and os.getuid() == 0
        and os.environ.get("FERN_VALIDATION_CONTAINER") == "1",
        "Disposable container root with dedicated worker UID",
    )
    def test_agent_invocation_retains_events_and_resumes_with_same_home(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            root.chmod(0o755)
            binary = root / "codex"
            binary.write_text(
                f"#!{sys.executable}\n"
                "import json, os, pathlib, sys\n"
                "args = sys.argv[1:]\n"
                "sys.stdin.read()\n"
                "final = pathlib.Path(args[args.index('--output-last-message') + 1])\n"
                "final.write_text('synthetic reply uid=' + str(os.getuid()))\n"
                "print(json.dumps({'type':'thread.started','thread_id':'synthetic-session'}))\n"
                "print(json.dumps({'type':'turn.completed'}))\n",
                encoding="utf-8",
            )
            binary.chmod(0o755)
            workspace = root / "workspace"
            workspace.mkdir()
            with patch.dict(
                os.environ,
                {
                    "PATH": f"{root}:{os.environ['PATH']}",
                    "CODEX_API_KEY": "synthetic-no-network-key",
                },
            ):
                first, session, _ = fern_ci.invoke_agent(
                    workspace,
                    root / "home",
                    fern_ci.WORKER,
                    "first",
                    "synthetic-model",
                    3,
                    root / "evidence-1",
                )
                second, resumed, _ = fern_ci.invoke_agent(
                    workspace,
                    root / "home",
                    fern_ci.WORKER,
                    "second",
                    "synthetic-model",
                    3,
                    root / "evidence-2",
                    session=session,
                )
            self.assertEqual(first, f"synthetic reply uid={fern_ci.WORKER}")
            self.assertEqual(first, second)
            self.assertEqual(resumed, session)
            process = json.loads((root / "evidence-2/process.json").read_text())
            self.assertEqual(process["command"][-3:], ["resume", session, "-"])
            self.assertTrue((root / "evidence-1/events.jsonl").is_file())
            self.assertEqual((root / "evidence-1/prompt.txt").read_text(), "first")


if __name__ == "__main__":
    unittest.main()
