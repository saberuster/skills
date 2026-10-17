# Godot 4 Project Hygiene

Use for layout, naming, third-party assets, line endings, generated files, UIDs,
and version control.

## Organization and Naming

- Keep assets near consuming scenes/features unless the repo already has a
  coherent shared library.
- Preserve consistent local conventions first. Naming-only changes need concrete
  readability, navigation, tooling, or boundary benefits.
- Without repo conventions, use Godot fallbacks: `snake_case` for directories,
  most files, and Resources; `PascalCase` for nodes and C# files/types.
- Keep third-party provenance identifiable, usually in `addons/` unless
  deliberately feature-local.
- Prefer text scenes/Resources when merge friendliness matters.
- Names expose responsibility, lifetime, and boundaries; avoid ambiguous shared
  names for node wrappers, domain models, persistence payloads, UI controls, and
  input intents.
- Consistent C#-first layouts such as `src/Core` and local prefix/suffix
  vocabulary are project contracts, not universal Godot rules.

## Version Control and UIDs

- Use version-matched version-control, export, and UID guidance.
- Ignore generated `.godot/` caches/binary import outputs according to the
  relevant version.
- Separate authored inputs, unchanged third-party raw inputs, and generated
  outputs to expose ownership; generators must not overwrite the first two.
- If generated outputs are intentionally tracked, commit their manifests too;
  generator-owned roots reject hand edits.
- Commit companion `.uid` files only where required by the format/minor version;
  let Godot create them instead of hand-writing or independently regenerating
  them.
- Handle companion `.uid` files when moving/deleting sources. Generator
  manifests record source-to-UID mappings and reject missing, orphaned, or
  conflicting UIDs.

## Common Risks

- Accidentally tracked generated caches/import outputs.
- Mixed ownership of authored/raw/generated content or hand patches in generated
  directories.
- Required UIDs ignored, missing, orphaned, hand-written, or absent from
  manifests.
- Naming changes replacing coherent local conventions without measurable
  benefit.
- Broad `Manager`, `Helper`, or `Extensions` names hiding unclear ownership.
- Runtime types taking on save/network payload responsibilities.
- Node-script prefixes no longer matching node lifetime/scene ownership.
