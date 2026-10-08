# Technical Docs

Create, revise, review, or consolidate technical project documentation intended
for version control. Compare identified documents or accepted contracts with
implementation, preserving decision status and distinguishing intended behavior
from observations and gaps. See the [skill instructions](SKILL.md) for the
complete workflow.

## Requirements and scope

This instruction-only skill needs read access to relevant project evidence and,
for revisions, write access to authorized documents. Runnable examples and
rendering checks need their own applicable tools and environment.

Review-only requests remain read-only. Ordinary explanations, design
discussions, and coding do not alone request documents or implementation audits.
Project instruction governance and persistent task tracking follow their
established workflows. Documentation work does not authorize commits,
publication, or unrelated implementation.

## Installation and updates

Give your agent an explicit request using the shared
[installation and update protocol][installation]. Replace
`<revision>` with an existing release tag or full commit SHA containing this
skill, and `<project-root>` with your project's absolute path. These prompts
select Codex project scope. For Claude Code, replace `Codex` with
`Claude Code`; for a user-wide installation, replace the project scope with
`my Codex user scope` or `my Claude Code user scope`.

**Install:**

```text
Install only technical-docs from https://github.com/saberuster/skills
at <revision> for Codex in project <project-root>. Follow the repository's
docs/installation.md protocol. Preserve existing skills and report the resolved
commit, destination, and checks performed.
```

**Update:**

```text
Update only the existing technical-docs installation in Codex project
<project-root> from https://github.com/saberuster/skills to <revision>.
Follow the repository's docs/installation.md protocol. Compare against its
recorded source revision and preserve local edits; ask me to resolve conflicts.
```

## Usage

In Codex, use `/skills` or type `$` to select the installed skill. The paths
below are illustrative project documents; replace them with your target paths.
Claude Code uses a [slash command](https://code.claude.com/docs/en/skills)
with the skill name at the start of the request:

```text
/technical-docs Compare docs/jobs.md with the current job cancellation
implementation. Report evidence and gaps without editing files.
```

CI checks discovery and loading; the requirements and scope above still apply.

**Read-only comparison:**

```text
Use $technical-docs to compare docs/jobs.md with the current job cancellation
implementation. Report evidence and gaps without editing files.
```

**Apply changes:** State the document scope and the intended change.

```text
Use $technical-docs to consolidate docs/setup.md and docs/quickstart.md into
docs/setup.md. Preserve supported instructions and repair affected links.
```

See the [behavioral cases][examples] for document
creation, scoped edits, read-only review, unresolved decisions, consolidation,
and implementation comparison. These cases describe expected behavior; they do
not establish successful execution on every host.

[Back to the skill catalog][catalog].

[installation]: https://github.com/saberuster/skills/blob/main/docs/installation.md
[examples]: https://github.com/saberuster/skills/blob/main/examples/technical-docs.md
[catalog]: https://github.com/saberuster/skills#available-skills
