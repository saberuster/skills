---
name: blender-low-poly
description: >-
  Create, refine, and validate low-poly models in Blender for stylized scenes
  and game assets. Use for low-poly props, buildings, vehicles, vegetation,
  characters, mesh cleanup, or Blender Python/MCP modeling workflows; includes
  visual iteration and optional game-engine delivery.
---

# Blender Low-Poly Modeling

Build recognizable, deliberately shaped assets and verify the result in the
intended view. Use this workflow with a tool-capable model, including
GPT-6-Astra; the skill supplies procedures and checks, not a model-weight update
or a guarantee of improved performance.

## Read only the needed branch

| Task | Read |
| --- | --- |
| Shape construction, topology, shading, simplification | [modeling-decisions.md][link-1] |
| Particular asset category | Relevant section of [asset-recipes.md][link-2] |
| Python, background Blender, or MCP execution | [blender-automation.md][link-3] |
| Visual review or an unsatisfactory result | [visual-review.md][link-4] |
| Game asset, UV, materials, glTF, Godot | [game-delivery.md][link-5] |
| Quantitative mesh inspection | [audit-helper.md][link-6], then run `scripts/audit_meshes.py` |
| Evidence, version migration, source conflicts | [sources.md][link-7] |

## 1. Establish the asset contract

Read the user's current brief and supplied references. Inspect existing assets
before editing. Resolve these facts from context; state reasonable assumptions
and continue when they do not block useful work:

- Subject and distinguishing silhouette; essential parts and intended use.
- Target camera, projection, viewing distance, output size, and whether other
  views matter.
- Dimensions, ground plane, orientation, attachment points, moving-part pivots.
- Static, rigid moving parts, or skinned deformation; required poses if
  animated.
- Shape language, facet strength, edge treatment, palette, material response.
- Explicit performance budget and simultaneous instances, if supplied; otherwise
  label the budget provisional.
- Deliverables: editable `.blend`, renders, or engine asset with export format.

Separate **shape/style**, **geometry cost**, and **runtime cost**. Flat shading
is not mesh reduction; a smooth-shaded asset can still be low-poly. Do not
invent a universal triangle limit.

For a reference image, first describe the major masses, ratios, negative spaces
and visible construction. Treat obscured/back surfaces as assumptions. Match
proportions before interpreting texture or lighting as geometry.

Use project style constraints only when the project or user supplied them. For
example, a brief asking for flat surfaces and no rounded corners calls for
selective or absent bevels; do not silently impose that preference on every
low-poly asset.

## 2. Inspect and choose an execution route

Record installed Blender version, active file/scene, mode, target
collection/objects, existing transforms, shared meshes, modifiers, materials and
external resources. In a large scene inspect only the requested scope.

Prefer available purpose-built Blender tools for their supported operations. Use
Python for repeatable construction or precise mesh editing; use UI control when
required. Inspect actual tool schemas and API availability rather than inventing
tool names or copying version-specific snippets.

Create a named task collection and retain references to new objects. Preserve
unrelated objects and settings. For a new isolated asset, a separate background
process is useful; never reset the user's open scene to obtain a clean start.
Checkpoint before topology changes or modifier application that would be
difficult to reverse.

The research snapshot is **2026-10-16**: official release pages and the
available local executable reported **Blender 5.2.2 LTS**. This is a dated
baseline, not a permanent latest-version claim. Probe `bpy.app.version` for
every new environment. See the automation reference for the Blender 4.1 normals
migration.

## 3. Decompose, then construct the blockout

Write a short parts plan: part -> construction method -> connection/pivot ->
visual check. Parameterize dimensions that must stay consistent. Choose the
smallest useful set of primitives, extruded sections, or custom meshes.

Establish the main silhouette, mass ratios, ground contact and negative spaces.
Model broad shape changes, taper, thickness and connections. A pile of untouched
primitives is a blockout, not automatically a finished stylized asset.

Use Mirror for symmetry and Array/linked instances for regular repetition when
they preserve editability. Place added edges where they improve visible contour,
planar changes, UV needs, or deformation. Do not distribute detail uniformly.

Inspect the target camera and complementary views before secondary detail. For
an explicitly single-view illustration, prioritize that view but still check
thickness, hidden intersections and shadows where they affect the result.

## 4. Refine structure and surface deliberately

Choose a construction recipe and complete meaningful features before decoration.
Keep moving parts separate with usable pivots. Use connected geometry where
deformation or actual continuity requires it; disconnected parts are acceptable
for assembled rigid objects.

Choose shading per part: deliberate flat facets, continuous smooth curvature, or
smooth regions separated by sharp edges. Use a small bevel only when the brief
and target view benefit. Weighted normals alter lighting, not silhouette. Do not
hide malformed topology with normals or dramatic lighting.

Treat Decimate as an optional reduction operation on suitable input, not as the
definition of low-poly. Preserve a source copy and compare silhouette, thin
parts, boundaries, material separation and deformation. Never apply a universal
modifier stack to every asset.

For organic assets, bound and seed procedural variation. Establish species,
growth direction, plane hierarchy or anatomy before adding variation. Random
vertex noise is not a substitute for designed form.

## 5. Run a build-observe-correct loop

After each meaningful stage, render or capture the actual Blender result.
Inspect the image; successful tool execution and object counts cannot certify
appearance.

1. Compare the result with the contract at target screen size.
2. Identify the highest-impact visible defect using a specific part and
   relation.
3. Make a targeted geometry/material/camera correction.
4. Capture the same view again to verify that correction.

Fix proportion and silhouette before surface detail, then structural
gaps/intersections, then shading/material issues. Keep target framing consistent
between comparisons. Use neutral inspection lighting as well as the intended
presentation; exclude staging meshes from asset budgets/export.

If screenshots or renders cannot be obtained, continue useful structural checks
and report visual validation as unavailable. Do not claim the asset has passed
visual review.

## 6. Validate according to use

- **Shape:** readable silhouette, plausible thickness, required parts,
  deliberate negative spaces and contact points.
- **Mesh:** inspect degenerates, duplicate geometry, loose elements, winding,
  unwanted intersections and modifier results. Distinguish intentional open
  surfaces from accidental holes. Use scale-relative tolerances; do not
  automatically weld or fill every boundary.
- **Animation:** inspect required poses with actual pivots/weights and final
  triangulation; a neutral pose is insufficient.
- **Cost:** report evaluated triangles and material usage. Distinguish Blender
  mesh positions from exported vertex records; verify export/runtime counts
  where relevant.
- **Delivery:** verify file creation, dependencies, export scope,
  scale/orientation, pivots, materials and required animation. Reimport in an
  isolated scene; inspect in the target engine when available. Clearly label
  unperformed checks.

Use the bundled audit helper to collect scoped metrics; interpret its warnings
in context. It does not establish visual quality, self-intersection freedom,
export vertex counts, or whole-scene GPU cost.

## 7. Finish with evidence

Save the editable source and requested outputs. Report the asset, paths, actual
Blender version, evaluated triangle count, material count, checks performed and
remaining limitations. Include an inspected preview when available. Stop when
the asset meets the brief; do not add unrequested detail to consume a budget.

[link-1]: references/modeling-decisions.md
[link-2]: references/asset-recipes.md
[link-3]: references/blender-automation.md
[link-4]: references/visual-review.md
[link-5]: references/game-delivery.md
[link-6]: references/audit-helper.md
[link-7]: references/sources.md
