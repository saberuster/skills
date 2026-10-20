# Validation and evidence

## Prepare the candidate and handoff

Establish the intended candidate before formal review or validation. Record the
base and complete scoped changes, including staged, unstaged and relevant
untracked files, or use an isolated snapshot with its complete dependency set.
Include required helpers, fixtures and shared resources, and identify owned
hunks in shared files. A commit label or tracked-only diff cannot describe
uncommitted additions. Reuse project plans, manifests and drift detection;
neither a separate report nor an immutable copy is required for every task.

Run applicable inexpensive checks first: local links, package validation,
formatting or compilation. A deterministic failure that invalidates the
candidate blocks costly review, runtime or model checks until repaired and
rechecked. Keep the failure evidence and report the blocked coverage. Environment
preparation may proceed early when independent of candidate edits; review and
validation may run in parallel once their inputs identify the same candidate.
This ordering does not replace any required repository gate.

Before dispatch, verify the receiver can read the diff, new files, complete
declared dependencies and supporting evidence in its working environment.
Supply the exact working directory, known-working command entrypoints, required
process-local settings, allowed side effects and evidence locations. A path on
another host or private tool history is not accessible input. Supply readable
copies or relevant original excerpts where appropriate; if inputs remain
inaccessible, report the handoff gap and defer only dependent work.

## Select checks and contain artifacts

Use applicable project entrypoints and acceptance criteria. Keep maintained
validation code separate from generated data. A request to leave Git unchanged
does not alone require moving reusable scripts outside the repository. Honor
explicit location choices; otherwise retain maintained scripts with the project.

Inspect discovery roots and exclusions before choosing output paths. Use the
project's designated artifact directory only when excluded from check inputs;
verify repository outputs are ignored and untracked and exclude them from
source snapshots. This includes caches, logs, temporary data, and shared locks.
If no suitable exclusion exists, use a task-specific temporary directory outside
scanned roots, preferably outside the repository. Redirect process-local cache
or output settings without changing project configuration solely to obtain a
pass. Preserve required in-tree build outputs; block only checks whose effects
remain unresolved.

Give delegated validators the target, allowed commands and side effects, input
boundaries, and artifact locations. Carry forward known-working interpreter and
tool entrypoints, required process-local environment or temporary-directory
settings, and known blockers. They collect evidence without implementing fixes
or changing controlled sources, documentation, fixtures, snapshots, assets,
manifests, or lockfiles. If a check unexpectedly changes controlled files, stop
that check, preserve the state, and report the paths. On contamination, retain
the failure and affected paths before a justified retry. Do not delete existing
files or change discovery exclusions to make the check pass.

For a new or changed isolated-agent delivery method, check one run's actual
input reads and scope before expanding the batch. Keep evaluator material out
of worker inputs. An omitted attachment or wrong working directory is a
delivery failure; correct it before judging the skill's behavior.

## Match evidence to delivery

For validation or review handoffs, retain the tested commit and relevant changes
or scoped hashes, working directory, exact commands, material environment,
observed exit codes, counts including skips, covered changes, and accessible
supporting output. Distinguish each check's exit code from a wrapper's status.
Include relevant preconditions for operations that cannot safely be repeated.

For isolated snapshots, give the location, recorded base and overlay, dependency
set, and relationship to the task diff, including owned hunks in shared files.
Report combined-working-tree failures separately. Snapshot success does not
validate other edits or the combined tree. Recheck target identity before
reporting; changed inputs make old results stale for the new target.

When inputs change during or after checks, identify affected checks from their
actual dependencies and conditions. Mark their prior evidence superseded for the
new candidate, retain it for the original target, and rerun necessary coverage
after the edits settle. Reuse matching results for unaffected dependencies;
do not request a blanket full rerun merely to assemble a report. If dependency
coverage is uncertain, report that gap and broaden the affected checks enough
to resolve it. Preserve all required repository gates, including independent PR
checks; a focused rerun is not a waiver of remaining coverage.

Reuse accessible artifacts and tool records when the target and conditions
match. Supply missing locations or actual output excerpts when the receiver
cannot access original records. Repeat only checks needed to close a real
evidence gap, when safe and authorized. Do not repeat a destructive action to
recreate its history. State unavailable evidence and the conclusions it leaves
unverified. No separate report file or independent review is mandatory.

Classify failed checks using baseline, fixture, and environment evidence. Fix
task-induced failures and rerun affected coverage; retain uncertainty when the
cause is unproven. An invocation failure alone does not establish that a tool
is unavailable; check documented or previously working local entrypoints first.
A zero exit code does not establish required coverage, and skipped checks are
not passes.

## Regressions, persistence, and guarded mutations

When adding a regression, reproduce the reported failure on unfixed code when
permitted and feasible. Verify the cause and reached boundary. A fixture that
fails an earlier guard for a different reason must be adjusted before it can
support the intended regression claim.

For serialization or persistence changes, round-trip the complete written
format, including outer envelopes, through the production reader. For
multi-step publication, exercise failures between consequential writes. Check
the project-defined guarantees for primary data, backups, in-memory commit
metadata, and retryability. Failure injection only before the first write does
not cover intermediate failure. Limit platform-specific filesystem claims to
the platforms actually verified.

For destructive actions conditioned on captured or user-confirmed state,
compare the expected state and mutate within one atomic boundary, such as a
transaction, lock, or compare-and-swap. Require reliable version or content
identity under the project contract. Null metadata, matching error categories,
and unknown identities do not establish unchanged resources. Refuse the action
when identity cannot be established. Regressions should cover intervening
changes and distinct contents producing the same fallback/error, and verify
that rejection preserves the current resource.
