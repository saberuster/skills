# Research Guide

Read this guide when selecting sources, comparing conflicting practices, or
recording evidence. Use it with the [main workflow](../SKILL.md); it does not
start another research pass.

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

No popularity metric proves these properties. A recent release is useful
context, not proof that the particular mechanism works. A related project can
be informative even when its task or runtime differs, provided those limits
remain explicit.

Search collections can reveal candidates. Inspect original files before using
a candidate as support. Compare independent upstreams where useful; forks,
mirrors, or several files repeating one implementation do not provide
independent corroboration. If only one relevant source is available, report
that limit rather than adding unrelated citations.

## Resolve conflicting advice

For each conflict, compare the problem each source solves, its runtime and
audience, the cost of adopting its rule, and the current repository's needs.
Follow applicable user and repository requirements. Explain why a difference
matters; do not silently promote an upstream convention into a universal rule.

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

Use a compact table or equivalent notes. Preserve the connection between the
question and the decision; a bibliography alone is insufficient.

| Question | Source and location | Observed practice | Conditions | Decision and reason | Validation |
| --- | --- | --- | --- | --- | --- |
| Which requests should load the skill? | Inspected primary URL, file, and section | What that source actually does | Required host and task assumptions | Adopt, adapt, or reject; explain local fit | A relevant check and its actual status |

Replace the placeholder row with actual evidence. Record the read date and a
commit permalink when available; otherwise identify the mutable branch URL.
Never infer a revision from a search date. Mark each claim's evidence:

- **Verified:** the cited source location was inspected and supports that claim.
  State separately whether any runtime behavior was tested.
- **Partial:** only part of the claim was inspected or a material assumption
  remains unresolved; identify the exact limit.
- **Unavailable:** the needed source could not be inspected; give the reason.

Do not label a whole project verified because one file was read. Distinguish
an author's success claim from visible implementation and observed execution.
Name important patterns rejected after comparison, with a short reason.

For natural trigger checks, make the skill discoverable without explicitly
invoking it and inspect actual loading evidence. Use explicit invocation for
execution checks so a selection failure does not hide a workflow issue.
Synthetic sources can test the research procedure reproducibly, but do not
prove real search access or a named provider worked. Reuse the host's existing
check framework instead of introducing a new evaluation system by default.

Keep raw search output and full execution traces outside the skill package.
Persist only knowledge future users need, when writes are authorized. Links
and original summaries do not grant permission to redistribute upstream files;
verify the relevant license and attribution before copying material.

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
