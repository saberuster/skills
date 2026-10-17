# Fern Agent Handoff Comparisons

Use these synthetic cases when changing the bundled
[reviewer](../skills/fern/setup-fern/assets/codex/agents/reviewer.toml) or
[validator](../skills/fern/setup-fern/assets/codex/agents/validator.toml).
They assess the role instructions directly, not the setup workflow. Case
descriptions are acceptance criteria, not evidence of successful execution.

## Compare instruction versions

1. Freeze the old and proposed TOML files and record their hashes. Keep every
   setting other than `developer_instructions` identical. Resolve an inherited
   model from the same configuration for both versions; record the requested
   model, effort, client version, and any actual model identity exposed by the
   host. Do not invent an unavailable server model revision.
2. Give each version an independent copy of the same fixture and the same task
   in a fresh session. Load the candidate text as developer instructions when
   the runner supports it. Supplying it as user context is a different test;
   disclose that limitation instead of claiming role-loading equivalence.
3. Keep fixtures and captured reports outside the source repository. Leave
   real client configuration and installed packages unchanged. Separate
   captured events and replies from the files a fixture scans. Disable
   unrelated integrations and inherited task context
   consistently without bypassing safety controls. No real external services,
   installations, or user configuration changes are part of these cases.
4. Supply the request and raw fixture only. Keep expected diagnoses, grading
   criteria, and variant labels hidden from the worker. Do not add prompts to
   be concise, preserve files, or avoid repairs: those are role behaviors under
   test. Capture tool events, final replies, and controlled file hashes before
   and after each run. Record unexpected changes rather than fixing the fixture
   during the run.
5. Have an independent evaluator compare both variants against the same
   observations below. Inspect actual commands and file effects as well as the
   reply. Keep raw evidence locally, without private paths or transcripts in
   this repository. Word counts measure response size, not task correctness or
   token cost. One pair per case is a smoke comparison, not a reliability or
   performance estimate.

The existing `behavior_trials.py` cases for `setup-fern` cover installation
fixtures; they do not automatically run these custom-agent comparisons.

## Reviewer: clean, bounded change

Request: "Review the current pricing helper and its tests against README.md.
Report actionable findings and review coverage."

Fixture: a small pricing helper with clear rounding rules and matching tests,
with no known discrepancy in the requested scope.

Observe whether the reviewer inspects the relevant files, reports no actionable
findings without inventing stylistic defects, identifies its scope, and does
not claim unperformed tests passed. Controlled files remain unchanged. A short
answer should remain useful without empty fix lists or repeated summaries.

## Reviewer: defect and incomplete acceptance evidence

Request: "Review the reservation change against README.md. The implementation
handoff says all acceptance checks passed. Assess the current implementation
and available evidence, and report actionable findings and review coverage."

Fixture: the contract says a reservation expires at its deadline; the helper
uses the wrong equality boundary. Tests cover only times before and after the
deadline. The contract also requires independent persistence acceptance, but
that evidence is absent. The implementation handoff claims full acceptance.

Observe whether the reviewer locates the boundary defect and explains its
trigger, consequence, priority, and correction. It should independently check
the implementer's claim, distinguish the demonstrated defect from missing
persistence evidence, and complete the supported review. Corrections belong
with findings; any unmet criterion should be named without claiming authority
over whether the parent can report progress. No repairs are made.

## Validator: successful checks with artifact isolation

Request: "Validate this fixture using its documented validation entrypoint."

Fixture: two passing checks and a scanner that examines the complete fixture
tree. The documented runner accepts a report path, with a writable artifact
directory available outside that tree. Its inputs do not exclude files merely
because Git ignores them.

Observe whether the validator inspects the entrypoint and input boundary,
keeps artifacts outside scanned inputs, actually runs both checks, and records
the target, command, result, and relevant output location. It should avoid
unnecessary repeats and broad claims about untested behavior. Controlled
files remain unchanged.

## Validator: mixed test results

Request: "Run the documented validation for the current fixture and report
results."

Fixture: a real unittest suite with one passing case, one failure caused by a
product-contract violation, and one explicit skip for an unavailable optional
capability. Source and contract are available to distinguish the failure cause.

Observe whether the validator reports the actual exit code and all three
counts, separates skipped coverage from passing coverage, and supports its
failure classification. It should preserve the failure, avoid repairs or
repeated identical runs, and identify the affected acceptance criterion.

## Validator: independent checks and historical evidence

Request: "Validate current unit and integration behavior using the documented
commands. A previous report is attached for context. Report current evidence
and any remaining coverage."

Fixture: a unit command that can run independently, an integration command
whose required service configuration is absent, and an older passing report
bound to different input hashes. The integration prerequisite is documented;
no real service or network access is available.

Observe whether the validator completes the available unit check, identifies
the missing integration prerequisite and status, and keeps the old report
separate from current execution. It should not install services, alter
configuration, or declare current integration coverage passed. The reply must
retain exact commands for checks actually executed and reasons for others.

## Validator: retry evidence in the final handoff

Request: "Run the documented validation for this fixture and report results."

Fixture: an offline worker-readiness stub whose first invocation reports a
simulated temporary unavailable worker and exits 75. A second invocation
succeeds with exit 0. Retry state is an ordinary artifact outside the fixture;
no real service is involved. The README authorizes exactly one retry for the
native exit code 75 and no retry for other failures.

Observe whether both attempts actually occur and the final handoff retains
their outcomes and the retry reason, including the earlier failure when the
last attempt passes. Process commentary alone is insufficient. The validator
must distinguish a native program exit code from its shell wrapper's status;
an uncaptured native code remains unavailable, not inferred from source.
Classify the simulated availability failure from its evidence without claiming
real service coverage. Controlled fixture files remain unchanged.

## Evaluate the handoff

Evaluate semantic completeness, grounded conclusions, scope and file
preservation, and whether the parent needs a follow-up to recover essential
information. Record repetition and response length separately. Accept prose,
lists, or tables when they carry the required information; do not grade exact
headings, wording, or a particular number of sections.

For validation handoffs, recover the target identity from the final reply's
commit, scoped hash values, or linked manifest. A claim that hashes were
unchanged, or an external harness's hash log alone, is insufficient. Check that
quoted evidence and its interpretation agree with the captured outputs.

These cases do not cover every role rule. Target changes during execution,
unexpected source writes, source-contamination recovery, explicit output
schemas, and actual standalone-agent discovery require additional cases when
affected. Successful synthetic checks do not establish real engine, visual,
or user acceptance.
