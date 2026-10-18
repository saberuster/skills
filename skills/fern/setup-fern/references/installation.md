# Project setup

Run the complete installed package with Python 3.11+; the installer uses only
the standard library and bundled assets. Local Codex and Codex Cloud use the
same command, with an explicit existing project directory:

```sh
python3 /path/to/setup-fern/scripts/install.py --project /path/to/project
```

On Windows use `python` and the actual paths. Add `--check` to compare without
writing. JSON results describe each resource; missing or different values make
a check return nonzero. Apply mode returns nonzero on errors.

## Bootstrap

If needed, obtain the complete skill package separately:

```sh
npx --yes skills@1.7.0 add https://github.com/saberuster/skills/tree/main/skills/fern/setup-fern --skill setup-fern --agent codex -g --copy -y
```

Use the destination reported by the CLI. This bootstrap requires Git, Node.js
and npx; the Python installer does not install or update skills.

## Destinations and merge rules

| Bundled resource | Project destination | Behavior |
| --- | --- | --- |
| `assets/codex/config.fragment.toml` | `.codex/config.toml` | Bundled selected keys replace existing values; other fields and comments remain |
| `assets/codex/agents/*.toml` | `.codex/agents/` | Copy six named agents, replacing those names and preserving unrelated agents |
| `assets/codex/user-instructions.md` | Root `AGENTS.md` | Append or replace one marked block, preserving surrounding text |

Create missing config files and tables. Prepare all selected config changes
in memory, validate them, then write the config once. A preparation failure
leaves that file unchanged; other resource files may already have completed.
Repeating setup leaves aligned bytes and modification times unchanged.
No receipts or backup records are needed or created.

Use one well-formed instruction block:

```markdown
<!-- fern:user-instructions:start -->
<contents of assets/codex/user-instructions.md>
<!-- fern:user-instructions:end -->
```

Invalid TOML, unsupported syntax that cannot be preserved, ambiguous markers
and linked write targets are reported for correction. The script checks each
target and its ancestors, leaving unrelated linked files alone. It replaces
changed files atomically and reads back the result.

`AGENTS.override.md` remains untouched; it may shadow root `AGENTS.md` in the
host. File writes do not establish effective configuration, custom-agent/model
availability or instruction loading. Verify these in the intended host when
requested. Codex Cloud publication and loading in a new task are separate
from project file setup.
