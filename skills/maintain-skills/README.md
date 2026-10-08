# Maintain Skills

List, install, update, and remove standalone agent skills through the Vercel
Skills CLI. Resolve the selected scope, check source records and shared paths,
and verify the result. See the [skill instructions](SKILL.md) for the complete
workflow.

## Requirements and scope

This instruction-only skill requires a compatible Node.js environment with
`npx`, access to the Skills CLI, and network access for remote packages. It
calls `npx skills` and supplies no separate installer. It does not author skill
content or manage plugins.

Read-only update checks and agent-isolated updates depend on verified CLI
capabilities; the upstream update interface reviewed for this skill provides
neither. Unknown provenance or unresolved local edits prevent automatic
replacement. Shared directories may affect several agents. Real CLI execution
and cross-host behavior require separate validation.

Invoke this skill explicitly. Its Codex metadata disables automatic selection;
Claude Code does not apply that metadata policy.

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
Install only maintain-skills from https://github.com/saberuster/skills
at <revision> for Codex in project <project-root>. Follow the repository's
docs/installation.md protocol. Preserve existing skills and report the resolved
commit, destination, and checks performed.
```

**Update:**

```text
Update only the existing maintain-skills installation in Codex project
<project-root> from https://github.com/saberuster/skills to <revision>.
Follow the repository's docs/installation.md protocol. Compare against its
recorded source revision and preserve local edits; ask me to resolve conflicts.
```

These prompts install or update this skill itself. Once available, it can carry
out explicitly requested maintenance of other standalone skills.

## Usage

In Codex, use `/skills` or type `$` to select `$maintain-skills`.
Claude Code uses a [slash command](https://code.claude.com/docs/en/skills)
with the skill name at the start of the request:

```text
/maintain-skills List the skills installed for Claude Code in this project.
```

CI checks discovery and loading; the CLI prerequisites and shared-path
constraints above still apply.

**Read-only inventory:**

```text
Use $maintain-skills to list the skills installed for Codex in this project.
```

**Apply changes:**

```text
Use $maintain-skills to update only format-report in this project's scope.
Preserve local edits and report any shared-client impact.
```

Here `format-report` is a synthetic skill name; replace it with the installed
skill you want to update. A request to check for updates remains read-only and
must not execute an update as a probe.

See the [behavioral cases][examples] for installation,
updates, removal, source tracking, shared paths, and read-only boundaries. These
cases describe expected behavior; they do not establish successful execution on
every host.

[Back to the skill catalog][catalog].

[installation]: https://github.com/saberuster/skills/blob/main/docs/installation.md
[examples]: https://github.com/saberuster/skills/blob/main/examples/maintain-skills.md
[catalog]: https://github.com/saberuster/skills#available-skills
