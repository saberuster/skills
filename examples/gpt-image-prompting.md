# gpt-image-prompting examples and behavioral cases

These synthetic requests describe expected behavior, not successful trials.
Give a fresh agent the core package and only the stated context and request.
Keep observations away from the trial agent. Permit instruction reads and
prompt text only; do not generate images or operate an asset pipeline.

## 1. Strict pixel specifications in one prompt

Request:

> Organize these approved requirements into one English GPT Image prompt:
> a round red potion bottle, cork stopper, centered front view, dark outline,
> compact pixel clusters, and stepped shading. One final 32 by 32 PNG, no
> background, alpha restricted to 0 or 255, at most 12 visible colors, and
> no text or cropped parts. Interior highlights can vary. Do not generate it.

Observe whether the result is one copyable titled prompt, with the requested
delivery requirements inside it. It should retain the design and counts,
distinguish final asset dimensions from generation dimensions, avoid inventing
API arguments, and make no claim of image production or validation.

## 2. Stylized concept illustration

Request:

> Structure an English prompt for a wide watercolor concept illustration of
> a hilltop observatory. Use rounded architecture, muted blue shadows and
> amber windows, soft washes, a distant three-quarter view, and atmospheric
> depth. Keep the upper left open for a title added later. PNG is sufficient;
> I have no exact resolution requirement. No lettering in the generated image.

Observe whether shape language, edges, color, and depth remain specific.
Pixel-grid, indexed-palette, binary-alpha, animation, and tile requirements
should not appear simply because the core also supports game assets.

## 3. Local revision with consequential changes

Context and request:

> The existing prompt describes a small silver robot with sharp mirror-like
> highlights, centered front view, blue eyes, and a transparent background.
> Change its body to matte clay. Preserve its silhouette, eye color, viewpoint,
> and background requirement. Return the revised prompt in English.

Observe whether material and highlight instructions change together and old
metal reflections disappear. Unaffected identity and output requirements
should remain. This is a prompt revision, not an image-generation request.

## 4. Exact text and independent outputs

Request:

> Write two independently usable English prompts for coordinated flat travel
> posters. Both use teal and cream, blocky shapes, and a single centered title.
> Poster 1 shows a lighthouse and says exactly "NORTH". Poster 2 shows a
> mountain hut and says exactly "SOUTH". Each should be a separate portrait
> image, not a contact sheet. No other words. Keep the order given here.

Observe whether each prompt repeats the needed style and output requirements,
retains the correct text once, and does not depend on "same as above".
Separate images must not become one combined sheet.

## 5. Unresolved conflict

Request:

> Make one final prompt for a single portrait that must show the face entirely
> from the front and entirely from the back at the same time. Do not use a
> mirror, split view, extra head, or extra image. Ask if this is inconsistent.

Observe whether the agent identifies the conflicting requirements and asks
which view should govern instead of inventing a workaround or weakening both.
