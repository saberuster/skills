# Runner Contract

Read when integrating/debugging `scripts/invoke_godot.ps1`, inspecting detailed
structured results, or assessing host supervision and cleanup boundaries.
Ordinary invocation, path checks, timeouts, exit codes, and required evidence
remain in [Validation and Build Support](validation.md).

## Supervision and Lifetime

The PowerShell 7.2+ runner supports Windows and Linux. Linux controller-liveness
monitoring requires kernel 5.3+ pidfd and x64/ARM64.

Before launching Godot, the supervisor joins a Windows Job Object (kill members
when the last handle closes; disallow breakaway) or creates a Linux
session/process group. It retains execution-unit identity after engine exit
until controller cleanup. On abnormal controller exit, Windows cleans up through
Job handle lifetime; Linux detects pidfd/controller-pipe EOF and terminates its
own group. Other hosts need equivalent existing supervision; do not fall back to
unconstrained launch.

## Cleanup Confirmation

`run.termination=execution-unit-empty` and `cleanupConfirmed=true` mean only
that Windows Job ActiveProcesses was zero at inspection, or the Linux group had
no live executable processes. Z/X members no longer execute; the host owns
reaping. Failed/timed-out inspection reports `termination-unconfirmed` and
retains `cleanupError`.

This guarantee excludes Linux descendants deliberately escaping through
setsid/setpgid, processes launched by external services, and whole-host
termination. Use stronger existing project supervision if those capabilities are
needed. Waiting for the parent alone cannot confirm descendants; see [.NET
Process.Kill](https://learn.microsoft.com/en-us/dotnet/api/system.diagnostics.process.kill?view=net-10.0#remarks)
and [Windows Job
Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects).

Linux checks compare PID namespaces and `NSpgid`; do not treat `/proc/<pid>`
directory names from ancestor-namespace mounts as execution-unit process IDs.
Existing groups with unobservable members remain explicitly unconfirmed.
Namespace fields/controller probes follow
[proc_pid_status](https://man7.org/linux/man-pages/man5/proc_pid_status.5.html)
and [pidfd_open](https://man7.org/linux/man-pages/man2/pidfd_open.2.html).

## Output and Failure Evidence

Preserve actual engine exits separately from supervision termination. No
obtained engine exit means `godotExitCode=null`. Keep run identity, partitioned
arguments, artifact paths, output-collection status, and cleanup errors even
when collection fails. A timeout, open output pipe, or unconfirmed cleanup
cannot count as success. The invocation reference defines exit precedence,
status codes, and bounded collection/confirmation waits.

The supervisor closes completed capture writers before reporting successful
output collection. After successful collection and confirmed process cleanup,
inspect the fresh main log plus this run's stdout and stderr capture files. Keep
`unclassifiedErrors` as an array of original error-header strings, deduplicated
by exact text across channels, capped at 50 entries in main-log/stdout/stderr
order. Scan every channel even after reaching the cap so read failures remain
visible. `messages` identifies channels with errors and their artifact paths;
existing JSON fields and CLI parameters remain unchanged. The existing
`AllowedLogErrorPattern` applies to raw error lines in all three channels.

With native exit zero and a fresh main log, unclassified errors in any channel
return `67 / log-errors`. A missing or unreadable capture returns `69 /
output-collection` after zero exit and records the inspection failure in
`run.outputError`; preserve a nonzero native exit instead of replacing it.
Existing timeout, cleanup, output-failure, native-exit and stale-log precedence
remains unchanged. Retain captured errors as evidence even when the main log is
stale. Empty readable captures are valid, and ordinary warning lines alone do
not fail the run.

Process cleanup evidence does not establish that engine objects or Resources
were released. Keep shutdown errors visible even when gameplay assertions
passed; do not automatically allowlist them.
