"""Set BLENDER to run actual background Blender tests; no live editor is touched."""

import hashlib
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLENDER = os.environ.get("BLENDER")
REF = ROOT / "skills/blender/reference-scene/scripts"


@unittest.skipUnless(
    BLENDER and Path(BLENDER).is_file(),
    "BLENDER not set to an actual executable; live Blender validation not run",
)
class BlenderIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="scene-skills-")
        cls.folder = Path(cls.temp.name)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def run_blender(self, script, *args, blend=None, success=True):
        command = [BLENDER, "--background", "--factory-startup"]
        if blend:
            command.append(str(blend))
        command += [
            "--python-exit-code",
            "1",
            "--python",
            str(script),
            "--",
            *map(str, args),
        ]
        run = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=180,
        )
        if success:
            self.assertEqual(run.returncode, 0, run.stdout[-6000:] + run.stderr[-2000:])
        else:
            self.assertNotEqual(run.returncode, 0, run.stdout[-2000:])
        return run

    def test_two_compositions_and_audit_cli(self):
        for variant in ("courtyard", "workshop"):
            with self.subTest(variant=variant):
                blend = self.folder / (variant + ".blend")
                report = self.folder / (variant + ".audit.json")
                self.run_blender(
                    REF / "build_example.py", "--variant", variant, "--output", blend
                )
                original = hashlib.sha256(blend.read_bytes()).hexdigest()
                self.run_blender(
                    REF / "audit_scene.py",
                    "--collection",
                    "Environment",
                    "--output",
                    report,
                    blend=blend,
                )
                result = json.loads(report.read_text())
                self.assertTrue(result["passed"])
                self.assertGreater(len(result["objects"]), 20)
                self.assertEqual(
                    original, hashlib.sha256(blend.read_bytes()).hexdigest()
                )
                self.run_blender(
                    REF / "build_example.py",
                    "--variant",
                    variant,
                    "--output",
                    blend,
                    success=False,
                )
                self.assertEqual(
                    original, hashlib.sha256(blend.read_bytes()).hexdigest()
                )

    def test_audit_real_failure_cases(self):
        self.run_blender(ROOT / "tests/scene_blender_fixture.py", ROOT, self.folder)


if __name__ == "__main__":
    unittest.main()
