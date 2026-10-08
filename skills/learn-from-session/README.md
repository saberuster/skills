# Learn from Session

Extract reusable lessons from the current conversation and improve
user-maintained skills. Prefer verified methods, user corrections, and useful
repeated operations; update existing skills when possible. Some sessions need
no changes. See the [skill instructions](SKILL.md) for the complete workflow.

## Requirements and scope

Analysis needs the available conversation and read access to relevant skills.
Applying changes also requires an available `skill-creator` for authoring and
validation. If it is unavailable, the skill reports proposals and incomplete
implementation; it does not install that dependency automatically. This
workflow targets Codex; behavior on other hosts has not been validated.

An explicit request authorizes scoped source edits unless it asks only for
analysis. Automatic selection alone does not authorize writes. Establish the
user-maintained source directory separately: installation does not make
installed copies, system skills, third-party skills, or plugin caches writable.
Links must resolve inside the authorized source scope. The skill does not scan
other sessions or authorize commits, publication, installation, or unrelated
settings changes.

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
Install only learn-from-session from https://github.com/saberuster/skills
at <revision> for Codex in project <project-root>. Follow the repository's
docs/installation.md protocol. Preserve existing skills and report the resolved
commit, destination, and checks performed.
```

**Update:**

```text
Update only the existing learn-from-session installation in Codex project
<project-root> from https://github.com/saberuster/skills to <revision>.
Follow the repository's docs/installation.md protocol. Compare against its
recorded source revision and preserve local edits; ask me to resolve conflicts.
```

## Usage

In Codex, use `/skills` or type `$` to select the installed skill.
Claude Code uses a [slash command](https://code.claude.com/docs/en/skills)
with the skill name at the start of the request:

```text
/learn-from-session Analyze this conversation and suggest reusable skill
improvements without editing files.
```

CI checks discovery and loading; the editing workflow's Codex focus and
`skill-creator` dependency still apply.

**Read-only analysis:**

```text
Use $learn-from-session to analyze this conversation and suggest reusable skill
improvements. Do not edit files.
```

**Apply changes:** Replace `<skill-source-root>` with the actual directory you
maintain, rather than an installed copy or cache.

```text
Use $learn-from-session to learn from this conversation and apply useful
changes.
My user-maintained skill sources are in <skill-source-root>; limit edits to that
directory. Use the available skill-creator for authoring and validation.
```

See the [behavioral cases][examples] for evidence,
authorization, dependency, and source-scope checks. These cases describe
expected behavior; they do not establish successful execution on every host.

[Back to the skill catalog][catalog].

[installation]: https://github.com/saberuster/skills/blob/main/docs/installation.md
[examples]: https://github.com/saberuster/skills/blob/main/examples/learn-from-session.md
[catalog]: https://github.com/saberuster/skills#available-skills
