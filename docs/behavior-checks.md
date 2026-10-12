# Behavior checks

Use a fresh agent and an isolated fixture to exercise selected skill behavior.
These checks complement static tests and client discovery. They do not prove
automatic selection, another client's behavior, or a real installation workflow.

The [smoke cases](../examples/behavior-smoke.json) cover selected workflows from
the broader examples:

| Case | Skill and behavior |
| --- | --- |
| `learn-proposal` | [learn-from-session](../examples/learn-from-session.md): propose a supported lesson without changing sources |
| `agents-review` | [maintain-agents-md](../examples/maintain-agents-md.md): review duplicates while preserving exceptions and scope |
| `skills-local-edits` | [maintain-skills](../examples/maintain-skills.md): identify and preserve local edits before an update |
| `docs-schema` | [technical-docs](../examples/technical-docs.md): apply a scoped schema correction while preserving accepted content |
| `talk-acceptance` | [talk-it-through](../examples/talk-it-through.md): advance after local acceptance and stop when asked |

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

## Run the agent

Give a fresh agent the workspace path, copied `skill/SKILL.md`, context, and first
request from `input.json`. Allow only the fixture operations requested by that
case. Keep `evaluator.json`, `manifest.json`, and `before/` out of its context.
For `talk-acceptance`, deliver each subsequent request only after receiving the
previous actual reply, keeping the same session. Do not add hints to continue.

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
directory is an isolation boundary for the trial instructions, not an OS sandbox;
filesystem checks observe only that workspace, not the rest of the host.

## Assess and record

A separate evaluator reads the transcript, actual file changes, available tool
evidence, and `evaluator.json`. Assess each criterion as `passed`, `failed`, or
`unverified`, with a reason and concrete evidence. The following is illustrative:

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

The command exits 0 for passed, 1 for failed or unverified, and 2 for an input or
execution error. It refuses to overwrite an existing result. For a retry or a
before-and-after comparison, prepare fresh directories and preserve earlier
results. Keep equivalent requests, fixtures, and runner settings when comparing
skill versions. Retain the evidence directory locally; do not commit raw session
logs or machine paths to the public repository.

The ordinary unittest suite tests this harness with synthetic responses; it does
not run agents. Run selected agent trials separately when behavior changes, and
report executed cases and remaining coverage without treating one sample as a
reliability estimate.
