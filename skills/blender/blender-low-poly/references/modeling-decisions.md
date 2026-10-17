# Modeling decisions

These are conditional modeling choices. Source IDs resolve in
[sources.md][link-1]; numerical starting points below are adjustable heuristics,
not industry limits.

## Shape and representation

Use silhouette to allocate geometry. A contour-changing vertex has more value at
long viewing distance than an interior subdivision that changes neither shape
nor material. Check negative spaces: a chair's leg gaps, a vehicle's wheel
clearances, and a tree's canopy openings often communicate more than surface
marks. [SH10, A02, A03; prioritization synthesized]

| Form/need | Starting method | Why / stop condition |
| --- | --- | --- |
| Box-like prop or building | Cube, edit dimensions, inset/extrude selected regions | Clear planes and controllable proportions; stop adding cuts when they do not affect structure |
| Tapered limb, trunk, pipe or post | Sparse polygon rings, scaled sections, bridge/extrude | Put sections at contour changes; use enough radial segments for intended angularity |
| Symmetric body or vehicle | Half mesh + Mirror | Maintain center seam and cross-sections; do not duplicate both halves manually |
| Repeated structural elements | Array or linked duplicates | Keep spacing and section consistent; choose whether repetition is editable or export-ready |
| Rigid assembly | Separate intersecting/abutting parts where appropriate | Preserve moving pivots; inspect visible penetration and unwanted internal geometry |
| Skinned organic form | Connected loops around required bends | Allocate deformation geometry before face/garment detail |
| Designed rock/faceted mass | Low-resolution solid + deliberate plane edits | Preserve a resting face and hierarchy of planes; avoid uniform jitter |
| Existing dense organic geometry | Duplicate, simplify, inspect; retopologize if required | Accept only if silhouette and downstream constraints survive |

Choose cylinder/cone segment counts by observed outline, not a default
high-resolution primitive. Try a sparse count and increase only when the
intended silhouette needs it. An intentional octagonal lamp and a nominally
circular wheel have different criteria.

## Extrude, inset and connectivity

Extrude from a chosen region to grow continuous forms. Inset when a rim, panel
or opening has actual visual/structural value; check thickness at concave
corners. Do not add edge loops solely to make a wireframe dense. [SH07]

In interactive Blender, canceling the **move after extrusion** can leave the new
geometry in place. Inspect or undo the extrusion itself when cancellation was
intended. Repeated coincident faces can cause dark shading and confusing
cleanup. [SH07]

Use merge-by-distance only with a scope and tolerance appropriate to model
scale. Protect intended seams, separate layers and close mechanical gaps.
Recalculate normals after connectivity changes when orientation can be inferred,
then inspect the result; open sheets and nested shells may need deliberate
sidedness.

Treat n-gons as an authoring convenience for stable planar regions. Before
export inspect their tessellation, especially for concavity, holes or
nonplanarity. Do not force all-quads on every static asset. For deformation,
place loops and triangle diagonals according to observed bending, not a
universal quad rule. [A09, A10, P14]

## Modifier choices and order

| Modifier | Use when | Inspect / avoid |
| --- | --- | --- |
| Mirror | Shape is symmetric or temporarily symmetric | Local axis, origin, seam merge threshold, center drift; clipping does not repair a distant seam |
| Array | Repetition has measured spacing | Relative offset depends on bounds; use constant/object offset when appropriate |
| Solidify | A sheet must have thickness | Scale, offsets, corner thickness, intersecting surfaces |
| Bevel | Selected edges need readable width/chamfer | Nonuniform scale, narrow edges, clamp overlap, topology growth and softened silhouette |
| Weighted Normal | Large flat regions need stable lighting | Compatibility with chosen sharp/smooth regions and export; no silhouette repair |
| Triangulate | Stable triangle choices are needed | Nonplanar quads, concave n-gons, deformation and baking consistency |
| Decimate | Dense input has removable redundancy | Compare at target view; preserve material/UV seams and thin parts |
| Skin | Edge skeleton is a useful branching blockout | Branch radii, junction overlap, roots; generated topology still needs review |
| Subdivision | Continuous curvature is actually required | Often conflicts with deliberately faceted output; inspect evaluated cost |

Select order from dependency: mirror a half-branch skeleton before Skin if the
skeleton must be mirrored; resolve geometry affecting a bevel before judging its
width; establish export triangles before tangent-dependent bake acceptance. Do
not assume all modifiers commute. [A11, P14; ordering decisions synthesized]

## Shading is a design decision

- **Faceted solid:** mark intentional planes flat; avoid small triangles with
  arbitrary orientations that produce glittering noise.
- **Hard-surface object:** keep large faces stable, split sharp transitions and
  add chamfer geometry only where needed. Weighted normals may help shading but
  are optional.
- **Sparse continuous curve:** smooth its surface while retaining sufficient
  silhouette segments. Smooth shading cannot round an angular outline.
- **Mixed asset:** assign these choices by part. Do not make every face smooth
  or flat merely for consistency. [SH02, SH05, P01]

Check normals under a simple broad light and with face orientation/backface
culling. A black patch can be a flipped face, overlapping face, degenerate
triangle, a bad custom normal, or a material issue; identify the cause before
changing global lighting.

## Reduction strategy

First remove invisible **redundancy** only if camera access, animation, shadows
and collision/export requirements permit it. Simplify weak secondary forms and
coplanar subdivisions before damaging the primary outline.

- **Collapse:** suitable for general reduction candidates; inspect small
  features and irregular triangles.
- **Planar dissolve:** useful on nearly coplanar areas; protect needed
  boundaries and material/UV discontinuities.
- **Un-Subdivide:** useful for sufficiently regular subdivision-derived
  topology; not arbitrary geometry.
- **Manual retopology:** choose when meaningful contours, animation loops or
  deliberate planar layout cannot survive automated reduction. [SH03, SH06]

Compare before/after in the same target and side views. Record evaluated
triangles, not the Decimate ratio alone. A clean hand-built low-poly mesh may
need no decimation. Voxel remeshing can destroy intended planes and increase
cost; use it only when its connectivity benefits justify rebuilding. [SH03,
SH06]

[link-1]: sources.md
