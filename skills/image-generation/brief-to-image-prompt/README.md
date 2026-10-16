# Brief to Image Prompt

Develop an idea or brief by resolving consequential creative choices, then use
`gpt-image-prompting` to express the established requirements as a prompt.
See the [skill instructions](SKILL.md) for the workflow.

## Requirements and scope

Both `brief-to-image-prompt` and [gpt-image-prompting][core] must be available to
the current host. The entry resolves the core by name using host discovery or
supported invocation; it does not assume an installation path or install it.
Using the same source revision for both skills is recommended.

Use this entry when the main work is clarifying the desired image. Known
requirements, existing-prompt edits, and reviews can use the core directly.
Honor an explicitly selected skill; a reference image alone does not change
the main task.

This instruction-only workflow produces prompt text, not images, processed
assets, or verification results. The core owns output, language, and revision
rules, including requested alternatives, review-only findings, and fragments.

Codex metadata allows implicit invocation. Claude Code does not apply
`agents/openai.yaml`; metadata alone does not establish policy parity. Discovery,
dependency loading, and behavior require separate verification.

## Installation and updates

Use the shared [installation and update protocol][installation]. Replace
`<revision>` with an existing tag or full commit SHA containing both skills and
`<project-root>` with your project's absolute path. These prompts select Codex
project scope. For Claude Code, replace `Codex` with `Claude Code`; for user scope,
replace the project scope with `my Codex user scope` or
`my Claude Code user scope`.

**Install:**

```text
Install only brief-to-image-prompt and gpt-image-prompting from
https://github.com/saberuster/skills at <revision> for Codex in project
<project-root>. Follow docs/installation.md. Preserve existing skills and report
the resolved commit, destinations, and checks performed.
```

**Update:**

```text
Update only the existing brief-to-image-prompt and gpt-image-prompting
installations in Codex project <project-root> from
https://github.com/saberuster/skills to <revision>. Follow docs/installation.md.
Compare with their recorded source revisions and preserve local edits; ask me
to resolve conflicts.
```

## Usage

In Codex:

```text
Use $brief-to-image-prompt to turn my quiet forest game idea into a GPT Image
prompt. I have not chosen a visual style yet; help me choose before drafting.
```

In Claude Code:

```text
/brief-to-image-prompt Write an English GPT Image prompt for a wide watercolor
banner: two foxes resting under a maple tree, soft autumn light, no lettering.
Choose the small background details freely.
```

The entry asks about conflicting hard requirements, information necessary for
delivery, and consequential choices the user has retained. Optional details can
be omitted; leaving them unspecified does not grant creative freedom. Use
freedom the user has delegated, and proceed directly when the brief is complete.
The [synthetic cases][examples] describe acceptance criteria, not successful runs.

[Back to the skill catalog][catalog].

[core]: https://github.com/saberuster/skills/blob/main/skills/image-generation/gpt-image-prompting/README.md
[installation]: https://github.com/saberuster/skills/blob/main/docs/installation.md
[examples]: https://github.com/saberuster/skills/blob/main/examples/brief-to-image-prompt.md
[catalog]: https://github.com/saberuster/skills#available-skills
