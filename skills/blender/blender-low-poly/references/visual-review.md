# Visual review and correction

This reference is an original operational synthesis of the shape and asset
sources. Scores are decision aids, not a validated model-quality benchmark.

## Make evidence comparable

Capture the intended game/presentation view at target resolution and a
complementary front/side or oblique view. Keep framing, lighting and scale
consistent for before/after comparisons. Use a neutral background and a broad
light to expose planes. Use the final presentation lighting after basic geometry
reads clearly.

Evaluate the actual rendered pixels at expected on-screen size. Zooming into a
high-resolution render can encourage detail that disappears in use. For a fixed
camera, prioritize that view; inspect other angles for structural errors, shadow
problems and any allowed rotation.

Separate asset objects from floor, camera, lights and dimension references.
Include a silhouette or untextured view when color/lighting obscures structural
problems. For transparent parts inspect against both light and dark backgrounds
if transparency is required.

## Review order

| Priority | Question | Concrete intervention |
| --- | --- | --- |
| 1. Identity | Does the asset read as the intended subject at its actual size? | Change silhouette, mass ratios, distinctive feature sizes |
| 2. Proportion | Are height/width/depth and part relationships correct? | Edit dimensions, cross-sections and landmark positions |
| 3. Construction | Are thickness, joints, gaps and supports coherent? | Repair connections, contact planes and negative spaces |
| 4. Surface | Are facets deliberate and large planes stable? | Change topology, normals or bevel selection based on the cause |
| 5. Color/material | Do regions separate and match the brief under useful lighting? | Adjust palette areas, roughness, material assignment or texture sampling |
| 6. Cost/delivery | Does the asset meet the explicit runtime/export contract? | Remove redundant detail or fix export/import rather than changing the brief |

Do not raise a lower-priority score by concealing a higher-priority defect.
Extra bolts cannot correct a vehicle's wheelbase; high-contrast lighting cannot
certify clean normals.

## Diagnose common failures

| Symptom | Inspect first | Correct |
| --- | --- | --- |
| Primitive collage / toy blocks without intent | Tapers, connections, mass overlap, thickness | Replace the main mass with deliberate cross-sections; improve joints and negative space |
| Too round or inflated | Bevel/Subdivision stack, radii and smooth shading | Remove irrelevant rounding; keep only deliberate chamfers |
| Too boxy | Width/depth ratios, profile changes, meaningful contour cuts | Adjust silhouette locally; do not apply global smoothing as a shape fix |
| Noisy faceting | Small triangles, unbounded displacement, inconsistent plane sizes | Consolidate broad planes, reduce random amplitude or remove random edits |
| Flat silhouette with wrong volume | Front/side/top consistency | Rebuild cross-section depth, not just the currently visible contour |
| Black patches / shimmering | Winding, overlapping faces, zero area, z-fighting | Fix geometry or sidedness before material/lighting changes |
| Sliver bevels or shading pinches | Unapplied scale, narrow geometry, concave corners | Correct scale on appropriate static copies, reduce width or rebuild local edges |
| Soft silhouette despite low triangle count | Too many similar masses / weak negative spaces | Simplify hierarchy and increase relevant shape contrast |
| Character joints collapse | Pivot, weights, edge spacing and triangle direction | Test each cause; add/reorient local bend geometry only where needed |
| Export looks different | Shader support, normals, triangulation, textures, color space | Compare neutral render and imported result, then fix the specific pipeline mismatch |

## Use bounded iteration

For each iteration record: view -> visible defect -> edit -> observed change.
Choose the highest-impact defect, make a small coherent batch, and compare
again. Save a checkpoint before a broad redesign.

Stop when the explicit brief and relevant checks pass. If two targeted attempts
do not improve the same defect, reconsider its diagnosis or construction method
rather than accumulating compensating modifiers.

Report checks as **passed**, **failed**, **not applicable**, or **not
performed**. Never replace a missing screenshot or engine test with a confident
narrative. A numeric mesh audit can pass while the model remains visually poor.
