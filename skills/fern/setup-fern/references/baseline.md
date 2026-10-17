# Fern Baseline

This is the curated general environment selected by `setup-fern`. Directory
selection defines the required skills; the available leaf packages come from
the selected source snapshot. Do not replace these selectors with a maintained
list of individual skill names.

## Sources and selection

| Source | Tracked branch | Selection | Policy |
| --- | --- | --- | --- |
| `saberuster/skills` | `main` | All leaf packages in `skills/fern/` and `skills/meta/` | Required |
| `saberuster/skills` | Same snapshot | Other skill directories requested for the project | Optional |
| `cli/cli` | `trunk` | Only `skills/gh/` | Required external skill |
| Codex host | Host managed | `skill-creator`, `openai-docs` | Availability check only |

Do not select `gh-fix-ci` or `gh-address-comments`. Do not install other skills
from `cli/cli` merely because the source contains them. External skills are
selected individually; the directory rule applies to the user's own source.

Resolve each tracked branch once at the beginning of a run. Record its commit
SHA and use that immutable snapshot for discovery, installation, and resource
application throughout the run. Refresh branch resolution on the next run.
The resolved SHA is evidence of that run, not a permanent pin replacing the
tracked branch.

Discover every leaf containing `SKILL.md` under the required directories in the
resolved snapshot. Validate package names, duplicates, and package boundaries
before installation. An empty or missing required directory is a source error;
do not silently substitute the entire repository. Report leaves removed or
renamed upstream as migration candidates; directory membership does not
authorize automatic deletion of existing installations.

## Optional capabilities

Use project context to propose relevant directories outside Fern and Meta.
Install an optional directory when the request already selects it or the user
chooses it. Show the directory and discovered packages before acting when the
selection is unresolved. Do not infer that a project requires every specialty.
Use the same `saberuster/skills` snapshot for optional and required packages.

## Skill installation contract

Use `maintain-skills` for package files and source records. Select Codex, user
scope, and copied packages for the general environment unless the user requests
a different target. Inspect actual destinations and shared bindings before
replacement; a Codex entry can share files with another client.

For each own-source directory, use a source URL or explicit snapshot path that
preserves that directory boundary. Verify the available CLI's listing and
selection behavior before choosing flags. Where supported, selecting all leaves
uses `--skill '*'` with explicit `--agent codex`; `--all` can broaden client
selection and is unsuitable for this baseline. Quote `'*'` for the shell.

For `gh`, select its exact leaf name from the resolved `cli/cli` snapshot.
Record or verify the CLI's actual source provenance; do not maintain a parallel
skill lock file. If the CLI records only an immutable revision, state that fact
and let the next Fern run resolve the branch again. Do not claim that a generic
CLI update command will follow Fern's branch policy automatically.

### Bootstrap

When `maintain-skills` is unavailable, read its instructions directly from the
resolved Meta snapshot. Verify the existing Skills CLI version and supported
listing, Codex targeting, scope, and copy options. Use that protocol to install
the missing required packages. The bootstrap does not require a previously
installed copy of `maintain-skills` or a second installer implementation.

Keep the loaded orchestration instructions and resources available outside any
destination that will be replaced. Defer replacement of `setup-fern` and an
already installed `maintain-skills` until operations relying on their loaded
versions finish. Continue using the selected snapshot after replacement.

## Host and runtime checks

Check that the host exposes usable `skill-creator` and `openai-docs` skills.
Identify whether each entry is host managed or a standalone installation when
the source is visible. Do not install a second same-name copy to satisfy a
missing host capability. Report absence or uncertain provenance and the host
action needed; do not invent a repository fallback.

Check the host's support for standalone custom agent TOMLs, the selected
configuration keys, and the requested model identifiers before application.
Do not silently replace an unavailable model with another model. A missing
host capability can leave setup partial while independent compatible items
are completed. Report that limitation explicitly.

The [Codex installation procedure](codex-installation.md) covers the separate
agent, configuration, and instruction resources. Skill installation success,
resource readback, and discovery in a fresh Codex chat are separate evidence.

## Source evidence

These observations reuse the shared research inspected on 2026-10-17. The
branch links are mutable; verify the actual installed CLI when executing.

- [Vercel Skills README](https://github.com/vercel-labs/skills) and
  [discovery source](https://github.com/vercel-labs/skills/blob/main/src/skills.ts)
  support source subdirectories and leaf selection. Adopt directory discovery
  for own skills; keep explicit Codex targeting and check version behavior.
- [GitHub CLI skill](https://github.com/cli/cli/blob/trunk/skills/gh/SKILL.md)
  supplies the selected external skill. Track `trunk` and resolve one snapshot
  per run; the reference does not establish local installation success.
- [Codex custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents)
  document personal TOML discovery. Adopt ordinary copied agent files for a
  portable environment; validate host support separately from source parsing.

The sources support the design and selection mechanism. They do not prove that
an installation, model spawn, or new-chat discovery has run successfully.
