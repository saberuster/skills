"""Exercise deterministic Fern project resource application in temporary directories."""

import importlib.util
import os
import shutil
import tempfile
import tomllib
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "skills/fern/setup-fern"
SPEC = importlib.util.spec_from_file_location(
    "fern_resources", PACKAGE / "scripts/resources.py"
)
resources = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(resources)


class FernResourceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "project"
        self.root.mkdir()
        self.package = Path(self.temporary.name) / "package"
        shutil.copytree(PACKAGE / "assets", self.package / "assets")
        self.config = self.root / ".codex/config.toml"
        self.instructions = self.root / "AGENTS.md"

    def run_setup(self, check=False):
        return {
            item["name"]: item
            for item in resources.apply_resources(self.package, self.root, check)
        }

    def snapshot(self):
        return {
            str(path.relative_to(self.root)): (
                path.read_bytes(),
                path.stat().st_mtime_ns,
            )
            for path in self.root.rglob("*")
            if path.is_file()
        }

    def test_project_layout_and_repeat_preserve_bytes_and_mtimes(self):
        first = self.run_setup()
        self.assertEqual(len(first), 11)
        self.assertEqual({item["status"] for item in first.values()}, {"added"})
        self.assertTrue(self.instructions.is_file())
        self.assertEqual(len(list((self.root / ".codex/agents").glob("*.toml"))), 6)
        self.assertTrue(self.config.is_file())
        self.assertFalse((self.root / ".codex/fern").exists())
        self.assertFalse((self.root / ".agents").exists())
        before = self.snapshot()
        self.assertEqual(
            {item["status"] for item in self.run_setup().values()}, {"unchanged"}
        )
        self.assertEqual(self.snapshot(), before)

    def test_existing_root_rules_are_appended_and_override_is_untouched(self):
        original = b"# Project rules\r\nKeep these rules exactly."
        self.instructions.write_bytes(original)
        override = self.root / "AGENTS.override.md"
        override.write_bytes(b"Override remains user owned.\n")
        result = self.run_setup()
        self.assertEqual(result[resources.INSTRUCTIONS]["status"], "added")
        self.assertEqual(result[resources.INSTRUCTIONS]["path"], str(self.instructions))
        raw = self.instructions.read_bytes()
        self.assertTrue(raw.startswith(original + b"\r\n\r\n"))
        self.assertEqual(raw.count(resources.START), 1)
        self.assertEqual(override.read_bytes(), b"Override remains user owned.\n")
        before = self.snapshot()
        self.run_setup()
        self.assertEqual(self.snapshot(), before)

    def test_existing_named_agents_are_overwritten_and_unrelated_agents_kept(self):
        agent = self.root / ".codex/agents/reviewer.toml"
        agent.parent.mkdir(parents=True)
        agent.write_bytes(b"Custom reviewer content, including invalid TOML")
        unrelated = agent.parent / "personal.toml"
        unrelated.write_bytes(b"Personal content")
        result = self.run_setup()
        self.assertEqual(result["agents/reviewer.toml"]["status"], "updated")
        self.assertEqual(
            agent.read_bytes(),
            (self.package / "assets/codex/agents/reviewer.toml").read_bytes(),
        )
        self.assertEqual(unrelated.read_bytes(), b"Personal content")
        self.assertFalse((self.root / ".codex/fern").exists())

    def test_check_never_creates_files_or_changes_bytes_or_mtimes(self):
        self.assertEqual(
            {item["status"] for item in self.run_setup(check=True).values()},
            {"missing"},
        )
        self.assertEqual(self.snapshot(), {})
        self.run_setup()
        (self.root / ".codex/agents/reviewer.toml").write_text(
            "different", encoding="utf-8"
        )
        self.config.write_bytes(self.config.read_bytes().replace(b"= 4", b"= 7"))
        before = self.snapshot()
        result = self.run_setup(check=True)
        self.assertEqual(result["agents/reviewer.toml"]["status"], "different")
        self.assertEqual(
            result["config:agents.max_concurrent_threads_per_session"]["status"],
            "different",
        )
        self.assertEqual(self.snapshot(), before)

    def test_config_overrides_existing_values_and_types_preserving_others(self):
        self.config.parent.mkdir()
        original = b'# Personal\r\nmodel = "mine"\r\n\r\n[agents] # Keep header\r\nmax_concurrent_threads_per_session = "custom" # Keep value\r\ncustom = 17\r\n'
        self.config.write_bytes(original)
        result = self.run_setup()
        self.assertEqual(
            result["config:agents.max_concurrent_threads_per_session"]["status"],
            "updated",
        )
        content = self.config.read_bytes()
        self.assertIn(b"= 4 # Keep value\r\n", content)
        self.assertIn(b"[agents] # Keep header\r\n", content)
        self.assertNotIn(b"\n", content.replace(b"\r\n", b""))
        parsed = tomllib.loads(content.decode())
        self.assertEqual(parsed["model"], "mine")
        self.assertEqual(parsed["agents"]["custom"], 17)
        self.assertEqual(parsed["tools"]["update_plan"]["enabled"], True)

    def test_dotted_keys_update_and_unsupported_inline_tables_are_preserved(self):
        self.config.parent.mkdir()
        self.config.write_bytes(
            b'tools.update_plan.enabled = false # Retain\nmodel = "mine"\n'
        )
        result = self.run_setup()
        self.assertEqual(
            result["config:tools.update_plan.enabled"]["status"], "updated"
        )
        self.assertIn(
            b"tools.update_plan.enabled = true # Retain\n", self.config.read_bytes()
        )
        self.config.write_bytes(
            b"agents = { max_concurrent_threads_per_session = 2 } # Retain\n"
        )
        result = self.run_setup()
        self.assertEqual(
            result["config:agents.max_concurrent_threads_per_session"]["status"],
            "conflict",
        )
        self.assertEqual(
            result["config:agents.default_subagent_model"]["status"], "conflict"
        )
        self.assertTrue(
            self.config.read_bytes().startswith(
                b"agents = { max_concurrent_threads_per_session = 2 } # Retain\n"
            )
        )

    def test_managed_instruction_block_is_replaced_without_prior_state(self):
        self.instructions.write_bytes(
            b"# Prefix\r\n"
            + resources.START
            + b"\r\nCustom previous rules\r\n"
            + resources.END
            + b"\r\n# Suffix\r\n"
        )
        result = self.run_setup()
        self.assertEqual(result[resources.INSTRUCTIONS]["status"], "updated")
        raw = self.instructions.read_bytes()
        self.assertTrue(raw.startswith(b"# Prefix\r\n"))
        self.assertTrue(raw.endswith(b"\r\n# Suffix\r\n"))
        self.assertIn(resources.START, raw)
        self.assertNotIn(b"Custom previous rules", raw)
        self.assertFalse((self.root / ".codex/fern").exists())

    def test_obsolete_instruction_markers_are_reported_without_migration(self):
        original = b"<!-- fern:subagent-instructions:start -->\nOld rules\n<!-- fern:subagent-instructions:end -->\n"
        self.instructions.write_bytes(original)
        before = (self.instructions.read_bytes(), self.instructions.stat().st_mtime_ns)
        for check in (False, True):
            result = self.run_setup(check=check)[resources.INSTRUCTIONS]
            self.assertEqual(result["status"], "conflict")
            self.assertIn("unsupported", result["reason"])
            self.assertEqual(
                (self.instructions.read_bytes(), self.instructions.stat().st_mtime_ns),
                before,
            )

    def test_invalid_toml_preserves_config_while_other_resources_complete(self):
        self.config.parent.mkdir()
        original = b"[agents\ninvalid config"
        self.config.write_bytes(original)
        result = self.run_setup()
        self.assertTrue(
            all(
                row["status"] == "conflict"
                for name, row in result.items()
                if name.startswith("config:")
            )
        )
        self.assertEqual(self.config.read_bytes(), original)
        self.assertTrue(self.instructions.is_file())
        self.assertTrue((self.root / ".codex/agents/reviewer.toml").is_file())

    def test_malformed_markers_are_preserved(self):
        for raw in (
            resources.START,
            resources.END + resources.START,
            resources.START + resources.END + resources.START + resources.END,
        ):
            self.instructions.write_bytes(raw)
            self.assertEqual(
                self.run_setup()[resources.INSTRUCTIONS]["status"], "conflict"
            )
            self.assertEqual(self.instructions.read_bytes(), raw)

    def test_old_malformed_state_is_ignored_and_left_unchanged(self):
        old = self.root / ".codex/fern/receipt.json"
        old.parent.mkdir(parents=True)
        old.write_bytes(b"No longer valid JSON")
        before = (old.read_bytes(), old.stat().st_mtime_ns)
        self.assertEqual(
            {item["status"] for item in self.run_setup().values()}, {"added"}
        )
        self.assertEqual((old.read_bytes(), old.stat().st_mtime_ns), before)
        self.assertEqual(list(old.parent.iterdir()), [old])

    def test_linked_project_resources_are_rejected(self):
        outside = Path(self.temporary.name) / "outside"
        outside.mkdir()
        try:
            os.symlink(outside, self.root / ".codex", target_is_directory=True)
        except OSError as error:
            self.skipTest(f"Symlink creation unavailable: {error}")
        result = self.run_setup()
        self.assertTrue(
            all(
                row["status"] == "conflict"
                for name, row in result.items()
                if name != resources.INSTRUCTIONS
            )
        )
        self.assertEqual(list(outside.iterdir()), [])
        self.assertTrue(self.instructions.exists())

    def test_multiple_config_changes_use_one_atomic_write(self):
        self.config.parent.mkdir()
        self.config.write_bytes(
            b"# Preserve this comment\n[agents]\nmax_concurrent_threads_per_session = 1\n"
        )
        original = resources._atomic
        writes = []

        def capture(path, content):
            if path == self.config:
                writes.append(content)
            original(path, content)

        with mock.patch.object(resources, "_atomic", side_effect=capture):
            result = self.run_setup()
        self.assertEqual(len(writes), 1)
        self.assertTrue(
            all(
                row["status"] in {"added", "updated"}
                for name, row in result.items()
                if name.startswith("config:")
            )
        )
        self.assertTrue(
            self.config.read_bytes().startswith(b"# Preserve this comment\n")
        )
        self.assertEqual(
            tomllib.loads(self.config.read_text())["agents"][
                "max_concurrent_threads_per_session"
            ],
            4,
        )

    def test_final_table_header_without_newline_accepts_selected_keys(self):
        baseline = (self.package / "assets/codex/config.fragment.toml").read_bytes()
        for header, key, value, prefix in (
            (
                b"[agents]",
                ("agents", "max_concurrent_threads_per_session"),
                4,
                b'model = "personal"\n',
            ),
            (
                b"[tools.update_plan] # Keep header comment",
                ("tools", "update_plan", "enabled"),
                True,
                b'model = "personal"\n' + baseline.split(b"[tools.update_plan]")[0],
            ),
        ):
            with self.subTest(header=header):
                edited = resources._config_edit(header, key, value)
                self.assertTrue(edited.startswith(header + b"\n"))
                self.assertEqual(
                    resources._flatten(tomllib.loads(edited.decode()))[key], value
                )
                self.config.parent.mkdir(exist_ok=True)
                self.config.write_bytes(prefix + header)
                with mock.patch.object(
                    resources, "_atomic", wraps=resources._atomic
                ) as atomic:
                    result = self.run_setup()
                self.assertTrue(
                    all(
                        row["status"] in {"added", "unchanged"}
                        for name, row in result.items()
                        if name.startswith("config:")
                    )
                )
                self.assertEqual(
                    sum(call.args[0] == self.config for call in atomic.call_args_list),
                    1,
                )
                self.assertEqual(
                    tomllib.loads(self.config.read_text())["model"], "personal"
                )
                self.assertIn(header + b"\n", self.config.read_bytes())

    def test_late_unsupported_config_key_preserves_entire_config(self):
        self.config.parent.mkdir()
        original = b'[tools.update_plan]\nenabled = """custom""" # Unsupported scalar\n'
        self.config.write_bytes(original)
        before = self.config.stat().st_mtime_ns
        with mock.patch.object(resources, "_atomic", wraps=resources._atomic) as atomic:
            result = self.run_setup()
        self.assertTrue(
            all(
                row["status"] == "conflict"
                for name, row in result.items()
                if name.startswith("config:")
            )
        )
        self.assertEqual(self.config.read_bytes(), original)
        self.assertEqual(self.config.stat().st_mtime_ns, before)
        self.assertFalse(
            any(call.args[0] == self.config for call in atomic.call_args_list)
        )

    def test_unrelated_sibling_symlink_does_not_block_selected_files(self):
        outside = Path(self.temporary.name) / "outside.toml"
        outside.write_bytes(b"Unrelated data")
        sibling = self.root / ".codex/agents/personal.toml"
        sibling.parent.mkdir(parents=True)
        try:
            os.symlink(outside, sibling)
        except OSError as error:
            self.skipTest(f"Symlink creation unavailable: {error}")
        self.assertEqual(
            {row["status"] for row in self.run_setup().values()}, {"added"}
        )
        self.assertEqual(outside.read_bytes(), b"Unrelated data")
        self.assertTrue(sibling.is_symlink())

    def test_selected_file_symlink_is_rejected_even_for_check(self):
        outside = Path(self.temporary.name) / "reviewer.toml"
        outside.write_bytes(
            (self.package / "assets/codex/agents/reviewer.toml").read_bytes()
        )
        selected = self.root / ".codex/agents/reviewer.toml"
        selected.parent.mkdir(parents=True)
        try:
            os.symlink(outside, selected)
        except OSError as error:
            self.skipTest(f"Symlink creation unavailable: {error}")
        before = (outside.read_bytes(), outside.stat().st_mtime_ns)
        for check in (False, True):
            self.assertEqual(
                self.run_setup(check=check)["agents/reviewer.toml"]["status"],
                "conflict",
            )
            self.assertEqual((outside.read_bytes(), outside.stat().st_mtime_ns), before)
            self.assertTrue(selected.is_symlink())

    def test_write_failure_reports_failure_without_creating_state(self):
        original = resources._atomic

        def fail_instructions(path, content):
            if path == self.instructions:
                raise OSError("Simulated write failure")
            original(path, content)

        with mock.patch.object(resources, "_atomic", side_effect=fail_instructions):
            result = self.run_setup()
        self.assertEqual(result[resources.INSTRUCTIONS]["status"], "failed")
        self.assertTrue(self.config.exists())
        self.assertFalse(self.instructions.exists())
        self.assertFalse((self.root / ".codex/fern").exists())


if __name__ == "__main__":
    unittest.main()
