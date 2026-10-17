# Bug fix

Restore established behavior. Establish the expected result from requirements,
tests, prior decisions, or the user's report; current code alone does not define
correctness. If the desired behavior is a new decision, resolve that boundary
before implementing it and use the Feature method for the changed contract.

1. Reproduce the reported failure on the relevant surface before editing when
   permitted and feasible. Record inputs, expected/actual results, and the
   affected version. A fixture failing an earlier unrelated guard is not the
   reproduction. If reproduction is blocked, state the gap and investigate
   available evidence without claiming the bug is verified or fixed.
2. Trace the symptom to its mechanism. Test competing explanations with focused
   reads, instrumentation, or experiments. Use a debugger when useful. When
   repeated fixes fail, test their shared premise before another change.
3. Implement the smallest justified correction. Use an architect for a
   consequential boundary change; local restructuring may support the fix.
   Keep unrelated cleanup and new behavior outside the task.
4. Replay the original failure against the fix. Add or use a regression on the
   actual failing path when proportionate, and check affected neighboring
   behavior. A cheap local regression can fail before the fix and pass after;
   do not require a new test framework for a reversible setting change.

Use Fern's shared validation rules. Finish at the authorized endpoint; consult
delivery instructions only when that endpoint includes Git, PR, or CI work.
Report the defect, cause, correction, before/after evidence, and remaining gaps.
