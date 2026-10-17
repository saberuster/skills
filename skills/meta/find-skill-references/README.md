# Find Skill References

Find and compare open-source practices for a specific or planned agent skill
when you want references. The skill inspects relevant implementations and
explains what can be reused or adapted, with source links and limits. See the
[skill instructions](SKILL.md) for the workflow and the
[research guide](references/research-guide.md) for source selection and evidence.

## Requirements and scope

This instruction-only package uses the host's available search, code browsing,
or verified local source access. It prefers Exa when available and respects a
provider named by the user, but has no mandatory tool or runtime dependency.
If evidence is inaccessible, the response identifies the missing sources and
keeps unsupported recommendations provisional.

The reference question determines whether to inspect similar skills, domain
implementations, or instruction mechanisms. Applicable inspected evidence can
be reused. Ordinary creation, editing, review, and explanation do not trigger
research or require earlier research records. Research does not authorize
editing the target, installing skills, or executing a referenced skill's task.

The Codex metadata permits implicit invocation, so a request such as "Find
open-source examples for a release-note review skill" can select it without
naming it. Selection still depends on the host, discoverability, competing
skills, and the request. Claude Code does not apply the Codex metadata policy.
Repository routing should preserve the reference-seeking condition.

Discovery, natural selection, and research behavior need separate verification.
The catalog's recorded checks describe their tested source revision and do not
establish automatic invocation on every host.

## Installation and updates

The source package is `skills/meta/find-skill-references/` in
`saberuster/skills`. Install this leaf directory; `meta` is a collection,
not an installable skill. All required resources are inside the leaf package.
This package was renamed from `research-skill-patterns`; the rename does not
update or remove existing installed copies. An authorized migration must check
the old installation's source and local edits through the shared protocol.

Use the shared [installation and update protocol][installation]. Replace
`<revision>` with an existing release tag or full commit SHA containing this
skill, and `<project-root>` with your project's absolute path. For Claude Code,
replace `Codex` with `Claude Code`; specify user scope if that is intended.

**Install:**

```text
Install only find-skill-references from https://github.com/saberuster/skills
at <revision>, using source skills/meta/find-skill-references/,
for Codex in project <project-root>. Follow docs/installation.md in that
repository. Preserve existing skills and report the resolved commit,
destination, and checks performed.
```

**Update:**

```text
Update only the existing find-skill-references installation in Codex project
<project-root> from https://github.com/saberuster/skills to <revision>.
Use source skills/meta/find-skill-references/ and follow that
repository's docs/installation.md protocol. Compare against the recorded
revision and preserve local edits; ask me to resolve conflicts.
```

## Usage

In Codex, use `/skills` or type `$` to select `$find-skill-references`.
For example:

```text
Use $find-skill-references to find open-source practices for a planned
release-note review skill. Compare the useful approaches and their limits.
```

Claude Code uses a [slash command](https://code.claude.com/docs/en/skills):

```text
/find-skill-references Find open-source references for this release-note skill's
workflow. Explain what could be reused or adapted, with source links.
```

These examples use a synthetic task. Requests to create a skill, fix its text,
review its workflow, or explain its trigger alone do not select this skill.
Researching another skill does not invoke that skill. When research and
authoring are both requested, collaborating workflows share one research pass.

See the [behavioral cases][examples] for expected decisions and failure paths.
Cases specify expectations; actual execution must be assessed separately.

[Back to the skill catalog][catalog].

[installation]: https://github.com/saberuster/skills/blob/main/docs/installation.md
[examples]: https://github.com/saberuster/skills/blob/main/examples/find-skill-references.md
[catalog]: https://github.com/saberuster/skills#available-skills
