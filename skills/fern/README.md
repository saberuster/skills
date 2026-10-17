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

## Status

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
`unslop` handles focused language editing.
Existing installations are unchanged; select the new source path and name
when installing or migrating a skill. Discovery under `commit` and `reflect`
has not been verified. Plugin packaging and installation are not configured yet.
