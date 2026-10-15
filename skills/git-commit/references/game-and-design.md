# Game and design projects

Read this supplement when the proposed commit changes gameplay, visual design,
creative assets, or design deliverables. Keep the main skill's format and project
precedence. This reference does not authorize staging, committing, or mutating
checks for a message-only or review request.

## Choose type and scope

Choose an existing type by the change's intent, including for binary assets.
Use `feat` for new gameplay or interaction, `fix` for an established defect, and
`docs` for design rationale. `style` means code formatting, not art or UI design.
Do not classify assets as `chore` merely because they are images or models.
For tuning and visual revisions, use project conventions and the actual purpose;
do not invent a defect or add a new type taxonomy.

Reuse established system or experience scopes such as `combat`, `inventory`,
`save`, `hud`, or `onboarding`; design projects may use `illustration` or
`animation`. Omit scope when it adds little. Avoid a registry for every asset.

```text
feat(combat): add hit pause for heavy attacks
fix(hud): prevent health text overlap at small resolutions
docs(design): record inventory layout tradeoffs
```

## Explain intent and evidence in the body

For non-obvious changes to feel, balance, layout, or visual hierarchy, briefly
explain the problem or hypothesis, what changed, and the expected effect. Keep
self-explanatory commits short. Distinguish an intended benefit from an observed
result; do not claim improved feel, balance, or comprehension from a passing test.

```text
feat(combat): add hit pause for heavy attacks

Heavy and light attacks currently have similar impact feedback.
Add a short pause to make heavy hits feel more forceful.

Checked animation recovery and attack chaining; feel awaits playtesting.
```

## Keep assets and dependencies complete

Apply the main skill's intent grouping and dependency ordering. Keep code,
scenes, assets, and required metadata for one coherent intent together when
needed for a usable intermediate version. Split an unrelated UI fix from a
combat feature; keep that feature's script, scene, and effect assets complete.
Do not split solely by file type. Inspect binary changes using available previews
or source tools; a filename or diff summary alone may not explain the change.

Follow project rules for editable sources, exports, import metadata, caches, and
large files. Check relevant references and external dependencies; avoid missing
textures, fonts, audio, linked files, or stale exports needed by this change.
A design handoff should retain required editable sources and working links.

## Identify compatibility impact

Consider existing saves, replays, mods, public resource identifiers, and shared
component interfaces when the change touches them. Base breaking markers on an
actual incompatible contract, including contracts used by asset consumers.
A major art revision, UI redesign, or balance adjustment alone does not imply
`!`. Describe affected consumers and the supported migration or known loss of
compatibility when breaking markers apply; do not invent a migration path.

## Choose proportionate checks

Honor required project checks and reuse relevant evidence. Choose additional
checks for the changed behavior and available tools; this table is guidance.
Report checks actually performed and any gaps without claiming unobserved results.

| Change | Relevant checks |
| --- | --- |
| Gameplay logic or tuning | Related tests or reproducible runtime scenarios; successful execution does not establish balance. |
| UI, animation, or visuals | Inspect actual output at affected sizes, states, or animation phases. |
| Images, audio, models, or scenes | Open or import relevant files and check required dependencies and references. |
| Design files, prototypes, or documents | Check editability, links, needed exports, and whether a proposal or accepted decision is identified. |
| Saves, replays, or public interfaces | Exercise affected old data or callers and identify migration or invalidation scope. |

Do not require the full test suite, screenshots, or human playtesting for every
commit. Record pending playtesting when relevant; automated checks and visual
inspection do not establish player experience or human acceptance.
