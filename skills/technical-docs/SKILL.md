---
name: technical-docs
description: Create, revise, review, or consolidate technical project documentation intended for version control, or compare implementation with identified documents or accepted contracts. Use for requested documentation work or required documentation updates, not explanation-only requests or task tracking.
---

# Technical Docs

Turn project facts, requirements, and decisions into documentation that readers
can use and maintain with the project. Cover existing documents and drafts
intended for the repository; being tracked already is not a prerequisite.

## Scope

Use for requested documentation work, including documentation updates required
by an implementation task and comparisons of identified documents or accepted
contracts with implementation. A comparison can produce findings without
changing documents. Ordinary explanations, design discussions, and coding do not
by themselves request new documents. Review-only requests remain read-only;
authorized revisions should produce the actual edits.

Follow the project's language, source format, paths, templates, and authority.
Keep project instruction governance and persistent execution tracking in their
established workflows; storing those files in Git does not make them ordinary
technical documentation.

## Workflow

1. Identify the readers, what they need to understand, decide, or do, and the
   existing document location. Read local rules and relevant surrounding content
   before adding another entrypoint.
2. Establish the basis: accepted requirements and decisions for intended
   behavior; source, schemas, configuration, tests, and observations for
   implemented behavior. Distinguish both from proposals, assumptions, and
   unknowns. Ask only about material gaps unresolved by available context;
   continue independent authorized work.
3. Choose the smallest useful structure. Make local corrections directly;
   outline substantial new documents or reorganizations before drafting. An
   outline need not create an approval gate. Use the intent table below and read
   only the relevant sections of
   [content-patterns.md](references/content-patterns.md).
4. Write or revise around the reader's questions. Preserve agreed scope,
   normative strength, identifiers, and decision status. When authorities
   disagree, explain the discrepancy and change only the authorized side or
   sides; do not relax a contract to hide an implementation mismatch.
5. Verify the affected content and its relationships using the rules below. For
   substantive reviews or implementation comparisons, use
   [review.md](references/review.md). Fix task-induced problems within scope and
   report remaining gaps.
6. Deliver the requested document, edits, or review. Summarize meaningful
   changes, checks actually performed, and unresolved matters that affect use.
   Documentation work does not itself authorize staging, committing, publishing,
   or unrelated implementation.

## Document intent

| Reader's need | Content to prioritize |
| --- | --- |
| Enter the project or get started | Purpose, prerequisites, first useful result, navigation |
| Establish requirements | Outcomes, scope, observable acceptance, unresolved decisions |
| Propose or record a design | Context, options, evidence, decision status, consequences |
| Consult a contract or reference | Precise behavior, inputs and outputs, defaults, errors, boundaries |
| Understand architecture | Responsibilities, ownership, relationships, flows, constraints |
| Learn, operate, or troubleshoot | Appropriate starting knowledge, actions, expected results, diagnosis and recovery |
| Adopt a new version | Old and new behavior, affected consumers, compatibility and migration |

These are content responsibilities, not mandatory files or development stages.
Sections may serve different needs within one document when their purpose and
status remain clear. Split documents when audience, lifecycle, size, or reuse
warrants it. Do not generate a requirements/design/spec sequence or a directory
tree merely to satisfy a classification.

## Writing and maintenance rules

- Retain necessary constraints and exceptions when shortening text.
- Use steps for ordered actions, tables for comparisons or structured reference,
  and diagrams for relationships or flows when they clarify the content. Match
  the project's renderer; keep diagrams editable and consistent with the prose,
  with useful labels and text alternatives.
- Distinguish runnable examples from illustrative fragments. Give the
  prerequisites, inputs, working directory, placeholders, and expected result
  needed to use the example; do not invent command syntax, outputs, or
  successful runs.
- Maintain an authoritative home for each substantive rule. Link or summarize
  where needed rather than maintaining competing copies. Preserve useful
  navigation and identifiers; repair affected links and anchors when moving or
  renaming content.
- Keep current guidance aligned with its stated version. Preserve historical
  decisions and supersession relationships under local conventions. Add status,
  applicability, or verification dates when they change how readers should use
  the content, rather than requiring metadata and changelogs on every page.
- Update generated documentation through its source and established generation
  process.
- Keep durable contracts and validation entrypoints in project docs; place
  transient execution logs and task progress in their appropriate records. Do
  not freeze private implementation choices without a reader or contract need.

## Verification and delivery

Choose checks that cover the change: relevant source facts and versions, local
paths and anchors, terminology, examples, and rendering. Use the project's
existing documentation checks where applicable. Execute changed runnable
examples in an available, authorized environment; if that is not possible,
identify the missing prerequisite and distinguish static inspection from
execution. Prose-only edits do not require unrelated application tests.

For a substantial new document or reorganization, consider an independent reader
check using the document and the references its intended readers can access.
Check whether readers can find and use the information; this does not establish
technical correctness. Small edits need no fixed interview, brainstorming round,
or independent review ceremony.

Review findings should identify location, evidence, impact, and a focused
correction. Keep unverified questions separate from demonstrated defects. For
requirements, design, or contract readiness judgments, identify the affected
scope and unresolved decisions; document readiness does not certify
implementation.

The source rationale is in [sources.md](references/sources.md). Consult it when
maintaining this skill or resolving a writing-policy question, not as a
mandatory reading or browsing step for each document task.
