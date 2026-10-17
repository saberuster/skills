# Layout, Themes, and Controls

Use for Godot UI implementation, local styling fixes, and visual review. Start
with project design/actual controls, then verify version-matched theme
items/inheritance.

## Layout Expresses the Gameplay Task

Identify persistent information, current decisions, primary actions, and areas
needed for gameplay before arranging HUD, windows, and feedback. Implement
reference relationships in scenes; copying colors into unrelated navigation,
cards, or spacing is insufficient.

For windows with title/body/action bars, identify background/spacing ownership
separately. When title/footer must touch edges, do not wrap the whole window in
one outer padding; body spacing belongs to the body. Inset titles and other
designs are valid too; edge alignment is not universal.

Identify scrollable content/actions that must remain visible. Use real long
text, empty lists, and disabled reasons to check hierarchy. Cover design
coordinates and supported window ratios, scaling, and actual fonts; one polished
screenshot does not prove every size.

## Style Ownership

- Trace inherited Theme, type variations, and instance overrides. Read final
  resolved items to distinguish intentional default fallback from missing
  styling; do not only search local color assignments.
- Put reused styling in shared Theme/existing variations; preserve meaningful
  instance differences. Factories create/configure, composites own combined
  behavior; native Buttons need not become subclasses.
- Confirm sharing before mutating StyleBoxes/icons/shared Resources. For
  single-instance changes, choose local resources using project-version
  ownership rules so hover/selection does not contaminate other controls.

## Check Controls and States

Inventory only used/affected controls. Mark designed, intentionally inherited,
missing, or unverified; presence does not establish complete styling.

| Control/part | Checks |
| --- | --- |
| Buttons, toggles, options | Background, text, icons, focus overlays, applicable normal/hover/pressed/selected/disabled states; hover/focus after selection |
| Radio/checkbox | Internal box, check, ring, dot graphics and selected/unselected/disabled resources, beyond outer background/text |
| Sliders, scrollbars, range controls | Track, fill, handles/drag parts, actually supported highlight/disabled styling, keyboard/drag feedback |
| Text input, lists, composite windows | Selection/edit/error feedback, focus, clipping/wrapping, scrolling/fixed action regions as behavior requires |

Theme keys/states differ by control; use local APIs, version-matched docs, or
source. For Button types, check `hover_pressed` and `font_hover_pressed_color`;
ordinary hover/pressed settings do not prove selected-hover readability. Focus
does not always replace current colors; observe actual state/style layering.
[Button 4.7
documentation](https://docs.godotengine.org/en/4.7/classes/class_button.html)

## Visual Changes and Geometry Stability

Compare effective content margins, border space, and minimum sizes across
normal, hover, selected, and disabled states. Intentional animation may change
geometry; accidental changes can shift text/hit areas or resemble repeated
hover. Node identity may remain unchanged during this jitter.

Check effective padding instead of only raw `content_margin_*`: negative values
may fall back to StyleBox defaults, such as StyleBoxFlat border widths. Use
project-version effective-margin APIs such as `get_margin` together with final
rectangles. [StyleBox 4.7
documentation](https://docs.godotengine.org/en/4.7/classes/class_stylebox.html)

Distinguish outlines, focus frames, icon strokes, separators, and state bars by
role. Same-role differences need design reasons; different roles need not share
thickness. Do not universalize one project's line widths, corners, or colors.

For drag previews that reparent or project content, capture the target's
authoritative scroll/clipping container when activating the preview. Keep that
owner stable for the preview, while deriving bounds from its current geometry as
layout or scrolling changes. Moving a replaced item into a palette during
candidate projection must not move the original drop region there. Clip detached
drop-target overlays and hit testing to the target's visible region.

## Validation Observations

Inspect key combined states on actual backgrounds, pairing input with selected
values, focus, and action receipts. State boards reveal gaps but cannot replace
click/keyboard paths; equal color fields do not prove contrast. Sample generic
examples and affected business callers for shared components.

These links are maintenance version entrypoints; switch to the actual project
minor version when executing. See also [Theme 4.7
documentation](https://docs.godotengine.org/en/4.7/classes/class_theme.html) for
types, variations, and resource-item APIs. No project upgrade is required.
