# Changelog

## Unreleased

Planned next minor release: `0.2.0`.

### Added

- `codex-config` under `skills/meta/` with a concise entrypoint for inspecting,
  changing, and verifying Codex configuration against the target runtime,
  configuration layers, and enforced requirements. Fern retains baseline
  ownership and receipts while routing general configuration diagnosis to
  this independent skill.
- Repository-wide native Windows regressions on every PR/push and full run,
  plus manual dispatch. Automatically includes new non-engine test modules,
  requires junction/symlink execution, rejects unexpected skips, and records
  exact POSIX/Linux exclusions with test and environment evidence.
- Repository-wide validation layers with a unified local Docker launcher,
  deterministic PR checks, affected runtime and agent checks, and full
  scheduled/manual/release coverage. Includes every existing test module,
  client discovery, public-snapshot installation, real background Blender
  integration and eligible synthetic agent cases across skill collections.
  Reports missing prerequisites, skipped paths, unrequested model runs and
  manual coverage gaps separately; retains the README discovery table.
- Docker-based Setup Fern validation with a host standard-library launcher,
  isolated checks, real scripted Skills CLI installation and Codex discovery,
  and optional actual worker/evaluator model sessions for eleven setup cases.
  Retains failure evidence and adds a real Linux permission-denial/retry case.
  The repository-wide runtime/full workflows select these checks alongside
  other collections, with explicit model selection and credentials for agent
  behavior runs.
  These entrypoints do not establish native role loading, Windows junction
  migration, live interruption recovery, or a hosted CI pass.
- `fern` as an explicitly invoked entry for selecting workflows, coordinating
  available skills and agents, implementing changes, and completing the user's
  authorized task in the current main agent. It absorbs the former Implement
  procedure with bug fix, feature, and refactoring playbooks and shared
  validation and delivery references. Preserves evidence, authorization,
  signing, PR, and latest-head CI contracts, including scanned output roots.
  Fern is published and accessible from this repository; installed copies need
  an explicit switch through `maintain-skills`. Its pinned Codex and Claude Code
  [discovery jobs](https://github.com/saberuster/skills/actions/runs/39066063246)
  passed; live setup and actual agent behavior require separate checks.
- Synthetic Fern workflow and delivery cases, including ten selected smoke
  fixtures for scope, steering, stale evidence, coupled work, evidence reuse,
  pending Git operations, and actual bug fix, feature, and refactoring work.
  Former Implement narrative cases are retained under Fern. Actual behavior
  trials and client discovery remain separate from these definitions.
- Two offline `setup-fern` behavior cases for mixed agent/config ownership and
  recovery from an already-written file with a stale receipt. Include scoped
  restoration that preserves later edits, exact backups and per-unit records.
  Preconstructed interruption artifacts do not prove live crash recovery,
  skill installation or host loading; actual trial outcomes remain separate.
- The `godot` collection, migrated from `saberuster/agent-skills`: the standalone
  `setup-godot-skills` package and all five former `godot-dev` plugin skills,
  including metadata, references, build scripts, and Godot helper regressions.
  Skill names, workflows, and the setup skill's curated selection are preserved.
  Packages now install individually; existing installed copies are unchanged.
  Client discovery from these sources and real Godot execution remain unverified.
- The `blender` collection, migrated from `saberuster/agent-skills` with
  `blender-low-poly`, `character-rig`, and `reference-scene`, their metadata,
  references, scripts, component regressions, and background Blender tests.
  Skill names and workflows are preserved; package text and Python formatting
  follow this repository's conventions. Unreal transfer tests remain with their
  plugin in `agent-skills`. Existing installations are unchanged, and client
  discovery from these relocated sources remains unverified.
- `setup-fern` for the curated personal Codex environment: directory-selected
  Fern and meta skills, optional project collections, branch-following `gh`,
  and host checks for `skill-creator` and `openai-docs`. Includes selected
  config values, subagent scheduling instructions, conflict-aware resource
  application, and synthetic acceptance cases. Skill installation reuses
  `maintain-skills`; source maintenance does not apply changes to the host.
- Six standalone Codex custom agents copied from `saberuster/agent-skills`
  and relocated from root `agents/` into
  `skills/fern/setup-fern/assets/codex/agents/`: `architect`, `debugger`,
  `docs_researcher`, `reviewer`, `validator`, and `visual_reviewer`. Role
  definitions are preserved and travel with the complete Fern setup package.
- `unslop` in `skills/fern` for focused prose revision and review, preserving
  meaning, claim strength, exact content, and the writer's voice. Includes
  contextual patterns, counterexamples, source rationale, and synthetic behavior
  cases for English, Chinese, unchanged good text, and editing boundaries.
- The `meta` collection for skill maintenance, project instructions, agent
  readiness reviews, and skill research. `find-skill-references` finds and
  compares open-source practices when the user seeks references for a specific
  or planned skill. Includes a scoped repository entry rule and synthetic
  behavior cases.
- Shared package discovery for standalone skills and skills grouped in
  collections, used by client probes, behavior trials, and package checks.
  Catalog links fall back to `SKILL.md` when a package has no README.
- An initial `fern` README recording the personal workflow plugin project's
  inspiration from pstack and Fern, and its goal of accomplishing complex tasks
  with the simplest effective methods.
- Moved `git-commit` into `skills/fern/commit` and renamed it to `commit`
  (Commit), preserving its commit workflow and game/design guidance. Updated
  metadata, catalog links, usage, and behavioral cases. Existing installations
  are unchanged; client discovery under the new name remains unverified.
- Moved `technical-docs` into `skills/fern/technical-writing` and renamed
  it to `technical-writing` (Technical Writing), preserving its documentation
  workflow and supporting references. Updated usage, behavioral cases, and
  source discovery for the nested location. Existing installations are unchanged.
- Removed the `technical-writing` README; its catalog entries now link directly
  to `SKILL.md`. Catalog generation uses `SKILL.md` for packages without a README.
- Simplified `technical-writing` into one short workflow with document patterns
  and review details loaded as needed. Outlines now depend on unclear scope or
  structure, readiness labels on an explicit request or project requirement,
  and implementation comparisons use proportionate evidence reporting.
- `git-commit` for Conventional Commits 1.0.0 message drafting, review, and
  authorized scoped commits, with five fallback preferences, existing lint
  integration, and synthetic cases for format and execution boundaries. Defaults
  to complete commits per independent intent, ordered by dependency and checked
  per commit, without hard file or line count limits.
  Includes optional game and design guidance for asset completeness,
  compatibility, experience claims, and proportionate checks.

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

- `setup-fern` distinguishes the target chat runtime from a terminal CLI when
  diagnosing an unavailable plan tool, and checks runtime-specific configuration
  evidence before inferring support from a feature list or online schema.
- `setup-fern` now enables native Codex task progress with
  `tools.update_plan.enabled = true` in its maintained config fragment.
  Resource merges and receipts include this key while preserving unrelated
  tool configuration and existing per-key conflict handling.
- Validation entrypoints distinguish direct-script and package imports,
  including environments with an unrelated installed `scripts` namespace.
  The unittest child uses module execution to retain the repository import
  root; subprocess regressions cover both failures without global `PYTHONPATH`.
- Defined the exact byte range for Fern instruction receipt hashes, excluding
  the line ending after the end marker. Recognize existing receipts that
  included one immediately following LF or CRLF without normalizing internal
  edits or rewriting receipts during read-only checks. Added fresh-session
  compatibility cases alongside the existing same-session repeat case.
- `setup-fern` now carries the complete personal user instruction baseline:
  initiative, instruction precedence, writing style, subagent delegation,
  built-in explorer model selection (`gpt-6-luna`, `high`), and testing rules.
  Fresh environments receive the full rules in their user instruction file;
  existing environments preserve personal edits and migrate the former
  subagent-only block after checking ownership and overlapping rules.
- Clarified optional Fern custom-agent loading checks using native role spawns,
  correlated parent and child records, and actual instructions and settings.
  Added synthetic cases separating loading from blocked task probes and
  unavailable trace evidence, without claiming new host validation.
- `setup-fern` now requires explicit invocation in Codex. Disable implicit
  selection through its invocation policy while retaining `$setup-fern` use.
- Require each verified `find-skill-references` claim to match supporting content
  actually read from its cited primary file in the current task. Label unread
  citations as unverified and cached inspections as prior evidence; add a paired
  source-access regression case.
- Simplified Fern's `architect`, `debugger`, `docs_researcher`, and
  `visual_reviewer` instructions and replaced fixed report templates with
  task-sized handoffs. Preserved role boundaries and evidence requirements,
  including decision status, diagnostic confidence, versioned sources, and
  visual finding locations. Clarified diagnostic artifact isolation and exit
  evidence, and added paired behavior cases for all four roles. Model settings
  are unchanged.
- Clarified behavior-case selection for constraints that could block useful
  work: cover both a triggering case and a nearby case that should remain allowed.
- Simplified Fern's `reviewer` and `validator` developer instructions while
  preserving role boundaries, evidence requirements, validation statuses, and
  failure classifications. Replaced fixed report sections and global
  final-report blocking verdicts with task-sized handoffs and specific unmet
  acceptance criteria. Added paired behavior-comparison cases; existing
  installations and model settings are unchanged.
- Renamed `research-skill-patterns` to `find-skill-references`. Research now
  starts when the user seeks open-source references for a specific or planned
  skill; ordinary creation, editing, review, and explanation do not trigger it
  or require cached research. Updated the package, invocation metadata,
  repository rule, catalog links, and behavior cases. Implicit invocation
  remains enabled. Existing installed copies are unchanged; client discovery
  and natural selection for the renamed package require separate verification.
- Simplified `commit` by consolidating authorization and validation guidance,
  shortening commit grouping, and removing repeated workflow details from its
  game/design supplement and README. Existing commit and evidence boundaries
  are preserved.
- Added a goal-relevance check to `talk-it-through` before deepening discussion
  branches, preserving deliberate goal changes and necessary scope extensions.
  Added runnable cases for multi-turn drift, explicit reframing, and a necessary
  technical branch within the same goal.
- Condensed `talk-it-through` into three sections covering discussion, shared
  understanding, and continuation or closure. Preserved meaningful questions,
  local-decision follow-through, explicit stopping, and authorization boundaries.
- Moved `talk-it-through` into `skills/fern/talk-it-through` and removed the
  `thinking` collection. Updated catalog links; the skill name
  and invocation policy are unchanged. Existing installations are unchanged;
  client discovery from the relocated source remains unverified.
- Renamed `skills/meta-skills` to `skills/meta` and moved `maintain-skills`,
  `maintain-agents-md`, and `agent-ready` into it alongside
  `research-skill-patterns`. Updated catalog links and installation source paths;
  skill names and invocation policies are unchanged. Existing installations are
  unchanged; discovery of the relocated packages remains unverified.
- Simplified the meta skills by consolidating research guidance, loading
  CLI compatibility and direct-removal details only when needed, centralizing
  the agent-readiness report contract, and linking language rules from the
  AGENTS.md skill's README. Existing evidence, authorization, and report
  requirements are preserved.
- Simplified `reflect` into four stages with an early return for no supported
  candidates and conditional loading of routing branches. Consolidated repeated
  rules while preserving independent review, authoring dependencies, write
  authorization, evidence boundaries, and complete proposed-patch validation.
- Moved `learn-from-session` to `skills/fern/reflect` and renamed it to
  `reflect`. Expanded current-session learning to route durable preferences,
  project rules, facts, and reusable methods to appropriate existing sources,
  with evidence, conflict, visibility, recall, and expiry checks. Preserved
  proposal-only defaults and existing explicit write authorization. Updated
  usage and synthetic cases; existing installations are unchanged, and client
  discovery for the renamed package remains unverified.
- Clarified the image-prompt skills' primary tasks: creative brief development,
  visual extraction, and organizing, revising, or reviewing established prompts.
  Explicit skill selection remains supported. Shared rules now distinguish
  review-only feedback, reusable fragments, and full prompts, with separately
  copyable prompts for requested independent outputs. Optional omissions do not
  grant creative freedom. Consolidated output rules in the core, moved its
  structure guide into the entrypoint, and made the pixel example conditional.
  Added narrative cases and executable smoke definitions for these boundaries.
- Grouped `brief-to-image-prompt`, `gpt-image-prompting`, and `image-to-prompt`
  under `skills/image-generation/`, with a collection README and updated catalog,
  dependency links, and source-path guidance. Skill names, prompt workflows,
  and individual installation destinations are unchanged.
- `technical-writing` now gives direct guidance for clear prose, reader actions,
  and accessible instructions. Removed repeated example and review rules,
  consolidated source boundaries, and recorded pstack as a writing reference.
- `git-commit` maintenance guidance now describes disposable live Git trials
  for commit contents, intermediate-version checks, and preservation of unrelated
  work, with a combined split-execution case and explicit evidence limits.
- `maintain-agents-md` is shorter: language rules, authorization limits, and
  reporting duties are each stated once. Trimming now names what to remove
  (generic advice, discoverable facts, scope-chain duplicates) while keeping
  obligations. Reviews flag loading-size risk and sibling host files such as
  `CLAUDE.md`, creating a missing file follows the coverage guide, and the
  description covers creation, coverage audits, and nested or override files.
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
