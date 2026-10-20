# Atlas Layout and Validation

## Establish the Mapping

Keep these coordinate systems explicit:

- Map grid: the TileSet cell shape, layout, and `tile_size`.
- Atlas grid: texture dimensions, `texture_region_size`, margins, separation,
  and each module's region coordinates and span.
- Placement: the stored map cell, intended logical footprint, orientation,
  visual anchor, and any permitted visual overlap.

Read actual image dimensions and metadata; reject out-of-bounds regions,
conflicting atlas regions, and missing module definitions before saving.
Atlas spans count source regions, not automatically occupied map cells.
Keep IDs and alternatives stable when maps already refer to them.

A whole module can span several atlas regions while remaining one tile.
A Pattern (`TileMapPattern`) stores several cell placements and can reuse an
external TileSet; its placed cells remain individually editable. Terrain rules
solve specified neighbor connections and need appropriate terrain variants and
peering data.
Choose these independently from whether art is generated or hand drawn.

## Align the Visuals

Use the source's actual tile region, intended anchor, map cell center, and
orientation to derive `TileData.texture_origin`. Do not reuse an offset from a
different atlas or assume centered art is correct for every module. Test an
asymmetric module against a visible map grid, including any supported flips or
transpose. Confirm pixel rounding at the project's intended camera scale.

For nonrectangular layouts, use the version's map conversion and Pattern mapping
APIs rather than treating all coordinates as Cartesian offsets. If origin or
transform handling is uncertain, make a small disposable alignment scene and
verify saved output before changing the production map.

## Check Coverage and Replacement

A placed multi-region atlas tile records its map anchor. Its image can extend
across neighboring cells without reserving those cells. Maintain an explicit
logical footprint for generators or editing tools that need exclusive coverage.
Rendering bounds, logical occupancy, collision polygons, and navigation regions
are separate definitions; verify each requested behavior independently.

Expand every placement into its transformed logical footprint. Check unintended
overlaps, uncovered required cells, boundary overflow, and replacement remnants
across relevant layers. Allow declared visual overlaps and intentional gaps.
Do not infer completeness from anchor counts alone. When replacing a large
module, clear or replace all affected logical footprints within owned scope.

After saving, reload without relying on already-cached in-memory objects and
compare source references, module IDs, anchors, transforms, and layer settings.
Ensure every requested manual adjustment survives a read-only check and any
regeneration path that promises to preserve it.

## Capture Evidence

Finish exports and consistency checks, import, then capture the actual scene.
Record engine version, scene path, viewport/camera settings, run ID, and checks.
Hash the actual referenced textures plus metadata, saved TileSet and relevant
scenes at baseline and completion; include import settings when material.
Use unique directories even when labels repeat. Recheck during capture when
possible; latch observed changes as invalid even if bytes are later restored.
Keep diagnostic images but exclude invalidated runs from comparisons. Hashes
cannot prove that loaded imports match source or detect every transient edit.

## Official API References

Select the project's minor version in these Godot documentation pages:

- [TileSetAtlasSource][atlas]: region sizing and atlas tile spans.
- [TileData][data]: visual origin and per-tile properties.
- [TileMapLayer][layer]: cell identifiers and map/Pattern coordinate methods.
- [Using TileMaps][maps]: editable Patterns and terrain painting.

[atlas]: https://docs.godotengine.org/en/stable/classes/class_tilesetatlassource.html
[data]: https://docs.godotengine.org/en/stable/classes/class_tiledata.html
[layer]: https://docs.godotengine.org/en/stable/classes/class_tilemaplayer.html
[maps]: https://docs.godotengine.org/en/stable/tutorials/2d/using_tilemaps.html
