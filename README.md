# Skills

Focused standalone agent skills by saberuster, licensed under the
[MIT License](LICENSE). Use them to maintain project instructions and installed
skills, reflect on a session, write technical documentation, review project
readiness for agent work, and work through ideas and decisions, or compose
structured GPT Image prompts from briefs and reference images, and prepare
Conventional Commits.

[meta](skills/meta/README.md) groups skills for maintaining skills and project
instructions, reviewing project readiness for agent work, and grounding skill
creation, editing, and review in inspected open-source examples. It includes
`maintain-skills`, `maintain-agents-md`, `agent-ready`, and
`research-skill-patterns`. Client discovery for the relocated packages remains
unverified.

[fern](skills/fern/README.md) groups personal workflows for accomplishing
complex tasks with the simplest effective methods. It includes
[Technical Writing](skills/fern/technical-writing/SKILL.md), migrated
from `technical-docs`, [Unslop](skills/fern/unslop/SKILL.md) for focused
language editing, and [reflect](skills/fern/reflect/README.md), migrated from
`learn-from-session`. Discovery for `reflect` remains unverified; its
predecessor's results do not establish discovery for the renamed package.

[Image generation](skills/image-generation/README.md) groups the three GPT Image
prompting skills.

[Thinking](skills/thinking/README.md) groups skills for exploring ideas,
clarifying questions, and working through decisions. It includes
`talk-it-through`; client discovery from its relocated source remains unverified.

## Available skills

Open the linked README or skill instructions for its purpose and requirements.
The status columns report discovery and loading with the tested
clients; see [Validation and compatibility](#validation-and-compatibility) for
the coverage limits.

<!-- agent-support:start -->

| Skill | Codex | Claude Code |
| --- | --- | --- |
| [agent-ready](skills/meta/agent-ready/README.md) | &mdash; | &mdash; |
| [brief-to-image-prompt](skills/image-generation/brief-to-image-prompt/README.md) | &#9989; | &#9989; |
| [git-commit](skills/git-commit/README.md) | &#9989; | &#9989; |
| [gpt-image-prompting](skills/image-generation/gpt-image-prompting/README.md) | &#9989; | &#9989; |
| [image-to-prompt](skills/image-generation/image-to-prompt/README.md) | &#9989; | &#9989; |
| [maintain-agents-md](skills/meta/maintain-agents-md/README.md) | &mdash; | &mdash; |
| [maintain-skills](skills/meta/maintain-skills/README.md) | &mdash; | &mdash; |
| [reflect](skills/fern/reflect/README.md) | &#9989; | &#9989; |
| [research-skill-patterns](skills/meta/research-skill-patterns/README.md) | &mdash; | &mdash; |
| [talk-it-through](skills/thinking/talk-it-through/README.md) | &#9989; | &#9989; |
| [technical-writing](skills/fern/technical-writing/SKILL.md) | &#9989; | &#9989; |
| [unslop](skills/fern/unslop/SKILL.md) | &#9989; | &#9989; |

&#9989; discovery passed; &#10060; discovery failed; &mdash; unknown.
Channel: `pinned`. Versions:
Codex `codex-cli 0.161.0`; Claude Code `2.1.292 (Claude Code)`.
Tested source commit: `389317b5161fc3a00d6cd7fea9e7f13a69b129cf`.
Evidence: [CI run](https://github.com/saberuster/skills/actions/runs/38963411239).

<!-- agent-support:end -->

## Get started

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

CI checks every skill with Codex and Claude Code in isolated temporary projects,
without sending model prompts. The table shows the latest matching results for
the pinned clients. A default-branch push, including a merged PR, reruns the
checks and refreshes the table with a bot commit; branch and PR runs publish
previews. Weekly runs also check the latest published clients separately.

Discovery does not validate task behavior, external tools, installation, or
invocation-policy parity. Each skill's documentation explains its dependencies
and limits. See [Development and validation](docs/development.md) for CI failure
handling, evidence rules, client versions, and local discovery commands.

## Development

Use Python 3.11 or later and Node.js 22 or later; CI uses Node.js 24. From the
repository root, create an isolated environment and install pinned dependencies:

```text
python -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
npm ci
```

On Windows, replace `.venv/bin/python` with `.venv\Scripts\python.exe` in all
commands. Activation is not required. Run the static checks:

```text
.venv/bin/python -m ruff check .
.venv/bin/python -m ruff format --check .
.venv/bin/python -m unittest discover -s tests -v
npm run lint:md
```

Follow [AGENTS.md](AGENTS.md) for contribution rules. The
[validation guide](docs/development.md) explains formatting and discovery
checks. [Synthetic cases](examples/) describe behavioral expectations to
exercise separately with the [behavior check guide](docs/behavior-checks.md);
passing static checks does not validate agent decisions.

## Releases

The initial public release is `v0.1.0`. It starts a new version history for
this repository. Tags version the whole repository;
[CHANGELOG.md](CHANGELOG.md) records user-visible changes. Before 1.0, changes
to task scope or instruction behavior increment the minor version; compatible
corrections increment the patch version. There is no separate skill version
file.

## License

Copyright (c) 2026 saberuster. See [LICENSE](LICENSE). External documentation
is linked for reference and is not included in this repository's license grant.
Development dependencies retain their own licenses.
