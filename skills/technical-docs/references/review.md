# Review and verification

Use the sections needed for the request. A local correction needs its relevant
context and checks, not a full audit. Reviewing alone does not authorize edits;
when revisions are requested, complete the corrections within that scope.

## Purpose and evidence

- Can the intended reader understand, decide, or do what the document promises?
  Does its introduction match the actual coverage?
- Are facts supported by the relevant project sources, with intended behavior,
  observed behavior, proposals, assumptions, and unknowns distinguishable?
- Do omissions, contradictions, or ambiguous terms change a reader's decision or
  action? Check applicable roles, prerequisites, configuration precedence,
  failure paths, and compatibility.
- Are requirements observable and covered by acceptance conditions? Are quality
  attributes included only when relevant and measurable?
- Do design records explain meaningful alternatives and the evidence for a
  decision, its status, and relevant consequences? Follow local ownership and
  dating conventions without inventing metadata.
- Do contracts specify guarantees and non-guarantees without unnecessarily
  fixing private algorithms? Existing code or passing tests alone do not
  establish intended behavior.
- Are instructions and examples consistent with their stated environment and
  version? Separate expected sample output from output actually observed.

## Reading and maintenance

- Check information order, useful headings, terminology, cross-references, and
  distracting repetition. Keep conditions close to the actions or claims they
  qualify.
- Check links, anchors, exact paths, images, and the existing documentation
  build or lint rules as applicable. Inspect the rendered result when layout,
  diagrams, or format-specific features changed; disclose an unavailable
  renderer.
- Check whether readers can access the referenced material. A useful
  cross-reference need not be expanded into duplicated prose.
- After consolidation, preserve relevant decisions, requirement IDs, current
  entrypoints, and history. Update affected inbound links and document
  replacement locations under local conventions.
- Keep current guidance and historical records distinguishable. A recent Git
  modification date is not proof of technical revalidation.

For substantive new or reorganized content, an independent reader can work
without the author's conversation history. Provide the intended audience,
document, and normally available references. Ask realistic questions such as
locating the correct procedure, explaining a component boundary, or identifying
success and failure outcomes. Revise supported gaps; do not require a fixed
question count or repeated passes without new concerns. Reader comprehension is
separate from source verification and execution.

## Implementation reconciliation

Use this branch when asked to compare identified documentation or accepted
contracts with an implementation. Do not turn ordinary writing or an informal
code explanation into an implementation audit.

1. Establish the requested document version, implementation revision and
   relevant local changes, comparison scope, environment, roles, and evidence
   time. Do not substitute an older deployment or test report for the requested
   checkout.
2. Associate each capability with its accepted basis. Trace the complete user
   entrypoint and the layers needed to fulfill it; a helper, schema, or isolated
   instance does not establish the whole capability. Undecided behavior is an
   open design question, not a demonstrated missing feature.
3. Separate source/configuration evidence, checks actually executed for the
   relevant target, and gaps. Distinguish unobserved behavior, unavailable
   prerequisites, and demonstrated contract violations. Label historical
   evidence and unsupported completion summaries accordingly.
4. For each compared capability, show the accepted basis, implementation
   evidence, runtime evidence, and remaining gap or next step. Use a compact
   table or equivalent format. Limit the conclusion to the scope and conditions
   these observations support.
5. Explain disagreements without silently rewriting requirements, weakening
   contracts, or changing code to make the comparison pass. Make only the
   document or implementation changes already authorized; a gap in one
   capability need not stop independent work.

When follow-up tasks are requested, include the observation and source, user
scenario, expected change, preserved contracts, and observable acceptance. The
comparison alone does not request a roadmap or implementation.

## Findings and readiness

Lead with findings ordered by impact, each with a location, evidence, concrete
consequence, and correction. If none are supported, say `No findings` and state
meaningful coverage limits.

For requirements, design, or contract reviews, conclude with `Ready`,
`Conditionally ready`, or `Not ready` for the stated document purpose,
identifying the requirements or decisions affected by unresolved questions. This
judgment does not certify implementation, runtime behavior, or visual quality.

For edits, briefly report the changed content, actual checks, and material gaps.
Avoid adding a separate report file unless the task or project requires one.
