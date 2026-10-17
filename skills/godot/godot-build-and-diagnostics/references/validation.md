# Godot Validation and Build Support

Map risk-matched validation contracts to Godot build, import, serialization,
editor, and runtime evidence.

## Diagnose Before Editing

1. Reproduce using documented repository commands/editor paths.
2. Record command, exit status, relevant logs, actual minor version, and .NET
   version if applicable.
3. Classify project code, Godot/toolchain, import/serialization,
   environment/permissions, or log-path failures.
4. Change the smallest supported boundary and validate the same path.

Do not turn build, plugin, permission, or log-path failures into scene/Resource
refactors without evidence.

`.NET: Assemblies not found` after a successful build can be an
execution-environment symptom. Verify the engine-side and project assemblies
actually exist and inspect resolved absolute project/log paths; when authorized,
compare the same engine and build in the intended execution environment. Success
there supports an environment-dependent failure, not a specific permission cause
or a universal diagnosis for this message. Do not default to elevation or bypass
a failed log preflight.

## Evidence Levels

- Static/compile: syntax, types, analyzers, non-runtime contracts.
- Editor/import: settings, exports, import state, editor-only configuration.
- Serialization: scene/Resource loading, UID/reference integrity, save round
  trips.
- Headless runtime: SceneTree startup, lifecycles, autoload, transitions,
  nonvisual integration.
- Windowed: UI, focus, physical input, viewport, rendering, cameras, audio,
  editor interaction.

Run required levels only, but compilation does not replace import, scene
loading, runtime, UI, or input evidence. Put test adapters, replacement scenes,
fixed randomness, and external-service doubles at composition roots using
production contracts.

## Choose Execution and Control Paths

Inventory existing drivers, test scenes, validation scripts, and version-matched
Godot APIs first. Run needed entrypoints directly from CLI; establish behavior
through object state, functional logs, assertions, saves, or stable screenshots.
Do not open the editor/Computer Use solely to click Run.

- Prefer headless CLI for nonvisual loading, lifecycles, autoload, transitions,
  and integration.
- For rendering without editor context, launch the actual game/scene directly;
  prefer trustworthy API screenshots/state.
- For import refresh, editor serialization, `EditorScript`, tools, or plugin
  context, launch editor/API entrypoints.
- For repeated semantic input/sequences, prefer drivers consuming production
  actions/contracts; inspect state/logs instead of treating driver calls as
  behavior success.

Even for windowed evidence, go directly to the entrypoint: `--editor --path
<project-root>`, `--scene <scene>`, `--write-movie <artifact>`, or capture
scripts. Do not open Project Manager first; requiring a window does not require
Computer Use.

Before reusing smoke/drivers, inspect assumptions about vehicle/character
capabilities, routes/geometry, survivability, camera state, and end conditions.
Choose the smallest driver covering the risk; longer/broader smoke does not
automatically replace focused validation.

Use Computer Use only for evidence these paths cannot obtain, such as real
window focus, OS physical input, mouse capture, actual player-window
rendering/camera, audio experience, or editor interaction without programmatic
access. Identify missing evidence first and reinforce observations with state,
properties, logs, or saves afterward.

Add narrow test seams only when project edits are authorized and the seam has
reusable validation value. Do not modify production sources during
read-only/one-off investigation merely to avoid Computer Use; obtain maximal
existing-command evidence, then perform minimal windowed checks for remaining
risks.

## Scenes, Resources, and Generated Assets

After scene, Resource, export, or setting changes:

1. Perform editor/import checks.
2. Round-trip saves through matching APIs/editor when IDs, ownership,
   references, animations, or connections may change.
3. Inspect unintended rewrites, section reordering, UID churn, and unrelated
   imports.
4. Load actual entrypoints/affected scenes and inspect fresh logs.

For generated assets, also validate ownership ledgers/manifests and applicable
UID maps; round-trip supported `.tres`/`.tscn`; require second-run zero diffs
only for stable text, otherwise compare output sets, reference graphs, loading,
and runtime semantics; inspect import refresh/editor logs after publication.
Deletion/failure injection belongs only in temporary fixtures or isolated output
roots.

## Unified Invocation and Log Preflight

Information-only `--version` or `--help` runs call confirmed executables
directly and retain output/exit codes, without project roots/logs.
Build/import/run project commands use `scripts/invoke_godot.ps1` on PowerShell
7.2+. The runner builds argument arrays, injects checked `--path`/`--log-file`,
places `EngineArgs` before `--`, and emits the separator only when `UserArgs`
exists. Neither array may contain `--`; `UserArgs` cannot contain engine
options. Do not replace arrays with joined strings, `Invoke-Expression`, or
another shell parse.

```powershell
& '<skill-root>\scripts\invoke_godot.ps1' `
  -GodotExecutable '<project-matched-godot>' `
  -ProjectRoot '<project-root>' `
  -Purpose 'headless-smoke' `
  -TimeoutSeconds 120 `
  -EngineArgs @('--headless', '--scene', 'res://tests/headless_smoke.tscn') `
  -UserArgs @('--smoke-mode', 'focused')
```

Preserve the raw Godot exit code immediately before log reading/result
formatting. Nonzero Godot exits propagate unchanged and take precedence after
normal exit. Runner statuses: `64` invalid arguments, `65` preflight failure,
`66` missing/stale log, `67` unclassified errors in the current log or captured
stdout/stderr, `68` timeout with execution-unit cleanup requested, `69` launch
failure or output collection/inspection/termination-confirmation failure after
zero exit. Output failures preserve any raw code obtained (propagating nonzero),
run identity, arguments, and artifact paths. Timeout is runner interruption, not
an engine-reported failure; keep `godotExitCode=null` if no engine exit was
obtained rather than using supervisor termination codes. JSON retains raw exit,
paths, argument partitions, and failure kind.

Default logs are `<purpose>-<runId>.log`; explicit paths use mutually exclusive
file locks so runners cannot claim each other's logs. Lock sidecars remain, with
leases released by handle lifetime. Repeat preflight before launch; keep
directories unchanged during runs, since preflight is not isolation against
malicious replacement. Capture pre-run fingerprints/start time; require existing
logs whose contents/metadata changed and timestamps belong to this run. After
output collection completes, scan Godot error headers in the fresh main log and
both capture files created for this run. Never substitute another run's output;
a missing or unreadable capture is an output-collection failure, not an empty
result. Apply explicit allowlists to each channel; ordinary warnings do not
become errors. Allowlists need explicit user/repo/CI contracts; do not invent
patterns to make checks pass, including for shutdown resource errors.

`scripts/prepare_godot_log.ps1` is the single PowerShell path-preflight
implementation for standalone diagnostics/other runner integration. `-PathOnly`
returns `path-validated` with `writableAtCheckTime=false` and cannot authorize
launch. Runner preflight validates main logs and `-RunnerRunId`-derived
lock/stdout/stderr paths within allowed, ignored boundaries, then acquires path
locks before full write checks. Reject any existing target/ancestor symlink,
junction, or reparse point, even inside projects; use direct paths, keeping
required external authorization. Check existing logs through non-truncating
write opens for read-only, locks, or directory placeholders; probe missing logs
with CreateNew and clean up. Failure never edits `.gitignore`.

### Without PowerShell 7.2+

Prefer existing host adapters. Without an equivalent entrypoint, run manually
only if the host implements every contract:

1. Confirm root/executable from `project.godot` and commands; select
   independent, ignored, project-local logs by run identity.
2. Check normalized root boundaries and links in all existing ancestors/files;
   reject linked paths if resolution is unreliable. Retain user/repo/CI
   provenance for explicit external paths.
3. Check actual target writability without truncation and reject
   directories/read-only/locked files; recheck before launch and avoid
   concurrent log writers.
4. Build `--path`, `--log-file`, and `--` partitions with host argument arrays
   and finite total timeout/child termination.
5. Preserve raw exits first, then check fresh logs, unclassified errors, and
   project postconditions; separate stdout/stderr from structured results.

This branch does not require `.ps1`. Missing reliable path/lock/timeout support
blocks only this engine invocation; report missing capability and continue
authorized static work without repeatedly trying absent PowerShell.

Existing `--log-file` targets need full adapter checks, not only parent checks.
Resolve relative paths from project roots; project-local logs must be
Git-ignored.

### Timeouts and Output

`-TimeoutSeconds` defaults to 120, may follow known build/import budgets, and
must be finite, positive, and at most 2147483 seconds. Timing starts with
supervisor launch, including initialization. After engine return, output
collection waits at most 5.5 seconds and termination confirmation at most 5
seconds. Clean up this execution unit on timeout, interruption, or
original-parent exit; never kill other Editors by process name. Open pipes,
timeout, or unconfirmed termination cannot count as success.

The bundled runner supports Windows/Linux on PowerShell 7.2+; Linux requires
kernel 5.3+ and x64/ARM64. Other hosts require equivalent existing supervision,
never unconstrained launch. Read [Runner Contract](runner-contract.md) when
diagnosing/integrating supervision, interpreting detailed result fields, or
assessing process escape/namespace limitations.

`-Json` stdout contains exactly one result object. Child stdout/stderr go to
separate files beside this run's log. JSON `run` records paths, runId,
start/end, timeout, and termination state. Normal mode uses the same artifacts;
child output must not contaminate JSON.

Stop/report exact paths/errors on project-local preflight failure. Sandbox
`writable_roots` do not authorize `C:\tmp`, `/tmp`, or generic temporary log
roots; disposable artifacts do not bypass project-local paths.

External logs require explicit user/repository/CI configuration. The runner
takes `-RequestedLogFile`, `-AllowExternalLog`, and `-ExternalLogReason`; the
standalone preflight helper instead takes `-RequestedLogFile`, `-AllowExternal`,
and `-ExternalPathReason`. Do not invent paths/provenance. For an already
configured CI path:

```powershell
& '<skill-root>\scripts\invoke_godot.ps1' `
  -GodotExecutable '<project-matched-godot>' `
  -ProjectRoot '<project-root>' `
  -Purpose 'ci-import' `
  -RequestedLogFile $ConfiguredCiLog `
  -AllowExternalLog `
  -ExternalLogReason $ConfiguredCiLogSource `
  -EngineArgs @('--headless', '--import')
```

Variables above must come from actual authorized configuration. After external
preflight, the first Godot run still validates target-process compatibility.

Keep other project diagnostics local too: logs in `.godot/codex-logs/`,
screenshots/movies/profiles in `.godot/codex-artifacts/` or existing ignored
directories. Only minimal repro fixtures entirely isolated from the target
project may use explicit temporary roots; do not apply fixture rules to project
commands.

Classify `Failed to open 'user://logs/...log'`, external `--log-file`
initialization failures, and preflight blocks as log-path/environment failures
until project evidence proves another cause.

## Import and Result Consistency

Prefer `--headless --import`, which starts the editor, waits for import, and
exits. Do not append short `--quit-after` guesses. Confirm no GUI Editor for the
same project is running before launch; if unconfirmed, stop/report rather than
concurrently writing caches/serialization.

Automation, drivers, generators, and smoke succeed only when:

1. Godot exits zero.
2. Runner verifies a fresh main log and readable current stdout/stderr without
   unclassified Godot errors in any channel.
3. Declared project-tool success markers exist.
4. Output files, loading, references, object state, and other project
   postconditions pass.

A functional success marker does not override errors reported during shutdown.
Execution-unit cleanup confirms process termination, not that Godot objects or
Resources were released. Runner owns the first two/evidence outputs.
Markers/postconditions belong to callers/project tools; do not hardcode
project-specific strings into the general skill or replace side-effect
validation with runner success.

## LFS Assets and Failed Imports

If Git status and diff disagree for LFS assets, or a clean filter fails, inspect
command exit codes, stderr, and the affected paths' attributes before
interpreting an empty diff. For read-only content verification, compare the
actual file's SHA256 and byte count with the LFS pointer from the explicitly
selected comparison target (index, HEAD, or pinned review base); do not mix
targets. A match proves only that those asset bytes match that target, not that
the worktree is clean, the filter is healthy, or imports pass. Preserve
mismatching content and report inaccessible evidence as a blocker. Do not
repeatedly refresh the index or change Git configuration, permissions, or assets
merely to clear status markers.

When an asset fails to parse or import, especially in a new worktree, inspect
the source file before changing scene or gameplay code:

1. Check the affected path's Git attributes and actual bytes. A Git LFS pointer
   (including `version https://git-lfs.github.com/spec/v1`, object ID, and size)
   is not the binary asset expected by the importer.
2. Distinguish locally available LFS objects from missing downloads. `git lfs
   checkout` materializes available content; it does not download missing
   objects. Fetch only the needed assets through the repository's configured LFS
   workflow, then materialize them. Report authentication/network failures
   separately and preserve existing local edits. See the [Git LFS checkout
   contract](https://github.com/git-lfs/git-lfs/blob/main/docs/man/git-lfs-checkout.adoc).
3. Once source assets are real, run the supervised import path above. If failure
   persists, inspect the affected import metadata and fresh logs against the
   pre-run state or a known-good baseline. A failure marker such as
   `valid=false` is diagnostic evidence to investigate using the actual Godot
   version, not a reason to reset every import file.
4. Repair only changes attributable to the failed import. Preserve authored
   import options, UIDs, and unrelated work; prefer the importer or a narrowly
   justified restoration. Do not bulk-delete `.godot` or restore all `.import`
   files as the default fix. Godot keeps asset import configuration alongside
   the source; see [Import
   process](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/import_process.html).
5. Re-import and load the affected resource or actual scene, checking fresh logs
   and expected references. Successful code compilation does not establish that
   a GLB, texture, or audio asset is usable.

## Build and Runtime Identity

Use this branch when diagnosing or changing version reporting, reproducibility,
replay inputs, or stale binaries. Ordinary build validation does not require
adding an identity system or producing an export.

- Separate source revision and dirty state captured at build time, build
  identity, runtime session identity, and selected content/input identity. A
  supervisor run ID identifies the command invocation; it does not prove which
  source or content an artifact contains.
- Inspect the existing build pipeline and its declared manifest contract.
  Generating a manifest is insufficient: verify inclusion and readback from the
  actual assembly or artifact that will run. For .NET embedded resources, check
  build target ordering and the resulting assembly rather than assuming a
  generated file was embedded.
- Launch that artifact through the relevant entrypoint. Compare its reported
  identity with the manifest read from the artifact, the runtime UI when
  applicable, and the actual on-disk log for that session. Do not infer an old
  binary's provenance from the current checkout or working directory.
- Preserve explicit unknown/unavailable states when Git metadata or input
  identity cannot be established. An unnamed injected input must not silently
  acquire the default content's identity. Check that a restart uses the selected
  input snapshot and a new session identity when the project promises those
  behaviors.
- Select boundary cases affected by the change: clean versus modified source
  (including staged or untracked files if covered by the project's dirty-state
  contract), builds without Git metadata, and named versus unnamed inputs.
  Record mismatches separately from missing evidence; an in-memory value or UI
  screenshot alone does not prove artifact inclusion or log persistence.

Keep project-specific manifest schemas, resource names, success markers, and
release policy in the project. Report separately what was generated, embedded or
packaged, launched, displayed, and written to disk.

## Behavioral and Windowed Evidence

For relevant UI transitions, refresh interaction, coordinates, or clipping, read
[UI State and Input Validation](ui-validation.md); ordinary build checks do not
expand to UI audits.

- After automation, inspect transforms/state/behavior/functional logs to prove
  input receipt.
- After tool success, inspect properties, counts, references, saves, or fresh
  logs to prove effects.
- Identify editor viewport, embedded run, floating window, or standalone sources
  of visuals.
- Use actual runtime cameras for composition, occlusion, focus, fonts,
  animation, audio, and interaction.
- Only current-run fresh logs establish current state.
- Prefer `--write-movie`/capture scripts into `.godot/codex-artifacts/` for
  screenshots, movies, frame stats, and profiles. Without equivalent
  programmatic observation, Computer Use screenshots with window/time/action
  context can support corresponding visual acceptance, never invisible state,
  collision, or saving.

## Reporting

Separate hard errors, project warnings, tool-call errors, transient import
candidates, and optional platform noise. State implemented/diagnosed results;
root cause and evidence excluding alternatives; actual
commands/editor/log/runtime checks; missing programmatic evidence and escalation
reason when using Computer Use; unverified items/residual risks; and changed
persistent sources of truth rather than only generated output.
