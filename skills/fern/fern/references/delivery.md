# Commit, publication, and CI

Apply only the steps covered by existing user authorization. Preserve the
requested endpoint; the workflow does not authorize merging or monitoring
automations.

## Validate the selected delivery and commit

When delivering part of a changed tree, inspect dependencies on excluded files
or changes. Validate that selected delivery or reuse evidence matching its
complete dependency set. Full-tree success alone is insufficient. Keep
required changes together within scope; resolve any scope expansion before
committing.

Stage only task changes and follow user/project commit conventions and signing
requirements. Run `git diff --cached --check` after staging to include new files.
Wait for each state-changing Git process to finish and read its final result
before dependent operations. A running-process handle is not completion. Check
the resulting task head and content before pushing. On failure or uncertainty,
inspect the head, index, and working tree before retrying; preserve staged work
and do not publish a prior commit as though a failed batch were complete.

## Push without losing remote work

Push only the authorized task branch. Before every push, refresh and compare
the remote task branch, intended base, and local head. Inspect the resulting
diff for unrelated or newly conflicting changes. If another writer or automation
advanced the remote branch, integrate those commits without overwriting remote
history. Preserve authorization limits if integration requires wider changes.

Resolve generated-content conflicts using evidence matching the delivered
source, regenerating it when appropriate. Textual conflict resolution alone
cannot preserve a stale success claim. Verify integrated content and repeat
checks affected by the resolution before a normal push.

For GitHub GH007 rejection, verify the intended account's public noreply
address. Correct only affected unpublished commits created for this task
within authorization. Use command-scoped identity, preserve signing and privacy
settings, verify file contents are unchanged, then retry a normal push. Do not
change global identity or rewrite published commits.

## Create or reuse the task PR

Query for an open PR matching repository, head branch, and base branch. Reuse
it; otherwise create an ordinary non-draft PR unless the user requests draft
delivery. Describe the concrete problem, resulting behavior, and actual
validation. If a matching PR is draft and ordinary PR delivery is authorized,
mark it ready; a failed conversion leaves that endpoint incomplete.

After uncertain PR creation, query again before retrying. When available, call
`attach_artifact` for every created or reused task PR with
`artifact_type: "pull_request"` and its URL. Report unavailable or failed
attachment separately from creation; do not create another PR to retry an
attachment.

## Follow CI for the latest head

Read the PR's latest head SHA. Inspect PR checks, that commit's check-runs and
statuses, and relevant Actions runs. Match runs to the PR and head, including
an associated merge-test run when applicable. Inspect workflow triggers and
branch/path filters and required external checks where configured. An empty
check list alone establishes nothing.

After push or PR creation, allow registration time and recheck empty results
against workflow evidence. Use bounded waits, for example 20-60 seconds with
backoff when unchanged. Keep waiting while applicable CI is pending/running
and progress is possible. Re-read the head after updates and before reporting;
old-head results cannot validate a new head.

| Observed state | Action and conclusion |
| --- | --- |
| Applicable current-head checks succeed | Report passed with head SHA and check/run evidence. Explain skips or neutral outcomes; missing required coverage is not passed. |
| Repeated empty results and no applicable CI in configuration | Report no applicable CI, inspected configuration, and checks made, separately from passing CI. |
| Expected checks missing, pending, or running | Investigate registration and continue waiting. If blocked, report incomplete CI and exact remaining work. |
| Cancelled or timed-out run | Inspect cause; retry only when authorized and useful. These outcomes are not success. |
| Permission or environment blockage | Preserve work; report the failed operation, evidence, and prerequisite. |
| Failed check | Inspect logs and causality. Fix task-induced failures, repeat affected local checks, commit/push within authorization, and follow the new head. Support unrelated failures with baseline evidence; retain uncertainty when unproven. |

If a CLI diagnostic assertion fails only on CI, inspect raw output for ANSI
formatting and wrapping before changing product behavior. Prefer a stable
diagnostic identifier or branch-specific prefix over a full rendered sentence;
retain independent exit-status and file-content or other effect checks.

If continuation needs unavailable access, an external change, or a user
decision, preserve the result and report the blocker and remaining work. Do not
label pending work complete or add an automation to replace CI follow-through.
