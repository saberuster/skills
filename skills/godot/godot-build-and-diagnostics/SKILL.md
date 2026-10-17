---
name: godot-build-and-diagnostics
description: Build, import, run, validate, or diagnose Godot 4 projects using supervised commands, current logs, and risk-matched editor, serialization, runtime, and input evidence.
---

# Godot Build and Diagnostics

Reproduce, classify, and validate Godot 4 build, import, serialization, editor,
headless, runtime, and environment issues. Obtain current command/fresh-log
evidence before changing the smallest supported boundary.

## Workflow

1. Read `AGENTS.md`, `project.godot`, validation scripts, language
   configuration, import settings, and existing tests.
2. Confirm actual minor version, editor/command path, working directory, .NET
   version if applicable, and log location.
3. Inventory existing test drivers/scenes, Godot APIs/tool scripts, and
   entrypoints; choose the cheapest programmatic path covering the risk.
4. Reproduce through that path and record full command/editor path, exit status,
   and fresh relevant logs.
5. Classify project code, Godot/toolchain, import/serialization,
   environment/permissions, log paths, or player-visible behavior.
6. Change only the smallest supported boundary and revalidate through the same
   path.

Use `$godot-scripting` for script changes and
`$godot-scene-and-resource-authoring` for scene, Resource, imported-asset, or
setting changes. Do not fix paths, plugins, permissions, or log directories
through scene/architecture refactors.

## Read References as Needed

- Before any build, import, editor, headless, runtime, or export command, read
  `references/validation.md`.
- For asset parse failures in a new checkout, follow its LFS and failed-import
  branch; for build/version reporting or reproducibility issues, follow its
  build and runtime identity branch.
- For combined UI states, refresh timing, focus, scrolling/clipping, or scaled
  input, also read [UI State and Input Validation](references/ui-validation.md).
- With PowerShell 7.2+, project commands use `scripts/invoke_godot.ps1` for
  argument partitioning, log preflight, exit propagation, and current-log
  checks. Without it, follow the host-independent contract in
  `references/validation.md`, using an existing equivalent runner or reporting
  the execution block.
- For standalone log-path/preflight diagnosis, use
  `scripts/prepare_godot_log.ps1`; do not invent temporary directories.
- Read `references/runner-contract.md` only when integrating/debugging the
  runner, inspecting its structured result, or assessing host
  supervision/cleanup limitations.

## Stable Rules

- Check exit status, the fresh main log, and the current run's captured
  stdout/stderr; zero exit does not prove no project errors. Process cleanup and
  functional success markers do not establish an error-free engine run.
- Prefer existing test drivers/scenes or version-matched Godot APIs run directly
  from CLI; use Computer Use only for necessary evidence unavailable
  programmatically.
- Match validation levels to observable risk; compilation cannot replace
  scene-load, UI, input, camera, or imported-asset evidence.
- Engine arguments precede `--`; project arguments follow. Do not concatenate
  command strings.
- Run confirmed executables directly for information-only `--version`/`--help`,
  retaining output/exit status without requiring project logs. Project runs use
  independent `<purpose>-<runId>.log` through runner/preflight;
  timeout/output/argument contracts are in validation, supervision details in
  runner-contract.
- Prefer `--headless --import` and wait for completion, without short
  `--quit-after` guesses or concurrent GUI Editor import of the same project.
- Preflight conservatively rejects symlink/junction/reparse points in
  logs/ancestors and checks existing logs for read-only/locks/actual write
  opening. Stop and report failed project-local preflight; do not fall back to
  system temporary roots or interpret sandbox `writable_roots` as log advice.
- External paths require explicit user/repo/CI configuration and recorded
  provenance; filesystem writability does not prove subprocess writability.
- Classify unwritable default logs separately from project-code failures.
- Report only executed commands, editor paths, logs, and visible evidence;
  identify unverified items/residual risks.
