# Meta Skills

Skills for maintaining skills and agents: their instructions, configuration,
lifecycle, review, and continuous improvement. Classify by what the skill
maintains; an ordinary task performed by an agent does not belong here merely
because an agent performs it.

## Skills

- [Research Skill Patterns](research-skill-patterns/README.md): inspect relevant
  open-source examples and explain what to adopt, adapt, or reject when creating,
  editing, or reviewing a skill.

## Package layout

Each child is an independent skill with its own `SKILL.md`, interface metadata,
and required resources. This collection has no `SKILL.md` of its own. Install
the selected leaf package, retaining its leaf name as the skill identifier.

Existing skills elsewhere in the repository keep their current source paths.
The new collection does not migrate installations or change recorded sources.
