# Godot Script Review

Use for focused `godot-scripting` reviews and review-derived refactor plans.
Confirm project language, Godot minor version, scene contracts, and actual
validation evidence first.

## Common Checks

- Do node scripts provide broad services needing no transforms, processing,
  SceneTree, or serialization?
- Is required state injected only after `AddChild()`, letting entry callbacks
  observe invalid objects?
- Do registration, subscriptions, timers, cancellation sources, and async tasks
  match owner lifetime?
- Do signals/events hide a single required command/query target?
- Does gameplay read physical keys/devices directly instead of semantic actions?
- Does dynamic UI rebuild repeatedly for display-text changes? For necessary
  rebuilds, does it restore only previously owned, still-valid semantic focus
  not superseded by later navigation? Check style geometry, input during
  refresh, and stale event bindings on reused controls.
- Does generated code omit non-obvious Inspector, lifecycle, parent injection,
  Resource mutation, or dynamic assembly comments?

## GDScript Checks

- Are typed/dynamic styles mixed unintentionally?
- Do unsafe casts/untyped lookups hide broken scene contracts?
- Are exports, signal names, and payloads stable and explicit about required
  configuration?
- Does `preload`/`load` hardcode replaceable external dependencies?
- Are warnings too noisy, or too permissive for deliberately typed code?

## C# Checks

- Can captured lambdas/custom signal subscriptions outlive freed receivers?
- Are generated Godot signal events invoked as ordinary C# events instead of
  through `EmitSignal`?
- Are exported values, collections, or signal payloads incompatible with
  Variant?
- Have filenames, main types, or Godot `partial` classes drifted?
- Are internal Inspector members public without a reason?
- Are `async void`, fire-and-forget tasks, cancellation, and object validity
  after awaits handled correctly?
