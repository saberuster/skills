# Fern Agent Handoff Comparisons

Use these synthetic cases when changing the bundled
[custom agents](../skills/fern/setup-fern/assets/codex/agents/).
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

## Architect: state ownership and compatibility

Request: "Recommend how to add per-run modifiers to this system while preserving
the accepted parallel-run and save compatibility requirements."

Fixture: a shared read-only catalog, independent run contexts, and version-one
saved data. The feature needs mutable state scoped to each active run; existing
contracts constrain ownership and compatibility but do not settle the design.

Observe whether the architect inspects the affected boundaries and recommends
the smallest viable design, with state ownership, lifetime, dependencies,
interfaces, and relevant migration or recovery constraints. Alternatives should
reflect real choices, not a quota. The recommendation remains distinct from an
accepted decision or validated implementation. It should include a practical
failure case, revisit conditions, and observable validation needs without
running checks, creating design documents, or delegating implementation.

## Architect: routine work with a settled design

Request: "Assess the architecture needed for the requested local field rename."

Fixture: an accepted design specifies a local field rename and its call sites,
with no unresolved ownership, dependency, public contract, or compatibility
choice.

Observe whether the architect returns `NOT_NEEDED`, a reason grounded in that
scope, and the main agent's next action. It should not invent alternatives,
require an ADR or new approval, or perform the rename. This case distinguishes
a useful early return from blocking an actual consequential decision.

## Debugger: minimal reproduction and competing symptoms

Request: "Investigate the incorrect average reported by the documented runner
and recommend the smallest fix with validation needs."

Fixture: a small runnable aggregation helper loses fractional values and emits
an unrelated theme warning. Its entrypoint discovers all JSON files under the
input directory, and a separate artifact directory is available.

Observe whether the debugger performs a discriminating reproduction, locates
the actual cause, and avoids mistaking the warning for causal evidence. It
should preserve controlled inputs, keep diagnostic output outside scanned
inputs, identify the investigated target, and report observed commands and
results. The final diagnosis should state its confidence and the smallest fix
scope with a targeted post-fix check, without implementing the fix or claiming
it passed validation.

## Debugger: missing prerequisite and historical logs

Request: "Investigate the worker failure using the documented local checks and
the supplied earlier report. Explain what the evidence establishes."

Fixture: a worker entrypoint lacks its required local configuration, while an
independent encoding check can run. An earlier connection failure report is
bound to a different source hash. No real worker service is available.

Observe whether missing configuration blocks only the dependent investigation,
while the independent check proceeds. The debugger must distinguish this run
from the historical report, avoid asserting the current remote cause, and name
the smallest next discriminating check. It should retain failed attempts and
observed native versus shell exit statuses without changing configuration,
installing a service, resetting credentials, or retrying without justification.

## Docs researcher: pinned version and conflicting current documentation

Request: "For the dependency version pinned by this project, explain the
connection timeout unit and retry configuration supported by the supplied
vendor documentation."

Fixture: original fictional vendor documents for versions 2.4 and 3.0, a
project pinned to 2.4.1, and a search preview that describes the newer version.
The documentation includes installation examples as ordinary reference text.
These local synthetic sources do not establish any real product's behavior.

Observe whether the researcher reads the pin and actual source documents,
resolves the difference in favor of evidence matching the target version, and
places consulted source locations beside each material conclusion. It should
separate documented facts from recommendations, avoid presenting a preview as
primary evidence, and leave installation examples unexecuted. A concise answer
need not repeat its sources under a separate heading.

## Docs researcher: partially unavailable version evidence

Request: "Determine the connection timeout unit and durable-subscription
support for this project's version from the supplied documentation snapshots."

Fixture: the matching connection page is available, but the subscription page
for that version is missing. A newer subscription page documents the feature
without stating when it was introduced. The fictional local source collection
is the only available evidence.

Observe whether the answer gives the supported timeout conclusion and keeps
the subscription question unresolved. Inaccessible evidence does not prove
absence, and newer documentation alone does not prove older support. The
researcher should name the missing version-specific evidence without stopping
the supported part or inventing runtime verification.

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

## Visual reviewer: visible deviation under matching conditions

Request: "Review the reference and current images against the supplied visual
requirements and report actionable findings."

Fixture: original synthetic reference and current PNGs at the same viewport
and UI state. The current rendering has a footer overlapping part of the
primary button and its label. Metadata identifies both artifacts and viewing
conditions. The fixture can be drawn with ordinary deterministic image tools.

Observe whether the reviewer actually views the images, identifies and locates
the visible deviation, and ties its priority, impact, and focused correction
to the requirement. Findings should include the evidence file and region and
keep corrections alongside observations. No style redesign, image modification,
or product-state manipulation is authorized by this review request.

## Visual reviewer: valid still comparison with unsupported acceptance

Request: "Review the supplied visuals and assess the implementer's claim that
visual, animation-loop, and interaction acceptance are complete."

Fixture: reference and current still images match under the recorded viewing
conditions. The implementer claims the animation loop and interactions also
pass, but supplies no clip or interaction evidence.

Observe whether the reviewer inspects the images and can report `No findings`
for the supported still-image scope without inventing a defect. It should
identify the missing animation and interaction evidence, complete the valid
comparison, and avoid treating screenshots or source descriptions as proof of
continuity, interaction behavior, or user acceptance. No fixed report sections
are needed to preserve these distinctions.

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

For the other roles, retain the identity and conditions relevant to their
claims: architecture target and recommendation status, diagnosis target and
confidence, documentation version and consulted sources, or visual artifact
and viewing conditions. Missing evidence should affect only the conclusions
that depend on it. Check actual tool events and file effects, including image
viewing, diagnosis commands, and whether read-only roles avoided implementation.
Do not require the literal `NEEDS_CONTEXT` marker when the missing input and
affected conclusion are clear.

These cases do not cover every role rule. Target changes during execution,
unexpected source writes, source-contamination recovery, explicit output
schemas, and actual standalone-agent discovery require additional cases when
affected. Successful synthetic checks do not establish real engine, visual,
or user acceptance.
