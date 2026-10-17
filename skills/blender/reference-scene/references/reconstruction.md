# From Images to Space

## Facts, Scale, and Blockout

Record purpose, reference views, layout anchors, major silhouettes/color blocks,
dimension evidence, and unknown regions. When perspective is inconsistent,
preserve the user's chosen overall relationships. Clarify adjustments affecting
purpose, circulation, or experience; identify and explain minor structural
corrections.

Cross-check scale using doors, tabletops, vehicles, and people. Unlabeled
dimensions are estimates; foreshortened pixel lengths are not exact
measurements. Block out ground boundaries, buildings, entrances, routes, and
large objects first. Record whether cameras are perspective or orthographic; do
not distort models to suit one shot.

Check semantic relationships: vehicle fronts face exit routes, opening doors
clear posts, accessible tabletops stand above ground, and beams/posts support
roofs. Check slopes and turns in local frames instead of fixed world X/Y.
Resolve silhouettes, proportions, and color blocks before bottle caps or screws.
Rerender according to actual changes; do not mechanically repeat every view.

## Backsides, Editing, and Portability

A single image has no unique 3D solution. Infer building rears, cabinet backs,
canopy undersides, and vehicle underbodies from visible construction and
comparable uses, and label the inference. Necessary structure cannot exist only
in textures. Preserve object groups and identity; merge or instance according to
editing, import, and performance needs rather than fixed counts.

Color distribution, simplified silhouettes, polygon style, bevels, and
reflections jointly determine style. Procedural nodes are valid for source
authoring; state which representations become geometry, are baked, or are
rebuilt in the engine for exchange. Billboards and single-sided surfaces depend
on viewing range. Subjects requiring close all-around viewing cannot rely on
representations that work from only one camera.

When source and engine coordinate conventions differ, derive the conversion from
their axis bases and verify position and orientation with an asymmetric sample
in the engine; do not infer Euler-angle signs.

Generator replay may overwrite refinement. Identify the source of truth and
prefer new output directories. Do not reset the user's unsaved Blender session
to run validation examples.
