# Runtime, Lifecycle, and Communication

Use for script-level instantiation, SceneTree lifetime, signals, input, and
async boundaries. Match APIs and duplication semantics to the actual project
minor version.

## Instantiation and Lifecycle

- Instantiate through typed/explicit creation boundaries when the root contract
  is known.
- Inject required state before `AddChild()` so `_enter_tree()`, `_ready()`,
  `_EnterTree()`, `_Ready()`, and child initialization see valid objects.
- Constructors handle field defaults/code-owned internal initialization;
  tree-membership operations belong in lifecycle callbacks.
- Use scene-unique names within the current scene contract, never across
  instance, parent, or sibling ownership boundaries.
- Preserve initialization/cleanup actually required by project base classes
  through explicit base calls or sealed template methods; do not call
  mechanically without a contract.
- Clear static instance references only if still pointing to the object exiting.
- Do not disguise missing scene nodes/singletons with detached `new NodeType()`
  objects.

## Signals, Events, and Dependencies

- Godot signals suit scene/editor connections, cross-language observers, and
  Variant boundaries.
- Ordinary language events suit same-language notifications when they preserve
  types/lifetimes more clearly.
- Use narrow direct calls for commands/queries with one required target; do not
  hide targets through signals, callables, or global buses.
- Godot usually disconnects connections associated with freed objects, but
  captured delegates, longer-lived emitters, and custom subscriptions may need
  explicit cleanup.
- Keep registration/unregistration and subscription/unsubscription in the same
  ownership boundary.

## Semantic Input

- Map semantic actions/intents through `InputMap` or project adapters.
- Keep keyboard, mouse, gamepad, touch, dead zones, and remapping at the input
  boundary.
- Create owner-bound input scopes only when multiple modal layers actually
  compete.
- Remove matching scopes/tokens when owners exit; do not blindly pop a shared
  stack.

## Dynamic UI Refresh and Interaction State

For countdowns, live lists, or selection feedback causing hover jitter, lost
focus, or interrupted clicks, trace refresh calls before inferring performance
problems from visual symptoms.

1. Record business identifiers/control instance identity, text/data changes,
   hover, focus, and rectangles. Distinguish destruction/recreation, same-node
   style geometry, and parent layout/scroll movement; mechanisms may coexist.
2. Separate content/structure changes. Update existing controls for
   countdown/display-state changes; adjust structure by stable business
   identifiers for additions, removals, or sorting. Do not use frequently
   changing text as a full-list rebuild signature.
3. Check effective margins, minimum sizes, and hit areas after updates. Equal
   raw normal/hover fields may resolve to different fallbacks. Use
   version-matched effective values and actual geometry so text displacement is
   not misdiagnosed as node recreation.
4. For necessary rebuilds, capture semantic option identifiers before freeing
   old nodes. After new controls enter the tree with valid state, restore focus
   only to corresponding controls still present, visible, and interactive. Use
   established UI fallback for removed/disabled items; do not rely on stale
   references/indices. Schedule restoration only if this region originally owned
   focus; recheck later navigation has not superseded intent before restoring.
   Abandon stale requests if the player moves focus, the region closes, or a new
   update replaces the rebuild while awaiting entry/layout. Existing
   interaction/update generations may establish this; a start-of-update snapshot
   alone must not steal focus back.
5. Check refreshed handlers target current objects without duplicate
   subscriptions. Virtualized/reused closures must not submit old identifiers.
   Simple lists need no generic diff framework/global focus manager.

Validation must include real data updates: refresh repeatedly under a stationary
pointer observing identity, hover, and focus; select by keyboard and continue
navigation; move elsewhere after focus capture before restoration; update
between press/release and confirm the product action without targeting another
item. Pausing countdowns/disabling refresh is not a fix.

Structural changes, virtualization, and full-page replacements may use different
strategies preserving player selection/intent; "never rebuild" is not a rule.
Large-collection performance needs separate evidence; small-list interaction
passes do not prove it. Collect real input/rendering evidence through existing
project entrypoints when needed; mark runtime results unobserved for static
review.

## Drag Coordinates and Temporary Suspension

- When selection can scroll, page, or reframe a view, trace the press event
  through selection and drag arming. Capture the pointer-to-object offset in a
  consistent view mapping; a selection refresh must not reinterpret the original
  press under a different mapping. Grabbing a later visible fragment of one
  logical object must retain the offset to the movable object's origin. During
  deliberate drag scrolling or paging, use the updated pointer mapping while
  preserving that offset; do not disable navigation as a blanket fix.
- If application code consumes a release in `_Input` and commits its own drop,
  check whether it bypassed normal GUI drag cleanup. Capture any needed preview
  handoff geometry before ending the drag. Settle the application transaction
  and clear its active-drag token before ending a still-active Viewport drag
  (`GuiCancelDrag()` in Godot 4.7 C#). Let Godot free its drag-preview
  `Control`; do not free it as application-owned content. Guard
  `NotificationDragEnd` against already-settled tokens so cleanup cannot reject
  or resubmit a committed command.
- In that custom path, judge semantic success from the application transaction
  and postconditions. `GuiIsDragSuccessful()` reports the engine GUI drop result
  and may be false after explicit cancellation even though the application
  committed. Preserve normal GUI completion for ordinary `_DropData` paths; do
  not cancel every release unconditionally.
- When a modal temporarily suspends gameplay, distinguish the player's running
  intent from effective running state. Notify affected presentation consumers on
  both suspension and release, even if the normal simulation update now returns
  early. Keep simulation time, work animations, and work sounds consistent with
  the intended pause behavior, and restore the prior running or paused intent on
  cancellation. UI animation and ambience may continue when the product calls
  for it; this does not require globally pausing the SceneTree.

## Async Work and Cleanup

- Make async results observable. Use non-awaitable entries only when framework
  signatures require them, handling exceptions at that boundary.
- Tie node-owned task cancellation to tree membership/disposal lifetime.
- After each resumed wait, recheck cancellation, Godot validity, SceneTree, and
  ownership.
- Keep domain async work independent of node lifetime where possible; adapt
  cancellation/scene access at the owning node boundary.
