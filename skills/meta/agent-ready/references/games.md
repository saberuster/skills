# Games and engine-driven projects

Load this guidance only for a game or engine-driven task. Apply the general
rubric first; do not treat a particular engine or ECS architecture as required.

## Match evidence to the result

- **Rules:** Test deterministic state transitions, scoring, inventories, or
  turn resolution without the engine when that isolates the actual rules.
- **Engine interaction:** Exercise scene lifecycle, input routing, signals,
  physics, resource loading, timing, and persistence through their real engine
  boundaries. Direct rule calls can bypass the bug the player encounters.
- **Visual result:** Inspect the rendered state under the relevant viewport,
  camera, assets, and platform. A headless run or successful exit does not prove
  rendering, layout, animation, or visual correctness.
- **Human experience:** Leave feel, readability in motion, pacing, and usability
  to a stated playtest or human evaluation. Do not substitute automated rule
  assertions or screenshots for those judgments.

For a reproducible scenario, record more than a random seed: include initial
world and save state, engine/build and asset versions, clock/timestep and event
ordering, action/input sequence, and platform-specific dependencies. Identify
uncontrolled physics, scheduling, or external inputs as limits. Recommend a
small scenario loader or replay only when a traced task benefits from it.

## Godot-specific checks

Inspect the project's engine version, entry scene, autoloads, resource paths,
and signal/input connections on the selected task. Distinguish pure logic
checks from running actual scenes. Godot headless execution does not establish
that rendered output is correct; report unavailable rendering explicitly.

Do not assume worktree isolation also isolates `user://`. Check how the project
name and custom user directory resolve on this host, along with ports, saves,
editor/import caches, and external services. Multiple worktrees can share these
resources. Inspect configuration before concurrent execution and prefer explicit
per-run state/port configuration or serial execution when that is sufficient.
Do not delete saves or change global engine settings to obtain a clean run.
