"""Exercise install-probe failure gates without network or real installers."""

import copy
import hashlib
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
    inspect_source_lock,
    installation_home,
    parse_install,
    run,
    select_packages,
    skills_cli_fallback_sha256,
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
        self.assertEqual(first[0]["source_hash_algorithm"], "git_tree_oid")

    def use_fallback_hash(self):
        digest = skills_cli_fallback_sha256(self.expected["example"]["path"])
        self.lock["skills"]["example"]["skillFolderHash"] = digest
        self.write_lock()
        return digest

    def test_cli_fallback_uses_paths_raw_bytes_locale_order_and_excludes_caches(self):
        package = self.root / "hash-vector"
        files = {
            ".hidden": b"hidden\n",
            "a_b": b"underscore",
            "a-B": b"dash",
            "a.txt": b"lower",
            "B.txt": b"upper",
            "nested/z": b"\x00\xff\r\n",
        }
        for name, content in files.items():
            path = package / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        for name in (".git/config", "nested/node_modules/module/file"):
            path = package / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"ignored")
        # This fixed upstream localeCompare order differs from Python sorted().
        digest = hashlib.sha256()
        for name in (".hidden", "a_b", "a-B", "a.txt", "B.txt", "nested/z"):
            digest.update(name.encode("utf-8"))
            digest.update(files[name])
        self.assertEqual(skills_cli_fallback_sha256(package), digest.hexdigest())

    def test_cli_fallback_is_accepted_but_installed_bytes_are_still_required(self):
        self.use_fallback_hash()
        rows, _ = verify_installed(self.home, self.expected)
        self.assertEqual(rows[0]["source_hash_algorithm"], "skills_1_7_0_sha256")
        (self.home / ".agents/skills/example/asset.txt").write_bytes(b"tampered")
        with self.assertRaisesRegex(DiscoveryError, "byte mismatch"):
            verify_installed(self.home, self.expected)

    def test_cli_fallback_reads_original_paths_before_normalizing_hash_names(
        self,
    ):
        directory = self.root / "backslash-vector"
        directory.mkdir()
        path = directory / "a\\b.txt"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"backslash filename")
        expected = hashlib.sha256(b"a/b.txtbackslash filename").hexdigest()
        self.assertEqual(skills_cli_fallback_sha256(directory), expected)

    def test_fallback_rejects_each_wrong_remote_provenance_field(self):
        self.use_fallback_hash()
        original = copy.deepcopy(self.lock)
        for field, wrong in {
            "source": "other/repository",
            "sourceType": "local",
            "sourceUrl": "https://github.com/other/repository.git",
            "ref": "main",
            "skillPath": "skills/other/SKILL.md",
        }.items():
            with self.subTest(field=field):
                self.lock = copy.deepcopy(original)
                self.lock["skills"]["example"][field] = wrong
                self.write_lock()
                with self.assertRaisesRegex(DiscoveryError, rf"example\.{field}"):
                    verify_installed(self.home, self.expected)

    def test_arbitrary_malformed_and_wrong_hashes_are_rejected(self):
        for digest in (None, {}, "", "c" * 40, "d" * 64, "x" * 64, "d" * 63):
            with self.subTest(digest=digest):
                self.lock["skills"]["example"]["skillFolderHash"] = digest
                self.write_lock()
                with self.assertRaisesRegex(
                    DiscoveryError, r"example\.skillFolderHash"
                ):
                    verify_installed(self.home, self.expected)

    def test_fallback_digest_errors_are_bounded_and_cannot_accept_unknown_hash(self):
        for failure in (OSError("missing node"), subprocess.TimeoutExpired("node", 60)):
            with (
                self.subTest(failure=failure),
                mock.patch(
                    "scripts.check_fern_install.subprocess.run", side_effect=failure
                ),
            ):
                with self.assertRaisesRegex(DiscoveryError, "fallback SHA-256"):
                    skills_cli_fallback_sha256(self.source)
        self.lock["skills"]["example"]["skillFolderHash"] = "d" * 64
        self.write_lock()
        with mock.patch(
            "scripts.check_fern_install.skills_cli_fallback_sha256",
            side_effect=DiscoveryError("unavailable"),
        ):
            _, _, diagnostic = inspect_source_lock(self.home, self.expected)
            self.assertIn("diagnostic_errors", diagnostic)
            with self.assertRaisesRegex(DiscoveryError, "skillFolderHash"):
                verify_installed(self.home, self.expected)

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
        with self.assertRaisesRegex(DiscoveryError, "provenance mismatch: skills"):
            verify_installed(self.home, self.expected)

    def test_missing_malformed_and_invalid_schema_locks_name_the_failed_field(self):
        lock_path = self.home / ".agents/.skill-lock.json"
        cases = (
            (None, "lock", "missing"),
            (b"not JSON", "lock", "malformed_json"),
            (b"[]", "lock", "parsed"),
            (b'{"version":2,"skills":{}}', "version", "parsed"),
            (b'{"version":3,"skills":[]}', "skills", "parsed"),
            (b'{"version":3,"skills":{"example":null}}', "example.record", "parsed"),
        )
        for content, field, read_status in cases:
            with self.subTest(content=content):
                if content is None:
                    lock_path.unlink()
                else:
                    lock_path.write_bytes(content)
                _, _, diagnostic = inspect_source_lock(self.home, self.expected)
                self.assertEqual(diagnostic["read_status"], read_status)
                with self.assertRaises(DiscoveryError) as caught:
                    verify_installed(self.home, self.expected)
                self.assertIn(field, str(caught.exception))

    def test_diagnostics_distinguish_missing_provenance_field_from_null(self):
        record = self.lock["skills"]["example"]
        del record["ref"]
        self.write_lock()
        _, _, missing = inspect_source_lock(self.home, self.expected)
        record["ref"] = None
        self.write_lock()
        _, _, null = inspect_source_lock(self.home, self.expected)
        self.assertFalse(missing["mismatches"][0]["actual_present"])
        self.assertTrue(null["mismatches"][0]["actual_present"])
        self.assertIsNone(null["mismatches"][0]["actual"])

    def test_diagnostics_survive_failure_cleanup_and_exclude_unknown_fields(self):
        self.lock["token"] = "secret-top-level"
        record = self.lock["skills"]["example"]
        record["credential"] = "secret-extra-field"
        record["sourceUrl"] = (
            "https://user:secret-password@github.com/other/repo.git?token=secret-query#secret-fragment"
        )
        record["ref"] = "wrong-ref"
        self.write_lock()
        target = self.root / "diagnostic-home"
        report = {}
        with (
            mock.patch("scripts.check_fern_install.sys.platform", "linux"),
            mock.patch(
                "scripts.check_fern_install.tempfile.gettempdir",
                return_value=str(self.root),
            ),
        ):
            with self.assertRaisesRegex(
                DiscoveryError, r"example\.sourceUrl, example\.ref"
            ):
                with installation_home(target, self.expected, report) as (_, home):
                    shutil.copytree(self.home / ".agents", home / ".agents")
                    verify_installed(home, self.expected)
        self.assertFalse(target.exists())
        diagnostic = report["source_lock"]
        self.assertEqual(diagnostic["version"], 3)
        self.assertEqual(diagnostic["package_set"], ["example"])
        self.assertEqual(diagnostic["records"]["example"]["ref"], "wrong-ref")
        self.assertEqual(diagnostic["mismatches"][1]["expected"], self.revision)
        self.assertEqual(diagnostic["mismatches"][1]["actual"], "wrong-ref")
        self.assertNotIn("secret", json.dumps(report))
        self.assertNotIn("credential", json.dumps(report))

    def test_diagnostic_capture_cannot_mask_original_failure(self):
        target = self.root / "diagnostic-home"
        report = {}
        with (
            mock.patch("scripts.check_fern_install.sys.platform", "linux"),
            mock.patch(
                "scripts.check_fern_install.tempfile.gettempdir",
                return_value=str(self.root),
            ),
            mock.patch(
                "scripts.check_fern_install.inspect_source_lock",
                side_effect=RuntimeError("secondary"),
            ),
        ):
            with self.assertRaisesRegex(DiscoveryError, "original failure"):
                with installation_home(target, self.expected, report):
                    raise DiscoveryError("original failure")
        self.assertFalse(target.exists())
        self.assertEqual(report["source_lock"]["read_status"], "diagnostic_error")
        self.assertNotIn("secondary", json.dumps(report))

    def test_first_verification_diagnostics_are_not_recomputed_after_failure(self):
        self.lock["skills"]["example"]["skillFolderHash"] = "d" * 64
        self.write_lock()
        target = self.root / "diagnostic-home"
        report = {}
        with (
            mock.patch("scripts.check_fern_install.sys.platform", "linux"),
            mock.patch(
                "scripts.check_fern_install.tempfile.gettempdir",
                return_value=str(self.root),
            ),
            mock.patch(
                "scripts.check_fern_install.skills_cli_fallback_sha256",
                side_effect=DiscoveryError("first hash failure"),
            ) as digest,
        ):
            with self.assertRaisesRegex(DiscoveryError, "skillFolderHash"):
                with installation_home(target, self.expected, report) as (_, home):
                    shutil.copytree(self.home / ".agents", home / ".agents")
                    verify_installed(home, self.expected, report=report)
        digest.assert_called_once()
        self.assertFalse(target.exists())
        self.assertIn(
            "first hash failure", report["source_lock"]["diagnostic_errors"][0]
        )

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
                self.assertEqual(owned, target.resolve())
                self.assertTrue(home.is_relative_to(target.resolve()))
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
