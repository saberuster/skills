# Content patterns

Use only the sections relevant to the reader's purpose. These are content needs,
not mandatory templates or stages. Combine purposes when they serve the same
reader; split files when audience, authority, lifecycle, or navigation warrants
it. Do not create a requirements/design/spec sequence just to fit a taxonomy.

## Entry and onboarding

- Give the intended reader a short path from prerequisites to a first useful
  result, including a success check and relevant environment limitations.
- Link to maintained setup and support details instead of duplicating them.

## Requirements and acceptance

- State the problem, affected users, desired outcomes, scope, and constraints.
  Make requirements observable and connect acceptance conditions to their IDs.
- Include quality requirements only when relevant, with a way to judge them.
  Keep unresolved choices visible rather than inventing commitments.

Illustrative acceptance condition:

> Given a user with an expired invitation, when they submit it, the service
> rejects the request with `INVITATION_EXPIRED` and does not create an account.

## Design, RFC, and ADR

- Explain the decision, meaningful alternatives, evidence, and consequences.
  Separate measured results from hypotheses and provisional from accepted choices.
- Preserve decision history and supersession under project conventions. Do not
  rewrite historical rationale as though current guidance had always applied.
- Link stable conclusions to their contract when separate. An approved RFC may
  already be authoritative; do not require another document.

## Contracts and reference

- Describe observable guarantees, conditions, inputs, outputs, errors, and
  recovery. Include ownership, state transitions, persistence, concurrency, or
  idempotency where they affect consumers; leave private algorithms open unless
  they are accepted constraints.
- Preserve exact API and schema identifiers, types, defaults, allowed values,
  precedence, required fields, and applicable versions.
- Use MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY for actual obligations or
  permissions. Keep conformance criteria and validation entrypoints here;
  individual run results belong in execution records.

Illustrative contract:

> Cancelling a pending job MUST set its state to `cancelled` and emit one
> `Cancelled` event. Repeating cancellation MUST return `cancelled` without
> another event. Cancelling a running job MUST return `conflict` without
> changing state. The locking strategy is an implementation choice.

## Architecture and explanation

- Explain boundaries, responsibilities, state ownership, dependencies, and the
  relevant flow, including lifecycle and failure boundaries.
- Use diagrams when helpful and link to maintained decisions and interfaces
  rather than producing a code inventory.

## Tutorials, tasks, and runbooks

- Tutorials develop understanding through a coherent example; task guides help
  prepared readers achieve a goal. State the starting state and show success.
- Number reader actions in dependency order and distinguish system responses
  from actions. Place applicable conditions before the instruction.
- For runbooks, include triggers, impact, checks before acting, stop conditions,
  and recovery or escalation where applicable.

## Troubleshooting

- Start from an observable symptom and preserve searchable error strings.
- Separate confirmed causes from hypotheses, with checks to distinguish them.
  Identify workaround limits, how to verify recovery, and when to escalate.

## Migration and release information

- Explain affected versions and consumers, behavior changes, compatibility,
  and required actions. Include order-sensitive steps, deprecations, completion
  checks, and rollback limits where relevant.
- Preserve identifier traceability and historical records. Release notes should
  emphasize reader-visible effects and link to detailed migration guidance.
