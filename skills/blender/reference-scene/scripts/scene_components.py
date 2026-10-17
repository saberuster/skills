"""Small deterministic mesh-part library; pure geometry first, optional bpy assembly."""

import math


def positive(*values):
    if any(
        isinstance(v, bool)
        or not isinstance(v, (int, float))
        or not math.isfinite(v)
        or v <= 0
        for v in values
    ):
        raise ValueError("Dimensions must be finite and positive")


def vec(value):
    if len(value) != 3 or any(not math.isfinite(x) for x in value):
        raise ValueError("Expected a finite 3-vector")
    return tuple(value)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cross(a, b):
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def normalized(v):
    v = vec(v)
    length = math.sqrt(dot(v, v))
    if length < 1e-12:
        raise ValueError("Direction cannot be zero")
    return tuple(x / length for x in v)


def box(name, center, size, material="surface"):
    if not isinstance(name, str) or not name:
        raise ValueError("Name is required")
    center = vec(center)
    size = vec(size)
    positive(*size)
    vertices = [
        (
            center[0] + x * size[0] / 2,
            center[1] + y * size[1] / 2,
            center[2] + z * size[2] / 2,
        )
        for x, y, z in [
            (-1, -1, -1),
            (1, -1, -1),
            (1, 1, -1),
            (-1, 1, -1),
            (-1, -1, 1),
            (1, -1, 1),
            (1, 1, 1),
            (-1, 1, 1),
        ]
    ]
    return {
        "name": name,
        "vertices": vertices,
        "faces": [
            (0, 3, 2, 1),
            (4, 5, 6, 7),
            (0, 1, 5, 4),
            (1, 2, 6, 5),
            (2, 3, 7, 6),
            (3, 0, 4, 7),
        ],
        "material": material,
    }


def frame(name, width, depth, height, post=0.1, beam=0.12):
    positive(width, depth, height, post, beam)
    if 2 * post >= min(width, depth) or beam >= height:
        raise ValueError("Frame members exceed opening")
    parts = [
        box(
            f"{name}_post{i}",
            (x, y, (height - beam) / 2),
            (post, post, height - beam),
            "structure",
        )
        for i, (x, y) in enumerate(
            [
                (x, y)
                for x in (-(width - post) / 2, (width - post) / 2)
                for y in (-(depth - post) / 2, (depth - post) / 2)
            ]
        )
    ]
    parts += [
        box(
            f"{name}_beam{i}",
            (0, y, height - beam / 2),
            (width, post, beam),
            "structure",
        )
        for i, y in enumerate((-(depth - post) / 2, (depth - post) / 2))
    ]
    parts += [
        box(
            f"{name}_cross{i}",
            (x, 0, height - beam / 2),
            (post, depth - 2 * post, beam),
            "structure",
        )
        for i, x in enumerate((-(width - post) / 2, (width - post) / 2))
    ]
    return parts


def table(name, width, depth, height, leg=0.07, top=0.05):
    positive(width, depth, height, leg, top)
    if 2 * leg >= min(width, depth) or top >= height:
        raise ValueError("Table dimensions leave no usable structure")
    parts = [
        box(name + "_top", (0, 0, height - top / 2), (width, depth, top), "surface")
    ]
    parts += [
        box(
            f"{name}_leg{i}",
            (x, y, (height - top) / 2),
            (leg, leg, height - top),
            "structure",
        )
        for i, (x, y) in enumerate(
            [
                (x, y)
                for x in (-(width - leg) / 2, (width - leg) / 2)
                for y in (-(depth - leg) / 2, (depth - leg) / 2)
            ]
        )
    ]
    return parts


def fence(name, width, height, count=9, gap=0.03, thickness=0.04):
    positive(width, height, gap, thickness)
    if type(count) is not int or count < 2:
        raise ValueError("Fence count must be an integer >= 2")
    slat = (width - (count - 1) * gap) / count
    positive(slat)
    parts = [
        box(
            f"{name}_slat{i}",
            (-width / 2 + slat / 2 + i * (slat + gap), 0, height / 2),
            (slat, thickness, height),
            "surface",
        )
        for i in range(count)
    ]
    parts += [
        box(
            f"{name}_rail{i}",
            (0, thickness, z),
            (width, thickness, height * 0.08),
            "structure",
        )
        for i, z in enumerate((height * 0.2, height * 0.8))
    ]
    return parts


def place(parts, origin=(0, 0, 0), forward=(1, 0, 0), up=(0, 0, 1), prefix=""):
    """Local X follows forward; local Y is up cross forward; local Z is corrected up."""
    origin = vec(origin)
    x = normalized(forward)
    y = normalized(cross(normalized(up), x))
    z = cross(x, y)
    return [
        dict(
            p,
            name=prefix + p["name"],
            vertices=[
                tuple(
                    origin[i] + v[0] * x[i] + v[1] * y[i] + v[2] * z[i]
                    for i in range(3)
                )
                for v in p["vertices"]
            ],
        )
        for p in parts
    ]


def repeat(parts, count, step, prefix="copy"):
    if type(count) is not int or count < 1:
        raise ValueError("Repeat count must be a positive integer")
    step = vec(step)
    return [
        part
        for i in range(count)
        for part in place(parts, tuple(i * x for x in step), prefix=f"{prefix}{i}_")
    ]


def bounds(parts):
    vertices = [v for p in parts for v in p["vertices"]]
    if not vertices:
        raise ValueError("No geometry")
    return (
        [min(v[i] for v in vertices) for i in range(3)],
        [max(v[i] for v in vertices) for i in range(3)],
    )


def build_blender(parts, collection_name, palette):
    """Create a new collection only after validating all geometry/names/material keys."""
    import bpy

    names = [p["name"] for p in parts]
    if (
        not parts
        or len(names) != len(set(names))
        or any(n in bpy.data.objects for n in names)
    ):
        raise ValueError("Empty parts or conflicting names")
    if collection_name in bpy.data.collections:
        raise ValueError("Collection already exists")
    for p in parts:
        if p["material"] not in palette:
            raise ValueError("Missing palette entry")
        for vertex in p["vertices"]:
            vec(vertex)
        if any(
            len(f) < 3
            or any(type(i) is not int or not 0 <= i < len(p["vertices"]) for i in f)
            for f in p["faces"]
        ):
            raise ValueError("Invalid face")
    materials = {}
    for key in {p["material"] for p in parts}:
        color = palette[key]
        if len(color) != 4 or any(
            not math.isfinite(x) or not 0 <= x <= 1 for x in color
        ):
            raise ValueError("Invalid palette colour")
    collection = bpy.data.collections.new(collection_name)
    bpy.context.scene.collection.children.link(collection)
    created = []
    meshes = []
    try:
        for key in {p["material"] for p in parts}:
            material = bpy.data.materials.new(collection_name + "_" + key)
            material.use_nodes = True
            material.node_tree.nodes.get("Principled BSDF").inputs[
                "Base Color"
            ].default_value = palette[key]
            material.node_tree.nodes.get("Principled BSDF").inputs[
                "Roughness"
            ].default_value = 0.7
            materials[key] = material
        for p in parts:
            mesh = bpy.data.meshes.new(p["name"])
            meshes.append(mesh)
            mesh.from_pydata(p["vertices"], [], p["faces"])
            mesh.update()
            uv = mesh.uv_layers.new(name="UV0")
            for poly in mesh.polygons:
                for j, loop in enumerate(poly.loop_indices):
                    angle = 2 * math.pi * j / poly.loop_total
                    uv.data[loop].uv = (
                        0.5 + 0.5 * math.cos(angle),
                        0.5 + 0.5 * math.sin(angle),
                    )
            mesh.materials.append(materials[p["material"]])
            obj = bpy.data.objects.new(p["name"], mesh)
            collection.objects.link(obj)
            created.append(obj)
        return created
    except Exception:
        for obj in created:
            bpy.data.objects.remove(obj, do_unlink=True)
        for mesh in meshes:
            bpy.data.meshes.remove(mesh)
        for material in materials.values():
            bpy.data.materials.remove(material)
        bpy.data.collections.remove(collection)
        raise
