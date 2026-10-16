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

Observe automatic selection separately: this settled local revision belongs
directly to `gpt-image-prompting`, which preserves unaffected choices. An image
supplied only as background context does not make image extraction the main task.

Explicit-invocation variant:

> Use $brief-to-image-prompt for the same revision.

Observe whether it honors the named skill, uses its core dependency, and performs
the local revision without reopening settled choices or requiring image extraction.

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

## 8. Optional unspecified details

Request:

> Use $brief-to-image-prompt to write an English prompt for a wide watercolor
> banner of two foxes resting beneath a maple tree in soft autumn light.
> No lettering.

Observe whether it drafts from the supplied choices without blocking on optional
details such as clothing, extra scenery, or precise poses. It should leave those
details unspecified instead of treating silence as permission to invent them.

## 9. Requested independent prompts

Request:

> Use $brief-to-image-prompt to write two separate English prompts for woodland
> banners. Both use watercolor, soft autumn light, and no lettering. The first
> shows two foxes resting beneath a maple tree; the second shows two badgers
> resting beneath an oak. Each is a separate wide image. Keep this order.

Observe whether it honors the explicit entry skill and returns two individually
copyable, self-contained prompts with each banner's subject, tree, style, and
delivery requirements. It should not return one combined image or require the
second prompt to refer to the first.

## Routing checks

- Positive: creative brief clarification with optional image or older-prompt
  context, and explicit invocation of this skill.
- Settled requirements, local prompt revision, and prompt review route directly
  to the core when no entry skill is explicitly requested.
- Negative: a request to generate an actual image or verify exported asset pixels.
- Check discovery, explicit loading, and implicit selection separately. Passing
  a supplied-instructions trial does not establish installed host discovery.
