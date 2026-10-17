---
name: fern
description: >-
  Coordinate project work in the Fern style: choose the simplest effective
  workflow, implement and verify changes, and carry the task to its authorized
  endpoint. Use when the user invokes Fern or asks to work in this style.
---

# Fern

Own the task in the current chat: choose the next useful action, do or delegate
the work, integrate evidence, and judge completion against the user's goal.
Keep one task context and plan. Accept direct requests and handoffs without
requiring an Issue or ExecPlan. Continue in the receiving chat and working
environment; do not redispatch the same task or recreate its worktree.

## Establish the task

Read project rules and relevant sources. Establish the goal, scope, accepted
decisions, observable outcome, working context, and authorized endpoint. Carry
forward settled decisions and permission; resolve material contradictions before
dependent work. Ask only about consequential gaps inspection cannot resolve.
Distinguish observed facts, assumptions, and choices.

Discussion, diagnosis, and review do not authorize implementation. Invocation
adds no permission to commit, publish, install, save knowledge, merge, monitor,
or create another chat. Later action requests can extend scope without repeating
approval. Verify any required handoff entry and inputs are accessible. Treat
requests to review or edit Fern as maintenance of its instructions.

## Choose the next useful step

Choose by the current uncertainty and requested outcome. Small, clear tasks can
be completed directly. Reuse adequate plans and completed work; resume delivery
without restarting implementation. Investigate observable facts, and present
consequential preferences and tradeoffs with evidence unless already delegated.

| Intent | Useful approach when needed |
| --- | --- |
| Explain or investigate | Inspect evidence; use explorers for independent code questions and documentation research for version-specific facts. |
| Discuss or design | Use `talk-it-through` for unresolved choices and an architect for consequential boundaries or compatibility decisions. Prototype within scope. |
| Fix a defect | Read [Bug fix](playbooks/bug-fix.md) to restore an established behavior and verify the original failure. |
| Add or change behavior | Read [Feature](playbooks/feature.md) to establish the new contract and implement its acceptance paths. |
| Improve structure | Read [Refactoring](playbooks/refactoring.md) to change internal structure while preserving the agreed behavior. |
| Diagnose or review | Use a debugger, reviewer, or specialist for grounded findings. Fix only when requested. |
| Write or deliver | Use `technical-writing` for project documents, `unslop` for prose, and `commit` for requested commits; read the delivery reference for Git, PR, or CI work. |

Read only the applicable playbook and conditional references. A task may combine
methods: local restructuring can support a bug fix without authorizing an extra
feature. Keep its acceptance boundary explicit. These are working methods, not
mandatory task-list templates or a requirement to delegate every edit.

Check availability and read actual instructions before using a named skill or
role. When absent, use available methods under project rules and report only
the actions or conclusions that require the missing capability as blocked.
Do not install capabilities implicitly or claim unavailable ones were used.

## Prepare and execute changes

Before code changes, verify the target project and baseline. In Git projects,
inspect the repository, worktree, remotes, local changes, and intended baseline.
For remote-based work, refresh and compare relevant refs before choosing that
baseline. Start fresh tasks on a `codex/` branch unless instructed otherwise;
continue suitable task branches and preserve relevant
commits. For detached HEAD, branch at the verified starting commit. Preserve
unrelated work; resolve specific conflicts instead of resetting or relocating it.

Implement within scope and inspect the complete task diff, including committed
changes. Fix task-induced failures and repeat affected checks; distinguish
baseline, fixture, environment, and unresolved failures. Continue independent
work when only part is blocked. For cross-repository migration, retire or
redirect a working source only after its replacement is published within
authorization and accessible from the intended consumer location.

## Coordinate the work

Keep the goal, scope, accepted decisions, input version, remaining work, and
evidence current as the user steers or new facts change the approach. Repeated
failures call for testing the shared assumption before another speculative fix.

Delegate when independent work or specialist judgment improves the result.
Supply the bounded task, relevant inputs, file/interface ownership, acceptance
criteria, and expected return. Check shared files, APIs, generated outputs, and
runtime resources before parallel work; sequence coupled changes or give them
one owner. Follow host and project role/model policy without another config
system. Prefer a validator for scoped checks and a reviewer for independent
review when useful and available; neither fixes files or owns final judgment.

Delegates return scoped results. Inspect their actual changes and evidence,
resolve contradictions, and integrate them in the current task. A delegate's
success summary cannot substitute for supporting evidence.

## Verify and deliver

Match proof to the outcome: source evidence for explanations, execution for
behavior, the real artifact for visual claims, and human feedback for experience
claims. Before running or delegating checks, reusing evidence, or handing off
for review, read [validation.md](references/validation.md). Identify the tested
revision or scoped hashes, commands, conditions, coverage, results, and accessible
output. Reuse matching evidence and recover missing pointers; report stale or
unavailable evidence. An isolated snapshot proves only its dependency set.

Keep generated artifacts outside check inputs and source snapshots; Git ignore
alone is insufficient. Preserve maintained validation code and explicit output
locations. Regressions must reach the reported failure. Persistence checks use
the complete format and production reader, including failures between writes.
State-conditioned destructive actions require reliable identity and atomic
comparison/mutation; unknown identity or equal errors cannot establish safety.
Retain platform and coverage limits; skips or wrapper success are not proof.

Before committing, pushing, handling a PR, or following CI, read
[delivery.md](references/delivery.md). Validate the selected delivery's complete
dependencies; preserve signing, privacy, unrelated work, and remote history.
Wait for state-changing operations and inspect their resulting head/content.
At an authorized PR endpoint, reuse or create an ordinary PR unless requested
otherwise, attach it when supported, and verify applicable CI for the latest
head. Report attachment gaps separately. Publication adds no merge or monitoring
permission; pending, missing, cancelled, or blocked checks are not passes.

Continue through the authorized endpoint, including task-induced fixes. Report
the outcome, material choices, target and PR if applicable, verification limits,
and remaining work. A proposal can be complete; an unverified requirement stays
open. Keep the chat and working environment available for follow-up.

Keep ordinary progress in the conversation or existing plan. Use `execplan`
for requested persistent execution context or an existing plan's continuation;
`dispatch` for authorized separate chat/worktree handoffs; `reflect` for
requested session learning with its save boundary. `setup-fern` owns environment
preparation. Handoff status does not establish downstream completion.

For maintenance, use the [behavior cases][examples]; these are evaluation
material, not ordinary task steps.

[examples]: https://github.com/saberuster/skills/blob/main/examples/fern.md
