# Behavior checks

Use a fresh agent and an isolated fixture to exercise selected skill behavior.
These checks complement static tests and client discovery. They do not prove
automatic selection, another client's behavior, or a real installation workflow.
The repository-wide [validation layers](validation.md) define when to run
these cases, how Docker and CI select them, and how to report unexecuted cases.

When a new behavioral constraint could block useful work, include both a case
that should trigger it and a nearby case that should remain allowed.

The [smoke cases](../examples/behavior-smoke.json) cover selected workflows from
the broader examples:

| Case | Skill and behavior |
| --- | --- |
| `reflect-*` (seven cases) | [reflect](../examples/reflect.md): stop when no durable candidate exists, preserve proposal defaults, route knowledge, apply authorized updates without duplication, preserve unresolved obligations, handle an unavailable skill author, and check stale knowledge during recall |
| `agents-*` (ten cases) | [maintain-agents-md](../examples/maintain-agents-md.md): discover coverage and effective sources, review commands, preserve policy, apply language preferences, and respect edit scope |
| `skills-local-edits` | [maintain-skills](../examples/maintain-skills.md): identify and preserve local edits before an update |
| `setup-fern` cases (twelve) | [setup-fern](../examples/setup-fern.md): apply complete user rules, exercise their delegation policy, repeat resource merges with the plan tool baseline, compare read-only, verify persisted receipts, exercise mixed ownership including an owned false plan tool value and interrupted recovery, and retry after a real fixture permission failure |
| `codex-config-*` (four cases) | [codex-config](../examples/codex-config.md): distinguish target-bound schema evidence from an online schema gap, apply a user-level edit under a project override, and preserve configuration when managed requirements disallow the requested value |
| `fern-workflow-*` (ten cases) | [fern](../examples/fern.md): review scope, local edits, accepted decisions, stale evidence, coupled work, evidence handoff, pending Git decisions, and actual bug fix, feature, and refactoring work |
| `docs-schema` | [technical-writing](../examples/technical-writing.md): apply a scoped schema correction while preserving accepted content |
| `talk-acceptance` | [talk-it-through](../examples/talk-it-through.md): advance after local acceptance and stop when asked |
| `talk-goal-drift` | [talk-it-through case 7](../examples/talk-it-through.md#7-a-drifting-branch-and-an-explicit-new-goal): check a drifting branch against the goal, distinguish interest from agreement, and follow an explicit goal change |
| `talk-needed-branch` | [talk-it-through case 8](../examples/talk-it-through.md#8-a-necessary-branch-within-the-same-goal): continue a necessary technical branch within the existing goal |
| `ready-*` (eight cases) | [agent-ready](../examples/agent-ready.md): trace real fixture tasks, calibrate recommendations, distinguish validation layers, and preserve review scope |
| `references-*` (five cases) | [find-skill-references](../examples/find-skill-references.md): inspect primary sources for requested comparisons, verify each cited file, resolve conflicts, reuse evidence, report gaps, and preserve scope |
| `search-*` (seventeen cases) | [deep-search](../examples/deep-search.md): plan evidence collection, run broad Exa then conditional Parallel gaps, stop when sufficient, preserve specialist routes and complete returned records, and deliver actual artifacts with partial coverage at caps |
| `image-prompt-review`, `image-prompt-fragment`, `image-prompt-multiple` | [gpt-image-prompting](../examples/gpt-image-prompting.md): review without rewriting, return a scoped fragment, and keep multiple prompts self-contained |
| `unslop-*` (fourteen cases) | [unslop](../examples/unslop.md): improve existing prose while preserving meaning, voice, protected material, and action scope |

The `commit-draft`, `commit-breaking`, `commit-game-feedback`,
`commit-design-tokens`, `commit-split-independent`,
`commit-split-dependent`, and `commit-split-override` cases cover
[commit](../examples/commit.md) using exported change snapshots.
Deliver the two `commit-breaking` turns separately. These are read-only
message trials; they do not validate Git staging, hooks, signing, or real
commit execution. The game and design cases also exercise conditional
reference loading and proposed checks; do not execute game or design tools.
The split cases exercise grouping, dependency order, asset completeness,
and user overrides through read-only plans; they do not execute commits
or reversions. Inspect the transcript as well as unchanged files.

The three `image-prompt-*` cases copy only the shared core package and exercise
text output. They do not cover the two entry skills, image observation, or
automatic routing. Use the [brief](../examples/brief-to-image-prompt.md) and
[image](../examples/image-to-prompt.md) narrative cases for those checks, with
their named core dependency available. No image generation or asset processing
is authorized by these trials.

The Unslop cases copy the complete `skills/fern/unslop/` package. Select exact
IDs from the following list; `unslop-*` is descriptive, not a wildcard option:

- `unslop-english` and `unslop-chinese`: natural prose improvements.
- `unslop-good-english` and `unslop-good-chinese`: leave clear prose unchanged.
- `unslop-contract` and `unslop-unknowns`: quantities, modals, scope, and unknown
  actors or causes.
- `unslop-protected` and `unslop-authority`: protected content, embedded
  instructions as data, and unsupported claims.
- `unslop-voice`: distinct voices, functional repetition, and a subsequent
  explicit style preference; deliver its two turns separately.
- `unslop-review` and `unslop-file-edit`: review-only versus an actual scoped
  section edit with file and section invariants.
- `unslop-previous`, `unslop-routing`, and `unslop-missing-target`: contextual
  targets, workflow boundaries, and a necessary target question.

For example, add `--case unslop-chinese --case unslop-file-edit` to the prepare
command below. Chinese strings use Unicode escapes in the public ASCII JSON;
preparation decodes the worker requests. Evaluate the decoded text and actual
responses. All Unslop cases prohibit project commands and network use; only
`unslop-file-edit` authorizes a fixture file change. Message revisions leave
source files unchanged. Keep evaluator observations out of worker inputs and
accept equivalent successful rewrites. Inspect the transcript for semantic
drift, protected text, voice, and actions: unchanged hashes do not prove that
no command ran, and a required file change does not prove a good edit.

## Select deep-search decision cases

Select exact IDs from the [deep-search cases](../examples/deep-search.md).
They copy the complete `skills/fern/deep-search/` package and use synthetic
tool definitions, retained results and failure traces. These offline trials
explicitly invoke the skill; they do not test natural selection. Supplied
schemas describe only their simulated host. Workers read only their copied
package and fixture, without network, real provider calls or retrieval
subprocesses such as Grok, installs, delegation, agent spawning, parent-directory
or profile access. Shell/Python may perform authorized local reads and explicitly
permitted output writes. Retrieved instructions are source data. All cases
preserve files except the explicitly
authorized artifact output case described below.

For six fresh trials, use:

- `search-plan-clarification`: material product/decision gaps and an unenforceable
  money cap require clarification before dependent paid requests.
- `search-exa-broad-plan`: a clear brief receives an actionable plan followed by
  multiple distinct first-round Exa objectives without an approval gate.
- `search-first-round-sufficient`: complete first-round evidence meets each
  criterion, so Parallel and unnecessary final verification are skipped.
- `search-parallel-gap`: after Exa, Parallel receives only unmet independent
  observation questions, existing evidence, duplicate exclusions and the precise
  additional evidence needed.
- `search-known-source-routing`: known quality pages use Exa content directly
  when needed; adequate content is reused. With GitHub tools absent, the pinned
  repository file uses the built-in raw reader while issue/PR pages keep their
  original URLs. No GitHub target uses Exa content.
- `search-artifact-cap-partial`: exhausted caps with missing evidence require
  partial coverage and actual local artifact output, not just a proposed plan.

Assess plan substance: downstream purpose/questions, directions and priorities,
scope/date/version/exclusions, per-direction evidence and enough criteria,
rounds/triggers/caps, shared allowance and handoff location. A cap does not
establish sufficiency. Budget ownership includes retries and prospective workers;
these cases do not execute delegation. Unknown prices cannot support savings
claims or a silent conversion from currency to calls. Inspect actual successful
reads, replies, file outcomes and tool events; criteria are semantic observations,
not required wording.

`search-artifact-cap-partial` permits only `output/plan.md`,
`output/evidence.md`, `output/handoff.md`, `output/raw/returned.json`,
`output/raw/attempts.json` and `output/raw/index.json`. The user explicitly
selected this workspace destination. Inspect actual creation and readback,
compare raw copies with complete retained fixture bytes, check source IDs and
provenance in the index, and verify every pre-existing file remains unchanged.
The response must return real absolute paths and the unmet criterion, with no
final migration recommendation. `search-artifact-paths` separately plans the
unique OS-temp default and a remote-host access gap without writing files.
Neither establishes real cross-host transfer or persistent storage.

The ten retained IDs remain available: `search-cache-complete`,
`search-shared-budget`, `search-schema-recovery`, `search-mixed-cache`,
`search-official-and-github`, `search-social-evidence`,
`search-staged-escalation`, `search-x-native`, `search-x-grok` and
`search-x-default`. Inspect complete cache reuse, correction of current schemas
only for unresolved requests, per-item retry preservation and source-instruction
isolation. The shared-budget case honors the explicit Exa request with two of
three attempts left. The staged case reuses adequate built-in official evidence,
uses Exa for the uncovered direction, and reserves Parallel for a remaining gap.

The official/GitHub case uses known OpenAI specialist documentation/schema
locators and direct GitHub file/issue tools without forced rediscovery. Keep API
contracts, pinned implementation, merged changes, release and deployment
evidence distinct. Exa content preference for substantive known pages is a
workflow choice, not proof of extraction superiority.

X retains native X -> installed usable local Grok -> current host model default.
`search-x-native` needs no Grok probe. `search-x-grok` uses inspected synthetic
help with `--single`, `--output-format`, `--tools`, `--max-turns` and `--cwd`,
reuses the retained successful readiness trace, and plans an empty temporary
working directory. A process or turn can cause multiple underlying calls and
does not enforce a money or API-count cap. Report usage and unknown counters;
this success case has no hard monetary/API cap. `search-x-default` has failed
authentication despite command/version presence and therefore uses the host
default without login, installation or a silent Exa/Parallel switch.

The social case reuses retained provider records but treats a post and its
repost as one underlying report. With native X and usable Grok absent,
`builtin_search` is the supplied host default for new X discovery and
`builtin_fetch` reads the known status page. A stale status snapshot does not
establish today's availability; selected posts do not establish representative
sentiment or native platform coverage.

For example, add `--case search-exa-broad-plan --case search-parallel-gap` to
the launcher below. An actual model run supplies offline decision evidence and,
for the artifact case, authorized fixture file outcomes. It does not establish
online MCP compatibility, authentication, live retry behavior, retrieval quality,
natural selection, cross-agent coordination, native X coverage or monetary
savings. Report unexecuted cases as not run.

## Run agent cases in Docker

Use the [unified validation launcher](validation.md) for any eligible case from
any collection. Run locally through Docker; repository automation uses the
runtime and full CI workflows. From the repository root:

```text
python scripts/run_validation.py --layer affected --base origin/main --output /tmp/skills-agent-001 --run-agent --model YOUR_ACCESSIBLE_MODEL
```

Supply `CODEX_API_KEY` in the launching environment, or the local
`OPENAI_API_KEY` alias, and a model accessible to that credential. These are
real model calls. No model runs unless `--run-agent` is explicit. A planned
case left unrequested is `not_run` and leaves overall coverage partial; a
requested model run without its prerequisite fails.

Repeat `--case` for exact case IDs to narrow a run. The full layer without
case selection plans every eligible smoke case, including skills outside
Fern. The planner reports skills without executable cases as coverage gaps.
Use `--plan-only` to inspect selection without Docker or model calls. See the
[validation guide](validation.md#request-actual-agent-execution) for CI opt-in,
credentials, isolation and evidence rules. Generic explicit skill delivery is
not a natural-selection test.

The worker and evaluator run as separate users in a disposable container.
Each case starts a fresh worker, while later requests resume only that case's
session. The worker receives the copied skill and fixture inputs; evaluator
criteria, source examples and baseline evidence remain inaccessible. For
`reflect-stale-recall`, the worker instead receives only its ordinary task and
project context. Preserve that negative control when using another runner.

Keep case manifests, actual transcripts and tool events, intermediate
snapshots, assessments and recorded results. Filesystem invariants and a
separate evaluator both contribute to the result. Evaluator agreement does
not replace independently checking actions, preservation, ordering and outputs.
The manual delivery procedure below remains useful for cases requiring tools
or host behavior beyond the automated executor.

## Run Setup Fern in Docker

Setup Fern uses the same layered launcher. For two selected fixture cases:

```text
python scripts/run_validation.py --layer affected --check agent-behavior --case fern-resource-merge --case fern-read-only --output /tmp/fern-behavior-001 --run-agent --model YOUR_ACCESSIBLE_MODEL
```

Use the full layer with `--run-agent` for all eligible repository cases, or
repeat `--case` for the exact Fern case IDs below. Existing calls to
`python scripts/run_fern_validation.py --suite behavior` remain compatible and
select Fern cases only. Choose a fresh absolute output directory outside the
checkout and real client profiles; on Windows use a writable absolute path.

The permission-retry case creates a real Linux permission denial, then repairs
fixture permissions before the separately delivered retry request. Retain
actual tool output and per-turn file statistics to check the denied attempt
and unchanged completed units. Preconstructed interruption fixtures do not
kill a live process. These cases do not establish native custom-agent spawning
or instruction loading, Windows junction migration, or live crash recovery.

## Prepare

From the repository root, use the development environment described in the
[README](../README.md#development). Choose a new output directory outside this
repository and outside real client profiles. Replace the example path below
with a writable temporary path on Windows, and use `.venv\Scripts\python.exe`.

```text
.venv/bin/python scripts/behavior_trials.py prepare --output /tmp/skills-behavior-001
```

Add `--case reflect-proposal` to select one case; repeat `--case` for several.
Preparation refuses to overwrite an existing run. Each case directory contains:

- `workspace/`: the synthetic project and complete copied skill package.
- `input.json`: context, skill location, and ordered user requests.
- `evaluator.json`: evaluator-only observations and filesystem invariants.
- `manifest.json`: preparation time, source revision and hashes, case and
  fixture hash, and initial workspace hashes.
- `before/`: the original workspace for inspecting changes.

## Select Fern workflow cases

Select the exact IDs `fern-workflow-review`, `fern-workflow-local-edit`,
`fern-workflow-steering`, `fern-workflow-stale-evidence`,
`fern-workflow-coupled-plan`, `fern-workflow-evidence-reuse`,
`fern-workflow-pending-commit`, `fern-workflow-bug-fix`,
`fern-workflow-feature`, and `fern-workflow-refactoring`. Each copies the
complete Fern package, including playbooks and shared references. These cases
do not exercise environment setup or installation. Missing optional skills
and roles are intentional inputs in the local-edit and steering cases.

Deliver the steering turns separately in the same fresh session. Retain an
intermediate file snapshot to verify first-turn preservation and second-turn
application. Inspect saved JSON values as well as the harness invariants.
The evidence and pending-process cases use synthetic retained records; they
exercise decisions, not actual test execution, Git signing, publication, or CI.
Coupled-plan exercises Fern's dependency and shared-resource coordination.
Stale-evidence also covers known environment reuse and pilot delivery failures;
its paths and commands are simulated inputs. Evidence-reuse remains a control
against unnecessary validation. General dispatch policy is tested separately
by `fern-delegation-plan`; none establishes real agent coordination.

The three development cases exercise Fern directly without a separate
implementation skill. Give each fresh worker its input context, request, and
copied package. Inspect actual reads to confirm the relevant playbook was used,
and retain commands, exit statuses, counts, changes, and before/after evidence.
The fixtures permit Python with `-B` and stdlib `unittest` for project checks;
no Git, network, installation, other agents, caches, or additional artifacts.
Run checks from each case's workspace, for example:

```text
python -B -m unittest discover -s . -p test_retries.py -v
python -B -m unittest discover -s . -p test_shipping.py -v
python -B -m unittest discover -s . -p test_invoice.py -v
```

Use only the command matching that fixture and the available interpreter.
The bug baseline must fail on the reported regression before the fix and pass
afterward without changing tests. The feature case starts with passing old
checks and needs actual tests of the new behavior and compatibility. The
refactor requires passing before/after checks and a real reduction of
duplication, preserving the intentional edge behavior. File invariants alone
do not prove these outcomes. Explicit invocation trials do not establish
automatic selection or host discovery.

## Select Fern setup cases

Select the twelve case IDs from the table below. `fern-delegation-plan` reads
the copied user-instruction asset as effective synthetic policy and proposes
handoffs without invoking setup. The other cases use isolated fixture Codex
homes, the complete copied `setup-fern` package and a
synthetic frozen source SHA. Workers may not use network, installers, real
user-profile access or model spawns. The complete instruction asset includes
initiative, user precedence, writing style, delegation, built-in explorer model
and reasoning defaults, and testing rules. Assess the full content as well as
markers and receipt hashes.

| Case | Focus |
| --- | --- |
| `fern-resource-merge` | Add the plan tool baseline to an existing table, preserve unrelated tool settings, and repeat in the same session |
| `fern-read-only` | Inventory gaps and conflicts without writes |
| `fern-delegation-plan` | Apply the maintained user-level dispatch policy to proposed briefs, completed-agent resumption and bounded waiting; no setup or actual delegation |
| `fern-fresh-user-instructions` | Complete rules and a canonical receipt in a new home |
| `fern-legacy-instructions-migrate` | Owned legacy block and historical receipt including LF |
| `fern-legacy-instructions-edited` | Locally edited legacy policy preserved |
| `fern-persisted-receipts-update` | Fresh reader of canonical, following-LF and following-CRLF current-marker receipts |
| `fern-persisted-receipts-edited` | Internal whitespace, line-ending edits and target mismatch preserved |
| `fern-persisted-receipts-read-only` | Current and legacy historical receipt checks without canonicalization |
| `fern-mixed-resource-update` | Update an owned false plan tool value and other owned units alongside edited and unknown agent/config units |
| `fern-interrupted-resource-recovery` | Adopt an already-written value and restore only unchanged applied agents |
| `fern-permission-retry` | Preserve a failed config unit, then retry it after actual fixture permissions are repaired |

The [missing plan tool scenarios](../examples/setup-fern.md#native-plan-tool-unavailable)
route to the executable `codex-config` cases below. They are separate from
these twelve cases for the setup package.

Deliver the two `fern-resource-merge` turns separately in the same session,
retaining the first application before the repeat. Check that
`tools.update_plan.enabled` becomes true in its existing table, unrelated
`tools.web_search.allowed_domains` survives, its per-key receipt is correct,
and the repeat leaves content stable without duplicate TOML tables. In
`fern-mixed-resource-update`, verify that the receipt-owned false plan tool
value becomes true with a new per-unit receipt while the edited and unknown
units retain their existing conflicts. For
`fern-fresh-user-instructions`, check creation in the effective Codex home and
the `instructions:user-rules` receipt. Compare
`fern-legacy-instructions-migrate` with `fern-legacy-instructions-edited`: the
former allows replacing an exactly owned historical block, while the latter
requires all fixture files to remain unchanged. Retain actual reads and writes
to establish that the old receipt is removed only after new-block readback in
the successful case. The read-only case also requires an unchanged workspace.

For every newly recorded instruction receipt, independently hash the raw
bytes from the start marker's opening `<` through the end marker's closing
`>` inclusive. Exclude any following LF or CRLF and preserve internal bytes.
Check the recorded target and source SHA as well as the digest. Compatibility
reads may test only that exact range and, when present in the file, the range
plus its single immediately following LF or CRLF. An internal edit or target
mismatch must remain unresolved. A compatible historical receipt for an already
aligned block does not require rewriting its hash or source revision.

Run each persisted-receipt case with a fresh worker. Its prior-run blocks and
receipts are synthetic fixture files, not observed output from another agent.
They exercise consumer decisions independently of same-session memory. The
update case uses short historical bodies to avoid duplicating the current
asset; verified ownership does not mean those bodies are already aligned.
The read-only case must retain its historical hashes and legacy receipt key.
Inspect actions as well as final files to distinguish validation from an
unauthorized normalization write.

For an actual cross-session handoff, follow the
[producer-to-consumer procedure](../examples/setup-fern.md#persisted-instruction-receipts-in-a-fresh-session)
using retained artifacts from an authorized fixture run and a new isolated
home. Keep the producing snapshot and raw bytes, use a fresh check-only worker,
and compare all target and receipt bytes afterward. Report this executed
handoff separately from synthetic prior-run compatibility and from actual host
loading. Neither fixture preparation nor a first executor's success claim is
evidence that a later executor read and accepted its receipt.

Run the mixed-resource and interrupted-recovery cases with fresh workers and
no earlier replies. Their agent files, receipts and journal are synthetic raw
artifacts. Compare selected file hashes and parsed config values independently;
retain actual actions to assess validation and receipt ordering. The recovery
case supplies a previously written config file and a later edit to an applied
agent; it does not actually interrupt a live process. The harness automatically
checks required changes, while evaluator criteria cover preservation of
conflicting units, original backups, unrelated content and per-unit receipts.
Neither fixture defines a new installer or standard journal format.

These fixtures do not prove actual Codex instruction loading, explorer model
availability or spawning, live source resolution, or skill installation. Use
the [setup examples](../examples/setup-fern.md) for the additional narrative
cases and keep those unexecuted expectations separate from recorded runs.

## Select Codex configuration cases

Select the four exact IDs `codex-config-runtime-schema`,
`codex-config-online-schema-gap`, `codex-config-layered-edit`, and
`codex-config-policy-conflict`. Each copies only the complete `codex-config`
package and supplies offline synthetic runtime, configuration, and support
records. See the [narrative cases](../examples/codex-config.md) for acceptance
details; keep those details and evaluator criteria out of worker inputs.

The two diagnostic cases require an unchanged workspace. The runtime-schema
case supplies support evidence bound to the Desktop target; the online-schema
case intentionally lacks it. The edit case requires changes only to the user
config and its named exact-byte backup, preserving the higher-precedence
project file. The policy-conflict case requires the full fixture unchanged
because the requested value violates retained target managed requirements.

Workers may inspect fixture files and use Python standard-library parsing with
`-B`. No network, installers, real profile access, CLI/runtime invocation, or
model spawns are allowed. Retain actual reads, commands, replies, before/after
parses and files; inspect semantic preservation and backup ordering separately
from filesystem invariants. These are instructions-only agent decision checks,
not live discovery, runtime compatibility, loaded configuration, tool exposure,
or native UI checks. Natural selection remains a separate unverified
expectation.

## Select reflection cases

Select the seven `reflect-*` cases by their exact IDs:

| Case | Focus and observed file boundary |
| --- | --- |
| `reflect-empty` | Reject temporary notes and generic advice after reading the candidate rubric, without loading later references or starting a reviewer; unchanged workspace |
| `reflect-proposal` | Evidence-backed skill improvement proposal; unchanged workspace |
| `reflect-routing` | Route different kinds of durable knowledge to appropriate sources; unchanged workspace |
| `reflect-save-repeat` | Save authorized project knowledge and reconcile a repeated request; only the existing project document may change |
| `reflect-conflict` | Keep an existing obligation active while a proposed conflict is unresolved; unchanged workspace |
| `reflect-missing-author` | Propose skill changes when the required author is unavailable and apply an independent document update; only the existing project document may change |
| `reflect-stale-recall` | Check a stale fact through the ordinary project's reading entrypoint without invoking reflection; unchanged workspace |

Deliver the two `reflect-save-repeat` requests separately in the same session.
Retain the file contents after the first response as well as the final contents
to check the initial save and detect repeated writes. For
`reflect-stale-recall`, start a fresh agent with the case's ordinary task and
project context; do not provide or load `skill/SKILL.md`. Its prewritten
`AGENTS.md` and linked memory exercise the reading contract only; a passing
result does not prove a complete save-and-recall sequence across sessions.

For `reflect-empty`, retain observed tool actions to establish that the
candidate rubric was read and routing, reviewer references, and an independent
reviewer were not used. An unchanged workspace alone does not establish this
early exit.

## Select AGENTS.md maintenance cases

The ten `agents-*` cases are individually selectable; selection uses exact IDs,
not wildcard expansion. Their full definitions live in the smoke JSON, with
[narrative acceptance cases](../examples/maintain-agents-md.md).

| Case | Focus and observed file boundary |
| --- | --- |
| `agents-review` | Equivalent duplicate, documentation exception, nested scope; unchanged workspace |
| `agents-coverage` | Sparse instructions and eight coverage responsibilities grounded in canonical sources; unchanged workspace |
| `agents-discovery` | Nested discovery, supplied synthetic host precedence, and unknown-host boundary; unchanged workspace |
| `agents-command-review` | Stale command, prerequisites, success signal, and deployment effects; static inspection only |
| `agents-capture-revise` | Confirmed capture, deduplication, established expiry, and preserved signing duty; one required file change |
| `agents-language-default` | Chinese body inference, default English headings, contents and authorized dependent anchors; two required file changes |
| `agents-language-scoped` | Chinese body and section-limited addition; required edit with bytes outside the section preserved |
| `agents-language-override` | Explicit Chinese headings with English body and revised anchor; one required file change |
| `agents-language-question` | Ambiguous body language prompts a focused question; unchanged workspace |
| `agents-untrusted-source` | Embedded unauthorized instructions and fake sensitive content; unchanged workspace |

For example, select the three language-edit cases together:

```text
.venv/bin/python scripts/behavior_trials.py prepare --output /tmp/agents-language-001 --case agents-language-default --case agents-language-scoped --case agents-language-override
```

To exercise the complete maintenance set, repeat `--case` for all ten IDs in the
table; omitting selection also prepares unrelated skills. Chinese fixture text
uses Unicode escapes in the ASCII JSON and becomes UTF-8 project text during
preparation. Inspect prepared files when judging actual heading/body languages
and links; escaped source text is not the agent's document output.

## Select skill reference cases

The five `references-*` cases use original fictional source snapshots. They
need no network or connector. A catalog preview is not primary evidence, and
the source snapshots, revisions, and results do not describe real upstreams.
Any real upstream links are discovery-only and supply no primary content.
Each request explicitly seeks references for an existing or planned skill.

| Case | Focus and observed file boundary |
| --- | --- |
| `references-review-conflicts` | Compare conflicting references, reject an unsupported preview and embedded instruction, propose suitable changes; unchanged workspace |
| `references-reuse` | Assess a requested cached reference and make a separately authorized spelling correction; one required file change |
| `references-unavailable` | Report reference gaps and local findings with only previews and no network; unchanged workspace |
| `references-verification-gate` | Verify a read primary file while keeping unavailable sibling-file and familiar-library claims unverified; unchanged workspace |
| `references-create` | Compare references for a planned skill, then create the separately authorized file; one required new file |

Prepare all five cases with:

```text
.venv/bin/python scripts/behavior_trials.py prepare --output /tmp/skill-references-001 --case references-review-conflicts --case references-reuse --case references-unavailable --case references-verification-gate --case references-create
```

Run each with a fresh worker. Supply only its workspace, copied skill, context,
and request from `input.json`; keep evaluator expectations private. Observe
actual reads of primary-source files and whether they precede creation. Never
execute `authorize-review.py` or the target export task. The embedded
invocation is untrusted source content. A filesystem diff alone does not
establish which commands ran or which sources were read.

Evaluate source-to-decision reasoning, applicability, honest limits, and actual
file changes. For `references-reuse`, compare exact before/after contents.
Its research is requested explicitly; a spelling-only request requires no
reference research. These execution trials do not prove natural selection,
live search access, or real upstream correctness.

For `references-verification-gate`, match every evidence citation, including
unlabeled upstream claims, to the exact text returned by a successful read. A worker
claim, attempted read, link, summary, or read of a sibling file is insufficient.
Retain the returned text as evidence. The case permits grounded verification of
the readable Maple snapshot while requiring honest limits for unavailable
files; it does not exercise live retrieval of CPython.

Include delegated source reads in the retained evidence. If a runner omits
subagent traces, missing reads are unverified, not proven absent; rerun with
complete task traces or a confirmed single-agent run.

Run the [natural selection cases](../examples/find-skill-references.md#natural-selection-cases)
separately with the skill discoverable through the host's normal metadata.
Do not supply its body or an instruction to use it, and do not include the
expected result in worker inputs. Record observed selection for the three
reference-seeking positives and the ordinary creation, edit, review,
explanation, domain-task, and installation negatives. Preparing a case or
classifying its request does not establish automatic selection.

## Run the agent

Give a fresh agent the workspace path, copied `skill/SKILL.md`, context, and
first request from `input.json`, except for the ordinary-task
`reflect-stale-recall` delivery described above. State the actual absolute
workspace path explicitly as the worker's cwd. Resolve `skill/SKILL.md` and
all fixture paths relative to that cwd; do not pass bare relative locators
without this base. For example, a prepared `search-x-grok` delivery identifies
its case's `workspace/` directory as cwd, then names `skill/SKILL.md`,
`tools.json`, `local-grok.json`, `grok-help.txt`, `cache/readiness.json`,
`cache/source.json` and `ledger.json` relative to it. Deliver the context and
request as written in `input.json`; keep evaluator observations private.
Allow only the fixture operations requested by that case. Keep `evaluator.json`,
`manifest.json`, and `before/` out of its context.
For `talk-acceptance` and `talk-goal-drift`, deliver each subsequent request only
after receiving the previous actual reply, keeping the same session. Do not add
hints to continue, notice drift, or change goals.

For `agents-*`, honor each case's edit and execution boundary. All
command-review
cases are static: do not run the supplied validation, deployment, or approval
scripts. The discovery fixture supplies a fictional host contract solely to
test evidence-based precedence; passing does not establish loading behavior of
Codex, Claude Code, or any other real host. The ambiguous body-language case
ends after the initial question; it does not supply a language answer. Review
cases require no file changes, while edit cases require actual authorized
changes as well as semantic preservation. Inspect observed actions for command
execution: an unchanged workspace alone cannot prove that no command ran.

The eight `ready-*` cases are executable synthetic project reviews. Their
Python standard-library commands use `-B` to preserve the read-only workspace;
inspect command effects before running them. Do not start listeners, install
dependencies, or execute data-writing paths. Supply only worker inputs, never
the expected diagnoses from the case descriptions or evaluator criteria. A
passing simulated review does not establish readiness of a real project or
prove browser, rendering, or human-experience behavior.

The maintenance case replaces `npx skills` with `python mock_skills.py`. Its
inventory, source records, upstream files, and command log are synthetic. Never
substitute a real CLI, user installation, or remote source for this fixture.

Record each exact request and actual reply in a transcript JSON file:

```json
{
  "turns": [
    {
      "request": "Exact request from input.json",
      "response": "Actual agent reply",
      "actions": ["Observed command or artifact; label agent-reported actions"]
    }
  ]
}
```

Keep tool output or other supporting evidence when needed to assess a criterion.
Do not replace missing observations with an agent's success claim. The prepared
directory is an isolation boundary for the trial instructions, not an OS
sandbox;
filesystem checks observe only that workspace, not the rest of the host.

## Live Git trials

Use this maintainer procedure when validating actual `commit` execution,
such as the [split execution case](../examples/commit.md#live-split-execution-and-intermediate-versions).
It is not a requirement for ordinary commits. The snapshot helper above does
not create or verify live Git fixtures; retain these trial artifacts separately.

1. Create a disposable repository outside the source repository and client
   profiles, with no remote. Copy the skill package and record its revision and
   file hashes. Prepare a runnable baseline, synthetic intended changes, and
   unrelated staged, unstaged, and untracked work. Record fixture-local
   identity, signing, hooks, and configuration; do not alter user configuration
   to prepare the trial. If signing is not exercised, state that coverage limit.
2. Before running the agent, save the baseline commit and expected logical
   changes in evaluator-only evidence. Record index entries (path, mode, stage,
   and blob content), working-file hashes, and tracking/staging status. Useful
   inspection commands include `git ls-files --stage -z`,
   `git status --porcelain=v1 -z`, and `git cat-file blob <object-id>`.
   Include untracked files in the baseline; status labels alone cannot prove
   unchanged contents. Keep expected outcomes and baseline evidence outside
   the agent's inputs.
3. Give a fresh agent the copied skill, fixture path, and a request naming the
   changes it may commit. Allow staging, relevant checks, and local commits
   within that fixture. Retain observed actions and check output. When a hook
   checks the staged candidate, record its tree and result, then compare that
   tree with the resulting commit so evidence cannot silently apply to a
   different version.
4. Independently inspect the commits created since the recorded baseline.
   For each commit, compare `git ls-tree -r -z <commit>` and its blob contents
   with the expected cumulative logical changes: paths, modes, object types,
   and content must match. Check intent completeness and prerequisite order;
   accept valid alternative ordering of independent intents. Do not infer
   grouping from messages or a fixed commit count alone.
5. Create a fresh isolated checkout or export matching each recorded commit
   tree, and run that version's relevant checks there. Verify that the copy
   includes the required files and dependencies before running checks. Retain
   the commit/tree IDs, commands, exit codes, and output for each version.
   Do not let later working-tree changes supply missing files or mask an
   unusable intermediate version. Report unavailable checks as unverified.
6. Compare the remaining index entries and working files with the expected
   final state. For untouched paths, compare with the baseline. For paths
   shared with intended changes, construct the expected index from the final
   committed version plus the preserved unrelated staged changes, then the
   expected working file by adding the preserved unstaged changes. Compare
   these versions and their differences; do not require the whole index blob
   to equal its baseline. Verify untracked files retain their contents and
   tracking state. Check relevant modes and paths as well as hashes. This
   comparison concerns content and staging state, not byte-identical
   `.git/index` metadata. Confirm configuration and hooks remain as prepared.

Retain a local result with per-commit checks, preservation comparisons, observed
failures, and coverage limits. Use a separate evaluator to inspect the evidence;
keep raw transcripts and machine paths out of the public repository. A passing
synthetic trial does not establish real engine behavior, visual quality, human
acceptance, or unexercised signing and rejecting-hook paths.

## Assess and record

A separate evaluator reads the transcript, actual file changes, available tool
evidence, and `evaluator.json`. Assess each criterion as `passed`, `failed`, or
`unverified`, with a reason and concrete evidence. The following is
illustrative:

```json
{
  "evaluator": "Evaluator identity",
  "criteria": {
    "supported-lesson": {
      "status": "passed",
      "reason": "The proposal follows the supplied verified correction.",
      "evidence": ["Turn 1: exact header and row order are both addressed."]
    }
  }
}
```

Use the actual criterion IDs for the selected case. Missing assessments or
evidence remain unverified. Save this JSON separately, then record the run:

```text
.venv/bin/python scripts/behavior_trials.py record --trial /tmp/skills-behavior-001/reflect-proposal --transcript /tmp/transcript.json --assessment /tmp/assessment.json --runner "Codex desktop subagent" --model "actual model/version, or unavailable"
```

Record the actual runner and model/version when exposed; state unavailable when
the host does not expose it. The recorder retains transcript and assessment,
copies `after/`, and writes `result.json` with observed file changes, source and
case drift, and the supplied semantic assessments. A failed invariant or
criterion fails the run. Incomplete turns, unassessed criteria, or source/case
drift prevent a passing result. Recording does not independently establish that
an evaluator's semantic judgment is correct.

The command exits 0 for passed, 1 for failed or unverified, and 2 for an input
or
execution error. It refuses to overwrite an existing result. For a retry or a
before-and-after comparison, prepare fresh directories and preserve earlier
results. Keep equivalent requests, fixtures, and runner settings when comparing
skill versions. Retain the evidence directory locally; do not commit raw session
logs or machine paths to the public repository.

The ordinary unittest suite tests this harness with synthetic responses; it does
not run agents. Run selected agent trials separately when behavior changes, and
report executed cases and remaining coverage without treating one sample as a
reliability estimate.
