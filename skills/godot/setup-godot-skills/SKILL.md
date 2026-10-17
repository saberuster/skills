---
name: setup-godot-skills
description: Set up or refresh curated standalone agent skills for Godot projects. Select applicable skills from multiple sources, installing missing skills and updating existing ones on every run.
---

# Setup Godot Skills

Maintain the applicable selection from [catalog.md](references/catalog.md).
Every setup run does both: fill missing skills and refresh existing skills.
A setup request authorizes these operations within its scope; an inspection or
recommendation request remains read-only.

## Establish the target

- Default to the current Git repository or worktree root and the current agent
  client. Respect explicit directory, scope, and client overrides. If there is
  no repository or the client is unknown, resolve the target with the user;
  never silently fall back to a user-wide installation.
- Keep the installation root separate from the Godot project directory. Locate
  the relevant `project.godot` and language/test configuration. For multiple
  projects, use the user's selected project or agreed combined requirements;
  ask when the selection changes which skills apply.
- Explicit plans, such as starting a C# Godot project, take precedence over
  absent files in a new repository. Otherwise use project evidence, excluding
  generated caches and vendored examples. Ask only about unresolved conditions
  needed to select skills; do not launch Godot or install an SDK to detect them.

## Select the skills

Read the catalog shipped with this loaded skill, then apply project conditions,
explicit user selections, repository exclusions, and this-run skips. Do not
discover and add new upstream skills automatically or update this setup skill
in the middle of a run.

- Use one identified source and ref per skill. Honor user pins and source
  overrides; a conflicting installed source requires a user decision.
- A missing skill that remains selected must be installed even on a repeat run.
  Deleting its directory is not an exclusion.
- A one-time skip expires after this run. When the user requests a lasting
  exclusion, record its skill name and scope in the repository's effective
  project instructions, preserving other content. Use an existing convention,
  or create the appropriate client-readable instruction file if needed. Keep
  installation provenance in the installer's records, not a second registry.
- Respect lasting exclusions until the user explicitly re-enables the item.
  An ambiguous request that contradicts an exclusion needs clarification.
- Skills outside this run's selection remain unchanged, including skills that
  no longer match project conditions. Report formerly applicable items without
  automatically removing or updating them.

## Reconcile every selected item

Follow [installation.md](references/installation.md) for source inspection,
installation, update mechanics, and verification. Default to full-directory
copies. Check actual destinations as well as installer records.

| Observed state | Action |
| --- | --- |
| Entire destination absent and no source or shared-path conflict | Install the selected skill, even if a stale installation record exists. |
| Existing copy matches its recorded baseline and selected source | Check upstream; update if changed, otherwise report current. |
| Different source, local edits, missing internal files, uncertain baseline, or incompatible shared destination | Preserve it, explain the conflict, and wait for the user's choice for this item. |
| Upstream unavailable, removed, or incompatible | Preserve any existing copy and report the unresolved item; do not label it current. |

For a conflict, identify the destination, existing and requested sources, and
the concrete difference. Offer relevant choices such as keep for this run,
exclude persistently, or replace from the selected source. Replace only after
the user chooses it. Continue independent, nonconflicting items meanwhile;
do not classify an ordinary unmodified older version as a conflict.

## Verify and report

Read back destinations, complete package contents, and source records after
mutations. Report the target root/client and each item's installed, updated,
current, skipped, conflict, or failed status with a reason. Partial failure is
not completion; re-inspect state before retrying only affected operations.
File installation does not establish discovery or loading in the current chat.

This skill manages standalone skills. Its catalog excludes the five Godot
authoring and diagnostic skills in this collection: `godot-best-practices`,
`godot-scripting`, `godot-scene-and-resource-authoring`, `godot-ui-authoring`,
and `godot-build-and-diagnostics`. It does not install plugins, change game
code, provision runtimes, or remove skills.
For maintenance evaluation, see [acceptance cases](evals/cases.md); those cases
are not instructions to execute during ordinary setup.
