# Research Guide

Use this guide for detailed candidate comparison, conflicting advice, an
evidence-record template, source starting points, or selection-testing
procedures. The [main workflow](../SKILL.md) owns research depth, provenance,
authorization, evidence status, reporting, and persistence requirements.

## Choose evidence that answers the question

Start from a concrete local uncertainty. A skill about database migrations
needs relevant migration implementations or tests as well as instruction
patterns. A trigger-only edit may need selection examples without a new domain
survey. Look for reusable mechanisms rather than matching names alone.

Evaluate candidates on these dimensions:

| Dimension | Inspect |
| --- | --- |
| Task fit | Similar inputs, outputs, failure modes, and user expectations |
| Primary evidence | The actual instructions, code, tests, or maintenance docs |
| Boundaries | Preconditions, exclusions, permissions, and failure handling |
| Verifiability | Examples or tests that expose the claimed behavior |
| Compatibility | Host capabilities, dependencies, and repository conventions |
| Maintenance | Relevant versions, visible changes, and known limitations |

A recent release is context, not proof that a particular mechanism works.
Forks, mirrors, and repeated implementations do not provide independent
corroboration.

## Resolve conflicting advice

For each conflict, compare the problem each source solves, its runtime and
audience, adoption costs, and the current repository's needs.

For example, an upstream creator may discourage extra README files to keep
agent context small, while the local repository uses a README for human
installation instructions. Keeping a human-facing README and a concise
`SKILL.md` can satisfy the local need without loading both into every task.
This is an adaptation justified by the local audience, not a requirement that
every skill have a README.

Similarly, descriptions can emphasize trigger conditions or include a brief
purpose. Choose wording for the host's discovery model and the local task.
Use nearby positive and negative requests to observe actual selection; a
preferred upstream style alone cannot establish that selection improved.

## Record evidence and decisions

Use this optional template when the evidence needs a structured record.

| Question | Source and location | Observed practice | Conditions | Decision and reason | Validation |
| --- | --- | --- | --- | --- | --- |
| Which requests should load the skill? | Inspected primary URL, file, and section | What that source actually does | Required host and task assumptions | Adopt, adapt, or reject; explain local fit | A relevant check and its actual status |

Replace the placeholder row with actual evidence and include the provenance
and claim-level status required by the main workflow. A search date cannot
establish a revision; inspection of one file cannot verify an entire project.

## Check selection and execution separately

For natural trigger checks, make the skill discoverable without explicitly
invoking it and inspect actual loading evidence. Use explicit invocation for
execution checks so a selection failure does not hide a workflow issue.
Synthetic sources can test the research procedure reproducibly, but do not
prove real search access or a named provider worked. Reuse the host's existing
check framework instead of introducing a new evaluation system by default.

## Starting points for skill mechanics

These sources informed the design questions above. Their branch links are
mutable. Inspect the relevant current or pinned file before relying on it in
a new task; this list is not evidence that a future task has read those files.
Select domain implementations separately when the question requires them.

- [Agent Skills specification][specification] and [best practices][practices]:
  inspect metadata, package structure, progressive loading, and context fit.
- [OpenAI skill-creator][openai]: compare concrete use cases, package resources,
  and validation guidance with the host repository's conventions.
- [Anthropic skill-creator][anthropic]: examine related-skill research, version
  comparisons, and description selection checks as separate concerns.
- [Superpowers writing-skills][superpowers]: examine observed failures and
  scenario checks; assess its testing requirements before transferring them.
- [Agent Skills description guidance][descriptions]: inspect natural selection
  checks and near-miss requests for the actual target host.
- [Skills Dojo][dojo]: compare selection and effectiveness as evaluation
  dimensions; this package does not depend on its evaluation tools.

[specification]: https://agentskills.io/specification
[practices]: https://github.com/agentskills/agentskills/blob/main/docs/skill-creation/best-practices.mdx
[openai]: https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md
[anthropic]: https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md
[superpowers]: https://github.com/obra/superpowers/blob/main/skills/writing-skills/SKILL.md
[descriptions]: https://github.com/agentskills/agentskills/blob/main/docs/skill-creation/optimizing-descriptions.mdx
[dojo]: https://github.com/brandonburrus/skills-dojo/blob/main/README.md
