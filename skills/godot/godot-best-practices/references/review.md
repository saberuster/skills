# Godot 4 Project-Wide Review

Coordinate reviews across scripts, scenes/Resources, UI, and build validation.
Focused skills own specialized rules; this reference does not duplicate their
full checklists.

## Preparation

Inspect `project.godot`, actual minor version, rendering/runtime assumptions,
main scene; relevant scenes, Resources, scripts, addons, generated files,
languages; autoload, settings, InputMap, validation/tests; `AGENTS.md`, docs,
naming/layout conventions; current diff, fresh logs, and run evidence.

Classify provenance first:

- Authoritative project source and normal repo metadata support conclusions
  about runtime structure/development artifacts.
- Exported, converted, recovered/decompiled projects establish only
  runtime-visible scenes, dependencies, ownership, lifetime, and asset
  relationships.
- Mark potentially removed/reconstructed comments, formatting, version-control
  practice, tests, and author intent unknown.
- Claiming those unknowns as confirmed process defects is itself a review
  problem.

## Output Contract

When `$game-development-best-practices` is active, use its P0-P3
severity/finding structure. Otherwise order by impact, including location/scene
path, behavior/maintenance risk, trigger, evidence, and minimal fix/validation
direction.

If no findings exist, say so and identify uncovered checks/validation gaps. Do
not manufacture style findings to fill reports.

## Focused Routing

- Native layout, theme overrides, control states, composites, or Showcase
  dependencies: `$godot-ui-authoring`, choosing layout/theme or Showcase
  references. Route refresh/input evidence to scripting/diagnostics.
- Scripts, lifecycle, signals, input, or language risks: `$godot-scripting`,
  which chooses its review references.
- Scenes, Resources, autoload, assets, UIDs, organization, or editor authoring:
  `$godot-scene-and-resource-authoring`, which chooses its references.
- Builds, import, serialization, logs, headless, or UI/input runtime evidence:
  `$godot-build-and-diagnostics`, which chooses validation references.

## Cross-Domain Checks

- Conflicting authoritative copies of the same state across scenes, scripts, and
  Resources.
- Contradictory ownership, lifetimes, or external dependencies between
  structure/script contracts.
- Unverified fallbacks replacing actual versions, editor behavior, or
  serialization semantics.
- Code-only review ignoring real composition, assets, imports, and runs.
- Lower-level checks mistaken for player-visible behavior evidence.
- Refactors changing architecture, language, asset truth sources, and validation
  entries without migration order/stop conditions.

## Refactor Plans

Specify target behavior, invariants, ownership migration, focused-skill
responsibilities, edit order, risk-matched validation, and stop conditions. Do
not extract both Scene and Resource automatically or smuggle language
migrations, broad naming cleanup, or architecture replacement into fixes.
