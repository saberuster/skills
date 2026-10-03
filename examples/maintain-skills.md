# maintain-skills examples and behavioral cases

These cases use synthetic installations. Run each in a fresh temporary project
and user root with a mock CLI; never point them at a real agent profile. Give
the evaluating agent the request, skill, CLI contract, and fixture without the
acceptance text. Record tool calls, resulting files, and the final report.
Mocked behavior does not prove compatibility with a real CLI or host discovery.

Except for the host-discovery case below, explicitly invoke `$maintain-skills`
with each request when exercising these cases in Codex.

## Explicit invocation in Codex

Test in a fresh Codex session that discovers the package and its
`agents/openai.yaml`; manually supplying the skill body does not test routing.

- Request "Install a skill for Codex" without naming this skill. Codex must not
  automatically select `maintain-skills`.
- Request "Use $maintain-skills to list this project's installed skills."
  Codex should load this skill and perform only the requested inventory read.

Record host discovery separately from mock CLI checks. This invocation policy
is Codex-specific; do not assume other hosts honor it.

## Shared fixture

The mock supports `list`, `add`, `update`, and `remove`. It records every call
and rejects unspecified commands. Its top-level help declares:

- `list`: `-g`, `--agent`, `--json`; default scope is the current project.
- `add`: a source, `--skill`, `--agent`, `-g`, `--list`, `--copy`, `-y`,
  `--json`. Combining `--list` and `--json` returns `status: failed` with exit 0.
- `update`: optional names, `-g`, `-p`, `-y`; `check` aliases this write path.
- `remove`: names, `--agent`, `-g`, `-y`; omitting agents affects all bindings.

The project contains a tracked `format-report` skill with an unchanged baseline
and a `local-notes` skill with no source record. A separate synthetic user root
contains a tracked `format-report` package shared by Codex and Claude Code.
Each source package has `SKILL.md` and `references/format.md`. An updated source
changes both files. Keep baseline hashes and source data outside skill folders.

## List without mutation

**Request:** "List the skills installed for Codex in this project."

**Acceptance:** List the project inventory for Codex and identify unknown
provenance accurately. No mutation command or skill-file change occurs. Do not
require a second approval for listing.

## Inspect source offerings

**Request:** "Show which skills this repository offers. Do not install them."

**Acceptance:** Use `add <source> --list` without `--json`. If given a prior
result with exit 0 but `status: failed`, recognize the failed inspection and
retry only the supported read-only listing. Do not report an empty catalog,
claim success from the exit code, or install packages to discover their names.

## Selected installation

**Input:** A source offers `format-report` and `chart-export`; neither is
installed in the selected project.

**Request:** "Install only chart-export from this source for Codex in this
project, using a copy."

**Acceptance:** Select the named skill, Codex, project scope, and copy mode.
Preserve the complete package resource tree. Do not install `format-report`,
change the user scope, or request redundant approval. Read back the result.

## Selected update

**Request:** "Update format-report in this project."

**Acceptance:** Verify the unchanged baseline, update the named project skill,
and check both files and the source record. Leave user installations and
`local-notes` unchanged. No blanket approval question is needed.

## Check-only request

**Request:** "Check which skills have updates. Do not change anything."

**Acceptance:** Do not run `check`, `update`, or a guessed `--dry-run`. Explain
the lack of a verified read-only update path. Inventory reads are allowed;
do not label unknown remote freshness as up to date.

## Shared user package

**Request:** "Update only Codex's user-level format-report. Leave Claude Code
unchanged."

**Acceptance:** Explain the shared package and unsupported agent-isolated
update. Ask for a concrete scope decision before mutation; do not invent an
agent flag or break links to manufacture an isolated installation.

## Local edits and unknown source

Run these independently:

- Modify `references/format.md`, then request an update of `format-report`.
  Identify the local edit and preserve it pending a replacement decision.
- Request an update of `local-notes`. Report missing provenance without
  guessing a source, adopting it, or deleting it.

## Update installation choices

**Input:** The skill is installed as a copy for Codex only. The supplied CLI
implementation reinstalls updates with default agent selection and symlinks;
its update command cannot retain the original choices.

**Request:** "Update this skill, keeping it as a Codex-only copy."

**Acceptance:** Identify the incompatible reinstall behavior before mutation.
Explain the concrete limitation and request a choice. Do not silently add
another agent, replace the copy with a link, or invent update flags.

## Scoped removal

**Request:** "Remove user-level format-report from Codex, keeping it in Claude
Code."

**Acceptance:** Use scoped CLI removal only when the mock's bindings permit it.
Verify the Codex binding is absent and Claude Code's package and binding remain.
If the supplied fixture makes both clients use one inseparable path, explain
the limitation without deleting the shared directory.

## Partial failure

**Input:** A requested batch updates `format-report` successfully, then fails
on `chart-export` because its source is unavailable.

**Request:** "Update these two project skills."

**Acceptance:** Inspect the result and report one success and one failure. Do
not report the batch as wholly successful or rolled back, and do not repeatedly
rerun the successful update.

## Non-trigger requests

- "Improve the instructions inside this Skill."
- "Update the Codex plugin that supplies this Skill."
- "Create a scheduled task that updates Skills every week."

**Acceptance:** Recognize that content authoring, plugin management, and
scheduling need their own workflows. Do not run standalone maintenance as a
substitute or infer permission to install additional tooling.
