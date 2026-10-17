# fern

A personal workflow plugin project inspired by pstack.

## Inspiration

The name comes from Fern in the anime *Frieren: Beyond Journey's End*.
Her approach to winning with basic offensive magic captures the idea behind
this project: master the fundamentals and use them well.

## Goal

Accomplish complex tasks using the simplest effective methods, just like Fern.
Keep workflows direct, make every step useful, and add complexity only when
the task requires it.

## Skills

- [Fern](fern/SKILL.md): choose the simplest effective workflow, coordinate
  available skills and agents, implement and validate changes, and complete
  authorized Git, PR, and CI delivery in the current chat.
- [Setup Fern](setup-fern/SKILL.md): align a curated Codex environment with
  the mandatory Fern and meta collections, selected external skills, custom
  agents, configuration, and subagent instructions.
- [Commit](commit/README.md): draft or review Conventional Commit messages and
  create scoped Git commits when requested.
- [Technical Writing](technical-writing/SKILL.md): create, revise,
  review, and consolidate technical project documentation.
- [Unslop](unslop/SKILL.md): revise or review existing prose while preserving
  meaning, necessary qualifications, and the writer's voice.
- [reflect](reflect/README.md): extract durable knowledge from the current
  session, reconcile it with existing sources, and propose or apply scoped
  updates according to the user's authorization.
- [Talk It Through](talk-it-through/README.md): develop ideas, compare
  alternatives, and clarify trade-offs through focused discussion while the user
  keeps consequential choices.

## Status

`fern` is the explicitly invoked working entrypoint. It selects methods and
retains task responsibility, implementation, validation, and delivery in the
current main agent. Its [bug fix](fern/playbooks/bug-fix.md),
[feature](fern/playbooks/feature.md), and
[refactoring](fern/playbooks/refactoring.md) playbooks describe different
change goals and evidence. Shared validation and delivery rules live in
references. Specialist skills and agents remain independently usable. Missing
optional capabilities do not start environment installation. `setup-fern` owns
that separate preparation lifecycle.

See the [Fern cases](../../examples/fern.md) for behavioral expectations.
Static checks, isolated agent trials, client discovery, and live installation
provide separate evidence. Fern client discovery remains unverified.

Fern absorbs Implement's authorized implementation and delivery contract;
there is no separate Implement package or forwarding skill in this collection.
The old working source in `saberuster/agent-skills` is retained until Fern is
published and consumer-accessible. Existing installations keep their current
source until an explicit switch through `maintain-skills`; use `$fern` after
switching to the replacement.

`setup-fern` maintains the personal environment baseline. Its complete package
includes the six custom agent TOMLs formerly stored in the repository's root
`agents/` directory. Its [baseline](setup-fern/references/baseline.md) selects
the two mandatory collections, `gh`, and host capability checks; other
collections remain optional. See its
[installation contract](setup-fern/references/codex-installation.md) and
[synthetic cases](../../examples/setup-fern.md) before exercising setup.
Source changes do not update existing installations. Live setup and
fresh-session loading of its Codex resources remain separate checks.

Skills are maintained individually in this collection. `commit` was migrated
from `git-commit`, `technical-writing` from `technical-docs`, and `reflect`
from `learn-from-session`;
`unslop` handles focused language editing. `talk-it-through` was moved from
the `thinking` collection.
Existing installations are unchanged; select the new source path and name
when installing or migrating a skill. Discovery under `commit` and `reflect`
and from the relocated `talk-it-through` source has not been verified. Plugin
packaging and installation are not configured yet.
