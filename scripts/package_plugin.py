"""Build a deterministic portable skills plugin from a worktree or Git commit."""

import argparse
import hashlib
import io
import json
import re
import subprocess
import zipfile
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
NAME = re.compile(r"[a-z0-9]+(?:[.-][a-z0-9]+)*")
SEMVER = re.compile(
    r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)"
    r"(?:-(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*)"
    r"(?:\.(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*))*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
)
EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    ".ruff_cache",
    ".pytest_cache",
    ".mypy_cache",
    ".cache",
    ".aws",
    ".ssh",
}
EXCLUDED_FILES = {
    ".env",
    ".ds_store",
    "thumbs.db",
    "credentials",
    "credentials.json",
    "auth.json",
    ".npmrc",
    ".netrc",
}
UNSUPPORTED_COMPONENTS = {"mcp.json", ".mcp.json", ".app.json", "hooks.json"}


def excluded(path, skill_roots=(), *, is_dir=False):
    """Exclude generated state and local credentials, preserving skill resources."""
    parts = path.parts[1:] if path.parts[0] in skill_roots else path.parts
    return (
        any(part.lower() in EXCLUDED_DIRS for part in parts)
        or (
            path.parts[0] not in skill_roots
            and path.parts[0].lower() in {"build", "dist"}
        )
    ) or (
        not is_dir
        and (
            path.name.lower() in EXCLUDED_FILES
            or path.name.lower().startswith(".env.")
            or path.suffix.lower() in {".pyc", ".pyo", ".pem", ".key"}
        )
    )


def safe_path(value):
    path = PurePosixPath(value)
    if (
        not value
        or "\\" in value
        or ":" in value
        or path.is_absolute()
        or any(part in {"", ".", ".."} for part in value.split("/"))
        or any(part.endswith((".", " ")) for part in path.parts)
    ):
        raise ValueError(f"Unsafe package path: {value!r}")
    return path


def git(root, *args, input_data=None):
    return subprocess.run(
        ["git", "-c", "core.autocrlf=false", "-C", str(root), *args],
        check=True,
        capture_output=True,
        input=input_data,
    ).stdout


def linked(path):
    return path.is_symlink() or getattr(path.lstat(), "st_file_attributes", 0) & 0x400


def source_files(root, plugin, ref):
    prefix = f"skills/{plugin}/"
    files = {}
    if ref is not None:
        if not ref or ref.startswith("-"):
            raise ValueError("Git ref must be a nonempty revision, not an option")
        commit = (
            git(root, "rev-parse", "--verify", f"{ref}^{{commit}}").decode().strip()
        )
        tree = git(root, "ls-tree", "-rz", "--full-tree", commit, "--", prefix[:-1])
        candidates = []
        for item in tree.split(b"\0"):
            if not item:
                continue
            header, raw_path = item.split(b"\t", 1)
            mode, kind, oid = header.split()
            name = raw_path.decode("utf-8")
            if not name.startswith(prefix):
                raise ValueError("Git tree contains a path outside the plugin")
            relative = name[len(prefix) :]
            path = safe_path(relative)
            if kind != b"blob" or mode not in {b"100644", b"100755"}:
                raise ValueError(f"Linked or special Git source: {relative}")
            candidates.append((relative, oid))
        skill_roots = {
            relative.split("/")[0]
            for relative, _ in candidates
            if len(PurePosixPath(relative).parts) == 2
            and relative.endswith("/SKILL.md")
        }
        selected = [
            (relative, oid)
            for relative, oid in candidates
            if not excluded(PurePosixPath(relative), skill_roots)
        ]
        if selected:
            # Read committed bytes directly: export-ignore, export-subst, global
            # attributes and checkout line-ending preferences cannot change them.
            raw = git(
                root,
                "cat-file",
                "--batch",
                input_data=b"\n".join(oid for _, oid in selected) + b"\n",
            )
            content = io.BytesIO(raw)
            for relative, oid in selected:
                actual_oid, kind, size = content.readline().split()
                if actual_oid != oid or kind != b"blob":
                    raise ValueError("Unexpected Git blob response")
                files[relative] = content.read(int(size))
                if len(files[relative]) != int(size) or content.read(1) != b"\n":
                    raise ValueError("Incomplete Git blob response")
        return files, {"mode": "git-ref", "commit": commit, "preview": False}
    plugin_root = root / "skills" / plugin
    for path in (root / "skills", plugin_root):
        if linked(path):
            raise ValueError(f"Linked source directory: {path.name}")
    skill_roots = {
        child.name
        for child in plugin_root.iterdir()
        if child.is_dir() and (child / "SKILL.md").is_file()
    }

    def visit(directory):
        for path in sorted(directory.iterdir()):
            relative = path.relative_to(plugin_root).as_posix()
            safe_path(relative)
            if linked(path):
                raise ValueError(f"Linked source: {relative}")
            if excluded(PurePosixPath(relative), skill_roots, is_dir=path.is_dir()):
                continue
            if path.is_dir():
                visit(path)
            elif path.is_file():
                files[relative] = path.read_bytes()
            else:
                raise ValueError(f"Special source file: {relative}")

    visit(plugin_root)
    try:
        commit = git(root, "rev-parse", "HEAD").decode().strip()
        dirty = bool(
            git(root, "status", "--porcelain", "--untracked-files=all", "--", prefix)
        )
    except subprocess.CalledProcessError:
        commit, dirty = None, None
    return files, {
        "mode": "working-tree",
        "commit": commit,
        "dirty": dirty,
        "preview": True,
    }


def nonblank(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a nonblank string")


def portable_manifest(native, plugin):
    if not isinstance(native, dict):
        raise ValueError("Native manifest must be an object")
    allowed = {
        "$schema",
        "name",
        "version",
        "description",
        "author",
        "homepage",
        "repository",
        "license",
        "keywords",
        "interface",
        "skills",
        "extensions",
    }
    unknown = set(native) - allowed
    if unknown:
        raise ValueError(
            f"Unsupported native manifest fields/components: {sorted(unknown)}"
        )
    if native.get("name") != plugin:
        raise ValueError("Manifest name must match the selected plugin directory")
    version = native.get("version")
    if not isinstance(version, str) or not SEMVER.fullmatch(version):
        raise ValueError("Plugin version must use strict SemVer")
    portable = {"$schema": SCHEMA, "name": plugin, "version": version}
    for field in ("description", "homepage", "repository", "license"):
        if field in native:
            nonblank(native[field], field)
            portable[field] = native[field]
    if "author" in native:
        if not isinstance(native["author"], dict):
            raise ValueError("author must be an object")
        portable["author"] = native["author"]
    if "keywords" in native:
        if not isinstance(native["keywords"], list):
            raise ValueError("keywords must be an array")
        for value in native["keywords"]:
            nonblank(value, "keyword")
        portable["keywords"] = native["keywords"]
    extensions = native.get("extensions", {})
    if not isinstance(extensions, dict):
        raise ValueError("extensions must be an object")
    extensions = dict(extensions)
    openai = extensions.get("com.openai", {})
    if not isinstance(openai, dict):
        raise ValueError("extensions.com.openai must be an object")
    openai = dict(openai)
    if set(openai) - {"interface"}:
        raise ValueError("Unsupported OpenAI extension components/settings")
    if "interface" in native:
        if "interface" in openai and openai["interface"] != native["interface"]:
            raise ValueError("Conflicting native and portable interface metadata")
        openai["interface"] = native["interface"]
    interface = openai.get("interface", {})
    if not isinstance(interface, dict):
        raise ValueError("interface must be an object")
    for field, value in interface.items():
        if field == "capabilities":
            if not isinstance(value, list):
                raise ValueError("interface.capabilities must be an array")
            for item in value:
                nonblank(item, field)
        elif field == "defaultPrompt" and isinstance(value, list):
            if not 1 <= len(value) <= 3:
                raise ValueError("defaultPrompt accepts one to three prompts")
            for item in value:
                nonblank(item, field)
        else:
            nonblank(value, f"interface.{field}")
            if field.endswith("URL") and (
                urlsplit(value).scheme != "https" or not urlsplit(value).netloc
            ):
                raise ValueError(f"interface.{field} requires an absolute HTTPS URL")
            if field in {"brandColor", "brandColorDark"} and not re.fullmatch(
                r"#[0-9A-Fa-f]{6}", value
            ):
                raise ValueError(f"Invalid interface.{field}")
    if len(interface.get("shortDescription", "")) > 30:
        raise ValueError("interface.shortDescription exceeds 30 characters")
    if openai:
        extensions["com.openai"] = openai
    if extensions:
        portable["extensions"] = extensions
    return portable


def validate_skill(name, data, agent=None):
    if len(name) > 64 or not NAME.fullmatch(name) or "." in name:
        raise ValueError(f"Invalid skill directory name: {name}")
    if len(data) > 1024 * 1024:
        raise ValueError(f"SKILL.md exceeds 1 MiB: {name}")
    lines = data.decode("utf-8").splitlines()
    if not lines or lines[0] != "---" or "---" not in lines[1:]:
        raise ValueError(f"Missing YAML frontmatter: {name}")
    metadata = yaml.safe_load("\n".join(lines[1 : lines.index("---", 1)]))
    if not isinstance(metadata, dict):
        raise ValueError(f"Frontmatter must be an object: {name}")
    if metadata.get("name") != name:
        raise ValueError(f"Skill name must match directory: {name}")
    nonblank(metadata.get("description"), f"{name} description")
    if agent is not None:
        metadata = yaml.safe_load(agent.decode("utf-8"))
        if not isinstance(metadata, dict):
            raise ValueError(f"agents/openai.yaml must be an object: {name}")
        interface = metadata.get("interface")
        if interface is not None:
            if not isinstance(interface, dict):
                raise ValueError(f"Invalid agent interface: {name}")
            for field in ("display_name", "short_description"):
                nonblank(interface.get(field), f"{name} {field}")
            if "default_prompt" in interface:
                nonblank(interface["default_prompt"], f"{name} default_prompt")
        policy = metadata.get("policy", {})
        if not isinstance(policy, dict) or set(policy) - {
            "products",
            "allow_implicit_invocation",
        }:
            raise ValueError(f"Invalid agent policy: {name}")
        invocation = policy.get("allow_implicit_invocation")
        if invocation is not None and not isinstance(invocation, bool):
            raise ValueError(f"Invalid invocation policy: {name}")
        products = policy.get("products")
        if products is not None and (
            not isinstance(products, list)
            or any(item not in {"CHAT", "CODEX", "HERMES"} for item in products)
        ):
            raise ValueError(f"Invalid product policy: {name}")


def json_bytes(value):
    return (
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    ).encode()


def rewrite_root_markdown(data, skills):
    """Retarget root documentation links for relocated skills and manifest."""

    def replace(match):
        target = match.group("target")
        relative = target.removeprefix("./")
        if relative.split("/", 1)[0] in skills:
            target = "skills/" + relative
        elif relative.split("#", 1)[0] == ".codex-plugin/plugin.json":
            target = relative.replace(".codex-plugin/plugin.json", "plugin.json", 1)
        return match.group("prefix") + target

    content = data.decode("utf-8")
    content = re.sub(r"(?P<prefix>\]\(\s*<?)(?P<target>[^\s)>]+)", replace, content)
    content = re.sub(
        r"(?m)^(?P<prefix> {0,3}\[[^\]\n]+\]:\s*<?)(?P<target>[^\s>]+)",
        replace,
        content,
    )
    return content.encode("utf-8")


def package_plugin(root=ROOT, plugin="fern", output_dir="dist", ref=None):
    """Return output paths; preview builds never imply a released version."""
    root = Path(root).resolve()
    if len(plugin) > 64 or not NAME.fullmatch(plugin):
        raise ValueError("Invalid plugin name")
    output = Path(output_dir).resolve()
    source = (root / "skills" / plugin).resolve()
    if output.is_relative_to(source):
        raise ValueError("Output directory must be outside the source plugin")
    files, provenance = source_files(root, plugin, ref)
    manifest = portable_manifest(json.loads(files[".codex-plugin/plugin.json"]), plugin)
    skills = sorted(
        path.split("/")[0]
        for path in files
        if len(PurePosixPath(path).parts) == 2
        and path.endswith("/SKILL.md")
        and not path.startswith(".")
    )
    if not skills:
        raise ValueError("Plugin has no direct child skills")
    for name in skills:
        validate_skill(
            name, files[f"{name}/SKILL.md"], files.get(f"{name}/agents/openai.yaml")
        )
    entries = {"plugin.json": json_bytes(manifest)}
    seen = {"plugin.json": "plugin.json"}
    for relative, data in sorted(files.items()):
        path = safe_path(relative)
        if path.parts[0] == ".codex-plugin":
            continue
        if relative == "plugin.json" or path.parts[0] in UNSUPPORTED_COMPONENTS:
            raise ValueError(f"Conflicting or unsupported root component: {relative}")
        target = f"skills/{relative}" if path.parts[0] in skills else relative
        safe_path(target)
        if target in entries:
            raise ValueError(f"Duplicate archive path: {target}")
        if any(
            existing.startswith(target + "/") or target.startswith(existing + "/")
            for existing in entries
        ):
            raise ValueError(f"File/directory collision in archive: {target}")
        for index in range(1, len(PurePosixPath(target).parts) + 1):
            component = "/".join(PurePosixPath(target).parts[:index])
            folded = component.casefold()
            if folded in seen and seen[folded] != component:
                raise ValueError(f"Case collision in archive: {target}")
            seen[folded] = component
        if len(path.parts) == 1 and path.suffix.lower() == ".md":
            data = rewrite_root_markdown(data, skills)
        entries[target] = data
    for field in ("logo", "logoDark", "composerIcon", "composerIconDark"):
        interface = (
            manifest.get("extensions", {}).get("com.openai", {}).get("interface", {})
        )
        if field in interface:
            asset = interface[field].removeprefix("./")
            safe_path(asset)
            if asset not in entries:
                raise ValueError(f"Missing interface asset: {asset}")
    stream = io.BytesIO()
    with zipfile.ZipFile(
        stream, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as archive:
        for name, data in sorted(entries.items()):
            info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data, compresslevel=9)
    zip_data = stream.getvalue()
    with zipfile.ZipFile(io.BytesIO(zip_data)) as archive:
        if archive.testzip() is not None or set(archive.namelist()) != set(entries):
            raise ValueError("Final archive structure or CRC verification failed")
        for name, data in entries.items():
            if archive.read(name) != data:
                raise ValueError(f"Final archive bytes differ: {name}")
        if json.loads(archive.read("plugin.json")) != manifest:
            raise ValueError("Final archive manifest verification failed")
    basename = f"{plugin}-{manifest['version']}.zip"
    digest = hashlib.sha256(zip_data).hexdigest()
    build = {
        "plugin": plugin,
        "version": manifest["version"],
        "source": provenance,
        "skills": skills,
        "archive": basename,
        "sha256": digest,
        "entries": {
            name: hashlib.sha256(data).hexdigest()
            for name, data in sorted(entries.items())
        },
    }
    outputs = {
        basename: zip_data,
        f"{basename}.sha256": f"{digest}  {basename}\n".encode(),
        f"{basename.removesuffix('.zip')}.build.json": json_bytes(build),
    }
    paths = [output / name for name in outputs]
    if any(path.exists() or path.is_symlink() for path in paths):
        raise ValueError("Output already exists; choose a fresh output directory")
    output.mkdir(parents=True, exist_ok=True)
    created = []
    try:
        for name, data in outputs.items():
            path = output / name
            with path.open("xb") as handle:
                created.append(path)
                handle.write(data)
    except OSError:
        for path in created:
            path.unlink()
        raise
    return paths


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plugin", default="fern")
    parser.add_argument("--output-dir", type=Path, default=Path("dist"))
    parser.add_argument(
        "--ref", help="Build this exact Git commit; omit for a worktree preview"
    )
    args = parser.parse_args()
    try:
        paths = package_plugin(ROOT, args.plugin, args.output_dir, args.ref)
    except (
        ValueError,
        OSError,
        KeyError,
        yaml.YAMLError,
        subprocess.CalledProcessError,
    ) as error:
        parser.exit(1, f"Packaging failed: {error}\n")
    for path in paths:
        print(path)


if __name__ == "__main__":
    main()
