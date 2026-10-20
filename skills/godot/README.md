# Godot skills

Each leaf directory is an independent skill package:

- [Godot Project Grounding](godot-best-practices/SKILL.md) establishes project
  and version evidence and coordinates project-wide reviews or refactor plans.
- [Godot Scripting](godot-scripting/SKILL.md) handles GDScript, Godot C#,
  lifecycle, signals, input, and runtime interactions.
- [Godot Scenes and Resources](godot-scene-and-resource-authoring/SKILL.md)
  handles scenes, Nodes, Resources, imports, settings, and serialization.
- [Godot TileSet](godot-tileset/SKILL.md) handles tile atlases, placement
  footprints, editable map layers, and source-bound scene validation.
- [Godot UI Authoring](godot-ui-authoring/SKILL.md) handles native layouts,
  themes, combined control states, reusable components, and UI showcases.
- [Godot Build and Diagnostics](godot-build-and-diagnostics/SKILL.md) handles
  supervised builds, imports, runs, fresh logs, and validation evidence.
- [Setup Godot Skills](setup-godot-skills/SKILL.md) installs missing and
  refreshes existing items from its curated standalone skill catalog.

Install individual leaf packages through the repository's
[installation workflow](../meta/maintain-skills/SKILL.md), selecting the
requested client and scope. Keep the full leaf directory, including metadata,
references, and any scripts. The development skills cooperate by skill
name and retain standalone fallbacks. Engine-independent
`game-development-best-practices` is optional for relevant gameplay work.

The setup skill retains its separate
[curated catalog](setup-godot-skills/references/catalog.md). Moving the packages
into one collection does not add the development skills to that catalog;
install those only when explicitly selected. The setup skill does not install
plugins or runtimes.

## Runtime requirements

Builds and runs require the project's matching Godot executable; C# projects
also require a matching Godot .NET build and .NET SDK. Static reviews do not
require an engine launch.

Runner and log-preflight helpers live in
`skills/godot/godot-build-and-diagnostics/scripts/` from the repository root:
keep `invoke_godot.ps1` and `prepare_godot_log.ps1` together. Update external
callers that still use the old plugin or top-level skill paths. The runner
requires PowerShell 7.2+ and supports Windows and Linux; Linux additionally
requires kernel 5.3+ and x64 or ARM64. Other hosts need an existing equivalent
supervisor under the skill's validation contract.

Read [Validation](godot-build-and-diagnostics/references/validation.md)
before project commands, and read the
[Runner Contract](godot-build-and-diagnostics/references/runner-contract.md)
when integrating or diagnosing supervision.

## Source and validation

This collection is the maintained source for the packages migrated from
`saberuster/agent-skills`: `skills/godot/setup-godot-skills/` and the five
packages formerly under `plugins/godot-dev/skills/`. These are standalone skill
packages; plugin manifests are not part of this collection. The migration
preserves skill IDs, workflows, and script behavior. Any historical plugin
validation applies only to its recorded source snapshot.

From this repository root, use its development environment for the packaging,
documentation, and isolated Godot helper regression checks:

```console
python -m unittest discover -s tests -p test_godot_build_regressions.py -v
```

See the [TileSet behavior cases](../../examples/godot-tileset.md) for isolated
planning trials; these do not execute an editor or game.

Repository checks do not establish client discovery, automatic skill selection,
or real Godot execution. Those checks, C# builds, GUI/input behavior, and visual
or gameplay acceptance require separate evidence for the actual project and
host.
