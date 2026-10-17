# UI State and Input Validation

Choose the smallest scenario distinguishing UI defects from driver defects
within existing build/log/runtime contracts. Follow [Validation and Build
Support](validation.md); do not create another runner or fixed test dimensions.

## Select Affected Combinations

Select representative control types, transitions, data changes, and
window/viewport scaling; do not default to exhaustive Cartesian products. Shared
theme changes cover affected types; ordinary Buttons do not substitute for
radio, checkbox, or slider checks.

| Risk | Action and observation |
| --- | --- |
| Missing combined states | Select then hover/focus; read actual draw mode, resolved theme items, and state; inspect text/graphics against real backgrounds |
| Refresh interrupts interaction | Update text under a stationary pointer; record identity, hover, focus, rectangles; refresh between press/release and inspect action/target |
| Rebuild loses focus | Continue Tab/directional navigation after keyboard selection; inspect fallback for removed/disabled options; navigate elsewhere between focus capture/restoration and verify stale restoration is abandoned |
| Modal layers compete | Open, confirm/cancel, return; inspect focus destination and background receipt of input that should be consumed |
| A segmented object can be dragged across pages | Grab a later visible fragment through the real press/selection path; check the view mapping and logical grab offset, then verify both cancellation and a valid drop, including deliberate paging when supported |
| Application code consumes release and commits its own drop | Use the real GUI drag path; assert the intended change commits exactly once, `GuiIsDragging()` becomes false, and closing/recreating the owning UI produces no drag-preview errors in fresh logs. After explicit engine cancellation, `GuiIsDragSuccessful()` need not be true; semantic success must follow the application result |
| A modal suspends ongoing work | Compare opening during active work with opening while already paused; observe clock, work-animation progress and work-sound playback, then cancel by button and Escape and check restoration of the prior state |
| Layout/clipping | Use long text, empty states, affected ratios/scales; verify fixed actions visible and scroll content reachable |
| Candidate previews reparent targets inside scrollable editors | Use the real press/drag/release path with long content; scroll during a preview, then replace an item that the candidate returns to a palette. Verify release at the visible original target commits, clipped-out positions cannot activate or accept drops, and detached target overlays remain clipped. Cancel a separate attempt and check the original content is restored |

Record actual text/data changes; disabling refresh does not establish stability.
Read effective margins/final rectangles instead of only raw fallback-prone
fields. Wait on bounded layout/state completion conditions; longer fixed delays
are not automatically root-cause fixes.

For segmented drags, do not use a helper that silently selects the first
fragment or changes the viewed page before pressing. Compute the expected
destination from the actual grab offset and check that the fixture satisfies its
real constraints, such as duration, availability, and deadline. For temporary
suspension, establish real activity before testing the running case. Inspect
animation progress and sound playback or scheduling, not only a running flag;
assert ambience and UI behavior according to the intended pause design.

## Check Coordinates and Injection Layer First

Record event-coordinate source and target Viewport. Window/embedder, viewport,
canvas, and control-local coordinates are distinct. Trace stretch,
CanvasLayer/CanvasItem transforms, and driver conversion to avoid duplicate
scaling/missing conversion.

Godot 4.7 `Viewport.push_input(event, in_local_coords)` uses `true` for
coordinates already in that viewport, `false` for embedder coordinates converted
by the engine. Control/canvas coordinates do not qualify merely because named
"local"; transform them to target viewport first. Check actual minor
version/language bindings rather than applying `PushInput(..., true)` to every
failed click. [Viewport
API](https://docs.godotengine.org/en/4.7/classes/class_viewport.html#class-viewport-method-push-input)

Confirm the driver with a known hittable control/coordinates; inspect target
hit/hover, value, focus, or receipts. Successful calls/zero exits do not prove
product receipt. Fix inconsistent driver spaces before moving product controls
or relaxing expectations to accommodate bad events.

Distinguish direct values/callbacks, production input replay, and native
device/window paths. GUI injection validates downstream hit/routing but not OS
focus, device collection, or device-emulation settings. Defects in those layers
need native rechecks; retain limits if unavailable.

## Visible Regions and Evidence

Fixed action bars, confirmation buttons, and nonscrolling information belong
inside designed visible regions. ScrollContainer content may intentionally
exceed clipping; check scrolling reachability/operation. Do not assert every
descendant inside viewport or infer no occlusion from on-screen rectangles
alone.

Theme assertions establish configuration, screenshots establish captured
appearance, and replay establishes actual transitions. Combine evidence for the
defect; one image does not prove continuous hover/focus stability. Sample
Showcase and affected business callers for shared components; report only
executed entries/states.

## Failures and Rechecks

Separate product state/style defects, driver coordinate/timing defects, and
environment issues. Retain run identity, actual size/scale, injection layer,
assertions, logs, and code baseline; do not join one pre-change size with
another post-change entrypoint into a complete pass.

After first failure, perform bounded rechecks distinguishing hypotheses; record
changed conditions/test changes. Later passes after intermittent failures do not
prove root-cause resolution. Retain initial conditions, later results, and
unconfirmed cause; do not rerun indefinitely for green or delete assertions.
