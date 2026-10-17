"""Isolated Godot build-helper regressions; no real Godot execution is verified.

PowerShell tests require 7.2+ and explicitly skip when it is unavailable.
"""

import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_ROOTS = {
    "godot-build-and-diagnostics": ROOT
    / "skills/godot/godot-build-and-diagnostics/scripts",
}
PWSH = os.environ.get("PWSH") or shutil.which("pwsh")


@unittest.skipUnless(
    PWSH, "PowerShell 7.2+ unavailable; no PowerShell behavior verified"
)
class GodotBuildRegressionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="godot-build-regression-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "project with spaces"
        self.root.mkdir()
        (self.root / "project.godot").write_text("config_version=5")
        self.fake = Path(self.temp.name) / "fake godot.ps1"
        self.fake.write_text("""$log = $args[[array]::IndexOf($args, '--log-file') + 1]
$root = $args[[array]::IndexOf($args, '--path') + 1]
[IO.File]::WriteAllText((Join-Path $root 'child-started.txt'), [string]$PID)
[IO.File]::WriteAllLines((Join-Path $root 'received-args.txt'), [string[]]$args)
Write-Output 'child stdout, not JSON'
[Console]::Error.WriteLine('child stderr, not JSON')
if ($args -contains '--fake-wait') { Start-Sleep -Seconds 2 }
if ($args -notcontains '--fake-stale') { [IO.File]::WriteAllText($log, "Godot Engine fixture`n") }
if ($args -contains '--fake-error') { [IO.File]::AppendAllText($log, "ERROR: fixture`n") }
if ($args -contains '--fake-stdout-error') { [Console]::Out.WriteLine('ERROR: fixture') }
if ($args -contains '--fake-stderr-error') { [Console]::Error.WriteLine('ERROR: fixture') }
if ($args -contains '--fake-warning') { [Console]::Error.WriteLine('WARNING: fixture') }
if ($args -contains '--fake-many-errors') {
    1..60 | ForEach-Object { [Console]::Error.WriteLine("ERROR: fixture $_") }
}
if ($args -contains '--fake-repeated-errors') {
    1..60 | ForEach-Object { [Console]::Error.WriteLine('ERROR: repeated') }
    [Console]::Error.WriteLine('SCRIPT ERROR: after repeats')
}
if ($args -contains '--fake-exit') { exit 23 }
exit 0
""")

    def command(self, skill, script, params, before="", after=""):
        invocation = Path(self.temp.name) / f"{time.monotonic_ns()}.json"
        invocation.write_text(json.dumps(params))
        env = os.environ.copy()
        env.update(
            SKILL_TEST_SCRIPT=str(SCRIPT_ROOTS[skill] / script),
            SKILL_TEST_PARAMS=str(invocation),
            SKILL_TEST_PYTHON=sys.executable,
        )
        cmd = [
            PWSH,
            "-NoProfile",
            "-Command",
            "$p = Get-Content -LiteralPath $env:SKILL_TEST_PARAMS -Raw | ConvertFrom-Json -AsHashtable; "
            + before
            + " & $env:SKILL_TEST_SCRIPT @p; $testExit = $LASTEXITCODE; "
            + after
            + "; exit $testExit",
        ]
        return cmd, env

    def call(self, skill, script, params, before="", after=""):
        cmd, env = self.command(skill, script, params, before, after)
        run = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=20)
        self.assertTrue(run.stdout.strip(), run.stderr)
        return run.returncode, json.loads(run.stdout)

    def preflight(self, path="", **kwargs):
        return self.call(
            "godot-build-and-diagnostics",
            "prepare_godot_log.ps1",
            {
                "ProjectRoot": str(self.root),
                "RequestedLogFile": str(path),
                "Json": True,
                **kwargs,
            },
        )

    def runner_params(self, **kwargs):
        return {
            "GodotExecutable": str(self.fake),
            "ProjectRoot": str(self.root),
            "Purpose": "smoke",
            "Json": True,
            **kwargs,
        }

    def runner(self, **kwargs):
        return self.call(
            "godot-build-and-diagnostics",
            "invoke_godot.ps1",
            self.runner_params(**kwargs),
        )

    def test_godot_path_boundaries_and_external_approval(self):
        code, result = self.preflight()
        self.assertEqual((code, result["status"]), (0, "ready"))
        external = Path(self.temp.name) / "project with spaces-other" / "out.log"
        for path in ("../outside.log", external):
            code, result = self.preflight(path)
            self.assertEqual((code, result["status"]), (1, "blocked"))
        self.assertFalse(external.parent.exists())
        code, result = self.preflight(
            external, AllowExternal=True, ExternalPathReason="explicit test fixture"
        )
        self.assertEqual((code, result["isExternal"]), (0, True))

    def test_godot_rejects_directory_and_file_links(self):
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        for kind in ("directory", "file", "dangling"):
            with self.subTest(kind=kind):
                linked = self.root / (
                    "linked-dir" if kind == "directory" else "linked.log"
                )
                target = outside if kind == "directory" else outside / "target.log"
                if kind == "file":
                    target.write_text("untouched")
                elif kind == "dangling" and target.exists():
                    target.unlink()
                try:
                    linked.symlink_to(target, target_is_directory=kind == "directory")
                except OSError as exc:
                    self.skipTest(f"Symlink creation unavailable: {exc}")
                try:
                    code, result = self.preflight(
                        linked / "out.log" if kind == "directory" else linked
                    )
                    self.assertEqual((code, result["status"]), (1, "blocked"))
                    self.assertIn("reparse point", " ".join(result["blockers"]))
                    if kind == "file":
                        self.assertEqual(target.read_text(), "untouched")
                finally:
                    linked.unlink()

    def test_godot_existing_file_readonly_directory_and_lock(self):
        path = self.root / "existing.log"
        path.write_text("original")
        code, _ = self.preflight(path)
        self.assertEqual(code, 0)
        self.assertEqual(path.read_text(), "original")
        path.chmod(0o444)
        try:
            code, _ = self.preflight(path)
            self.assertEqual(code, 1)
        finally:
            path.chmod(0o644)
        path.unlink()
        path.mkdir()
        self.assertEqual(self.preflight(path)[0], 1)
        path.rmdir()
        path.write_text("original")
        params = {
            "ProjectRoot": str(self.root),
            "RequestedLogFile": str(path),
            "Json": True,
        }
        code, result = self.call(
            "godot-build-and-diagnostics",
            "prepare_godot_log.ps1",
            params,
            '$lock = [IO.File]::Open($p.RequestedLogFile, "Open", "ReadWrite", "None"); try {',
            "} finally { $lock.Dispose() }",
        )
        self.assertEqual((code, result["status"]), (1, "blocked"))
        self.assertFalse((self.root / ".gitignore").exists())

    def test_runner_json_arguments_unique_logs_raw_exit_and_errors(self):
        code, first = self.runner(
            EngineArgs=["--headless", "--scene", "res://a b.tscn"],
            UserArgs=["--sample", "hello world"],
        )
        self.assertEqual((code, first["status"]), (0, "success"))
        self.assertEqual(first["userArgs"], ["--sample", "hello world"])
        args = (self.root / "received-args.txt").read_text().splitlines()
        self.assertEqual(args[-3:], ["--", "--sample", "hello world"])
        self.assertIn("res://a b.tscn", args)
        self.assertIn("child stdout", Path(first["run"]["stdoutPath"]).read_text())
        self.assertIn("child stderr", Path(first["run"]["stderrPath"]).read_text())
        code, second = self.runner()
        self.assertEqual(code, 0)
        self.assertNotEqual(first["logPath"], second["logPath"])
        for args, expected, kind in (
            (["--fake-exit"], 23, "godot-exit"),
            (["--fake-stale"], 66, "stale-log"),
            (["--fake-error"], 67, "log-errors"),
        ):
            code, result = self.runner(EngineArgs=args)
            self.assertEqual((code, result["failureKind"]), (expected, kind))
        code, _ = self.runner(
            EngineArgs=["--fake-error"], AllowedLogErrorPattern=["^ERROR: fixture$"]
        )
        self.assertEqual(code, 0)

    def test_runner_inspects_each_current_output_stream(self):
        for channel in ("stdout", "stderr"):
            with self.subTest(channel=channel):
                code, result = self.runner(EngineArgs=[f"--fake-{channel}-error"])
                self.assertEqual(
                    (code, result["failureKind"], result["godotExitCode"]),
                    (67, "log-errors", 0),
                )
                self.assertEqual(result["unclassifiedErrors"], ["ERROR: fixture"])
                self.assertNotIn("ERROR:", Path(result["logPath"]).read_text())
                self.assertTrue(
                    any(
                        channel in message
                        and result["run"][f"{channel}Path"] in message
                        for message in result["messages"]
                    )
                )

    def test_runner_output_warnings_duplicates_limits_and_allowlist(self):
        code, result = self.runner(EngineArgs=["--fake-warning"])
        self.assertEqual((code, result["unclassifiedErrors"]), (0, []))
        args = ["--fake-error", "--fake-stdout-error", "--fake-stderr-error"]
        code, result = self.runner(EngineArgs=args)
        self.assertEqual((code, result["unclassifiedErrors"]), (67, ["ERROR: fixture"]))
        for channel, path in (
            ("log", result["logPath"]),
            ("stdout", result["run"]["stdoutPath"]),
            ("stderr", result["run"]["stderrPath"]),
        ):
            self.assertTrue(
                any(
                    channel in message and path in message
                    for message in result["messages"]
                )
            )
        code, result = self.runner(
            EngineArgs=args, AllowedLogErrorPattern=["^ERROR: fixture$"]
        )
        self.assertEqual((code, result["unclassifiedErrors"]), (0, []))
        code, result = self.runner(EngineArgs=["--fake-many-errors"])
        self.assertEqual(code, 67)
        self.assertEqual(
            result["unclassifiedErrors"], [f"ERROR: fixture {i}" for i in range(1, 51)]
        )
        code, result = self.runner(EngineArgs=["--fake-repeated-errors"])
        self.assertEqual(
            (code, result["unclassifiedErrors"]),
            (67, ["ERROR: repeated", "SCRIPT ERROR: after repeats"]),
        )

    def test_runner_output_errors_preserve_exit_and_stale_log_priority(self):
        for extra, expected, kind in (
            (["--fake-exit"], 23, "godot-exit"),
            (["--fake-stale"], 66, "stale-log"),
        ):
            with self.subTest(extra=extra):
                code, result = self.runner(EngineArgs=["--fake-stderr-error", *extra])
                self.assertEqual((code, result["failureKind"]), (expected, kind))
                self.assertEqual(result["unclassifiedErrors"], ["ERROR: fixture"])

    def test_runner_missing_or_unreadable_completed_output_fails(self):
        # Alter a copied runner at the collection/inspection boundary. This avoids
        # racing the live capture handles and adds no production-only test switch.
        source_dir = SCRIPT_ROOTS["godot-build-and-diagnostics"]
        source = (source_dir / "invoke_godot.ps1").read_text(encoding="utf-8")
        marker = "$afterLog = Get-FileSnapshot -Path $preflight.logPath"
        self.assertEqual(source.count(marker), 1)
        copied_dir = Path(self.temp.name) / "inspection-fixture"
        copied_dir.mkdir()
        shutil.copy2(source_dir / "prepare_godot_log.ps1", copied_dir)
        for channel in ("stdout", "stderr"):
            for unreadable in (False, True):
                for raw_exit in (0, 23):
                    with self.subTest(
                        channel=channel, unreadable=unreadable, raw_exit=raw_exit
                    ):
                        injection = f"[IO.File]::Delete($run.{channel}Path); "
                        if unreadable:
                            injection += f"[void][IO.Directory]::CreateDirectory($run.{channel}Path); "
                        (copied_dir / "invoke_godot.ps1").write_text(
                            source.replace(marker, injection + marker), encoding="utf-8"
                        )
                        with patch.dict(
                            SCRIPT_ROOTS, {"godot-build-and-diagnostics": copied_dir}
                        ):
                            code, result = self.runner(
                                EngineArgs=["--fake-exit"] if raw_exit else []
                            )
                        self.assertEqual(
                            (code, result["failureKind"], result["godotExitCode"]),
                            (raw_exit or 69, "output-collection", raw_exit),
                        )
                        self.assertIn(channel, result["run"]["outputError"])
                        self.assertTrue(result["run"]["cleanupConfirmed"])
                        self.assertIn(
                            result["run"][f"{channel}Path"],
                            " ".join(result["messages"]),
                        )

    def test_runner_requires_ignored_companion_paths(self):
        if not shutil.which("git"):
            self.skipTest("git unavailable")
        subprocess.run(["git", "-C", str(self.root), "init", "--quiet"], check=True)
        ignore = self.root / ".gitignore"
        ignore.write_text("*.log\n")
        code, result = self.runner()
        self.assertEqual((code, result["failureKind"]), (65, "preflight"))
        self.assertFalse(list(self.root.rglob("*.lock")))
        self.assertFalse(list(self.root.rglob("*.stdout.txt")))
        self.assertEqual(ignore.read_text(), "*.log\n")

    def test_runner_timeout_and_invalid_budget(self):
        code, result = self.runner(EngineArgs=["--fake-wait"], TimeoutSeconds=0.8)
        self.assertEqual((code, result["failureKind"]), (68, "timeout"))
        self.assertEqual(result["run"]["termination"], "execution-unit-empty")
        self.assertTrue(result["run"]["cleanupConfirmed"])
        self.assertTrue(result["run"]["timedOut"])
        for value in (0, -1):
            self.assertEqual(self.runner(TimeoutSeconds=value)[0], 64)

    @unittest.skipIf(
        os.name == "nt",
        "POSIX inherited-pipe fixture; Windows process semantics remain separate",
    )
    def test_output_collection_failure_preserves_native_exit_and_evidence(self):
        fake = Path(self.temp.name) / "native-fixture"
        fake.write_text(
            "#!"
            + sys.executable
            + "\n"
            + """import pathlib, subprocess, sys
args = sys.argv[1:]
root = pathlib.Path(args[args.index('--path') + 1])
pathlib.Path(args[args.index('--log-file') + 1]).write_text('Godot fixture\\n')
child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(120)'])
(root / 'pipe-child.pid').write_text(str(child.pid))
sys.exit(23)
"""
        )
        fake.chmod(0o755)
        try:
            code, result = self.runner(GodotExecutable=str(fake))
            self.assertEqual(
                (code, result["godotExitCode"], result["failureKind"]),
                (23, 23, "output-collection"),
            )
            self.assertTrue(result["run"]["runId"])
            self.assertTrue(result["run"]["outputError"])
            self.assertTrue(Path(result["run"]["stdoutPath"]).exists())
            self.assertIn("--path", result["engineArgs"])
            self.assert_process_exited(int((self.root / "pipe-child.pid").read_text()))
            self.assertTrue(result["run"]["cleanupConfirmed"])
        finally:
            pid_file = self.root / "pipe-child.pid"
            if pid_file.exists():
                try:
                    os.kill(int(pid_file.read_text()), 15)
                except ProcessLookupError:
                    pass

    @staticmethod
    def process_running(pid):
        if os.name == "nt":
            import ctypes

            api = ctypes.WinDLL("kernel32", use_last_error=True)
            api.OpenProcess.restype = ctypes.c_void_p
            api.WaitForSingleObject.argtypes = [ctypes.c_void_p, ctypes.c_uint]
            api.CloseHandle.argtypes = [ctypes.c_void_p]
            handle = api.OpenProcess(
                0x100000, False, pid
            )  # SYNCHRONIZE, bound to this process instance.
            if not handle:
                if ctypes.get_last_error() == 87:
                    return False
                raise ctypes.WinError(ctypes.get_last_error())
            try:
                state = api.WaitForSingleObject(handle, 0)
                if state not in (0, 258):
                    raise ctypes.WinError(ctypes.get_last_error())
                return state == 258
            finally:
                api.CloseHandle(handle)
        # pidfd is namespace-aware and becomes readable on exit, including unreaped zombies.
        import select

        try:
            handle = os.pidfd_open(pid)
        except ProcessLookupError:
            return False
        try:
            poll = select.poll()
            poll.register(handle, select.POLLIN)
            return not poll.poll(0)
        finally:
            os.close(handle)

    def assert_process_exited(self, pid):
        deadline = time.monotonic() + 5
        while self.process_running(pid) and time.monotonic() < deadline:
            time.sleep(0.02)
        self.assertFalse(
            self.process_running(pid), f"runner left descendant {pid} running"
        )

    def descendant_fixture(self):
        self.fake.write_text("""$root = $args[[array]::IndexOf($args, '--path') + 1]
$log = $args[[array]::IndexOf($args, '--log-file') + 1]
$child = [Diagnostics.Process]::new()
$child.StartInfo.FileName = $env:SKILL_TEST_PYTHON
$child.StartInfo.UseShellExecute = $false
foreach ($arg in @('-c', 'import os,pathlib,sys,time; pathlib.Path(sys.argv[1]).write_text(str(os.getpid())); time.sleep(120)', (Join-Path $root 'descendant.pid'))) {
    $child.StartInfo.ArgumentList.Add($arg)
}
[void]$child.Start()
$deadline = [datetime]::UtcNow.AddSeconds(5)
while (-not (Test-Path (Join-Path $root 'descendant.pid'))) {
    if ([datetime]::UtcNow -gt $deadline) { exit 91 }
    Start-Sleep -Milliseconds 20
}
[IO.File]::WriteAllText($log, "Godot fixture`n")
if ($args -contains '--fake-hang') { Start-Sleep -Seconds 120 }
exit 23
""")

    def cleanup_descendant(self):
        pid_file = self.root / "descendant.pid"
        if pid_file.exists():
            pid = int(pid_file.read_text())
            if self.process_running(pid):
                os.kill(pid, signal.SIGTERM)
            pid_file.unlink()

    def test_runner_parent_exit_and_timeout_cleanup_actual_descendant(self):
        self.descendant_fixture()
        outsider = subprocess.Popen(
            [sys.executable, "-c", "import time; time.sleep(120)"]
        )
        try:
            for args, expected in (([], 23), (["--fake-hang"], 68)):
                with self.subTest(args=args):
                    try:
                        code, result = self.runner(EngineArgs=args, TimeoutSeconds=6)
                        self.assertEqual(code, expected, result)
                        pid = int((self.root / "descendant.pid").read_text())
                        # Assert before fallback cleanup: a status string alone is insufficient evidence.
                        self.assert_process_exited(pid)
                        self.assertTrue(result["run"]["cleanupConfirmed"])
                        self.assertIsNone(
                            outsider.poll(), "unrelated process was terminated"
                        )
                    finally:
                        self.cleanup_descendant()
        finally:
            outsider.terminate()
            outsider.wait(timeout=5)

    def test_runner_interruption_and_controller_exit_cleanup_actual_descendant(self):
        self.descendant_fixture()
        modes = ("terminate",) if os.name == "nt" else ("interrupt", "kill-controller")
        for mode in modes:
            with self.subTest(mode=mode):
                cmd, env = self.command(
                    "godot-build-and-diagnostics",
                    "invoke_godot.ps1",
                    self.runner_params(EngineArgs=["--fake-hang"]),
                )
                runner = subprocess.Popen(
                    cmd,
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                try:
                    deadline = time.monotonic() + 10
                    while (
                        not (self.root / "descendant.pid").exists()
                        and time.monotonic() < deadline
                    ):
                        time.sleep(0.02)
                    pid = int((self.root / "descendant.pid").read_text())
                    self.assertTrue(self.process_running(pid))
                    if mode == "interrupt":
                        runner.send_signal(signal.SIGINT)
                    elif mode == "terminate":
                        runner.terminate()
                    else:
                        runner.kill()
                    runner.communicate(timeout=8)
                    self.assert_process_exited(pid)
                finally:
                    if runner.poll() is None:
                        runner.kill()
                        runner.communicate(timeout=5)
                    self.cleanup_descendant()

    @unittest.skipUnless(os.name == "nt", "Windows junction behavior requires Windows")
    def test_godot_rejects_windows_junction(self):
        target = Path(self.temp.name) / "outside"
        target.mkdir()
        junction = self.root / "linked-directory"
        subprocess.run(
            ["cmd.exe", "/c", "mklink", "/J", str(junction), str(target)],
            capture_output=True,
            text=True,
            check=True,
        )
        try:
            code, result = self.preflight(junction / "out.log")
            self.assertEqual((code, result["status"]), (1, "blocked"))
            self.assertFalse((target / "out.log").exists())
        finally:
            junction.rmdir()

    def test_runner_explicit_log_concurrency(self):
        path = self.root / "shared.log"
        params = self.runner_params(
            RequestedLogFile=str(path), EngineArgs=["--fake-wait"]
        )
        cmd, env = self.command(
            "godot-build-and-diagnostics", "invoke_godot.ps1", params
        )
        first = subprocess.Popen(
            cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        try:
            deadline = time.monotonic() + 8
            while (
                not (self.root / "child-started.txt").exists()
                and time.monotonic() < deadline
            ):
                time.sleep(0.02)
            self.assertTrue((self.root / "child-started.txt").exists())
            code, result = self.runner(RequestedLogFile=str(path))
            self.assertEqual((code, result["failureKind"]), (65, "preflight"))
            output, error = first.communicate(timeout=10)
            self.assertEqual(first.returncode, 0, error)
            self.assertEqual(json.loads(output)["status"], "success")
        finally:
            if first.poll() is None:
                first.kill()
                first.communicate()


if __name__ == "__main__":
    unittest.main()
