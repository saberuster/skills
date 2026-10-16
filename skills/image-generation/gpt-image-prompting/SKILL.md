---
name: gpt-image-prompting
description: >-
  Structure, revise, or check established image requirements as a complete
  GPT Image prompt. Provides the shared prompt standard used by brief and
  reference-image entry skills. Produces prompt text, including delivery
  requirements; does not generate images or process assets.
---

# GPT Image Prompting

Express established requirements as one self-contained, copyable GPT Image
prompt. Own the prompt structure and consistency rules; the calling workflow
owns brief development, image observation, and consequential creative choices.
This skill also works directly on sufficiently specified requirements or an
existing prompt. No other skill is required by this core.

## Use the available information

- Preserve the user's intent, accepted choices, literal image text, and scope.
  Distinguish explicit requirements, supplied observations, and assumptions
  internally; do not put this bookkeeping into the image prompt.
- A later explicit change replaces the affected earlier requirement. Keep
  unaffected requirements. Observations and assumptions do not override the
  user's instructions. Ask about incompatible current hard requirements.
- If a consequential preference is unresolved, surface the decision for the
  current workflow to ask the user before finalizing. Do not choose a style,
  subject design, use, or technical specification merely to fill a section.
  Honor creative freedom the user has already delegated.
- Refine wording and organization without changing meaning. Optional unknowns
  may be omitted; an unknown required specification needs clarification.
  Do not require the user to complete a form or reconfirm settled choices.

## Apply the shared standard

Read [prompt-structure.md](references/prompt-structure.md) when composing or
revising the prompt. It defines six semantic sections:

1. Task and use
2. Image content
3. Composition and viewpoint
4. Visual treatment
5. Output requirements
6. Constraints and freedom

Use the titles in the prompt language. Include only relevant, supported
content; omit empty or irrelevant sections. Keep the meaning and order stable
without padding a small request. State a requirement once, in its appropriate
section, and keep related statements consistent.

Read conditional guidance only when needed:

| Situation | Reference |
| --- | --- |
| Style description, stylized or pixel art, or game-asset specifications | [Visual styles and assets](references/visual-styles-and-assets.md) |
| Attached references, image editing, exact lettering, or related outputs | [References, edits, and series](references/references-edits-and-series.md) |

## Return the prompt

Default to Chinese, with titled natural-language sections inside one fenced
text block. Follow an explicitly requested language or representation instead.
Translate instructions and headings, not literal text meant to appear in the
image. A requested JSON or YAML representation is not an API schema.

Delivery requirements belong inside the prompt, including final dimensions,
transparency, file format, count, layout, and applicable asset constraints.
Do not split them into a separate specification or handoff appendix. Describe
them as desired outcomes, not as already verified properties. Distinguish a
final asset's dimensions from an intermediate generation or enlarged preview.
Do not invent tool settings or promise that prose enforces an exact export.

For separately usable prompts, repeat the necessary shared information in each;
do not rely on "same as above". Only an explicitly reference-dependent task
may rely on identified attachments. Keep analysis and material uncertainty
outside the copyable prompt, briefly and only when useful.

Before returning, check subject counts, relationships, directions, literal
text, reference roles, output organization, and constraints across sections.
For revisions, remove superseded requirements and resolve affected descriptions
without changing unrelated choices. Prompt review does not validate generated
pixels, asset readiness, or a model's actual output.

This skill ends at prompt text. It does not generate or edit images, export or
validate assets, install tooling, or launch another production workflow.
