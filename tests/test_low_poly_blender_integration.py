"""Optional real-Blender regression for the low-poly audit helper.

Set BLENDER to the Blender executable's full path, then run from the repo root:
python -m unittest discover -s tests -p test_low_poly_blender_integration.py -v
"""

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
AUDIT_SCRIPT = (
    REPO_ROOT
    / "skills"
    / "blender"
    / "blender-low-poly"
    / "scripts"
    / "audit_meshes.py"
)
FIXTURE = Path(__file__).with_name("low_poly_blender_fixture.py")
BLENDER = os.environ.get("BLENDER")


@unittest.skipUnless(
    BLENDER and Path(BLENDER).is_file(),
    "Set BLENDER to the full path of a Blender executable to run integration tests.",
)
class LowPolyBlenderIntegrationTests(unittest.TestCase):
    def test_scoped_read_only_audit(self):
        self.assertTrue(
            AUDIT_SCRIPT.is_file(), f"Audit script is missing: {AUDIT_SCRIPT}"
        )
        with tempfile.TemporaryDirectory(prefix="low-poly-audit-") as temporary:
            work = Path(temporary)
            config = work / "config"
            config.mkdir()
            output = work / "audit-report.json"
            environment = os.environ.copy()
            environment["BLENDER_USER_CONFIG"] = str(config)
            completed = subprocess.run(
                [
                    str(Path(BLENDER).resolve()),
                    "--background",
                    "--factory-startup",
                    "--disable-autoexec",
                    "--python-exit-code",
                    "1",
                    "--python",
                    str(FIXTURE),
                    "--",
                    str(AUDIT_SCRIPT),
                    str(output),
                ],
                cwd=work,
                env=environment,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=180,
                check=False,
            )
            diagnostics = completed.stdout + "\n" + completed.stderr
            self.assertEqual(completed.returncode, 0, diagnostics)
            self.assertIn("LOW_POLY_AUDIT_TESTS_PASSED", completed.stdout, diagnostics)
            self.assertIn(
                "NONFINITE_JSON_TESTS_PASSED 6", completed.stdout, diagnostics
            )
            self.assertTrue(output.is_file(), diagnostics)
            report = json.loads(output.read_text(encoding="utf-8"))
            # Python's JSON reader accepts NaN by default; strict re-encoding rejects it.
            json.dumps(report, allow_nan=False)
            self.assertEqual(report["totals"]["scoped_mesh_objects"], 4)
            self.assertTrue(report["totals"]["all_scoped_mesh_objects_evaluated"])


if __name__ == "__main__":
    unittest.main()
