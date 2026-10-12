# References, edits, and series

Use these modules only where the task needs them. They add information to the
same six sections, not additional mandatory deliverables.

## Reference mapping

For an explicitly attachment-dependent prompt, identify inputs using stable
names or verified attachment order. State each image's role, the attributes to
inherit, the subject or region they control, and relevant exclusions. Resolve
overlapping authority according to the user's choices.

For example, one image can define character shape while another defines the
palette. Do not also import the second image's objects or the first image's
background without a reason in the request. Separate new generation guided by
references from editing an identified base image.

Standalone text prompts describe the needed features in words. Avoid "match
the reference" or hidden attachment dependencies in such prompts. Preserve
observations provided by the image workflow without inventing unseen surfaces
or claiming that user-supplied descriptions were visually inspected.

## Image edits and prompt revisions

Changing an existing prompt is distinct from requesting an edit to an image.
An image-edit prompt needs an identified base image and an intended change.
State three compatible sets: requested changes, retained attributes, and
necessary consequential adjustments. Remove changes from the preservation set.

A metal-to-clay change can affect surface reflections and highlights while
leaving identity and composition intact. A request to isolate a hairstyle
retains that element's shape and color; it should not carry over full-body
framing, clothing, or facial details that recreate the removed person.

Changing a viewpoint may reveal unknown surfaces. Treat any completion as a
design choice within the user's granted freedom, not an observed property.
Ask about consequential unresolved choices rather than silently redesigning
the subject. Reference presence alone does not authorize an image-edit task.

## Exact text and layout

Preserve literal text, punctuation, case, and specified line breaks. Record
placement, occurrence count, hierarchy, and relevant font characteristics.
Separate image lettering from instructions. Do not translate, correct, or
add text without authorization, or add "no text" where lettering is required.
Unclear source text is not permission to invent words.

## Related outputs

Keep shared identity, proportions, shape language, palette, and rendering
separate from requested per-output changes. A feature that varies must not
also be locked. State the number, order, and organization of outputs; retain
the user's choice of independent images or a combined sheet.

For each independently usable prompt, include its relevant shared baseline
and reference mapping. A shared sheet can state the baseline once and list
its cells or views. Avoid vague instructions such as "same as before".

For turnarounds, distinguish viewpoint, subject facing, and screen placement.
Use an agreed scale and stable datum such as head height or foot baseline.
Do not stretch views to force equal bounding boxes; silhouettes can differ
with viewpoint. For animation, include relevant states, frame order, canvas,
anchors, and timing when supplied.

Treat multiview consistency, pixel-grid purity, slicing, loops, and engine
readiness as requested outcomes, not as accomplishments of prompt writing.
