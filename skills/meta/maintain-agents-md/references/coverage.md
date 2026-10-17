# Coverage and source discovery

Use this guide for comprehensive AGENTS.md reviews, completion requests, or new
files. Evaluate the project's actual needs; these are responsibilities to
inspect, not mandatory headings or a request to redesign the implementation.

## Establish coverage

Identify the target paths, effective instruction chain, and available evidence.
Inspect relevant README files, contribution guides, maintained architecture
decisions, build and test configuration, CI, and document or skill entrypoints.
A filename or heading alone does not establish coverage: follow its content
and links far enough to tell whether an agent can use the guidance. An
inaccessible source is unknown, not proof that a rule does not exist. Scale
the report to the project; a short summary can cover several responsibilities.

| Responsibility | Question and useful evidence |
| --- | --- |
| Project Overview | Can an agent identify the project's purpose and relevant entrypoints? Use the maintained README or product brief; omit background that does not affect work. |
| Repository Structure | Can an agent locate the module to change and its verification entrypoint? Check a concise responsibility map, source layout, and generated-file boundaries; avoid a full directory listing. |
| Architecture Guidelines | Are existing dependency, ownership, and compatibility obligations discoverable? Link maintained decisions or contracts; do not promote observed code patterns into mandatory policy. |
| Development Workflow | Are setup, implementation, and handoff steps available for the requested work? Follow contribution guidance and task scripts rather than inventing a branching or approval process. |
| Build and Validation | Are applicable checks reproducible, with prerequisites, working directory, parameters, and success criteria? Compare runbooks with scripts and CI; separate execution evidence from inspection. |
| Modification Boundaries | Are read-only, generated, protected, or externally managed paths and consequential operations identified where relevant? Use explicit project decisions and ownership records; do not invent restrictions. |
| Code Review and Completion Criteria | Can an agent tell which review, verification, compatibility, and documentation obligations define completion? Check contribution requirements, review guidance, and enforced checks, including scoped exceptions. |
| Documentation and Skills | Can an agent find the authoritative procedure or relevant skill when needed? Prefer a small task-oriented index with usable links and invocation conditions over copying instructions. |

## Resolve sources

- A valid link to stale guidance does not establish correctness: check that
  the destination and section exist and serve the claimed purpose.
- Distinguish a missing rule from a missing navigation link, and propose the
  smallest supported repair. Do not invent policies to fill this table.
- When sources disagree, report the concrete conflict; a newer timestamp or
  divergent script does not withdraw a normative rule.

## Report useful gaps

For a missing responsibility, identify the inspected scope, available evidence,
the decision or task that lacks guidance, and the proposed location or link.
Report coverage without treating document length or a complete set of headings
as success.
