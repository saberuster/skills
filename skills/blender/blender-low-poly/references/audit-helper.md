# Read-only mesh audit helper

`scripts/audit_meshes.py` produces observations for one explicitly named
collection, including child collections, or an explicit list of object names
through its Python function. It never assumes the selected objects or whole
scene are the intended scope. Missing scope, missing names, no mesh objects, and
mesh Edit Mode are errors. It does not change mode, selection, the active
object, transforms, geometry, modifiers, materials, or the saved `.blend` file.
Temporary mesh caches and dependency-graph evaluation are necessary to inspect
evaluated geometry; the temporary evaluated mesh and temporary BMesh are
released.

## Run

From a terminal, substitute the three paths and exact collection name:

```powershell
& 'C:\path\to\blender.exe' --background 'C:\assets\asset.blend' --python-exit-code 1 --python 'C:\skills\blender-low-poly\scripts\audit_meshes.py' -- --collection 'Asset' --output 'C:\reports\asset-audit.json' --triangle-budget 1500
```

The output folder must exist. The optional JSON output path is an explicit write
destination and an existing file at that path is replaced. Omit `--output` to
print JSON only. Blender also writes its own terminal status lines, so use
`--output` when another program needs a clean JSON file. `--python-exit-code 1`
makes Python exceptions visible to command-line automation. Budget excess and
topology warnings are report data, not process failures.

Inside Blender Python, import the file with `importlib.util` and call:

```python
import importlib.util

spec = importlib.util.spec_from_file_location(
    "low_poly_audit", r"C:\skills\blender-low-poly\scripts\audit_meshes.py"
)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)
report = audit.audit_meshes(
    object_names=["Body", "Wheel.L", "Wheel.R"], triangle_budget=1500
)
```

Supply either `collection_name="Asset"` or `object_names=[...]`, never both. The
helper uses `bpy` and `bmesh`; it must run in Blender. It is intended for
Blender 4.1+ and 5.x. Detecting color attributes and dependency-graph mode
avoids several historical API assumptions; this is not a guarantee of
compatibility with every release. Record `blender_version` from each result.

## What the report means

| Field | Interpretation |
| --- | --- |
| `base.triangles` | `Mesh.loop_triangles` count before modifiers, counted once per scoped object. |
| `evaluated.triangles` | Mesh component after current dependency-graph evaluation; may differ from a render evaluation. |
| `vertices`, `edges`, `polygons` | Blender mesh data counts; not exact engine vertex counts or draw calls. |
| `world_aabb` | Axis-aligned bounds computed from mesh vertices transformed into world space; `null` for an empty mesh. Non-finite vertices are excluded and mark the bounds incomplete. |
| `blender_object_dimensions_property` | Blender's current object property, included for context. Use the per-stage computed AABB when comparing base and evaluated bounds. |
| `transform` | Local/world matrices, scale, determinant, mirrored and singular-transform observations. A negative determinant can come from parents as well as the object's own scale. |
| `source_mesh` | Shared datablock users and object names. Multiple objects using one mesh are counted per object placement, not deduplicated into one scene asset. |
| `modifiers` | Modifier type and viewport/render flags. Different flags warrant export/render checks. Equal flags do not establish identical render output. |
| `materials` | Available slots, assigned slot names, face use, and invalid indices. Default index 0 with zero slots is treated as unassigned, not as corrupted mesh data. |
| `uv_layers`, `color_layers` | Layer names and color attribute domain/type where available; no packing, coverage, seam or texture-quality claim. |
| `topology.loose_vertices` | Vertices with no connected edges. |
| `topology.loose_edges` | Edges with no connected faces. |
| `topology.boundary_edges` | Edges with one adjacent face. Open sheets and cards may intentionally have these. |
| `topology.non_manifold_edges_including_boundary` | BMesh non-manifold edge count, including open boundaries and wire edges. |
| `topology.non_manifold_edges_excluding_boundary` | The previous count with boundary edges excluded; still includes wire edges. |
| `topology.edges_with_more_than_two_faces` | A narrower multi-face edge diagnostic, reported separately. |
| `degenerate_triangles` | Candidates with world-space triangle area <= world AABB diagonal squared * relative epsilon; default epsilon `1e-12`. This is scale-relative, not a fixed meter threshold or a universal defect test. |
| `triangle_budget` | Report-only comparison of counted evaluated object meshes. Incomplete evaluation remains explicit; no hidden decimation or pass/fail exit occurs. |
| `nonfinite_numeric_fields` | JSON Pointer paths and classifications (`nan`, `positive_infinity`, `negative_infinity`) for any non-finite numeric values replaced by JSON `null`. This covers raw transforms/dimensions as well as calculated observations. `null` does not stand for zero or a valid transform. |

## Limits that must remain visible

- Collection instances, particle instances, and dependency-graph instance
  placements are not expanded. Geometry Nodes can output a mesh plus other
  components; the helper only observes the mesh component. Un-realized
  instances, curves, point clouds and volumes can therefore make the visible
  result much larger than the reported subtotal. Inspect these separately before
  claiming a complete scene budget.
- An explicit collection can contain objects excluded from the current view
  layer. Those receive a base report and an `evaluated_error`; totals retain an
  evaluated subtotal and a completeness flag. Non-mesh objects are listed as
  skipped. The script does not enable hidden/excluded collections.
- Current scene, frame, subframe, view layer and dependency-graph mode are
  recorded. The helper does not switch to render settings, inspect every frame,
  realize instances, apply modifiers or triangulate the authored mesh.
- Boundary, loose and small-triangle observations need the asset brief. A grass
  card, open building interior, collision proxy or procedural source has
  different requirements. The script makes no automatic repair.
- UV/normal/material splits, exporter choices, triangulation, indexing and
  engine processing can increase runtime vertex counts. There is no reliable
  draw-call estimate from material slot count alone.
- This is one technical check. It does not detect every self-intersection,
  winding error, shading defect, animation problem, UV issue, collision failure
  or export mismatch. Inspect the model at its intended camera distance and test
  the actual target import.
- Non-finite geometry and transforms are invalid numeric observations. The
  report retains the corresponding diagnostics, replaces non-finite output
  numbers with `null`, and lists their precise paths so strict JSON
  serialization can complete. This serialization safeguard does not repair the
  asset or guarantee Blender can evaluate every corrupted mesh.

The audit uses temporary evaluated meshes with `to_mesh_clear()` in `finally`,
and a temporary BMesh with `free()` in `finally`. It never calls `bpy.ops` or
saves the scene.

## Validation recorded for this version

Executed against Blender **5.2.2 LTS** in a separate
`--background --factory-startup` process. A cube reported 12 base triangles and
44 after a one-segment bevel. An open quad reported 4 boundary edges and zero
non-manifold edges after excluding boundaries. Fixtures also verified loose
vertices/edges, a collinear degenerate triangle, invalid material indices,
UV/color layers, a negative world determinant, shared mesh users, differing
viewport/render flags, and incomplete evaluation of an excluded collection.
Explicit object scope, empty-scope refusal, Edit Mode refusal, report-only
budgets, and JSON output were exercised. A scene snapshot verified unchanged
selection, active object, object/mesh/material/collection datablocks, frame,
file path, source geometry, transforms and modifier flags during the normal
audit. Compatibility with Blender 4.1-5.1 has not been executed in this
validation environment.

After the non-finite serialization fix, the same fixture passed again. A
targeted test injected NaN and positive/negative infinity into reported matrix
values, verified six replacement paths, and successfully serialized the complete
report with `allow_nan=False`. A separate nested-value check covered JSON
Pointer escaping and retention of finite zero, booleans and existing nulls. This
validates report serialization, not Blender's handling of arbitrary corrupted
geometry.

## Reproduce repository regression coverage

From the `skills` repository root, set `BLENDER` to an existing Blender
executable and run:

```powershell
$env:BLENDER = 'C:\path\to\blender.exe'
python -m unittest discover -s tests -p test_low_poly_blender_integration.py -v
```

The repository test uses `tests/low_poly_blender_fixture.py` in a separate
background factory-startup process with temporary output and user-config
directories. It exercises scope refusals, topology and material observations,
read-only state, incomplete evaluation, budgets, strict JSON, and six non-finite
replacement paths. The non-finite public-API case uses finite inputs that
overflow derived area thresholds; a separate nested-value case covers NaN, both
infinities, and JSON Pointer escaping. It does not require or modify an open
editor session. When `BLENDER` is missing or is not a file, the test explicitly
skips. CI unit-test discovery includes this integration test and skips it when
`BLENDER` is missing or is not a file. Set `BLENDER` locally to execute the
fixture when changing the audit. A copied standalone skill remains usable
without these repository-only fixtures.
