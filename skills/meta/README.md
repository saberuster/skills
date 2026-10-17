# Meta

Skills for maintaining skills and project instructions, reviewing project
readiness for agent work, and improving skill workflows through research.

## Skills

- [Maintain Skills](maintain-skills/README.md): list, install, update, and remove
  standalone skills while preserving the requested scope and local edits.
- [Maintain AGENTS.md](maintain-agents-md/README.md): capture, review, trim, and
  revise durable project instructions.
- [Agent Ready](agent-ready/README.md): review how reliably agents can locate,
  change, run, and verify a project.
- [Research Skill Patterns](research-skill-patterns/README.md): inspect relevant
  open-source examples and explain what to adopt, adapt, or reject when creating,
  editing, or reviewing a skill.

## Package layout

Each child is an independent skill with its own `SKILL.md`, interface metadata,
and required resources. This collection has no `SKILL.md` of its own. Install
the selected leaf package, retaining its leaf name as the skill identifier.

The source paths for `maintain-skills`, `maintain-agents-md`, and `agent-ready`
are now under `skills/meta/`. The former `meta-skills` collection is named `meta`,
including its existing `research-skill-patterns` package. Skill identifiers are
unchanged. This source reorganization does not update existing installations or
their recorded sources.
