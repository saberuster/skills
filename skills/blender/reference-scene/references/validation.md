# Geometry and Multiple-View Acceptance

Resolve `$SkillRoot` to the absolute directory containing the loaded `SKILL.md`,
including installed or linked locations. Use explicit input and output paths so
the caller's working directory does not determine script resolution:

```powershell
$SkillRoot = '<absolute loaded skill root>'
& $Blender --background --factory-startup '<absolute scene path>/scene.blend' --python-exit-code 1 --python "$SkillRoot/scripts/audit_scene.py" -- --collection Environment --output '<absolute output directory>/audit.json'
```

Optional `--requirements` accepts data such as the following. Names identify
actual objects in the selected collection; lengths are meters:

```json
{
  "require_closed": ["Cabinet"],
  "gaps": [{"id":"entrance", "left":"LeftPost", "right":"RightPost", "axis":0, "minimum_m":1.2}],
  "alignments": [{"id":"vehicle-forward", "object":"Vehicle", "local_axis":[0,-1,0], "world_direction":[0,-1,0], "maximum_degrees":1.0}]
}
```

gaps measures world-axis AABB separation and suits axis-aligned objects only.
Check inclined or curved routes and door-opening paths in local space or with
collision tests. alignments uses actual world matrices, including parents and
transforms. Measure clearance from real geometry rather than substituting
expected constants.

The script checks evaluated geometry for non-finite coordinates, degenerate
faces, materials, and UVs. Boundary/non-manifold edges are always reported and
fail only for require_closed objects. Texture checks cover file existence or
packing in relevant materials and do not prove complex graphs export. The source
is not saved. `--meters-per-unit` explicitly sets units; the default uses scene
scale. JSON passed records check results: failure exits 1, configuration error
2, success 0. Blender's `--python-exit-code` may unify exception exit codes;
read the report for classification.

Visual coverage includes the main reference angle, opposite direction, sides,
actual height, and occluded regions; choose views for the scene. Check
orientation, supports, thickness, floating/intersecting objects, openings, and
circulation. Save camera and visibility state. Signs of forward T, up U, and
transverse B must match component semantics; do not fix crossbeams to world X.

Distinguish automated geometry, image observation, exchange readback, engine
loading, runtime, and gameplay evidence. A finite screenshot set does not
mathematically prove defect-free 360-degree coverage. Inspect screenshot
contents even when files exist or rendering exits 0: blank, stale, wrong-window,
cropped, or incorrectly oriented images cannot establish acceptance.

For engine delivery, use captures from the target engine as the report's primary
images and before/after comparison. Keep camera and unrelated rendering
conditions comparable, and label intentional differences. Label Blender previews
separately by purpose, such as source inspection or asset thumbnails; do not mix
them with engine captures as evidence of a lighting improvement under equivalent
conditions.

Tie screenshots, recordings, measurements, and acceptance notes to the delivered
revision. After regeneration, refresh affected evidence and dimension-dependent
documentation, or identify them as belonging to an earlier revision.
