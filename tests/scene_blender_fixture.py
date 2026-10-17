"""Audit regressions invoked only in a fresh background Blender process."""

import argparse
import importlib.util
import math
import sys
from pathlib import Path

import bpy

parser = argparse.ArgumentParser()
parser.add_argument("root", type=Path)
parser.add_argument("folder", type=Path)
args = parser.parse_args(sys.argv[sys.argv.index("--") + 1 :])


def load(name, filename):
    path = args.root / "skills/blender/reference-scene/scripts" / filename
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


c = load("scene_components", "scene_components.py")
audit = load("audit_scene", "audit_scene.py")

palette = {"surface": (0.4, 0.2, 0.1, 1)}
panel = {
    "name": "OpenPanel",
    "vertices": [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)],
    "faces": [(0, 1, 2, 3)],
    "material": "surface",
}
c.build_blender([panel], "Open", palette)
assert audit.audit("Open")["passed"]
assert not audit.audit("Open", {"require_closed": ["OpenPanel"]})["passed"]
bad = c.build_blender([c.box("BadMaterial", (0, 0, 0), (1, 1, 1))], "Bad", palette)[0]
bad.data.materials.clear()
assert not audit.audit("Bad")["passed"]
degenerate = dict(
    panel,
    name="Degenerate",
    vertices=[(0, 0, 0), (1, 0, 0), (2, 0, 0)],
    faces=[(0, 1, 2)],
)
c.build_blender([degenerate], "DegenerateCollection", palette)
assert not audit.audit("DegenerateCollection")["passed"]
c.build_blender(
    [
        c.box("Left", (-1, 0, 0.5), (0.2, 0.2, 1)),
        c.box("Right", (1, 0, 0.5), (0.2, 0.2, 1)),
    ],
    "Gap",
    palette,
)
req = {
    "gaps": [
        {"id": "gap", "left": "Left", "right": "Right", "axis": 0, "minimum_m": 1.7}
    ]
}
assert audit.audit("Gap", req)["passed"]
req["gaps"][0]["minimum_m"] = 1.9
assert not audit.audit("Gap", req)["passed"]
right = bpy.data.objects["Right"]
right.rotation_euler.z = math.pi / 2
bpy.context.view_layer.update()
req = {
    "alignments": [
        {
            "id": "forward",
            "object": "Right",
            "local_axis": [1, 0, 0],
            "world_direction": [0, 1, 0],
            "maximum_degrees": 0.01,
        }
    ]
}
assert audit.audit("Gap", req)["passed"]
req["alignments"][0]["world_direction"] = [1, 0, 0]
assert not audit.audit("Gap", req)["passed"]
before = set(bpy.data.objects)
try:
    c.build_blender([panel], "ShouldNotExist", palette)
except ValueError:
    pass
else:
    raise AssertionError("Name collision accepted")
assert set(bpy.data.objects) == before and "ShouldNotExist" not in bpy.data.collections
try:
    audit.audit("Gap", {"require_closed": ["typo"]})
except ValueError:
    pass
else:
    raise AssertionError("Unknown requirement accepted")
print("BLENDER_AUDIT_FAILURE_CASES_OK")
