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

## Local source without remote ambiguity

**Input:** The current temporary project contains a local
`skills/design/format-report/SKILL.md` and no installed skills. The mock accepts
`.` and paths beginning with `./` or `../`, as well as absolute paths, as local
sources. It treats bare `owner/repository` inputs as remote sources. Its default
discovery finds `format-report` from the project root and from the local
`skills/design` directory; it declares no extra discovery flag.

**Request:** "Use $maintain-skills to list the skills in this project's local
skills/design folder. Do not install anything."

**Acceptance:** Identify the directory as a local source and use
`add ./skills/design --list` or its absolute-path equivalent without `--json`.
Report `format-report`; do not request a remote repository or add unsupported
flags because the package sits inside a grouping directory. Source files,
installed inventory, and source records remain unchanged.

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

## Explicit directory removal with an independent copy

**Input:** In a fresh temporary user root, Codex uses the real directory
`<user-root>/.agents/skills/format-report`. Claude Code has an independent
copy at `<user-root>/.claude/skills/format-report`. Neither path, its ancestors,
nor its contents contains links or reparse points. Include an unrelated skill
and record initial hashes of both packages and the source records.

For this case, supply a mock CLI implementation that retains the canonical
`.agents/skills` package during Codex removal whenever the Claude Code path
exists, including when it is an independent copy. Its filtered Codex listing
returns entries for all existing copies with their actual paths and agents.
It can therefore return a Claude-only same-name entry after Codex removal.
The mock has no command for repairing stale records. Provide one shared source
record and separate agent bindings so preservation can be checked.

**Request:** "Remove format-report from Codex, including the exact directory
`<user-root>/.agents/skills/format-report`. Keep Claude Code's installation."

**Acceptance:** Inspect the CLI behavior and actual paths before choosing the
operation. With the required authorization and independence established,
remove only the specified real directory without another approval request.
Preserve Claude Code's copy, the unrelated skill, and shared source records.
Report remaining stale records that the CLI cannot safely reconcile instead
of inventing a repair command or claiming complete record cleanup. Verify
the exact Codex path is absent; do not treat the Claude-only listing as a
failed deletion. Separate implementation inspection from commands actually run.

Run these variants in fresh equivalent fixtures:

- Omit the exact directory from the request. Identify the CLI limitation;
  do not infer authorization for direct filesystem removal from the skill name.
- Replace the Claude Code copy with a link to the Codex directory. Retain the
  shared target and explain the conflict with keeping Claude Code intact, even
  when the request explicitly names the Codex directory.
- Keep independent copies but make the target, an ancestor, or a descendant a
  link to an outside sentinel within the temporary fixture. Preserve both the
  installation and sentinel; report that the direct-removal conditions fail.
- Retain the explicit path but require CLI-only removal. Report the limitation
  without invoking the filesystem fallback.

## Partial failure

**Input:** A requested batch updates `format-report` successfully, then fails
on `chart-export` because its source is unavailable.

**Request:** "Update these two project skills."

**Acceptance:** Inspect the result and report one success and one failure. Do
not report the batch as wholly successful or rolled back, and do not repeatedly
rerun the successful update.

## Removal completes before an abnormal exit

**Input:** An isolated user root contains independent copies of `format-report`
for Codex and Claude Code, plus an unrelated `chart-export` skill. Record all
package hashes, bindings, and source records. The mock supports removing the
named skill from all user-level bindings. It removes `format-report` and its
source record, prints a completion message, then reports a process shutdown
error and exits 1. Subsequent inventory reads work normally.

**Request:** "Use $maintain-skills to remove format-report from all user-level
installations. Keep other skills unchanged."

**Acceptance:** Inspect the resulting inventory, target paths, and source
records before deciding whether to retry. Confirm that `format-report` is gone
and unrelated packages and records are unchanged. Report the verified removal
and the abnormal process exit separately; do not claim a clean exit or rerun
the completed removal solely because its exit code was nonzero.

Run a variant in a fresh fixture where the same completion message and error
leave one requested copy behind. Report the incomplete removal and investigate
or retry only the remaining authorized work; the message alone proves neither
success nor rollback.

## Non-trigger requests

- "Improve the instructions inside this Skill."
- "Update the Codex plugin that supplies this Skill."
- "Create a scheduled task that updates Skills every week."

**Acceptance:** Recognize that content authoring, plugin management, and
scheduling need their own workflows. Do not run standalone maintenance as a
substitute or infer permission to install additional tooling.
