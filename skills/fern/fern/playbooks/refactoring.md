# Refactoring

Change internal structure while preserving the agreed observable contract.
Name the structural benefit and boundaries to preserve: callers, outputs,
errors, side effects, ordering, persisted formats, and performance constraints
where relevant. A nicer directory layout alone does not establish an improvement.

1. Inspect the actual callers and current behavior. Select existing checks or
   capture a focused characterization, snapshot, or old/new comparison before
   moving code. Type checks and lint alone do not prove behavioral equivalence.
2. Define the target structure and why it reduces coupling, duplication, hidden
   state, or reading effort. Use an architect for consequential ownership or
   compatibility choices. Prefer a small concrete improvement over speculative
   abstraction; do not impose a fixed redesign on a local cleanup.
3. Move in small verifiable steps. Update affected callers, generated artifacts,
   and references; check string-based uses during renames. Remove superseded
   internal paths when all consumers have moved. Honor external compatibility
   and published-source migration requirements.
4. Compare behavior at the preserved boundaries and inspect the integrated
   diff. Keep edge cases and failure behavior in the comparison. Verify the
   promised structural benefit as well as the preserved behavior.

If an existing bug or desired feature emerges, identify it separately. Do not
silently change behavior during a refactor. Include the fix only when the task
already authorizes it or the scope is extended; separate its acceptance and
evidence from the equivalence claim.

Use Fern's shared validation and authorized delivery rules. Report the
structural change, preserved contract, equivalence evidence, benefit, and gaps.
