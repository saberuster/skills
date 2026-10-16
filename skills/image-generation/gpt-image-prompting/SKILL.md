---
name: gpt-image-prompting
description: >-
  Structure established image requirements, revise existing GPT Image prompts,
  or review them without rewriting. Provides shared output rules for brief and
  reference-image entry skills. Produces text only, not images or assets.
---

# GPT Image Prompting

Own prompt wording, output structure, and consistency. Use directly for known
requirements or existing prompts. A calling entry owns brief development,
image observation, and creative choices; this core needs no other skill.

## Resolve scope and information

- Follow the requested deliverable: review-only returns findings and suggested
  corrections without a replacement prompt; a fragment request returns only
  the reusable text for that scope; otherwise compose or revise full prompts.
- Preserve intent, accepted choices, literal image text, and exact requirements.
  Later explicit changes replace only affected requirements. Observations and
  assumptions do not override instructions or become verified facts.
- When drafting or revising, ask about conflicting hard requirements, missing
  information necessary for the deliverable, and consequential choices the user
  has not delegated. Do not silently choose identity, style, or asset specifications
  when that would materially change the intended result. Omit optional gaps;
  omission does not grant creative freedom. Use freedom already granted.
- Ask directly when used alone; when an entry is active, let it resolve the
  missing choices. Do not require a full form or reconfirm settled decisions.

## Compose and revise

Use these semantic sections for full prompts. They are an authoring convention,
not special GPT Image syntax. Keep relevant sections in order, omit empty ones,
and state each requirement once. Do not expand a fragment into a full prompt.

| Section | Information to express |
| --- | --- |
| Task and use | What to create or edit, its use, and intended communication. |
| Image content | Subjects, counts, attributes, actions, setting, and relationships. |
| Composition and viewpoint | View, framing, placement, scale, depth, and negative space. |
| Visual treatment | Medium, shapes, color, shading, edges, texture, and detail. |
| Output requirements | Final dimensions, background and alpha, format, count, layout, and asset specifications. |
| Constraints and freedom | Remaining invariants, exclusions, and explicitly flexible details. |

- Describe relationships, contact, and overlaps, not just object lists.
  Distinguish screen placement, camera direction, and subject facing; clarify
  anatomical sides when needed. Do not present estimated coordinates as measured.
- Prefer useful proportions, readability, and edge or detail instructions to
  filler quality tags. Camera terms and exclusions should serve the task.
- Refine wording without losing required attributes, literal strings, view order,
  or permitted variations. For revisions, remove superseded instructions and
  adjust their consequences while preserving unaffected choices.

Read conditional guidance only when needed:

| Situation | Reference |
| --- | --- |
| Style description, stylized or pixel art, or game-asset specifications | [Visual styles and assets](references/visual-styles-and-assets.md) |
| Attached references, image editing, exact lettering, or related outputs | [References, edits, and series](references/references-edits-and-series.md) |

## Deliver the result

Default to Chinese; preserve literal image text rather than translating it.
Honor the requested language and format. Full prompts use natural-language
section titles inside a fenced text block; fragments need only the requested
text. A requested JSON or YAML representation is not an API schema.

For full-prompt requests, default to one. If multiple independent prompts are
requested, make each self-contained and separately copyable, repeating its baseline
instead of "same as above". Preserve requested order and separate-image versus
combined-sheet organization. Only explicitly reference-dependent tasks may
rely on identified attachments.

Keep applicable delivery requirements inside the prompt, not in a separate
specification or handoff appendix. Do not invent specs to fill sections or add
unrelated ones to fragments. Distinguish final asset dimensions from generation
dimensions or enlarged previews. Requirements express desired outcomes, not
verified properties or promises that prose can enforce an exact export.

Check counts, relationships, directions, literal text, reference roles, and
constraints across the requested output. Keep analysis and material uncertainty
outside copyable prompt text, briefly. Review-only findings describe prompt
issues, not validated image defects; report no material issues when appropriate.

This skill ends at text. Do not invent tool settings, generate or edit images,
export or validate assets, install tooling, or launch a production workflow.
