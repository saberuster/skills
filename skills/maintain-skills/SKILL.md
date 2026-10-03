---
name: maintain-skills
description: List, install, update, or remove standalone agent skills through the Vercel Skills CLI. Use for installed-skill maintenance, not editing skill instructions or managing plugins.
---

# Maintain Skills

Use `npx skills` for standalone skill maintenance. Let the CLI handle package
files and source records; do not build another installer or registry.

## Establish the operation

- Determine the action, skill or source, target agents, and project or user
  scope from the request and conversation. Ask only for unresolved choices
  that change the operation; a clear request already authorizes that operation.
- Use the requested project as the working directory. Identify the available
  CLI version and read `npx skills --help` before choosing flags. The commands
  below are examples, not a substitute for the installed version's behavior.
  If Node.js or npx is unavailable, report the missing prerequisite.
- Inspect the selected scope with `list`, using JSON when supported. Identify
  skill paths, recorded sources, target agents, and resolved symlink or
  junction targets. A visible skill is not necessarily tracked for updates.
  Report missing provenance rather than guessing a repository from its name.

## Choose the command

| Request | Command example |
| --- | --- |
| List project skills | `npx skills list --json` |
| List user skills for Codex | `npx skills list -g --agent codex --json` |
| Inspect skills offered by a source | `npx skills add <source> --list` |
| Install a selected project skill | `npx skills add <source> --skill <name> --agent codex` |
| Install a selected user skill | `npx skills add <source> --skill <name> --agent codex -g` |
| Update one project skill | `npx skills update <name> -p` |
| Update one user skill | `npx skills update <name> -g` |
| Update all user skills | `npx skills update -g` |
| Remove a user skill from Codex | `npx skills remove <name> --agent codex -g` |

For project removal, run from that project and omit `-g`. Pass multiple names
or agents only when requested and supported by that command. Preserve an
explicit copy-versus-link preference using the CLI's supported install option.
Use `-y` only when its effects stay within the established request. Do not use
`--all` to resolve ambiguity or to recover from a failed selective operation.

### Install

Select the requested skill rather than installing an entire repository by
default. Check same-name destinations before replacement. Existing local work
or a link into an authored repository needs a concrete conflict decision; do
not overwrite it merely because the installation command permits replacement.
Use a supplied source or the CLI's search when the source is unresolved.

### Update

Update only skills with sufficient source records, within the requested scope.
Keep unknown-source skills unchanged and explain what information is missing.
Respect pinned revisions and project installation rules; do not silently replace
a requested revision with the source's latest branch.

Before replacement, check for local edits against a recorded baseline when one
is available. An upstream hash in a lock file alone does not prove the installed
files are unchanged. If local edits exist or cannot be distinguished from
upstream changes, preserve the files and resolve that uncertainty before
overwriting. Do not reset or pull a linked source checkout as a shortcut.

Check how the available version reinstalls updated packages, including agent
selection and copy-versus-link behavior. An update may use install defaults
rather than retain the original choices. Establish that it can preserve the
requested targets and installation method before running it; otherwise explain
the limitation and resolve the choice instead of silently changing the layout.

Account for shared directories and links: updating one package may affect
several agents. The currently documented update flags select names and
project/user scope, not an agent. If the user requires one agent only, do not
silently broaden the update or invent `update --agent`; explain the actual
shared targets and obtain a choice if the requested isolation is unsupported.

Treat "check for updates" as read-only. Do not use `update` as a probe. In the
upstream implementation reviewed for this skill, `check` routes to `update`
and can write; there is no documented update `--dry-run`. Unless the available
version provides a verified read-only path, report that limitation. Do not
pass guessed flags, including subcommand help flags that may be ignored.

### Remove

Use the CLI's removal operation with explicit names, agents, and scope where
supported. Inspect shared paths before claiming removal is isolated to one
agent. Preserve packages still needed by other agents. If the CLI cannot honor
the requested scope, explain the limitation instead of deleting directories
manually. Treat plugin-owned skills and host-bundled system skills as outside
this standalone workflow.

## Verify and report

Read back the relevant inventory and, for mutations, check affected paths and
available source records. Verify the requested selection and scope, including
whether shared installations remain intact. Do not infer success solely from
an exit code, or claim that file installation proves the current chat loaded it.

Report what succeeded, failed, or was skipped, with the affected scope and any
remaining action. After partial failure, inspect the resulting state before a
targeted retry; do not repeatedly rerun the whole batch. Never report a rollback
or restoration unless it was performed and verified.

## Boundaries and references

This skill covers standalone installations through the existing CLI. Plugin
lifecycle management, skill-content authoring, scheduled updates, and a new
declarative synchronization format are separate tasks.

Consult the [Skills CLI documentation](https://github.com/vercel-labs/skills)
for supported operations. For ambiguous update behavior, inspect the matching
version of [CLI routing](https://github.com/vercel-labs/skills/blob/main/src/cli.ts)
and [update logic](https://github.com/vercel-labs/skills/blob/main/src/update.ts).
The linked `main` branch can differ from the installed release.
