"""Exercise the bundled Fern CLI in disposable project directories."""

import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "skills/fern/setup-fern/scripts"
sys.dont_write_bytecode = True


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


resources = load("fern_test_resources", SCRIPTS / "resources.py")
with mock.patch.dict(sys.modules, {"resources": resources}):
    installer = load("fern_test_installer", SCRIPTS / "install.py")


class InstallerTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="fern-project-test-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.project = self.root / "project"
        self.project.mkdir()

    def snapshot(self):
        return {
            path.relative_to(self.project).as_posix(): (
                path.read_bytes() if path.is_file() else None,
                path.stat().st_mtime_ns,
            )
            for path in self.project.rglob("*")
        }

    def run_setup(self, *flags):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            status = installer.main(["--project", str(self.project), *flags])
        return status, json.loads(output.getvalue())

    def test_project_is_required_and_old_install_options_are_rejected(self):
        for arguments in ([], ["--project", str(self.project), "--target", "local"]):
            with (
                self.subTest(arguments=arguments),
                contextlib.redirect_stderr(io.StringIO()),
            ):
                with self.assertRaises(SystemExit) as error:
                    installer.parser().parse_args(arguments)
                self.assertEqual(error.exception.code, 2)

    def test_installs_bundled_config_agents_and_root_rules(self):
        status, report = self.run_setup()
        self.assertEqual(status, 0, report)
        self.assertEqual(report["project"], str(self.project))
        self.assertEqual({row["status"] for row in report["results"]}, {"added"})
        assets = installer.PACKAGE / "assets/codex"
        for role in resources.ROLES:
            actual = self.project / ".codex/agents" / f"{role}.toml"
            self.assertEqual(
                actual.read_bytes(), (assets / "agents" / actual.name).read_bytes()
            )
        config = tomllib.loads((self.project / ".codex/config.toml").read_text())
        baseline = tomllib.loads((assets / "config.fragment.toml").read_text())
        self.assertEqual(config, baseline)
        instructions = (self.project / "AGENTS.md").read_bytes()
        self.assertIn(resources.START, instructions)
        self.assertIn(resources.END, instructions)
        self.assertIn(
            (assets / "user-instructions.md").read_bytes().strip(), instructions
        )
        self.assertFalse((self.project / ".agents").exists())
        self.assertFalse((self.project / "skills-lock.json").exists())
        self.assertFalse((self.project / ".codex/AGENTS.md").exists())
        self.assertFalse((self.project / ".codex/fern").exists())
        self.assertIn("not verified", report["runtime"])

    def test_check_reports_missing_resources_without_creating_files_or_directories(
        self,
    ):
        before = self.snapshot()
        status, report = self.run_setup("--check")
        self.assertEqual(status, 1)
        self.assertTrue(
            any(row["status"] in installer.FAILURES for row in report["results"])
        )
        self.assertEqual(self.snapshot(), before)

    def test_repeated_apply_and_check_are_unchanged(self):
        status, report = self.run_setup()
        self.assertEqual(status, 0, report)
        before = self.snapshot()
        for flags in ((), ("--check",)):
            with self.subTest(flags=flags):
                status, report = self.run_setup(*flags)
                self.assertEqual(status, 0, report)
                self.assertEqual(
                    {row["status"] for row in report["results"]}, {"unchanged"}
                )
                self.assertEqual(self.snapshot(), before)

    def test_existing_named_agent_is_overwritten_with_bundled_content(self):
        agent = self.project / ".codex/agents/reviewer.toml"
        agent.parent.mkdir(parents=True)
        agent.write_bytes(b'name = "reviewer"\n# Existing project customization\n')
        status, report = self.run_setup()
        self.assertEqual(status, 0, report)
        self.assertTrue(any(row["status"] == "updated" for row in report["results"]))
        self.assertEqual(
            agent.read_bytes(),
            (installer.PACKAGE / "assets/codex/agents/reviewer.toml").read_bytes(),
        )
        self.assertTrue((self.project / ".codex/config.toml").is_file())
        self.assertTrue((self.project / "AGENTS.md").is_file())

    def test_missing_project_returns_json_failure_without_creating_it(self):
        missing = self.root / "missing"
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            status = installer.main(["--project", str(missing)])
        self.assertEqual(status, 1)
        self.assertEqual(
            json.loads(output.getvalue())["results"][0]["status"], "failed"
        )
        self.assertFalse(missing.exists())

    def test_parent_segments_are_normalized_without_resolving_links(self):
        nested = self.root / "nested"
        nested.mkdir()
        args = installer.parser().parse_args(
            ["--project", str(nested / "../project"), "--check"]
        )
        with mock.patch.object(installer, "apply_resources", return_value=[]) as apply:
            report = installer.install(args)
        self.assertEqual(report["project"], str(self.project))
        apply.assert_called_once_with(installer.PACKAGE, self.project, check=True)


if __name__ == "__main__":
    unittest.main()
