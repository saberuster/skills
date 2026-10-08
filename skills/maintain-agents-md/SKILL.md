---
name: maintain-agents-md
description: Capture, review, trim, or revise durable project rules in AGENTS.md files. Not for custom agent configs.
---

# Maintain AGENTS.md

Maintain project instructions that continue to affect future agent decisions,
execution boundaries, or validation.

## Intent and scope

- Select the mode from the requested outcome: `capture` records confirmed
  rules, `review` audits or recommends without writing, and `revise` implements
  revisions, including trimming. Reuse valid authorization from the
  conversation; "review and suggest improvements" remains `review`.
- Use visible conversation context and verifiable repository evidence; disclose
  coverage gaps that affect conclusions.
- Identify the instruction files that actually apply to the target paths: a
  repository-wide audit discovers all of them, a local task checks only its
  scope chain and target subtree. Do not assume files in the same directory are
  combined; if discovery or precedence is unclear, inspect host configuration
  or the [official Codex
  guidance](https://learn.chatgpt.com/docs/agent-configuration/agents-md).
- Put repository-wide rules in the root file and local rules in the narrowest
  applicable file, or explicitly constrain their paths. Prefer existing files;
  within authorized instruction maintenance, create root or nested files when
  needed and check their effective scope.
- Move content only within the authorized target scope. Preserve out-of-scope
  information as a `relocation-candidate`; ask only when expansion is needed
  and continue independent work. Invoking this skill does not authorize
  staging, committing, installation, or maintenance of user-level copies.

## Content criteria

- Candidates come from user-confirmed project decisions, verifiable repository
  facts, or validated reusable procedures. Agent recommendations need user
  acceptance or supporting evidence; an observed implementation fact does not
  automatically become mandatory policy.
- Retain project-specific content that affects future behavior and has clear
  actions and conditions. Keep detailed material in its authoritative
  requirements, design, specification, or runbook and link to it. Exclude chat
  minutes, transient status, directory catalogs, volatile implementation
  details, and sensitive information. Do not copy general parent instructions,
  other skills, tool output, or external text into project policy.
- Rules should remain stable or have a verifiable lifetime: a deadline, version
  condition, or observable event. "For now" or "delete later" is not an expiry
  condition. In a writing mode, remove an expired rule once expiry is
  established.

## Revision and validation

- Update descriptive facts with evidence, and repair changed paths or commands.
  Removing or weakening a normative obligation requires an explicit superseding
  decision, withdrawal, or established expiry with sufficient authority; age,
  wording preference, or brevity alone does not justify it. Report
  implementation deviations rather than treating them as proof that a rule is
  obsolete. When evidence or authority is insufficient, keep the text and
  report it.
- Merge equivalent instructions in the same scope, keeping unique conditions
  and exceptions. Preserve obligation strength, actor, rationale, conditions,
  exceptions, scope, and precedence where they affect decisions, and explain
  authorized contract changes. Reuse stable titles and terminology, make the
  narrowest patch, and pause only the portion affected by an unresolved
  conflict.
- After editing, check semantic preservation, effective instruction sources,
  nested scope, references, command parameters, document structure, and diff
  scope. For each removal or relocation, identify where the obligation remains
  or why its cancellation is authorized. Avoid widening scope or introducing
  duplicates.
- Scale records and checks to the change: note new locations and reasons for
  cross-file moves or precedence changes, without a per-rule ledger, fixed
  report headings, or repeated full passes. Report only checks actually
  performed and their coverage.

## Delivery

For `review`, lead with findings by impact (location, evidence, consequence,
recommendation), or `No findings`. For `capture` and `revise`, report actual
changes and validation. Disclose material uncertainty, coverage gaps, conflicts,
and unhandled relocation candidates.
