# Content patterns

Read the sections relevant to the document's purpose. These are questions to
answer, not mandatory templates. Combine purposes in clearly identified sections
when that serves the same audience; split files when audience, authority,
lifecycle, or navigation warrants it. Do not automatically create separate
requirements, design, and specification files or four documentation directories.

## Entry and onboarding

- Explain the project's purpose, intended users, and the first useful outcome.
- Provide supported prerequisites, setup, and a short path to that outcome,
  including how to recognize success.
- Link to maintained development, contribution, configuration, and support
  material instead of duplicating it.
- State relevant limitations or environment differences before the reader
  encounters them.

## Requirements and acceptance

- Identify the problem, actors, intended outcomes, scope, non-goals, and
  relevant dependencies or constraints.
- Express each requirement through observable conditions and results. Use
  scenarios, thresholds, state tables, rules, or Given/When/Then where useful.
- Check requirement-to-acceptance coverage when requirements have traceable
  identifiers.
- Include performance, reliability, security, privacy, accessibility,
  compatibility, and observability requirements only when relevant; define how
  each will be judged.
- Keep unresolved product decisions visible rather than completing a template
  with invented commitments.

Illustrative acceptance condition, not a universal threshold:

> Given a user with an expired invitation, when they submit it, the service
> rejects the request with `INVITATION_EXPIRED` and does not create an account.

## Design, RFC, and ADR

- Explain the decision boundary, context, drivers, and constraints. Describe
  alternatives only as far as needed to understand the choice; one viable option
  can still warrant a record of its consequences.
- Place supporting evidence beside the claim or decision. Separate measured
  results from hypotheses and describe what evidence would invalidate the
  rationale.
- Record the decision and its status using the project's vocabulary, including
  provisional or unresolved choices where applicable.
- Cover relevant consequences: ownership, dependencies, security/privacy,
  operations, performance, compatibility, migration, rollback, and risks.
- Preserve accepted decision history and supersession links according to project
  conventions. Keep current usage instructions current without rewriting
  historical rationale as though it were always true.
- Link stable conclusions to the local contract authority when the project
  separates it from design history. An approved RFC may itself be authoritative;
  do not require another document.

## Contracts and reference

- Define observable guarantees and relevant scope, ownership/source of truth,
  invariants, interfaces, state transitions, and conformance criteria.
- State applicable conditions, inputs, outputs, side effects, errors, recovery
  behavior, and non-guarantees. Consider persistence, permissions, concurrency,
  and idempotency when they affect consumers.
- For API, schema, and configuration reference, preserve exact identifiers and
  cover types, defaults, allowed values/ranges, precedence, required fields, and
  version availability where relevant.
- Use MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY only for actual obligations or
  permissions. State the project's interpretation when needed.
- Leave private helpers and algorithms open unless they are themselves an
  accepted constraint. Describe consumer-visible behavior rather than producing
  a code inventory.
- Keep durable validation entrypoints and conformance criteria here; keep
  individual command runs and their results in validation or execution records.

Illustrative contract:

> Cancelling a pending job MUST set its state to `cancelled` and emit one
> `Cancelled` event. Repeating cancellation MUST return `cancelled` without
> another event. Cancelling a running job MUST return `conflict` without
> changing state. The locking strategy is an implementation choice.

## Architecture and explanation

- Explain system boundaries, component responsibilities, ownership,
  dependencies, and the relevant flow of data or control.
- Describe important lifecycles and constraints, including where state is owned
  and how failures cross boundaries.
- Use a diagram when relationships or sequence are easier to understand
  visually. Match labels to code and prose; identify the diagram's scope and
  preserve its editable source.
- Give enough rationale to explain the structure. Link to decision records and
  interface references for details that already have a maintained home.

## Tutorials, tasks, and runbooks

- A tutorial should guide a learner through a coherent example with explanations
  and checkpoints. A task guide should help a prepared reader accomplish a
  specific goal.
- State relevant prerequisites, permissions, versions, environment, and starting
  state. Explain placeholders and whether examples are complete or illustrative.
- Order actions by dependencies; show expected output or another success check
  where it helps the reader proceed.
- Include likely failure paths and recovery. For runbooks, state operational
  triggers, checks before acting, impact, stop conditions, and escalation or
  rollback when applicable.
- Distinguish commands verified in the applicable environment from commands
  reviewed only as text.

## Troubleshooting

- Start from an observable symptom, exact error message, or diagnostic result.
  Preserve exact error strings needed for search, including localized strings
  when necessary.
- Separate confirmed causes from possible causes and provide checks that
  distinguish them.
- Distinguish a workaround from a resolution, explaining relevant limitations
  and side effects.
- Show how to verify recovery and when the available evidence calls for
  escalation. Avoid presenting an unverified guess as the cause.

## Migration and release information

- Identify the affected versions and consumers, old and new behavior or
  guarantees, compatibility impact, and necessary action.
- Explain prerequisites, order-sensitive migration steps, deprecation behavior,
  and how consumers can verify completion.
- Describe rollback when feasible and relevant, including restrictions after
  irreversible data or schema changes.
- In release notes, prioritize reader-visible effects and required actions; link
  to detailed migration or reference material.
- Preserve identifiers and traceability across renamed or replaced contracts.
  Follow project conventions for historical release records.
