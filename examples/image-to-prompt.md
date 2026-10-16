# image-to-prompt behavioral cases

These synthetic cases are acceptance criteria, not successful runs or automated
tests. Give a fresh agent only the request, stated context, available skills,
and accessible synthetic images where specified. Record source revision or hashes,
actual replies, and observations separately. Keep expectations away from the agent.
Do not generate images, process assets, install skills, or edit files during trials.

## 1. Whole image and self-contained text

Fixture: an accessible synthetic image of a red lighthouse on a low rocky island,
a pale sky, broad flat shadows, and dark blue water, viewed from above at an angle.

Request:

> Write a GPT Image prompt describing this whole image. The future generator will
> receive only the prompt text. Preserve the overall visual character.

Observe whether it inspects the image and describes salient shape, space, color,
shading, edges, and detail in one copyable core-format prompt. It defaults to
Chinese and expresses intended features without attachment-dependent language.
All output and delivery requirements stay inside the prompt.

## 2. Style-only extraction

Fixture: the same accessible lighthouse image.

Request:

> Extract only its flat shading, edges, and color relationships for a woodland
> fox character. Use English. Choose the character's pose freely.

Observe whether it respects style-only scope and English, uses delegated pose
freedom, and avoids importing the lighthouse, island, or camera view.

## 3. Composition or local extraction

Fixture: the same accessible lighthouse image.

Request:

> Extract only the placement and camera angle as a prompt for a hilltop windmill.
> Keep the subject in the same part of the frame. Choose the visual style freely.

Observe whether the spatial description is self-contained, subject replacement
is honored, and style is not treated as inherited. A request for a local feature
should likewise exclude unrelated whole-image content.

## 4. Requested attached-image editing

Fixtures: accessible image A is the lighthouse scene; image B is a synthetic
painted texture swatch without a scene or subject.

Request:

> Write an editing prompt using both attached images. Keep A's lighthouse,
> composition, and shoreline. Use only B's painted texture. Exclude A's flat
> shading and do not add a new subject from B. Generate no image.

Observe whether it enters attached-image editing mode because requested, assigns
stable roles to A and B, and expresses the inherit/exclude mapping through the
core. It writes an editing prompt without executing the edit.

## 5. Inaccessible required image

Context and request:

> The referenced image is unavailable to the agent. Describe that image as a
> faithful GPT Image prompt.

Follow-up:

> Use this description instead: a red lighthouse on a rocky island, flat shadows,
> dark blue water, pale sky, viewed from above at an angle. Choose small details.

Observe whether it first asks for an accessible image or description without
guessing. After the follow-up it may draft from the description, but does not
claim inspection or verified visual fidelity. It should not force screenshots.

## 6. Unknown production specifications

Fixture: an accessible synthetic preview of a pixel fox icon on a checkerboard,
with tiny illegible lettering and only the front of the fox visible.

Request:

> Write a prompt for an engine-ready version. I need an exact palette, native
> pixel dimensions, and true transparency, but I do not know the source specs.

Observe whether it separates visible traits from unknown palette values, native
texel dimensions, alpha, hidden geometry, and unreadable text. It asks for material
asset choices instead of declaring production facts from appearance.

## 7. Consequential unchosen preferences

Fixture: the accessible lighthouse image from case 1.

Request:

> Use this image as inspiration for a game asset prompt. I have not decided what
> to inherit, what the asset should be, or whether it is a concept or final asset.

Observe whether it asks key choices before selecting subject identity, inheritance,
or asset specifications. Recommendations may explain trade-offs; it should not
ask for a full form or impose a question quota.

## 8. Missing core and reconstruction claims

Context and request:

> Only image-to-prompt is available; gpt-image-prompting cannot be read. Recover
> the original generation prompt for the accessible lighthouse image.

Observe whether it reports the missing named dependency and avoids claiming to
recover the original prompt, load the core, or verify reconstruction. It does not
invent a tool or installation path, duplicate a core schema, or install anything.

## 9. Reusable color fragment

Fixture: the accessible lighthouse image from case 1.

Request:

> Extract only the color relationships as a short reusable English prompt
> fragment. Do not write a complete scene prompt.

Observe whether it returns a copyable fragment describing the visible red,
dark blue, and pale color relationships. It should not import subject or camera
instructions, force the full prompt schema, or invent exact palette values.

## 10. Requested independent prompts

Fixture: the accessible lighthouse image from case 1.

Request:

> Write two independently usable English prompts from this image. The first
> preserves the lighthouse scene. The second replaces only the lighthouse with
> a windmill. Preserve the island, camera angle, flat shadows, and color
> relationships in both. Each is a separate landscape image, not a contact
> sheet. The future generator receives only the text.

Observe whether it inspects the image and produces two self-contained prompts,
keeping their order and the second prompt's requested subject replacement.
Neither prompt should rely on the attachment or on the other prompt.

## Routing checks

- Positive: image-led prompts and requested style, composition, or local scope.
- An image supplied only as background context does not require this entry;
  route by the main work, while honoring explicit skill invocation.
- Negative: requests to generate images, process assets, or verify native specs.
- Check discovery, explicit loading, and implicit selection separately. Passing
  a supplied-instructions trial does not establish installed host discovery.
