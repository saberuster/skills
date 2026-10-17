# Godot 4 Asset Editing

Read for editing/reviewing scenes, Resources, imported assets, import metadata,
caches, or project settings.

## Choose the Most Robust Editing Path

Direct text editing is suitable for `.gd`, `.cs`, ordinary docs/configuration,
and small local `.tscn`/`.tres` edits whose target properties and final diff are
clear.

Prefer Godot APIs for scene-tree/node-ownership changes; signal connections,
exported Resource references, `ext_resource`, `sub_resource`, animations, or
bulk rewrites; and changes requiring editor context, import refresh, or Godot
serialization.

Choose headless GDScript, `EditorScript`, tool scripts, Godot C# tool code, or
editor operations from project language and required context.

## Do Not Hand-Edit Fragile Outputs

- Do not hand-edit `.res`, `.scn`, imported binaries, generated `.godot/`
  caches, or import outputs.
- Edit `.import`/`project.godot` only for narrow, semantically clear changes,
  then validate through Godot/editor.
- Preserve UIDs, resource IDs, node paths, section order, signal semantics, node
  ownership, and external/internal Resource relationships in text
  scenes/Resources.
- When these relationships are unclear, use Godot APIs rather than guessing.

## Validation Expectations

- Run editor/import checks after scene, Resource, export, or project-setting
  changes.
- Use Godot API saves/editor resaves when serialized IDs, ownership, references,
  animations, or connections may be affected.
- Inspect final diffs for unintended rewrites, section reordering, UID churn,
  and unrelated import changes.

## Generated Asset Pipelines

Use ownership ledgers, staging, failure recovery, and obsolete-output cleanup
contracts. File-based Godot manifests also record required UIDs and reject
duplicate logical IDs, paths, and UIDs.

Treat generation/migration as a staged transaction, publishing in this order:

1. Generate source files within staging boundaries.
2. Wait for complete Godot import.
3. Generate project-owned Godot Resources.
4. Wait again for import/serialization refresh.
5. Verify actual loading, UIDs, and references.
6. Perform project-declared determinism checks.
7. Update consumer references.
8. Confirm obsolete outputs have zero references.
9. Delete only old outputs proven owned by this generator's ledger.

Retain the previous valid result until loading, references, determinism, and
consumer checks pass. Stop publication at any failure; do not update consumers
early, overwrite authored inputs, or delete old assets.

Prefer the project-version editor/tool scripts and `ResourceSaver` for
`.tres`/`.tscn` generation. If external text generation is required, pin the
minor-version structure, ordering, encoding, and persistent logical-ID-to-UID
mapping, then round-trip supported Resources through the matching editor.

Require a second-run zero diff only for stable text serialization or
project-declared deterministic outputs. For editor resaves/unstable
serialization, compare output sets, reference graphs, loading, and runtime
semantics rather than bytes.

Names/ownership must not exist only in README prose. Generators/validators must
mechanically check applicable names, persistent logical IDs, paths, UIDs,
Resource references, manifest ownership, and zero references to obsolete
outputs. Fail explicitly on duplicates, missing/conflicting data, unauthorized
overwrites, or obsolete outputs still referenced by consumers. Project sources
of truth define concrete names, logical IDs, and directories; do not hardcode
them into this general skill.

## Editor-Owned Graph Resources

Modify `VisualShader`, `Animation`, `AnimationLibrary`, and other graph/track
Resources through the matching editor/APIs and save with `ResourceSaver`. Do not
construct/patch their serialization with raw string concatenation.

## Multi-File Third-Party Assets

Use a project-owned typed adapter Resource when runtime code needs typed Godot
references, Inspector assignment, or compatibility/version validation. Otherwise
use importers, manifests, PackedScenes, or equivalent project-owned contracts.

Validate required files, reference types, and supported versions during
generation/import; fail explicitly for missing/incompatible data. Runtime code
must not infer related files from adjacent directories or filename conventions.
