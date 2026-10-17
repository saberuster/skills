---
name: setup-fern
description: Set up, update, or check a curated personal Fern environment for Codex. Use to align Fern and meta skills, selected external skills, custom agents, configuration, and subagent instructions on a new or existing machine.
---

# Setup Fern

Align the user-level Codex environment with the maintained Fern baseline.
Use this workflow for an authorized setup, update, or read-only check; editing
this package alone does not authorize applying it to the current machine.

## Establish the baseline and target

1. Read [the baseline](references/baseline.md). Select every leaf skill in
   `skills/fern` and `skills/meta` from the declared source. Select additional
   directories only from the user's project needs or explicit choices. Keep
   external skills individually selected, and inspect the required host skills.
2. Identify the operation, user-level Codex skill destination, effective
   `CODEX_HOME`, host version, and available tools. Inspect existing source
   records, same-name packages, links, custom agents, config, and effective
   user instructions. Do not print credentials or unrelated configuration.
3. Resolve each declared branch once to a commit for this run. Use that
   snapshot for discovery, package content, and Codex resources. Read the
   target snapshot's baseline before applying changed requirements. If it
   expands the established scope, present the difference before applying it.

For a check request, compare inventory and resource content without writing
target files, receipts, or backups, or running installer update commands.
Report gaps and conflicts; do not convert inspection into setup.

## Apply the selected skills

Use `$maintain-skills` for skill operations. It owns CLI compatibility checks,
source tracking, installation, and updates. Read its complete instructions
and affected references before invoking commands. Keep Codex, user scope, and
ordinary copied packages explicit; inspect shared targets before replacement.

If `maintain-skills` is absent, read it from the same verified source snapshot
and follow its protocol to bootstrap the two mandatory directories. Do not
assume a missing skill is callable. Keep the loaded instructions and resources
in a temporary snapshot outside installation destinations until the run ends.

Discover the selected directory contents from that snapshot instead of keeping
a second list of leaf names. Use supported directory selection and explicit
Codex targeting; never use `--all`, which may select other agents too. If the
CLI needs names, derive them from the selected directories. Verify the current
CLI can consume the resolved revision and retain usable remote provenance;
do not substitute an untracked temporary local-path install. Stop only the
affected operation if it cannot honor the source, copy mode, or target scope.

Install missing packages and refresh unchanged managed packages. Preserve
local edits and unknown ownership until a concrete conflict is resolved.
Apply `gh` from its selected external snapshot. Check host-provided skills
without installing duplicates. Do not remove unrelated skills, old names, or
skills that disappeared upstream as an implicit part of setup or update.

## Apply the Codex resources

Follow [Codex installation](references/codex-installation.md) for comparison,
backups, merges, receipts, and recovery. The owned resources are:

- [Custom agent files](assets/codex/agents/): copy standalone TOMLs into the
  selected Codex home; no config registration or source checkout is required.
- [Config fragment](assets/codex/config.fragment.toml): merge only its three
  selected keys; preserve all unrelated values, tables, and comments.
- [Subagent instructions](assets/codex/subagent-instructions.md): maintain one
  Fern block in the effective user instruction file, respecting overrides.

Compare current values to the last successfully applied baseline. Do not
overwrite local changes, adopt unknown files silently, or write through a
symlink or junction into an authored repository. Record only resources that
were successfully written and read back; leave failed items at their previous
applied revision. A receipt covers Codex resources, not skill source records.

Refresh installed `setup-fern` and `maintain-skills` last, after work that uses
their loaded versions. Continue using the frozen snapshot through completion;
new instructions take effect in a fresh session, not midway through this run.

## Verify and report

Read back installed skill files and CLI provenance, custom agent TOML, merged
config, the effective instruction block, and successful receipt entries.
Report added, refreshed, unchanged, conflicted, missing-host, and failed items
with source branch and resolved revision. After a partial failure, inspect
actual state and retry only unfinished items; do not claim a whole-run rollback.

Separate file application from fresh-session discovery and runtime use.
Report incompatible host fields or unavailable model defaults as gaps instead
of silently changing the baseline. Custom role instructions constrain duties;
permissions remain inherited from the parent session. Do not install plugins,
change login or approval settings, or update the Codex host as part of Fern.
