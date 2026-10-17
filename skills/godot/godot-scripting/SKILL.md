---
name: godot-scripting
description: Write, generate, diagnose, review, or refactor GDScript and Godot C# in Godot 4 projects, preserving script, scene, lifecycle, input, and editor contracts.
---

# Godot Scripting

Use this skill for Godot 4 GDScript and C# work. Confirm the project's minor
version, language mix, and conventions, then keep implementation consistent with
actual scene contracts, lifetimes, and serialization boundaries.

## Workflow

1. Read `AGENTS.md`, `project.godot`, relevant scenes, scripts, tests, and
   language configuration.
2. Confirm the actual Godot minor version. Use matching documentation, editor,
   or source for version-sensitive conclusions; when unknown, use Godot 4.7 only
   as an explicitly labeled investigation fallback.
3. Read only references needed for the current language and task; mixed-language
   projects do not require both sets unconditionally.
4. Before coding, identify the owner, SceneTree lifetime, Inspector contract,
   external dependencies, runtime state, and cleanup points.
5. After generating or editing scripts, perform language-level checks. Also use
   `$godot-build-and-diagnostics` when build, import, editor, or runtime
   evidence is needed.

Also use `$godot-scene-and-resource-authoring` for scene-tree restructuring,
`.tscn`, `.tres`, Resource ownership, or editor assets. Add
`$game-development-best-practices` only for engine-independent gameplay
architecture, input semantics, or data boundaries.

## Read References as Needed

- For instantiation, SceneTree lifetimes, signals, language events, input
  mapping, async cleanup, dynamic UI refresh/focus, or dependency direction,
  read `references/runtime-and-lifecycle.md`.
- For `.gd`, read `references/gdscript.md`.
- For `.cs`, `.csproj`, or Godot .NET, read `references/csharp.md`.
- For script reviews or review-derived refactor plans, read
  `references/review.md`.

## Stable Rules

- Derive from Godot node types only when transforms, frame processing, SceneTree
  notifications, serialization, or editor hierarchy are needed.
- Inject state that must be valid before tree entry before `AddChild()`; perform
  tree-dependent lookup, registration, and connection in the appropriate
  lifecycle callbacks.
- Use typed exports and truthful Inspector visibility. Do not expose internal
  Inspector-only nodes as public runtime APIs without a reason.
- Express required commands and queries through narrow direct methods; use
  signals or events for facts that have occurred and may have independent
  observers.
- Consume semantic input actions; keep physical keys and device details out of
  gameplay rules.
- Tie registration, subscriptions, timers, async work, and cancellation to the
  owner's lifetime. Recheck object validity after async resumption.
- Generated code must explain non-obvious Inspector, lifecycle, signal, Resource
  mutation, parent injection, and dynamic assembly contracts in the code; do not
  narrate ordinary control flow.
