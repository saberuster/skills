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
- [Setup Fern](setup-fern/SKILL.md): apply bundled custom agents, configuration
  and complete instructions to a Codex project.
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
- [Deep Search](deep-search/SKILL.md): explicitly invoke in Codex to plan
  source coverage, search with Exa and specialist tools, fill gaps with
  Parallel, and hand off cited evidence within bounded rounds and budgets.

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
provide separate evidence. Fern's pinned Codex and Claude Code
[discovery jobs](https://github.com/saberuster/skills/actions/runs/39066063246)
passed. Those results do not establish live setup or actual agent behavior.

Fern absorbs Implement's authorized implementation and delivery contract;
there is no separate Implement package or forwarding skill in this collection.
Fern is published and accessible from this repository. Existing installations
keep their current source until an explicit switch through `maintain-skills`;
use `$fern` after switching to the replacement.

`setup-fern` applies its bundled project resources through one Python installer.
It merges `.codex/config.toml`, copies the six custom agent TOMLs into
`.codex/agents/`, and adds the complete instruction asset to root `AGENTS.md`.
The same command works locally and in Codex Cloud. Skill installation is
separate. See its [usage and merge rules](setup-fern/references/installation.md)
and [synthetic cases](../../examples/setup-fern.md).
Source changes do not update existing installations. File application and
fresh-session loading of its Codex resources remain separate checks.
