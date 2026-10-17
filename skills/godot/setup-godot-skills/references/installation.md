# Installation and Updates

Use the existing Skills CLI for package files and provenance. Explicitly invoke
`$maintain-skills` when available, following its current contract. If repository
rules require it and it is unavailable, report that prerequisite without
installing it implicitly. Otherwise use the workflow below directly.
Read the available CLI version and `npx skills --help` before choosing flags.
Node.js/npm and Git must already be available; report missing prerequisites.

For Windows clone failures, inspect the original Git error: a CLI authentication
message can hide a checkout or temporary-directory permission failure. When
needed, give only the CLI subprocess a writable task-local `TEMP`/`TMP` and
`core.longpaths=true` through Git's process configuration. Preserve inherited
configuration entries and leave global settings and credentials unchanged.

## Inspect before writing

Work from the resolved installation root. Inspect the requested scope, known
source records, physical destinations, and resolved links. A user-level or
plugin-provided same-name skill is not evidence of a repository installation;
surface duplicate or shared-path effects before adding or replacing a copy.
Do not turn a request for one client into updates for other clients.

Inspect the selected upstream skill folder at its requested ref, including
metadata, references, scripts, and required companion tools. Preserve the whole
folder. If it requires resources outside that folder or an unavailable plugin
runtime without a supported fallback, report the dependency rather than
installing a whole plugin, unrelated skills, or extra tools.

Compare the current installed contents against a reliable installation baseline
before replacement, not just against today's upstream files. Use the existing
installer's content-hash algorithm when its record supports that comparison;
an upstream tree hash alone does not prove the local copy is unchanged. Missing
internal files, unrecorded manual copies, and unreadable or corrupt records
require a conflict decision. Do not infer ownership from a matching name.

## Install or refresh the selected package

Examples below run at the chosen repository root, with `<source>` replaced by
the catalog's exact remote skill URL/ref. Replace `<client>` and `<name>` with
the established targets. These are CLI examples, not shell interpolation code.

```console
npx skills list --json
npx skills add <source> --list
npx skills add <source> --skill <name> --agent <client> --copy
```

Add `--global` only for an explicit user-level target. Use `--yes` only after
resolving selection, local-content conflicts, and shared effects. Do not use
`--all`. Check command output as well as its exit status; discovery options and
JSON support vary by CLI version.

For updates, first verify that the installed CLI preserves the requested scope,
client, source/ref, and copy method. Do not assume a bare `update` does so.
When it cannot, a selective `add` from the same exact source/ref with explicit
client and copy options can refresh an unmodified copy after the checks above.
Preserve pinned refs; do not replace them with `main`. If neither operation can
honor the requested targets, report the limitation and ask for a choice.

Do not use a potentially writing `check` or `update` as a read-only probe, and
do not invent `update --agent` or `update --dry-run`. Use supported read-only
source inspection to determine whether the selected package changed. Upstream
rename, removal, or a catalog source change does not authorize deletion or
migration of the existing copy.

After each operation, verify the actual target, full contents, and resulting
source/ref record. An absent destination with an old lock entry still needs
installation. A failed source fetch is unresolved, not "already up to date."
Preserve unrelated skills and instruction content. Keep any retry scoped to
the observed remaining work; do not promise rollback unless verified.

## Tool references

- [Skills CLI documentation](https://github.com/vercel-labs/skills)
- [Maintained standalone installation
  workflow](https://github.com/saberuster/skills/blob/main/skills/meta/maintain-skills/SKILL.md)
- [Project installation
  records](https://github.com/vercel-labs/skills/blob/main/src/local-lock.ts)
- [Update
  implementation](https://github.com/vercel-labs/skills/blob/main/src/update.ts)

The linked branches are mutable. Inspect the matching installed version when
resolving tool behavior; these links are not evidence of a successful install.
