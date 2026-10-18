---
name: setup-fern
description: Apply Fern's bundled configuration, custom agents and instructions to a Codex project, or check alignment without writes.
---

# Setup Fern

Use the bundled [installer](scripts/install.py) for explicitly requested project
setup or updates. Reading or editing this package does not authorize applying it.

1. Identify the project directory. Compare existing `AGENTS.md` rules outside
   the Fern block with the bundled [rules](assets/codex/user-instructions.md).
   Resolve actual contradictions before applying; preserve unrelated text.
2. Run `python /path/to/setup-fern/scripts/install.py --project /path/to/project`.
   Add `--check` for a read-only comparison. Read [usage](references/installation.md)
   for prerequisites, destinations and merge behavior.
3. Read the JSON results and exit status. Report changed, unchanged, missing or
   different resources and any errors with their actual paths. Do not convert
   a check into an installation or bypass malformed content or linked targets.

Bundled values replace selected config keys, same-name custom agents and the
Fern instruction block. The user's other fields, files and text remain intact.
Limit work to the requested project; do not install skills or providers, change
user profiles or approvals, commit changes or publish an environment implicitly.

File application does not prove effective host settings, custom-agent loading
or model access. Report those separately and verify them when requested.
