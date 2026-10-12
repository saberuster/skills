---
name: brief-to-image-prompt
description: >-
  Turn an idea or brief into a GPT Image prompt, clarifying consequential
  creative preferences first. Use for prompt writing and revision, not image
  generation or asset processing.
---

# Brief to Image Prompt

Develop a brief into a usable GPT Image prompt through the current conversation.
Preserve intent, constraints, settled choices, and delegated creative freedom.
Produce text only; do not generate images or process or verify assets.

## Load the shared contract

Load `gpt-image-prompting` by name through the current host's skill discovery,
available skill location, or supported skill invocation. Do not invent a `Skill`
tool, assume sibling or absolute installation paths, or install the dependency.
If missing or unreadable, report the named dependency without claiming to apply
it. Both skills must be available; using the same source revision is recommended.
The core owns prompt structure, language, and output contracts.

## Resolve the brief

- Read the brief, conversation, reference images, and older prompts as relevant
  context. The primary request owns this entry; an image used as context does
  not require another entry skill.
- Ask about consequential unresolved preferences before deciding style, subject
  identity, composition, purpose, or asset specifications. Offer meaningfully
  different options with concise reasons when they help the user choose.
- Ask only about gaps that could change the result. Do not impose a whole form,
  question quota, or confirmation when enough information is supplied. Use
  creative freedom where the user has authorized it.
- Clean up supplied wording and organize known constraints independently while
  consequential choices remain open. Do not treat an undecided option as accepted
  or silently settle it in a finished prompt.
- Distinguish exact production requirements from concept goals. Keep explicit
  pixel, frame, palette, text, transparency, and delivery constraints exact;
  ask when a missing asset specification matters instead of inventing it.

## Compose and revise

Use the resolved brief with `gpt-image-prompting` to deliver one copyable prompt.
Keep output and delivery requirements inside that prompt. Default to Chinese
prompt text, preserve literal image text, and honor the user's language and
format overrides through the core.

Revise locally when a choice changes; preserve unaffected decisions. Explain
only material assumptions or unresolved choices outside the prompt. Do not
promise generated results or claim verification of the prompt's effects.

The [acceptance cases][examples] are evaluation material, not a runtime checklist.

[examples]: https://github.com/saberuster/skills/blob/main/examples/brief-to-image-prompt.md
