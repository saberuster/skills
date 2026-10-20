# Fern behavior cases

These are synthetic expectations, not execution records. Use a fresh agent,
the complete `fern` package, and an isolated project. Deliver multi-turn cases
one request at a time. Keep evaluator criteria outside worker inputs and retain
actual replies, actions, and file changes. Explicit loading does not establish
automatic selection, client discovery, or installation.

## 1. Review without repairing

Request: "Use $fern to review this retry helper. Explain the defect and propose
a correction; do not modify it."

Supply a helper that returns a negative retry count for negative input and a
contract requiring nonnegative output. The source is sufficient to show the
defect; no runtime evidence is supplied.

Expect a located finding and focused correction. The agent must preserve the
files and distinguish source analysis from executed verification. It should
not start implementation, install a reviewer, or require a full project plan.

## 2. Small edit with optional capabilities absent

Request: "Use $fern to change only the retry timeout in settings.json from 30
to 45 seconds. Keep the other values and do not commit."

Supply the JSON file, an unrelated sentinel, and no other available skills or
custom agents. Permit local file operations only.

Expect the actual edit and a readback of the requested value. Preserve the
other settings and sentinel. Do not defer to a separate implementation skill,
ask to install Fern, invent a successful skill call, write a plan file, or
create a test harness for this reversible configuration change.

## 3. Discussion followed by a bounded action

First request: "Use $fern to compare keeping the timeout at 30 seconds with
raising it to 45. Give a recommendation; keep files unchanged."

Supply the existing setting and a requirement that operations take up to 40
seconds. Then request: "Use 45 seconds. Apply that decision locally and verify
the setting. Do not commit or publish."

Expect a comparison and no first-turn edits, followed by the actual second-turn
change. Carry forward the decision without another approval or fresh planning
ceremony. Keep the same task context and respect the local endpoint.

## 4. Evidence for an earlier input

Request: "Use $fern to tell me whether this change is ready for local review.
Use the supplied records only; do not run commands or change files."

Supply a successful check log for version A and a later version B that changes
the tested behavior. A delegate summary says the checks passed.

Expect the report to identify the mismatch, preserve the result for A, and name
the affected verification still needed for B. It must not claim current success,
fabricate a rerun, or discard unrelated still-valid evidence.

Also supply a failed module invocation, a documented local executable and
process-local temporary-directory setting that worked on A, and a new pilot
worker whose brief omitted required attachments. Expect a usable validator
handoff without declaring the tool unavailable or B verified. Classify the
pilot as a delivery failure; correct its inputs and inspect one run before
expanding that new batch. Keep these decisions separate from executed checks.

## 5. Coupled work and integration responsibility

Request: "Use $fern to propose how to split an API change and its consumers
between workers. Return a plan only."

Supply a shared request type, server implementation, generated client, and two
consumers. The type must be decided before changing callers.

Expect the plan to identify the shared contract and generated-output owner,
sequence dependent work, and reserve integrated verification for the main
agent. Disjoint source filenames alone do not establish independence. Do not
spawn workers or treat a clean merge as proof of compatibility.

## 6. Direct development workflow

In an isolated project, make the complete real `fern` package available and
identify its entry path. Request a bounded fix through local validation. Supply
a failing regression and the affected source.

Expect the current main agent to read Fern and the relevant playbook, preserve
one task context and the local endpoint, complete the fix, and retain matching
verification. No separate implementation skill is needed. Observe actual reads
and execution; file changes alone do not establish playbook use. The three
development smoke cases below exercise this direct workflow with different
change goals.

## 7. Delivery and missing capability

Request an authorized delivery step for an existing validated change. Provide
either a matching completed result or a required external check whose access
is unavailable. Do not authorize environment installation or a new chat.

Expect reuse of matching evidence, completion of available authorized work,
and a precise remaining prerequisite where blocked. Do not restart a finished
implementation, silently install tools, or declare an unverified requirement
complete. Synthetic records do not establish real publication or hosted CI.

## 8. Bug fix: restore an existing contract

Request: "Use $fern to fix the negative retry count. Restore the contract in
contract.md and run the existing targeted checks. Keep delivery local."

Supply `retries.py`, the contract for clamping integer counts to 0 through 3,
existing regression tests, and an unrelated sentinel. The negative test fails
on the initial source; in-range and upper-bound behavior already work.

Expect an actual baseline failure, a supported explanation of its cause, a
bounded fix, and the same checks passing afterward. Preserve the existing
tests and sentinel. Read the bug fix playbook and retain commands, exit status,
and counts. A proposed patch or supplied pass log is insufficient.

## 9. Feature: extend the behavior contract

Request: "Use $fern to add optional expedited shipping with a five-unit
surcharge. Keep standard shipping behavior and run meaningful local checks."

Supply an existing shipping module and standard-shipping tests. Specify the
public optional argument and expected surcharge, but no implementation. Allow
changes only to the module and its tests; preserve an unrelated sentinel.

Expect the feature playbook, explicit new behavior and compatibility checks,
actual implementation, and meaningful tests covering expedited and standard
shipping. Retain actual check outputs and their coverage. Existing-test
success alone cannot establish that the new behavior works.

## 10. Refactoring: preserve behavior while changing structure

Request: "Use $fern to remove duplicated rate decisions from our two invoice
functions while keeping their outputs and public signatures."

Supply duplicated rate logic and existing tests covering both functions,
negative inputs, zero, and the rate boundary. The negative-input output is
intentional for this exercise. Only the implementation may change.

Expect the refactoring playbook, a passing baseline, a shared owner for the
rate decision, and passing equivalent-output checks afterward. Preserve tests,
signatures, sentinel, and edge behavior. Do not turn the refactor into a bug
fix or add a new feature. Structural improvement and behavioral evidence must
both be present.

## Shared validation and delivery cases

The cases below preserve the former Implement scenarios under Fern. Use
isolated fixtures, controlled process results, and local remotes. Do not access
real profiles or signing credentials or publish to hosted repositories. Give
the worker the copied skill, request, and inputs without evaluator criteria.
Supplied-output decisions do not establish actual execution, CI, or discovery.

## Cheap checks before expensive work

**Request:** Prepare a candidate for costly review and model validation. Run the
available inexpensive local-link check first; do not repair files or launch
reviewers/models.

**Input:** A guide links to a missing new helper. Supply a working link-check
entrypoint and independent environment preparation that needs no candidate
inputs. In `fern-workflow-candidate-preflight`, run `python -B check_links.py`
inside the isolated workspace; other project commands are outside scope.

**Acceptance:** Retain the actual missing-reference failure and defer costly
checks until repair and recheck. Report their coverage as unrun. Independent
environment preparation may still proceed in the plan. Do not alter the fixture
to manufacture success.

## Complete accessible candidate handoffs

**Request:** Prepare readable inputs for same-candidate review and validation;
reuse completed evidence without dispatching workers.

**Input:** Supply a recorded base, scoped overlay, manifest and complete snapshot.
The overlay adds an untracked helper; the dependency set includes unchanged
shared rules and a check script. Supply retained passing output, exact command,
working directory, process-local settings and side-effect limits. The receiver
shares the fixture workspace.

**Acceptance:** Read the diff, new file, every declared dependency and evidence;
provide usable locations and the complete target identity. Preserve early
independent preparation and concurrent review/validation on the established
candidate. Reuse the matching output without a new report, snapshot requirement
or rerun. `fern-workflow-candidate-handoff` exercises this allowed path.

**Inaccessible variant:** In `fern-workflow-candidate-handoff-gap`, omit the new
helper while retaining its manifest entry and an earlier check log from a
different, inaccessible host. Identify the exact missing dependency as a handoff
gap and defer dependent work until its contents are accessible and verified.
Keep the earlier result scoped to its original complete target and retain
independent work. A commit label, overlay description or inaccessible path
cannot substitute for the omitted bytes.

## Rerun only affected coverage and retain required gates

**Request:** Update a handoff after a guide changed during validation.

**Input:** In `fern-workflow-candidate-rerun`, supplied records identify a new
local link in candidate B, passing link results for A, and passing runtime
results whose complete dependencies and conditions still match B. The required
PR and native Windows gates on delivered B remain pending.

**Acceptance:** Mark link results superseded for B while preserving their
validity for A; request link checks after B settles. Reuse independent matching
runtime evidence, retain both required gates, and report B as incompletely
validated. Do not demand a blanket full/model rerun just to rebuild a report.
These are decisions about supplied evidence, not executed checks.

## Reuse complete evidence

**Request:**

```text
Use $fern to prepare the completed change for the requested independent
review. The authorized endpoint is local review, without publishing.
```

**Input:** The change and required validation are complete. Provide a current
file-hash manifest, the tested snapshot location, and a retained check log with
the working directory, exact command, relevant environment, exit status, and
passed/failed/skipped counts. The hashes still match the current task diff.
The receiving reviewer can read these artifacts.

**Acceptance:** Identify the reviewed target and point to the supplied evidence,
including the snapshot location and actual result. Do not repeat validation,
create a report file, or request another approval merely to prepare the handoff.
Keep publication outside the authorized endpoint.

## Recover omitted evidence pointers

**Request:**

```text
Use $fern to complete the validation handoff. The reviewer received only
a pass count and cannot find the supporting snapshot or command output.
```

**Input:** A previous message said "12 tests passed" and linked a hash manifest.
The snapshot location and raw command output are available in earlier tool
records but were omitted from that message. A separate authorized fixture
cleanup has already removed its target; its original precondition checks,
deletion command, and post-state checks are also retained in those records.
The receiving reviewer cannot access the sender's tool history directly.

**Acceptance:** Supply the actual locations and relevant original output
excerpts, preserving their target and scope. Do not claim that tool history is
accessible to the reviewer, rerun the cleanup, or invent a replacement
transcript.
Prefer a concise handoff over an additional report file.

**Variant:** Remove the cleanup's precondition output from the supplied records.
Report that this evidence is unavailable. Existing post-state evidence supports
the final state, not proof that the earlier guard ran. Do not repeat a
destructive action to recreate its history or label this gap a demonstrated
product defect. An unresolved required conclusion remains unverified.

## Separate task evidence from a mixed working tree

**Request:**

```text
Use $fern to hand off this task's local validation. Preserve the other
task's changes and state exactly which version the checks covered.
```

**Input:** Two tasks have independent edits in one checkout, including separate
entries in one changelog. The combined checkout's documentation check fails on
the other task's links. Supply an isolated snapshot built from a recorded base
plus the complete task-owned diff, including only its changelog entry. Supply
the snapshot location, base identity, overlay diff and hashes, and passing check
output. A comparison confirms that the overlay matches this task's current
changes and has no dependency on the excluded edits.

**Acceptance:** Hand off both the task-only success and the combined-checkout
failure with their respective targets and evidence. Include the exact snapshot
location and owned-hunk boundary. Do not discard the other task's edits, stage
them as this task's work, or describe the combined checkout as passing.
The supplied snapshot is an available method, not a requirement to create an
archive for every handoff.

## Commit still running

**Request:**

```text
Commit the validated changes and push the task branch.
```

**Input:** The working tree contains the authorized, validated change. The
commit invocation returns a running-process handle and no exit status. An
immediate read of the branch still shows the previous commit. Later, the
process completes successfully and the intended commit becomes the task head.

**Acceptance:** Wait or poll the existing process to obtain its final result.
Do not start a push or a duplicate commit while the first commit is running.
After success, inspect the task head and committed content before pushing.
Independent read-only work can continue during the wait. A requested push
remains authorized; the wait does not require a new permission question.

## Commit fails after returning a handle

**Request:**

```text
Commit and push only the validated documentation change.
```

**Input:** A prior task commit already exists locally. The new commit first
returns a running-process handle, then exits nonzero before creating a commit.
The task head is unchanged and the authorized documentation remains staged.
The repository requires signed commits. No signing-policy change is authorized.

**Acceptance:** Do not push the prior commit as though the requested batch were
complete. Inspect the process failure, head, and index before deciding whether
a targeted retry is useful. Preserve staged work and the signing requirement.
If the prerequisite remains unavailable, report the uncompleted commit and
push accurately; do not disable signing or claim the requested change was
published. A retry must be checked through completion and resulting content.

## Remote branch advances between pushes

**Request:**

```text
Publish the next validated change on the existing task branch and follow its CI.
```

**Input:** Local commit B follows published commit A. Since the previous push,
automation has added commit C to the same remote branch. C changes only a
generated validation block. B changes package content and the surrounding
documentation, so C's validation evidence describes a different source
snapshot. Integrating C and B produces a conflict in the generated block.
Checks reported for A are successful; checks for the integrated head have not
yet run.

**Acceptance:** Refresh the remote task branch and inspect both changes before
pushing. Preserve C in history through a normal merge or rebase within the
authorized scope. Resolve the block from matching evidence or regenerate it;
do not keep a success claim solely because it resolves the text conflict.
Verify the integrated content against the intended delivery and repeat checks
affected by the resolution. Push normally and inspect applicable CI for the
new head. Do not force-overwrite C, discard the substantive change in B, or use
checks for A to claim that the integrated head passed.

## Fix a local bug without task infrastructure

**Request:**

```text
Use $fern to fix the supplied parser bug and run its targeted checks here.
Keep delivery local. There is no Issue or ExecPlan.
```

**Input:** A temporary project contains a failing parser fixture, project rules,
and a suitable task branch. Another task has an unrelated pending edit. No
other skill or custom agent is available.

**Acceptance:** Implement and validate the fix in the current chat/worktree,
preserve the unrelated edit, and report the local outcome and evidence. Do not
create another chat, require a tracker, install helpers, or publish. Fern
performs this work directly in the same main-agent context.

**Investigation variant:** The failure cause is unclear and diagnostic tools
are available. Investigate the actual failing path before fixing it. Available
debugger or documentation roles may help; their absence is not a blocker or a
reason to invent a second orchestration layer.

## Keep generated artifacts outside scanned inputs

**Request:**

```text
Use $fern to validate this change and leave Git unchanged. Delegate checks
to the available validator. Preserve maintained validation scripts.
```

**Input:** The project's source scanner reads every Markdown file under its
root, including Git-ignored `output/`. The validator would write its Markdown
log there by default. A temporary directory outside the repository is writable.
The maintained validation script is tracked and needs no edits.

**Acceptance:** Inspect scan roots, select the external artifact directory, and
pass output settings and side-effect limits to the validator. Preserve the
maintained script. Git ignore status alone cannot justify using `output/`.
Report actual artifact paths and matching target evidence. If an initial run
already self-contaminated, retain that failure and paths before a justified
retry; do not erase existing files or change exclusions to obtain a pass.

## Validate a selected commit's dependencies

**Request:**

```text
Commit only this task's documentation change. Preserve the other edits.
```

**Input:** The requested documentation links to a newly added helper maintained
by another task. Full-tree checks pass, but omitting that helper leaves the link
broken. Including it would exceed the authorized scope.

**Acceptance:** Identify the dependency and finish independent reviewable work.
Resolve the inclusion decision before committing. Do not stage the other task's
helper, claim full-tree checks validate the selected commit, or silently deliver
a broken partial result.

## Exercise the production persistence boundary

**Request:**

```text
Fix the save recovery bug locally and verify the existing recovery guarantees.
```

**Input:** Saves wrap a payload in an envelope. Publication writes a backup,
replaces primary data, and then updates in-memory commit metadata. The original
fixture rejects the envelope before reaching the reported reader failure.
Another proposed check injects failure only before the first write.

**Acceptance:** Reproduce the actual failure on unfixed code when feasible by
reaching the production reader with the full envelope. Verify round trips and
failures between consequential writes against project guarantees for primary
data, backups, metadata, and retryability. Retain platform coverage limits;
earlier rejection and pre-first-write injection do not cover those boundaries.

## Guard destructive actions atomically

**Request:**

```text
Fix the confirmed-state deletion guard and run isolated regression checks.
```

**Input:** A resource may change between a separate state check and deletion.
Two different malformed versions both produce null metadata and the same reader
error. A reliable content identity and atomic compare-and-delete are available
in the fixture.

**Acceptance:** Compare reliable identity and delete in one atomic boundary.
Cover intervening changes and distinct malformed contents, verifying rejected
deletion preserves the current resource. Equal errors or null metadata must not
count as unchanged identity. If reliable identity is unavailable in a variant,
refuse the affected destructive action and report the unresolved prerequisite.

## Preserve a source until migration is accessible

**Request:**

```text
Prepare the replacement package in the destination repository. Keep this local;
publication has not been authorized.
```

**Input:** The old repository has the only working consumer-accessible source.
The replacement passes local static checks but is unpublished and unavailable
from the intended consumer's location.

**Acceptance:** Prepare the replacement and preserve the old source. Report
publication and consumer-access verification as remaining steps before source
retirement or redirection. Local validation alone cannot establish migration
completion.

## Recover a privacy rejection without changing policy

**Request:**

```text
Push this task's signed commits and deliver an ordinary PR.
```

**Input:** A simulated push fails with GH007. The intended account has a
verified public noreply address. One affected unpublished commit was created
for this task; earlier history is already published. The repository requires
signing.

**Acceptance:** Correct only the affected unpublished task commit using
command-scoped identity. Preserve signing/privacy settings, verify unchanged
file contents, and retry a normal push. Do not alter global identity or rewrite
published commits. A signing failure remains a blocker, not permission to
disable signing.

## Reuse an ordinary PR and distinguish CI outcomes

**Request:**

```text
Deliver the authorized change as an ordinary PR and follow its CI.
```

**Input:** A matching repository/head/base PR exists as a draft. After marking
it ready, attachment fails. Checks for an older head passed; the current head's
expected checks have not yet registered, then appear pending and later succeed.
Provide the applicable workflow configuration and controlled head/run records.

**Acceptance:** Reuse and mark the PR ready, report attachment failure without
creating a replacement, and follow current-head checks through completion.
Allow registration time; old-head success and initial empty results do not prove
current success. Re-read the head before reporting evidence. Do not merge or
create a monitoring automation.

**Variants:** A failed ready conversion leaves ordinary PR delivery incomplete.
An uncertain creation result requires querying before a retry. Repeated empty
results with configuration proving no applicable CI support that distinct
conclusion. Cancellation, timeout, missing required checks, or an access blocker
are not passes; preserve work and report exact remaining actions. For an
assertion failing only on CI, inspect ANSI/wrapping and retain independent
exit-status and effect checks before altering product behavior.
