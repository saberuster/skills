# Commit

Draft or review Conventional Commit messages and create scoped commits when
requested. The [skill instructions](SKILL.md) contain the workflow and five
editable fallback preferences: type, scope, body, breaking changes, and checks.
The format follows [Conventional Commits 1.0.0][spec]; the common type vocabulary
comes from [commitlint's conventional preset][preset].

For gameplay, visual assets, or design deliverables, the skill reads
[game and design guidance](references/game-and-design.md) as needed for
classification, asset completeness, compatibility, and relevant checks.

## Requirements and scope

Git and repository access are needed for inspecting or creating real commits.
Supplied diffs are enough for message drafting, with evidence limits stated.
No additional skill, commitlint installation, or release tool is required.
Use an existing project checker when available; do not add dependencies or hooks
as a side effect of preparing a commit.

User choices and project rules override the fallback preferences. Drafting and
review are read-only; authorized commits group complete intents in dependency
order, preserving unrelated work, hooks, and signing. See the
[skill instructions](SKILL.md) for authorization, breaking syntax, grouping,
and validation details.

Codex metadata allows implicit invocation. Claude Code does not apply
`agents/openai.yaml`; discovery and behavior require separate verification.

## Installation and updates

Follow the shared [installation and update protocol][installation]. Replace
`<revision>` with a tag or full commit SHA that contains this skill and
`<project-root>` with the target project's absolute path. For Claude Code,
replace `Codex` below with `Claude Code`; user scope can be requested explicitly.

The source is `skills/fern/commit/`, migrated from `skills/git-commit/` and
renamed from `git-commit`. Existing installations are unchanged. Select the new
source path and skill name when migrating; treat an old `git-commit`
installation as a separate migration, preserving local edits. Discovery under
the new name has not been verified.

**Install:**

```text
Install only commit from https://github.com/saberuster/skills at <revision>
for Codex in project <project-root>. Follow docs/installation.md. Preserve
existing skills and report the resolved commit, destination, and checks.
```

**Update:**

```text
Update only my existing commit installation in Codex project <project-root>
from https://github.com/saberuster/skills to <revision>. Follow
docs/installation.md. Compare the recorded source and preserve local edits;
ask me to resolve conflicts.
```

## Usage

```text
Use $commit to draft a message for the staged changes. Do not commit.
```

```text
Use $commit to commit the parser fix and its tests. Preserve unrelated work.
```

```text
/commit Review this message against Conventional Commits 1.0.0 only.
```

The [synthetic cases][examples] define expected behavior, not verified results.
See the [skill catalog][catalog] for client discovery evidence.

[spec]: https://www.conventionalcommits.org/en/v1.0.0/
[preset]: https://github.com/conventional-changelog/commitlint/tree/master/%40commitlint/config-conventional
[installation]: https://github.com/saberuster/skills/blob/main/docs/installation.md
[examples]: https://github.com/saberuster/skills/blob/main/examples/commit.md
[catalog]: https://github.com/saberuster/skills#available-skills
