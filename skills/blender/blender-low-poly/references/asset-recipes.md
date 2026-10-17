# Asset recipes

Use the matching recipe after the asset brief and primary silhouette are
settled. Treat all suggested segment counts, shape allocations and acceptance
checks as **heuristics**. Adapt them to the reference, camera, animation and
delivery contract; they are not universal budgets. Source IDs resolve through
[sources.md][link-1]. Old tutorial geometry remains useful; old UI commands do
not. Recipes marked **original synthesis** extend the evidence into a practical
agent workflow.

## Buildings and modular architecture

**Start:** Use a footprint box, storey heights and a separate roof mass.

- Extrude the principal storeys; shape a pitched roof with a ridge, eave
  overhang and visible thickness.
- Establish secondary wings and balconies before timber trim or roof ornament.
- Inset or extrude visible openings; use separate pieces for doors that must
  move.
- Duplicate structural beams with measured spacing; inspect their corner
  junctions. [A01]
- Prototype wall, corner, opening and floor modules together; check their
  assembly in the engine. [A05] **Decisive check:** Read the roof profile,
  entrance and floor divisions from the intended camera. **Repair:** If the
  building reads as stacked boxes, change roof/wing proportions and recess depth
  before adding surface detail. **Repair:** If modules leave gaps, correct
  dimensions, origins and connection planes before concealing seams with trim.
  **Heuristic:** Preserve one dimensional grid for assembly; permit deviations
  only in intentionally irregular decorative pieces.

## Furniture and storage

**Original synthesis**, grounded in the family-blockout method of [A05].
**Start:** Divide each object into supported mass, supports and required
negative spaces.

- Build a chair's seat, back and support positions; establish the gap beneath
  the seat before handles or stitching.
- Build a cabinet's carcass, door/drawer fronts and recesses; make its depth
  visible.
- Model one repeated leg, slat or drawer accurately, then duplicate or instance
  it.
- Separate moving fronts; locate hinges at their actual edges and slide axes
  along drawer travel.
- Add bevels only where their width remains useful at the target screen size.
  **Decisive check:** Confirm seat thickness, support spacing and opening gaps
  in a flat-material preview. **Repair:** If the object appears solid or muddy,
  enlarge meaningful gaps and simplify competing trim. **Repair:** If repeated
  pieces drift, correct the source dimensions and transforms rather than each
  copy independently. **Heuristic:** Retain hidden geometry when an opening,
  animation, shadow or future view can reveal it.

## Appliances and electronic equipment

**Original synthesis**; no source here establishes one canonical appliance
workflow. **Start:** Use a housing, functional opening and one distinctive
control/interface area.

- Match the housing proportions and major panel breaks before subdividing its
  surfaces.
- Establish door thickness, vents, screen recesses or a cooking cavity only to
  the required viewing depth.
- Represent unreadable vent repetition with a simpler surface treatment when the
  brief permits it.
- Keep buttons, knobs and handles large enough to read without competing with
  the main silhouette.
- Separate controls and doors only when movement or material separation requires
  it. **Decisive check:** Identify the appliance category from its
  housing/opening relationship without labels. **Repair:** If identification
  depends on tiny text, strengthen the characteristic opening or control layout.
  **Repair:** If vents dominate, reduce their count or contrast; do not fill
  every available surface with detail. **Heuristic:** Model a visible gap, rim
  or recess with geometry when it changes silhouette, parallax or interaction.

## Frames, tools and machinery

**Start:** Identify the load-bearing frame, working element and connections
between them.

- For visible angle iron, extrude the long edge of a narrow plane into an L
  section and give it thickness.
- Assemble a reusable braced cell; duplicate it into the larger frame, then add
  exceptional connections. [A04]
- Use simpler solid bar sections where the camera cannot resolve the hollow or L
  profile.
- Place shafts, grips and rotating elements around explicit axes; retain those
  axes as meaningful pivots.
- Add fasteners only when they clarify scale or assembly at the intended view.
  **Decisive check:** Follow a plausible structural path from base to working
  element. **Repair:** If a mechanism looks decorative, fix unsupported masses
  and ambiguous joints before surface detail. **Repair:** If repeated braces
  create visual noise, simplify the cell or increase its spacing. **Heuristic:**
  Test required mechanical travel with temporary rotations before joining rigid
  parts.

## Vehicles

**Start:** Set wheelbase, wheel radius, track width, body envelope and cabin
placement.

- Align references against a dimensioned box; use photographs to resolve forms
  absent from blueprints. [A03]
- Build a sparse side strip with divisions around wheel arches and major profile
  changes.
- Open and shape the arches, extend the body toward the center and mirror the
  half mesh.
- Reconcile front and top widths as the side profile develops; do not model from
  one view alone.
- Keep wheels separate and select their radial resolution by the visible
  contour. [A02]
- Add cabin, hood and bumper plane changes before lights, trim and handles.
  **Decisive check:** Judge wheel/body ratios and cabin position in silhouette
  before evaluating material detail. **Repair:** If the car feels wrong, check
  wheel placement, roof height and overhang lengths first. **Repair:** If wheels
  intersect, correct clearance and required steering/suspension travel rather
  than hiding the contact. **Heuristic:** Set wheel origins on their rotation
  axes; place a door origin on its hinge axis.

## Branching trees

**Start:** Use an edge skeleton with a dominant trunk and a few main branches.

- Extrude branches relative to their parent directions; shorten lengths and
  reduce radii toward the tips.
- Add bounded branch-direction and length variation, then give the skeleton
  volume with Skin.
- Place foliage masses at branch ends. [A06]
- Inspect Skin junctions: intersecting branches can overlap, while Branch
  Smoothing can shrink the junction.
- Put Mirror before Skin when mirrored geometry is required; Skin's Symmetry
  option alone does not duplicate it. [A11] **Decisive check:** Read the trunk
  gesture and the entire crown silhouette before inspecting individual clusters.
  **Repair:** If junctions bulge or cross, reduce radii, separate branch origins
  or rebuild the local junction. **Repair:** If the tree resembles random noise,
  consolidate canopy masses and restore a clear branching hierarchy.
  **Heuristic:** Seed procedural variation and expose a few meaningful
  species/style parameters.

## Conifers, shrubs and grass

**Start:** Choose a tiered crown, clustered crown or blade-clump construction.

- For conifers, combine a tapered trunk with several low-sided canopy tiers.
- Vary tier outline and size; for broad crowns, compose a few unequal block-like
  volumes. [A08]
- For shrubs, establish the combined outer silhouette before distributing
  secondary lobes.
- For geometric grass, shape a few tapered blades with coherent growth
  directions, then duplicate the clump.
- Keep foliage-card construction as a separate choice when transparency and
  texture rendering are part of the brief. **Decisive check:** Recognize the
  plant's growth habit at its final screen size. **Repair:** If tiers resemble
  identical discs, change their silhouette, spacing and taper. **Repair:** If
  clumps look evenly stamped, vary orientation and proportion within a
  controlled range. **Heuristic:** Spend detail on the crown edge and
  characteristic gaps before adding interior leaves.

## Rocks and cliff pieces

**Original synthesis**; [A08] supports generated-rock exploration and
simplification, not the complete recipe below. **Start:** Choose a resting face,
dominant axis and a low-resolution solid.

- Shape the largest planes deliberately; establish one or two secondary breaks
  that explain the rock's character.
- Change the silhouette asymmetrically while retaining a convincing contact with
  the ground.
- For a cliff kit, align strata direction and connection regions across
  neighboring pieces.
- If simplifying generated geometry, inspect a duplicate and retain the editable
  source. **Decisive check:** Read a stable large form and intentional plane
  changes in a neutral material. **Repair:** If it resembles a scaled ball,
  flatten its base and introduce stronger unequal planes. **Repair:** If it
  contains slivers or tiny facets, merge or rebuild local regions instead of
  increasing random displacement. **Heuristic:** Use material variation to
  support the chosen planes; avoid unrelated color noise per face.

## Terrain and islands

**Start:** Use a grid sized for the required ridge, valley and placement
spacing.

- Raise broad masses with a large proportional influence radius, then add
  smaller local changes.
- Choose the falloff intentionally; inspect the resulting triangulation and
  facet pattern.
- Use Connected Only when nearby disconnected geometry must stay unaffected.
- Use Projected from View only when ignoring depth is intended. [A12]
- Establish traversable or buildable areas as explicit design constraints, not
  accidental flat leftovers. **Decisive check:** Inspect the terrain obliquely
  and from the gameplay camera; preserve readable slopes and usable regions.
  **Repair:** If peaks become needles, reduce local height change or
  redistribute surrounding vertices. **Repair:** If adjacent tiles split,
  enforce shared boundary positions before adding decorative cover.
  **Heuristic:** Keep broad height structure dominant; avoid equal-amplitude
  noise across the whole surface.

## Humanoid bodies and faces

**Start:** Choose static, rigid-part or skinned construction and the required
range of motion.

- Align body landmarks across front/side references; build the main proportions
  with sparse cross-sections.
- For expressive faces, establish eye/mouth loops and their depth before filling
  the surrounding head. [A07]
- Preserve the intended head, torso and limb relationships rather than adopting
  a tutorial's character proportions.
- Allocate geometry around bending areas and use deliberate triangles where they
  improve the result. [A09,A10]
- Build only the facial features, fingers and hidden anatomy required by the
  brief. **Decisive check:** Evaluate both the neutral silhouette and
  representative required poses. **Repair:** If the face is flat, correct
  side-view depth and jaw/forehead masses before facial detail. **Repair:** If a
  joint collapses, inspect weights, bone pivot and local connectivity
  separately. **Heuristic:** Do not force one neutral pose on every rig; match
  the rigging contract and motion range.

## Animals and creatures

**Start:** Use a mirrored abdomen volume and identify the characteristic head,
back and limb gesture.

- Extend the neck/head and haunches in side view; adjust widths from the front
  and top.
- Extrude legs from planned underside regions, tapering where contour or
  articulation changes.
- Correct stance in front view; taper ears and tail through successive
  extrusions. [A13]
- Allocate extra geometry at required bends rather than uniformly subdividing
  the animal.
- Keep species-defining features coherent: muzzle, ear placement, back line,
  feet and tail silhouette. **Decisive check:** Identify the creature from a
  plain silhouette before adding spots, fur or eye detail. **Repair:** If the
  torso looks like a slab, correct chest/abdomen/hip width relationships in
  another view. **Repair:** If the legs splay unintentionally, fix their
  attachment and stance rather than rotating the whole body. **Heuristic:**
  Place a merged ear/tail tip away from a major bend; use a small section
  instead when deformation needs it.

## Hair and fur masses

**Start:** Divide the hairstyle into a scalp mass and a few directional locks or
clumps.

- Use low-resolution curves with a shaped bevel profile for thick locks; control
  width, taper and tilt.
- Preserve the curves before converting a derived copy to mesh. [A05,A07]
- For a faceted style, choose curve/profile resolution from the desired planes
  instead of adding subdivision by default.
- Build broad fur tufts by the same mass-and-direction logic when appropriate.
  **Decisive check:** Inspect front, profile, back and the hairline for intended
  coverage and a clear parting direction. **Repair:** If scalp holes appear,
  adjust root coverage or the underlying cap instead of adding many thin
  strands. **Repair:** If locks resemble tubes, flatten their inner profile and
  widen the broad outer face. **Repair:** If conversion creates excessive
  triangles, reduce curve/profile resolution while checking the silhouette.
  **Heuristic:** Add isolated flyaways only when the design or final camera
  benefits from them.

## Clothing and soft accessories

**Start:** Choose fitted shell, loose garment or rigid accessory construction.

- For a fitted garment, duplicate the relevant body region and reshape it into
  the garment silhouette. [A07]
- For a loose garment, block out its independent hanging volume before
  considering folds.
- Add visible edge thickness where required; keep hems, cuffs and collars
  readable.
- Use cloth simulation only when its drape is useful, then simplify a derived
  result for the delivery target. [A05] **Decisive check:** Inspect garment/body
  separation in neutral and required bent poses. **Repair:** If the garment
  clings like painted skin, change the envelope and bridge areas where cloth
  spans the body. **Repair:** If it intersects, inspect garment clearance and
  deformation before deleting the underlying body. **Heuristic:** Delete covered
  body faces only after testing every required view and outfit state.
  **Heuristic:** Put a few folds at tension, compression or attachment regions;
  avoid uniform zigzag wrinkles.

## Clouds, smoke and magical volumes

**Original synthesis**; these are graphic geometry recipes, not physical fluid
simulation guidance. **Start:** Choose a recognizable overall volume, movement
direction and opacity strategy.

- Compose a few unequal low-resolution lobes into a dominant mass with limited
  secondary breakup.
- Use opaque or translucent geometry according to the renderer and brief;
  inspect overlaps in the target engine.
- For smoke, arrange masses along a rising or wind-driven path and vary size
  coherently along it.
- Keep motion controls simple: transform/scale lobes or move instances along a
  designed path. **Decisive check:** Read the entire cloud or plume against
  representative background values. **Repair:** If it resembles a bead chain,
  overlap and consolidate masses while varying rhythm. **Repair:** If
  transparency causes seams or sorting artifacts, change the geometry/material
  strategy instead of hiding it with lighting. **Heuristic:** Avoid dense
  intersecting transparent shells unless their cost and blending behavior have
  been verified.

## Fire, water splashes and stylized impact shapes

**Original synthesis**; derive the mesh from motion and graphic readability, not
decorative noise. **Start:** Choose a broad base, action direction and a few
large tapering tips or lobes.

- For fire, arrange tapered flame volumes around one dominant upward gesture;
  reserve small tongues for accents.
- For a splash, establish the impact center, outgoing sheet and largest droplets
  before small spray.
- For an impact effect, exaggerate the direction and timing of the main shape
  before fragment count.
- Test emissive materials under the actual exposure; preserve shape even when
  highlights are bright. **Decisive check:** Read the effect's cause, direction
  and extent in a representative still and during motion. **Repair:** If fire
  resembles crystals, soften the directional rhythm or vary taper and curvature
  deliberately. **Repair:** If a splash resembles a crown of identical spikes,
  change tip spacing, height and sheet thickness. **Heuristic:** Prefer a few
  animated shapes with clear timing over many static, evenly spaced fragments.

## Deformation diagnostics for any organic recipe

- Test required poses before texture polish; neutral topology alone does not
  establish animation quality. [A09]
- Inspect the final triangulation diagonal where a bending quad changes its
  visible form. [A10]
- If an artifact follows one bone unexpectedly, investigate weights and
  influence assignment.
- If a bend loses volume despite plausible weights, inspect pivot location and
  local topology.
- If an appendage twists poorly, inspect rig capability as well as mesh density.
- Recheck the intended camera after the repair; a technically improved bend must
  still preserve the design.

[link-1]: sources.md
