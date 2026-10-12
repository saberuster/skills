# Talk It Through

Explore ideas, designs, plans, and architecture through focused conversation.
Develop alternatives, explain trade-offs, and work through the questions that
matter while the user keeps consequential choices. See the
[skill instructions](SKILL.md) for the complete workflow.

## Requirements and scope

This instruction-only skill needs the conversation and relevant context.
Factual checks use available tools within the authorized scope. Discussion
notes stay in the conversation unless the user asks to save them; discussion
alone does not authorize implementation or external changes.

Codex metadata requires explicit invocation. Claude Code does not apply
`agents/openai.yaml`, so that setting does not establish invocation-policy
parity between clients. Client discovery and conversation behavior require
separate validation.

## Installation and updates

Give your agent an explicit request using the shared
[installation and update protocol][installation]. Replace
`<revision>` with an existing release tag or full commit SHA containing this
skill, and `<project-root>` with your project's absolute path. These prompts
select Codex project scope. For Claude Code, replace `Codex` with
`Claude Code`; for a user-wide installation, replace the project scope with
`my Codex user scope` or `my Claude Code user scope`.

**Install:**

```text
Install only talk-it-through from https://github.com/saberuster/skills
at <revision> for Codex in project <project-root>. Follow the repository's
docs/installation.md protocol. Preserve existing skills and report the resolved
commit, destination, and checks performed.
```

**Update:**

```text
Update only the existing talk-it-through installation in Codex project
<project-root> from https://github.com/saberuster/skills to <revision>.
Follow the repository's docs/installation.md protocol. Compare against its
recorded source revision and preserve local edits; ask me to resolve conflicts.
```

## Usage

Explicitly select the skill in your client and describe the idea or question
you want to explore. For example, in Codex:

```text
Use $talk-it-through to explore how a museum visit could feel like a detective
story. I have not chosen a direction yet, and I do not want visitors to feel
tested. Help me think through the possibilities before creating anything.
```

For Claude Code:

```text
/talk-it-through Help me explore the trade-offs in offline inventory updates
before we implement anything. I want to make the key business decisions.
```

Accepting one recommendation advances the discussion to the remaining material
questions. Ask to wrap up or defer when you want a stopping point.

The bundled [acceptance cases](evals/cases.md) cover creative exploration,
architecture trade-offs, evidence gaps, changed goals, continued discussion,
and explicit closure. They describe expected behavior, not successful runs.

[Back to the skill catalog][catalog].

[installation]: https://github.com/saberuster/skills/blob/main/docs/installation.md
[catalog]: https://github.com/saberuster/skills#available-skills
