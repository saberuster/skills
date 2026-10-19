# Codex marketplace and Fern plugin

This repository is a Codex marketplace named `saberuster-skills`. Its first
plugin, `fern`, packages the eight skills maintained in `skills/fern/`.
The standalone skill sources and invocation policies remain the same.

## Source layout

```text
.agents/plugins/marketplace.json
skills/fern/
  .codex-plugin/plugin.json
  LICENSE
  README.md
  commit/
  deep-search/
  fern/
  reflect/
  setup-fern/
  talk-it-through/
  technical-writing/
  unslop/
```

The marketplace resolves `./skills/fern` relative to the repository root.
The native Codex manifest lists each skill directory explicitly. Its paths
are relative to the plugin root and must stay inside that root. Codex rejects
`./` as a component path. Keep the list complete when adding or removing a
Fern skill. Each leaf retains its instructions, metadata, and resources.

This is Codex's native `.codex-plugin/plugin.json` format. The portable
Agent Plugins format uses a different root manifest and fixed component
layout; portable ingestion is not claimed for this package.

## Install and update

Use a Codex version with the `plugin` command. Check `codex plugin --help`
and its subcommand help in the target client. These commands are supported
by Codex CLI `0.162.1`.

For a local checkout, run from the repository root:

```text
codex plugin marketplace add .
codex plugin list --marketplace saberuster-skills --available --json
codex plugin add fern@saberuster-skills
```

After the marketplace files are published to the selected Git ref, consumers
can register the Git source instead:

```text
codex plugin marketplace add saberuster/skills --ref main
codex plugin add fern@saberuster-skills
```

Use a released tag or another published ref when pinning a consumer to a
specific revision. An unpublished working tree cannot be installed from Git.
Choose one source registration for this marketplace in a given profile.

Before switching from standalone Fern skills or another Fern marketplace,
inspect the existing source and preserve local edits. Remove or disable the
old installation only within the requested migration scope. Installing a
second copy can produce duplicate entries. Repository changes do not migrate
existing profiles automatically.

For updates, refresh the registered marketplace using
`codex plugin marketplace upgrade saberuster-skills`, then use the target
client's plugin update or reinstall flow. Check its help and resulting
installed version and skill list. Do not edit the plugin cache directly.

After installation, verify `fern@saberuster-skills` and all eight skills in
a fresh Codex session. Invoke Fern explicitly with `$fern`. The plugin does
not install external tools or apply project configuration, custom agents, or
user instructions. Invoke `$setup-fern` separately when that setup is wanted.

## Maintenance and releases

Edit skills at their existing `skills/fern/<name>/` paths. Update the native
manifest when membership or listing metadata changes. The marketplace entry
points to the plugin directory; it does not duplicate the plugin version.
Keep the bundled `LICENSE` identical to the root license.

The repository-managed plugin version is `0.2.0`. Repository tags
still version the whole repository. The plugin's SemVer version independently
identifies its bundled content for installation and updates. Before 1.0,
increment its minor version for scope or instruction behavior changes and
its patch version for compatible corrections. Bump once per shipped set of
plugin changes and record user-visible changes in `CHANGELOG.md`.

Use the repository [validation layers](validation.md). Deterministic checks
verify the marketplace source, plugin identity, exact skill membership,
contained paths, metadata, license, and snapshot inclusion. Standalone
client discovery and Skills CLI installation remain separate checks.

The `fern-plugin` runtime check registers the candidate marketplace in a
disposable Linux profile, inspects the available plugin, installs it, and checks
the installed plugin metadata, complete cache contents and discovered skill
paths. Expected version, website and membership come from the candidate
manifest. Reports retain source hashes, the pinned client version, CLI results,
app-server responses and cleanup outcomes. Run it through the unified launcher:

```text
python scripts/run_validation.py --layer affected --check fern-plugin --output /tmp/fern-plugin-001
```

Fern source and marketplace changes select this check in the affected layer;
the full layer always includes it. The `docker-context` check separately builds
synthetic contexts with each checked-in Docker ignore file. It verifies that
the exact public marketplace file survives with identical bytes while sibling
and nested `.agents` files remain excluded. Relevant filtering changes select
it in the affected layer; full validation includes both filters. It uses the
host Docker daemon and never mounts its socket inside a validation container.

No model calls are needed to check registration and loading. Those checks
do not establish natural selection, task behavior, or successful application
of the Setup Fern project resources. The `fern-plugin-host` manual entry keeps
Windows desktop, Codex Cloud, fresh-chat loading and remote marketplace
publication visible as `not_run` until separately tested. Use disposable
profiles for those procedures as well.

## Format references

- [OpenAI plugin packaging guide](https://developers.openai.com/plugins/build/plugins)
- [Codex 0.162.1 native manifest parser](https://github.com/openai/codex/blob/rust-v0.162.1/codex-rs/core-plugins/src/manifest.rs)
- [Codex 0.162.1 marketplace parser](https://github.com/openai/codex/blob/rust-v0.162.1/codex-rs/core-plugins/src/marketplace.rs)
