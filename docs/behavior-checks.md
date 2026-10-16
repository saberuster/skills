# Behavior checks

Use a fresh agent and an isolated fixture to exercise selected skill behavior.
These checks complement static tests and client discovery. They do not prove
automatic selection, another client's behavior, or a real installation workflow.

The [smoke cases](../examples/behavior-smoke.json) cover selected workflows from
the broader examples:

| Case | Skill and behavior |
| --- | --- |
| `learn-proposal` | [learn-from-session](../examples/learn-from-session.md): propose a supported lesson without changing sources |
| `agents-*` (ten cases) | [maintain-agents-md](../examples/maintain-agents-md.md): discover coverage and effective sources, review commands, preserve policy, apply language preferences, and respect edit scope |
| `skills-local-edits` | [maintain-skills](../examples/maintain-skills.md): identify and preserve local edits before an update |
| `docs-schema` | [technical-docs](../examples/technical-docs.md): apply a scoped schema correction while preserving accepted content |
| `talk-acceptance` | [talk-it-through](../examples/talk-it-through.md): advance after local acceptance and stop when asked |
| `ready-*` (eight cases) | [agent-ready](../examples/agent-ready.md): trace real fixture tasks, calibrate recommendations, distinguish validation layers, and preserve review scope |

The `commit-draft`, `commit-breaking`, `commit-game-feedback`,
`commit-design-tokens`, `commit-split-independent`,
`commit-split-dependent`, and `commit-split-override` cases cover
[git-commit](../examples/git-commit.md) using exported change snapshots.
Deliver the two `commit-breaking` turns separately. These are read-only
message trials; they do not validate Git staging, hooks, signing, or real
commit execution. The game and design cases also exercise conditional
reference loading and proposed checks; do not execute game or design tools.
The split cases exercise grouping, dependency order, asset completeness,
and user overrides through read-only plans; they do not execute commits
or reversions. Inspect the transcript as well as unchanged files.

## Prepare

From the repository root, use the development environment described in the
[README](../README.md#development). Choose a new output directory outside this
repository and outside real client profiles. Replace the example path below
with a writable temporary path on Windows, and use `.venv\Scripts\python.exe`.

```text
.venv/bin/python scripts/behavior_trials.py prepare --output /tmp/skills-behavior-001
```

Add `--case learn-proposal` to select one case; repeat `--case` for several.
Preparation refuses to overwrite an existing run. Each case directory contains:

- `workspace/`: the synthetic project and complete copied skill package.
- `input.json`: context, skill location, and ordered user requests.
- `evaluator.json`: evaluator-only observations and filesystem invariants.
- `manifest.json`: preparation time, source revision and hashes, case and
  fixture hash, and initial workspace hashes.
- `before/`: the original workspace for inspecting changes.

## Select AGENTS.md maintenance cases

The ten `agents-*` cases are individually selectable; selection uses exact IDs,
not wildcard expansion. Their full definitions live in the smoke JSON, with
[narrative acceptance cases](../examples/maintain-agents-md.md).

| Case | Focus and observed file boundary |
| --- | --- |
| `agents-review` | Equivalent duplicate, documentation exception, nested scope; unchanged workspace |
| `agents-coverage` | Sparse instructions and eight coverage responsibilities grounded in canonical sources; unchanged workspace |
| `agents-discovery` | Nested discovery, supplied synthetic host precedence, and unknown-host boundary; unchanged workspace |
| `agents-command-review` | Stale command, prerequisites, success signal, and deployment effects; static inspection only |
| `agents-capture-revise` | Confirmed capture, deduplication, established expiry, and preserved signing duty; one required file change |
| `agents-language-default` | Chinese body inference, default English headings, contents and authorized dependent anchors; two required file changes |
| `agents-language-scoped` | Chinese body and section-limited addition; required edit with bytes outside the section preserved |
| `agents-language-override` | Explicit Chinese headings with English body and revised anchor; one required file change |
| `agents-language-question` | Ambiguous body language prompts a focused question; unchanged workspace |
| `agents-untrusted-source` | Embedded unauthorized instructions and fake sensitive content; unchanged workspace |

For example, select the three language-edit cases together:

```text
.venv/bin/python scripts/behavior_trials.py prepare --output /tmp/agents-language-001 --case agents-language-default --case agents-language-scoped --case agents-language-override
```

To exercise the complete maintenance set, repeat `--case` for all ten IDs in the
table; omitting selection also prepares unrelated skills. Chinese fixture text
uses Unicode escapes in the ASCII JSON and becomes UTF-8 project text during
preparation. Inspect prepared files when judging actual heading/body languages
and links; escaped source text is not the agent's document output.

## Run the agent

Give a fresh agent the workspace path, copied `skill/SKILL.md`, context, and
first
request from `input.json`. Allow only the fixture operations requested by that
case. Keep `evaluator.json`, `manifest.json`, and `before/` out of its context.
For `talk-acceptance`, deliver each subsequent request only after receiving the
previous actual reply, keeping the same session. Do not add hints to continue.

For `agents-*`, honor each case's edit and execution boundary. All
command-review
cases are static: do not run the supplied validation, deployment, or approval
scripts. The discovery fixture supplies a fictional host contract solely to
test evidence-based precedence; passing does not establish loading behavior of
Codex, Claude Code, or any other real host. The ambiguous body-language case
ends after the initial question; it does not supply a language answer. Review
cases require no file changes, while edit cases require actual authorized
changes as well as semantic preservation. Inspect observed actions for command
execution: an unchanged workspace alone cannot prove that no command ran.

The eight `ready-*` cases are executable synthetic project reviews. Their
Python standard-library commands use `-B` to preserve the read-only workspace;
inspect command effects before running them. Do not start listeners, install
dependencies, or execute data-writing paths. Supply only worker inputs, never
the expected diagnoses from the case descriptions or evaluator criteria. A
passing simulated review does not establish readiness of a real project or
prove browser, rendering, or human-experience behavior.

The maintenance case replaces `npx skills` with `python mock_skills.py`. Its
inventory, source records, upstream files, and command log are synthetic. Never
substitute a real CLI, user installation, or remote source for this fixture.

Record each exact request and actual reply in a transcript JSON file:

```json
{
  "turns": [
    {
      "request": "Exact request from input.json",
      "response": "Actual agent reply",
      "actions": ["Observed command or artifact; label agent-reported actions"]
    }
  ]
}
```

Keep tool output or other supporting evidence when needed to assess a criterion.
Do not replace missing observations with an agent's success claim. The prepared
directory is an isolation boundary for the trial instructions, not an OS
sandbox;
filesystem checks observe only that workspace, not the rest of the host.

## Live Git trials

Use this maintainer procedure when validating actual `git-commit` execution,
such as the [split execution case](../examples/git-commit.md#live-split-execution-and-intermediate-versions).
It is not a requirement for ordinary commits. The snapshot helper above does
not create or verify live Git fixtures; retain these trial artifacts separately.

1. Create a disposable repository outside the source repository and client
   profiles, with no remote. Copy the skill package and record its revision and
   file hashes. Prepare a runnable baseline, synthetic intended changes, and
   unrelated staged, unstaged, and untracked work. Record fixture-local
   identity, signing, hooks, and configuration; do not alter user configuration
   to prepare the trial. If signing is not exercised, state that coverage limit.
2. Before running the agent, save the baseline commit and expected logical
   changes in evaluator-only evidence. Record index entries (path, mode, stage,
   and blob content), working-file hashes, and tracking/staging status. Useful
   inspection commands include `git ls-files --stage -z`,
   `git status --porcelain=v1 -z`, and `git cat-file blob <object-id>`.
   Include untracked files in the baseline; status labels alone cannot prove
   unchanged contents. Keep expected outcomes and baseline evidence outside
   the agent's inputs.
3. Give a fresh agent the copied skill, fixture path, and a request naming the
   changes it may commit. Allow staging, relevant checks, and local commits
   within that fixture. Retain observed actions and check output. When a hook
   checks the staged candidate, record its tree and result, then compare that
   tree with the resulting commit so evidence cannot silently apply to a
   different version.
4. Independently inspect the commits created since the recorded baseline.
   For each commit, compare `git ls-tree -r -z <commit>` and its blob contents
   with the expected cumulative logical changes: paths, modes, object types,
   and content must match. Check intent completeness and prerequisite order;
   accept valid alternative ordering of independent intents. Do not infer
   grouping from messages or a fixed commit count alone.
5. Create a fresh isolated checkout or export matching each recorded commit
   tree, and run that version's relevant checks there. Verify that the copy
   includes the required files and dependencies before running checks. Retain
   the commit/tree IDs, commands, exit codes, and output for each version.
   Do not let later working-tree changes supply missing files or mask an
   unusable intermediate version. Report unavailable checks as unverified.
6. Compare the remaining index entries and working files with the expected
   final state. For untouched paths, compare with the baseline. For paths
   shared with intended changes, construct the expected index from the final
   committed version plus the preserved unrelated staged changes, then the
   expected working file by adding the preserved unstaged changes. Compare
   these versions and their differences; do not require the whole index blob
   to equal its baseline. Verify untracked files retain their contents and
   tracking state. Check relevant modes and paths as well as hashes. This
   comparison concerns content and staging state, not byte-identical
   `.git/index` metadata. Confirm configuration and hooks remain as prepared.

Retain a local result with per-commit checks, preservation comparisons, observed
failures, and coverage limits. Use a separate evaluator to inspect the evidence;
keep raw transcripts and machine paths out of the public repository. A passing
synthetic trial does not establish real engine behavior, visual quality, human
acceptance, or unexercised signing and rejecting-hook paths.

## Assess and record

A separate evaluator reads the transcript, actual file changes, available tool
evidence, and `evaluator.json`. Assess each criterion as `passed`, `failed`, or
`unverified`, with a reason and concrete evidence. The following is
illustrative:

```json
{
  "evaluator": "Evaluator identity",
  "criteria": {
    "supported-lesson": {
      "status": "passed",
      "reason": "The proposal follows the supplied verified correction.",
      "evidence": ["Turn 1: exact header and row order are both addressed."]
    }
  }
}
```

Use the actual criterion IDs for the selected case. Missing assessments or
evidence remain unverified. Save this JSON separately, then record the run:

```text
.venv/bin/python scripts/behavior_trials.py record --trial /tmp/skills-behavior-001/learn-proposal --transcript /tmp/transcript.json --assessment /tmp/assessment.json --runner "Codex desktop subagent" --model "actual model/version, or unavailable"
```

Record the actual runner and model/version when exposed; state unavailable when
the host does not expose it. The recorder retains transcript and assessment,
copies `after/`, and writes `result.json` with observed file changes, source and
case drift, and the supplied semantic assessments. A failed invariant or
criterion fails the run. Incomplete turns, unassessed criteria, or source/case
drift prevent a passing result. Recording does not independently establish that
an evaluator's semantic judgment is correct.

The command exits 0 for passed, 1 for failed or unverified, and 2 for an input
or
execution error. It refuses to overwrite an existing result. For a retry or a
before-and-after comparison, prepare fresh directories and preserve earlier
results. Keep equivalent requests, fixtures, and runner settings when comparing
skill versions. Retain the evidence directory locally; do not commit raw session
logs or machine paths to the public repository.

The ordinary unittest suite tests this harness with synthetic responses; it does
not run agents. Run selected agent trials separately when behavior changes, and
report executed cases and remaining coverage without treating one sample as a
reliability estimate.
