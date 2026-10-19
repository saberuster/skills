"""Retained scratch fixtures must fail closed on filtering or Docker errors."""

import io
import json
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import check_docker_context as checker


def write_archive(path, entries):
    with tarfile.open(path, "w") as archive:
        for name, data in entries:
            info = tarfile.TarInfo(name)
            info.size = len(data)
            archive.addfile(info, io.BytesIO(data))


class DockerContextTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.root = self.base / "source"
        self.output = self.base / "result"
        self.payload = b'{"name":"synthetic-marketplace"}\r\n'
        for name in checker.FILTERS:
            source = self.root / name
            source.parent.mkdir(parents=True, exist_ok=True)
            source.write_bytes(b"**/.agents\n!.agents/plugins/marketplace.json\n")
        marketplace = self.root / checker.MARKETPLACE
        marketplace.parent.mkdir(parents=True)
        marketplace.write_bytes(self.payload)
        self.calls = []

    def docker(self, command, **kwargs):
        self.calls.append(command)
        kwargs["stdout"].write(b"synthetic Docker log\n")
        if command[1] == "export":
            write_archive(
                Path(command[3]), [("./" + checker.MARKETPLACE, self.payload)]
            )
        return subprocess.CompletedProcess(command, 0)

    def run_fixture(self, side_effect=None):
        with (
            mock.patch.object(checker.shutil, "which", return_value="docker"),
            mock.patch.object(
                checker.subprocess, "run", side_effect=side_effect or self.docker
            ),
        ):
            return checker.run(self.root, self.output, 10)

    def test_both_filters_use_exact_bytes_and_retain_complete_evidence(self):
        report = self.run_fixture()
        self.assertEqual(report["status"], "passed")
        self.assertEqual(len(report["fixtures"]), 2)
        self.assertEqual(
            report["source_hashes"], checker.hashes(checker.source_bytes(self.root))
        )
        self.assertEqual(report["final_source_hashes"], report["source_hashes"])
        self.assertEqual(
            json.loads((self.output / "evidence/summary.json").read_text()), report
        )
        self.assertFalse((self.output / "source-manifest.json").exists())
        for index, name in enumerate(checker.FILTERS):
            context = self.output / f"fixture-{index}/context"
            self.assertEqual(
                (context / name).read_bytes(), (self.root / name).read_bytes()
            )
            self.assertEqual((context / checker.MARKETPLACE).read_bytes(), self.payload)
            for decoy in checker.DECOYS:
                self.assertTrue((context / decoy).is_file())
            fixture = report["fixtures"][index]
            self.assertTrue(fixture["marketplace_bytes_match"])
            self.assertEqual(len(fixture["commands"]), 3)
            self.assertEqual(len(fixture["cleanup"]), 2)
            self.assertTrue(
                all(
                    item["exit_code"] == 0
                    for item in fixture["commands"] + fixture["cleanup"]
                )
            )
        self.assertFalse(any(call[1] in ("run", "start") for call in self.calls))
        self.assertNotEqual(self.calls[0][5], self.calls[5][5])

    def test_archive_rejects_missing_changed_duplicate_or_leaked_members(self):
        valid = (checker.MARKETPLACE, self.payload)
        cases = (
            [],
            [(checker.MARKETPLACE, self.payload.replace(b"\r\n", b"\n"))],
            [valid, valid],
            [valid, (".agents/plugins/private.txt", b"excluded")],
            [valid, ("skills/fixture/.agents/plugins/marketplace.json", b"excluded")],
            [valid, ("../outside.txt", b"unsafe")],
        )
        for entries in cases:
            with self.subTest(entries=entries):
                archive = self.base / "fixture.tar"
                write_archive(archive, entries)
                with self.assertRaises(checker.ContextError):
                    checker.inspect_archive(archive, self.payload)

    def test_archive_rejects_symlink_marketplace_and_malformed_tar(self):
        archive = self.base / "fixture.tar"
        with tarfile.open(archive, "w") as exported:
            member = tarfile.TarInfo(checker.MARKETPLACE)
            member.type = tarfile.SYMTYPE
            member.linkname = "README.md"
            exported.addfile(member)
        with self.assertRaises(checker.ContextError):
            checker.inspect_archive(archive, self.payload)
        archive.write_bytes(b"not a tar archive")
        with self.assertRaises(tarfile.TarError):
            checker.inspect_archive(archive, self.payload)

    def test_archive_failure_cleans_both_resources_and_other_fixture_runs(self):
        def docker(command, **kwargs):
            result = self.docker(command, **kwargs)
            if command[1] == "export":
                write_archive(Path(command[3]), [(".agents/private.txt", b"excluded")])
            return result

        report = self.run_fixture(docker)
        self.assertEqual(report["status"], "failed")
        self.assertEqual(len(report["fixtures"]), 2)
        for fixture in report["fixtures"]:
            self.assertEqual(len(fixture["cleanup"]), 2)
            self.assertIn("Excluded", fixture["error"])

    def test_nonzero_build_exit_still_attempts_image_cleanup(self):
        def docker(command, **kwargs):
            result = self.docker(command, **kwargs)
            return (
                subprocess.CompletedProcess(command, 17)
                if command[1] == "build"
                else result
            )

        report = self.run_fixture(docker)
        self.assertEqual(report["status"], "failed")
        for fixture in report["fixtures"]:
            self.assertEqual(fixture["commands"][0]["exit_code"], 17)
            self.assertEqual(len(fixture["cleanup"]), 1)
            self.assertEqual(
                fixture["cleanup"][0]["command"][1:4], ["image", "rm", "--force"]
            )

    def test_create_timeout_attempts_container_and_image_cleanup(self):
        def docker(command, **kwargs):
            if command[1] == "create":
                raise subprocess.TimeoutExpired(command, kwargs["timeout"])
            return self.docker(command, **kwargs)

        report = self.run_fixture(docker)
        self.assertEqual(report["status"], "failed")
        for fixture in report["fixtures"]:
            self.assertTrue(fixture["commands"][1]["timed_out"])
            self.assertIsNone(fixture["commands"][1]["exit_code"])
            self.assertEqual(len(fixture["cleanup"]), 2)

    def test_cleanup_failure_changes_success_into_failure_and_continues_cleanup(self):
        def docker(command, **kwargs):
            result = self.docker(command, **kwargs)
            return (
                subprocess.CompletedProcess(command, 3)
                if command[1] == "rm"
                else result
            )

        report = self.run_fixture(docker)
        self.assertEqual(report["status"], "failed")
        for fixture in report["fixtures"]:
            self.assertTrue(fixture["cleanup_failed"])
            self.assertEqual(len(fixture["cleanup"]), 2)

    def test_source_drift_fails_even_when_both_exports_pass(self):
        def docker(command, **kwargs):
            result = self.docker(command, **kwargs)
            if command[1] == "export":
                (self.root / checker.FILTERS[0]).write_bytes(b"changed\n")
            return result

        report = self.run_fixture(docker)
        self.assertEqual(report["status"], "failed")
        self.assertIn("changed during validation", report["error"])

    def test_missing_docker_writes_failed_summary(self):
        with mock.patch.object(checker.shutil, "which", return_value=None):
            report = checker.run(self.root, self.output, 10)
        self.assertEqual(report["status"], "failed")
        self.assertIn("Docker is required", report["error"])
        self.assertEqual(report["fixtures"], [])
        self.assertTrue((self.output / "evidence/summary.json").is_file())

    def test_output_validation_and_positive_deadline(self):
        for output, timeout in (
            (self.root / "result", 10),
            (self.root, 10),
            (self.base, 10),
            (self.output, 0),
        ):
            with (
                self.subTest(output=output, timeout=timeout),
                self.assertRaises(checker.ContextError),
            ):
                checker.run(self.root, output, timeout)
        self.assertFalse(self.output.exists())


if __name__ == "__main__":
    unittest.main()
