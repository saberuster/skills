# Skills

Focused standalone agent skills by saberuster, licensed under the
[MIT License](LICENSE). Use them to maintain project instructions and installed
skills, learn from a session, and write technical documentation.

## Available skills

Open a skill's README for its purpose, requirements, installation, updates, and
usage examples. The status columns report discovery and loading with the tested
clients; see [Validation and compatibility](#validation-and-compatibility) for
the coverage limits.

<!-- agent-support:start -->

| Skill | Codex | Claude Code |
| --- | --- | --- |
| [learn-from-session](skills/learn-from-session/README.md) | &#9989; | &#9989; |
| [maintain-agents-md](skills/maintain-agents-md/README.md) | &#9989; | &#9989; |
| [maintain-skills](skills/maintain-skills/README.md) | &#9989; | &#9989; |
| [technical-docs](skills/technical-docs/README.md) | &#9989; | &#9989; |

&#9989; discovery passed; &#10060; discovery failed; &mdash; unknown.
Channel: `pinned`. Versions:
Codex `codex-cli 0.161.0`; Claude Code `2.1.292 (Claude Code)`.
Tested source commit: `0aefd09e4a5c97360dcf2a7b4bf7bcd781a4bef1`.
Evidence: [CI run](https://github.com/saberuster/skills/actions/runs/37757752378).

<!-- agent-support:end -->

## Get started

1. Choose a skill from the table and read its requirements.
2. Use that skill's installation prompt to select a revision, client, and scope.
3. Follow its usage examples after confirming discovery in a fresh session.

Skills are installed individually from `skills/<name>/`. Each folder contains
its human-facing `README.md`, agent instructions in `SKILL.md`, metadata, and
any supporting resources. Repository development dependencies are not needed to
use the skills. The [shared installation protocol](docs/installation.md)
covers destinations, source tracking, and preserving local edits.

## Validation and compatibility

CI checks every skill with Codex and Claude Code in isolated temporary projects,
without sending model prompts. The table shows the latest matching results for
the pinned clients. A default-branch push, including a merged PR, reruns the
checks and refreshes the table with a bot commit; branch and PR runs publish
previews. Weekly runs also check the latest published clients separately.

Discovery does not validate task behavior, external tools, installation, or
invocation-policy parity. Each skill's README explains its own dependencies and
limits. See [Development and validation](docs/development.md) for CI failure
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
exercise separately; passing static checks does not validate agent decisions.

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
