# Changelog

## Unreleased

Planned next minor release: `0.2.0`.

### Added

- `technical-docs` for creating, revising, reviewing, and consolidating project
  documentation, including comparisons with implementation and contracts.
- Synthetic documentation cases for scoped edits, review-only requests,
  unresolved decisions, consolidation, and implementation evidence.
- `maintain-skills` for standalone skill maintenance through the Vercel Skills
  CLI, with scope-aware installation, updates, removal, and result checks.
- Synthetic maintenance cases covering shared paths, unknown sources, local
  edits, read-only requests, and partial failures.
- Pinned Markdown linting and supported automatic fixes, with the same lint
  check in CI.
- `learn-from-session` for learning from the current conversation and improving
  user-maintained skill sources through an available `skill-creator`.
- Synthetic session-learning cases for evidence, authorization, and source
  scope.

### Changed

- `learn-from-session` now considers reusable operations and selects
  instructions, templates, or scripts based on their benefit and maintenance
  cost. Simple commands remain examples unless a helper adds meaningful value;
  script candidates carry execution and verification details to `skill-creator`.
- Clarified Skills CLI 1.7.0 source listing flags and failure results that can
  accompany a zero exit code, with a read-only inspection case.
- Disabled implicit invocation for `maintain-skills` in Codex; invoke it
  explicitly with `$maintain-skills`.
- Fixed Markdown heading, list, and code-fence styles across documents.
- Standardized README skill summaries, usage labels, and paragraph wrapping.
- Standardized example titles and case labels, skill-body wrapping, and
  changelog list spacing without changing behavior.
- Installation and update instructions now accept a selected skill name.
- The migrated skill's default prompt requests scoped implementation, matching
  its explicit-invocation contract, instead of always requesting approval
  first. Analysis-only requests remain read-only; implicit selection does not
  authorize writes. Implicit invocation remains enabled.

## 0.1.0 - 2026-10-02

### Added

- `maintain-agents-md` for capturing, reviewing, and revising durable project
  rules.
- Codex interface metadata with implicit invocation enabled.
- A synthetic example and behavioral cases for authorization, scope, and
  semantic preservation.
- Package validation and project-scoped setup instructions.
