# Blender automation

Use this reference when controlling Blender through Python, MCP or background
execution. Source IDs PY01-PY09 resolve in [sources.md][link-1]. Respect the
active tool's contract when it differs from a generic example here.

## Capability and state discovery

Record `bpy.app.version_string`, `bpy.app.background`, `bpy.data.filepath`,
active scene, mode and requested objects. Inspect collection membership,
parents, transforms, data users, modifiers and visibility. For an unfamiliar
API, inspect RNA properties or matching-version official documentation. Do not
infer compatibility from a tutorial date or `/latest` page label.

Use purpose-built MCP scene/query/render tools first. Where code execution is
necessary, inspect how the tool returns data; some expect a JSON-serializable
`result`, others capture stdout. Do not assume that filenames on the tool server
are accessible to the agent host. Confirm paths and transport before writing or
retrieving screenshots.

If an interactive MCP connection is unavailable, use an installed Blender
executable in a separate background process when possible. Otherwise provide the
executable script and explicitly mark execution/visual verification pending.
Never claim a simulated tool result.

Example in PowerShell, replacing all paths with observed absolute paths:

```powershell
& 'C:\path\to\blender.exe' --background --factory-startup --python-exit-code 1 --python 'C:\task\build_asset.py'
```

`--factory-startup` is appropriate only in this new isolated process. For
inspecting an existing file, pass its path without overwriting it; disable auto
execution where appropriate to the environment. Read the process exit status and
output, then verify output files.

## Choose operators, data API and BMesh deliberately

| Operation | Preferred practical route |
| --- | --- |
| Scene inspection, names, parameters, materials, collections | Data API; no selection changes necessary |
| Standard primitive creation, origin setting, import/export | Available purpose-built tool, otherwise an operator with explicit context |
| Deterministic custom topology / batch geometry | `Mesh.from_pydata` or BMesh |
| Mesh edits while in Edit Mode | `bmesh.from_edit_mesh`, then `bmesh.update_edit_mesh` |
| Inspect modifier output | Dependency graph evaluated object and temporary mesh |

Operators depend on active object, selection, mode and sometimes editor area.
They return a completion state, not the newly created object. Capture created
object references immediately; auto suffixes such as `.001` make later guessed
name lookup unreliable. Set both selection and active object for each relevant
operator. [PY05]

Use `bpy.context.temp_override(...)` with consistent window/area/region
membership if an operator requires context. A background process has no usable
interactive viewport; choose data operations or a real render instead of
inventing an area. Restore user selection/mode when temporarily changed. [PY06]

## Reliable geometry patterns

For custom meshes, validate vertex indices and face winding before creation.
`from_pydata` does not prevent invalid input. Run `mesh.validate()` on newly
generated data when needed and inspect whether it repaired anything; validation
can mutate a mesh, so it does not belong in a read-only audit. Call
`mesh.update()` after construction. [PY01]

Link new objects into the intended collection; creating a datablock alone does
not display it. Return created objects directly from helper functions. Put
adjustable design parameters in one small configuration section and give parts
semantic names.

For an owned Object Mode BMesh, write changes back with `bm.to_mesh(mesh)` and
release it with `bm.free()` in `finally`. For an Edit Mode BMesh, use
`bmesh.from_edit_mesh(mesh)` and
`bmesh.update_edit_mesh(mesh, loop_triangles=True, destructive=True)` after
topology edits; do not free the borrowed edit BMesh. Accessing `obj.data` during
Edit Mode may read stale data. [PY02, PY04]

Check `obj.data.users` before editing shared geometry. Make the data single-user
only when the intended edit should not propagate. Avoid accidentally making
every repeated chair unique or modifying every chair when only one should
change.

Use object matrices for world-space measurements. Account for parenting and
negative scale. Apply transforms only when the specific static-object workflow
needs it; do not blindly apply transforms to rigs, animated hierarchies or
linked/shared assets.

After changes, update the view layer/dependency graph before reading dimensions
or evaluated results. Do not retain evaluated references across dependency-graph
updates. For evaluated mesh access:

```python
depsgraph = bpy.context.evaluated_depsgraph_get()
evaluated = obj.evaluated_get(depsgraph)
mesh = evaluated.to_mesh()
try:
    mesh.calc_loop_triangles()
    triangles = len(mesh.loop_triangles)
finally:
    evaluated.to_mesh_clear()
```

Treat this mesh as temporary. Do not attach it to persistent scene objects. Use
a documented persistent-copy route when an export copy is required. Also inspect
evaluated instances when they matter: a geometry node or collection instance is
not necessarily represented in the object's direct mesh. [PY03]

## Version-sensitive areas

The dated research baseline is Blender **5.2.2 LTS**; it was both published on
official release/download pages and found on the local executable during
preparation. Future runs must probe their own version. Blender 5.3 was listed as
upcoming in that snapshot. [PY08, PY09]

Blender **4.1 removed** `Mesh.use_auto_smooth`, `auto_smooth_angle`,
`create_normals_split`, `calc_normals_split` and `free_normals_split`. Modern
workflows use sharp/smooth flags, a supported angle-based operation/modifier and
`Mesh.corner_normals`. Do not resurrect removed properties inside broad
`try/except` blocks. [PY07]

Inspect current operator/modifier properties before setting fields from older
tutorials, including Triangulate options, Eevee settings and glTF exporter
parameters. Feature detection must preserve the requested behavior: if a feature
is absent, choose and report an equivalent route or state the limitation.
Silently skipping a setting can change the asset.

For shader construction, locate named sockets or stable identifiers and confirm
they exist; avoid unexplained positional socket indices. For export options,
inspect the registered export operator rather than assuming a memorized keyword
is still accepted.

## Repeatability and recovery

Keep model-generation code, presentation setup and export/audit steps
distinguishable. Parameter changes should not require rewriting unrelated code.
Use a random seed for procedural variants and record it with the asset.

Prefer small, meaningful execution batches with observable outputs. If a long
operation times out, inspect the scene/files/process before retrying; a timeout
does not prove nothing happened. Return created/changed names and metrics, then
obtain a preview. Never repeatedly run an additive script and assume it replaces
old objects.

For repeat runs, use a unique task scope and explicitly owned objects. When
updating existing work, patch the requested parts. Only replace a generated
collection if its ownership is established; do not globally delete objects or
purge all orphaned data.

Save checkpoints to new filenames before hard-to-reverse changes. On failure,
preserve diagnostics and the last good output. Report the actual completed
stage, not an intended final state.

[link-1]: sources.md
