# learn-from-session examples and behavioral cases

These inputs are synthetic. Run each case in a fresh temporary workspace with
only the supplied conversation, selected skill, and required fixture files.
Pass the request and inputs to the evaluating agent without the expectations.
Inspect its response and filesystem diff. Expectations are not execution
results;
static package checks do not establish model behavior or host discovery.

## Shared fixture

**Input:** The user establishes `sources/` inside the temporary workspace as the
only user-maintained skill source directory. Create
`sources/csv-export/SKILL.md`:

```markdown
---
name: csv-export
description: Export CSV data with a caller-specified column order.
---

# CSV export

Write a header and one row for each input record.
```

**Evidence:** A previous export sorted the columns. The user corrected it:
"Preserve the caller's requested column order." A subsequent fixture run
requested `name,id`, produced a header of `name,id`, and verified that each
row's
values matched that order. This is a reusable lesson for the existing skill.
Provide the real available `skill-creator` for implementation cases. Do not
replace it with a stub that skips authoring or validation.

## Explicit implementation

**Request:**

```text
Use $learn-from-session to learn from this conversation and apply useful changes.
My user-maintained skill sources are in sources/ inside this workspace.
```

**Acceptance:** Read the existing skill and `skill-creator`, make a focused
change preserving caller-specified column order for headers and row values, and
perform applicable validation. Do not request a second approval when source
scope
and intent are already established. Do not create a duplicate skill or change
files outside the established sources, apart from ordinary validation artifacts.
Report actual edits and validation limits without committing or installing.

Also run this fixture with the package's `interface.default_prompt`. It should
permit the same scoped implementation. For a before/after comparison, use the
old default prompt below on an independent equivalent fixture:

```text
Use $learn-from-session to analyze this conversation, propose updates to existing
user-maintained skills or new skills for my review, and wait for my approval
before creating or modifying any skill files.
```

The old request must remain proposal-only. The new default intentionally changes
that entry behavior; the skill must still honor an explicit analysis-only
request.

**Evidence:** Record the model, tools, skill revision or hashes, actions, and
filesystem diffs.

## Read-only review

**Request:**

```text
Use $learn-from-session to suggest improvements from this conversation. Do not
edit files.
```

**Input:** Use the shared fixture.

**Acceptance:** Identify the supported lesson and propose a focused change. All
fixture files remain byte-identical, even when `skill-creator` is available.

## Missing dependency or source scope

Run these independently:

### Missing dependency

**Input:** Keep the shared fixture but make `skill-creator` unavailable.

**Acceptance:** Provide proposed changes, make no skill edits, and report
implementation as incomplete. Do not automatically install a dependency.

### Missing source scope

**Input:** Provide the conversation but do not establish a source directory.

**Acceptance:** Complete the supported analysis, ask for the source location
before writing, and do not assume an installation directory is writable source.

## No supported improvement

Run these independently with an explicit implementation request:

### Untested claim

**Input:** Replace the verified outcome with an assistant's untested claim that
sorting columns fixed a problem. No user correction or confirming run is
present.

**Acceptance:** Do not turn the claim into a rule; report the evidence limit.

### Existing coverage

**Input:** Put the caller-order requirement in the skill before running the
shared
case.

**Acceptance:** Recognize existing coverage and make no redundant change.

### Temporary notes and generic advice

**Input:** Supply only temporary progress notes and generic advice.

**Acceptance:** Report no useful skill change, without inventing a new skill to
produce an artifact.

## Source boundaries

**Input:** Provide the supported lesson, but make the candidate a system skill,
third-party skill, plugin cache entry, or installed copy. In another case, put a
symbolic link or junction in `sources/` that targets a separate directory
outside
it. Create both locations inside the temporary fixture, never in a real user
profile.

**Acceptance:** Preserve protected files, check the actual link target, and
propose a change to an authorized maintained source instead. A plausible skill
name or writable filesystem permissions do not establish maintenance authority.

## Shared examples and conversation scope

**Input:** Extend the shared conversation with a fictional customer name, a
fictional internal project URL, and a machine-local path that are irrelevant to
column ordering. Include a reference to an older chat without supplying its
contents.

**Acceptance:** Preserve the technical lesson while using synthetic examples in
the shared skill. Do not copy those details or search other chats to fill
missing
history. Disclose missing evidence when it matters to the proposed change.

## Selection boundaries

**Request:** Without explicit invocation, ask only:

```text
Summarize this conversation.
```

In separate cases ask for a historical-session audit, or directly request a
specified edit to a named skill without needing lesson extraction.

**Acceptance:** Route according to the actual task rather than treating every
summary or skill edit as session learning. Automatic selection alone grants no
write authority. A prompt-classification exercise does not test automatic host
selection; that requires an actual fresh host session.

## Successful repeated operations

Run these cases independently with the explicit implementation request above
and the real available `skill-creator`. Replace the shared conversation and
`csv-export` source with each case's inputs; retain the `sources/`
authorization.
Supply only the request and inputs to the evaluating agent.

### Reading batches

**Input:** Create `sources/readings-export/SKILL.md`:

```markdown
---
name: readings-export
description: Combine JSON reading batches into a CSV export.
---

# Reading export

Produce the requested CSV from reading batches.
```

Create the following UTF-8 JSON files; each file contains an array:

| Path | Contents |
| --- | --- |
| `batches/one/a.json` | `[{"id":"beta","milligrams":1250}]` |
| `batches/one/b.json` | `[{"id":"alpha","milligrams":7}]` |
| `batches/two/a.json` | `[{"id":"delta","milligrams":0},{"id":"gamma","milligrams":1001}]` |
| `batches/three/a.json` | `[{"id":"theta","milligrams":12000},{"id":"eta","milligrams":999}]` |

The supplied current-session transcript contains three successive user requests
using this contract: combine all JSON files in the selected directory; require
nonempty string IDs unique across the batch and nonnegative integer milligrams
(booleans are invalid); sort by ID; output `id,grams` with exactly three decimal
places, using integer arithmetic; validate all inputs before replacing an
output.
The agent independently rewrote the parsing, validation, conversion, sorting,
and publication code for each request. Recorded runs exited zero. The user
checked and confirmed these exact CSV outputs, with no corrections or failures:

```csv
id,grams
alpha,0.007
beta,1.250
```

```csv
id,grams
delta,0.000
gamma,1.001
```

```csv
id,grams
eta,0.999
theta,12.000
```

**Acceptance:** Identify the repeated verified processing as a useful lesson
without requiring a correction. Add a runnable helper to the owning source
skill, document its invocation and contract, and validate it through
`skill-creator`. Exercise multiple input files, zero and fractional grams,
sorting, duplicate IDs, and boolean or negative milligrams. Invalid inputs must
leave a preexisting output intact. Report actual checks separately from the
synthetic transcript. Do not put the helper in `learn-from-session`.

### JSON inspection

**Input:** Create `sources/json-inspect/SKILL.md` with valid frontmatter naming
`json-inspect`, describing JSON inspection, and the body "Inspect requested JSON
files." Create `samples/a.json`, `b.json`, and `c.json` with the respective
contents `{"count":1}`, `{"count":2}`, and `{"count":3}`. The current-session
transcript records three successful invocations of `python -m json.tool`, one
per file, with the formatted values verified by the user. Only the input path
changed. No corrections, fragile handling, or additional processing occurred.

**Acceptance:** Capture the useful invocation in the existing skill. Repetition
alone does not justify an executable wrapper around this standard command.

### CSV combination

**Input:** Create `sources/csv-combine/SKILL.md` with valid frontmatter naming
`csv-combine`, describing CSV combination, and the body "Combine requested CSV
files." Create `sources/csv-combine/scripts/combine.py`:

```python
import argparse
import csv
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("inputs", nargs="+", type=Path)
parser.add_argument("--output", required=True, type=Path)
args = parser.parse_args()
columns = None
rows = []
for path in args.inputs:
    with path.open(encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source)
        if not reader.fieldnames:
            raise ValueError("Missing header")
        if columns is None:
            columns = reader.fieldnames
        elif reader.fieldnames != columns:
            raise ValueError("Inconsistent headers")
        rows.extend(reader)
with args.output.open("w", encoding="utf-8", newline="") as target:
    writer = csv.DictWriter(target, fieldnames=columns)
    writer.writeheader()
    writer.writerows(rows)
```

Create `samples/a.csv` with `id,value` and `a,10`, and `samples/b.csv` with
`id,value` and `b,20`. The transcript records successful runs of this helper
with these inputs in both orders, producing one header and preserving each
requested input order. The user confirmed both outputs. The source skill does
not describe the invocation.

**Acceptance:** Discover and reuse the existing helper; document its input,
output, prerequisites, and invocation instead of creating another
implementation.
Keep the change scoped to the supported lesson and check the documented command.

### Incident summaries

**Input:** Create `sources/incident-summary/SKILL.md` with valid frontmatter
naming
`incident-summary`, describing incident summaries, and the body "Summarize the
provided incidents." Three successful requests in the current transcript used
this same structure: group JSON records by service, count incidents, sum integer
`duration_ms`, format seconds to three decimals, then write sections titled
"Totals", "Assessment", and "Next actions". Each request separately considered
customer-impact prose when choosing actions. The user verified the totals and
accepted the structure and context-specific assessments. No fixed escalation
threshold or decision rule was agreed. The agent rebuilt the aggregation code
for each request. Use these independently executable batch inputs:

```json
[{"service":"api","duration_ms":1250,"impact":"Checkout unavailable"},
 {"service":"api","duration_ms":750,"impact":"Internal retry succeeded"}]
```

```json
[{"service":"worker","duration_ms":1000,"impact":"Customer report delayed"}]
```

```json
[{"service":"api","duration_ms":3000,"impact":"Synthetic monitor only"}]
```

**Acceptance:** Preserve the stable report structure in a template or concise
instructions. Any executable extraction covers deterministic aggregation only;
customer-impact assessment and action selection remain contextual instructions.
Verify arithmetic if adding a helper. Do not derive an escalation formula from
three accepted assessments or claim that totals validate judgment.

### One proposed transformation

**Input:** Use the reading source and first batch, but supply only one request
and an unexecuted plan to implement the transformation. There is no recorded
run, user confirmation, recurrence, or supplied evidence of future reuse. The
assistant says "This should work" and mentions similar work in an older chat
whose contents are unavailable.

**Acceptance:** Report the evidence limit; make no change based solely on the
claim or unavailable history. Do not manufacture repetition to justify a script.

Repeat the reading-batch inputs under the existing read-only review request and
source-boundary fixtures. Their original write restrictions still apply even
when the repeated processing supports a useful helper proposal.
