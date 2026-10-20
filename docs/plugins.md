# Codex marketplace and Fern plugin

This repository is a Codex marketplace named `saberuster-skills`. Its first
plugin, `fern`, packages the skills maintained in `skills/fern/`.
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

This source uses Codex's native `.codex-plugin/plugin.json` format. The
[release packager](#build-a-downloadable-plugin) exports the portable Agent
Plugins layout without moving the maintained sources.

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

The installation branch is `main`; it can contain unreleased changes under
the last released plugin version. Record the resolved commit SHA for an exact
snapshot, or pin to a plugin release tag such as `fern/v0.3.0`.
An unpublished working tree cannot be installed from Git.
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

After installation, verify `fern@saberuster-skills` and all bundled skills in
a fresh Codex session. Invoke Fern explicitly with `$fern`. The plugin does
not install external tools or apply project configuration, custom agents, or
user instructions. Invoke `$setup-fern` separately when that setup is wanted.

## Maintenance and releases

Edit skills at their existing `skills/fern/<name>/` paths. Update the native
manifest when membership or listing metadata changes. The marketplace entry
points to the plugin directory; it does not duplicate the plugin version.
Keep the bundled `LICENSE` identical to the root license.

Each plugin manifest is the sole source of its version. Accumulate changes on
`main` and bump once per released batch. Repository and individual skill
versions are not maintained; existing repository tags remain historical.
Use plugin-scoped tags such as `fern/v0.3.0` for new releases.

Use the project skill `$release-plugin` at
`.agents/skills/release-plugin/SKILL.md` for classification and publication.
`$release-plugin fern` first presents a read-only release brief with the scope,
version, Git delivery route, checks and endpoint. Confirmation authorizes the
approved edits, integration into `main`, tag push, CI draft verification and
formal publication without repeated per-step approvals. Explicit local-only
or draft-only requests narrow that endpoint. Material scope changes require a
revised brief; failed checks remain blockers. In `0.x`, added capabilities or
changed usage contracts require a minor bump; restoring an existing promise or
making compatible improvements requires a patch. Take the highest impact in
the batch. Changes outside the delivered plugin that do not affect its use
require no plugin
release. Record changes by plugin in `CHANGELOG.md`, including migration
guidance for incompatible minor releases.

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

## Build a downloadable plugin

Run [package_plugin.py](../scripts/package_plugin.py) with Python 3.11+ and
PyYAML from `requirements-dev.txt`. It discovers every direct child of
`skills/<plugin>/` containing `SKILL.md`, including newly added skills absent from
the native manifest list. Keep that list synchronized for native installation;
it does not select ZIP membership. Each skill's resources travel with it.

| Trigger | Action |
| --- | --- |
| Execute a confirmed release brief, after updating its version | Invoke the script through `$release-plugin` to inspect a working-tree preview; direct local packaging remains available |
| Push `<plugin>/v<VERSION>` after validating its commit | GitHub Actions packages that commit and creates or completes its Release draft with verified attachments |
| Ordinary edit, branch push or merge | No release packaging; existing CI runs regression tests |

From the repository root:

```text
python scripts/package_plugin.py --plugin fern --output-dir dist/preview
python scripts/package_plugin.py --plugin fern --ref <validated-commit-sha> --output-dir dist/release
```

Use a new output directory for each build. Existing output files are not
overwritten. The default reads working-tree content; `--ref` resolves a Git
revision and reads that commit without switching the checkout. The script
does not update versions, commit, tag, upload, or publish.

The output contains `fern-VERSION.zip`, its `.zip.sha256` checksum and a
`fern-VERSION.build.json` report recording source provenance and packaged file
hashes. The ZIP has root `plugin.json`, `LICENSE`, and `skills/<name>/` plus
the plugin's other supporting files. The portable manifest derives its version
and metadata from the native manifest; no second version is maintained.
Generated caches and local credential files are excluded. Linked paths and
unsupported components fail instead of producing a misleading partial package.

The script rereads the ZIP to check its contents. Deterministic archive tests
and successful construction do not establish ChatGPT import or runtime support;
test the actual archive with the target host. Skill tools and filesystem access
still depend on that host. This ZIP is for plugin upload, not a guarantee of
public directory submission readiness.

## Tag-triggered release drafts

One [release-plugin.yml](../.github/workflows/release-plugin.yml) serves all
plugins. After release preparation and validation, push the plugin tag pointing
to the intended commit on `main`, for example `fern/v0.3.0`. The tagged commit
must contain this workflow. Push each release tag separately, using credentials
that trigger Actions; another workflow's `GITHUB_TOKEN` push does not.

The workflow runs on GitHub's Ubuntu runner. It checks the tag, manifest name
and version, and commit membership in `main`, then packages that exact commit.
It creates a Release draft named for the plugin/version and uploads the ZIP,
checksum and build report. Each tag has its own run and concurrency group;
adding another plugin with the same source layout needs no new workflow.
The upload step uses GitHub's built-in token with `contents: write`; no extra
secret is needed. The release helper currently targets github.com.

Rerun a failed Actions run to resume the same draft. Matching attachments are
retained, missing ones are uploaded, and mismatched files or an already published
Release cause failure without replacement. Never move a release tag to retry.
The skill inspects the run and downloaded attachments, then publishes under
the confirmed brief unless a draft-only endpoint was requested. Draft creation
does not establish full release validation or host import.
GitHub's automatic repository source archive is separate from the plugin ZIP.

## Format references

- [OpenAI plugin packaging guide](https://developers.openai.com/plugins/build/plugins)
- [Codex 0.162.1 native manifest parser](https://github.com/openai/codex/blob/rust-v0.162.1/codex-rs/core-plugins/src/manifest.rs)
- [Codex 0.162.1 marketplace parser](https://github.com/openai/codex/blob/rust-v0.162.1/codex-rs/core-plugins/src/marketplace.rs)
- [GitHub workflow triggers](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow)
- [GitHub Releases API](https://docs.github.com/en/rest/releases/releases)
