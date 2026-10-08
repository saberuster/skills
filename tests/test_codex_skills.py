"""Isolated protocol and discovery regressions; no external Codex or model calls."""

import copy
import hashlib
import json
import os
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.check_codex_skills import (
    DiscoveryError,
    JsonLineProcess,
    check_codex,
    discover_expected,
    isolated_environment,
    isolated_project,
    package_sha256,
    verify_discovery,
)


class CodexDiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.repo = self.root / "repo"
        source = self.repo / "skills/demo/SKILL.md"
        source.parent.mkdir(parents=True)
        source.write_text(
            "---\nname: demo\ndescription: Read a synthetic document.\n---\nInstructions.\n",
            encoding="ascii",
        )
        (source.parent / "resource.txt").write_text("Resource.\n", encoding="ascii")
        self.expected = discover_expected(self.repo)
        self.project = self.root / "project"
        self.result = {
            "data": [
                {
                    "cwd": str(self.project),
                    "errors": [],
                    "skills": [
                        {
                            "name": "demo",
                            "description": "Read a synthetic document.",
                            "path": str(self.project / ".agents/skills/demo/SKILL.md"),
                            "enabled": True,
                            "scope": "repo",
                        }
                    ],
                }
            ]
        }

    def test_isolated_copy_preserves_package_and_removes_credentials(self):
        with isolated_project(self.repo) as (project, home):
            self.assertEqual(
                (project / ".agents/skills/demo/resource.txt").read_text(),
                "Resource.\n",
            )
            self.assertTrue((project / ".git").is_dir())
            with patch.dict(
                os.environ, {"OPENAI_API_KEY": "synthetic", "CODEX_HOME": "host"}
            ):
                env = isolated_environment(home)
            self.assertNotIn("OPENAI_API_KEY", env)
            self.assertEqual(Path(env["CODEX_HOME"]), home / ".codex")
            self.assertEqual(Path(env["HOME"]), home)
            self.assertEqual(Path(env["USERPROFILE"]), home)
            self.assertFalse((home / ".codex/auth.json").exists())
        self.assertFalse(project.exists())
        self.assertTrue((self.repo / "skills/demo/resource.txt").exists())

    def test_invalid_source_yaml_fails(self):
        (self.repo / "skills/demo/SKILL.md").write_text(
            "---\nname: [\n---\n", encoding="ascii"
        )
        with self.assertRaisesRegex(DiscoveryError, "invalid YAML"):
            discover_expected(self.repo)

    def test_missing_source_skill_fails(self):
        (self.repo / "skills/empty").mkdir()
        with self.assertRaisesRegex(DiscoveryError, "missing source SKILL.md"):
            discover_expected(self.repo)

    def test_source_hash_covers_resources(self):
        (self.repo / "skills/demo/resource.txt").write_text(
            "Changed.\n", encoding="ascii"
        )
        changed = discover_expected(self.repo)
        self.assertNotEqual(
            self.expected["demo"]["source_sha256"], changed["demo"]["source_sha256"]
        )

    def test_package_hash_uses_portable_case_sensitive_path_order(self):
        package = self.repo / "skills/demo"
        (package / "Z-resource.txt").write_bytes(b"Uppercase resource.\n")
        (package / "a-resource.txt").write_bytes(b"Lowercase resource.\n")
        expected = hashlib.sha256()
        for name in ["SKILL.md", "Z-resource.txt", "a-resource.txt", "resource.txt"]:
            expected.update(name.encode("ascii") + b"\0")
            expected.update(hashlib.sha256((package / name).read_bytes()).digest())
        self.assertEqual(package_sha256(package), expected.hexdigest())

    def test_discovery_matches_real_source_fields(self):
        records, failures, ignored, global_errors = verify_discovery(
            self.result, self.expected, self.project
        )
        self.assertEqual(failures, [])
        self.assertEqual(ignored, [])
        self.assertEqual(global_errors, [])
        self.assertEqual(records[0]["status"], "passed")

    def test_missing_and_duplicate_discovery_fail(self):
        for skills, count in [([], 0), (self.result["data"][0]["skills"] * 2, 2)]:
            with self.subTest(count=count):
                result = copy.deepcopy(self.result)
                result["data"][0]["skills"] = skills
                records, failures, _, global_errors = verify_discovery(
                    result, self.expected, self.project
                )
                self.assertEqual(records[0]["status"], "failed")
                self.assertIn(f"found {count}", failures[0])
                self.assertEqual(global_errors, [])

    def test_global_or_system_name_cannot_substitute_for_repo_skill(self):
        for scope in ["user", "system"]:
            with self.subTest(scope=scope):
                result = copy.deepcopy(self.result)
                found = result["data"][0]["skills"][0]
                found.update(scope=scope, path=str(self.root / "host/demo/SKILL.md"))
                _, failures, _, global_errors = verify_discovery(
                    result, self.expected, self.project
                )
                self.assertTrue(any("path" in failure for failure in failures))
                self.assertTrue(any("scope" in failure for failure in failures))
                self.assertTrue(global_errors)

    def test_description_and_enabled_mismatch_fail(self):
        result = copy.deepcopy(self.result)
        result["data"][0]["skills"][0].update(description="Wrong", enabled=False)
        _, failures, _, global_errors = verify_discovery(
            result, self.expected, self.project
        )
        self.assertTrue(any("description" in failure for failure in failures))
        self.assertTrue(any("enabled" in failure for failure in failures))
        self.assertEqual(global_errors, [])

    def test_host_load_errors_fail(self):
        self.result["data"][0]["errors"] = [
            {"path": "demo/SKILL.md", "message": "bad YAML"}
        ]
        _, failures, _, global_errors = verify_discovery(
            self.result, self.expected, self.project
        )
        self.assertIn("bad YAML", failures[0])
        self.assertTrue(global_errors)

    def test_partial_discovery_responses_fail(self):
        for result in [{}, {"data": []}, {"data": [{}]}, {"data": [None]}]:
            with self.subTest(result=result), self.assertRaises(DiscoveryError):
                verify_discovery(result, self.expected, self.project)

    def test_wrong_project_fails(self):
        self.result["data"][0]["cwd"] = str(self.repo)
        with self.assertRaisesRegex(DiscoveryError, "cwd"):
            verify_discovery(self.result, self.expected, self.project)

    def process(self, script, timeout=3):
        return JsonLineProcess(
            [sys.executable, "-u", "-c", script],
            self.root,
            isolated_environment(self.root / "home"),
            timeout,
        )

    def test_protocol_notifications_do_not_replace_response(self):
        script = (
            "import json,sys\n"
            "sys.stdin.readline()\n"
            "print(json.dumps({'method':'notice','params':{}}))\n"
            "print(json.dumps({'id':1,'result':{'ok':True}}))\n"
        )
        with self.process(script) as server:
            self.assertEqual(server.request(1, "initialize", {}), {"ok": True})
        self.assertIsNotNone(server.process.poll())

    def test_protocol_malformed_partial_and_host_error_fail(self):
        outputs = [
            ("garbage\n", "Malformed"),
            ('{"id":1,"result":{}}', "truncated"),
            ('{"id":1}\n', "missing object result"),
            ('{"id":2,"result":{}}\n', "Unexpected response id"),
            ('{"id":1,"error":{"message":"synthetic failure"}}\n', "synthetic failure"),
        ]
        for output, message in outputs:
            with (
                self.subTest(output=output),
                self.process(
                    "import sys\nsys.stdin.readline()\nsys.stdout.write("
                    + repr(output)
                    + ")\n"
                ) as server,
            ):
                with self.assertRaisesRegex(DiscoveryError, message):
                    server.request(1, "initialize", {})
            self.assertIsNotNone(server.process.poll())

    def test_timeout_cleans_up_process(self):
        started = time.monotonic()
        with self.process("import time\ntime.sleep(30)", timeout=0.15) as server:
            with self.assertRaisesRegex(DiscoveryError, "Timed out"):
                server.request(1, "initialize", {})
        self.assertIsNotNone(server.process.poll())
        self.assertLess(time.monotonic() - started, 10)

    def test_missing_executable_is_actionable(self):
        report = check_codex(self.repo, executable=str(self.root / "missing-codex"))
        self.assertEqual(report["status"], "failed")
        self.assertEqual(report["behavior"], "not_run")
        self.assertFalse(report["scan_completed"])
        self.assertIn("executable not found", report["errors"][0])

    def run_fake_harness(self, body="", timeout=3):
        fake = self.root / "fake_codex.py"
        inventory = [
            {"name": name, "description": source["description"]}
            for name, source in discover_expected(self.repo).items()
        ]
        fake.write_text(
            "import json,os,sys\n"
            "from pathlib import Path\n"
            "if '--version' in sys.argv:\n"
            "    print('codex-cli synthetic')\n"
            "    sys.exit(0)\n"
            "assert 'OPENAI_API_KEY' not in os.environ\n"
            "first=json.loads(sys.stdin.readline())\n"
            "assert first['method']=='initialize'\n"
            "print(json.dumps({'id':1,'result':{'codexHome':os.environ['CODEX_HOME'],"
            "'userAgent':'synthetic'}}),flush=True)\n"
            "assert json.loads(sys.stdin.readline())['method']=='initialized'\n"
            "request=json.loads(sys.stdin.readline())\n"
            "assert request['method']=='skills/list'\n"
            "cwd=request['params']['cwds'][0]\n"
            f"skills={inventory!r}\n"
            "for skill in skills:\n"
            "    skill.update(path=str(Path(cwd)/'.agents/skills'/skill['name']/'SKILL.md'),"
            "enabled=True,scope='repo')\n"
            "errors=[]\n" + body + "\n"
            "print(json.dumps({'id':2,'result':{'data':[{'cwd':cwd,'skills':skills,"
            "'errors':errors}]}}),flush=True)\n"
            "assert sys.stdin.readline()==''\n",
            encoding="ascii",
        )
        with patch(
            "scripts.check_codex_skills.executable_command",
            side_effect=lambda _, args: [sys.executable, "-u", str(fake), *args],
        ):
            return check_codex(self.repo, timeout=timeout)

    def test_full_harness_only_sends_discovery_methods(self):
        report = self.run_fake_harness()
        self.assertEqual(report["status"], "passed", json.dumps(report))
        self.assertEqual(report["client_version"], "codex-cli synthetic")
        self.assertEqual(report["skills"][0]["status"], "passed")
        self.assertTrue(report["scan_completed"])
        self.assertEqual(
            report["skills"][0]["source_sha256"], report["skills"][0]["staged_sha256"]
        )
        changed = self.run_fake_harness(
            "(Path(cwd)/'.agents/skills/demo/resource.txt').write_text('Changed.')"
        )
        self.assertEqual(changed["status"], "failed")
        self.assertIn("package changed", changed["errors"][0])
        self.assertTrue(changed["scan_completed"])

    def test_row_failure_preserves_completed_scan_and_other_success(self):
        source = self.repo / "skills/other/SKILL.md"
        source.parent.mkdir()
        source.write_text(
            "---\nname: other\ndescription: Other skill.\n---\nBody.\n",
            encoding="ascii",
        )
        report = self.run_fake_harness("skills[0]['description']='Wrong'")
        self.assertTrue(report["scan_completed"])
        self.assertEqual(report["status"], "failed")
        self.assertEqual(
            [(s["name"], s["status"]) for s in report["skills"]],
            [("demo", "failed"), ("other", "passed")],
        )

    def test_global_load_error_invalidates_completed_scan(self):
        report = self.run_fake_harness(
            "errors=[{'path':'unknown/SKILL.md','message':'bad YAML'}]"
        )
        self.assertFalse(report["scan_completed"])
        self.assertEqual(report["status"], "failed")
        self.assertIn("bad YAML", report["errors"][0])

    def test_attributable_load_error_is_a_row_failure(self):
        report = self.run_fake_harness(
            "errors=[{'path':skills[0]['path'],'message':'bad YAML'}]"
        )
        self.assertTrue(report["scan_completed"])
        self.assertEqual(report["skills"][0]["status"], "failed")

    def test_global_unexpected_skill_invalidates_completed_scan(self):
        report = self.run_fake_harness(
            "skills.append(dict(skills[0],name='unexpected'))"
        )
        self.assertFalse(report["scan_completed"])
        self.assertEqual(report["status"], "failed")

    def test_leaked_duplicate_invalidates_completed_scan(self):
        report = self.run_fake_harness("skills.append(dict(skills[0],scope='user'))")
        self.assertFalse(report["scan_completed"])
        self.assertEqual(report["skills"][0]["status"], "failed")

    def test_report_timeout_leaves_scan_incomplete(self):
        report = self.run_fake_harness("import time\ntime.sleep(30)", timeout=0.25)
        self.assertFalse(report["scan_completed"])
        self.assertEqual(report["status"], "failed")
        self.assertTrue(any("Timed out" in error for error in report["errors"]))


if __name__ == "__main__":
    unittest.main()
