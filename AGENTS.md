# Contributor and agent instructions

See [README.md](README.md) for setup, installation, usage, and release conventions.

## Maintain skills

- Edit skill sources in `skills/<name>/`. Keep `SKILL.md`, `agents/openai.yaml`,
  and any required resources consistent; keep packages self-contained. Add
  resources only when the skill needs them, not to fill a template.
- Preserve task scope, authorization boundaries, conditions, and exceptions.
  Explain intentional behavior changes and update the relevant synthetic cases
  in `examples/`. Reviewing or editing a skill does not mean performing its task.
- Keep public instructions and examples in English. Use ASCII text and LF line
  endings to match the repository's checks. Record user-visible changes in
  `CHANGELOG.md`; follow the README version policy.

## Validate changes

Use the isolated development environment and interpreter paths in the README.
Install the pinned `requirements-dev.txt`; use the same Ruff version as CI.
From the repository root, run these with that environment's Python:

```text
python -m ruff check .
python -m ruff format --check .
python -m unittest discover -s tests -v
```

Ruff rules live in `ruff.toml`; use `python -m ruff format .` to apply formatting.
The existing tests validate skill frontmatter and interface metadata, local
Markdown links, and text hygiene. They do not validate agent decisions. For
behavior changes, exercise relevant cases from `examples/` in an isolated
project and report actual outcomes and coverage. Distinguish local checks from
host discovery, behavior tests, and hosted CI results.

## Keep contributions public-safe

Use synthetic examples. Exclude credentials, private conversations, machine-local
paths, private repository links, and generated environments or caches. Include
third-party material only with verified redistribution rights and required
attribution; do not assume the root MIT license covers external material.
