# Skin-Weight Repair

Read this when changing weights or writing a procedural repair. Choose masks,
falloffs, and acceptance poses for the actual character; this is not a universal
rebinding recipe.

## Surface ownership and transitions

- Removing a distant bone's influence can expose a hard boundary at the pelvis
  or axilla. Inspect the transition under moderate bending as well as the
  extreme pose; keep appropriate parent/child blending instead of cutting
  weights at a fixed height.
- Nearby limbs can contaminate a spatial mask. Combine geometry with existing
  influence membership and, where useful, surface adjacency. Freeze unrelated
  areas such as cuffs, fingers, or previously validated contact regions, and
  check the combined result after overlapping edits.
- For vertices confirmed to represent attribute splits on the same continuous
  surface, keep weights consistent without welding geometry or changing UVs.
  Coincident points on separate layers, accessories, or disconnected surfaces
  are not automatically equivalent.
- Reassign removed mass only to bones justified by that surface's anatomy. Lock
  unrelated channels explicitly when a patch must preserve their behavior.

## Final constraints matter

- Normalization and per-vertex influence pruning can undo a change bound, alter
  locked channels, or create abrupt differences between neighbors. Validate the
  final assigned weights after every such step, including across seams and patch
  boundaries.
- Obtain the influence budget from the requested export/runtime contract. Do not
  hard-code a fixed count or silently prune a smoother binding to an assumed
  limit.
- In an Adam-based optimizer, constant per-vertex gradient scaling can largely
  cancel between the first and second moments. Multiplying gradients by a mask
  is not a guarantee of a tapered final edit. Inspect actual output deltas and
  support sets; do not infer locality from the optimizer's input mask.
- Clipping weights and then renormalizing does not guarantee that the clipped
  bounds still hold. Adding unrelated bone channels and pruning them later can
  also introduce discontinuities. These are failure checks, not a recommendation
  to build an optimizer; accept any candidate only after pose and regression
  evidence.

## Blender execution and reference data

- Inspect the installed Blender version and available action/slot APIs before
  scripting. When sampling, ensure the intended action and slot are active and
  account for NLA blending; restore state that the task is meant to preserve.
- For background Python, use `--python-exit-code 1` before `--python` and
  inspect diagnostics, expected outputs, and a saved-file reopen. A process exit
  code alone is not a completed validation. Prefer a separate background process
  when an interactive scene contains unrelated unsaved work.
- Compare authored values and actual dependencies rather than transient
  datablock identifiers such as session UIDs. A hash difference caused only by a
  runtime identifier is not an asset regression.
- Appending a reference mesh can also load rig, action, and material
  dependencies. Track which datablocks were newly loaded and remove only
  temporary dependencies that are no longer used; check that the delivered
  object and action sets remain intentional.
- If Blender rejects appending from the currently open file, use a separate
  working copy or explicit reference input. Preserve the reference, and verify
  that rerunning the repair reconstructs the intended result when a generator is
  part of the delivery.
