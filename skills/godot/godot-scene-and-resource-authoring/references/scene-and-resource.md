# Scenes, Nodes, and Resources

Map project composition, ownership, lifetime, and runtime state to Godot
scenes/Resources. Match version-sensitive behavior to the actual project minor
version.

## Representation

- Use `.tscn` scenes and feature-local subscenes for fixed editor-visible
  composition.
- Focused scripts/tools may own procedural, pooled, streamed, modded, testing,
  or debug structures.
- Use typed Resources/`.tres` for reusable, assignable, editor-tunable
  definitions.
- Store per-instance mutable state in Nodes, plain objects, or explicitly
  instance-owned Resources.

Feature complexity does not require extracting both subscenes and Resources.
Decide independently from ownership, lifetime, spawning, replacement, testing,
reuse, and editor tuning.

When code constructs fixed project structure normally maintained in the editor,
record `Dynamic assembly exemption: ...` with the real runtime reason, bounded
scope, and remaining Inspector/scene contracts. Self-contained reusable script
types may own small internal subtrees belonging to their abstraction.

## Scene and Node Ownership

- Reusable scenes must not depend on fixed parent, sibling, or `Main` paths.
- Unless root transforms are an explicit contract, keep reusable roots neutral
  in position, rotation, and scale. Place instances and visual corrections on
  parent instances, attachment points, or internal presentation nodes.
- Keep fixed local NodePaths and scene signal connections within scene-owned
  structure.
- Export/inject replaceable external scenes, Resources, Nodes, and
  parent-selected NodePaths.
- Use parenting when child lifetimes follow parents; otherwise choose a
  sibling/higher owner.
- Keep Inspector-only configuration internal unless another owner has a real
  runtime contract.

## Main Scenes, UI, and Autoload

- Entry scenes focus on top-level composition, flow, transitions, and wiring.
- Separate world/gameplay and UI roots only when camera transforms, transitions,
  or input routing need it.
- Use `CanvasLayer` when UI must be independent of world camera transforms.
- Autoload holds only broad state/services meaningful across scenes, with a
  narrow API.
- Add a persistent shell only when cross-scene UI, audio continuity, loading, or
  transitions need a stable owner; do not let it absorb gameplay rules or become
  a service locator.

## Resources and Runtime State

- Treat shared/cached Resources as read-only definitions unless explicit
  ownership makes them instance-local and mutable.
- Trace whether a Resource comes from a PackedScene instance, path cache,
  external asset, or runtime construction before mutation.
- Select `resource_local_to_scene`, `Duplicate()`/`duplicate()`,
  `DuplicateDeep()`/`duplicate_deep()`, or separate runtime state only after
  checking project-version semantics.
- Godot 4.7 deep-container/nested-Resource duplication depends on local/external
  subresource modes; do not generalize to other versions without validation.
- Authoritative Resource/plain-object definitions must not read mutable global
  runtime state.
- Prefer plain objects when no transforms, processing, SceneTree notifications,
  serialization, or editor hierarchy are needed.

## Runtime Instances and Assembly

- Use typed/explicit creation boundaries when root contracts are known.
- Inject state required before entry before `AddChild()`; leave tree-dependent
  lookups, registration, and connections to lifecycle callbacks.
- Instantiate dynamically only for dynamic runtime counts, timing, or data;
  prefer editor-visible fixed composition.
- Parents provide new instances with external Resources/runtime references;
  children must not reach up to `Main` or across sibling branches for required
  setup.
