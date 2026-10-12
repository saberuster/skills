# Visual styles and assets

Treat visual style and intended use as independent dimensions. Pixel art may
be a concept illustration; painterly work may have strict game-asset limits.
Apply constraints from the actual request, not from a category label alone.

## Describe a visual language

Use relevant dimensions rather than relying on a style name alone:

| Dimension | Useful distinctions |
| --- | --- |
| Medium | Pixel art, vector illustration, ink, watercolor, or stylized 3D rendering. |
| Shape language | Rounded or angular forms, simplification, exaggeration, silhouette, and proportional tendencies. |
| Color organization | Palette relationships, color blocks, saturation, contrast, and accent placement. |
| Shading | Flat fills, discrete shade steps, gradients, cast-shadow design, and simplified illumination. |
| Edges and linework | Outlines, hard or soft transitions, brush edges, or pixel stair steps. |
| Detail strategy | Focal areas, deliberately simplified regions, texture density, and readability at the intended viewing size. |

Specific subject anatomy or proportions belong in Image content; global
stylization belongs in Visual treatment. These descriptions must agree.
Material and lighting are useful when relevant, not mandatory photographic
defaults. Describe watercolor through washes and edges, for example, rather
than forcing it into a physical camera setup.

Styles can combine across dimensions. "Pixel rendering, exaggerated cartoon
shapes, and a restrained warm palette" describes compatible choices. For
different treatments within one image, state each treatment's subject or region.
Clarify incompatible instructions for the same feature instead of stacking
style labels or selecting a hidden winner.

## Pixel-specific descriptions

When relevant, describe logical pixel scale, cluster organization, edge
stepping, outlines, shade ramps, isolated pixels, and dithering. Use the user's
preferences or supplied observations; pixel art does not universally prohibit
dithering, outlines, gradients, or semi-transparent effects.

Keep separate the source texel grid, an enlarged presentation, and eventual
on-screen size. An enlarged screenshot does not establish a native resolution,
exact palette, or alpha rule. State supplied exact constraints in Output
requirements. Do not infer them merely from a pixel-like appearance.

## Conditional game-asset requirements

Use only specifications needed for the requested asset:

- Static sprites and icons: final canvas, occupied area, margins, background,
  alpha policy, palette restrictions, and alignment anchor when supplied.
- Animation and directions: required states, views, frame count and order,
  common canvas and anchor, and timing or loop requirements when supplied.
- Tiles: tile dimensions, seamless edges, adjacency, and permitted variation.
- UI pieces: intended display size, border preservation, and nine-slice areas
  when requested.

For a series, read
[References, edits, and series](references-edits-and-series.md). Put these
requirements inside the prompt, not in a separate asset contract. Avoid
assigning frame counts, indexed color, or technical limits to concept art
unless the user actually wants them.

Final specifications may require downstream work. Express the desired file,
pixel, alignment, or animation properties without claiming to have exported,
sliced, palette-quantized, tested, or integrated anything. A prompt can request
seamless tiles or matching views; writing it is not evidence of those results.
