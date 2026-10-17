# Curated Skills

This is the selection shipped with `setup-godot-skills`, not an inventory of all
upstream offerings. Install complete skill directories from the exact sources
below. Default refs track `main`; retain explicit user pins or source choices.
Recheck upstream contents and dependencies before installation or update.

| Skill and source directory | Include when | Purpose and boundary |
| --- | --- | --- |
| [game-development-best-practices](https://github.com/saberuster/agent-skills/tree/main/skills/game-development-best-practices) | A Godot game project exists or is explicitly planned. | Engine-independent ownership, architecture, input, assets, and validation. Includes four references and UI metadata; it does not supply Godot API or editor tooling. |
| [csharp-refactoring](https://github.com/dotnet/skills/tree/main/plugins/dotnet/skills/csharp-refactoring) | The selected Godot project uses C#, or the user explicitly intends C#. | Behavior-preserving C# refactoring. Include `references/operation-catalog.md`. Symbol-aware tools are preferred; the skill documents fallbacks. Installing it does not install a C# LSP. |
| [testability-obstacle](https://github.com/dotnet/skills/tree/main/plugins/dotnet-test/skills/testability-obstacle) | C# is selected and a compatible .NET unit-test project already exists. | Minimal seams for deterministic tests of ordinary C# logic. Check framework support for its time/testing APIs. Existing tests avoid the mandatory external scaffolding handoff used when no test project exists. |
| [test-gap-analysis](https://github.com/dotnet/skills/tree/main/plugins/dotnet-test/skills/test-gap-analysis) | C# is selected and relevant existing tests have identifiable discovery/assertion semantics. | Analyze behavioral gaps in existing tests. Include `references/mutation-catalog.md`. New-suite creation and unclear test semantics route to other upstream skills, outside this selection. |

The last two entries are for an existing test setup. An intention to add tests
does not by itself satisfy their prerequisites; report them as not yet
applicable. User intent can establish the project's language before files exist.
Tests belonging only to vendored code, caches, or unrelated tools do not
qualify.

## Compatibility and provenance

`game-development-best-practices` is maintained in `saberuster/agent-skills`.
The three C#/.NET entries come from the [.NET team's
repository](https://github.com/dotnet/skills),
which supports [individual skill
installation](https://github.com/dotnet/skills#individual-skills).
Their location inside `plugins/` does not request plugin installation. Required
files must stay within the selected skill folder; conditional handoffs do not
authorize installing sibling skills or tools automatically.

The C# skills supplement project-specific Godot rules. During selection, flag
conflicts with engine callbacks, scene/Resource serialization, or node ownership
and lifetime. Their language/test guidance does not establish Godot runtime or
visual validation. Preserve upstream skill contents rather than editing the
installed copy to conceal a dependency or compatibility problem.

Source inspection on 2026-10-08 used `dotnet/skills` revision
`0608d8924cd3173411e36650a7a01b4063e1f55a`. This is a research snapshot, not an
installation pin or proof that a later upstream revision has the same contract.
The collection's five Godot authoring and diagnostic skills
(`godot-best-practices`, `godot-scripting`,
`godot-scene-and-resource-authoring`, `godot-ui-authoring`, and
`godot-build-and-diagnostics`), SDK provisioning, plugin runtimes, and unrelated
workflow skills are outside this initial selection. Expand the catalog through a
separate
maintenance request, or honor explicitly named additions in the current request
without silently rewriting the shipped catalog.
