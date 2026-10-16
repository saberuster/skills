---
name: brief-to-image-prompt
description: >-
  Develop an idea or incomplete brief into GPT Image prompts by resolving
  creative requirements and consequential preferences. Use when the main task
  is brief development, not merely formatting or editing an established prompt.
  Produces text only, not images or processed assets.
---

# Brief to Image Prompt

Develop creative requirements through the current conversation. For automatic
selection, known requirements and local prompt edits belong to
`gpt-image-prompting`; visual extraction belongs to `image-to-prompt`.
Honor an explicitly selected entry and use context without needless switching.
Produce text only; do not generate images or process or verify assets.

## Load the shared contract

Load `gpt-image-prompting` through host discovery, its available skill location,
or supported invocation. Do not invent tools or installation paths or install
it. If unavailable, report the missing dependency without pretending to apply
it. Both skills are required; the same source revision is recommended.
The core owns clarification thresholds, language, output modes, and revisions.

## Resolve the brief

- Read relevant conversation, references, and older prompts. An image used as
  background context does not by itself require another entry.
- Use the core's clarification threshold to resolve consequential creative
  choices. Offer meaningful options with reasons when useful, without imposing
  a question quota. Complete briefs can proceed immediately.
- Clean up supplied wording and organize known constraints independently while
  consequential choices remain open. Do not treat an undecided option as accepted
  or silently settle it in a finished prompt.
- Distinguish exact production requirements from concept goals. Keep explicit
  pixel, frame, palette, text, transparency, and delivery constraints exact;
  do not invent technical specifications for concept exploration.

## Deliver

Pass resolved requirements to `gpt-image-prompting` and follow its output and
revision rules for the requested deliverable.

The [acceptance cases][examples] are evaluation material, not a runtime checklist.

[examples]: https://github.com/saberuster/skills/blob/main/examples/brief-to-image-prompt.md
