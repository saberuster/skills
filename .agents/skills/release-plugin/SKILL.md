---
name: release-plugin
description: Review a plugin release brief, then execute the confirmed release through publication using this repository's plugin-only version policy.
---

# Plugin Release

Use `skills/<plugin>/.codex-plugin/plugin.json` and that plugin's release
history. Fern is the current plugin. This is a project maintenance
skill, not a member of the Fern plugin.

## Release policy

- Version plugins only. The plugin manifest is the version source; do not add
  repository or individual skill versions. Keep historical repository tags.
- Use `main` for development and installation. Accumulate changes and bump once
  per release batch, not per PR. Identify unreleased snapshots by commit SHA;
  a manifest version on `main` alone does not establish a published release.
- For `0.x`, apply the highest impact in the batch:

  | Impact | Rule | Examples |
  | --- | --- | --- |
  | Minor | Add capabilities or change the usage contract, including incompatible changes | Add/remove/rename a skill; change default workflow, output contract, permission scope, or minimum environment requirements |
  | Patch | Restore an existing promise or improve it compatibly | Fix ignored constraints, clarify instructions, improve reliability, repair packaging, or correct bundled text and links |
  | No release | Change only repository maintenance without affecting delivered plugin content or usage requirements | CI, tests, or maintainer documentation |

  Judge actual effects, not diff size, file type, or commit prefix. Making an
  existing confirmation rule work is a patch; introducing that rule is a minor.
  Reset patch to zero for a minor bump. Document incompatible changes and
  migration steps even before 1.0. Establish a stable compatibility policy before
  moving to 1.0; do not invent that commitment during routine release work.
- Use plugin tags such as `fern/v0.3.0`. A tag and its published content stay
  fixed; corrections require a new release. Other plugins version independently.

## Review first

By default, `$release-plugin <plugin>` inspects read-only and presents a
concise brief, then waits for the user's confirmation. Build previews only
after confirmation; do not edit sources or mutate Git/remote state before it.
The default endpoint is a published GitHub Release. Creating or editing this
skill is not a release request. Honor explicit assessment-only, local-only or
draft-only requests.

Ask questions through requestUserInput (the host's supported interactive input
API, such as `request_user_input_async`). For brief review, offer concise choices
such as confirm and publish, revise the brief, or cancel; name the approved
endpoint in the confirmation choice. Wait for an explicit submitted answer;
a preselected option, timeout or silence is not confirmation. Use a text question
only when no suitable input tool is available in the current mode.

Read the plugin manifest, published release history, branch/HEAD and pending
changes, including bundled resources. Compare against the last published tag
and its exact commit; reconcile reverts and duplicate notes. The current
manifest or an old repository tag does not prove a plugin release. Establish
whether the version has shipped before choosing a first-release baseline.
Report missing evidence or no release-worthy changes instead of guessing.

The brief must identify:

- Repository/plugin, published baseline tag and commit, current HEAD and the
  inspected pending changes; distinguish included work from unrelated edits.
- Proposed version with minor/patch rationale, concise release notes and any
  migration impact.
- Planned version/docs edits, commit and route into `main`, tag push, CI draft
  and final publication, or the explicitly requested narrower endpoint.
- Completed and pending checks, blockers and evidence gaps. The final release
  SHA may be pending; approval covers the reviewed content and planned edits.

Confirmation authorizes the stated steps through the brief's endpoint. Continue
without asking again for each edit, commit, merge, push, tag or publication.
Reuse confirmation only for that same brief, not a later release batch. Before
execution, recheck the approved inputs. Material changes to included content,
version, delivery scope or endpoint require an updated brief and confirmation;
normal approved edits and their resulting commit SHAs do not. An unrelated
advance of `main` does not change the approved plugin content. Stop and report
required-check failures or unavailable evidence; approval does not waive them.
On retry, inspect existing progress and resume only incomplete approved steps.
If already published, verify that release without rebuilding or replacing it.

## Execute the confirmed brief

1. Apply the approved version once and organize `CHANGELOG.md` under a heading
   such as `fern 0.3.0 - YYYY-MM-DD`. Preserve unrelated pending notes and
   historical entries. Keep native plugin membership aligned with its skills.
   Build a local preview for the selected plugin in a fresh output directory;
   discover all plugin skills dynamically. For example:

   ```text
   python scripts/package_plugin.py --plugin fern --output-dir dist/preview
   ```

2. For a local-only endpoint, run its approved local checks and stop before
   Git delivery. Otherwise follow Git/PR requirements and configured signing.
   Commit the approved changes using Conventional Commits and integrate them
   into
   `main` as required by the approved route; preserve unrelated edits and
   branch protections. Bind the final candidate to an exact commit. Follow
   `docs/validation.md` and `docs/behavior-checks.md`, run full validation for
   that revision and inspect retained behavior evidence before delivery.
   Reassess affected evidence if the candidate changes. Distinguish passed,
   skipped, unrequested and manual checks; a green no-model run is incomplete.

3. Inspect remote tags/releases, then create and push only the approved
   `<plugin>/v<VERSION>` tag at that validated commit. Never move an existing
   release tag or substitute a later `main` commit. Observe the matching run
   of `.github/workflows/release-plugin.yml`, which builds and uploads the
   ZIP, checksum and build report to a Release draft. Inspect failed runs and
   resume them without replacing conflicting assets or duplicating releases.
   Verify the downloaded attachments, version, commit and archive hashes.

4. For the default published endpoint, publish the verified draft using the
   existing confirmation, then read back the published state and download
   links. Stop at the draft only when that endpoint was explicitly requested.
   Read `docs/plugins.md` for CI and recovery details.

Return the version, exact commit, validation results and remaining gaps. For
remote delivery, include the tag, Actions run, Release URL and ZIP download;
state whether the result is local preparation, a draft or a published release.
