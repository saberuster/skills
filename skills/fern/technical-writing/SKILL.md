---
name: technical-writing
description: Create, revise, review, or consolidate technical project documentation intended for version control, or compare implementation with identified documents or accepted contracts. Use for requested documentation work or required documentation updates, not explanation-only requests or task tracking.
---

# Technical Writing

Help readers understand, decide, or act through accurate project documentation.
Existing files and new drafts intended for the repository are both in scope.

## Scope

Use for requested documentation work or updates required by an implementation
task. Explanation, design discussion, or coding alone does not request a document
or implementation audit. Project instruction governance and persistent task
tracking keep their established workflows.

Review without editing unless changes are requested. Complete authorized edits
without expanding the task.

## Workflow

1. **Establish the target.** Identify the reader, intended outcome, document,
   and relevant project rules and evidence. Follow the project's language,
   format, paths, and authority. Ask only about material gaps that cannot be
   resolved from available context. Continue independent authorized work while
   keeping unresolved gaps explicit. Resolve them before claiming completion,
   or report the affected parts as incomplete.
2. **Write or revise.** Use the smallest structure that serves the reader.
   Outline first when scope or structure needs clarification; otherwise write
   directly. Read the relevant [content patterns](references/content-patterns.md)
   when choosing or refining a document type. Preserve scope, decision status,
   identifiers, constraints, and exceptions.
3. **Check and deliver.** Verify affected facts, examples, links, and rendering
   with applicable project checks. Fix issues introduced by the edit and report
   meaningful changes, checks performed, and remaining gaps. For substantive
   reviews or requested implementation comparisons, use
   [review and verification](references/review.md).

## Writing and maintenance rules

- Lead with the reader's answer or next action. Use plain, precise language,
  clear actors, and consistent terms. Explain unfamiliar terms, keep paragraphs
  focused, and remove repetition that adds no useful information.
- Separate accepted requirements, observed behavior, proposals, and unknowns.
  Existing code or passing tests do not establish intended behavior. Explain
  discrepancies without weakening a contract to fit its implementation.
- Keep one authoritative home for each rule. Repair affected links and anchors
  after consolidation or moves; preserve useful history and supersession links.
  Update generated documentation through its source. Add status or version
  metadata only when it changes how readers should use the content.
- Make examples usable: state needed prerequisites, inputs, working directory,
  placeholders, and expected results. Label illustrative fragments; never invent
  commands or successful runs. Run changed executable examples when available
  and authorized, otherwise state what remains unverified.
- Use descriptive headings and link text, and lists, tables, or diagrams when
  helpful. Match the renderer; retain editable diagram sources and consistent
  labels. Keep essential meaning in text, not solely in color, position, or
  images. Prose-only changes do not require unrelated application tests.
- For copied or packaged documents, check links from the intended delivery
  location. Bundled targets must remain available; external references need
  accessible sources. Local existence alone does not prove delivery works.
- Keep durable contracts and validation entrypoints in project docs; put
  transient execution logs and progress in their appropriate records.

Consult [sources](references/sources.md) when maintaining this skill or resolving
a writing-policy question, not during every documentation task.
