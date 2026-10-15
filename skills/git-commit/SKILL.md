---
name: git-commit
description: Draft or review Conventional Commit messages from actual changes, or create scoped Git commits when requested. Use for commit preparation and execution, not general Git maintenance or automatic commits after coding.
---

# Git Commit

Use Conventional Commits 1.0.0 with the small preference profile below. Drafting
or reviewing a message is read-only. A request to commit authorizes the necessary
scoped staging and commit; do not ask again when that authorization is clear.
Pushing, merging, and rewriting existing commits need their own task scope.

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
Apply it within the same task scope; message-only requests remain read-only.

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
| Before commit | Inspect the exact staged patch, run required project checks and relevant targeted checks, and use existing message validation when available. Preserve hooks and configured signing. |

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
2. Identify independent intents within the authorized scope. By default, split
   them into separate commits that can each be validated and reverted as a
   logical unit. Order dependencies with prerequisites first, keeping every
   intermediate state usable. Reverting a prerequisite must account for later
   dependents, usually by reverting them first; do not promise arbitrary reverts
   or cherry-picks. Keep a fix with its regression test and keep required code,
   scenes, assets, and metadata together. If splitting tightly coupled work
   would
   leave an unusable state, keep it together and briefly explain why. Apply no
   hard file or line count limit, and avoid arbitrary tiny splits. When
   committing is authorized, carry out the sequence without approval for each
   commit. If existing staged work is unrelated, preserve it and resolve the
   commit boundary before committing. Do not sweep it in, unstage it silently,
   or stage a whole partially staged file. Ask only when ownership or the
   intended boundary cannot
   be established.
3. Draft each message using the profile and actual compatibility impact. For a
   message-only or review request, return the message or findings here without
   staging, committing, or running mutating hooks. Accept valid standard-only
   breaking syntax even if it differs from the fallback preference.
4. When committing is requested, process groups in order. For each commit, stage
   only its intended paths or hunks. Review `git diff --cached` and
   `git diff --cached --check`; refuse an accidental empty commit. Run required
   project checks and proportionate checks, reusing still-relevant results.
   Tests run against the working tree may not validate a different staged
   version: account for that difference without discarding unstaged work.
   Final-state checks alone do not establish that earlier commits pass. Report
   unavailable checks; do not claim
   success or commit past a required failure without explicit authorization.
5. Use the project's installed message checker if present. Do not install
   commitlint, hooks, or release tooling just to use this skill. A manual format
   check is not a commitlint execution. Commit with the existing hooks,
   identity,
   and signing; use a message file with actual newlines for multiline messages,
   keeping it outside the staged changes. A hook or signing failure is a
   blocker,
   not permission to disable it. If a hook changes files, inspect those changes
   before restaging; do not retry blindly or amend without authorization.
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
