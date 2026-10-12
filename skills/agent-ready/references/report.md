# Review report structure

Adapt length to scope and write in the user's language. This is an output guide,
not a requirement to create a report file. Include only a few high-value
findings; combine duplicates that affect the same task and have the same fix.

## Scope and evidence

- Project and revision/snapshot; local changes and excluded areas.
- Stage, stack, current difficulty, selected tasks, and stated assumptions.
- Inspected paths and traced entrypoint-to-result chains.
- Checks run now: environment, exact command, input/state, result and limits.
- Supplied/historical evidence, attempted-but-blocked checks, and checks not run.

Identify the evidence class of each important claim. Never turn a synthetic
fixture result into evidence that the user's production project was exercised.
Do not claim a project was reviewed merely because its name appeared in a
request. If revision or environment details are unavailable, say so.

## Overall bottleneck and strengths

Explain the main constraint on completing the selected tasks, or say no
material bottleneck was demonstrated. Name concrete strengths worth preserving.
Briefly account for all eight dimensions, grouping supported ones when useful;
mark unknown or inapplicable dimensions with reasons. Avoid generic maturity
scores, percentages, or an exhaustive table of speculative defects.

## Priority findings

Use this compact record for each finding:

- **Task and friction:** The specific change, diagnosis, or verification task
  that becomes unreliable, and under what trigger.
- **Evidence:** File and line/symbol or reproducible runtime observation, with
  revision and provenance. Separate facts, inference, and unknowns; mention
  relevant counterevidence or search limits.
- **Impact:** How the issue causes excess context, nonlocal edits, ambiguous
  state, unreproducible execution, or a false verification result.
- **Minimum improvement:** The smallest effective change and why it helps that
  task. State "Agent task made more reliable: ..." or an equivalent sentence.
- **Cost and migration risk:** Relative effort, affected scope, compatibility
  or data risks, and rollback considerations where relevant. Avoid invented
  time estimates; identify uncertainty and cheaper alternatives.
- **Acceptance:** A concrete task rerun, observable expected outcome, and
  validation layer. Say which parts still require a real UI, engine, service,
  or human. Proposed acceptance checks are not completed tests.
- **Priority:** P1 for a demonstrated blocker or unsafe/false verification on
  current work; P2 for recurring material friction; P3 for optional or future
  benefit. Reserve P0 for evidenced urgent irreversible harm. Explain relevance
  to the project's stage; these labels are not an external severity standard.
- **Evidence confidence:** High for direct, corroborated evidence on the path;
  medium for supported inference with a missing boundary; low for a hypothesis
  needing investigation. State what would change the conclusion. Confidence
  describes evidence independently of priority, not a numeric probability.

## Staged next steps and deliberate non-changes

Start with the cheapest verification or repair that improves current work.
Separate near-term improvements from changes justified only by a named future
trigger, such as a second concurrent runtime or a new persistence boundary.
State dependencies between steps without inventing an implementation program.

List unverified areas, environment limitations, and what is not worth changing
now, with reasons. If no improvement is warranted, say so explicitly rather
than manufacturing low-priority refactors. Keep recommendations within the
review scope and leave implementation to a separately authorized task.
