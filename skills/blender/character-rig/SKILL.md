---
name: character-rig
description: >-
  Inspect and repair existing Blender character rigs and skin deformation using
  pose tests and animation regression checks. Use for joint alignment, skin
  weights, or deformation faults; not scene reconstruction, rig creation from
  scratch, or animation authoring alone.
---

# Character Rig

Diagnose the cause before changing a character's binding. Match the requested
inspection or repair scope; use separate diagnostic copies for test actions and
preserve a recoverable source.

## Diagnose and reproduce

- Inspect rest and posed geometry, bone hierarchy, actual skin influences,
  armature modifiers, and active actions or NLA tracks. Distinguish terminal
  display markers, deforming pivots, skin weights, topology, and animation
  faults. A protruding bone endpoint or left/right asymmetry alone does not
  establish a bad pivot.
- Separate imported UV/normal splits from genuine holes or disconnected
  surfaces. Judge joints against the surrounding shape and motion, not unsigned
  distance to the nearest surface alone.
- Reproduce each suspect joint with ordinary movement and, when useful, a stress
  pose. Derive rotations from the actual rest pose and anatomical direction
  rather than assuming imported bone axes. Label isolated tests that omit
  contact solving; their floating feet are not evidence of a production contact
  failure.
- Compare before and after at the same pose, frame, camera, and visibility.
  Inspect intermediate frames, silhouettes, close views, and obscured sides as
  relevant. Include existing actions: an idle pose or a single improved action
  does not establish a sound rig.

## Repair locally

- Prefer a scoped candidate that can be compared with the baseline. Identify
  which nearby surfaces belong to the torso or limb before redistributing
  influence; preserve a gradual joint transition and protect unrelated regions.
- For weight edits or procedural repair, read [skin-weight repair][link-1].
  Avoid replacing the whole binding with automatic weights merely because a
  local defect exists.
- Move a rest joint only when the evidence identifies a pivot problem.
  Revalidate the bind/rest relationship and affected animations after that
  change; do not force mirrored joints onto an asymmetric mesh.
- Keep changes outside the requested repair explicit. Check the appropriate
  invariants, such as rest geometry, materials, action curves, or unaffected
  contact behavior, instead of requiring every property to stay unchanged for
  every kind of repair.

## Verify and deliver

- Check finite evaluated coordinates, weight normalization, missing bone
  references, intended influence limits, and any protected channels. Edge
  stretch and collapsed-area metrics locate candidates for inspection; they do
  not prove tearing or visual acceptance.
- Recheck the affected pose range and existing animations on the combined
  result, including when separate patches overlap. Inspect the resulting images,
  not just whether rendering completed.
- Save and reopen the deliverable, verify dependencies and the intended active
  action, and tie evidence to its actual version or digest. Keep diagnostic
  actions separate from the production action set unless requested otherwise.
- Report structural checks, numerical scans, visual observations, and engine
  tests separately. State residual limitations and untested ranges. A Blender
  repair does not establish exported or engine-runtime correctness; perform
  those stages when requested.

[link-1]: references/skin-weight-repair.md
