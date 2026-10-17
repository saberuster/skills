# Research Skill Patterns

Ground skill creation, editing, and review in relevant open-source examples.
The skill adds a proportional research pass, records why an upstream pattern
fits or does not fit, and connects decisions to validation. See the
[skill instructions](SKILL.md) for the workflow and the
[research guide](references/research-guide.md) for source selection and evidence.

## Requirements and scope

This instruction-only package uses the host's available search, code browsing,
or verified local source access. It prefers Exa when available and respects a
provider named by the user, but has no mandatory tool or runtime dependency.
If evidence is inaccessible, useful drafts and partial reviews can proceed
with explicit research gaps; they are not reported as completed research.

Research covers both the skill's task domain and its instruction mechanisms.
Small text corrections can reuse applicable evidence without a broad search.
It supplements an existing authoring or review workflow and does not install
skills, execute a reviewed skill's task, or expand a read-only review into edits.

The Codex metadata permits implicit invocation. Selection still depends on the
host, discoverability, competing skills, and the request; this package is not a
global hook. Claude Code does not apply the Codex metadata policy. Repository
instructions can explicitly require this research pass for skill content work
and point to its installed `SKILL.md`. Other repositories must configure their
own entry point if they need that requirement.

Discovery, natural selection, and research behavior need separate verification.
The catalog's recorded checks describe their tested source revision and do not
establish automatic invocation on every host.

## Installation and updates

The source package is `skills/meta/research-skill-patterns/` in
`saberuster/skills`. Install this leaf directory; `meta` is a collection,
not an installable skill. The skill's name remains `research-skill-patterns`.
All required resources are inside the leaf package.

Use the shared [installation and update protocol][installation]. Replace
`<revision>` with an existing release tag or full commit SHA containing this
skill, and `<project-root>` with your project's absolute path. For Claude Code,
replace `Codex` with `Claude Code`; specify user scope if that is intended.

**Install:**

```text
Install only research-skill-patterns from https://github.com/saberuster/skills
at <revision>, using source skills/meta/research-skill-patterns/,
for Codex in project <project-root>. Follow docs/installation.md in that
repository. Preserve existing skills and report the resolved commit,
destination, and checks performed.
```

**Update:**

```text
Update only the existing research-skill-patterns installation in Codex project
<project-root> from https://github.com/saberuster/skills to <revision>.
Use source skills/meta/research-skill-patterns/ and follow that
repository's docs/installation.md protocol. Compare against the recorded
revision and preserve local edits; ask me to resolve conflicts.
```

## Usage

In Codex, use `/skills` or type `$` to select `$research-skill-patterns`.
For example:

```text
Use $research-skill-patterns while creating a skill for reviewing release
notes. Inspect relevant open-source examples and explain the decisions.
```

Claude Code uses a [slash command](https://code.claude.com/docs/en/skills):

```text
/research-skill-patterns Review the release-note skill's trigger and workflow.
Keep the review read-only and connect findings to inspected upstream evidence.
```

These examples use a synthetic task. Researching another skill does not invoke
that skill, and composing this package with a creator or reviewer shares one
research pass rather than repeating searches.

See the [behavioral cases][examples] for expected decisions and failure paths.
Cases specify expectations; actual execution must be assessed separately.

[Back to the skill catalog][catalog].

[installation]: https://github.com/saberuster/skills/blob/main/docs/installation.md
[examples]: https://github.com/saberuster/skills/blob/main/examples/research-skill-patterns.md
[catalog]: https://github.com/saberuster/skills#available-skills
