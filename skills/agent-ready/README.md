# Agent Ready

Review whether a new AI coding agent can locate, change, run, and verify a
project with limited context. Follow representative tasks through actual code
and runtime boundaries, then propose a few prioritized, evidence-backed
improvements. Works across technology stacks and writes reviews in the user's
language. See the [skill instructions](SKILL.md) for the workflow.

## Requirements and scope

This instruction-only skill needs read access to the selected project. Runtime
checks need the project's existing tools and an environment where their effects
are understood and authorized. Missing tools limit evidence; they do not alone
show an architecture defect. The skill does not install dependencies by default.

The default is review only. It does not edit the project, enforce a particular
architecture, or install itself. Recommendations identify the actual agent task,
minimum change, effort and migration risk, acceptance check, priority, and
independent evidence confidence. A simple project can need no changes.

## Installation and updates

Give your agent an explicit request using the shared
[installation and update protocol][installation]. Replace `<revision>` with an
existing release tag or full commit SHA containing this skill and
`<project-root>` with your project's absolute path. These prompts select Codex
project scope. For Claude Code, replace `Codex` with `Claude Code`; for user
scope, replace the project scope with `my Codex user scope` or
`my Claude Code user scope`.

**Install:**

```text
Install only agent-ready from https://github.com/saberuster/skills
at <revision> for Codex in project <project-root>. Follow the repository's
docs/installation.md protocol. Preserve existing skills and report the resolved
commit, destination, and checks performed.
```

**Update:**

```text
Update only the existing agent-ready installation in Codex project
<project-root> from https://github.com/saberuster/skills to <revision>.
Follow the repository's docs/installation.md protocol. Compare against its
recorded source revision and preserve local edits; ask me to resolve conflicts.
```

## Usage

In Codex, use `/skills` or type `$` to select the installed skill. In Claude
Code, use `/agent-ready` at the start of the request.

**Task-based review:**

```text
Use $agent-ready to review this prototype. Agents struggle to reproduce
checkout failures and change discount rules. Trace those tasks, preserve the
project, and recommend only improvements justified at this stage.
```

**Focused review:**

```text
/agent-ready Review whether two agents can independently reproduce and verify
save/load bugs in this game. Inspect runtime state as well as code isolation.
Do not edit files or install tools. State what requires a rendered playtest.
```

The [synthetic behavior cases][examples] cover simple projects, hidden coupling,
verification gaps, runtime isolation, and evidence boundaries. Static validation,
client discovery, synthetic agent trials, and real-project runtime evidence are
separate checks; none proves the others.

[Back to the skill catalog][catalog].

[installation]: https://github.com/saberuster/skills/blob/main/docs/installation.md
[examples]: https://github.com/saberuster/skills/blob/main/examples/agent-ready.md
[catalog]: https://github.com/saberuster/skills#available-skills
