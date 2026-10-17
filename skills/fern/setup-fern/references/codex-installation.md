# Codex Resource Installation

Apply the resources in `assets/codex/` from the same immutable snapshot used
for Fern skills. This procedure covers custom agents, selected configuration,
and a complete managed user instruction block. `maintain-skills` owns skill files
and their provenance.

## Establish targets and ownership

Resolve the actual Codex home from the host configuration and `CODEX_HOME`,
using the host's documented default only when no override applies. Inspect
these targets before preparing changes:

| Resource | Target | Owned unit |
| --- | --- | --- |
| `assets/codex/agents/*.toml` | `<CODEX_HOME>/agents/<name>.toml` | One selected file |
| `assets/codex/config.fragment.toml` | `<CODEX_HOME>/config.toml` | Three selected `[agents]` keys |
| `assets/codex/user-instructions.md` | Effective user instruction file | One complete marked rule block |
| Application receipt | `<CODEX_HOME>/fern/receipt.json` | Codex resource evidence only |

Inspect ancestor paths, targets, and relevant descendants for symlinks,
junctions, or other reparse points before writing. A link into a source
checkout is a migration case. Do not edit through it, reset its checkout, or
replace its target as part of normal setup.

Read any existing receipt and compare the current owned unit with both the
previously applied value and the incoming value. An absent target can be
created. An exact incoming match can be adopted without replacement. An owned
unit matching its last recorded application can be updated. A divergent unit
or existing unit without a reliable baseline needs a concrete conflict
decision before replacement. Backups do not by themselves authorize overwrites.

Proceed with independent nonconflicting units within the requested scope.
Keep conflicted units intact and report their paths and differences. Never
infer ownership from a familiar filename or a matching upstream commit alone.

## Prepare and apply

1. Validate every selected agent as TOML with nonempty `name`, `description`,
   and `developer_instructions`; match the filename to `name`. Preserve the
   bundled role instructions and model settings. Confirm host compatibility.
2. Prepare the complete next version of each affected file outside its target.
   Parse TOML after configuration changes and check instruction markers before
   writing. Preserve unrelated content and the existing file's permissions.
3. Before each authorized replacement, save the exact previous bytes and its
   target path under a run-specific backup directory in
   `<CODEX_HOME>/fern/backups/`. Record absence for a newly created target.
   Keep backups local; configuration and user instructions may be private.
4. Apply one prepared file at a time using a same-directory temporary file and
   atomic replacement where available. Re-read and validate each result before
   recording success. Stop dependent work after failure; inspect the actual
   state before retrying only unresolved units.
5. Update the receipt with successful per-unit outcomes and their source SHA.
   Keep the previous record for an unchanged or failed unit. Report pending
   conflicts and failures separately; a downloaded snapshot is not applied
   state.

### Custom agents

Copy the six packaged TOMLs into the personal `agents` directory as regular
files. They are discoverable standalone agents on a compatible host; no
per-agent registration table in `config.toml` is required. Preserve unrelated
custom agents and do not delete files absent from the current package.

The files retain their role-specific model and reasoning choices. Custom agent
settings do not grant permissions beyond the parent session. In particular,
do not describe a bundled `sandbox_mode` value as an effective permission
override; role instructions and inherited session permissions still apply.

### Configuration

The fragment owns only these keys under `[agents]`:

```toml
[agents]
max_concurrent_threads_per_session = 4
default_subagent_model = "gpt-6.1-sol"
default_subagent_reasoning_effort = "high"
```

Merge each selected key into the existing table using a TOML-aware edit that
preserves unrelated tables, keys, and comments. Create the table only when
absent. Do not append a second `[agents]` table, overwrite the entire config,
or introduce `agents.enabled` merely to repeat its default. Treat other valid
TOML representations of the same table structurally; do not rely on a text
search for one exact header. If a faithful merge is unavailable, report the
limitation and preserve the file rather than writing a lossy approximation.

Check inherited or higher-priority configuration that can override these
values. File readback establishes what was written; it does not establish the
effective settings of an existing chat.

### User instructions

Identify the user instruction file Codex actually loads. In the user directory,
`AGENTS.override.md` takes precedence over `AGENTS.md`; also inspect the host's
configured fallback filenames and document loading behavior. Do not update a
shadowed `AGENTS.md` and report the rules as active. When no effective user
file exists, create `<CODEX_HOME>/AGENTS.md` with the complete bundled baseline
inside the markers below; use a different default only if the host documents
one. The selected Codex home need not be the default home directory.

The [user instruction asset](../assets/codex/user-instructions.md) carries the
maintained personal rules for initiative, instruction precedence, writing,
subagent delegation, and testing, plus Fern's role guidance. Install all of it,
including the built-in `explorer` model `gpt-6-luna`, reasoning effort `high`,
and fresh or limited-history context guidance for explicit model overrides.
Use the asset from the resolved source snapshot; do not require access to the
author's original machine or recapture the destination's rules as the baseline.
Future baseline changes belong in this asset through source maintenance.

Use these exact block markers around the complete asset:

```markdown
<!-- fern:user-instructions:start -->
<contents of assets/codex/user-instructions.md>
<!-- fern:user-instructions:end -->
```

Require zero or one well-formed pair, accounting for the legacy markers below.
With no pair, inspect existing rules across all baseline topics for conflicts
or duplication before adding the block. With one current pair, apply ownership
checks and replace only that block. Preserve all surrounding user instructions.
For overlapping unmarked rules, show the exact proposed adoption or merge and
resolve the conflict before changing that content; do not silently delete it
or stack duplicate policies. Multiple, reversed, unmatched, or coexisting old
and new marker pairs require resolution; do not guess a range.

#### Migrate the former subagent block

Earlier versions used `fern:subagent-instructions:start/end` and the receipt
key `instructions:subagent-delegation`. During an authorized setup or update,
show the added rule topics before expanding this baseline. Check the legacy
target and block bytes using the [receipt rules](#receipt-and-recovery). A
matching block can be replaced in place with the complete new block, provided
surrounding rules do not conflict or duplicate the incoming rules. Keep the
surrounding content unchanged and back up the file before replacement.

An edited legacy block, an unknown baseline, or overlapping surrounding rules
needs a concrete conflict decision before replacement. Preserve the legacy
block and receipt while that decision is pending; continue independent work.
Do not append a second Fern block to bypass the conflict. After the new block
is successfully written and read back, record `instructions:user-rules` and
remove the superseded `instructions:subagent-delegation` entry. On failure,
retain the previous receipt and inspect the actual file before retrying.

## Receipt and recovery

Use a small versioned JSON receipt for Codex resources. For example:

```json
{
  "schema_version": 1,
  "resources": {
    "agents/reviewer.toml": {
      "source_commit": "<resolved source SHA>",
      "sha256": "<hash of applied file bytes>"
    },
    "config:agents.default_subagent_model": {
      "source_commit": "<resolved source SHA>",
      "value": "gpt-6.1-sol"
    },
    "instructions:user-rules": {
      "source_commit": "<resolved source SHA>",
      "target": "AGENTS.override.md",
      "sha256": "<hash from start marker through end marker, inclusive>"
    }
  }
}
```

Each successful agent file and config key gets its own entry. Store the
effective instruction target relative to Codex home. Use SHA-256 of exact file
bytes for agent files and compare parsed values for config keys.

For instruction blocks, compute SHA-256 from the opening `<` of the start
marker through the closing `>` of the end marker, inclusive. Exclude any
following line ending; it remains surrounding content during replacement.
Do not normalize internal whitespace or line endings.

For existing receipts using either instruction marker generation, verify the
recorded target and compare only the exact marked range and, if present, that
range plus its immediately following single LF or CRLF. Do not trim or accept
other byte differences. A matching existing receipt does not itself require a
rewrite. Record the canonical range only after an authorized successful write
and readback, or an exact-match recovery adoption under the rules below.
Read-only checks must not change receipts.

Keep skills and CLI lock records out of this receipt. A run with failures can
legitimately contain resources from several source commits. Never replace all
per-item revisions with the newest downloaded revision.

If a crash occurs between a file write and receipt update, re-read the target
and compare it with the prepared incoming value and backup before resuming.
An exact incoming match can be adopted; uncertainty remains a conflict. Do not
blindly replay the whole setup or claim the operation was transactional across
all resources.

For restoration, verify that the current target still matches this run's
applied result before replacing it with its exact backup. Restore only the
authorized affected files or units; preserve edits made since application.
Remove a newly created file only when its unchanged contents and original
absence are verified. Re-read restored resources and reconcile their receipts.
Report any recovery that remains incomplete.

## Migrating a linked agents directory

Treat an existing directory junction or symlink as a separate, explicit
migration decision. Inventory its binding, source path, unrelated agents, and
local modifications first. Prepare independent copies and backups before
detaching anything. Preserve unrelated agent files in the planned ordinary
directory and resolve selected-name conflicts individually.

When migration is authorized for the exact binding, detach only the verified
link itself using the platform's link-safe operation. Never recursively remove
the resolved source directory. Create the ordinary destination, copy the
approved files, and verify that the source checkout remains unchanged. A file
link or linked ancestor needs the equivalent scoped plan. If the source cannot
be inspected safely or ownership is unresolved, leave the binding intact and
report migration pending.

## Verification and source evidence

Report separately: successful file/key/block readback, parsed resource
validation, remaining conflicts, host capability checks, and discovery in a
fresh Codex chat. Do not claim fresh-chat loading or model availability from
source tests alone. This task's source validation does not require updating
the author's installed environment.

When fresh-session loading is requested, start a new parent session using the
selected Codex home and its normal configuration. Spawn each selected custom
role through the native agent tool without supplying its instruction text or
overriding model or effort. Direct instruction injection tests behavior, not
standalone discovery.

Where the host exposes the evidence, correlate parent and child records,
compare the actual child developer instructions with the installed TOML, and
check runtime model and effort against role settings and effective defaults.
An agent's self-description is insufficient; mark unavailable evidence as
unverified. Record the host version and tested client entrypoint, such as CLI
or desktop. Report loading separately from task probes blocked by tool or
environment errors; a successful spawn alone does not prove exact loading or
task execution. Keep private traces local and publish only sanitized results.

Shared research inspected on 2026-10-17 supports these boundaries:

- [Custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents)
  documents standalone TOML fields, `[agents]` defaults, and inherited
  permissions. Adopt copied files and selected-key merges; validate the actual
  host separately.
- [User instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
  documents file precedence. Apply the block to the effective file and report
  current-session versus fresh-chat evidence separately.
- [Configuration basics](https://learn.chatgpt.com/docs/config-file/config-basic)
  documents configuration locations and layering. Preserve unrelated settings
  and inspect effective overrides before claiming alignment.

These pages describe host contracts. The ownership receipt and backup policy
are Fern's local design, not claims of a built-in Codex synchronization API.
