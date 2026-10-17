# GDScript Guidance

Read this reference when the project contains `.gd` files or the user explicitly
asks about GDScript.

## Project and Version Baseline

- Determine whether the codebase uses typed, dynamic, or deliberately mixed
  code.
- Prefer one dominant style per project or module; mixing is allowed when
  intentional and readable.
- Use `class_name` for globally named editor types; keep anonymous, scene-local
  scripts private.
- Keep script names, class names, and scene/node responsibilities aligned enough
  for editor navigation.

## Comments

- Put required contract explanations in generated code, not only in surrounding
  prose.
- Use `##` documentation comments for stable reusable contracts that belong in
  generated docs or editor help; use ordinary comments for local lifecycle and
  implementation boundaries.
- Explain non-obvious `@export` properties, signals, public initialization
  methods, and parent injection points so scene authors understand required
  assignments and timing.
- Inline comments should explain `_ready()`, `_enter_tree()`, `_exit_tree()`,
  scene/export injection, `Dynamic assembly exemption: ...`, signal cleanup,
  Resource mutation, and Variant boundaries.
- Use concrete editor-facing wording such as "assigned by the parent scene" or
  "duplicate before runtime mutation"; do not narrate ordinary control flow.

## Static Types

Typed GDScript catches errors earlier and improves completion and long-term
readability. Prefer explicit types for public/cross-scene APIs, exports, signal
callback arguments, arrays/dictionaries passed across modules, and values from
`get_node`, casts, factories, or Resources.

Do not force an entire dynamic codebase to become typed without a migration
plan. Small prototypes may remain dynamic when the project explicitly
prioritizes iteration speed.

## Node References and Dependencies

- Prefer `@onready` references for required children owned by the same scene,
  keeping paths local where possible.
- Let parents provide external dependencies through typed exports, exported
  `NodePath`, Resources, or initialization methods.
- Export external scenes as `PackedScene`, for example `@export var
  bullet_scene: PackedScene`.
- Do not hardcode replaceable external resources with `preload("res://...")` or
  `load("res://...")`; reserve them for private implementation details owned by
  the script's scene and sharing its lifetime.
- Use `as` carefully: silent `null` may hide scene changes. When a type mismatch
  breaks a contract, use `is`, assertions, or explicit failure.
- Also use `$godot-scene-and-resource-authoring` for scene structure or Resource
  ownership decisions.

## Instantiation and Script Assembly

- Export scene dependencies for runtime-generated content, such as `@export var
  enemy_scene: PackedScene`, then instantiate according to runtime count,
  timing, or data.
- Self-contained reusable tools/custom script types may own a small internal
  subtree; export or inject replaceable external dependencies.
- When GDScript builds fixed project structure normally editor-authored, record
  `Dynamic assembly exemption: ...` with the reason, bounded scope, and
  editor-visible contract.

## Exports and Inspector Contracts

- Export properties designers/scene authors need to configure in the editor.
- Use typed exports to constrain Inspector values and express intent.
- Group or rename related settings when useful; exports do not replace clear
  ownership.
- For missing required configuration, consider `_get_configuration_warnings()`
  or validation that makes the problem visible in the editor.

## Signals

- Use signals for notifications/responses, not as a hidden command bus for
  unrelated behavior.
- Prefer past-tense or event-style names for facts that have occurred.
- Keep cross-scene/module signal payloads stable and typed.
- For code-connected signals, determine cleanup from whether the receiver may be
  freed before the emitter.

## Warnings and Safety

- Inspect project warning settings before recommending stricter rules.
- Typed projects may watch untyped declarations, inferred declarations, unsafe
  calls, and unsafe property access.
- Treat warning-setting changes as team workflow changes: explain migration
  scope and expected noise rather than switching them incidentally.
