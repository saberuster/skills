# GPT Image Prompting

Turn established requirements into a complete GPT Image prompt. This is the
shared standard behind `brief-to-image-prompt` and `image-to-prompt`, and can
also organize or revise an existing prompt directly. See the
[skill instructions](SKILL.md) for its scope.

## Requirements and scope

This instruction-only core needs no other skill or image-generation tool.
Its six sections cover task, content, composition, visual treatment, output
requirements, and constraints. The default result is one copyable prompt in
Chinese, with natural-language headings and all delivery requirements inside
it. A requested language or format takes precedence.

Guidance covers stylized and pixel art, strict game-asset specifications,
illustrations, references, edits, exact text, and related outputs as needed.
The core organizes established information. Brief development and image
analysis belong to the entry skills. It does not generate, export, process,
or verify images and assets.

Codex metadata allows implicit invocation. Client discovery, automatic
selection, dependency loading, and task behavior require separate evidence.
Reading this README or creating source files does not install these skills.

## Installation and updates

Use the shared [installation protocol][installation]. Replace `<revision>`
with an existing release tag or full commit SHA containing the skill, and
`<project-root>` with your project's absolute path. For Claude Code, replace
`Codex` with `Claude Code`; for user scope, replace the project destination
with `my Codex user scope` or `my Claude Code user scope`.

**Install:**

```text
Install only gpt-image-prompting from https://github.com/saberuster/skills
at <revision> for Codex in project <project-root>. Follow the repository's
docs/installation.md protocol. Preserve existing skills and report the resolved
commit, destination, and checks performed.
```

**Update:**

```text
Update the existing gpt-image-prompting installation in Codex project
<project-root> from https://github.com/saberuster/skills to <revision>.
Follow docs/installation.md, compare against its recorded source revision,
and preserve local edits. Ask me to resolve conflicts.
```

The entry skills require this core in their host's available skills. Their
READMEs explicitly select both packages for installation. They locate the
core through host discovery, not an assumed neighboring installation path.

## Usage

For Codex:

```text
Use $gpt-image-prompting to organize my approved potion-icon requirements into
one English prompt. Include the final 32 by 32 canvas, PNG format, and binary
alpha requirement in that same prompt. Preserve the supplied design.
```

For Claude Code:

```text
/gpt-image-prompting Reorganize this existing image prompt without changing
its subject, style, literal lettering, or output specifications.
```

See [synthetic acceptance cases][examples] for integration, revisions, style,
and series checks. They describe expected behavior, not successful runs.

[Back to the skill catalog][catalog].

[installation]: https://github.com/saberuster/skills/blob/main/docs/installation.md
[examples]: https://github.com/saberuster/skills/blob/main/examples/gpt-image-prompting.md
[catalog]: https://github.com/saberuster/skills#available-skills
