# Skills

Focused agent skills and a Codex plugin marketplace by saberuster, licensed under
the
[MIT License](LICENSE). Use them to maintain project instructions and installed
skills, reflect on a session, write technical documentation, review project
readiness for agent work, and work through ideas and decisions, or compose
structured GPT Image prompts from briefs and reference images, and prepare
Conventional Commits, model, reconstruct, and repair assets in Blender, and
develop and diagnose Godot projects.

[meta](skills/meta/README.md) groups skills for maintaining skills and project
instructions, configuring Codex, reviewing project readiness for agent work,
and finding open-source references for a specific or planned skill on request.
It includes
`maintain-skills`, `maintain-agents-md`, `agent-ready`, and
`find-skill-references`, plus [Codex Config](skills/meta/codex-config/SKILL.md)
for scoped configuration inspection, changes, and runtime verification.
Client discovery for new, renamed, and relocated packages remains unverified.

[fern](skills/fern/README.md) is a Codex plugin grouping personal workflows for
accomplishing
complex tasks with the simplest effective methods. It includes
[Fern](skills/fern/fern/SKILL.md) as an explicitly invoked entry for task
coordination and current-chat development through the authorized endpoint.
Fern owns implementation, validation, Git/PR/CI delivery, and final judgment
in the current main agent. Its bug fix, feature, and refactoring playbooks
provide task-specific methods with shared validation and delivery references.
The collection also includes
[Commit](skills/fern/commit/README.md), migrated from `git-commit`,
[Technical Writing](skills/fern/technical-writing/SKILL.md), migrated
from `technical-docs`, [Unslop](skills/fern/unslop/SKILL.md) for focused
language editing, [reflect](skills/fern/reflect/README.md), migrated from
`learn-from-session`, and
[Talk It Through](skills/fern/talk-it-through/README.md) for exploring ideas
and decisions. Discovery for `commit`, `reflect`, and the relocated
`talk-it-through` remains unverified; earlier results do not establish discovery
from these sources.

Fern is published in this repository and replaces the former Implement
procedure. Its pinned Codex and Claude Code
[discovery jobs](https://github.com/saberuster/skills/actions/runs/39066063246)
passed; discovery does not establish live setup or actual agent behavior.
Source changes do not update installed copies. Switch installed sources
through `maintain-skills` and the invocation from `$implement` to `$fern`
explicitly.

[Setup Fern](skills/fern/setup-fern/SKILL.md) applies bundled Codex resources
to a project: six custom agents, selected configuration values and complete
user instructions. Its Python installer merges `.codex/config.toml`, copies
`.codex/agents/` and manages a block in the root `AGENTS.md`. The same command
works locally and in Codex Cloud; it does not install skills. See
[installer usage](skills/fern/setup-fern/references/installation.md).

[Image generation](skills/image-generation/README.md) groups the three GPT Image
prompting skills.

[Deep Search](skills/fern/deep-search/SKILL.md), in the Fern collection, plans
source coverage before multi-round retrieval. Exa handles broad discovery;
OpenAI Docs, GitHub, and X use specialist routes, and Parallel fills assessed
gaps. Known substantive pages prefer Exa content when needed; GitHub files use
native tools then built-in raw reads, never Exa content. X uses native tools,
usable local Grok Build, then the host model's default search. It hands off
traceable evidence and coverage gaps in a caller-accessible package, using a
unique system temporary directory unless an output location is supplied.
Analysis stays with the calling task. In Codex, invoke `$deep-search`
explicitly; implicit selection is disabled.
A standalone skill cannot enforce tool-call ordering. Source creation does not
install it or establish client discovery.
See the [synthetic cases](examples/deep-search.md) for its behavior
boundaries.

[Blender](skills/blender/README.md) groups `blender-low-poly`, `character-rig`,
and `reference-scene`, migrated from `saberuster/agent-skills` with their
supporting resources and regression tests. Blender operations require a Blender
installation or a connected Blender tool. Client discovery from this repository
remains unverified.

[Godot](skills/godot/README.md) groups `setup-godot-skills` and the five former
`godot-dev` skills from `saberuster/agent-skills`, including their references,
build helpers, and isolated regressions. Each skill is independently installable.
The setup skill keeps its existing curated selection; grouping these packages
does not add the other five skills to that selection. Client discovery from the
relocated sources remains unverified.

## Available skills

Open the linked README or skill instructions for its purpose and requirements.
The status columns report discovery and loading with the tested
clients; see [Validation and compatibility](#validation-and-compatibility) for
the coverage limits.

<!-- agent-support:start -->

| Skill | Codex | Claude Code |
| --- | --- | --- |
| [agent-ready](skills/meta/agent-ready/README.md) | &#9989; | &#9989; |
| [blender-low-poly](skills/blender/blender-low-poly/SKILL.md) | &#9989; | &#9989; |
| [brief-to-image-prompt](skills/image-generation/brief-to-image-prompt/README.md) | &#9989; | &#9989; |
| [character-rig](skills/blender/character-rig/SKILL.md) | &#9989; | &#9989; |
| [codex-config](skills/meta/codex-config/SKILL.md) | &mdash; | &mdash; |
| [commit](skills/fern/commit/README.md) | &#9989; | &#9989; |
| [find-skill-references](skills/meta/find-skill-references/README.md) | &#9989; | &#9989; |
| [godot-best-practices](skills/godot/godot-best-practices/SKILL.md) | &#9989; | &#9989; |
| [godot-build-and-diagnostics](skills/godot/godot-build-and-diagnostics/SKILL.md) | &#9989; | &#9989; |
| [godot-scene-and-resource-authoring](skills/godot/godot-scene-and-resource-authoring/SKILL.md) | &#9989; | &#9989; |
| [godot-scripting](skills/godot/godot-scripting/SKILL.md) | &#9989; | &#9989; |
| [godot-ui-authoring](skills/godot/godot-ui-authoring/SKILL.md) | &#9989; | &#9989; |
| [gpt-image-prompting](skills/image-generation/gpt-image-prompting/README.md) | &#9989; | &#9989; |
| [image-to-prompt](skills/image-generation/image-to-prompt/README.md) | &#9989; | &#9989; |
| [maintain-agents-md](skills/meta/maintain-agents-md/README.md) | &#9989; | &#9989; |
| [maintain-skills](skills/meta/maintain-skills/README.md) | &#9989; | &#9989; |
| [reference-scene](skills/blender/reference-scene/SKILL.md) | &#9989; | &#9989; |
| [reflect](skills/fern/reflect/README.md) | &#9989; | &#9989; |
| [setup-fern](skills/fern/setup-fern/SKILL.md) | &#9989; | &#9989; |
| [setup-godot-skills](skills/godot/setup-godot-skills/SKILL.md) | &#9989; | &#9989; |
| [talk-it-through](skills/fern/talk-it-through/README.md) | &#9989; | &#9989; |
| [technical-writing](skills/fern/technical-writing/SKILL.md) | &#9989; | &#9989; |
| [unslop](skills/fern/unslop/SKILL.md) | &#9989; | &#9989; |

&#9989; discovery passed; &#10060; discovery failed; &mdash; unknown.
Channel: `pinned`. Versions:
Codex `codex-cli 0.161.0`; Claude Code `2.1.292 (Claude Code)`.
Tested source commit: `b65f4873cca34527c7c282139783cafb62e5d88f`.
Evidence: [CI run](https://github.com/saberuster/skills/actions/runs/39043119042).

<!-- agent-support:end -->

## Get started

For the complete Fern workflow, use the
[Codex marketplace](docs/plugins.md). Its plugin installs the eight Fern skills
from their maintained source directories. Individual skills remain available
through the standalone installation protocol below.

1. Choose a skill from the table and read its requirements.
2. Use the [installation protocol](docs/installation.md) to select a revision,
   client, scope, and the source directory linked in the catalog.
3. Follow its usage examples after confirming discovery in a fresh session.

Skills are installed individually from their source folder, usually
`skills/<name>/` or `skills/<collection>/<name>/`. Each skill folder contains
agent instructions in `SKILL.md`, metadata, and any supporting resources;
some also include a human-facing `README.md`. Development dependencies are not
needed to use the skills. The [shared installation protocol](docs/installation.md)
covers destinations, source tracking, and preserving local edits.

## Validation and compatibility

The agent support CI checks every skill with Codex and Claude Code in isolated
temporary projects without sending model prompts. The table shows the latest
matching discovery results for the pinned clients. A default-branch push,
including a merged PR, reruns those checks and refreshes the table with a bot
commit; branch and PR runs publish previews. Weekly runs also check the latest
published clients separately.

Discovery does not validate task behavior, external tools, installation, or
invocation-policy parity. Each skill's documentation explains its dependencies
and limits. See [Development and validation](docs/development.md) for CI failure
handling, evidence rules, client versions, and local discovery commands.

All repository validation uses three
[layers](docs/validation.md): deterministic PR checks, affected runtime and
agent checks, and full scheduled/manual/release checks. On a user machine,
run the unified Docker launcher; repository automation uses CI. Real agent
execution is explicit and retains traces, file assertions and independent
assessments. A no-model run reports planned behavior as not run. Skills without
executable cases and native/manual acceptance remain visible coverage gaps.
PR and full CI also run all non-engine regressions on a fresh Windows runner,
with explicit POSIX/Linux exclusions and required junction/symlink checks.
Workflow configuration does not establish a hosted pass.

## Development

Use Python 3.11 or later and Node.js 22 or later; CI uses Node.js 24. From the
repository root, create an isolated environment and install pinned dependencies:

```text
python -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
npm ci
```

On Windows, replace `.venv/bin/python` with `.venv\Scripts\python.exe` in all
commands. Activation is not required. These environments support editing and
focused script debugging. Run user-machine validation through Docker:

```text
python scripts/run_validation.py --layer pr --output /tmp/skills-pr-001
```

Use a fresh absolute output path outside the checkout and real client profiles;
on Windows, substitute a writable temporary path. See the
[validation guide](docs/validation.md) for prerequisites, affected/full layers,
check selection, actual agent execution and CI triggers.

Follow [AGENTS.md](AGENTS.md) for contribution rules. The
[development guide](docs/development.md) explains formatting and discovery
implementation. [Synthetic cases](examples/) describe behavioral expectations to
exercise separately with the [behavior check guide](docs/behavior-checks.md);
passing static checks does not validate agent decisions.

## Releases

The initial public release is `v0.1.0`. It starts a new version history for
this repository. Tags version the whole repository;
[CHANGELOG.md](CHANGELOG.md) records user-visible changes. Before 1.0, changes
to task scope or instruction behavior increment the minor version; compatible
corrections increment the patch version. There is no separate skill version
file. The Fern plugin has its own SemVer version in
[`skills/fern/.codex-plugin/plugin.json`](skills/fern/.codex-plugin/plugin.json).
Bump that version when shipping changes to any bundled skill or plugin metadata;
see the [plugin maintenance rules](docs/plugins.md#maintenance-and-releases).

## License

Copyright (c) 2026 saberuster. See [LICENSE](LICENSE). External documentation
is linked for reference and is not included in this repository's license grant.
Development dependencies retain their own licenses.
