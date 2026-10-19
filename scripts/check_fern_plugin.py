"""Check native Fern plugin installation and discovery in a disposable Linux home."""

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath

import yaml

if __package__ in {None, ""}:
    from check_codex_skills import (
        DiscoveryError,
        JsonLineProcess,
        executable_command,
        isolated_environment,
        package_sha256,
        same_path,
    )
    from fern_ci import run_process, write_json
else:
    from .check_codex_skills import (
        DiscoveryError,
        JsonLineProcess,
        executable_command,
        isolated_environment,
        package_sha256,
        same_path,
    )
    from .fern_ci import run_process, write_json

ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE = Path(".agents/plugins/marketplace.json")
PLUGIN = Path("skills/fern")


def require(condition, message):
    if not condition:
        raise DiscoveryError(message)


def object_value(value, label):
    require(isinstance(value, dict), f"{label}: expected object")
    return value


def array(value, label):
    require(isinstance(value, list), f"{label}: expected array")
    require(all(isinstance(row, dict) for row in value), f"{label}: malformed row")
    return value


def identifier(value):
    return isinstance(value, str) and re.fullmatch(r"[a-z0-9][a-z0-9._-]*", value)


def candidate(root):
    """Derive expectations from complete candidate sources, before any CLI runs."""
    root = root.resolve()
    marketplace_path = root / MARKETPLACE
    require(marketplace_path.resolve() == marketplace_path, "Linked marketplace source")
    marketplace = object_value(json.loads(marketplace_path.read_text()), "marketplace")
    marketplace_name = marketplace.get("name")
    require(identifier(marketplace_name), "Invalid marketplace name")
    rows = array(marketplace.get("plugins"), "marketplace plugins")
    rows = [row for row in rows if row.get("name") == "fern"]
    require(len(rows) == 1, "Expected exactly one Fern marketplace entry")
    require(
        rows[0].get("source") == {"source": "local", "path": "./skills/fern"},
        "Fern marketplace source must be ./skills/fern",
    )
    plugin = root / PLUGIN
    require(plugin.resolve() == plugin, "Linked plugin source")
    package_hash = package_sha256(plugin)
    manifest = object_value(
        json.loads((plugin / ".codex-plugin/plugin.json").read_text()), "manifest"
    )
    name, version = manifest.get("name"), manifest.get("version")
    require(name == "fern", "Candidate manifest is not Fern")
    require(identifier(version), "Invalid plugin version")
    interface = object_value(manifest.get("interface"), "manifest interface")
    website = interface.get("websiteURL")
    require(
        isinstance(website, str) and website.startswith("https://"),
        "Missing HTTPS plugin websiteURL",
    )
    paths = manifest.get("skills")
    require(isinstance(paths, list) and paths, "Manifest needs an explicit skill list")
    skills = {}
    for value in paths:
        require(isinstance(value, str), "Manifest skill path must be a string")
        relative = PurePosixPath(value)
        require(
            value.startswith("./")
            and len(relative.parts) == 1
            and identifier(relative.name),
            "Manifest skill path must name a direct leaf package",
        )
        source = plugin / relative.name
        require(
            source.resolve().parent == plugin.resolve(), "Skill source escapes plugin"
        )
        text = (source / "SKILL.md").read_text(encoding="utf-8")
        parts = text.split("---", 2)
        require(len(parts) == 3 and parts[0] == "", "Missing skill frontmatter")
        metadata = object_value(yaml.safe_load(parts[1]), "skill frontmatter")
        require(
            metadata.get("name") == relative.name, "Skill name differs from directory"
        )
        description = metadata.get("description")
        require(
            isinstance(description, str) and description.strip(), "Missing description"
        )
        require(relative.name not in skills, "Duplicate manifest skill")
        skills[relative.name] = {
            "description": description,
            "sha256": package_sha256(source),
        }
    leaves = {path.parent.name for path in plugin.glob("*/SKILL.md")}
    require(
        leaves == set(skills), "Manifest does not match complete Fern leaf packages"
    )
    return {
        "marketplace": marketplace_name,
        "name": name,
        "id": f"{name}@{marketplace_name}",
        "version": version,
        "website": website,
        "skills": skills,
        "source_hashes": {
            MARKETPLACE.as_posix(): hashlib.sha256(
                marketplace_path.read_bytes()
            ).hexdigest(),
            PLUGIN.as_posix(): package_hash,
        },
    }


def verify_identity(row, expected, version_key="version", id_key="pluginId"):
    require(row.get(id_key) == expected["id"], "Plugin identity differs from candidate")
    require(row.get("name") == expected["name"], "Plugin name differs from candidate")
    require(
        row.get(version_key) == expected["version"],
        "Plugin version differs from candidate",
    )


def verify_cli_listing(value, expected, installed):
    value = object_value(value, "CLI plugin list")
    rows = array(value.get("installed"), "installed plugins")
    available = array(value.get("available"), "available plugins")
    selected = rows if installed else available
    require(len(selected) == 1, "Expected exactly one candidate plugin")
    require(not (available if installed else rows), "Unexpected plugin listing entries")
    verify_identity(selected[0], expected)
    require(
        selected[0].get("marketplaceName") == expected["marketplace"],
        "CLI marketplace identity differs from candidate",
    )
    require(
        selected[0].get("installed") is installed
        and selected[0].get("enabled") is installed,
        "Unexpected plugin installation/enabled state",
    )


def verify_skills(rows, expected, location, *, discovery=False):
    rows = array(rows, "skills")
    found = {}
    for row in rows:
        name = row.get("name")
        if discovery and row.get("scope") == "system":
            require(isinstance(name, str), "Malformed system skill")
            continue
        require(isinstance(name, str), "Malformed skill name")
        prefix = expected["name"] + ":"
        require(name.startswith(prefix), f"Unexpected non-system skill: {name}")
        leaf = name[len(prefix) :]
        require(
            leaf in expected["skills"] and leaf not in found,
            "Unexpected or duplicate skill",
        )
        require(
            same_path(row.get("path"), location / leaf / "SKILL.md"),
            "Skill path escapes candidate package",
        )
        require(row.get("enabled") is True, "Plugin skill is disabled")
        require(
            row.get("description") == expected["skills"][leaf]["description"],
            "Skill description differs from candidate",
        )
        if discovery:
            require(row.get("scope") == "user", "Plugin skill has unexpected scope")
            require(
                row.get("pluginId") == expected["id"],
                "Skill pluginId differs from candidate",
            )
        found[leaf] = row
    require(set(found) == set(expected["skills"]), "Missing expected plugin skills")
    return found


def verify_rpc(replies, expected, project, home, cache):
    replies = object_value(replies, "app-server replies")
    for method in ("initialize", "plugin/list", "plugin/read", "skills/list"):
        object_value(replies.get(method), method)
    initialize = object_value(replies["initialize"], "initialize")
    require(
        same_path(initialize.get("codexHome"), home / ".codex"),
        "App-server escaped isolated home",
    )
    listing = object_value(replies["plugin/list"], "plugin/list")
    require(
        listing.get("marketplaceLoadErrors") == [],
        "Marketplace load errors or missing error array",
    )
    marketplaces = array(listing.get("marketplaces"), "marketplaces")
    require(len(marketplaces) == 1, "Unexpected or missing marketplaces")
    marketplace = marketplaces[0]
    require(
        marketplace.get("name") == expected["marketplace"], "Unexpected marketplace"
    )
    require(
        same_path(marketplace.get("path"), project / MARKETPLACE),
        "Marketplace path escapes fixture",
    )
    plugins = array(marketplace.get("plugins"), "marketplace plugins")
    require(len(plugins) == 1, "Unexpected marketplace plugin entries")
    read = object_value(replies["plugin/read"].get("plugin"), "plugin/read plugin")
    require(
        read.get("marketplaceName") == expected["marketplace"],
        "plugin/read marketplace differs",
    )
    require(
        same_path(read.get("marketplacePath"), project / MARKETPLACE),
        "plugin/read marketplace path differs",
    )
    for row in (plugins[0], object_value(read.get("summary"), "plugin summary")):
        verify_identity(row, expected, "localVersion", "id")
        require(
            row.get("installed") is True and row.get("enabled") is True,
            "App-server plugin is not installed and enabled",
        )
        interface = object_value(row.get("interface"), "plugin interface")
        require(
            interface.get("websiteUrl") == expected["website"],
            "Plugin website differs from candidate",
        )
    verify_skills(read.get("skills"), expected, project / PLUGIN)
    data = array(replies["skills/list"].get("data"), "skills/list data")
    require(
        len(data) == 1 and same_path(data[0].get("cwd"), project),
        "skills/list project differs",
    )
    require(data[0].get("errors") == [], "Skill load errors or missing error array")
    verify_skills(data[0].get("skills"), expected, cache, discovery=True)


def check_plugin(source=ROOT, executable="codex", timeout=60):
    report = {
        "check": "fern-plugin",
        "status": "failed",
        "model_requests": False,
        "checks": [],
        "processes": [],
        "app_server_replies": {},
        "errors": [],
        "limits": "Linux native plugin installation and loading only; no model invocation, Windows/Cloud host acceptance, or remote marketplace publication.",
    }
    expected = None
    source = Path(source).resolve()
    try:
        require(
            sys.platform == "linux", "Use the disposable Linux validation container"
        )
        require(timeout > 0, "Timeout must be positive")
        expected = candidate(source)
        report["candidate"] = expected
        report["source_hashes"] = expected["source_hashes"]
        with tempfile.TemporaryDirectory(prefix="fern-plugin-") as temporary:
            # Windows TEMP can use an 8.3 alias for the same directory.
            temporary = Path(temporary).resolve()
            project, home = temporary / "project", temporary / "home"
            (project / MARKETPLACE.parent).mkdir(parents=True)
            (project / ".git").mkdir()
            shutil.copy2(source / MARKETPLACE, project / MARKETPLACE)
            shutil.copytree(source / PLUGIN, project / PLUGIN)
            require(
                candidate(project) == expected, "Fixture copy differs from candidate"
            )
            env = isolated_environment(home)
            cache = (
                home
                / ".codex/plugins/cache"
                / expected["marketplace"]
                / expected["name"]
                / expected["version"]
            )

            def cli(arguments, *, parse=False):
                command = executable_command(executable, arguments)
                result = run_process(command, project, env, timeout)
                report["processes"].append(result)
                require(
                    result["returncode"] == 0
                    and result["timed_out"] is False
                    and not result["cleanup_error"],
                    f"CLI failed: {' '.join(arguments)}",
                )
                output = result["stdout"]
                require(
                    isinstance(output, str) and output.strip(),
                    "CLI returned empty output",
                )
                return (
                    object_value(json.loads(output), "CLI response")
                    if parse
                    else output
                )

            report["client_version"] = cli(["--version"]).strip()
            cli(["plugin", "marketplace", "add", str(project)])
            verify_cli_listing(
                cli(
                    [
                        "plugin",
                        "list",
                        "--marketplace",
                        expected["marketplace"],
                        "--available",
                        "--json",
                    ],
                    parse=True,
                ),
                expected,
                False,
            )
            installed = cli(["plugin", "add", expected["id"], "--json"], parse=True)
            verify_identity(installed, expected)
            require(
                same_path(installed.get("installedPath"), cache),
                "Installed plugin path escapes isolated cache",
            )
            require(cache.resolve() == cache, "Linked plugin cache escapes fixture")
            verify_cli_listing(
                cli(["plugin", "list", "--json"], parse=True), expected, True
            )
            report["checks"].append(
                "CLI marketplace registration, installation and enabled listing"
            )
            require(
                package_sha256(cache) == expected["source_hashes"][PLUGIN.as_posix()],
                "Complete cached plugin bytes differ from candidate",
            )
            report["checks"].append(
                "Complete cache matches source, including invocation policies and resources"
            )
            command = executable_command(executable, ["app-server", "--stdio"])
            server = JsonLineProcess(command, project, env, timeout)
            process = {
                "command": command,
                "kind": "app-server",
                "returncode": None,
                "shutdown": "pending",
                "cleanup_error": None,
            }
            report["processes"].append(process)
            replies = report["app_server_replies"]
            try:
                replies["initialize"] = server.request(
                    1,
                    "initialize",
                    {
                        "clientInfo": {"name": "fern_plugin_check", "version": "1.0"},
                        "capabilities": {"experimentalApi": True},
                    },
                )
                server.send({"method": "initialized"})
                replies["plugin/list"] = server.request(
                    2, "plugin/list", {"cwds": [str(project)]}
                )
                replies["plugin/read"] = server.request(
                    3,
                    "plugin/read",
                    {
                        "marketplacePath": str(project / MARKETPLACE),
                        "pluginName": expected["name"],
                    },
                )
                replies["skills/list"] = server.request(
                    4, "skills/list", {"cwds": [str(project)], "forceReload": True}
                )
                verify_rpc(replies, expected, project, home, cache)
                require(
                    server.process.poll() is None,
                    "App-server exited before controlled shutdown",
                )
                process["shutdown"] = (
                    "deliberate process-tree termination after protocol checks"
                )
                report["checks"].append(
                    "App-server plugin metadata and exact cache-backed namespaced skill discovery"
                )
            finally:
                if process["shutdown"] == "pending":
                    process["shutdown"] = (
                        "process-tree termination after failed protocol check"
                    )
                try:
                    server.close()
                except (OSError, RuntimeError, subprocess.SubprocessError) as error:
                    process["cleanup_error"] = str(error)
                    raise
                finally:
                    process["returncode"] = server.process.poll()
                    process["stderr"] = server.stderr
            require(
                process["returncode"] is not None,
                "App-server cleanup left process running",
            )
            require(candidate(project) == expected, "Plugin CLI mutated fixture source")
            require(
                package_sha256(cache) == expected["source_hashes"][PLUGIN.as_posix()],
                "App-server mutated cached plugin",
            )
        report["checks"].append("Disposable fixture cleaned up")
        report["status"] = "passed"
    except (
        OSError,
        ValueError,
        RuntimeError,
        subprocess.SubprocessError,
        yaml.YAMLError,
    ) as error:
        report["errors"].append(str(error))
    finally:
        if expected is not None:
            try:
                require(
                    candidate(source) == expected,
                    "Candidate source changed during plugin check",
                )
                report["checks"].append("Candidate source unchanged")
            except (OSError, ValueError, RuntimeError, yaml.YAMLError) as error:
                report["errors"].append(str(error))
                report["status"] = "failed"
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--codex", default="codex")
    parser.add_argument("--timeout", type=int, default=60)
    args = parser.parse_args()
    result = check_plugin(args.source, args.codex, args.timeout)
    write_json(args.report, result)
    print(f"fern-plugin: {result['status']}")
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
