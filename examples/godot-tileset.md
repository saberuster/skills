# Godot TileSet behavior cases

Use a fresh agent with only the complete `godot-tileset` package and the stated
fixture. Deliver the user request without the assessment criteria. Retain the
reply, tool actions, source snapshot, file outcomes, and a separate assessment.
These planning cases authorize no file writes, engine launches, or installation.
They test explicit skill use, not automatic discovery or real engine behavior.

## Mixed modules and existing edits

Request: "Use godot-tileset to plan a Godot 4 square-grid courtyard integration.
The map grid is 12 by 12. Slabs are 24 by 12 with no padding; a corner should
remain a reusable arrangement of small tiles. The atlas cells are 6 by 6 with
no separation. A stain is 36 by 24 and crosses slabs. Artists have edited the
saved map since its generator last ran. Keep their work. Give me the resource,
placement, and validation plan; do not edit or run anything."

Assess whether the response distinguishes atlas units, map units, whole tiles,
and Patterns; checks multi-cell footprints separately from stored anchors;
keeps the stain independently editable without imposing a fixed layer count;
and preserves the hand-authored map. Exact API claims require version evidence
or explicit qualification. No engine execution is claimed.

## Procedural terrain and optional collisions

Request: "Use godot-tileset to plan connected terrain for a procedurally generated
map. Some tile images overhang their map cells; cliffs need collision and grass
decoration does not. We have an existing generation pipeline. Give a read-only
plan that fits it."

Assess whether terrain connectivity remains a supported option, runtime
randomness is preserved, and visual overhang is not automatically treated as
occupied map cells or collision. The plan should obtain the actual version and
resource contracts before prescribing APIs or migration.

## Captures from a changing atlas

Request: "Use godot-tileset to assess this evidence: capture A finished, its PNG
atlas was then regenerated, and capture B ran without a confirmed import. Both
used the same output filenames. The manifest text stayed unchanged. Can these
images prove the new floor is integrated? Propose the smallest reliable rerun."

Assess whether the response identifies overwrite, actual-byte version, and
import-cache gaps; requests fresh distinct outputs after export and import;
and separates structure, runtime visibility, and visual acceptance. Source
hashes must not be presented as proof of imported-cache freshness.
