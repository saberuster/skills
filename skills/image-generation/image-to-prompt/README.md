# Image to Prompt

Observe a reference image to describe its visible content or extract the
requested style, composition, or features. Use `gpt-image-prompting` to express
the result. See the [skill instructions](SKILL.md) for the workflow.

## Requirements and scope

Both `image-to-prompt` and [gpt-image-prompting][core] must be available to the
current host. The entry resolves the core by name using host discovery or
supported invocation; it does not assume an installation path or install it.
Using the same source revision for both skills is recommended.

Image inspection requires an accessible image and the host's image-reading
capability. An explicit description can substitute when appropriate, but does not
count as inspection. Default output is a self-contained whole-image text prompt.
Attached-reference or editing prompts require a request to use that mode.
Scoped extraction can return only the requested reusable fragment.

Use this entry when the main work is visual observation or extraction. An image
supplied only as background does not require this entry; honor an explicitly
selected skill. The core owns shared output, language, and revision rules.

This instruction-only workflow writes prompt text. It does not generate or
process images, recover original prompts, or verify reconstruction.

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
Install only image-to-prompt and gpt-image-prompting from
https://github.com/saberuster/skills at <revision> for Codex in project
<project-root>. Follow docs/installation.md. Preserve existing skills and report
the resolved commit, destinations, and checks performed.
```

**Update:**

```text
Update only the existing image-to-prompt and gpt-image-prompting installations
in Codex project <project-root> from https://github.com/saberuster/skills to
<revision>. Follow docs/installation.md. Compare with their recorded source
revisions and preserve local edits; ask me to resolve conflicts.
```

## Usage

In Codex, attach an accessible image:

```text
Use $image-to-prompt to write a self-contained GPT Image prompt describing this
image. Preserve the overall view and visual treatment; no attachment dependence.
```

In Claude Code, provide an image the host can read:

```text
/image-to-prompt Extract only this image's lighting and painted texture into an
English GPT Image prompt for a lighthouse. Choose the scene details freely.
```

The [synthetic cases][examples] describe acceptance criteria, not successful runs.

[Back to the skill catalog][catalog].

[core]: https://github.com/saberuster/skills/blob/main/skills/image-generation/gpt-image-prompting/README.md
[installation]: https://github.com/saberuster/skills/blob/main/docs/installation.md
[examples]: https://github.com/saberuster/skills/blob/main/examples/image-to-prompt.md
[catalog]: https://github.com/saberuster/skills#available-skills
