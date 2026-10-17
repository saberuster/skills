# Godot Scene and Asset Review

Use for focused scene, Resource, editor-asset, and project-organization reviews.
Confirm minor version, content provenance, task scope, and current diff first.

## Scene and Ownership Checks

- Does `Main.tscn` mix independently owned gameplay, UI, camera, spawning,
  configuration, and state?
- Do reusable scenes depend on parent/sibling paths, external editor signal
  connections, or specific tree positions?
- Do reusable roots carry non-neutral transforms that compound parent placement,
  animations, pivots, or collision?
- Is fixed composition built imperatively without runtime reasons/bounded
  abstraction?
- Does parenting contradict lifetime ownership?
- Does a persistent shell lack cross-scene need or absorb gameplay as a god
  object/service locator?
- Is required configuration only prose, without exports, editor warnings, or
  validation?

## Resource and Data Checks

- Does autoload own scene-local state or expose an overly broad command surface?
- Are static definitions mixed with mutable runtime state?
- Do multiple instances accidentally mutate shared Resources?
- Is PackedScene, path-cache, external-asset, or instance ownership traced
  before mutation?
- Are shallow/deep/nested duplication semantics assumed without project-version
  validation?
- Are Nodes used without node lifetime/editor hierarchy needs?

## Asset Editing Checks

- Are fragile structured `.tscn`/`.tres` files directly edited without clear
  validation?
- Have UIDs, resource relationships, paths, connections, animations, or node
  ownership changed unintentionally?
- Are binaries, `.godot/` data, or import outputs hand-edited?
- Do generated assets lack auditable owner mappings, required UID mappings, or
  bounded output roots?
- Are graph Resources/generated directories patched with raw strings?
- Does runtime code guess related third-party files instead of consuming
  validated contracts?
- Do broad saves expand diffs, or is byte equality wrongly required for unstable
  serialization?

## Refactor Plan Additions

Explain separate reasons for extracting subscenes/Resources, text/API/editor
editing paths, save/import boundaries, and evidence required through
`$godot-build-and-diagnostics`. Do not automatically extract both Scene and
Resource without reasons.
