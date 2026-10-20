---
name: godot-tileset
description: Create, edit, diagnose, or validate Godot 4 TileSets and tile maps from modular assets, preserving editable tiles, placement rules, layers, and saved resources.
---

# Godot TileSet

Integrate modular assets into editable Godot tile maps. Read
[atlas layout and validation](references/atlas-layout.md) for alignment,
coverage checks, and evidence. Asset drawing remains a separate task; use an
available pixel-asset workflow when new artwork is requested.

## Workflow

1. Read project instructions, current changes, `project.godot`, relevant scenes,
   TileSets, source textures, import settings, and asset metadata. Confirm the
   engine minor version, projection, map grid, atlas layout, and intended edits.
   Resolve missing consequential inputs from project evidence or the user;
   label new defaults. Use version-matched APIs and documentation.
2. Choose the editing unit: a whole atlas tile for an indivisible module, a
   Pattern (`TileMapPattern`) for reusable arrangements of independently
   editable cells, or terrain rules for automatic neighbor connections.
   Preserve an existing suitable approach, including generator randomization
   and seed handling unless the task changes them. Choose alternatives and
   collision by task needs.
3. Establish source IDs, atlas coordinates, region sizes, logical footprint,
   placement anchor, and rendering origin from the actual assets. Preserve IDs
   referenced by existing maps, or migrate their uses explicitly. A multi-region
   atlas tile still has one map cell anchor; implement footprint-aware editing
   or generation when neighboring logical cells must be reserved.
4. Organize separately editable content by purpose, such as structure,
   replacement pieces, and regional wear. Select node types, layer count,
   sorting, transforms, and opacity from the project. Preserve collision and
   navigation contracts independently of visual layering.
5. Edit only task-owned resources. Preserve manual placements and resource
   properties. Keep read-only checks separate from rebuild commands; generators
   declare outputs and replacement scope, retain valid output on failure, and
   avoid overwriting unowned edits.
6. Save and reload the resources. Validate references, tile identifiers, atlas
   bounds, placement footprints, intended coverage, layers, and configured
   collision/navigation. Inspect the saved scene rather than only generator
   memory. Then import and inspect editor operations and the actual runtime.

## Validation and Delivery

- Reuse the project's launch procedure when present. Otherwise supervise the
  selected engine process with project path, logs, exit status, and a deadline;
  stop only processes started for this check. Build managed code when needed.
- Complete asset export, source consistency checks, and engine import before
  capture. Check that the intended saved scene and resources are actually used.
- In the editor, open the scene and TileSet, select and place representative
  modules, and exercise needed Pattern or terrain operations. Use a disposable
  scene or undo test edits. Report unavailable editor checks explicitly.
- In the actual scene, check joins, alignment, repeated regions, camera scale,
  sorting, and gameplay readability. Structural validity and visual acceptance
  are separate findings; headless success does not establish either appearance
  or editor usability.
- For comparisons, use a unique capture directory per run and record source
  fingerprints before and after capture, including actual referenced image
  bytes, metadata, TileSet, and scene files. Changed sources invalidate the run.
  Fingerprints identify sources; they do not establish import-cache freshness
  or provide a filesystem transaction.
- Deliver saved editable resources, placement/layer conventions, relevant
  checks, and labeled previews. State engine version and evidence limits.
