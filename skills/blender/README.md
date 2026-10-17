# Blender skills

Each leaf directory is an independent skill package:

- [Blender Low-Poly Modeling](blender-low-poly/SKILL.md) builds and reviews
  stylized models, with optional game asset delivery and a read-only mesh audit.
- [Character Rig](character-rig/SKILL.md) diagnoses and repairs existing rigs
  and skin deformation with pose comparisons and animation regression checks.
- [Reference Scene](reference-scene/SKILL.md) reconstructs editable environments
  from visual references, with optional reusable geometry and audit helpers.

Use a Blender-capable editor integration or an installed Blender executable
for scene operations. Python helpers that import `bpy` or `bmesh` run inside
Blender; pure geometry helpers can run with ordinary Python. Match API and
export options to the installed Blender version. Engine delivery requires the
actual target engine and its own import and runtime validation.

Repository checks validate packaging, documentation, and isolated regressions.
Blender integration tests skip unless `BLENDER` names an existing executable.
Numerical audits and successful scripts do not establish visual quality,
deformation quality, export fidelity, or engine acceptance. Retain the limits
recorded in each skill and its references.
