"""Read-only, explicitly scoped mesh audit for Blender 4.1+ / 5.x.

Run inside Blender, not system Python. No selection changes, bpy.ops calls,
modifier application, mesh cleanup, or .blend saves are performed.
"""

import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

import bmesh
import bpy


def _bounds(points):
    """Bounds of finite world-space points; an empty mesh has no AABB."""
    if not points:
        return None
    minimum = [min(point[axis] for point in points) for axis in range(3)]
    maximum = [max(point[axis] for point in points) for axis in range(3)]
    size = [high - low for low, high in zip(minimum, maximum)]
    return {"min": minimum, "max": maximum, "dimensions": size}


def _area_squared(a, b, c):
    ab = [b[i] - a[i] for i in range(3)]
    ac = [c[i] - a[i] for i in range(3)]
    cross = [
        ab[1] * ac[2] - ab[2] * ac[1],
        ab[2] * ac[0] - ab[0] * ac[2],
        ab[0] * ac[1] - ab[1] * ac[0],
    ]
    return sum(component * component for component in cross) * 0.25


def _matrix_values(matrix):
    return [[float(value) for value in row] for row in matrix]


def _json_safe(value, replacements, path=""):
    """Replace non-finite floats with null and retain their JSON Pointer paths."""
    if isinstance(value, float) and not math.isfinite(value):
        classification = (
            "nan"
            if math.isnan(value)
            else "positive_infinity"
            if value > 0
            else "negative_infinity"
        )
        replacements.append({"path": path, "classification": classification})
        return None
    if isinstance(value, dict):
        return {
            key: _json_safe(
                item,
                replacements,
                path + "/" + str(key).replace("~", "~0").replace("/", "~1"),
            )
            for key, item in value.items()
        }
    if isinstance(value, (list, tuple)):
        return [
            _json_safe(item, replacements, path + "/" + str(index))
            for index, item in enumerate(value)
        ]
    return value


def _mesh_report(mesh, obj, relative_area_epsilon):
    # These populate transient triangulation/BMesh caches, not scene geometry.
    mesh.calc_loop_triangles()
    world_points = [tuple(obj.matrix_world @ vertex.co) for vertex in mesh.vertices]
    finite_points = [
        point for point in world_points if all(math.isfinite(v) for v in point)
    ]
    nonfinite_vertices = len(world_points) - len(finite_points)
    bounds = _bounds(finite_points)
    diagonal_squared = sum(v * v for v in bounds["dimensions"]) if bounds else 0.0
    area_threshold = diagonal_squared * relative_area_epsilon
    threshold_squared = area_threshold * area_threshold
    degenerate_count = 0
    nonfinite_triangles = 0
    degenerate_sample = []
    for index, triangle in enumerate(mesh.loop_triangles):
        points = [world_points[vertex] for vertex in triangle.vertices]
        if not all(math.isfinite(value) for point in points for value in point):
            nonfinite_triangles += 1
            continue
        if _area_squared(*points) <= threshold_squared:
            degenerate_count += 1
            if len(degenerate_sample) < 20:
                degenerate_sample.append(index)

    bm = bmesh.new()
    try:
        bm.from_mesh(mesh)
        topology = {
            "loose_vertices": sum(not vertex.link_edges for vertex in bm.verts),
            "loose_edges": sum(not edge.link_faces for edge in bm.edges),
            "boundary_edges": sum(edge.is_boundary for edge in bm.edges),
            "non_manifold_edges_including_boundary": sum(
                not edge.is_manifold for edge in bm.edges
            ),
            "non_manifold_edges_excluding_boundary": sum(
                not edge.is_manifold and not edge.is_boundary for edge in bm.edges
            ),
            "edges_with_more_than_two_faces": sum(
                len(edge.link_faces) > 2 for edge in bm.edges
            ),
        }
    finally:
        bm.free()

    slot_count = len(obj.material_slots)
    usage = {}
    for polygon in mesh.polygons:
        usage[polygon.material_index] = usage.get(polygon.material_index, 0) + 1
    # Blender's default index 0 on a mesh with no slots means "unassigned".
    # It is not an out-of-range material error requiring mesh repair.
    invalid = {
        index: count
        for index, count in usage.items()
        if not (0 <= index < slot_count) and not (slot_count == 0 and index == 0)
    }
    colors = getattr(mesh, "color_attributes", None)
    legacy_colors = getattr(mesh, "vertex_colors", None) if colors is None else None
    color_layers = (
        [
            {"name": layer.name, "domain": layer.domain, "data_type": layer.data_type}
            for layer in colors
        ]
        if colors is not None
        else [
            {"name": layer.name, "domain": "CORNER", "data_type": "LEGACY"}
            for layer in (legacy_colors or [])
        ]
    )
    warnings = []
    if topology["boundary_edges"]:
        warnings.append(
            "Open boundaries detected; intentional open surfaces are valid. Review against the brief."
        )
    if topology["non_manifold_edges_excluding_boundary"]:
        warnings.append(
            "Loose or otherwise non-manifold edges detected; inspect intended topology before repair."
        )
    if topology["loose_vertices"]:
        warnings.append(
            "Loose vertices detected; they may be intentional procedural inputs."
        )
    if degenerate_count:
        warnings.append(
            "Zero or very small world-space triangles detected using a scale-relative threshold."
        )
    if invalid:
        warnings.append(
            "Some faces reference material slots outside the available slot range."
        )
    if nonfinite_vertices:
        warnings.append(
            "Non-finite vertex coordinates detected; bounds exclude these vertices and are incomplete."
        )
    return {
        "mesh_name": mesh.name,
        "vertices": len(mesh.vertices),
        "edges": len(mesh.edges),
        "polygons": len(mesh.polygons),
        "triangles": len(mesh.loop_triangles),
        "world_aabb": bounds,
        "world_aabb_complete": nonfinite_vertices == 0,
        "nonfinite_vertices": nonfinite_vertices,
        "nonfinite_triangles": nonfinite_triangles,
        "topology": topology,
        "degenerate_triangles": {
            "count": degenerate_count,
            "first_20_loop_triangle_indices": degenerate_sample,
            "space": "world",
            "area_threshold": area_threshold,
            "relative_area_epsilon": relative_area_epsilon,
            "formula": "triangle_area <= world_AABB_diagonal_squared * relative_area_epsilon",
        },
        "materials": {
            "slot_count": slot_count,
            "slots": [
                {
                    "index": i,
                    "material": slot.material.name if slot.material else None,
                    "link": slot.link,
                }
                for i, slot in enumerate(obj.material_slots)
            ],
            "used_valid_slot_indices": sorted(
                index for index in usage if 0 <= index < slot_count
            ),
            "face_count_by_material_index": usage,
            "invalid_index_face_counts": invalid,
            "faces_without_any_material_slot": len(mesh.polygons)
            if slot_count == 0
            else 0,
        },
        "uv_layers": [layer.name for layer in mesh.uv_layers],
        "color_layers": color_layers,
        "warnings": warnings,
    }


def _resolve_scope(collection_name, object_names):
    if (collection_name is None) == (object_names is None):
        raise ValueError(
            "Supply exactly one explicit collection_name or object_names scope."
        )
    if collection_name is not None:
        if not isinstance(collection_name, str) or not collection_name.strip():
            raise ValueError(
                "collection_name must be a nonempty exact collection name."
            )
        collection = bpy.data.collections.get(collection_name)
        if collection is None:
            raise ValueError(f"Collection not found: {collection_name!r}")
        objects = list(collection.all_objects)
        scope = {"kind": "collection_recursive", "name": collection.name}
    else:
        if isinstance(object_names, str):
            raise ValueError(
                "object_names must be an explicit sequence of object names, not a string."
            )
        names = list(object_names)
        if not names or any(
            not isinstance(name, str) or not name.strip() for name in names
        ):
            raise ValueError("object_names must contain nonempty exact object names.")
        missing = [name for name in names if bpy.data.objects.get(name) is None]
        if missing:
            raise ValueError(f"Objects not found: {missing!r}")
        objects = [bpy.data.objects[name] for name in dict.fromkeys(names)]
        scope = {"kind": "explicit_object_names", "names": list(dict.fromkeys(names))}
    meshes = sorted(
        (obj for obj in objects if obj.type == "MESH"), key=lambda obj: obj.name
    )
    if not meshes:
        raise ValueError(
            "The explicit scope contains no mesh objects; refusing an empty audit."
        )
    editing = [
        obj.name
        for obj in meshes
        if obj.mode == "EDIT" or getattr(obj.data, "is_editmode", False)
    ]
    if editing:
        raise ValueError(
            f"Exit mesh Edit Mode before auditing; no mode change was made: {editing!r}"
        )
    scope["mesh_object_names"] = [obj.name for obj in meshes]
    scope["skipped_non_mesh_objects"] = [
        {"name": obj.name, "type": obj.type, "instance_type": obj.instance_type}
        for obj in sorted(objects, key=lambda obj: obj.name)
        if obj.type != "MESH"
    ]
    return scope, meshes


def audit_meshes(
    *,
    collection_name=None,
    object_names=None,
    triangle_budget=None,
    relative_area_epsilon=1e-12,
):
    """Return JSON-compatible observations without repairing or changing scene data.

    `triangle_budget` compares the evaluated object-mesh subtotal only. Instances,
    non-mesh objects, other view layers, and render-only geometry are not included.
    """
    if triangle_budget is not None and (
        isinstance(triangle_budget, bool)
        or not isinstance(triangle_budget, int)
        or triangle_budget < 0
    ):
        raise ValueError("triangle_budget must be a nonnegative integer or None.")
    if not math.isfinite(relative_area_epsilon) or relative_area_epsilon <= 0:
        raise ValueError("relative_area_epsilon must be finite and greater than zero.")
    scope, objects = _resolve_scope(collection_name, object_names)
    depsgraph = bpy.context.evaluated_depsgraph_get()
    # IDs absent from this graph cannot support a trustworthy evaluated report.
    evaluated_object_names = {obj.original.name for obj in depsgraph.objects}
    reports = []
    for obj in objects:
        matrix = obj.matrix_world
        determinant = float(matrix.to_3x3().determinant())
        modifiers = []
        for modifier in obj.modifiers:
            record = {
                "name": modifier.name,
                "type": modifier.type,
                "show_viewport": modifier.show_viewport,
                "show_render": modifier.show_render,
            }
            if modifier.type == "NODES":
                group = getattr(modifier, "node_group", None)
                record["node_group"] = group.name if group else None
            modifiers.append(record)
        report = {
            "object": obj.name,
            "source_mesh": {
                "name": obj.data.name,
                "datablock_users": obj.data.users,
                "objects_sharing_mesh_datablock": sorted(
                    other.name
                    for other in bpy.data.objects
                    if other.type == "MESH" and other.data == obj.data
                ),
            },
            "transform": {
                "location": list(obj.location),
                "scale": list(obj.scale),
                "rotation_mode": obj.rotation_mode,
                "matrix_local": _matrix_values(obj.matrix_local),
                "matrix_world": _matrix_values(matrix),
                "world_linear_determinant": determinant,
                "negative_world_determinant": determinant < 0,
                "singular_world_transform": determinant == 0,
                "blender_object_dimensions_property": list(obj.dimensions),
            },
            "modifiers": modifiers,
            "viewport_render_modifier_flags_differ": any(
                mod["show_viewport"] != mod["show_render"] for mod in modifiers
            ),
            "geometry_nodes_present": any(mod["type"] == "NODES" for mod in modifiers),
            "instance_type": obj.instance_type,
            "base": _mesh_report(obj.data, obj, relative_area_epsilon),
            "evaluated": None,
            "evaluated_error": None,
        }
        if obj.name not in evaluated_object_names:
            report["evaluated_error"] = (
                "Object is absent from the current dependency graph (for example, an excluded collection)."
            )
        else:
            evaluated = None
            try:
                evaluated = obj.evaluated_get(depsgraph)
                mesh = evaluated.to_mesh(
                    preserve_all_data_layers=True, depsgraph=depsgraph
                )
                if mesh is None:
                    report["evaluated_error"] = (
                        "Evaluated object did not produce a mesh."
                    )
                else:
                    report["evaluated"] = _mesh_report(
                        mesh, evaluated, relative_area_epsilon
                    )
            except Exception as error:
                report["evaluated_error"] = f"{type(error).__name__}: {error}"
            finally:
                if evaluated is not None:
                    evaluated.to_mesh_clear()
        reports.append(report)

    evaluated_subtotal = sum(
        item["evaluated"]["triangles"]
        for item in reports
        if item["evaluated"] is not None
    )
    evaluated_count = sum(item["evaluated"] is not None for item in reports)
    complete = evaluated_count == len(reports)
    limitations = [
        "Counts describe scoped object mesh data, not a full rendered scene or engine draw-call count.",
        "Evaluated geometry uses the current scene, frame, view layer and dependency-graph mode; it is not a separate render evaluation.",
        "Collection instances, particle instances, un-realized Geometry Nodes instances, and other dependency-graph instance placements are not expanded or counted.",
        "Geometry Nodes mesh components can be counted, but curves, points, volumes and un-realized instances are outside this mesh audit.",
        "Shared mesh datablocks are counted once per scoped object placement; datablock users are reported separately.",
        "Mesh vertices are not exported/runtime vertex counts; UV seams, split normals, materials and exporter processing can change those counts.",
        "Topology warnings require asset intent; open boundaries and disconnected geometry can be intentional.",
        "This audit does not prove correct normals, absence of self-intersections, visual quality, deformation quality, collision validity, UV packing or export compatibility.",
    ]
    result = {
        "schema_version": 1,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "blender_version": bpy.app.version_string,
        "blend_file": bpy.data.filepath or None,
        "context": {
            "scene": bpy.context.scene.name,
            "view_layer": bpy.context.view_layer.name,
            "frame": bpy.context.scene.frame_current,
            "frame_subframe": bpy.context.scene.frame_subframe,
            "depsgraph_mode": getattr(depsgraph, "mode", "UNKNOWN"),
        },
        "scope": scope,
        "objects": reports,
        "totals": {
            "scoped_mesh_objects": len(reports),
            "base_triangles_per_object_sum": sum(
                item["base"]["triangles"] for item in reports
            ),
            "evaluated_mesh_objects": evaluated_count,
            "evaluated_triangles_subtotal": evaluated_subtotal,
            "all_scoped_mesh_objects_evaluated": complete,
            "includes_expanded_scene_instances": False,
        },
        "triangle_budget": None,
        "limitations": limitations,
    }
    if triangle_budget is not None:
        result["triangle_budget"] = {
            "limit": triangle_budget,
            "basis": "evaluated scoped object-mesh subtotal; excludes expanded instances and non-mesh geometry",
            "observed_subtotal": evaluated_subtotal,
            "subtotal_exceeds_limit": evaluated_subtotal > triangle_budget,
            "all_scoped_mesh_objects_evaluated": complete,
            "comparison": (
                "over_limit"
                if evaluated_subtotal > triangle_budget
                else "within_limit_for_counted_object_meshes"
                if complete
                else "undetermined_incomplete_evaluation"
            ),
            "report_only": True,
        }
    nonfinite_fields = []
    result = _json_safe(result, nonfinite_fields)
    result["nonfinite_numeric_fields"] = nonfinite_fields
    if nonfinite_fields:
        result["limitations"].append(
            "Non-finite numeric observations were replaced with null for valid JSON; "
            "nonfinite_numeric_fields records their JSON Pointer paths and original numeric classifications. "
            "Nulls do not mean zero or an acceptable transform."
        )
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--collection",
        required=True,
        help="Exact collection name; child collections are included.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional JSON destination. Parent directory must already exist.",
    )
    parser.add_argument(
        "--triangle-budget",
        type=int,
        help="Report-only budget for the evaluated object-mesh subtotal.",
    )
    parser.add_argument("--relative-area-epsilon", type=float, default=1e-12)
    args = parser.parse_args(argv)
    try:
        result = audit_meshes(
            collection_name=args.collection,
            triangle_budget=args.triangle_budget,
            relative_area_epsilon=args.relative_area_epsilon,
        )
    except (ValueError, TypeError) as error:
        parser.error(str(error))
    payload = json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return result


if __name__ == "__main__":
    # Blender handles arguments before --. Requiring -- prevents accidental
    # interpretation of Blender's command line as an implicit audit scope.
    main(sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else [])
