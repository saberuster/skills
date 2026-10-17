---
name: godot-scene-and-resource-authoring
description: Create, edit, import, generate, diagnose, or review Godot 4 scenes, Nodes, Resources, project settings, and serialized assets, preserving editor composition and content ownership.
---

# Godot Scene and Resource Authoring

Create, edit, and review Godot 4 scenes, Nodes, Resources, project
configuration, and imported assets. Preserve editor-visible composition,
explicit content sources of truth, and verifiable serialization.

## Workflow

1. Read `AGENTS.md`, `project.godot`, relevant `.tscn`, `.tres`, scripts, import
   settings, and current worktree changes.
2. Confirm the actual Godot minor version and whether content is authored input,
   third-party raw input, import output, generated output, or cache.
3. Evaluate scene, script, and Resource boundaries separately for ownership,
   lifetime, reuse, replacement, editor tuning, and runtime state.
4. Choose the most robust editing path: clear local text edits, Godot APIs, tool
   scripts, EditorScript, editor operations, or project generators.
5. Inspect final changes. Also use `$godot-build-and-diagnostics` when import,
   serialization, editor, or runtime evidence is needed.

Also use `$godot-scripting` when writing GDScript/Godot C#. Add
`$game-development-best-practices` only for engine-independent ownership, asset
governance, or migration invariants.

For native UI layout, themes, control states, or Showcase, prefer available
`$godot-ui-authoring`; this skill retains scene/Resource editing and
serialization responsibilities. If unavailable, follow existing scene contracts
and version-matched project APIs without expanding scope.

## Read References as Needed

- For scene composition, Node ownership, main scenes, UI, autoload, Resource
  definitions, runtime state, or instantiation boundaries, read
  `references/scene-and-resource.md`.
- For editing/generating `.tscn`, `.tres`, imported assets, graph Resources,
  `.import`, or `project.godot`, read `references/asset-editing.md`.
- For `WorldEnvironment`, `Environment`, `CameraAttributes*`, `Compositor`, sky,
  fog, glow, tonemap, exposure, or renderer-dependent visual settings, read
  `references/rendering-environment.md`.
- For 2D/3D light nodes, shadows, global illumination (`SDFGI`, `VoxelGI`,
  `LightmapGI`), `ReflectionProbe`, `Decal`, light bake modes, or per-renderer
  light and decal limits, read `references/lighting.md`.
- For directories, names, third-party content, UIDs, version control, or
  generated directories, read `references/project-hygiene.md`.
- For focused scene/asset reviews or review-derived refactor plans, read
  `references/review.md`.

## Stable Rules

- Do not prescribe autoload, `CanvasLayer`, signals, groups, inheritance,
  subscenes, or Resources as universal defaults.
- Decide scene, script, and Resource boundaries separately from ownership,
  lifetime, reuse, replacement, editor configuration, and runtime state.
- Reusable scenes must not depend on fixed parent, sibling, or `Main` paths;
  parents assign/inject replaceable external dependencies.
- Do not text-patch binary, imported, cached, or opaque graph assets.
- Generators manage only declared outputs, retain the last valid result on
  failure, and delete only ownership-verified obsolete content.
- Save only task-owned objects/assets; avoid broad resaves and unrelated UID,
  ordering, or import changes.
