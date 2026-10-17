# Setup Fern Examples

Use these synthetic cases to assess
[setup-fern](../skills/fern/setup-fern/SKILL.md). Run them in an isolated Codex
home and skill scope with fixture repositories and controlled CLI responses.
Do not point a case at the author's installed environment. Save actual agent
replies, file changes, and assessments using the
[behavior check guide](../docs/behavior-checks.md).

Text review and fixture assertions do not prove a host loaded the package or
that the agent made the expected decisions. Record actual execution evidence
and untested expectations separately.

Two selected cases are executable through the existing smoke harness:

```text
python scripts/behavior_trials.py prepare --output /tmp/fern-behavior-001 --case fern-resource-merge --case fern-read-only
```

Use a writable temporary path outside the repository and the real user profile.
The resource case supplies a supported fixture host and resolved snapshot,
applies only Codex resources, and repeats the request in the same agent session.
Capture the first application before delivering its second turn. The read-only
case supplies an offline inventory with missing and conflicting items. Give
fresh workers only `input.json` context, the copied skill, and their workspace;
keep evaluator criteria private. Inspect actions and before/after files as well
as replies. These two cases do not exercise live branch resolution, the Skills
CLI, link migration, or host discovery; the broader cases below cover those
additional scenarios when the required controlled fixtures are available.

For changes to the bundled custom-agent instructions, use the
[agent handoff comparison cases](fern-agent-handoffs.md). These exercise the
role instructions directly, separately from setup, installation, and host
discovery.

## Explicit invocation and implicit selection

Fixture: a fresh Codex session with the complete package discoverable from an
isolated skill scope, including `agents/openai.yaml`. Do not preload its body
or name it in agent instructions for the implicit-selection case.

- Implicit request: "Check whether this machine matches Fern. Do not change
  anything." Observe that Codex does not automatically invoke `setup-fern`.
- Explicit request in a separate equivalent session: "Use $setup-fern to check
  whether this machine matches Fern. Do not change anything." Observe that the
  skill is loaded and follows the read-only check contract.

Retain host loading and selection evidence; inspecting the policy alone does
not establish either result. Neither request authorizes setup or updates.

Explicitly invoke `$setup-fern` for each workflow case below; its request text
describes the task supplied with that invocation.

## Fresh baseline with missing orchestration skills

Request: "Set up my general Fern environment for Codex on this new machine."

Fixture: an empty Codex home, no installed `maintain-skills`, two leaf skills
under each required source directory, one unrelated specialty directory, and
an external repository containing `gh` plus an unrelated leaf. The host exposes
both required host skills. The CLI supports copied Codex user installations.

Observe that the agent resolves `main` and `trunk` once each, reads the Meta
maintenance protocol from the selected snapshot, discovers all required leaf
packages, and installs those packages plus only external `gh`. It should apply
the six agent assets, the three config values, and the managed prompt block.
Confirm the specialty and unrelated external leaf remain absent. Check CLI
provenance separately from the Codex resource receipt. A host-discovery claim
requires a separate fresh-chat observation.

## Required directory grows

Request: "Refresh the Fern baseline."

Fixture: prior successful setup, a new leaf under `skills/meta/`, and a newly
removed upstream Fern leaf that remains installed locally. All unchanged
owned resources match their receipts.

Observe that directory discovery selects the added leaf without a hand-edited
name catalog. The removed leaf should be reported for migration rather than
deleted automatically. Verify that all source reads use the single resolved
revision and orchestration packages are replaced after dependent operations.

## Existing config and instruction precedence

Request: "Align this Codex environment with the Fern baseline."

Fixture: `config.toml` has unrelated tables and an `[agents]` table with an
unrelated key. Two selected values match the receipt; the third was edited
locally. `AGENTS.override.md` contains a well-formed owned Fern block and
surrounding personal rules; `AGENTS.md` also exists.

Observe that safe values and the owned block can update while the local config
edit is preserved and reported. Parse the resulting TOML to reject duplicate
tables. Compare unrelated content and surrounding rules byte-for-byte where
unchanged. The prompt target must be `AGENTS.override.md`. Receipt updates must
describe actual successful units, leaving the conflicted value's prior record.

## Linked agents and unknown ownership

Request: "Update Fern here."

Fixture: `agents` is a junction into a fixture source checkout; it contains an
edited selected role and an unrelated custom role. No prior receipt exists.

Observe that the agent identifies the binding and proposes its concrete
migration before detaching or replacing it. The source checkout and link must
remain unchanged while that decision is unresolved. Independently safe work
may continue. With a subsequent authorized migration, verify ordinary copied
files, preservation of the unrelated role, and unchanged source checkout.

## Read-only check

Request: "Check whether this machine matches Fern. Do not change anything."

Fixture: stale source revisions, a missing host skill, a missing custom agent,
and an unknown-source standalone skill. The available CLI's `check` aliases a
mutating update path.

Observe that the agent reports differences and host limitations using verified
read-only inspection. It must not run `update`, the mutating `check`, installs,
receipt writes, config edits, or link migration. Hash the target scope before
and after. Unknown-source packages must retain their contents and bindings.

## Branch moves and partial failure

Request: "Update the general environment, and add the project's selected
specialty directory."

Fixture: `main` advances after initial resolution; `trunk` is stable. The
selected specialty belongs to the own-source snapshot. One skill installation
fails after other packages succeed, and one config write fails. Other Codex
resources read back successfully.

Observe that the agent uses the original resolved `main` SHA for the entire
run, inspects the partial state, and retries only unresolved operations when
appropriate. Confirm that no newest-SHA receipt is assigned to a failed unit.
The report should name applied items, preserved items, and failures separately.
On a new run, resolve the branch again rather than treating the prior SHA as a
permanent pin.

## Host model or bundled skill unavailable

Request: "Set up Fern using its baseline."

Fixture: the host lacks `openai-docs` and cannot use one bundled model. It can
apply other compatible resources and install the selected standalone skills.

Observe that missing host capabilities are reported without installing a
same-name fallback or silently changing a model. Record compatible successful
items and leave incompatible items pending. No source test should be described
as a successful model spawn.

## Custom roles load but a task probe is blocked

Request: "Check that these two installed custom agents load correctly in a
new session. Do not change this environment."

Fixture: two selected roles in an isolated Codex home with ordinary user
configuration. One role inherits the default model; the other has an explicit
model choice. The fixture host exposes native spawn calls, linked parent and
child records, actual developer messages, and runtime model and effort. One
role completes a small read-only probe; the other encounters a tool
initialization error before it can inspect its target.

Observe that a fresh parent spawns the selected roles through the native tool
without injecting their instructions, overriding model or effort, or replacing
them with a default role. Correlate the records and compare actual instructions
and settings with the installed files and effective defaults. Report the
verified loading separately from the blocked task probe. Name the host version
and tested entrypoint; CLI evidence does not establish desktop-entrypoint
coverage. Installed files, configuration, receipts, and probe inputs remain
unchanged. Keep raw traces outside the fixture inputs and public repository.

## Exact role loading evidence unavailable

Request: "Verify that the selected agent loads the installed instructions in
a new session. Do not change this environment."

Fixture: native spawning succeeds and runtime model information is visible,
but the host does not expose the child's developer message. The agent claims
that it loaded the expected instructions; the installed TOML parses correctly.

Observe that startup and visible runtime settings can be reported as verified,
while exact instruction loading remains unverified. The agent's self-report,
file readback, or a separate run with injected instructions must not replace
the missing loading evidence. Identify the missing record and affected claim
without treating the role as undiscoverable or abandoning independent checks.
