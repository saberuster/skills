---
name: image-to-prompt
description: >-
  Observe accessible reference images and express their content or selected
  style, composition, or features as GPT Image prompts or reusable fragments.
  Use when visual information must be extracted, not for text-only prompt
  edits, image generation, processing, or recovering an original prompt.
---

# Image to Prompt

Translate visible information into prompt text. For automatic selection,
text-only prompt edits belong to `gpt-image-prompting`; creative brief development
belongs to `brief-to-image-prompt`. Honor an explicitly selected entry; an image
appearing only as background context does not require switching to this skill.
Do not generate, process, or verify images or claim to recover original prompts.

## Load the shared contract

Load `gpt-image-prompting` through host discovery, its available skill location,
or supported invocation. Do not invent tools or installation paths or install
it. If unavailable, report the missing dependency without pretending to apply
it. Both skills are required; the same source revision is recommended.
The core owns clarification thresholds, language, output modes, and revisions.

## Inspect and resolve scope

- Inspect accessible images before describing them. Prioritize salient shape,
  spatial relationships, color, shading, edges, and detail over incidental noise.
- Default to the whole image and self-contained text that works without attaching
  the reference. Honor requested style-only, composition-only, or local extraction
  instead of importing unrelated features or inventing a target subject.
- Resolve inheritance and intended use with the core's clarification threshold;
  offer meaningful options when useful. A reusable fragment does not require a
  new subject, output dimensions, or unrelated creative choices.
- Separate observations from guesses. Do not invent hidden sides, unreadable
  text, native texel dimensions, exact palette values, or an alpha channel from
  visual appearance. Ask for unknown production specifications when they matter.
- If a required image is inaccessible, ask for an accessible image or description.
  Work from an explicit description if provided, but do not call it inspected or
  pretend its visual details are verified.

## Deliver

Use attached-image mode or an image-editing prompt only when requested. Establish
stable reference roles and an explicit inherit/exclude mapping through the core.
For self-contained output, express intended features in text rather than
instructions such as "match the attached image."

Pass resolved observations and choices to `gpt-image-prompting` and follow its
output and revision rules for the requested deliverable.

The [acceptance cases][examples] are evaluation material, not a runtime checklist.

[examples]: https://github.com/saberuster/skills/blob/main/examples/image-to-prompt.md
