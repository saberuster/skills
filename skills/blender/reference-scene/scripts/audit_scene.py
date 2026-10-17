"""Read-only evaluated-mesh audit; closed topology is an explicit per-object requirement."""

import argparse
import json
import math
import sys
from pathlib import Path


def audit(collection_name, requirements=None, meters_per_unit=None):
    import bmesh
    import bpy
    from mathutils import Vector

    req = requirements or {}
    if not isinstance(req, dict) or set(req) - {"require_closed", "gaps", "alignments"}:
        raise ValueError("Unknown requirement fields")
    collection = bpy.data.collections.get(collection_name)
    if collection is None:
        raise ValueError("Unknown collection: " + collection_name)
    objects = {o.name: o for o in collection.all_objects if o.type == "MESH"}
    if not objects:
        raise ValueError("Collection contains no mesh objects")
    unit = (
        meters_per_unit
        if meters_per_unit is not None
        else bpy.context.scene.unit_settings.scale_length
    )
    if not math.isfinite(unit) or unit <= 0:
        raise ValueError("Invalid unit scale")
    closed = req.get("require_closed", [])
    if not isinstance(closed, list) or any(n not in objects for n in closed):
        raise ValueError("Unknown require_closed object")
    records = {}
    issues = []
    deps = bpy.context.evaluated_depsgraph_get()
    images = set()
    for name, obj in sorted(objects.items()):
        evaluated = obj.evaluated_get(deps)
        mesh = evaluated.to_mesh(preserve_all_data_layers=True, depsgraph=deps)
        bm = bmesh.new()
        try:
            bm.from_mesh(mesh)
            bm.transform(obj.matrix_world)
            points = [tuple(v.co * unit) for v in bm.verts]
            if not points or any(not math.isfinite(x) for p in points for x in p):
                issues.append(name + ":empty_or_nonfinite")
                continue
            boundary = sum(e.is_boundary for e in bm.edges)
            nonmanifold = sum(not e.is_manifold for e in bm.edges)
            degenerate = sum(f.calc_area() * unit * unit < 1e-12 for f in bm.faces)
            slots = mesh.materials
            assigned = (
                bool(slots)
                and all(m is not None for m in slots)
                and all(f.material_index < len(slots) for f in bm.faces)
            )
            has_uv = bool(mesh.uv_layers)
            if has_uv:
                has_uv = all(
                    math.isfinite(x)
                    for item in mesh.uv_layers.active.data
                    for x in item.uv
                )
            records[name] = {
                "min_m": [min(v[i] for v in points) for i in range(3)],
                "max_m": [max(v[i] for v in points) for i in range(3)],
                "boundary_edges": boundary,
                "nonmanifold_edges": nonmanifold,
                "degenerate_faces": degenerate,
                "uv0_finite": has_uv,
                "materials_assigned": assigned,
            }
            if name in closed and nonmanifold:
                issues.append(name + ":not_closed_manifold")
            if degenerate or not bm.faces:
                issues.append(name + ":degenerate_or_no_faces")
            if not has_uv:
                issues.append(name + ":missing_or_invalid_uv")
            if not assigned:
                issues.append(name + ":missing_material")
            for mat in slots:
                if mat and mat.use_nodes:
                    for node in mat.node_tree.nodes:
                        if node.type == "TEX_IMAGE":
                            if node.image:
                                images.add(node.image)
                            else:
                                issues.append(name + ":unassigned_image_node")
        finally:
            bm.free()
            evaluated.to_mesh_clear()
    for image in images:
        if image.source in ("GENERATED", "VIEWER"):
            continue  # exists in memory; exportability is a separate question
        if image.source != "FILE":
            issues.append("image:" + image.name + ":unsupported_source_requires_review")
        elif (
            not image.packed_file
            and not Path(bpy.path.abspath(image.filepath)).is_file()
        ):
            issues.append("image:" + image.name + ":missing_file")
    measured = []
    ids = set()
    for kind in ("gaps", "alignments"):
        specs = req.get(kind, [])
        if not isinstance(specs, list):
            raise ValueError(kind + " must be an array")
        for item in specs:
            key = item.get("id")
            if not isinstance(key, str) or not key or key in ids:
                raise ValueError("Missing or duplicate requirement id")
            ids.add(key)
            if kind == "gaps":
                axis = item["axis"]
                minimum = item["minimum_m"]
                if (
                    type(axis) is not int
                    or axis not in (0, 1, 2)
                    or not math.isfinite(minimum)
                    or minimum < 0
                ):
                    raise ValueError("Invalid gap requirement")
                left, right = records[item["left"]], records[item["right"]]
                value = right["min_m"][axis] - left["max_m"][axis]
                passed = value + 1e-6 >= minimum
                measured.append(
                    {"id": key, "gap_m": value, "minimum_m": minimum, "passed": passed}
                )
            else:
                local = Vector(item["local_axis"])
                direction = Vector(item["world_direction"])
                limit = item["maximum_degrees"]
                if (
                    len(local) != 3
                    or len(direction) != 3
                    or any(not math.isfinite(x) for x in [*local, *direction, limit])
                ):
                    raise ValueError("Invalid alignment values")
                world = objects[item["object"]].matrix_world.to_3x3() @ local
                if (
                    world.length < 1e-12
                    or direction.length < 1e-12
                    or not 0 <= limit <= 180
                ):
                    raise ValueError("Invalid alignment direction/limit")
                value = math.degrees(world.angle(direction))
                passed = value <= limit + 1e-5
                measured.append(
                    {
                        "id": key,
                        "angle_degrees": value,
                        "maximum_degrees": limit,
                        "passed": passed,
                    }
                )
            if not passed:
                issues.append("requirement:" + key)
    return {
        "schema_version": 1,
        "passed": not issues,
        "source": bpy.data.filepath,
        "blender_version": bpy.app.version_string,
        "meters_per_unit": unit,
        "collection": collection_name,
        "objects": records,
        "measurements": measured,
        "issues": issues,
    }


def main():
    import bpy

    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--collection", required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--requirements", type=Path)
    p.add_argument("--meters-per-unit", type=float)
    args = p.parse_args(
        sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    )
    inputs = [Path(bpy.data.filepath).resolve()] if bpy.data.filepath else []
    if args.requirements:
        inputs.append(args.requirements.resolve())
    if args.output.resolve() in inputs:
        raise ValueError("Output must not overwrite input")
    try:
        req = (
            json.loads(args.requirements.read_text(encoding="utf-8-sig"))
            if args.requirements
            else {}
        )
        report = audit(args.collection, req, args.meters_per_unit)
        code = 0 if report["passed"] else 1
    except (ValueError, KeyError, TypeError, OSError) as exc:
        report, code = {"passed": False, "input_error": str(exc)}, 2
    args.output.write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print("SCENE_AUDIT", json.dumps({"passed": report["passed"], "code": code}))
    if code:
        raise RuntimeError("SCENE_AUDIT_FAILED code=" + str(code))


if __name__ == "__main__":
    main()
