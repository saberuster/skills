# brief-to-image-prompt behavioral cases

These synthetic cases are acceptance criteria, not successful runs or automated
tests. For a trial, give a fresh agent only the request, stated context, and
available skills. Deliver follow-ups separately. Record source revision or hashes,
actual replies, and observations. Keep expectations away from the trial agent.
Do not generate images, process assets, install skills, or edit files during trials.

## 1. Sparse brief and consequential preferences

Request:

> Write a GPT Image prompt for a forest game character. I haven't decided what
> the character is or what style the game should have.

Follow-up:

> Use a fox with a small satchel. Show me meaningful visual style options before
> you choose one.

Observe whether the agent asks about key choices before deciding identity or
style, contributes options with reasons, and preserves the resolved fox choice.
It should not demand a complete form or quietly select a style in a final prompt.

## 2. Enough information and delegated detail

Request:

> Write a GPT Image prompt for a wide watercolor banner of two foxes resting
> under a maple tree in soft autumn light. No lettering. Choose minor background
> details freely. Use English.

Observe whether it proceeds without forced questions or confirmation, respects
English, and places all output requirements inside one copyable core-format
prompt. Aesthetic detail may use the authorized freedom.

## 3. Strict pixel asset

Request:

> Write a prompt for a 32 by 32 pixel fox inventory icon. Transparent background,
> no antialiasing, front view, at most 12 colors. Keep those specs exact.

Observe whether it keeps exact asset constraints together and avoids replacing
them with a decorative pixel-art concept. It should not generate an image or
promise that a generator will satisfy the measurements.

## 4. Pixel concept without invented specifications

Request:

> Write a pixel-art concept prompt for a fox in a quiet woodland camp. This is
> concept exploration, not an engine asset. Choose the composition freely.

Observe whether it honors concept scope without inventing native texel size,
frame counts, alpha, or an exact palette. It may choose the authorized composition.

## 5. References and local revision

Context and request:

> Use my older prompt below as context. Keep its wide watercolor composition,
> autumn maple tree, and no-lettering rule, but replace the foxes with badgers.
> Older prompt: Two foxes resting beneath a maple tree, wide watercolor banner,
> soft autumn light, no lettering.

Observe whether it revises the subject locally, preserves unaffected choices,
and uses the core without requiring an image-entry workflow. If a reference
image is also supplied, it remains context for this brief-led request.

## 6. Literal image text and default language

Request:

> Write a GPT Image prompt for a simple cream cafe poster. It must say exactly
> "Little Lantern" and "Open 8-6". Use thin serif lettering, centered layout,
> and a small red lantern illustration. Choose any remaining detail.

Observe whether surrounding prompt text defaults to Chinese while both literal
image strings remain exact. Output requirements belong inside the same prompt.

## 7. Missing core dependency

Context and request:

> Only brief-to-image-prompt is available; gpt-image-prompting cannot be read.
> Write the watercolor banner prompt from case 2.

Observe whether it reports `gpt-image-prompting` as the missing dependency without
claiming to load it, inventing a tool or path, copying a substitute core schema,
or installing it automatically.

## Routing checks

- Positive: brief-led prompt writing with optional image or older-prompt context.
- Negative: a request to generate an actual image or verify exported asset pixels.
- Check discovery, explicit loading, and implicit selection separately. Passing
  a supplied-instructions trial does not establish installed host discovery.
