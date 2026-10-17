"""Run only inside an isolated Blender process; arguments follow Blender's --."""

import argparse
import contextlib
import importlib.util
import io
import json
import sys
from pathlib import Path

import bpy


def load_audit(path):
    spec = importlib.util.spec_from_file_location("low_poly_audit", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_nonfinite_json(audit):
    # Six observations exercise all classifications, nesting and JSON Pointer escaping.
    original = {
        "nan": float("nan"),
        "positive": float("inf"),
        "negative": float("-inf"),
        "nested": [float("nan"), {"a/b~c": float("inf")}, (float("-inf"),)],
        "finite": [0, 2.5, True, None, "unchanged"],
    }
    replacements = []
    safe = audit._json_safe(original, replacements)
    assert safe == {
        "nan": None,
        "positive": None,
        "negative": None,
        "nested": [None, {"a/b~c": None}, [None]],
        "finite": [0, 2.5, True, None, "unchanged"],
    }, safe
    assert replacements == [
        {"path": "/nan", "classification": "nan"},
        {"path": "/positive", "classification": "positive_infinity"},
        {"path": "/negative", "classification": "negative_infinity"},
        {"path": "/nested/0", "classification": "nan"},
        {"path": "/nested/1/a~1b~0c", "classification": "positive_infinity"},
        {"path": "/nested/2/0", "classification": "negative_infinity"},
    ], replacements
    assert original["positive"] == float("inf"), "Sanitizer mutated its input"
    json.dumps(safe, allow_nan=False)


def run(audit_script, output_path):
    audit = load_audit(audit_script)
    collection = bpy.data.collections.new("AuditFixtures")
    bpy.context.scene.collection.children.link(collection)

    def mesh_object(name, vertices, edges, faces, owner=collection):
        mesh = bpy.data.meshes.new(name + "Mesh")
        mesh.from_pydata(vertices, edges, faces)
        mesh.update()
        obj = bpy.data.objects.new(name, mesh)
        owner.objects.link(obj)
        return obj

    cube = mesh_object(
        "AuditCube",
        [
            (-1, -1, -1),
            (1, -1, -1),
            (1, 1, -1),
            (-1, 1, -1),
            (-1, -1, 1),
            (1, -1, 1),
            (1, 1, 1),
            (-1, 1, 1),
        ],
        [],
        [
            (0, 3, 2, 1),
            (4, 5, 6, 7),
            (0, 1, 5, 4),
            (1, 2, 6, 5),
            (2, 3, 7, 6),
            (3, 0, 4, 7),
        ],
    )
    bevel = cube.modifiers.new("AuditBevel", "BEVEL")
    bevel.width = 0.1
    bevel.segments = 1
    bevel.show_render = False
    cube.scale = (-1, 1, 1)
    cube.data.uv_layers.new(name="UVMap")
    cube.data.color_attributes.new(name="Tint", type="BYTE_COLOR", domain="CORNER")
    cube.data.materials.append(bpy.data.materials.new("AuditMaterial"))
    cube.data.polygons[0].material_index = 5
    clone = cube.copy()
    clone.name = "AuditSharedCube"
    clone.location = (4, 0, 0)
    collection.objects.link(clone)
    plane = mesh_object(
        "AuditPlane", [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)], [], [(0, 1, 2, 3)]
    )
    loose = mesh_object(
        "AuditLoose",
        [(0, 0, 0), (1, 0, 0), (0, 1, 0), (2, 0, 0), (4, 0, 0), (5, 0, 0), (9, 9, 9)],
        [(4, 5)],
        [(0, 1, 2), (0, 1, 3)],
    )
    empty = bpy.data.collections.new("AuditEmpty")
    bpy.context.scene.collection.children.link(empty)
    excluded = bpy.data.collections.new("AuditExcluded")
    bpy.context.scene.collection.children.link(excluded)
    mesh_object(
        "AuditExcludedPlane",
        [(0, 0, 0), (1, 0, 0), (0, 1, 0)],
        [],
        [(0, 1, 2)],
        excluded,
    )
    bpy.context.view_layer.layer_collection.children[excluded.name].exclude = True
    cube.select_set(True)
    bpy.context.view_layer.objects.active = cube
    bpy.context.view_layer.update()

    def snapshot():
        return {
            "active": bpy.context.view_layer.objects.active.name,
            "selected": sorted(obj.name for obj in bpy.context.selected_objects),
            "objects": sorted(obj.name for obj in bpy.data.objects),
            "meshes": sorted(mesh.name for mesh in bpy.data.meshes),
            "materials": sorted(mat.name for mat in bpy.data.materials),
            "collections": sorted(col.name for col in bpy.data.collections),
            "frame": bpy.context.scene.frame_current,
            "filepath": bpy.data.filepath,
            "mesh_data": {
                obj.name: (
                    [tuple(vertex.co) for vertex in obj.data.vertices],
                    [tuple(edge.vertices) for edge in obj.data.edges],
                    [
                        (tuple(face.vertices), face.material_index)
                        for face in obj.data.polygons
                    ],
                    tuple(obj.location),
                    tuple(obj.scale),
                    obj.mode,
                    [
                        (mod.name, mod.type, mod.show_viewport, mod.show_render)
                        for mod in obj.modifiers
                    ],
                    [layer.name for layer in obj.data.uv_layers],
                    [layer.name for layer in obj.data.color_attributes],
                )
                for obj in collection.objects
                if obj.type == "MESH"
            },
        }

    before = snapshot()
    report = audit.audit_meshes(collection_name=collection.name, triangle_budget=1)
    assert before == snapshot(), "Audit mutated scene data or selection"
    by_name = {item["object"]: item for item in report["objects"]}
    assert set(by_name) == {cube.name, clone.name, plane.name, loose.name}, (
        by_name.keys()
    )
    c = by_name[cube.name]
    assert c["base"]["triangles"] == 12, c
    assert c["evaluated"]["triangles"] > c["base"]["triangles"], c
    assert c["transform"]["negative_world_determinant"]
    assert c["viewport_render_modifier_flags_differ"]
    assert c["source_mesh"]["datablock_users"] == 2
    assert set(c["source_mesh"]["objects_sharing_mesh_datablock"]) == {
        cube.name,
        clone.name,
    }
    assert c["base"]["materials"]["invalid_index_face_counts"] == {5: 1}
    assert c["base"]["uv_layers"] == ["UVMap"]
    assert c["base"]["color_layers"][0]["name"] == "Tint"
    assert c["base"]["world_aabb"]["dimensions"] == [2, 2, 2]
    p = by_name[plane.name]["base"]
    assert p["triangles"] == 2
    assert p["topology"]["boundary_edges"] == 4
    assert p["topology"]["non_manifold_edges_including_boundary"] == 4
    assert p["topology"]["non_manifold_edges_excluding_boundary"] == 0
    assert p["warnings"]
    assert not p["materials"]["invalid_index_face_counts"]
    assert p["materials"]["faces_without_any_material_slot"] == 1
    loose_report = by_name[loose.name]["base"]
    assert loose_report["topology"]["loose_vertices"] == 1, loose_report
    assert loose_report["topology"]["loose_edges"] == 1, loose_report
    assert loose_report["degenerate_triangles"]["count"] == 1, loose_report
    assert report["triangle_budget"]["comparison"] == "over_limit"
    assert report["triangle_budget"]["report_only"]
    assert not report["totals"]["includes_expanded_scene_instances"]
    assert report["nonfinite_numeric_fields"] == []

    explicit = audit.audit_meshes(object_names=[plane.name], triangle_budget=2)
    assert (
        explicit["triangle_budget"]["comparison"]
        == "within_limit_for_counted_object_meshes"
    )
    partial = audit.audit_meshes(collection_name=excluded.name, triangle_budget=1)
    assert not partial["totals"]["all_scoped_mesh_objects_evaluated"]
    assert partial["objects"][0]["evaluated"] is None
    assert partial["objects"][0]["evaluated_error"]
    assert (
        partial["triangle_budget"]["comparison"] == "undetermined_incomplete_evaluation"
    )
    assert before == snapshot(), "Additional audit calls mutated the fixture"

    def expect_error(**kwargs):
        try:
            audit.audit_meshes(**kwargs)
        except ValueError:
            return
        raise AssertionError(f"Expected refusal: {kwargs!r}")

    expect_error()
    expect_error(collection_name=empty.name)
    expect_error(collection_name="MissingCollection")
    expect_error(object_names=[])
    expect_error(object_names=cube.name)
    expect_error(object_names=["MissingObject"])
    expect_error(collection_name=collection.name, object_names=[cube.name])
    for budget in (-1, True, 1.5):
        expect_error(collection_name=collection.name, triangle_budget=budget)
    for epsilon in (0, -1, float("nan"), float("inf")):
        expect_error(collection_name=collection.name, relative_area_epsilon=epsilon)
    assert before == snapshot(), "Invalid input changed the fixture"

    # Operators belong only to this fixture; the audit must refuse Edit Mode unchanged.
    for obj in bpy.context.selected_objects:
        obj.select_set(False)
    cube.select_set(True)
    bpy.context.view_layer.objects.active = cube
    bpy.ops.object.mode_set(mode="EDIT")
    expect_error(object_names=[cube.name])
    assert cube.mode == "EDIT", "Audit changed mode"
    bpy.ops.object.mode_set(mode="OBJECT")

    check_nonfinite_json(audit)
    # A finite input can overflow derived area thresholds. Exercise sanitization
    # through the public audit as well as the recursive helper above.
    overflow = audit.audit_meshes(
        object_names=[cube.name, loose.name, plane.name], relative_area_epsilon=1e308
    )
    assert overflow["nonfinite_numeric_fields"] == [
        {
            "path": f"/objects/{index}/{kind}/degenerate_triangles/area_threshold",
            "classification": "positive_infinity",
        }
        for index in range(3)
        for kind in ("base", "evaluated")
    ], overflow["nonfinite_numeric_fields"]
    for item in overflow["objects"]:
        for kind in ("base", "evaluated"):
            assert item[kind]["degenerate_triangles"]["area_threshold"] is None
    json.dumps(overflow, allow_nan=False)
    with contextlib.redirect_stdout(io.StringIO()):
        audit.main(
            [
                "--collection",
                collection.name,
                "--output",
                str(output_path),
                "--triangle-budget",
                "1000",
            ]
        )
    saved = json.loads(output_path.read_text(encoding="utf-8"))
    assert saved["totals"]["scoped_mesh_objects"] == 4
    json.dumps(saved, allow_nan=False)
    print("LOW_POLY_AUDIT_TESTS_PASSED", bpy.app.version_string)
    print("NONFINITE_JSON_TESTS_PASSED 6 reported replacement paths")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audit_script", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1 :])
    run(args.audit_script, args.output)
