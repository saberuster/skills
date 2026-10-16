# Reflect

Reflect on the current conversation and propose durable preferences, project
knowledge, verified procedures, and skill improvements. Reconcile candidates
with existing sources, review their evidence, and save only when explicitly
requested. See the [skill instructions](SKILL.md) for the complete workflow.

## Scope and requirements

Analysis uses visible conversation context and read access to relevant sources.
It does not scan other sessions or projects. Incomplete context remains labeled
as incomplete. A separate subagent reviews nonempty candidates when available;
otherwise the skill reports that only self-review was possible.

Writes require an explicit request and an established, user-maintained source.
Existing authorization needs no second approval. Skill edits require an
available `skill-creator`; project instruction edits use `maintain-agents-md`.
Missing companions leave those edits as proposals while independent authorized
document edits can proceed. Personal preference storage needs a supported,
configured destination; no memory API or background process is bundled.

Installed skill copies, third-party packages, system skills, and plugin caches
are read-only. Scope checks include resolved links. Reflection does not itself
authorize installation, commits, publication, external posts, or unrelated code
changes. Shared output uses synthetic examples instead of private transcripts.

Saved files, configured reading entrypoints, and successful recall in a fresh
task are different results. Applicability and expiry checks accompany saved
knowledge so later tasks do not depend on invoking reflection again.

## Usage

In Codex, select the skill with `/skills` or `$`. Claude Code uses a slash
command with the skill name at the start of the request.

**Propose without writing:**

```text
Use $reflect to learn from this conversation and propose useful changes.
```

```text
/reflect Review this conversation for durable knowledge without editing files.
```

**Save within an established scope:**

```text
Use $reflect to save verified project lessons in our existing docs/runbook.md.
Keep other destinations as proposals and preserve unrelated content.
```

**Apply skill improvements:**

```text
Use $reflect to learn from this conversation and apply supported improvements.
My user-maintained skill sources are in <skill-source-root>; limit writes to
that directory and use the available skill-creator for authoring and validation.
```

Replace placeholders with actual maintained sources. An invocation or a positive
response to a proposal alone does not request edits. Some sessions need no
persistent changes. See the [synthetic cases][examples] for expected behavior;
they do not establish successful execution on every host.

## Installation and migration

The source is `skills/fern/reflect/`, migrated and expanded from
`learn-from-session`. There is one maintained implementation under `reflect`;
existing installations are unchanged. The rename does not automatically remove
an old installation or preserve local edits in a new copy. Inspect existing
source records and local changes before a separately requested migration, then
verify discovery under `reflect` in a fresh session. Avoid retaining both
entries with overlapping implicit triggers.

Use the shared [installation protocol][installation]. Replace `<revision>`
with a release tag or full commit SHA that contains `reflect` and
`<project-root>` with the intended project.

```text
Install only reflect from https://github.com/saberuster/skills at <revision>
for Codex in project <project-root>. Follow docs/installation.md from that
repository. Preserve existing skills and report the resolved source revision,
destination, and checks performed.
```

For Claude Code, replace `Codex` with `Claude Code`; for user scope, explicitly
name that scope. This repository supports nested source discovery; that does
not establish arbitrary host support for a nested installed directory or
portable plugin archive. Follow the chosen host's installation flow.

Client discovery under the new name and cross-session recall remain separate
checks; do not transfer the old name's discovery result to this package.

## Design references

The workflow draws on [Cursor pstack reflection][pstack] for review and routing,
[LangMem][langmem] for memory types and reconciliation, [Everything Claude Code
continuous learning][ecc] for atomic scoped candidates, and [gstack
learning][gstack] and [Letta memory][letta] for retrieval and maintenance.
These are design references, not runtime dependencies or copied implementations.

[installation]: https://github.com/saberuster/skills/blob/main/docs/installation.md
[examples]: https://github.com/saberuster/skills/blob/main/examples/reflect.md
[pstack]: https://github.com/cursor/plugins/blob/main/pstack/skills/reflect/SKILL.md
[langmem]: https://langchain-ai.github.io/langmem/concepts/conceptual_guide/
[ecc]: https://github.com/affaan-m/everything-claude-code/blob/main/skills/continuous-learning-v2/SKILL.md
[gstack]: https://github.com/garrytan/gstack/blob/main/learn/SKILL.md
[letta]: https://docs.letta.com/configuration/memory
