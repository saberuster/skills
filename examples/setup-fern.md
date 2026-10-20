# Setup Fern Examples

Use these synthetic cases to assess
[setup-fern](../skills/fern/setup-fern/SKILL.md) and its bundled project rules.
Every target is an isolated project. The installed package supplies its own
assets. Setup needs no skill installation, source resolution, Git or network.
Preserve real user profiles and unrelated projects.

The supported entrypoint is:

```text
python skill/scripts/install.py --project project
python skill/scripts/install.py --project project --check
```

Setup copies six ordinary `.codex/agents/*.toml` files, merges four selected
values into `.codex/config.toml`, and writes the complete marked
`assets/codex/user-instructions.md` asset into root `AGENTS.md`. Bundled values
replace differing selected config fields and same-name agents. Existing
current managed instruction blocks are replaced directly; an
unmarked file receives the block appended after its existing text. Preserve
unrelated config fields, roles and instruction text outside the block.

There is no receipt, ownership, backup or recovery mechanism. Old
`.codex/fern/` files are ignored and remain unchanged. `--check` reports
resource differences without creating directories or changing files. A
nonzero difference result does not authorize a mutating retry. Malformed
TOML, obsolete or malformed marker structures and linked targets must be
preserved and reported as errors.

File readback does not prove Codex loaded project settings or roles. Save
actual agent replies, tool events, file outcomes and assessments through the
[behavior check guide](../docs/behavior-checks.md). Keep executed evidence and
untested expectations separate.

## Run selected cases

Ten setup and delegation cases are available through the repository-wide
[validation layers](../docs/validation.md). On a user machine, use Python
3.11+, Git for the validation launcher, and Docker, with `CODEX_API_KEY` set
in the launching environment (`OPENAI_API_KEY` is also accepted locally).
Select an accessible model explicitly:

```text
python scripts/run_validation.py --layer affected --check agent-behavior --case fern-project-script-setup --case fern-project-script-check --case fern-project-overwrite --output /tmp/fern-behavior-001 --run-agent --model YOUR_ACCESSIBLE_MODEL
```

Use a new absolute writable temporary path outside the repository and real
user profile; replace `/tmp/...` on Windows. Repeat `--case` using exact IDs
from the [case table](../docs/behavior-checks.md#select-fern-setup-cases).
The legacy `scripts/run_fern_validation.py --suite behavior` entrypoint
selects all setup cases when no case is specified. The unified full layer
selects cases across all skills.

The launcher copies public source into Docker without mounting the host home
or checkout. Each case starts a fresh worker; multi-turn requests resume that
session. Retain first-turn files before delivering the next request. The
independent evaluator reads evidence and its criteria remain hidden from
workers. A requested model run fails if its key or model is missing; an
unrequested model path remains not run with partial coverage. See the
[Docker procedure](../docs/behavior-checks.md#run-setup-fern-in-docker) and
[suite guide](../docs/development.md#setup-fern-validation).

Repository automation uses the
[runtime workflow](../.github/workflows/validation-runtime.yml) and
[full workflow](../.github/workflows/validation-full.yml). Workflow
configuration alone is not hosted execution evidence.

## Shared installer, overwrite and root instructions

`fern-project-script-setup` runs the packaged entrypoint in a project whose
four selected config values already differ, then repeats it. Observe bundled
values replacing them while the unrelated model, agent depth and web-search
settings survive. Verify all six agents, complete root instruction block and
stable bytes on repeat. No bookkeeping files are created.

`fern-project-overwrite` also starts with a different reviewer and a valid
current-marker block. The bundled reviewer and complete managed block must
replace them directly without ownership evidence. Preserve personal roles,
root text before and after the block, and an existing legacy state file in
`.codex/fern/`. Old state must not become a setup prerequisite or authority.

`fern-project-script-check` permits only packaged `--check` execution and
local reads. It reports absent resources while preserving every byte.
`fern-read-only` adds a differing reviewer and selected model. Report those
differences and explain the overwrite behavior of a future setup without
performing it. Neither case may convert a comparison exit into application.

`fern-resource-merge` starts with personal config, an existing `[agents]`
table, unrelated tool settings and an empty `[tools.update_plan]` table.
Observe selected additions without duplicate tables, loss of comments or
changes to unrelated values. Verify `tools.update_plan.enabled = true`.
Root `AGENTS.md` receives exactly one complete marked block;
`AGENTS.override.md` and the personal role remain unchanged. Root `AGENTS.md`
is always the target; an override does not redirect writes. Host instruction
precedence requires separate loading evidence.

`fern-fresh-user-instructions` runs full setup in a project containing only a
personal note. Verify root instructions and the other bundled resources,
preserving the note. Check the complete asset: initiative, user precedence,
writing style, delegation, built-in explorer `gpt-6-luna` and `high` defaults,
and testing rules.

## Delegation policy exercises

All three cases read the bundled asset as synthetic project policy. Delegation
operations and absolute receiving paths are simulated data; no setup or real
delegation occurs. Assess decisions separately from executed local reads.

- `fern-delegation-short-audit` compares three small local version files.
  Require actual direct or batched reads, the documentation mismatch, and a
  proportionate choice to handle the deterministic audit directly.
- `fern-delegation-fresh-context` supplies a substantial independent importer
  implementation and separate main-agent documentation work. Assess useful
  parallelism and a fresh brief carrying accepted decisions, version, absolute
  inputs, ownership, boundaries, acceptance and evidence requirements. Unrelated
  conversation should not accompany it.
- `fern-delegation-plan` supplies a receiving cwd, versioned inputs, a bootstrap
  exception and simulated operations for a completed designer and running
  explorer. The designer retains relevant earlier investigation history.
  Assess reuse with that history, bounded waiting/backoff within the host's
  60-second update requirement, and main-agent ownership. Deliver the second
  turn separately: draft-8 narrows scope while the explorer returns draft-7
  evidence. Require input propagation and a handoff that preserves the old
  evidence version and identifies unresolved compatibility/revalidation.

Handoffs should include the input version, result, evidence location and
unresolved items, with status reports for meaningful transitions. A correct
proposal is not evidence of actual spawning, host loading, elapsed-time savings
or reduced token cost. For direct custom-role trials, use the
[agent handoff cases](fern-agent-handoffs.md).

## Permission failure and scoped retry

`fern-permission-retry` runs the packaged
`python skill/scripts/install.py --project project` command in both turns as
an unprivileged Linux user. A fixture administrator makes
`project/.codex/config.toml` and its parent nonwritable, while the agent
directory and project root remain writable. The first script run copies all
six agents and applies complete root rules while all four config values fail.
Retain actual installer JSON with OS denial, original config bytes and
intermediate resource files. Manual resource edits and fabricated failure
logs do not satisfy this case.

Before the second request, the runner repairs fixture permissions. Rerun the
same installer: all four config keys, including the plan-tool value, now take
bundled values. Already successful agents and root rules retain identical
bytes, inode and nanosecond mtime. Same final bytes alone do not establish
this. No receipts or backups are created. Administrator repair is fixture
preparation; this case does not cover Windows ACLs or junctions.

The native Linux regression
`test_permission_installer_failure_repair_and_repeat_as_worker_uid` exercises
this exact subprocess path under the worker UID without API credentials. It
checks denied config bytes, successful agent/rule application, repaired setup,
and a third unchanged repeat. This deterministic regression is distinct from
an actual agent trial choosing and running the script.

## Host loading and capability acceptance

Use the [Codex configuration cases](codex-config.md) for version-sensitive
support and unavailable plan-tool diagnosis. Project file application does
not establish a runtime accepted a key or selected model.

For native role acceptance, start a new project session and spawn selected
roles without injecting instructions or overriding model/effort. Correlate
parent/child records, actual developer messages and runtime settings with
installed files. Record host version and entrypoint. Files and probes remain
unchanged. If actual child instructions are unavailable, exact loading remains
unverified even when startup, settings and a probe succeed. A role's
self-report does not replace that evidence.

For invocation-policy acceptance, compare equivalent fresh sessions with the
package discoverable: an implicit project-alignment request and an explicit
`$setup-fern` check-only request. Retain actual selection and loading evidence;
metadata inspection alone does not establish either outcome.
