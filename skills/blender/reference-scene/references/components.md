# Parameterized Component Library

`scene_components.py` provides box, frame, table, fence, place, repeat, bounds,
and optional build_blender. Pure geometry has no bpy dependency and supports
quick behavioral checks. Each part contains name/vertices/faces/material data;
use consistent caller-selected length units (meters in these examples).

frame width/depth/height are outside dimensions; post/beam describe sections.
table height includes its top. fence derives board width from overall width,
board count, and gaps. Dimensions must be finite and positive; sections must
preserve openings. Repetition is deterministic; callers wanting variation supply
explicit parameters from a fixed seed.

place aligns local X with forward, local Y with up cross forward, and local Z
with corrected up. Zero or parallel up/forward vectors are rejected. This
mathematical convention does not determine a vehicle's or gate's artistic front.
Map semantic axes into this frame before placement.

build_blender validates name collisions, material keys, and geometry before
creating a new collection; it does not overwrite collections or objects. palette
uses linear RGBA. UVs are usable per-face placeholders for color blocks and
basic checks, with no guarantee of texel density, continuous wood grain, or
production textures. Unwrap or adjust final materials for each surface.

Resolve `<skill-root>` to the directory containing the loaded `SKILL.md`,
including an installed or linked location. Set `$SkillRoot` to that absolute
path and use explicit output paths. These commands work independently of the
caller's working directory:

```powershell
$SkillRoot = '<absolute loaded skill root>'
& $Blender --background --factory-startup --python-exit-code 1 --python "$SkillRoot/scripts/build_example.py" -- --variant courtyard --output '<absolute output directory>/courtyard.blend'
& $Blender --background --factory-startup --python-exit-code 1 --python "$SkillRoot/scripts/build_example.py" -- --variant workshop --output '<absolute output directory>/workshop.blend'
```

The second example changes dimensions, layout, and forward direction and reuses
repeated workbenches. Export only the Environment collection; factory-startup
objects are outside it. The examples omit art details and production lighting
and do not constitute finished reference reconstruction.
