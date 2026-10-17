"""Pure geometry regressions for the reference-scene component library."""

import importlib.util
import math
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "skills/blender/reference-scene/scripts"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


components = load("scene_components", REFERENCE / "scene_components.py")


class ComponentTests(unittest.TestCase):
    def test_dimensions_and_rotated_local_frame(self):
        parts = components.frame("frame", 3, 5, 2.8)
        lo, hi = components.bounds(parts)
        for actual, expect in zip([hi[i] - lo[i] for i in range(3)], [3, 5, 2.8]):
            self.assertAlmostEqual(actual, expect)
        lo, hi = components.bounds(components.place(parts, (10, 20, 1), (0, 1, 0)))
        for actual, expect in zip(lo, [7.5, 18.5, 1]):
            self.assertAlmostEqual(actual, expect)
        for actual, expect in zip(hi, [12.5, 21.5, 3.8]):
            self.assertAlmostEqual(actual, expect)

    def test_closed_box_and_positive_signed_volume(self):
        p = components.box("box", (0, 0, 0), (2, 3, 4))
        edges = {}
        volume = 0
        for face in p["faces"]:
            for a, b in zip(face, face[1:] + face[:1]):
                edge = tuple(sorted((a, b)))
                edges[edge] = edges.get(edge, 0) + 1
            a = p["vertices"][face[0]]
            for i in range(1, len(face) - 1):
                volume += (
                    components.dot(
                        a,
                        components.cross(
                            p["vertices"][face[i]], p["vertices"][face[i + 1]]
                        ),
                    )
                    / 6
                )
        self.assertTrue(all(n == 2 for n in edges.values()))
        self.assertAlmostEqual(volume, 24)

    def test_repeated_parts_have_unique_names_and_bounds(self):
        parts = components.repeat(components.table("table", 2, 1, 0.9), 3, (3, 0, 0))
        self.assertEqual(len(parts), 15)
        self.assertEqual(len({p["name"] for p in parts}), 15)
        self.assertEqual(components.bounds(parts)[1][0], 7)

    def test_invalid_parameters_rejected(self):
        calls = [
            lambda: components.table("t", 0, 1, 1),
            lambda: components.table("t", 1, 1, 0.01),
            lambda: components.frame("f", 1, 1, 1, post=0.6),
            lambda: components.fence("f", 1, 1, 100, gap=0.1),
            lambda: components.repeat([], 0, (1, 0, 0)),
            lambda: components.place([], forward=(0, 0, 1), up=(0, 0, 1)),
            lambda: components.box("b", (0, 0, 0), (math.nan, 1, 1)),
        ]
        for call in calls:
            with self.assertRaises(ValueError):
                call()


if __name__ == "__main__":
    unittest.main()
