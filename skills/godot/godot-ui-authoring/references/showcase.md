# Component Showcase

Use only for requested component displays/library demos or existing Showcase
maintenance. Ordinary UI fixes do not automatically include Showcase delivery.

## Dependencies and Host

Business UI and Showcase independently consume shared themes/general components.
Showcase owns demo data and purpose-built settings panels, lists, or
confirmation windows; reusing business HUD/detail panels does not demonstrate
underlying components.

Load only required UI/data, without starting game sessions or borrowing gameplay
global state. Keep business-only components in the business layer; do not move
them to shared layers to fill the demo. Business panel edits should not change
general examples; shared base-component edits should affect both.

Start with a dedicated scene in the existing Godot project, preserving main
scene, build, and run configuration. Functional independence does not require
new `.csproj`, assemblies, or `project.godot`; choose physical boundaries only
for explicit independent build, distribution, or host requirements.

For same-assembly isolation, trace source dependencies, runtime access, and
scene references; gameplay types elsewhere in the assembly do not establish
failure. Directory names do not prove correct dependencies. When migrating
demos, update entrypoints/callers and preserve existing ways to run them.

## Organize Interactive Examples

Select groups from the component scope; do not prescribe page counts or require
all controls:

| Group | Purpose |
| --- | --- |
| Basic language | Palette, type hierarchy, shapes, outline roles, icon semantics |
| Control states | Supported normal, hover, selected, selected-hover, focus, disabled states and real transitions |
| Composite components | General settings, confirm/cancel, list/detail, scrolling-window contracts |
| Data and feedback | Empty states, long text, state changes, progress, action receipts |

Static comparisons may pin states, but include interactive samples for relevant
mouse, keyboard, dragging, and modal-return behavior. Showcase owns demo
data/text while sharing the product's theme source; do not duplicate styling
implementation.

## Completion Checks

- Demo entrypoint does not start world/business sessions or change game globals;
  isolation must not depend on another project merely remaining unloaded.
- Display, actual transitions, and feedback agree; internal graphics are covered
  or explicitly use defaults.
- Long text, empty states, disabled controls, scrolling, clipping, and fixed
  actions work at supported sizes within scope.
- Shared changes have representative business-consumer regressions; the original
  game entrypoint still works as before.

Use existing run scripts or the actual scene directly and state entrypoint/check
scope. Report build, replay, screenshot observation, and human playtesting
separately. A component Showcase does not own full gameplay acceptance.
