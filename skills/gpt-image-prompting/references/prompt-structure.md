# Prompt structure

The sections organize a complete generation request, including delivery
requirements. They are an authoring convention, not special GPT Image syntax.
Use natural language under concise titles localized to the prompt language.

## Six sections

| Section | Information to express |
| --- | --- |
| Task and use | What to create or edit, its intended use, and what it should communicate. |
| Image content | Subjects, counts, recognizable attributes, actions, setting, and relationships. |
| Composition and viewpoint | Projection, viewpoint, framing, placement, relative scale, depth, and negative space. |
| Visual treatment | Medium, shape language, color organization, shading, edges, texture, and detail strategy. |
| Output requirements | Final dimensions, background and alpha, format, number and organization of outputs, and applicable asset specifications. |
| Constraints and freedom | Remaining invariants, relevant exclusions, and explicitly flexible details. |

Preserve these roles without requiring every possible field. Place each
requirement where it is most useful; the final section is not a duplicate of
the preceding sections. A requested output size belongs in Output requirements
even when it is also mandatory. Do not invent output specifications for an
illustration or expand a focused edit into an unrelated design exercise.

## Make instructions concrete

- Describe relationships, not just object lists: who holds what, which hand,
  where contact occurs, and what overlaps or remains visible.
- Distinguish screen placement, camera/view direction, and subject facing.
  Use anatomical sides or an established convention when "left" or "right"
  could refer to different things.
- Express visual intent with relevant proportions and relationships. Do not
  claim measured coordinates when they were estimated from an image.
- Use camera language when it helps. A flat icon may need an orthographic view
  and clear silhouette rather than a lens or camera brand.
- Replace filler quality tags with useful instructions about readability,
  shapes, edge treatment, contrast, or detail. Keep specific exclusions that
  prevent a relevant failure; they remain ordinary prompt text.
- Preserve detailed user specifications. Editing for clarity must not erase
  required attributes, literal strings, view order, or allowed variations.

## Example: complete asset prompt

This example assumes the user has supplied the dimensions, palette limit,
alpha rule, and design. It illustrates the English output requested for this
example. Do not adopt these values as defaults for other tasks.

```text
[Task and use]
Create a single pixel-art potion icon for a game inventory.

[Image content]
Show one round glass bottle with a short neck, cork stopper, and red liquid.
Keep its silhouette easy to recognize at the final icon size.

[Composition and viewpoint]
Use a front view. Center the complete bottle with clear space around it.

[Visual treatment]
Use compact pixel clusters, a dark outline, and stepped shading. Concentrate
detail on the liquid level and one small highlight; keep the rest simple.

[Output requirements]
The final asset is one 32 by 32 pixel PNG with a transparent background.
Use at most 12 visible colors. Final alpha values must be either 0 or 255.
Keep the logical pixel grid distinct from any enlarged preview.

[Constraints and freedom]
Include no lettering, labels, surrounding props, or cropped bottle parts.
Small interior highlight shapes may vary within the established palette.
```

All requirements are in the same prompt. The example specifies an intended
final asset; it does not claim that an image has been produced or checked, or
that 32 by 32 is a supported native generation size.
