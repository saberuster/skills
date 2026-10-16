---
name: image-to-prompt
description: >-
  Describe an accessible reference image as a GPT Image prompt, or extract its
  requested style, composition, or local features. Use for prompt writing,
  not image generation, processing, or recovering an original prompt.
---

# Image to Prompt

Translate visible image information into a GPT Image prompt through the current
conversation. Produce text only; do not generate, process, or verify images, or
claim to recover the original generation prompt.

## Load the shared contract

Load `gpt-image-prompting` by name through the current host's skill discovery,
available skill location, or supported skill invocation. Do not invent a `Skill`
tool, assume sibling or absolute installation paths, or install the dependency.
If missing or unreadable, report the named dependency without claiming to apply
it. Both skills must be available; using the same source revision is recommended.
The core owns prompt structure, language, and reference roles.

## Inspect and resolve scope

- Inspect accessible images before describing them. Prioritize salient shape,
  spatial relationships, color, shading, edges, and detail over incidental noise.
- Default to the whole image and self-contained text that works without attaching
  the reference. Honor requested style-only, composition-only, or local extraction
  instead of importing unrelated features.
- Ask about consequential unresolved user choices before deciding them. Recommend
  meaningful options with reasons when useful; do not require a whole form or
  repeat questions already answered. Honor delegated creative freedom.
- Separate observations from guesses. Do not invent hidden sides, unreadable
  text, native texel dimensions, exact palette values, or an alpha channel from
  visual appearance. Ask for unknown production specifications when they matter.
- If a required image is inaccessible, ask for an accessible image or description.
  Work from an explicit description if provided, but do not call it inspected or
  pretend its visual details are verified.

## Compose and revise

Use resolved observations and choices with `gpt-image-prompting` to deliver one
copyable prompt with output and delivery requirements inside it. Default to
Chinese prompt text, preserve readable literal image text, and honor the user's
language and format overrides through the core.

Use attached-image mode or an image-editing prompt only when requested. Establish
stable reference roles and an explicit inherit/exclude mapping through the core.
For self-contained output, express intended features in text rather than
instructions such as "match the attached image."

Preserve unaffected choices during local revisions. Note material uncertainty
outside the prompt; do not promise exact reconstruction or verified results.

The [acceptance cases][examples] are evaluation material, not a runtime checklist.

[examples]: https://github.com/saberuster/skills/blob/main/examples/image-to-prompt.md
