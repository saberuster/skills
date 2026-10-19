"""Synthetic native plugin protocol regressions; no CLI, model, or Docker calls."""

import copy
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import check_fern_plugin as probe


class FernPluginTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.repo = self.root / "repo"
        self.plugin = self.repo / probe.PLUGIN
        self.skill = self.plugin / "demo"
        (self.skill / "agents").mkdir(parents=True)
        (self.skill / "SKILL.md").write_text(
            "---\nname: demo\ndescription: Synthetic skill.\n---\nDo work.\n",
            encoding="ascii",
        )
        (self.skill / "agents/openai.yaml").write_text(
            "policy:\n  allow_implicit_invocation: false\n", encoding="ascii"
        )
        (self.skill / "resource.txt").write_text(
            "Complete resource.\n", encoding="ascii"
        )
        self.manifest = {
            "name": "fern",
            "version": "1.3.7",
            "interface": {"websiteURL": "https://example.com/fern"},
            "skills": ["./demo"],
        }
        self.marketplace = {
            "name": "synthetic-market",
            "plugins": [
                {"name": "fern", "source": {"source": "local", "path": "./skills/fern"}}
            ],
        }
        self.write_manifests()
        self.expected = probe.candidate(self.repo)

    def write_manifests(self):
        (self.plugin / ".codex-plugin").mkdir(exist_ok=True)
        (self.plugin / ".codex-plugin/plugin.json").write_text(
            json.dumps(self.manifest), encoding="ascii"
        )
        (self.repo / probe.MARKETPLACE.parent).mkdir(parents=True, exist_ok=True)
        (self.repo / probe.MARKETPLACE).write_text(
            json.dumps(self.marketplace), encoding="ascii"
        )

    def replies(self, project, home):
        expected = self.expected
        cache = (
            home
            / ".codex/plugins/cache"
            / expected["marketplace"]
            / "fern"
            / expected["version"]
        )
        summary = {
            "id": expected["id"],
            "name": "fern",
            "localVersion": expected["version"],
            "installed": True,
            "enabled": True,
            "interface": {"websiteUrl": expected["website"]},
        }
        row = {
            "name": "fern:demo",
            "description": "Synthetic skill.",
            "path": str(project / probe.PLUGIN / "demo/SKILL.md"),
            "enabled": True,
        }
        discovered = dict(
            row,
            path=str(cache / "demo/SKILL.md"),
            scope="user",
            pluginId=expected["id"],
        )
        return {
            "initialize": {"codexHome": str(home / ".codex")},
            "plugin/list": {
                "marketplaceLoadErrors": [],
                "marketplaces": [
                    {
                        "name": expected["marketplace"],
                        "path": str(project / probe.MARKETPLACE),
                        "plugins": [copy.deepcopy(summary)],
                    }
                ],
            },
            "plugin/read": {
                "plugin": {
                    "marketplaceName": expected["marketplace"],
                    "marketplacePath": str(project / probe.MARKETPLACE),
                    "summary": summary,
                    "skills": [row],
                }
            },
            "skills/list": {
                "data": [{"cwd": str(project), "errors": [], "skills": [discovered]}]
            },
        }, cache

    def run_mocked(self, *, cli_failure=False, mutate=None, cleanup_failure=False):
        test = self

        def run_process(command, project, env, timeout):
            arguments = command[1:]
            expected = test.expected
            home = Path(env["HOME"])
            cache = (
                home
                / ".codex/plugins/cache"
                / expected["marketplace"]
                / "fern"
                / expected["version"]
            )
            row = {
                "pluginId": expected["id"],
                "name": "fern",
                "marketplaceName": expected["marketplace"],
                "version": expected["version"],
                "installed": False,
                "enabled": False,
            }
            result = {
                "command": command,
                "returncode": 0,
                "timed_out": False,
                "cleanup_error": None,
                "stdout": "Registered.\n",
                "stderr": "",
            }
            if arguments == ["--version"]:
                result["stdout"] = "codex-cli synthetic\n"
            elif "--available" in arguments:
                result["stdout"] = json.dumps({"available": [row], "installed": []})
            elif arguments[:2] == ["plugin", "add"]:
                shutil.copytree(project / probe.PLUGIN, cache)
                result["stdout"] = json.dumps(dict(row, installedPath=str(cache)))
                if mutate == "cache":
                    (cache / "demo/resource.txt").write_text("Damaged.")
            elif arguments == ["plugin", "list", "--json"]:
                result["stdout"] = json.dumps(
                    {
                        "installed": [dict(row, installed=True, enabled=True)],
                        "available": [],
                    }
                )
            if cli_failure:
                result["returncode"] = 2
            if mutate == "cli-timeout":
                result["timed_out"] = True
            if mutate == "malformed-cli":
                result["stdout"] = "{broken JSON"
            return result

        class FakeServer:
            def __init__(self, command, project, env, timeout):
                self.replies, _ = test.replies(project, Path(env["HOME"]))
                self.stderr = ["Synthetic stderr."]
                self.process = self
                self.code = None
                if mutate == "unexpected":
                    self.replies["skills/list"]["data"][0]["skills"].append(
                        {"name": "leaked-user", "scope": "user"}
                    )
                if mutate == "source":
                    (test.skill / "resource.txt").write_text("Changed source.")

            def request(self, request_id, method, params):
                if mutate == "rpc-error":
                    raise probe.DiscoveryError("Synthetic RPC protocol error")
                if mutate == "early-exit":
                    self.code = 0
                return self.replies[method]

            def send(self, message):
                pass

            def poll(self):
                return self.code

            def close(self):
                self.code = -9
                if cleanup_failure:
                    raise subprocess.TimeoutExpired("Synthetic cleanup failure", 1)

        with (
            patch.object(probe.sys, "platform", "linux"),
            patch.object(probe, "run_process", side_effect=run_process),
            patch.object(
                probe,
                "executable_command",
                side_effect=lambda executable, args: [executable, *args],
            ),
            patch.object(probe, "JsonLineProcess", FakeServer),
        ):
            return probe.check_plugin(self.repo)

    def test_complete_dynamic_candidate_and_controlled_shutdown(self):
        report = self.run_mocked()
        self.assertEqual(report["status"], "passed", report)
        self.assertEqual(report["candidate"]["version"], "1.3.7")
        self.assertEqual(set(report["candidate"]["skills"]), {"demo"})
        self.assertEqual(report["processes"][-1]["returncode"], -9)
        self.assertIn("deliberate", report["processes"][-1]["shutdown"])
        self.assertFalse(report["model_requests"])

    def test_cli_nonzero_is_failed(self):
        report = self.run_mocked(cli_failure=True)
        self.assertEqual(report["status"], "failed")
        self.assertEqual(len(report["processes"]), 1)
        self.assertEqual(report["processes"][0]["returncode"], 2)

    def test_full_resource_mismatch_is_failed(self):
        report = self.run_mocked(mutate="cache")
        self.assertEqual(report["status"], "failed")
        self.assertIn("cached plugin bytes", report["errors"][0])

    def test_unexpected_user_skill_is_failed(self):
        report = self.run_mocked(mutate="unexpected")
        self.assertEqual(report["status"], "failed")
        self.assertIn("Unexpected non-system", report["errors"][0])

    def test_candidate_mutation_overrides_success(self):
        report = self.run_mocked(mutate="source")
        self.assertEqual(report["status"], "failed")
        self.assertIn("Candidate source changed", report["errors"][-1])

    def test_cleanup_failure_is_failed(self):
        report = self.run_mocked(cleanup_failure=True)
        self.assertEqual(report["status"], "failed")
        self.assertIn("cleanup failure", report["processes"][-1]["cleanup_error"])

    def test_cli_timeout_or_malformed_json_is_failed(self):
        for mutation in ("cli-timeout", "malformed-cli"):
            with self.subTest(mutation=mutation):
                report = self.run_mocked(mutate=mutation)
                self.assertEqual(report["status"], "failed")
                self.assertTrue(report["errors"])

    def test_protocol_failure_or_early_server_exit_is_failed_and_cleaned_up(self):
        for mutation in ("rpc-error", "early-exit"):
            with self.subTest(mutation=mutation):
                report = self.run_mocked(mutate=mutation)
                self.assertEqual(report["status"], "failed")
                self.assertEqual(report["processes"][-1]["returncode"], -9)
                self.assertIn("failed protocol", report["processes"][-1]["shutdown"])

    def test_rpc_missing_metadata_errors_and_skill_path_escape_are_rejected(self):
        project, home = self.root / "project", self.root / "home"
        for corruption in (
            "website",
            "version",
            "errors",
            "missing",
            "escape",
            "duplicate",
            "home",
        ):
            with self.subTest(corruption=corruption):
                replies, cache = self.replies(project, home)
                if corruption == "website":
                    del replies["plugin/read"]["plugin"]["summary"]["interface"][
                        "websiteUrl"
                    ]
                elif corruption == "version":
                    replies["plugin/read"]["plugin"]["summary"]["localVersion"] = (
                        "0.0.0"
                    )
                elif corruption == "errors":
                    del replies["plugin/list"]["marketplaceLoadErrors"]
                elif corruption == "home":
                    replies["initialize"]["codexHome"] = str(self.root / "real-home")
                else:
                    rows = replies["skills/list"]["data"][0]["skills"]
                    if corruption == "missing":
                        rows.clear()
                    elif corruption == "duplicate":
                        rows.append(copy.deepcopy(rows[0]))
                    else:
                        rows[0]["path"] = str(cache / "../other/demo/SKILL.md")
                with self.assertRaises(probe.DiscoveryError):
                    probe.verify_rpc(replies, self.expected, project, home, cache)

    def test_malformed_cli_json_shape_is_rejected(self):
        for value in ([], {}, {"installed": [], "available": [None]}):
            with self.subTest(value=value), self.assertRaises(probe.DiscoveryError):
                probe.verify_cli_listing(value, self.expected, False)

    def test_every_rpc_result_requires_an_object(self):
        project, home = self.root / "project", self.root / "home"
        for method in ("initialize", "plugin/list", "plugin/read", "skills/list"):
            for malformed in (None, [], "invalid"):
                with self.subTest(method=method, malformed=malformed):
                    replies, cache = self.replies(project, home)
                    replies[method] = malformed
                    with self.assertRaises(probe.DiscoveryError):
                        probe.verify_rpc(replies, self.expected, project, home, cache)

    def test_missing_leaf_and_unsafe_manifest_paths_are_rejected(self):
        for value in ([], ["../demo"], ["./demo", "./demo"]):
            with self.subTest(value=value):
                self.manifest["skills"] = value
                self.write_manifests()
                with self.assertRaises(probe.DiscoveryError):
                    probe.candidate(self.repo)

    def test_non_linux_execution_is_rejected_without_cli(self):
        with (
            patch.object(probe.sys, "platform", "win32"),
            patch.object(probe, "run_process") as run,
        ):
            self.assertEqual(probe.check_plugin(self.repo)["status"], "failed")
            run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
