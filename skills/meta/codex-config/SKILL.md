---
name: codex-config
description: Inspect, change, and verify Codex configuration. Use for configuration questions, requested setting changes, conflicting overrides, or tools and settings that remain unavailable. Covers the effective configuration and target runtime, not skill installation, plugin lifecycle, or general application debugging.
---

# Codex Config

Resolve the requested configuration question or change against the runtime
that will use it. Keep the operation scoped to the named settings and host.

## Establish the target

- Distinguish explanation or diagnosis from an explicit change request.
  Inspection is read-only, including receipts and backups. A clear request to
  set a value authorizes that scoped edit without another confirmation.
- Identify the target client or session, its actual runtime version, effective
  Codex home, working directory, and intended persistence scope. A terminal
  CLI can differ from the runtime serving a Desktop chat. Do not infer the
  target version from an unrelated executable on PATH.
- Locate the configuration sources and applicable overrides for the selected
  setting. Inspect relevant fields rather than dumping the whole configuration
  or credentials. Resolve links before writing and confirm their targets are
  within the authorized scope.
- Use the established scope when clear. Ask only when an unresolved choice,
  such as this project versus user defaults, changes the intended outcome.

## Diagnose support and effective values

Read [configuration evidence](references/configuration-evidence.md) for source
selection, layering, and missing-tool diagnosis. Establish the requested key's
meaning, supported values, and target-version support before applying it.

Use available runtime inspection and matching schema or implementation
evidence. Consult current official documentation through `openai-docs` when
available, or directly through official sources. The skill remains usable
with retained versioned evidence; do not require a new network lookup when
the supplied evidence already resolves the question.

Trace the relevant value through overrides and enforced requirements. A saved
value can be valid yet shadowed or disallowed. Explain that distinction and
identify the controlling source. Do not edit a higher-priority source or
weaken managed requirements merely to make a lower-priority edit take effect.
If support or scope remains unresolved, preserve the affected setting and
continue independent work that is sufficiently supported.

## Apply an authorized change

1. Re-read the selected target before editing to detect concurrent changes.
   Parse existing TOML; preserve unrelated keys, comments, tables, and file
   permissions. Use a structural or lossless targeted edit, including for
   dotted keys or inline tables; do not append duplicate tables or reserialize
   the entire file if that loses unrelated content.
2. Prepare the smallest valid change to the authorized layer. For a one-run
   request, use a supported temporary override instead of making it persistent.
   If an enforced requirement forbids the requested value, report the constraint
   without writing an ineffective value or changing the policy.
3. Before replacing an existing file, retain its exact previous bytes in an
   appropriate local backup; record absence for a new file. Use a caller's
   established backup procedure when present. Keep private configuration local.
4. Apply the prepared edit and parse and read back the result. Preserve any
   edits made since inspection. On failure, inspect actual state and retry only
   unfinished work; restore a backup only when the current contents are still
   this operation's result and restoration is within scope.

An explicit ad hoc edit does not adopt Fern ownership or update its receipts.
When called by `setup-fern`, keep its selected baseline, conflict decisions,
backups, and receipt rules authoritative; report successful per-key readback
to that workflow. Do not install skills, manage plugins, change authentication,
or upgrade the host as an implicit configuration repair.

## Verify and report

Distinguish saved content, effective configuration, and observed behavior.
Report the selected layer and key, before/after values without secrets,
controlling overrides, performed checks, and unresolved evidence.

Use the target runtime's supported validation or inspection interface when
available. Establish whether this setting needs a new session, reload, or
restart; do not claim universal hot reload or restart requirements. If that
step cannot be performed, report it as pending. A parsed file or successful
command does not prove a running chat consumed the change. Verify the relevant
tool call or feature when feasible, and verify native UI display separately
when that display is the requested outcome.
