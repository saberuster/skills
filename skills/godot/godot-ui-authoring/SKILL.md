---
name: godot-ui-authoring
description: Design, implement, or review Godot 4 native UI layouts, themes, control states, reusable components, and UI showcase scenes. Use for reference-driven game UI and incomplete control styling, not web UI, gameplay rules, isolated build failures, or explanation-only Theme questions.
---

# Godot UI Authoring

Align reference designs, native Godot controls, and actual interaction. Handle
layout, themes, composite components, and UI Showcase within the requested mode:
design advice, read-only review, or authorized implementation.

## Establish Scope

Read project rules, actual minor version, relevant scenes/scripts/themes, and
run entrypoints. Confirm the worktree and selected design. Local styling fixes
follow affected controls/shared-style callers; do not automatically redesign
pages, create Showcase, or write design documents.

Identify native controls, theme resources, instance overrides, construction
helpers, and composite components. Factory methods are not custom control
classes. Assign styling by existing implementation rather than inventing another
UI system from wrapper names. Preserve required editor visibility for fixed
composition; code construction needs actual reusable internal subtrees, dynamic
data, or demo assembly reasons.

## From Design to Implementation

- Separate visual language, layout relationships, and business information in
  references. Implement selected shapes, hierarchy, spacing, and feedback; do
  not transplant decorative numbers without gameplay data into fictitious
  systems. Corner shapes, colors, line widths, and resolution are project
  inputs, not universal defaults.
- For layout, Theme, control styling, or visual review, read [Layout, Themes,
  and Controls](references/layout-and-theme.md). Check applicable
  states/internal graphics, including combinations, against actual controls.
  Inspect shared themes and local overrides together.
- For requested component-library displays, general demos, or existing Showcase
  changes, read [Component Showcase](references/showcase.md). Decouple demos
  from business UI; physical project boundaries follow real build/distribution
  needs.
- Trace real consumers of shared control changes. Rebuilding, focus loss, or
  interrupted input from refresh belong to script update strategy; recoloring
  cannot hide them.

## Collaboration and Checks

This skill owns UI design/control contracts. Use available focused skills as
needed without loading all for every small edit:

- `$godot-scripting`: control logic, signals, refresh, and focus lifetimes.
- `$godot-scene-and-resource-authoring`: scene/Resource ownership, editor
  operations, and serialization.
- `$godot-build-and-diagnostics`: build/run, input coordinates, and state
  validation.

When unavailable, complete scoped work through matching APIs, existing
scene/theme conventions, and run commands. Without runtime conditions, identify
source-only conclusions. Validate affected transitions, long text/empty states,
and layout scaling; observe real input results/rendering. Correct properties do
not prove readability; Showcase success does not prove business integration.

Design handoffs state inspectable rules/open decisions; reviews lead with
located, impactful findings; implementation handoffs state actual edits, checks,
and limits. Use existing documentation entrypoints and update docs only when
task/project rules require them; avoid adding a new explanation file for each
styling iteration.
