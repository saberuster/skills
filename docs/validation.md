# Validation layers

This is the repository-wide contract for selecting checks and interpreting
their evidence. It covers every skill collection, shared script, test, and CI
workflow. Use [development.md](development.md) for implementation details and
[behavior-checks.md](behavior-checks.md) for case delivery and assessment.

## Choose a layer

| Layer | Trigger | Checks | Evidence boundary |
| --- | --- | --- | --- |
| `pr` | Every pull request and push | Linux Docker checks plus native Windows regressions across all non-engine modules; Ruff and Markdown lint run in Linux | No model requests or real engine runs; mock clients and synthetic replies test the validation tools |
| `affected` | Changes affecting runtime or behavior; manual selection | Relevant pinned-client discovery, Fern snapshot installation, background Blender integration and selected agent cases; the PR layer runs independently | Only executed checks and cases supply runtime or model evidence |
| `full` | Weekly, manual, and release validation | The PR checks, all implemented runtime checks, pinned and latest-client discovery, and every eligible agent case when requested | The broadest automated coverage; remaining manual scenarios and missing cases stay explicit |

Layer membership describes which evidence to request. It does not make a
missing prerequisite, skipped test, or unrequested model run a pass. A full
no-model run can pass its executed checks while still reporting partial
coverage of the full plan.

## Run locally or in CI

On a user machine, run the unified launcher through Docker. From the repository
root, use Python 3.11+, Git, and a running Docker daemon:

```text
python scripts/run_validation.py --layer pr --output /tmp/skills-pr-001
python scripts/run_validation.py --layer affected --base origin/main --output /tmp/skills-affected-001
python scripts/run_validation.py --layer full --output /tmp/skills-full-001
```

Use a new absolute output directory outside the checkout and real client
profiles for each run. On Windows, replace `/tmp/...` with a writable absolute
temporary path. Host Python needs only its standard library; development and
client dependencies are installed inside Docker. The launcher copies public
working-tree sources, including unignored additions, into the build context.
It does not mount the host checkout, home, client profiles, or Docker socket.
Pinned tools and verified runtime downloads are defined in the
[container definition](../scripts/validation-ci/Dockerfile). Base image tags
and OS packages are not a fully immutable image lock.

Inspect the selection without Docker or model calls:

```text
python scripts/run_validation.py --layer affected --base origin/main --output /tmp/skills-plan-001 --plan-only
```

The planner records changed paths, selected checks and cases, and known
coverage gaps. Use `--base` to name the comparison revision. Check the plan
when validating unpublished files or a branch whose comparison base differs
from the intended PR. An unavailable base is an input error, not an empty
change set. Without `--base`, affected selection covers all current packages.
`--base` is valid only for the affected layer. The full layer includes pinned
and latest discovery by default; `--latest` adds that channel to an affected
run. The current working tree is the source under test; a commit label
alone does not establish byte-for-byte identity with a clean commit.

For repository automation, use the checked-in GitHub Actions workflows:

| Workflow | Role |
| --- | --- |
| [validate.yml](../.github/workflows/validate.yml) | Required Linux Docker and native Windows deterministic checks on pushes, PRs and manual runs |
| [validation-runtime.yml](../.github/workflows/validation-runtime.yml) | `affected` runtime checks and explicitly enabled agent behavior |
| [validation-full.yml](../.github/workflows/validation-full.yml) | Scheduled, manual and release `full` validation |
| [agent-support.yml](../.github/workflows/agent-support.yml) | Prompt-free client discovery and the generated README support table |
| [validation-windows.yml](../.github/workflows/validation-windows.yml) | All non-engine Windows regressions; reused by PR/full validation and available for a standalone manual run |

The agent-support workflow retains its report and README publication format.
Pinned discovery supplies layer 2 evidence; latest-client discovery supplies
layer 3 upstream compatibility evidence. Latest results do not overwrite the
README's pinned-client table. Read actual job conclusions and artifacts after
pushing: workflow configuration is not an observed hosted execution.

Before publishing a release, manually run full validation for the intended
revision and inspect its evidence. The `release: published` trigger provides a
post-publication regression run; it does not block publishing. There is no
automated release pipeline currently consuming an eval gate.

## Check selection and prerequisites

The launcher accepts repeated `--check` values to narrow the applicable plan.
Selecting a check outside that plan is an input error; use the full layer or
an appropriate affected scope instead. A focused run does not establish
completion of the rest of its layer. The affected layer runs runtime checks;
run the independent PR layer as well when validating the whole change locally.

| Check | What actually runs | Prerequisites and limits |
| --- | --- | --- |
| `checks` | Ruff, Markdown lint, and all non-engine unittest modules, including package/link hygiene, helper scripts, protocol mocks, installer and behavior harness regressions | No API key; PowerShell is supplied for the Godot helper fixtures; synthetic responses do not exercise model decisions |
| `codex-discovery` | Real Codex app-server initialization and skill listing in an isolated profile | No API key or model prompts; names, descriptions, paths, enabled state and load errors are checked |
| `claude-discovery` | Real Claude Agent SDK initialization with its bundled CLI in an isolated profile | No API key or model prompts; initialization lists available skill commands |
| `fern-install` | Real pinned Skills CLI installation from public snapshots, provenance checks and local discovery | Network required; verifies package installation separately from the project resource installer; no model prompts |
| `blender` | The two background Blender integration modules | A real Blender executable inside the container; controlled scene creation and audit checks, not visual or human acceptance |
| `agent-behavior` | Real Codex worker turns and a separate evaluator for selected smoke cases, plus filesystem invariants | Explicit `--run-agent`, accessible `--model` and API credential; real calls, tool actions and judgments must be retained |

The planner selects runtime checks from changed skill and helper paths. Shared
validation, package discovery, case definitions and runtime infrastructure can
affect several collections. A changed skill with no automated behavior case is
a coverage gap, not a reason to invent a successful behavior result. Inspect
the selected plan before narrowing it with explicit checks or cases.

All known unittest modules belong either to the deterministic layer or to the
separate real-engine check. Pure component geometry and fake Godot process
tests belong to `checks`; their names do not make them engine integration.
Standalone `python -m unittest discover -s tests -v` remains useful for
debugging, but can skip unavailable Blender or platform paths. Its green exit
alone does not establish the layered plan's runtime coverage.

## Fern installation provenance

The `fern-install` runtime check verifies the pinned Skills CLI against resolved
public source snapshots. A lock's `skillFolderHash` may contain either the Git
directory object ID or the CLI's supported content SHA-256 fallback. The probe
computes the expected value from the trusted snapshot for the corresponding
form; a hash-shaped string alone is insufficient. Repository, source URL,
revision and skill path must still match, and installed package bytes must
match the complete source package.

The content hash uses the existing Node runtime to preserve Skills CLI 1.7.0's
path ordering and byte-stream rules. This hash is separate from the probe's
complete package-byte check. The pinned upstream
[fallback selection][skills-hash-selection] and
[content hash algorithm][skills-content-hash] define the compatibility scope.
A supported fallback does not identify the network or API condition that
selected it.

Installation reports retain allowlisted lock provenance, lock structure and
field-level expected/actual differences before the disposable profile is
removed. They report the matched hash form on success. Missing or malformed
locks and failed hash computation remain failures with diagnostic evidence.
Unknown lock fields are not copied into the report.

`tests/test_fern_install.py` covers both hash forms, source-field mismatches,
content tampering and retained failure diagnostics in the deterministic
`checks` layer. Its content-hash fixtures require Node; Docker already supplies
it and native Windows CI checks the image's Node runtime before running tests.
These fixtures do not establish a real public installation or client discovery;
the separate `fern-install` runtime job provides that evidence.

The packaged Setup Fern installer has deterministic regression coverage in
`tests/test_setup_fern_installer.py` and `tests/test_setup_fern_resources.py`,
selected by `checks` on Linux and Windows. These execute the candidate script
with bundled assets against isolated projects: config merge, six agents, root
instructions, direct overwrites, one config write, selected-path link checks,
unrelated-content preservation, read-only comparison and unchanged repeats.
The installer does not install skills; the separate `fern-install` probe above
continues to validate public package distribution and client skill discovery.
A Linux-only deterministic test in `tests/test_fern_ci.py` runs the actual
installer as the container worker UID through permission failure, repair and
retry. Native Windows selection excludes this POSIX test explicitly. The
project-script agent cases separately exercise model command selection and scope.
Native custom-agent loading, effective project configuration and Cloud
publication/new-task discovery remain manual host checks, described in
[Setup Fern examples](../examples/setup-fern.md).

[skills-hash-selection]: https://github.com/vercel-labs/skills/blob/7407f3893ad4dceab546ac002c3ef806e4000c73/src/add.ts#L2099-L2121
[skills-content-hash]: https://github.com/vercel-labs/skills/blob/7407f3893ad4dceab546ac002c3ef806e4000c73/src/local-lock.ts#L145-L184

## Native Windows CI

The [Windows runner](../scripts/windows_ci.py) discovers the same non-engine
test modules as the Linux `checks` suite, including future modules. It covers
package and link hygiene, Windows paths, PowerShell helpers, mocked client
protocols, installation helpers, planners, launchers and the behavior harness.
The PR workflow always requests this job; it is not conditional on Godot
changes. The affected workflow relies on that independent PR check. Full
validation also calls it, and the reusable workflow supports manual dispatch.

The job uses `windows-2025`, Python 3.11, Git, Node, PowerShell 7.2+ and the pinned
`requirements-dev.txt` dependencies. It runs from the checkout root:

```powershell
python -m scripts.windows_ci --output "$env:RUNNER_TEMP/windows-regression"
```

The output must be a new directory outside the checkout. Exact POSIX/Linux
test IDs are excluded before execution and recorded with reasons; they run
in Linux Docker. Windows junction and symlink regressions must be present
and execute. Any remaining skip, missing required case, import error, failed
assertion or empty selection fails the Windows job. The two real Blender
modules stay in the separate engine check. No engine, live client discovery,
installation into a user profile or model call runs in this Windows suite.

The job uploads the test log and structured summary, including selected
modules, platform exclusions, counts, source revision and runtime versions.
The hosted image is Windows Server and normally runs as administrator; this
does not establish Windows 11 desktop behavior or ordinary-user permissions.
Those remain separate acceptance procedures. Local Docker results do not
replace this hosted Windows evidence, and configuring the job is not proof
that it has run successfully.

## Request actual agent execution

Model execution is explicit. For a focused affected run:

```text
python scripts/run_validation.py --layer affected --base origin/main --output /tmp/skills-agent-001 --run-agent --model YOUR_ACCESSIBLE_MODEL
```

For one or more exact cases:

```text
python scripts/run_validation.py --layer full --check agent-behavior --case agents-review --case docs-schema --output /tmp/skills-cases-001 --run-agent --model YOUR_ACCESSIBLE_MODEL
```

Set `CODEX_API_KEY` in the launching process's environment;
`OPENAI_API_KEY` is accepted as an alias by the launcher. Supply an accessible
model explicitly. The launcher forwards the selected credential, not the
host's saved ChatGPT login. Missing credentials or model fail a requested
agent run. The CLI's support for a local model provider does not by itself
make this runner support Ollama or LM Studio; that connection needs its own
implemented provider and endpoint configuration.

In CI, use the runtime workflow's trusted opt-in agent path or manual input.
The full workflow runs on its weekly schedule, manual dispatch and releases.
Its scheduled/release agent path requires `AGENT_EVAL_ENABLED` set to `true`;
manual dispatch uses its model-run input. Model jobs are sharded by skill so
case groups retain independent results and artifacts. Configure the
`CODEX_API_KEY` secret and a manual model input or explicit
`AGENT_TEST_MODEL` repository variable. The `run-agent-evals` PR label
requests the trusted same-repository behavior path; fork or missing-secret
restrictions must remain visible in the report.
Do not expose credentials to untrusted PR code. Ordinary PR checks and
prompt-free runtime checks need no API key.

Each selected case gets a fresh worker; later requests for that case resume
its session only after the preceding response. The worker receives the copied
skill and fixture inputs, with evaluator criteria and baseline evidence kept
outside its readable workspace. The ordinary-task negative control receives
its project context without the skill body. Explicit skill delivery exercises
execution after invocation; it does not establish natural discovery or
automatic selection.

The independent evaluator assesses actual replies, actions and file outcomes.
Deterministic invariants also reject unauthorized changes, missing required
changes and source/case drift. Evaluator agreement alone does not establish
correctness. Retain intermediate snapshots for multi-turn and retry cases,
including the real Linux permission-denial/retry fixture.

Use [behavior-checks.md](behavior-checks.md) for exact case IDs, special
delivery
rules, manual assessment and live Git procedures. The old
`scripts/run_fern_validation.py --suite checks|install|behavior` entrypoint
remains a Fern-specific compatibility interface. Use the unified launcher for
repository-wide selection.

## Read results honestly

| State | Meaning |
| --- | --- |
| `passed` | The check executed and met its assertions for the recorded source, fixture, client and model |
| `failed` | An executed check or criterion did not meet its assertions |
| `error` | Input, setup, timeout, tool or evidence collection prevented a valid result |
| `skipped` | A test explicitly declined execution; record its reason and missing coverage |
| `not_run` | A planned check or model case was not requested or could not be started; it supplies no passing evidence |
| `partial` | The aggregate has incomplete coverage, such as planned model cases left unrequested or platform-only skips |

A requested check whose prerequisite is absent fails instead of silently
becoming a successful empty run. Platform-specific skips still identify
uncovered platform paths. Linux Docker reports the Windows junction test as
skipped; the separate Windows CI job runs all non-engine modules and rejects
every runtime skip. It records exact POSIX/Linux case exclusions before
execution; Linux runs those cases. Its evidence does not erase the Linux skip
record.
A no-model run keeps planned agent cases `not_run`;
report that partial coverage even when its deterministic and runtime checks
pass. The outer summary distinguishes `passed`, `failed`, `partial` and
`not_run`;
detailed reports also expose setup errors and test skips. The separate
`coverage_status` distinguishes incomplete coverage from completion of the
selected checks: a focused run can pass while manual or unrepresented
scenarios remain uncovered. A partial no-model
run may exit successfully so credential-free CI remains usable, while its
summary still exposes missing model coverage. Do not describe a scheduled
workflow as a model regression run unless its agent steps actually executed.
Job success and artifact existence alone are insufficient.

Keep the output root's `plan.json`, `summary.json`, `summary.md` and source
manifest. Each launched check has a directory containing launcher evidence, a
source manifest and `evidence/summary.json` with its detailed reports. Retain
commands, exit codes, test counts and skip reasons. For discovery, retain
actual client versions and per-skill reports. For installation, retain resolved
public source revisions and copied-file comparisons. For behavior, retain
case/source hashes, actual transcripts, tool events, evaluator assessments,
per-turn snapshots and `evidence/trials/<case>/result.json`. Use the output's
summaries to locate the detailed reports; build failures may leave only launcher
evidence. Unrequested model checks and preflight failures appear only in the
root summary when no container was launched.

Report the requested and exposed runtime model/version, or state when the
runtime model is unavailable. A pass on a small local model or one hosted
model applies to that model and fixture; it does not establish another
model's behavior or statistical reliability. A before/after comparison needs
equivalent requests, fixtures and runner settings with separate evidence.

## Coverage that still needs a separate procedure

These are remaining evidence boundaries, including skills without executable
agent cases. Adding them to the full plan does not create an automated test.

| Area | Available automated evidence | Separate evidence still needed |
| --- | --- | --- |
| Skill packages and client support | Static package checks and real prompt-free listing | Natural selection, invocation-policy parity and fresh-chat host loading |
| Fern setup | Resource parsing, fixture behavior, snapshot installation and discovery | Native custom-agent spawning and user-instruction loading, Windows ACL handling and real producer-to-consumer handoff |
| Godot collection | Fake-process PowerShell helper regressions and package discovery | Real Godot import/build/runtime, editor/MCP operations, scene/resource behavior, UI and playtesting |
| Blender collection | Pure component geometry and background creation/audit regressions | Reference fidelity, render/visual quality, character deformation and editor/MCP workflows |
| Image prompt skills | Text fixture behavior for the shared prompt core | Real image observation, entry-skill routing, generated images and asset acceptance |
| Commit and delivery workflows | Read-only message/plan fixtures and synthetic delivery checks | Live staging, hooks, configured signing, intermediate commit builds and external PR/CI delivery |
| Other workflow skills | Eligible synthetic cases listed by the planner | Unrepresented requests, client-specific tools, real external services and human acceptance |

Run those procedures only within the user's authorized fixture or project
scope. Preserve their own artifacts and report them alongside the automated
layer result. Background engine checks, model judgments and screenshots do
not replace human acceptance of quality, comprehension, balance or usability.
