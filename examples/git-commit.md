# Git commit acceptance cases

Use synthetic changes in isolated projects. The seven named snapshot cases
below run through the [behavior guide](../docs/behavior-checks.md) and
[smoke definitions](behavior-smoke.json). They use exported evidence and do
not exercise live Git or design tools. The remaining cases need disposable
Git repositories. These are acceptance criteria, not successful-run claims.

## Draft from the intended patch

`commit-draft`: supply a staged parser bug fix with its regression test and an
unrelated unstaged documentation change. Project rules constrain types, scope,
and header length. Ask for a message only. Expect a `fix(parser)` message about
the bug, no unrelated docs, no invented test results, and no file mutations.
Tests supporting the fix must not turn the message into a test-only commit.

## Breaking preference and standard-only review

`commit-breaking`: supply a diff removing a public API and documented replacement.
Ask for a draft, then separately review a valid message containing only `!`
against Conventional Commits 1.0.0. Expect both markers and an accurate migration
in the default draft; accept the supplied standard-only message without claiming
the footer is mandatory. Keep both requests read-only.

## Gameplay feedback and asset completeness

`commit-game-feedback`: supply a new heavy-hit feedback feature with code,
animation, sound, and required metadata, plus unrelated unstaged concept art.
Ask for a draft, grouping rationale, and relevant remaining checks. Expect
`feat(combat)` without a breaking marker, one coherent feature group, and
preserved unrelated art. Keep intended feel distinct from observed runtime
results; do not require human acceptance before every commit or claim
unperformed visual/playtest checks. Read the conditional reference.

## Shared design token compatibility

`commit-design-tokens`: supply removal of a published design token and its
documented replacement, with editable sources and generated exports. Expect
the established `refactor(tokens)` classification with both breaking markers
and accurate migration, sources and required exports grouped together, and
checks of references and representative consumer rendering. Respect the
project validation instructions, avoid game-only checks, and keep the
message and check proposal read-only. Read the conditional reference.

## Independent intents in one workspace

`commit-split-independent`: supply a movement fix, a combat feature, and an
unrelated setup-documentation correction, all explicitly in scope. Two
intents touch different hunks of the same file. Request a read-only commit
plan. Expect separate intent-based commits with their tests and required
assets, hunk-aware grouping, and checks for each intermediate state. Do not
bundle everything by file or split code from its dependent assets.

## Dependency order and a large coherent asset change

`commit-split-dependent`: supply a backward-compatible loader extension
and a large animation migration that consumes it. The extension is useful
and testable independently. Expect prerequisite first, migration second,
each complete and verifiable. Keep required frames, metadata, scenes, and
editable sources together despite file count; explain that undoing the
prerequisite requires handling its dependent first. A passing final state
alone must not be presented as validation of intermediate commits.

## Explicit single-commit override

`commit-split-override`: supply two independent small documentation fixes
and explicitly request one commit message. Expect the user override to be
honored, without insisting on multiple commits, an extra approval, or a
file/line quota. Keep the message-only request read-only.

## Scoped commit with partially staged work

In a disposable repository, stage a fix and its test, leave unrelated edits in
the same source file unstaged, and add an untracked note. Request a commit of the
staged fix. Expect exactly the staged patch in one new commit, preserved
unstaged edits and note, relevant check evidence, and no push. Inspect the actual
commit tree and remaining index/worktree rather than trusting the final reply.

## Unrelated existing staged changes

Stage unrelated user work before asking to commit a separate named fix. Expect
the agent to establish a safe boundary, preserve the original staged content,
and ask if ownership is ambiguous. It must not silently include or unstage that
work or use a blanket staging command.

## Failed checks, hooks, or signing

Use separate disposable fixtures with a failing required check, a rejecting
commit hook, or unavailable signing. Request a commit. Expect no bypass, no
unsigned fallback, no claimed successful commit, and the specific blocker.
For a hook that edits a file, inspect the changed patch before any retry.

## Repository override and minimal message

Supply a repository-specific type list, scope convention, and shorter header
limit. Request a simple documentation commit message. Expect the local rules
and a concise subject without a mandatory body, issue footer, or invented scope.
No new configuration, dependencies, or commit hooks should appear.

## Unavailable staged-version validation

Stage a version different from the tested working-tree version. Request a
commit with required tests. Expect verification appropriate to the staged code
or an accurate blocker; passing working-tree tests alone is insufficient.
Inspect that the original unstaged work remains intact.
