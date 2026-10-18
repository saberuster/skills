---
name: codex-config
description: Inspect, change, and verify Codex configuration, including conflicting overrides and missing tools.
---

# Codex Config

Keep diagnosis read-only, including backups and receipts. A clear setting
change authorizes that scoped edit; clarify only unresolved scope.

1. **Identify the target.** Establish the client/runtime version, effective
   Codex home, project, and persistence scope. Desktop may use a different
   runtime from the terminal CLI. Read relevant fields only; redact secrets.
2. **Check support and precedence.** Confirm the key and allowed values against
   target-bound schema, documentation, or implementation. Trace overrides and
   managed requirements. Leave unsupported or unresolved settings unchanged;
   do not write forbidden values or alter policy or other layers to force an
   edit to take effect.
3. **Apply the requested change.** Use a supported temporary override for a
   one-run request. For file edits, resolve links within scope, re-read and
   parse TOML, and back up exact original bytes before writing (record absence
   for a new file). Preserve unrelated settings, comments, permissions, and
   concurrent changes with the smallest lossless edit. Parse and read back the
   result. On failure, inspect and retry unfinished work; restore only while
   current bytes still match your edit and restoration is within scope.
4. **Verify the outcome.** Report the layer, key, before/after values, controlling
   overrides, checks, and gaps. Distinguish saved content, effective values,
   tool exposure, successful calls, and native UI display. Check the target's
   reload requirements and runtime behavior when available; keep unperformed
   checks pending. A successful parse does not prove a running chat loaded it.

For source selection, layering, or missing-tool diagnosis, read
[configuration evidence](references/configuration-evidence.md). Use
`openai-docs` when available or official sources when more evidence is needed;
retained versioned evidence can suffice.

Keep edits within configuration scope. Ad hoc changes do not adopt Fern
ownership or update receipts. When called by `setup-fern`, follow its baseline,
conflict, backup, and receipt rules, and return successful per-key readback.
