# CLI edge cases

## Source listing

Read this section before inspecting source offerings with `add --list`.

In Skills CLI 1.7.0, `add --list` rejects `--json`; inspect source offerings
without that flag. This rejected combination can exit zero while reporting
`status: failed`. Check the reported result as well as the process exit code;
a failed inspection does not establish an empty catalog. Use the available
version's verified capabilities rather than assuming this quirk is universal.

## Direct directory removal

Read this section before direct removal or reconciling source records after a
scoped removal. The entrypoint's authorization, independence, and link-free
conditions must all hold; a CLI-only request rules out this fallback.

Verify that the available CLI leaves the explicitly authorized directory
behind. Resolve its absolute path and confirm it is the intended installation.
Check its ancestors, the target, and every descendant for symlinks, junctions,
or other reparse points that redirect removal. Establish that no other agent
depends on that directory; an independent copy and a link to this target have
different consequences. If any condition cannot be established, preserve the
directory and report the unresolved scope.

Delete only that directory. Preserve other same-name copies and other agents'
links. Use supported CLI operations to reconcile source records only when they
preserve other installations. Keep shared or uncertain records and report any
stale entries that remain; do not invent a registry-repair operation.
