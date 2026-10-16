# Review and verification

Inspect the requested scope. A local correction needs its relevant checks, not
a full audit. Apply the shared writing and maintenance rules in `SKILL.md`.

## Purpose and evidence

- Can readers understand, decide, or do what the document promises? Identify
  contradictions, omissions, or ambiguity that change their action or decision.
- Are requirements observable, design choices supported, and contracts clear
  about guarantees and limits? Keep open decisions distinct from defects and
  intended behavior distinct from implementation evidence.
- Do examples and claims match the relevant environment and version? Distinguish
  expected results, source inspection, executed checks, and historical reports.

## Reading and maintenance

When checking links, distinguish a broken target from unverified external access.

For substantial new or reorganized content, consider an independent reader check
using only the document and references its readers can access. Check whether
they can find the procedure, understand a boundary, or identify success. Use this
when comprehension is uncertain; it is not a required round or proof of technical
correctness.

## Compare documentation with implementation

Use only when asked to compare identified documents or accepted contracts with
an implementation. Ordinary writing or code explanation does not request this.

1. **Identify the comparison.** Establish the document, implementation revision,
   relevant local changes, and scope. Include environment and evidence timing
   when they affect the comparison; older deployment reports do not validate the
   current checkout.
2. **Trace the behavior.** Connect accepted requirements to the public entrypoint
   and relevant layers. A helper or isolated instance cannot establish the whole
   capability. Unresolved choices remain open decisions, not missing features.
3. **Report the differences.** Connect findings to the accepted basis and actual
   evidence. Distinguish source observations, executed checks, unavailable
   prerequisites, unknowns, and demonstrated violations. Use detail or a table
   proportional to the comparison; do not imply untested behavior was verified.

Do not change requirements or code to make them agree without authorization.
Follow-up tasks, when requested, should state the evidence, expected change,
preserved contracts, and observable acceptance. Comparison alone does not request
a roadmap.

## Findings and readiness

Lead with findings ordered by impact, each with its location, evidence,
consequence, and correction. If none are supported, say `No findings` and state
meaningful coverage limits.

Use `Ready`, `Conditionally ready`, or `Not ready` only when the user asks for a
readiness judgment or the project requires one. Tie it to the stated document
purpose and affected unresolved decisions; it does not certify implementation,
runtime behavior, or visual quality.

For edits, briefly report the result, actual checks, and material gaps. Create a
separate report file only when requested or required by the project.
