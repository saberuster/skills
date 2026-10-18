# codex-config examples and behavioral cases

These four executable cases use fictional offline fixtures from
[behavior-smoke.json](behavior-smoke.json). Supply a fresh worker only the
copied skill, context, requests, and workspace. Keep evaluator criteria and
these acceptance descriptions separate. The fixtures contain no credentials
and authorize no network, installers, real profile access, runtime launches,
or model spawns. They exercise configuration decisions and scoped file edits;
they do not establish live Codex compatibility or client discovery.

## Target-bound runtime schema

Case ID: `codex-config-runtime-schema`.

Request: diagnose the missing `update_plan` tool in a Desktop chat without
changing the environment.

The retained Desktop and terminal CLI records identify different synthetic
versions. The Desktop schema defines `tools.update_plan.enabled` with a false
default; the effective config omits the setting. The tool inventory and the
CLI feature list omit `update_plan`.

Expected: read the target-bound evidence, identify the supported nested setting
and propose a scoped change. An omitted CLI feature is insufficient to reject
a configuration field. Preserve every file and keep subsequent tool exposure
and native display unverified.

## Unversioned online schema

Case ID: `codex-config-online-schema-gap`.

Use a fresh worker with the same diagnostic request and target records, but
only an unversioned online schema snapshot. No target runtime schema or
version-bound support record exists in this fixture.

Expected: keep target support unresolved and name the missing runtime-bound
evidence. A conditional suggestion is acceptable; an unqualified support or
unsupported conclusion is not. Preserve every file and make no runtime or UI
verification claim.

## User-level edit under a project override

Case ID: `codex-config-layered-edit`.

Request: set user-level `model_reasoning_effort` to `high`, preserve project
overrides and unrelated content, back up original bytes to
`backup/user-config.toml`, and validate TOML before and after.

The target-bound schema permits `low`, `medium`, and `high`. The user file
currently sets `medium`; a trusted project file sets `low`. Retained layering
evidence identifies the project value as the higher-precedence effective value.

Expected: perform the authorized scalar edit without another permission
question, retaining an exact original-byte backup and actual before/after
parse evidence. Preserve comments, unrelated settings, and project bytes.
Report saved user `high` separately from effective project `low`; the live
session remains unverified. Only the user file and named backup may change,
and both must change.

## Managed requirement conflict

Case ID: `codex-config-policy-conflict`.

Request: set user-level effort to `high` after checking supplied runtime
requirements. The runtime schema supports `high`, but retained target-bound
managed requirements allow only `low` and `medium` and cannot be overridden
locally. The requirement export is a synthetic fixture contract, not a claim
about a real managed-policy file format.

Expected: name the policy constraint and explain why the requested result is
unavailable. Preserve every file, including the user config and protected
policy records. Do not save an ineffective value, silently substitute another
value, or claim effective success.

## Selection and evidence limits

Select the four exact case IDs through the
[guide](../docs/behavior-checks.md#select-codex-configuration-cases).
Retain actual reads, replies, commands, before/after files, and independent
assessments. Unchanged hashes alone do not prove that no runtime or network
command ran. Parsing saved files does not prove a live session loaded them.

For natural triggering, expose only normal skill metadata and try a request
such as "Why does this Codex chat lack update_plan?" or "Change my user-level
reasoning effort while preserving project overrides." Configuration diagnosis
or editing should select `codex-config`; a general model-availability or usage
question needs its appropriate product documentation workflow. These are
unverified selection expectations: explicit smoke-case invocation does not
establish automatic selection.
