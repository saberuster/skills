# Changelog

## Unreleased

Planned next minor release: `0.2.0`.

### Added

- `agent-ready` for read-only, task-based reviews of how reliably agents can
  locate, change, run, and verify a project, with a proportional eight-dimension
  rubric, actionable findings, and conditional game/engine guidance.
- Eight executable synthetic `agent-ready` cases for simplicity, coupling,
  sparse documentation, UI verification, environment limits, shared runtime
  state, justified non-changes, and untrusted review data.
- `gpt-image-prompting`, a shared six-section GPT Image prompt standard, with
  delivery requirements inside one copyable prompt and conditional guidance
  for styles, game assets, references, edits, lettering, and related outputs.
- `brief-to-image-prompt` and `image-to-prompt`, lightweight entries that use
  the core for preference-led brief refinement and standalone image-to-text
  prompting. Includes synthetic cases and explicit core dependency guidance.
- A provider-independent behavior trial helper with selected smoke cases,
  isolated fixtures, source and case hashes, before/after files, actual replies,
  and explicit evaluator assessments. Static tests exercise the helper without
  making model calls; live agent trials remain separate.
- `talk-it-through`, migrated from `saberuster/agent-skills`, for exploring
  alternatives and trade-offs while leaving consequential choices to the user.
  Includes its six synthetic acceptance cases and explicit Codex invocation
  policy.
- A generated README support table with emoji statuses for each skill and
  client, CI previews, and default-branch updates from matching discovery
  evidence.
- Continuous Codex and Claude Code skill discovery checks with isolated
  profiles, per-skill reports, pinned PR coverage, and weekly upstream checks.
  These initialize real clients without sending model prompts; behavioral
  acceptance and host-specific invocation policy remain separate.
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

- `maintain-agents-md` now checks comprehensive guidance coverage and executable
  command context, preserves concise navigation, and reports verification levels.
  Headings default to English unless the user specifies otherwise; body language
  follows the user or relevant repository documentation, with clarification when
  evidence is absent or conflicting. Added isolated behavioral cases for these
  contracts and existing maintenance boundaries.
- Claude discovery failures now retain exception types and execution stages,
  including explicit CLI-version and initialization timeout diagnostics.
- Local Markdown checks now parse links and images, including reference-style
  destinations and heading fragments, while ignoring code examples.
- Removed the installation protocol's requirement to copy the repository root
  license into each installed skill package.
- Moved `talk-it-through` acceptance cases into `examples/` and updated its
  evaluation links. Removed the obsolete pre-CI notice from the catalog.
- Condensed repeated guidance in the four skill entrypoints and grouped Skills
  CLI command examples without changing scope, authorization, or validation
  requirements. Each skill retains its installation guidance and resources.
- `maintain-skills` now distinguishes explicit local paths from remote
  repository shorthand without assuming grouped skills need extra discovery
  flags. Synthetic cases cover local source discovery and removals that
  complete or partially complete before an abnormal process exit.
- `maintain-skills` now allows direct removal of an explicitly authorized exact
  directory when verified CLI limitations prevent removal and no links or
  other-agent dependencies are involved. Removal checks distinguish independent
  same-name copies, preserve shared records, and report unresolved stale entries.
  Synthetic cases cover the fallback and its authorization and sharing limits.
- `technical-docs` now checks navigation from the intended delivery location
  when documents are moved, copied, or packaged, with a synthetic package-copy
  case and explicit limits for unverified external references.
- Moved skill-specific installation, update, and usage guidance into each
  skill's README. The repository README now provides navigation, discovery
  status, and development entrypoints, with shared protocols in `docs/`.
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
- `learn-from-session` now defaults to proposals without editing files,
  including explicit invocation and its default prompt. Applying suggestions
  or directly modifying skills requires an explicit user request; existing
  authorization needs no repeated approval. Implicit invocation remains enabled.

## 0.1.0 - 2026-10-02

### Added

- `maintain-agents-md` for capturing, reviewing, and revising durable project
  rules.
- Codex interface metadata with implicit invocation enabled.
- A synthetic example and behavioral cases for authorization, scope, and
  semantic preservation.
- Package validation and project-scoped setup instructions.
