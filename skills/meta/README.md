# Meta

Skills for maintaining skills and project instructions, reviewing project
readiness for agent work, configuring Codex, and finding open-source skill
references on request.

## Skills

- [Simplify Skill](simplify-skill/SKILL.md): trim redundant skill instructions
  and propose behavior-changing removals for the user to decide.
- [Codex Config](codex-config/SKILL.md): inspect, change, and verify Codex
  configuration against the target runtime and effective configuration layers.
- [Maintain Skills](maintain-skills/README.md): list, install, update, and remove
  standalone skills while preserving the requested scope and local edits.
- [Maintain AGENTS.md](maintain-agents-md/README.md): capture, review, trim, and
  revise durable project instructions.
- [Agent Ready](agent-ready/README.md): review how reliably agents can locate,
  change, run, and verify a project.
- [Find Skill References](find-skill-references/README.md): find and compare
  open-source practices when the user seeks references for a specific or
  planned skill.

## Package layout

Each child is an independent skill with its own `SKILL.md`, interface metadata,
and required resources. This collection has no `SKILL.md` of its own. Install
the selected leaf package, retaining its leaf name as the skill identifier.

The source paths for `maintain-skills`, `maintain-agents-md`, and `agent-ready`
are now under `skills/meta/`. The former `meta-skills` collection is named `meta`,
including the package now named `find-skill-references` (formerly
`research-skill-patterns`). The other skill identifiers are unchanged. Source
reorganization and renaming do not update existing installations or their
recorded sources.
