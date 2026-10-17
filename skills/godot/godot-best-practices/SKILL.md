---
name: godot-best-practices
description: Establish Godot 4 project and version baselines and coordinate project-wide reviews or refactor plans across focused workflows. Use focused companion skills directly for isolated implementation tasks.
---

# Godot Project Grounding and Workflow Coordination

Establish project facts, version evidence, and workflow boundaries. This
compatibility entrypoint coordinates focused skills rather than carrying all
scripting, editor-asset, and build details.

## Modes

- `triage`: establish version, languages, main scene, provenance, local rules,
  and validation chain.
- `guide`: answer questions spanning scenes, scripts, Resources, or project
  structure.
- `review`: coordinate project-wide review, leading with evidence-backed
  findings ordered by impact.
- `refactor-plan`: preserve target behavior/migration invariants and route
  edits/validation to focused skills.

## Evidence Order

1. User-fixed decisions, repository `AGENTS.md`, and project documentation.
2. Current `project.godot`, scenes, Resources, scripts, addons, import settings,
   tests, and validation scripts.
3. Project-bound editor, build configuration, run evidence, and actual Godot
   minor version.
4. Matching official docs, editor, or source.
5. General Godot principles in this skill.

Determine whether material is authoritative project source, exported packages,
automatic conversions, or recovered/decompiled results. Conclude source quality,
author intent, or development process only where evidence supports it. When the
minor version is unknown, Godot 4.7 is an explicitly labeled investigation
fallback, never a project fact.

## Workflow Routing

- Native UI layout, Theme, control states, composite components, or Showcase
  design/implementation/review: `$godot-ui-authoring`. For refresh/input
  diagnostics alone, lead with scripting/diagnostics.
- GDScript/Godot C# writing, generation, diagnostics, or review:
  `$godot-scripting`.
- Scenes, Nodes, Resources, `.tscn`, `.tres`, settings, or asset
  creation/edit/import/generation/review: `$godot-scene-and-resource-authoring`.
- Build, import, editor/headless runs, log diagnostics, or runtime validation:
  `$godot-build-and-diagnostics`.
- Add `$game-development-best-practices` only for engine-independent gameplay
  architecture, ownership, input semantics, asset governance, review severity,
  or migration invariants.

Choose one primary workflow per task; combine only for real boundary crossings.
Do not create file dependencies across skill directories; each workflow must
offer a safe standalone fallback.

## Read References as Needed

For project-wide `review` or cross-domain `refactor-plan`, read
`references/review.md`, then use relevant focused skills' specialized review
references.

## Stable Rules

- Do not prescribe autoload, `CanvasLayer`, signals, groups, inheritance,
  subscenes, or Resources as universal defaults.
- Decide scene, script, and Resource boundaries independently from ownership,
  lifetime, reuse, replacement, editor configuration, and runtime state.
- Project rules/verified Godot behavior take precedence; report conflicting
  tradeoffs rather than letting one layer silently override another.
- Report only actually obtained code, serialization, editor, build, and runtime
  evidence, identifying unverified items.
