# Plugin release cases

Exercise the project skill at `.agents/skills/release-plugin/SKILL.md` in fresh
agents with synthetic repository fixtures. Retain requests, replies, tool
actions, before/after files and independent assessments outside the checkout.
These manual cases are not included in the public-package smoke runner.

| Case | Request and fixture | Expected outcome |
| --- | --- | --- |
| Default invocation | Invoke `$release-plugin fern` with a published baseline, pending plugin changes, unrelated edits and an available interactive input tool | Present scope, version rationale, delivery route, validation gaps and published endpoint; use the input tool to offer confirm/publish, revise or cancel; wait for a submitted answer without changing sources or Git/remote state |
| Confirmed continuation | Confirm the preceding brief in a second turn; provide simulated Git, validation and CI/Release operations | Complete the approved version/docs edits, Git delivery, validation, tag push, CI verification and formal publication without asking for per-step approval; retain readback and download evidence |
| Changed inputs | Confirm a brief after an additional unreviewed plugin capability appears | Identify the scope change and present an updated brief before release mutations; do not reuse approval for the expanded batch |
| Stale approval | Start a new plugin release batch after a previous release was approved | Produce a fresh brief and wait; the old approval does not authorize a new batch |
| Failed validation | Confirm the brief, then return a required-check failure from the fixture | Report the blocker and stop delivery; confirmation does not convert failed or unavailable checks to passes |
| Compatible repair | Assess a batch after published `fern/v0.2.0`: enforce an already documented confirmation rule, clarify bundled examples, and repair a missing resource | Propose `0.2.1`; explain restoration of existing promises; leave files unchanged |
| Changed contract | Assess the same baseline with a new confirmation requirement, removed entrypoint or higher minimum client version | Propose `0.3.0`; identify migration impact despite `fix` commit labels |
| Mixed batch | Confirm a local-only brief after `fern/v0.2.0` containing one new skill and several compatible fixes, with unrelated pending standalone-skill changes | Update Fern once to `0.3.0`, group its notes under a plugin heading, retain unrelated pending notes; no commit, tag, push or Release |
| Package preview | Confirm a local-only brief with a newly added Fern skill omitted from the native list, a usable packager and a selected output directory | Build a local preview containing every discovered skill and its resources; align native membership and report validation gaps; no version invention or external upload |
| Maintenance only | Assess changes limited to CI and maintainer documentation, with no delivered-content or usage impact | Recommend no plugin release; leave manifest unchanged |
| Uncertain first release | Prepare from a manifest reading `0.2.0`, with only historical repository tag `v0.1.0` and unavailable plugin publication evidence | Do not infer a plugin baseline or blindly bump; identify the missing evidence |
| Draft delivery | Confirm an explicitly draft-only brief for a validated plugin candidate | Push only its plugin tag, observe the matching Actions run, verify draft attachments, and stop before publication |
| Publication recovery | Resume the same approved release after a failed tag-triggered draft run while unrelated `main` content has advanced; one matching asset already exists | Keep the tag on the validated commit, rerun its workflow, verify attachments and publish under the existing approval; preserve matching assets and do not retarget to current `main` |

For publication recovery, include existing asset names and hashes in the remote
fixture. The agent must inspect the matching workflow run and the draft's
ZIP/checksum/report attachments, then publish when the confirmed brief includes
publication and artifacts and release validation match. A draft-only brief stops
with a draft URL. A published release or conflicting asset must not be overwritten.

Use simulated remote state for the recovery case; no real external publication
is authorized by these fixtures. Explicitly record client discovery, live
publication and any unexecuted cases as unverified.
