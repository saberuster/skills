# Maintain AGENTS.md

Capture, create, review, trim, or revise durable project rules in `AGENTS.md`
files.
Preserve obligations and place local rules in their applicable scope. See the
[skill instructions](SKILL.md) for the complete workflow.

## Requirements and scope

This instruction-only skill needs a host that can read the target project and,
for edits, write the authorized files. It distinguishes read-only review from
authorized capture or revision and preserves obligations unless sufficient
authority establishes a change or expiry.

Comprehensive reviews use a [coverage guide](references/coverage.md) to find
missing guidance or navigation across eight project responsibilities. Local
maintenance stays within its requested scope. Build and test guidance is checked
against its maintained sources; inspected commands are distinguished from checks
actually run. This is not a full implementation or architecture audit.

Trimming removes generic advice a capable agent already follows, facts
discoverable from code or linked documents, and duplicates across the scope
chain, while keeping every obligation. Reviews flag files at risk of the host's
loading size limit and note sibling instruction files for other hosts, such as
`CLAUDE.md`, that import, link, or diverge from `AGENTS.md`.

The [language rules](SKILL.md#language) govern heading and body language,
user overrides, ambiguous evidence, and scoped edits with link repair.

The skill cannot recover missing conversation history or guarantee that another
host loads instruction files with Codex's precedence rules. It does not manage
custom agent configuration files. Invoking it does not authorize staging,
commits, installation, or edits to user-level instruction copies. Moving content
beyond the authorized target scope requires additional authority.

## Installation and updates

The source package is `skills/meta/maintain-agents-md/` in `saberuster/skills`.
Install this leaf directory; `meta` is a collection, not an installable skill.

Give your agent an explicit request using the shared
[installation and update protocol][installation]. Replace
`<revision>` with an existing release tag or full commit SHA containing this
skill, and `<project-root>` with your project's absolute path. These prompts
select Codex project scope. For Claude Code, replace `Codex` with
`Claude Code`; for a user-wide installation, replace the project scope with
`my Codex user scope` or `my Claude Code user scope`.

**Install:**

```text
Install only maintain-agents-md from https://github.com/saberuster/skills
at <revision>, using source skills/meta/maintain-agents-md/, for Codex in project
<project-root>. Follow the repository's docs/installation.md protocol.
Preserve existing skills and report the resolved commit, destination, and
checks performed.
```

**Update:**

```text
Update only the existing maintain-agents-md installation in Codex project
<project-root> from https://github.com/saberuster/skills to <revision>.
Use source skills/meta/maintain-agents-md/ and follow the repository's
docs/installation.md protocol. Compare against its recorded source revision
and preserve local edits; ask me to resolve conflicts.
```

## Usage

In Codex, use `/skills` or type `$` to select the installed skill.
Claude Code uses a [slash command](https://code.claude.com/docs/en/skills)
with the skill name at the start of the request:

```text
/maintain-agents-md Review this project's AGENTS.md files. Report findings and
suggested changes without editing files.
```

CI checks discovery and loading; the requirements and scope above still apply.

**Read-only review:**

```text
Use $maintain-agents-md to review this project's AGENTS.md files.
Report findings and suggested changes without editing files.
```

**Comprehensive review:**

```text
Use $maintain-agents-md to review this project's complete AGENTS.md guidance.
Check missing responsibilities and authoritative links as well as existing
rules. Report coverage, evidence, and proposed changes without editing files.
```

**Apply changes:** State both the scope and the intended change.

```text
Use $maintain-agents-md to remove equivalent duplicate rules in the root
AGENTS.md. Preserve all obligations, exceptions, and nested rules.
```

**Language choice:**

```text
Use $maintain-agents-md to revise the whole root AGENTS.md and its contents
links. Use English headings and Chinese body text. Preserve obligations.
```

See the [behavioral cases][examples] for expected
outcomes, non-trigger requests, and boundary checks. These cases describe
expected behavior; they do not establish successful execution on every host.

[Back to the skill catalog][catalog].

[installation]: https://github.com/saberuster/skills/blob/main/docs/installation.md
[examples]: https://github.com/saberuster/skills/blob/main/examples/maintain-agents-md.md
[catalog]: https://github.com/saberuster/skills#available-skills
