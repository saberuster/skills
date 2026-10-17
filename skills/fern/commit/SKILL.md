---
name: commit
description: Draft or review Conventional Commit messages from actual changes, or create scoped Git commits when requested. Use for commit preparation and execution, not general Git maintenance or automatic commits after coding.
---

# Commit

Use Conventional Commits 1.0.0 with the fallback preferences below. Drafting and
review are read-only: do not stage, commit, or run mutating hooks. A clear commit
request authorizes scoped staging and the commit sequence without repeated
approval. Pushing, merging, amending, and rewriting commits need separate scope.

## Resolve conventions

Read applicable project instructions, contribution guidance, commitlint config
(including package.json), hooks, and a few recent messages. Explicit user choices
and project requirements take precedence over this skill's fallback preferences.
Use history for context, not to override configured rules. If the user's requested
format conflicts with an enforced rule, explain the specific conflict rather than
silently changing configuration or bypassing checks.

When the proposed commit involves gameplay, visual design, creative assets, or
design deliverables, read [Game and design projects](references/game-and-design.md)
for type selection, dependency completeness, compatibility, and relevant checks.

The standard syntax is:

```text
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

`feat` describes a feature and `fix` a bug fix. Scope and body are optional.
Separate the body and footer section with blank lines. Breaking changes can use
`!` before the colon, a `BREAKING CHANGE:` footer, or both. Other trailers follow
the standard token/separator form; include issue references only when supported
by the task. The standard does not mandate a complete type list, a header length,
or both breaking markers. Do not label these extra preferences as specification
requirements.

## Preference profile

These are editable fallback defaults, not a new commit format. Keep project
overrides in the project's existing instructions or commitlint configuration;
do not create another configuration system for this skill.

| Area | Default preference |
| --- | --- |
| Type | Use the common config-conventional set: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`. Choose by intent; use `chore` only when a more specific type does not fit. |
| Scope | Optional. Reuse an established component or package name when it adds useful context; omit it for a broad change. Do not invent an exhaustive scope registry. |
| Body | Omit for self-explanatory changes. Otherwise explain the reason, relevant behavior change, or tradeoff briefly; avoid a file inventory or command log. |
| Breaking change | Prefer both `!` and a `BREAKING CHANGE:` footer describing the incompatibility and migration. This is stricter than the standard; honor an explicit standard-only request. Never invent a migration path. |
| Before commit | Follow the validation and execution steps in [Prepare and commit](#prepare-and-commit). |

Use lowercase types and a concise action-oriented description without a final
period. Follow the requested or established message language. Use configured
length and case rules; without them, favor brevity rather than inventing a hard
limit. `style` means code formatting, not visual design changes. Tests accompanying
a fix belong with that fix; `test` is appropriate for a test-only change. Any type
can carry a breaking change.

## Prepare and commit

1. Establish the target repository and requested change boundary. Inspect status,
   staged and unstaged diffs, and relevant untracked files. For example, use
   `git status --short`, `git diff --cached`, and `git diff`. Base a proposed
   commit on its intended patch, not on every visible workspace change. With an
   exported diff only, state that repository and execution checks are
   unavailable.
2. By default, put each independent intent in a separate commit that can be
   validated and reverted as a unit. Put prerequisites first, keeping
   intermediate states usable. Reverting a prerequisite must account for its
   dependents, usually by reverting them first; do not promise arbitrary reverts
   or cherry-picks. Keep fixes with regression tests and required code, scenes,
   assets, and metadata.
   Keep tightly coupled work together when splitting breaks a state, and explain
   why. Use no file or line quota or arbitrary tiny splits.

   Preserve unrelated staged work: do not include it, silently unstage it, or
   stage a whole partially staged file. Resolve boundaries before committing;
   ask only if ownership or scope remains unclear.
3. Draft each message using the profile and actual compatibility impact. For
   message-only or review requests, return the message or findings here.
4. When committing is requested, process groups in order. For each commit, stage
   only its intended paths or hunks. Review `git diff --cached` and
   `git diff --cached --check`; refuse an accidental empty commit. Run required
   project checks and proportionate checks, reusing still-relevant results.
   Tests run against the working tree may not validate a different staged
   version: account for that difference without discarding unstaged work.
   Final-state checks alone do not establish that earlier commits pass. Report
   unavailable checks; do not claim success or commit past a required failure
   without explicit authorization.
5. Use the project's installed message checker if present. Do not install
   commitlint, hooks, or release tooling just to use this skill. A manual format
   check is not a commitlint execution. Commit with the existing hooks,
   identity, and signing; use a message file with actual newlines for multiline
   messages, keeping it outside the staged changes. A hook or signing failure
   blocks the commit; do not disable either. Inspect hook changes before
   restaging; do not retry blindly or amend without authorization.
6. Verify each resulting commit's message and contents and the remaining
   status. Report hashes, intents, and checks in commit order, plus remaining
   changes. If no commit was made, say whether the result is a draft or blocked.

## Sources

- [Conventional Commits 1.0.0][spec] defines the message syntax.
- [config-conventional][preset] supplies the common type vocabulary and lint
  defaults; the project's installed version and overrides determine actual rules.
- [commitlint rules][rules] include the optional
  `breaking-change-exclamation-mark` rule for requiring both breaking markers.
- [commitlint configuration][config] explains extending an existing preset.

[spec]: https://www.conventionalcommits.org/en/v1.0.0/
[preset]: https://github.com/conventional-changelog/commitlint/tree/master/%40commitlint/config-conventional
[rules]: https://commitlint.js.org/reference/rules.html
[config]: https://commitlint.js.org/reference/configuration.html
