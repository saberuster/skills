"""Exercise install-probe failure gates without network or real installers."""

import copy
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts.check_codex_skills import DiscoveryError, package_sha256
from scripts.check_fern_install import (
    check_install,
    disposable_home,
    fetch_snapshot,
    parse_install,
    run,
    select_packages,
    verify_installed,
    verify_user_discovery,
)


class FernInstallTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="fern-probe-unit-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.home = self.root / "home"
        self.source = self.root / "source"
        package = self.source / "skills/fern/example"
        package.mkdir(parents=True)
        (package / "SKILL.md").write_text(
            "---\nname: example\ndescription: Example skill\n---\nBody.\n",
            encoding="ascii",
        )
        (package / "asset.txt").write_bytes(b"full package resource\n")
        self.expected = select_packages(self.source, ["skills/fern"])
        self.revision = "a" * 40
        self.tree_oid = "b" * 40
        self.source_record = {
            "repository": "saberuster/skills",
            "branch": "main",
            "sha": self.revision,
            "url": "https://github.com/saberuster/skills.git",
        }
        self.expected["example"].update(
            source=self.source_record, tree_oid=self.tree_oid
        )
        shutil.copytree(package, self.home / ".agents/skills/example")
        self.lock = {
            "version": 3,
            "skills": {
                "example": {
                    "source": "saberuster/skills",
                    "sourceType": "github",
                    "sourceUrl": "https://github.com/saberuster/skills.git",
                    "ref": self.revision,
                    "skillPath": "skills/fern/example/SKILL.md",
                    "skillFolderHash": self.tree_oid,
                }
            },
        }
        self.write_lock()

    def write_lock(self):
        (self.home / ".agents/.skill-lock.json").write_text(
            json.dumps(self.lock), encoding="ascii"
        )

    def install_row(self):
        return {
            "name": "example",
            "status": "installed",
            "source": "saberuster/skills",
            "ref": self.revision,
            "path": str(self.home / ".agents/skills/example"),
            "scope": "global",
            "agents": ["Codex"],
            "mode": "copy",
        }

    def discovery_result(self):
        return {
            "data": [
                {
                    "cwd": str(self.root),
                    "errors": [],
                    "skills": [
                        {
                            "name": "example",
                            "description": "Example skill",
                            "enabled": True,
                            "scope": "user",
                            "path": str(self.home / ".agents/skills/example/SKILL.md"),
                        }
                    ],
                }
            ]
        }

    def test_complete_copied_package_and_source_lock_pass_twice_without_changes(self):
        first, original = verify_installed(self.home, self.expected)
        second, repeated = verify_installed(self.home, self.expected)
        self.assertEqual(first, second)
        self.assertEqual(original, repeated)
        self.assertEqual(
            first[0]["sha256"]["canonical"],
            package_sha256(self.expected["example"]["path"]),
        )
        self.assertFalse((self.home / ".codex/skills/example").exists())

    def test_lock_rejects_each_wrong_remote_provenance_field(self):
        original = copy.deepcopy(self.lock)
        for field, wrong in {
            "source": "other/repository",
            "sourceType": "local",
            "sourceUrl": "/tmp/source",
            "ref": "main",
            "skillPath": "skills/other/SKILL.md",
            "skillFolderHash": "c" * 40,
        }.items():
            with self.subTest(field=field):
                self.lock = copy.deepcopy(original)
                self.lock["skills"]["example"][field] = wrong
                self.write_lock()
                with self.assertRaisesRegex(DiscoveryError, "provenance mismatch"):
                    verify_installed(self.home, self.expected)

    def test_missing_lock_entry_is_an_incomplete_install(self):
        self.lock["skills"] = {}
        self.write_lock()
        with self.assertRaisesRegex(DiscoveryError, "missing or unexpected skills"):
            verify_installed(self.home, self.expected)

    def test_missing_resource_and_extra_file_both_fail_byte_equality(self):
        installed = self.home / ".agents/skills/example"
        (installed / "asset.txt").unlink()
        with self.assertRaisesRegex(DiscoveryError, "byte mismatch"):
            verify_installed(self.home, self.expected)
        (installed / "asset.txt").write_bytes(b"full package resource\n")
        (installed / "unselected.txt").write_bytes(b"unexpected")
        with self.assertRaisesRegex(DiscoveryError, "byte mismatch"):
            verify_installed(self.home, self.expected)

    def test_missing_package_and_duplicate_codex_copy_are_rejected(self):
        installed = self.home / ".agents/skills/example"
        shutil.copytree(installed, self.home / ".codex/skills/example")
        with self.assertRaisesRegex(DiscoveryError, "duplicate Codex"):
            verify_installed(self.home, self.expected)
        shutil.rmtree(installed)
        with self.assertRaisesRegex(DiscoveryError, "Missing canonical package"):
            verify_installed(self.home, self.expected)

    def test_installer_requires_complete_successful_explicit_codex_copy_results(self):
        parse_install(
            json.dumps([self.install_row()]),
            ["example"],
            "saberuster/skills",
            self.revision,
            self.home,
        )
        cases = [[], [self.install_row(), self.install_row()], "not JSON"]
        for field, value in {
            "status": "failed",
            "source": "local",
            "ref": "main",
            "mode": "symlink",
            "scope": "project",
            "agents": ["Codex", "Claude Code"],
            "path": str(self.root / "outside"),
        }.items():
            row = self.install_row()
            row[field] = value
            cases.append([row])
        for rows in cases:
            with self.subTest(rows=rows), self.assertRaises(DiscoveryError):
                parse_install(
                    rows if isinstance(rows, str) else json.dumps(rows),
                    ["example"],
                    "saberuster/skills",
                    self.revision,
                    self.home,
                )

    def test_source_selection_rejects_missing_and_empty_directories(self):
        with self.assertRaisesRegex(DiscoveryError, "Missing required"):
            select_packages(self.source, ["skills/meta"])
        (self.source / "skills/meta").mkdir()
        with self.assertRaisesRegex(DiscoveryError, "Empty required"):
            select_packages(self.source, ["skills/meta"])

    def test_source_selection_derives_names_and_rejects_nested_packages(self):
        selected = select_packages(self.source, ["skills/fern"])
        self.assertEqual(set(selected), {"example"})
        nested = self.source / "skills/fern/example/nested"
        nested.mkdir()
        (nested / "SKILL.md").write_text(
            "---\nname: nested\ndescription: Nested\n---\n", encoding="ascii"
        )
        with self.assertRaisesRegex(DiscoveryError, "Nested package boundary"):
            select_packages(self.source, ["skills/fern"])

    def test_user_discovery_rejects_disabled_wrong_scope_and_wrong_path(self):
        verify_user_discovery(
            self.discovery_result(), self.expected, self.root, self.home
        )
        for field, value in {
            "enabled": False,
            "scope": "repo",
            "path": str(self.root / "leaked/SKILL.md"),
        }.items():
            with self.subTest(field=field):
                result = self.discovery_result()
                result["data"][0]["skills"][0][field] = value
                with self.assertRaisesRegex(DiscoveryError, "discovery mismatch"):
                    verify_user_discovery(result, self.expected, self.root, self.home)

    def test_user_discovery_rejects_load_errors_duplicates_and_missing_skill(self):
        for kind in ("load_error", "duplicate", "missing", "unexpected"):
            with self.subTest(kind=kind):
                result = self.discovery_result()
                entry = result["data"][0]
                if kind == "load_error":
                    entry["errors"] = [{"message": "invalid skill"}]
                elif kind == "duplicate":
                    entry["skills"].append(copy.deepcopy(entry["skills"][0]))
                elif kind == "missing":
                    entry["skills"] = []
                else:
                    entry["skills"].append({"name": "leaked", "scope": "user"})
                with self.assertRaises(DiscoveryError):
                    verify_user_discovery(result, self.expected, self.root, self.home)

    def test_disposable_home_rejects_existing_directory_and_non_temp_target(self):
        with (
            mock.patch("scripts.check_fern_install.sys.platform", "linux"),
            mock.patch(
                "scripts.check_fern_install.tempfile.gettempdir",
                return_value=str(self.root),
            ),
        ):
            for target in (self.home, self.root / "missing/nested"):
                with self.subTest(target=target), self.assertRaises(DiscoveryError):
                    with disposable_home(target):
                        self.fail("Unsafe target was accepted")
            target = self.root / "new-home"
            with disposable_home(target) as (owned, home):
                self.assertEqual(owned, target)
                self.assertTrue(home.is_relative_to(target))
                self.assertTrue(home.is_dir())
            self.assertFalse(target.exists())

    def test_failed_guard_never_invokes_installer(self):
        with (
            mock.patch("scripts.check_fern_install.select_packages", return_value={}),
            mock.patch("scripts.check_fern_install.sys.platform", "win32"),
            mock.patch("scripts.check_fern_install.subprocess.run") as process,
        ):
            report = check_install(self.root / "unused")
        self.assertEqual(report["status"], "failed")
        self.assertIn("disposable Linux", report["errors"][0])
        process.assert_not_called()

    def test_nonzero_installer_exit_is_recorded_and_fails(self):
        commands = []
        with mock.patch(
            "scripts.check_fern_install.subprocess.run",
            return_value=subprocess.CompletedProcess(["installer"], 9, "[]", "failed"),
        ):
            with self.assertRaisesRegex(DiscoveryError, "Command failed"):
                run(["installer"], self.root, {}, 1, commands)
        self.assertEqual(commands[0]["returncode"], 9)
        self.assertEqual(commands[0]["stderr"], "failed")

    def test_branch_is_resolved_once_and_fetch_uses_immutable_sha(self):
        commands = []
        with mock.patch(
            "scripts.check_fern_install.run",
            side_effect=[f"{self.revision}\trefs/heads/main\n", "", "", ""],
        ) as execute:
            source = fetch_snapshot(
                "saberuster/skills", "main", self.root / "snapshot", {}, 1, commands
            )
        self.assertEqual(source["sha"], self.revision)
        calls = [call.args[0] for call in execute.call_args_list]
        self.assertEqual(sum(command[1] == "ls-remote" for command in calls), 1)
        self.assertEqual(calls[2][-1], self.revision)
        self.assertNotIn("main", calls[2])


if __name__ == "__main__":
    unittest.main()
