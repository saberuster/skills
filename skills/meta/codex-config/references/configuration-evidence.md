# Configuration Evidence

## Select sources for the target runtime

Use session metadata, the host's runtime information, or a command explicitly
bound to the target executable to identify the version and client entrypoint.
Keep a separately installed CLI's results labeled with that CLI's version.

Prefer configuration inspection from the target runtime for effective values.
For key support and syntax, inspect its versioned schema, documented contract,
or matching implementation. Current official documentation helps locate those
sources and explain semantics; an unversioned online schema is a discovery
lead, not proof that an older or different runtime supports the field.
If sources conflict, name the version or entrypoint mismatch rather than
silently choosing the newest source. Do not invent a supported setting from
its name, a release announcement, or another client's behavior.

Read only the affected setting and source metadata. Redact secrets from
diagnostics and reports, including command output and configuration diffs.
Use supported inspection commands or APIs only after checking their
availability and whether they mutate state.

## Trace precedence and constraints

Determine which layers the target actually loads: temporary or invocation
overrides, project configuration and trust, selected profiles, user settings,
managed defaults or requirements, and built-in defaults where applicable.
Verify ordering and merge behavior for this runtime; do not hard-code a
historical precedence list or assume every field merges identically.

Resolve the effective Codex home and project directory before choosing a
file. Distinguish a requested future default from a value for the active
project or current invocation. Respect explicit scope even when another layer
still wins. Report a shadowing override without silently editing both layers.

Managed defaults and enforced requirements have different roles. Inspect the
relevant requirement when a value is rejected or constrained. A local file
change cannot by itself establish that a managed requirement has changed.

## Missing native tool example

If `update_plan` is unavailable, inspect the runtime serving that chat and
its configuration evidence, including nested `[tools]` settings. Absence from
`features list` alone does not establish lack of support; that command's
inventory is not the full configuration schema.

On a runtime whose schema defines `tools.update_plan.enabled`, compare the
effective value with its documented default. If the key is absent, the default
is false, and no higher layer changes it, enabling the setting is a supported
configuration candidate. Apply it only within the requested edit scope.
If only the online schema contains the field, target support remains unresolved
until matching runtime evidence is available.

After configuration is loaded, an exposed callable tool, a successful call,
and a visible progress component are separate observations. Do not infer the
last two from a TOML parse, schema definition, or tool listing alone.

## Official entrypoints

Consult these for the current contract, then check applicability to the target
version. They are references, not a locally pinned support matrix.

- [Config basics](https://learn.chatgpt.com/docs/config-file/config-basic):
  configuration locations, precedence, and project trust.
- [Configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference):
  keys, types, and the current schema.
- [Developer settings](https://learn.chatgpt.com/docs/developer-settings):
  runtime inspection and temporary setting interfaces.
- [Managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration):
  defaults, enforced requirements, and field-specific composition.
