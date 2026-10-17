# Game delivery: low-poly assets

Use this reference when the deliverable must run in a game engine. Treat the
rules below as a decision process; project constraints override illustrative
defaults. Resolve source IDs in `sources.md`. Perform version-sensitive steps
against the installed Blender and target-engine versions.

## Establish the delivery contract

- Record engine/version, renderer, target hardware, target resolution, camera
  distance range, and expected visible instance count.
- Identify static props, deforming meshes, articulated parts, transparent
  surfaces, and intentionally open geometry.
- Record units, model forward, ground plane, pivot purpose, attachment points,
  and modular snapping rules.
- State whether the deliverable includes source `.blend`, interchange files,
  textures, collision, animations, or LODs.
- Use the project's budgets. If absent, state provisional budgets and assess the
  asset in a representative scene.
- Separate visual simplicity from runtime cost; flat shading does not reduce
  topology.
- Preserve an editable source and build export results from an explicit
  collection or duplicate.
- Record export settings and external dependencies so another machine can repeat
  the conversion.

## Count the geometry that will actually ship

Inspect both source meshes and meshes evaluated after modifiers. [P01, P09, P10]

| Measure | Interpretation |
| --- | --- |
| Source vertices/faces | Editing complexity before evaluated modifiers |
| Evaluated triangles | Triangle count for the evaluated mesh components in the measured context; reconcile with exporter settings, instances and final export |
| Exported vertex records | Complete attribute entries after discontinuities/splitting |
| Mesh primitives/surfaces | Material and geometry submission partitions |
| Unique texture resources | Resolution, format, color space, and memory dependencies |
| Visible instances | Scene-level repetition, shadows, animation, and submission pressure |

- Remember that one geometric position may need several normal, UV, color, or
  skinning attribute entries.
- Expect hard normals and UV seams to increase exported vertex records; do not
  weld away intentional shading boundaries.
- Use a cube only as an explanatory example: 8 positions, 24 face-normal
  records, and 12 triangles are a possible indexed representation.
- Do not promise that every exporter produces that representation; unindexed or
  differently split data can differ.
- Inspect shared accessor/buffer references before summing glTF accessor counts;
  avoid counting shared storage repeatedly.
- Count material partitions separately from unique stored vertices; a material
  boundary does not always duplicate the buffer.
- Report primitive counts as structural evidence, not an exact whole-frame
  draw-call count.
- Measure actual calls/frame time in the engine when performance is part of
  acceptance.

## Choose the color and material strategy

Choose by required edits, visual detail, and engine support. Keep color roles
consistent across an asset family. [P01, P11]

| Strategy | Choose when | Check before delivery |
| --- | --- | --- |
| A few shared materials | A prototype or genuinely different surface behavior needs separate slots | Duplicate materials, primitive count, transparency partitions |
| Shared palette texture + UV | Large color regions, coherent asset families, or recoloring dominate | Stable color-role mapping, filtering, mip behavior, export UVs |
| Vertex/corner colors | Geometry carries the needed color detail without image textures | Exported color attributes, interpolation, color space, shader use |
| Unique UV + painted/baked textures | Labels, localized wear, hand-painted detail, or baking justify it | Distortion, seams, density, padding, image dependencies |

- Prefer changing a shared palette/material over duplicating near-identical
  materials per object.
- Do not add a material slot for every face-color variation without assessing
  its partition cost.
- Keep genuinely different roughness, metalness, masking, or shader behavior
  separate when needed.
- Do not assume that one shared material automatically produces one draw call
  for the whole scene.
- Reuse mesh resources for repeated identical parts where the engine's workflow
  supports it.

## Palette UVs

- Define named roles such as body, secondary, accent, dark trim, and metal; do
  not hardcode a universal color count.
- Place the selected faces' UV coordinates inside the intended swatch, away from
  neighboring colors.
- Permit deliberate UV overlap for shared swatches; classify overlap by purpose
  before treating it as a defect.
- Use a separate suitable UV set when a lightmap or unique bake requires
  distinct surface coverage.
- Test close, distant, and oblique views with the actual engine filtering and
  texture-import settings.
- Inspect the smallest mip levels used in play; swatches can mix during
  reduction even when their base image is correct.
- Use larger swatches, appropriate gutters, or an explicitly implemented
  palette-index shader when needed.
- Choose nearest/linear filtering and mip policy from the observed result; do
  not universally disable mipmaps.
- Verify recoloring in the engine using at least one visibly different palette.
- Treat palette shaders as engine implementations; a Blender node graph does not
  establish their portability.

## Vertex and corner colors

- Choose the attribute domain intentionally: interpolate shared vertex colors
  for gradients or preserve per-corner color boundaries.
- Inspect the result at boundaries and on triangulated faces; interpolation can
  create unintended intermediate colors.
- Confirm the exporter includes the intended color attribute and the engine
  material actually consumes it.
- For glTF, inspect `COLOR_0` and remember that it multiplies the base color.
  [P10]
- Use a neutral base-color factor when the vertex color should supply the
  unmodified color.
- Check color-space conversions before compensating with brighter values.
- Record whether changing a color requires editing geometry data or can happen
  through runtime parameters.

## Conventional UVs and baking

- Select projection/unwrap methods from the shape: simple projection, seam-based
  unwrap, or constrained quad strips.
- Use a checker texture where stretching matters; evaluate a palette mapping by
  color assignment instead.
- Preserve orientation and readable scale on labels and other directional
  artwork.
- Establish texel density by viewing importance; avoid spending equal texture
  area on invisible and focal surfaces.
- Set margins using the actual unwrap/packing method and intended texture
  resolution. [P13]
- In Blender Fraction mode, `1/1024` means one pixel around an island for a
  1024-square texture; inspect other modes separately.
- Do not copy a universal `0.008` or `0.01` margin from an older tutorial.
- Allow sufficient edge dilation and island separation for the lowest relevant
  mip and expected viewing angle.
- Keep overlapping artistic UVs separate from non-overlapping bake/lightmap
  requirements.
- Verify baked results after the final relevant triangulation, UV, normal, and
  tangent changes.

## Keep shaders portable

- Use exporter-recognized material arrangements for interchange; arbitrary
  Blender shaders do not serialize as executable engine shaders. [P01]
- Use a verified Principled/PBR path for portable shaded surfaces; use unlit
  only when the art direction calls for lighting-independent color.
- Bake procedural detail or reproduce it in an engine shader; identify which
  system owns the final appearance.
- Inspect the exported material rather than inferring success from a correct
  Blender render.
- Use sRGB for base-color image content and linear/Non-Color for data maps such
  as roughness, metalness, and normals. [P10]
- For glTF normal maps, verify tangent-space orientation and +Y convention;
  confirm the actual map rather than guessing from its filename.
- Generate/export tangents when the material requires them; omit them only after
  confirming no dependent feature is used. [P07]
- For packed glTF metallic/roughness textures, inspect roughness in G and
  metallic in B.
- Apply backface culling intentionally for closed surfaces; keep double-sided
  rendering only where the visible back face is required.
- Isolate small blended regions when appropriate so they do not move an entire
  asset into a more expensive transparency path.
- Compare under representative engine lighting and exposure; do not fix an
  import error by changing unrelated light intensity.

## Prepare geometry and transforms

- Verify intended dimensions numerically before export; use a known-size
  reference in the target scene.
- Use metres for glTF distances and verify the exporter/engine conversion once.
  [P10]
- Set pivots by purpose: placement contact, hinge, wheel axle, attachment, or
  modular snapping point.
- Keep an assembly's meaningful hierarchy and offsets; do not centre every child
  independently.
- Inspect non-uniform and negative scale, parent transforms, constraints,
  armatures, and animation dependencies.
- Apply only transforms that the asset pipeline requires and that preserve
  intended behavior.
- Do not run Apply All Transforms blindly on an existing rig or articulated
  assembly.
- Lock critical triangulation on an export copy or through evaluated modifiers;
  retain the editable authoring mesh. [P02, P14]
- Inspect nonplanar quads, concave n-gons, silhouettes, and deforming regions
  after triangulation.
- Choose diagonals deliberately when a face's shading or deformation depends on
  them.
- Query the installed modifier properties; do not assume an older `Keep Normals`
  option still exists.
- Export a rig's verified rest/default pose as required by the pipeline, then
  inspect animation separately.

## Export and reimport acceptance loop

1. Save the editable source and identify the exact export collection/objects.
2. Confirm modifier evaluation, geometry-instance realization/export, and
   hierarchy options against the asset's needs.
3. Exclude test cameras, lights, staging planes, and helpers unless the delivery
   contract includes them.
4. Export normals, UVs, colors, tangents, skinning, and morphs only as required;
   record the chosen switches.
5. Package or reference every required image; check all external paths from the
   consumer's location.
6. Import into a fresh test scene in the target engine, using the intended
   renderer.
7. Check bounds, scale, forward, pivot, hierarchy, names, missing parts,
   material slots, and texture links.
8. Inspect front/back faces, intentional openings, hard/smooth boundaries, color
   regions, and normal-map direction.
9. Exercise articulation, animation extremes, attachments, and collisions where
   applicable.
10. Compare near/far and oblique views at gameplay resolution; inspect both
    shaded and wireframe views.
11. For a new or changed import pipeline, use a disposable test copy to check
    that re-export/reimport preserves material overrides and references; omit
    this extra mutation for a routine asset on an already verified pipeline.
12. Save the verified export and report checks performed, remaining limitations,
    and untested engine behavior.

Do not claim engine compatibility from Blender-only screenshots. If the engine
is unavailable, deliver the export and mark engine validation unperformed.

## Optional Godot workflow

Apply this section only when Godot is the target. Verify its installed version
and renderer before following inspector-specific recipes.

- Choose explicit `.glb`/ `.gltf` for consumers that should not require Blender;
  choose `.blend` when installed-Blender conversion fits local/team/CI
  iteration. [P03]
- Remember that `.blend` import invokes Blender's glTF exporter; it does not
  bypass interchange limitations.
- Keep the original `.blend` as the editable source even when only a `.glb`
  enters the runtime asset folder.
- Distinguish Godot camera forward `-Z` from oriented model front `+Z`; Blender
  model front convention is `-Y`. [P02]
- Let the verified coordinate conversion handle axis changes; avoid compensating
  rotations in three different stages.
- Put engine-specific behavior in wrapper/inherited scenes, import scripts, or
  external resources as appropriate. [P07]
- Extract/reuse external materials when customizing shaders or filtering; verify
  them in an instantiated scene. [P08]
- Keep source material names stable; renaming can break external-material
  associations.
- Use a separate suitable UV2 when baked lightmaps require it; do not reuse
  overlapping palette UVs automatically.
- Generate simple collision by gameplay purpose: primitive/convex shapes for
  suitable moving bodies and trimesh for appropriate static geometry.
- Check collision position and scale after import; visual topology does not
  prescribe collision density.
- Inspect automatic LOD on and off at the closest and farthest supported
  gameplay views. [P06]
- Disable or override LOD per mesh if it damages characteristic facets,
  openings, or deformation; use authored alternatives where justified.
- Check engine settings rather than assuming import defaults or property names
  from `latest` documentation.

## Diagnose the actual cost

- Profile a representative scene with expected visible counts, lighting,
  shadows, and animation. [P04, P05]
- Compare frame time, not just an uncapped FPS number or triangle total.
- Investigate submission/material changes, vertex processing, fragment work,
  transparency, shadows, and animation separately.
- Reduce unnecessary material/texture changes before destroying a silhouette
  that already meets its geometry budget.
- Keep static mesh combination spatially sensible; merging everything can
  prevent useful individual culling.
- Group repeated instances according to visibility and locality; a huge
  MultiMesh group can share unfavorable bounds/LOD behavior.
- Recheck color and silhouette after every meaningful LOD or atlas optimization.

## Handoff record

Record actual Blender/exporter and engine versions; intended camera/scale/pivot
conventions; file paths and dependencies; evaluated
triangle/vertex-record/material/texture counts; deliberate UV overlap or open
surfaces; export settings; collision/LOD/animation status; target-engine
screenshots or measurements; reimport result; and unperformed checks.

Treat the retrieved documentation's version labels as source metadata, not proof
of the latest stable release. Use P12 only for general troubleshooting context:
its older Hubs-specific modifier, animation, and unlit recipes are not current
universal instructions. Do not report a model-capability improvement percentage
without an independent controlled evaluation.
