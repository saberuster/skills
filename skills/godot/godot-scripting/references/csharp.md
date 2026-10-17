# Godot C# Guidance

Read only when the project contains `.cs`, `.csproj`, Godot .NET configuration,
or the user explicitly asks about C#.

## Project and Version Baseline

- Confirm the project uses a Godot .NET build and generated bindings are current
  before diagnosing missing signals or exports.
- Keep C# class names, filenames, and Godot `partial` declarations aligned.
- Follow existing .NET formatting/analyzers; this reference adds Godot boundary
  rules.
- Do not make C# and GDScript jointly own the same responsibility layer unless
  the boundary is intentional.
- Reserve `Serializable*` names for save, network, or persistence payloads, not
  ordinary runtime domain objects.

## Formatting and Analyzer Changes

When introducing or changing C# quality rules, use the project's SDK and naming
policy rather than imposing a fixed SDK version or naming convention.

- Apply code-style fixes before whitespace formatting, then verify both. A
  successful fix command does not prove that all diagnostics were resolved; some
  naming fixes do not support solution-wide Fix All.
- Use symbol-aware renaming for unresolved naming diagnostics and inspect
  references. Preserve engine overrides, exported/serialized names and their
  scene or Resource data, and unrelated symbols with the same spelling; also
  check `nameof` and inferred anonymous-property names when they affect output
  contracts.
- Use temporary violating examples to confirm that the check rejects the
  intended rules and that unresolved fixes return failure. Remove the examples
  after verification, including on failure, then check the real sources again.

## Comments

- Put required contract explanations in generated code, not only surrounding
  prose.
- Use XML documentation for stable public contracts: reusable public components,
  Resource APIs, non-obvious `[Export]`/`[Signal]` members, and parent
  injection/initialization methods.
- Inline comments explain Godot-specific boundaries: lifecycle choices,
  scene/export injection, `Dynamic assembly exemption: ...`, signal cleanup,
  Resource duplication/runtime mutation, and Variant conversion.
- Use concrete editor-author wording such as "assigned by the parent scene" or
  "duplicate before runtime mutation"; do not narrate ordinary flow.
- If ordinary flow needs comments to be understandable, consider renaming,
  splitting methods, extracting a Resource/plain C# object, or explicit scene
  contracts.

## Exports and Inspector Contracts

- Use `[Export]` for fields/properties saved with a scene/Resource and editable
  in the Inspector.
- Keep Inspector-only `[Export]` members private; expose only for a real runtime
  contract with other objects.
- Export only Variant-compatible types.
- Prefer typed node/Resource exports when editor assignment is clearer than
  runtime lookup.
- Avoid complex getters that obscure Inspector defaults. Grouping improves
  readability but cannot hide confused responsibilities.

## Nodes and External Dependencies

- Use focused `Node` subclasses for scene-owned behavior; use plain C# objects
  for logic needing no Godot lifecycle, transform, processing, or serialization.
- Use typed `[Export]` references for parent-provided nodes; export Resources
  only when data needs editor assignment or reuse.
- Use `[Export] PackedScene`, typed exports, or `NodePath` for external scenes,
  Resources, or parent-selected nodes.
- Do not hardcode replaceable dependencies with
  `ResourceLoader.Load("res://...")` or assemble dependencies through
  cross-scene `GetNode<T>("../...")`.
- Keep child lookup within the scene boundary. Store mutable runtime state in
  node fields, plain objects, or per-instance containers, not shared Resource
  definitions.
- Also use `$godot-scene-and-resource-authoring` for scene structure/Resource
  ownership decisions.

## Instantiation and Script Assembly

- Export scene dependencies for runtime-generated content, for example `[Export]
  public PackedScene EnemyScene { get; set; }`, then instantiate by runtime
  count, timing, or data.
- Use `PackedScene.Instantiate<T>()` when the root type is known, injecting
  required state before `AddChild()`.
- A Factory class is not required for every scene; a focused creation method
  suffices if typed instantiation, initialization before tree entry, and
  ownership are preserved.
- Self-contained reusable tools/custom script types may own a small internal
  subtree; export or inject external dependencies.
- When C# constructs fixed project structure normally editor-maintained, record
  `Dynamic assembly exemption: ...` with the runtime reason, bounded scope, and
  remaining visible Inspector/scene contracts.

## Methods, Signals, and Events

- Prefer narrow methods for commands/queries with one required target. Use
  notifications when the sender reports a fact and does not own all responses.
- Use Godot signals for scene/editor connections, cross-language observers, or
  Variant APIs; ordinary C# events for pure C# domain notifications.
- Declare custom signals as public delegate types ending in `EventHandler` with
  `[Signal]`.
- Emit through `EmitSignal` and `SignalName`; do not invoke generated events
  like ordinary events.
- Rebuild when custom C# signals/exports must appear in the editor.
- If captured lambdas or custom signals subscribed with `+=` may outlive the
  receiver, retain the delegate and unsubscribe with `-=` at the matching
  lifecycle point.
- Consider `Connect` when automatic disconnection or `ConnectFlags` is needed.

## Lifecycle and Node Access

- Resolve references requiring nodes in the tree in `_Ready()`.
- Use `_EnterTree()`/`_ExitTree()` when registration/subscriptions must match
  tree membership.
- Fail explicitly for missing/mistyped nodes; prefer `GetNode<T>()` or typed
  exports.
- Do not cache nodes across scene changes without explicit ownership and
  lifetime.

## Async Work and Node Lifetime

- Return `Task` for real async work. Use `async void` only when a required
  callback cannot return a task, handling/routing exceptions at that boundary.
- Observe every fire-and-forget task through an owner helper, continuation, or
  explicit error sink.
- Tie node-owned work to cancellation sources matching tree/disposal lifetime;
  cancel and dispose at matching cleanup points.
- After every `await`, recheck cancellation and `GodotObject.IsInstanceValid()`
  before accessing nodes, SceneTree, or children.

## Variant-Compatible Data

- Collections exported/crossing Variant boundaries need Godot-recognized
  collection types.
- Keep plain C# domain objects outside Variant boundaries unless deriving from a
  compatible Godot type or explicitly adapted.
- Check signal-payload/exported-property Variant compatibility before blaming
  editor/bindings.
