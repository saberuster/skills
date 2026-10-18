# Contributor and agent instructions

See [README.md](README.md) for setup, installation, usage, and release
conventions.

## Maintain skills

- Edit skill sources at their cataloged path: `skills/<name>/` or
  `skills/<collection>/<name>/`. Keep `SKILL.md`, `agents/openai.yaml`,
  and any required resources consistent; keep packages self-contained. Add
  resources only when the skill needs them, not to fill a template.
- Place general skills for maintaining skills or agents in `skills/meta/`.
  The collection covers their instructions, configuration, lifecycle, review,
  and improvement; each leaf remains an independent package.
  The personal Fern environment composition entrypoint and its supporting
  Codex resources belong in `skills/fern/setup-fern/`.
- Maintain the Codex marketplace in `.agents/plugins/marketplace.json` and
  the Fern plugin manifest in `skills/fern/.codex-plugin/plugin.json`. Keep its
  explicit skill list aligned with the Fern leaf packages; do not copy or move
  those sources merely to package the plugin. Follow `docs/plugins.md` for
  plugin versions and validation.
- When the user seeks open-source references for a specific or planned skill,
  apply [find-skill-references](skills/meta/find-skill-references/SKILL.md).
  Ordinary skill creation, editing, review, or explanation does not require
  research or prior research evidence. Share one research pass across
  collaborating workflows when research is requested.
- Preserve task scope, authorization boundaries, conditions, and exceptions.
  Explain intentional behavior changes and update the relevant synthetic cases
  in `examples/`. Reviewing or editing a skill does not mean performing its
  task.
- Keep public instructions and examples in English. Use ASCII text and LF line
  endings to match the repository's checks. Record user-visible changes in
  `CHANGELOG.md`; follow the README version policy.

## Validate changes

Use the repository-wide [validation layers](docs/validation.md): deterministic
PR checks, affected runtime/agent checks and full scheduled/manual/release
checks. On a user machine, use `scripts/run_validation.py` through Docker;
repository automation uses the checked-in CI workflows. Inspect the affected
plan and select checks for changed scripts, skill packages and shared resources.
Keep skills without executable cases and host-only procedures as explicit gaps.
A no-model run must report planned agent cases as not run; skipped and
unrequested checks do not establish complete layer coverage.

Actual behavior changes require relevant isolated agent trials and retained
replies, actions, file outcomes and assessments. Use the
[behavior check guide](docs/behavior-checks.md) for special case boundaries and
manual procedures. Synthetic replies in harness tests do not establish agent
behavior. Keep package checks, public-snapshot installation, client discovery,
model outcomes, real engines and human acceptance as separate evidence.

For focused implementation debugging, use the isolated development environment
and pinned dependencies in the README. Ruff rules live in `ruff.toml`;
Markdown rules live in `.markdownlint-cli2.jsonc`. Supported lint fixes do not
guarantee complete automatic formatting. Direct unittest discovery may skip
unavailable engine or platform paths; inspect and report them explicitly.
Changing validation scripts, fixtures, test selection or prerequisites requires
updating their layer mapping, affected checks and relevant CI/documentation.

## Keep contributions public-safe

Use synthetic examples. Exclude credentials, private conversations,
machine-local paths, private repository links, and generated environments or
caches. Include third-party material only with verified redistribution rights
and required attribution; do not assume the root MIT license covers external
material.
