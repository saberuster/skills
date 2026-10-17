# Evidence and version ledger

Research date: **2026-10-16**, Asia/Shanghai. The main search/fetch route was
**Exa**. This is a dated evidence snapshot; revisit version-sensitive
documentation for a new Blender release.

Four workstreams issued **22 searches requesting 170 result slots**. The curated
ledger contains **51 unique URLs on 26 hosts**: 48 substantive text sources
(including partial/section-focused reads), two overview-only pages, and one
metadata-only page excluded from technical evidence. These are not 170
independently read sources. Translated official pages are separate URLs, not
independent confirmation.

English and Chinese queries were used. Read materials also include one Japanese
tutorial. Video titles, thumbnails and linked downloads were not treated as
watched/read content. Official API/manual/specification pages govern technical
behavior; original practitioner tutorials inform construction choices.
Unsupported universal budgets and outdated UI instructions were excluded.

**Version evidence:** PY08/PY09 listed Blender 5.2.2 LTS, and the local
executable reported 5.2.2 LTS (build 2026-09-15, d13f752e3b9c). A documentation
title alone does not prove release status. Godot guidance is optional and
version-probed; no latest Godot release claim is made here.

**Attribution:** The skill is an original procedural synthesis, not a
reproduction of source tutorials. "Heuristic" and "original synthesis" label
decisions developed for the agent workflow. Quality gates and numeric examples
are not validated performance benchmarks. No closed/paywalled course was claimed
as read.

Original external titles are retained verbatim when rendered, including Chinese
and Japanese titles, to preserve source identity. Numeric HTML character
references keep this Markdown file ASCII; JSON Unicode escapes preserve the
exact title values in `sources.json`. All authored summaries and caveats are in
English.

For machine-readable provenance and source-specific limitations, inspect
`sources.json`.

## Shape, topology and shading

### SH01

[Bevel Modifier &#8212; Blender Manual][link-1]

- Access: en; fetched_full_relevant_page.
- Use: Bevel is a nondestructive alternative to the edit-mode operation;
  segments add edge loops. Angle, weight, and vertex-group limits allow
  selective bevel placement instead of beveling every edge.
- Limit: Fetched latest page identifies itself as Blender 5.2 LTS; a search
  result for the same URL said 5.1. Verify installed Blender and its versioned
  manual. Attribute names and custom normal behavior are version-sensitive.

### SH02

[Smooth By Angle Modifier &#8212; Blender Manual][link-2]

- Access: en; fetched_full_relevant_page.
- Use: This bundled Geometry Nodes asset sets edge sharpness from neighboring
  face angles. The Angle input controls what counts as smooth; Ignore Sharpness
  can override manually marked sharp edges.
- Limit: Page identifies as 5.2 LTS. Do not assume old Auto Smooth mesh-property
  APIs or UI locations. Check available operator/asset in the actual version.

### SH03

[Decimate Modifier &#8212; Blender Manual][link-3]

- Access: en; fetched_full_relevant_page.
- Use: An already economical mesh usually does not benefit from Decimate; dense
  sculpted or subdivided meshes can. Collapse progressively merges vertices;
  ratio is calculated using triangle counts.
- Limit: Page identifies as 5.2 LTS. Its Angle Limit wording appears
  counterintuitive; do not repeat the higher/lower inequality without runtime
  verification. Preserve boundaries and inspect the result.

### SH04

[Clean Up &#8212; Blender Manual][link-4]

- Access: en; fetched_full_relevant_page.
- Use: Delete Loose removes disconnected loose geometry. Degenerate Dissolve
  collapses short connected edges. Merge by Distance merges nearby selected
  vertices, with a threshold that can also destroy intentional gaps.
- Limit: Page identifies as 5.2 LTS. Names/options should be checked in
  installed version; thresholds must be relative to asset dimensions.

### SH05

[Mesh Structure &#8212; Blender Manual][link-5]

- Access: en; fetched_full_relevant_page.
- Use: Triangles are planar; quads are useful for deformation and subdivision.
  Flat and smooth shading change how normals are interpreted, without adding
  silhouette geometry.
- Limit: Page identifies as 5.2 LTS. Custom/free-normal storage and importer
  claims are version-specific and are not promoted to universal skill rules.

### SH06

[Remeshing &#8212; Blender Manual][link-6]

- Access: en; fetched_full_relevant_page.
- Use: Voxel remeshing is useful for sculpt preparation, messy intersections,
  and approximate stand-ins. Automatic remeshing is not a reliable source of
  final deformation topology.
- Limit: Page identifies as 5.2 LTS. Preserve-attribute and quad-remesh options
  may differ by release; validate actual functionality.

### SH07

[&#25380;&#20986;&#38754; &#8212; Blender &#25163;&#20876;][link-7]

- Access: zh-Hans/en; fetched_full_relevant_page.
- Use: Extrusion creates border faces and then transforms the selected region.
  Canceling the movement does not remove newly created extrusion geometry, so an
  aborted transform can leave duplicates.
- Limit: Fetched Chinese latest page identifies as 5.2 LTS and includes
  untranslated English. Search discovered a dev page; fetched latest instead.
  UI/operator options are version-sensitive.

### SH08

[Mirror Modifier &#8212; Blender Manual][link-8]

- Access: en; fetched_full_relevant_page.
- Use: Mirror uses local axes through the object origin, or the transform of an
  explicit mirror object. Clipping constrains seam vertices; Merge joins
  corresponding vertices within the merge threshold.
- Limit: Page identifies as 5.2 LTS. Use verified mirror origin/axes and safe
  scale-aware thresholds; don't confuse adding a modifier with applying it
  destructively.

### SH09

[Low-Poly 3D Assets in Blender Tutorial &#8212; Zenva/GameDev Academy][link-9]

- Access: en; fetched_partial_18000_characters_relevant_written_lessons_read.
- Use: Primitive parameters control segment density at creation time.
  Orthographic views, numeric transforms, and snapping support proportion and
  alignment checks.
- Limit: Originally 2019; page updated 2024. Old UI, mixed transcript versions,
  and deliberately customized keyboard shortcuts are not current defaults. No
  claim of viewing embedded videos.

### SH10

[Creating a game sprite: Box Modelling the basic outline &#8212;
Mike/GameFromScratch][link-10]

- Access: en; fetched_full_relevant_page.
- Use: A mirrored primitive can be shaped with extrusion, loop insertion, and
  vertex adjustments against top and side references. Adding detail later is
  easier than removing poorly planned complexity.
- Limit: 2013 tutorial. Retain modeling reasoning, not obsolete shortcuts,
  interface positions, or exact commands; its wording sometimes conflates adding
  and applying a modifier.

### SH11

[Beginner's Overview of 3D Game Asset Creation &#8212; Chunck Trafagander/CG
Cookie][link-11]

- Access: en; fetched_full_relevant_page.
- Use: Use references or a sketch so geometry is not built solely from an
  untested mental image. When reducing a high-poly source, prioritize
  silhouette-affecting detail; excessive reduction can cause bake artifacts.
- Limit: 2024 article; software/product recommendations were not adopted.
  Post-bake geometry changes are not generalized as safe because
  triangulation/tangent/bake consistency must be checked.

### SH12

[&#12525;&#12540;&#12509;&#12522;&#12391;&#32032;&#20307;&#12434;&#20316;&#12429;&#12358;&#65281;&#20316;&#12427;&#12392;&#12365;&#12398;&#12467;&#12484;&#12392;&#12399;&#65311;
&#8212; CGbox][link-12]

- Access: ja; fetched_full_relevant_page.
- Use: Runtime economy and intentionally faceted visual style are distinct
  meanings of low poly. Each vertex has strong silhouette impact; keep a distant
  overall view during modeling.
- Limit: Blender 2.9 tutorial, originally 2021 and updated 2023. Arbitrary
  ring-count rules and the broad claim that all game meshes are low-poly were
  rejected; no claim of viewing video.

## Asset construction

### A01

[Creating a Low Poly Medieval House in Blender: Part 1][link-13]

- Access: en; substantial text read: house, roof, balcony, timber sections;
  extraction capped at 18,000 chars.
- Use: Begin from a box, extrude storeys, merge paired top vertices into a roof
  ridge, then form eaves and roof thickness. Repeat timber pieces by duplication
  and rotation; locate the origin at the building base.
- Limit: 2015 tutorial uses Blender 2.7-era right-click selection, Background
  Images and old shortcuts. Reuse geometric intent only; do not copy UI
  sequences. Hidden-face removal is conditional, not suitable for every export
  or use.

### A02

[Create a Low Poly Camaro in Blender: Part 1][link-14]

- Access: en; full extracted modeling text read.
- Use: Build the side profile first with loops at wheel-arch boundaries, wheel
  centers, door boundaries and upper arch height; remove wheel-center vertices
  and shape the arches. Extrude toward the center, remove center faces and
  mirror with clipping; repeatedly reconcile side, front and top views.
- Limit: 2014 Blender 2.7-era UI and shortcuts; the tutorial's 14-sided wheels
  are an example, not a universal budget. Some prose has shortcut inaccuracies.

### A03

[How I made my Shelby GT350R model using Blender][link-15]

- Access: en; full extracted text read.
- Use: Use a cube at real vehicle dimensions to scale and align orthographic
  blueprints. Supplement blueprints with photographs of the same vehicle variant
  because blueprints alone do not establish all forms.
- Limit: 2016 reflective project diary. Its later subdivision/PBR and Unity 5
  stages are not a prescription for a faceted low-poly asset.

### A04

[Making Metal Structures][link-16]

- Access: en; full extracted text read.
- Use: Form an L-shaped angle-iron section from a narrow plane and an extruded
  edge; add thickness with Solidify. Assemble repeatable structural units from
  these bars, then duplicate the units to form larger frames.
- Limit: 2024 tutorial aimed at metal realism. Only model the L cross-section
  and wall thickness when the expected view resolves them; a rectangular prism
  may suffice for distant stylized beams.

### A05

[Behind the Scenes: Dark Fantasy Kit &#8211; Part II][link-17]

- Access: en; full extracted article text read.
- Use: Prototype an entire modular family in rough shapes and flat material
  colors, and test scale and modular assembly in the engine before detailing.
  Use box modeling for primary forms and beveled curves for curved forms; reuse
  Mirror and Array where repetition is deliberate.
- Limit: 2018 high/low PBR workflow. Old Auto Smooth, material packing and
  engine references need current validation. Microdetail baking is optional for
  graphic low-poly styles.

### A06

[Procedural low poly trees][link-18]

- Access: en; full extracted text read.
- Use: Generate a branching edge skeleton by turning new branches relative to
  the parent direction and shrinking lengths by recursion depth. Vary branch
  direction and whether branching occurs; use per-vertex radii with Skin to give
  the skeleton thickness.
- Limit: 2022 conceptual implementation. Randomization should be seeded and
  bounded for repeatable art direction; that restriction is synthesis, not a
  documented author setting.

### A07

[Complete 3D Game Character Creation Guide (From Blender to Godot)][link-19]

- Access: en; read reference setup/head sections and targeted knees, shoulders,
  elbows/hands sections; did not claim whole 105k-character article reviewed;
  also hair construction, bangs, main hair, and clothing/shirt sections.
- Use: Align front/side references to shared body landmarks and real scale;
  inspect perspective as well as orthographic views. For an expressive face,
  establish mouth and eye loops first, add their side-view depth, then connect
  the surrounding head.
- Limit: Written for Blender 4.0+/Godot 4.2+. Subdivision, anime facial detail,
  addons and toon shading are optional and may conflict with a compact faceted
  style. Avoid treating its style or vertex counts as universal.

### A08

[Blender&#8212;lowpoly&#39118;&#26684;&#21270;&#26696;&#20363;&#20043;&#36827;&#38454;&#31687;&#8212;&#26519;&#20013;&#32440;&#40548;&#8212;&#31532;&#19977;&#33410;&#35838;&#65306;&#26641;&#26408;&#12289;&#30707;&#22836;&#27169;&#22411;&#21046;&#20316;&#22270;&#25991;&#25945;&#31243;][link-20]

- Access: zh-CN; full written lesson read; embedded video not watched.
- Use: Conifers can combine a low-sided trunk with layered conical crowns,
  varying each layer in size and outline. Broadleaf trees can combine several
  chunky crown masses of different sizes.
- Limit: The tutorial explicitly uses Blender 3.2.1; verify add-on availability
  separately. It describes M as grouping, so confirm the actual command in the
  installed version. Only page text was read, not the paid video.

### A09

[Optimizing topology for a game Character][link-21]

- Access: en; read theory, method, results and partial discussion from first
  18,000 extracted chars; figures not visually inspected.
- Use: The author's controlled comparison found inside knee/elbow collapse with
  one edge arrangement and better retained form with a different arrangement.
  Test topology by posing it; a clean rest-pose mesh is insufficient evidence of
  deformation quality.
- Limit: 2018 small case study, not a universal anatomical theorem. Do not
  attribute all deformation errors to topology: joint position, weights and
  twist bones also matter.

### A10

[Animated Low Poly Characters][link-22]

- Access: en; read introduction, visual style, polycount, topology and initial
  rig section from 18,000 extracted chars; figures not visually inspected.
- Use: Cylinder circumference constrains connected body topology; determine limb
  cross-sections deliberately. Extra joint geometry can preserve form with a
  modest triangle cost, while bone pivot placement changes the same mesh's
  deformation.
- Limit: 2014 hardware, texture and bone budgets are obsolete and excluded.
  Strong claims against subdivision are style-specific, not general modeling
  rules.

### A11

[Skin Modifier &#8212; Blender 5.2 LTS Manual][link-23]

- Access: en; full extracted text read.
- Use: Skin produces a surface from an edge/vertex skeleton and per-vertex
  radii; original faces are ignored. Branch intersections can overlap; Branch
  Smoothing relaxes them while also shrinking the result.
- Limit: Live /latest page identified itself as Blender 5.2 LTS when fetched on
  2026-10-16 Asia/Shanghai. Must validate installed Blender version. This is a
  manual label, not independent release-status evidence.

### A12

[Proportional Editing &#8212; Blender 5.2 LTS Manual][link-24]

- Access: en; full extracted text read.
- Use: Proportional Editing transforms nearby unselected elements with
  adjustable radius and falloff. Connected Only follows mesh connectivity,
  preventing nearby disconnected fingers or pieces from moving together.
- Limit: Live /latest page identified itself as Blender 5.2 LTS when fetched on
  2026-10-16 Asia/Shanghai. Prefer installed-version documentation before
  scripting.

### A13

[How to model a low-poly dog in Blender 3.0 on iPad][link-25]

- Access: en; full extracted tutorial text read.
- Use: Shape the abdomen from a half-cube with Mirror, extend neck/head/haunches
  in side view, then adjust widths from another view. Extrude legs from belly
  faces and add loops where contour or joints demand changes; correct their
  stance from the front.
- Limit: Blender 3.0 and Astropad-specific UI. Several axis/left-right
  descriptions are inconsistent; preserve geometric construction rather than
  literal controls. A tiny intentional ear recess should not become an
  accidental open boundary.

### A14

[Low-Poly Forest Environment &#8211; Free Blender Tutorial & File][link-26]

- Access: en; overview text read; linked blend/video not inspected.
- Use: The page describes a scene blockout using a displaced ground plane,
  cylinder trunks, cone/sphere canopies and scaled icosahedron rocks.
- Limit: Excluded from core rules: generic counts, mandatory
  apply-all-modifiers, aggressive UV minimization and small-detail advice lack
  sufficient context. Do not claim its video or file was studied.

### A15

[Build-a-bird Tutorial][link-27]

- Access: en; brief written outline read; videos not watched.
- Use: The outline starts with cube extrusion blockout and later includes
  mirroring, rigging and weight-paint troubleshooting.
- Limit: Not sufficient evidence for detailed topology steps; excluded from core
  recipes.

### A16

[Building a Stylized Low-poly Modular Diorama for the first time][link-28]

- Access: en; metadata only; body not returned.
- Use: Metadata only; excluded from technical evidence.
- Limit: Not used as evidence.

## Game asset delivery

### P01

[Blender Manual &#8212; glTF 2.0][link-29]

- Access: en; fetched; mesh/material/export sections read.
- Use: glTF export triangulates quads and n-gons. UV and normal discontinuities
  can increase exported vertex count. The exporter recognizes selected Blender
  material-node arrangements; it does not serialize arbitrary shader graphs.
- Limit: Page identifies itself as 5.2 LTS; this does not establish release
  status. Pin documentation to installed Blender.; Alpha-mode detection, node
  sockets, exporter options, extensions and material-color handling are
  version-sensitive.

### P02

[Godot &#8212; Model export considerations][link-30]

- Access: en; fetched and read.
- Use: Godot cameras look toward -Z; oriented models conventionally face +Z.
  Blender model front maps from -Y. Control triangulation in the authoring tool
  before export. Validate transforms and rest pose.
- Limit: Fetched stable page identifies Godot 4.7. Verify against project's
  installed version and conventions.; Do not blindly apply all transforms to an
  existing rig.

### P03

[Godot &#8212; Available 3D formats][link-31]

- Access: en; fetched and read.
- Use: Godot recommends glTF; .blend import invokes installed Blender's glTF
  exporter. Explicit glTF export removes the Blender installation dependency
  from consumers; .blend supports rapid local iteration.
- Limit: Options and requirements are current-page claims, not assumptions for
  every installed release.; Do not repeat old claims that all FBX import
  requires external FBX2glTF; newer import paths use ufbx.

### P04

[Godot &#8212; Optimizing 3D performance][link-32]

- Access: en; fetched and read.
- Use: Costs include culling, transparency, lighting, skinning and draw
  submission, not just triangles. Repeated meshes/materials can benefit from
  instancing. Spatial grouping still matters for culling.
- Limit: latest explicitly warns it is unstable. Forward+-specific automatic
  instancing is renderer-sensitive.

### P05

[Godot &#8212; GPU optimization][link-33]

- Access: en; fetched and read.
- Use: Reuse materials and shaders; atlas use can reduce texture/state changes.
  Combining meshes trades fewer submissions against worse per-object culling.
- Limit: latest is unstable. Some broad mobile statements are dated; avoid
  carrying them into a general rule.; No universal triangle or draw-call budget
  follows from this page.

### P06

[Godot &#8212; Mesh level of detail (LOD)][link-34]

- Access: en; fetched and read.
- Use: Imported scene meshes can receive automatic LOD using meshoptimizer;
  selection is screen-space dependent. Compare LOD on/off in wireframe and
  frame-time views; disable problematic meshes or author manual alternatives.
- Limit: latest is unstable. Default import settings, property names and
  thresholds must be verified in the target version.; Low-poly faceted assets
  may need artistic silhouette checks beyond an automatic geometric metric.

### P07

[Godot &#8212; Import configuration][link-35]

- Access: en; fetched and read.
- Use: Tangents are needed for tangent-space normal/height features; unnecessary
  attributes can be omitted after confirming material needs. UV2 lightmap
  generation is a distinct import setting from surface-color UVs.
- Limit: Fetched stable page identifies 4.7; Blender-specific importer options
  are version-sensitive.; Do not prescribe all import switches globally; branch
  by actual asset features.

### P08

[Godot &#8212; Advanced Import Settings][link-36]

- Access: en; fetched and read.
- Use: Use primitive or appropriate convex collision for moving bodies;
  triangle-mesh collision is for static bodies. Extracted external materials
  survive reimport; renaming source materials can break those associations.
- Limit: latest is unstable. Verify exact inspector controls and supported
  physics shapes in the selected engine backend/version.

### P09

[Khronos glTF Tutorial &#8212; Meshes][link-37]

- Access: en; fetched and read.
- Use: Each mesh primitive connects vertex attributes, optional indices and a
  material. An index identifies the complete aligned attribute entry, rather
  than only a geometric position.
- Limit: This explains glTF 2.0 structure; it is not a guarantee about any
  engine's batching implementation.

### P10

[Khronos glTF 2.0 Specification][link-38]

- Access: en; fetched twice; coordinate, mesh and material sections read.
- Use: glTF uses meters and a right-handed Y-up system with asset front +Z.
  Primitives correspond to GPU draw data; splitting allows material assignments,
  but final render-pass draw count is engine-dependent.
- Limit: Retrieved document header identifies specification 2.0.1 dated
  2021-10-11. It is authoritative for this snapshot; do not label it the latest
  revision.; Extensions and renderer behavior require separate verification.

### P11

[&#12298;&#19968;&#21400;&#31859;&#26102;&#20809;&#12299;&#24320;&#21457;&#26085;&#24535;(2)
&#8212; &#35843;&#33394;&#26495;][link-39]

- Access: zh-CN; fetched and read.
- Use: The developer maps model UV regions into a small palette and changes
  palette colors in Godot. Palette coordinates can encode semantic color roles
  for engine-side recoloring.
- Limit: Published 2025-06-18. Author explicitly distinguishes their rounded
  flat-color style from faceted low-poly.; The author's
  one-material-one-drawcall shorthand is not adopted as an exact invariant.

### P12

[Hubs &#8212; Using the Blender glTF Exporter][link-40]

- Access: en; fetched and read; version-sensitive recipes excluded.
- Use: Export troubleshooting should check scale, placement, selected export
  scope and target-platform material support.
- Limit: Multiple animation/modifier/unlit recipes describe older exporter
  behavior. Use only generic diagnostic principles; prefer current Blender
  manual for implementation.; Hubs-specific Draco and unlit recommendations are
  not Godot rules.

### P13

[Blender Manual &#8212; UV Operators][link-41]

- Access: en; fetched and read.
- Use: Choose projection/unwrap methods by shape; Smart UV's lower angle limit
  generates more islands. Margin meaning depends on method. Fraction mode
  relates directly to UV bounds; 1/1024 gives one pixel around an island at 1024
  square resolution.
- Limit: Fetched page identifies 5.2 LTS. Unwrap methods and labels vary by
  Blender release.; Do not prescribe a universal 0.008 or 0.01 margin without
  texture/mipmap requirements.

### P14

[Blender Manual &#8212; Triangulate Modifier][link-42]

- Access: en; fetched and read.
- Use: Triangulate offers controlled quad diagonals and n-gon tessellation. An
  export-copy modifier can lock the diagonal used by the engine while retaining
  an editable authoring mesh.
- Limit: Fetched page identifies 5.2 LTS. The page no longer lists the old Keep
  Normals option; inspect installed RNA/UI rather than assuming old recipes.

## Automation and versions

### PY01

[Mesh API][link-43]

- Access: en; fetched relevant text; extraction capped at 6,500-7,500 characters
  per page.
- Use: Mesh storage, loops, corner normals and geometry access; validate newly
  generated input rather than assuming from_pydata rejects invalid faces.
- Limit: Dated snapshot; match the installed Blender version. current/latest and
  release pages can change.

### PY02

[Modes and Mesh Access][link-44]

- Access: en; fetched relevant text; extraction capped at 6,500-7,500 characters
  per page.
- Use: Object Mode data can be stale during Edit Mode; choose the appropriate
  Mesh or BMesh route.
- Limit: Dated snapshot; match the installed Blender version. current/latest and
  release pages can change.

### PY03

[Dependency graph API][link-45]

- Access: en; fetched relevant text; extraction capped at 6,500-7,500 characters
  per page.
- Use: Evaluated objects include modifier results; temporary to_mesh data must
  be released and cannot become persistent scene data.
- Limit: Dated snapshot; match the installed Blender version. current/latest and
  release pages can change.

### PY04

[BMesh Module][link-46]

- Access: en; fetched relevant text; extraction capped at 6,500-7,500 characters
  per page.
- Use: Distinguish owned BMesh from borrowed Edit Mode BMesh; flush changes and
  free only owned data.
- Limit: Dated snapshot; match the installed Blender version. current/latest and
  release pages can change.

### PY05

[Using Operators][link-47]

- Access: en; fetched relevant text; extraction capped at 6,500-7,500 characters
  per page.
- Use: Operator poll failures depend on context; direct data operations can be
  more suitable for batch tasks.
- Limit: Dated snapshot; match the installed Blender version. current/latest and
  release pages can change.

### PY06

[Context API][link-48]

- Access: en; fetched relevant text; extraction capped at 6,500-7,500 characters
  per page.
- Use: Temporary overrides require consistent window/area/region relationships;
  dependency-graph updates invalidate evaluated references.
- Limit: Dated snapshot; match the installed Blender version. current/latest and
  release pages can change.

### PY07

[Blender 4.1 Python API release notes][link-49]

- Access: en; fetched relevant text; extraction capped at 6,500-7,500 characters
  per page.
- Use: The 4.1 release removed legacy auto-smooth and split-normal calculation
  properties; modern code must use the supported sharp/smooth and corner-normal
  system.
- Limit: Dated snapshot; match the installed Blender version. current/latest and
  release pages can change.

### PY08

[Blender Download][link-50]

- Access: en; fetched relevant text; extraction capped at 6,500-7,500 characters
  per page.
- Use: Retrieved 2026-10-16: stable download listed Blender 5.2.2 LTS, released
  2026-09-15; 5.3 was upcoming.
- Limit: Dated snapshot; match the installed Blender version. current/latest and
  release pages can change.

### PY09

[Blender 5.2 LTS releases][link-51]

- Access: en; fetched relevant text; extraction capped at 6,500-7,500 characters
  per page.
- Use: Retrieved 2026-10-16: 5.2 LTS initial release July 14, 2026; current
  listed patch 5.2.2 on September 15, 2026.
- Limit: Dated snapshot; match the installed Blender version. current/latest and
  release pages can change.

[link-1]: https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/bevel.html
[link-2]: https://docs.blender.org/manual/en/latest/modeling/modifiers/normals/smooth_by_angle.html
[link-3]: https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/decimate.html
[link-4]: https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/cleanup.html
[link-5]: https://docs.blender.org/manual/en/latest/modeling/meshes/structure.html
[link-6]: https://docs.blender.org/manual/en/latest/modeling/meshes/retopology.html
[link-7]: https://docs.blender.org/manual/zh-hans/latest/modeling/meshes/editing/face/extrude_faces.html
[link-8]: https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/mirror.html
[link-9]: https://gamedevacademy.org/blender-tutorial/
[link-10]: https://gamefromscratch.com/creating-a-game-sprite-modelling-in-blender-part-2-box-modelling-the-basic-outline/
[link-11]: https://cgcookie.com/posts/beginner-s-overview-of-3d-game-asset-creation
[link-12]: https://cgbox.jp/2021/11/04/blender-lowpoly-modeling/
[link-13]: https://cgi.tutsplus.com/creating-a-low-poly-medieval-house-in-blender-part-1--cms-24002t
[link-14]: https://design.tutsplus.com/tutorials/create-a-low-poly-camaro-in-blender-part-1--cms-21730
[link-15]: https://www.lmhpoly.com/blog/how-i-made-my-shelby-gt350r-model-using-blender
[link-16]: https://blend.beehiiv.com/p/metal-structures
[link-17]: https://runemarkstudio.com/3d/diary_2_dark_fantasy_pack/
[link-18]: https://lflo.dev/projects/low-poly-tree-blender.html
[link-19]: https://codernunk.com/tutorials/complete-3d-character-guide/
[link-20]: https://huke88.com/baike/a58857/
[link-21]: https://www.diva-portal.org/smash/get/diva2:1218697/FULLTEXT01.pdf
[link-22]: https://www.theseus.fi/server/api/core/bitstreams/188f6621-ac9a-43b7-b8b5-cb067c00c972/content
[link-23]: https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/skin.html
[link-24]: https://docs.blender.org/manual/en/latest/editors/3dview/controls/proportional_editing.html
[link-25]: https://astropad.com/blog/how-to-model-a-low-poly-dog-in-blender-3-0/
[link-26]: https://dunkingdoggames.com/low-poly-forest-environment-in-blender/
[link-27]: https://www.autonomoussoup.com/single-post/build-a-bird-tutorial
[link-28]: https://www.artstation.com/blogs/niklasfrogner/Bl66/building-a-stylized-low-poly-modular-diorama-for-the-first-time
[link-29]: https://docs.blender.org/manual/en/latest/addons/scene_gltf2.html
[link-30]: https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/model_export_considerations.html
[link-31]: https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html
[link-32]: https://docs.godotengine.org/en/latest/tutorials/performance/optimizing_3d_performance.html
[link-33]: https://docs.godotengine.org/en/latest/tutorials/performance/gpu_optimization.html
[link-34]: https://docs.godotengine.org/en/latest/tutorials/3d/mesh_lod.html
[link-35]: https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/import_configuration.html
[link-36]: https://docs.godotengine.org/en/latest/tutorials/assets_pipeline/importing_3d_scenes/advanced_import_settings.html
[link-37]: https://github.khronos.org/glTF-Tutorials/gltfTutorial/gltfTutorial_009_Meshes.html
[link-38]: https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html
[link-39]: https://www.gcores.com/articles/200589
[link-40]: https://docs.hubsfoundation.org/creators-using-the-blender-gltf-exporter
[link-41]: https://docs.blender.org/manual/en/latest/modeling/meshes/editing/uv.html
[link-42]: https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/triangulate.html
[link-43]: https://docs.blender.org/api/current/bpy.types.Mesh.html
[link-44]: https://docs.blender.org/api/current/info_gotchas_meshes.html
[link-45]: https://docs.blender.org/api/current/bpy.types.Depsgraph.html
[link-46]: https://docs.blender.org/api/current/bmesh.html
[link-47]: https://docs.blender.org/api/current/info_gotchas_operators.html
[link-48]: https://docs.blender.org/api/current/bpy.types.Context.html?highlight=temp_override
[link-49]: https://developer.blender.org/docs/release_notes/4.1/python_api/
[link-50]: https://www.blender.org/download/
[link-51]: https://www.blender.org/releases/5-2/
