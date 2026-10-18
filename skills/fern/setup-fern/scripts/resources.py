"""Apply bundled Fern project resources while preserving unrelated content."""

from __future__ import annotations

import json
import os
import re
import stat
import tempfile
import tomllib
from pathlib import Path

START = b"<!-- fern:user-instructions:start -->"
END = b"<!-- fern:user-instructions:end -->"
INSTRUCTIONS = "instructions:user-rules"
ROLES = (
    "architect",
    "debugger",
    "docs_researcher",
    "reviewer",
    "validator",
    "visual_reviewer",
)


def ensure_plain_path(path: Path) -> None:
    """Reject links on the selected path or its ancestors."""
    path = Path(os.path.abspath(path))
    for item in (*reversed(path.parents), path):
        try:
            info = item.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise ValueError(f"Linked or reparse path requires migration: {item}")


def _flatten(data: dict, prefix: tuple = ()) -> dict:
    result = {}
    for key, value in data.items():
        path = (*prefix, key)
        if isinstance(value, dict):
            result.update(_flatten(value, path))
        else:
            result[path] = value
    return result


def _scalar(value: object) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, (int, str)):
        return json.dumps(value)
    raise ValueError("Unsupported baseline scalar")


def _config_edit(raw: bytes, key: tuple[str, ...], value: object) -> bytes:
    """Edit plain/dotted scalar keys; reject syntax that cannot be kept faithfully."""
    text = raw.decode("utf-8")
    before = _flatten(tomllib.loads(text))
    lines = text.splitlines(keepends=True)
    newline = "\r\n" if "\r\n" in text else "\n"
    section = ()
    sections = []
    matches = []
    scalar = r'(?:"(?:[^"\\\r\n]|\\.)*"|\x27[^\x27\r\n]*\x27|true|false|[+-]?[0-9_]+)'
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("["):
            # Parsing the header avoids treating quoted table names as dotted names.
            try:
                probe = _flatten(tomllib.loads(line + "\nfern_probe = 0\n"))
                section = next(iter(probe))[:-1]
            except (ValueError, StopIteration):
                section = ("<unsupported>",)
            sections.append((section, index))
        assignment = re.match(r"^(\s*)([^#\r\n=]+?)(\s*=\s*)(.*?)(\r?\n)?$", line)
        if not assignment:
            continue
        prefix, name, equals, tail, ending = assignment.groups()
        try:
            parsed = _flatten(tomllib.loads(name + " = 0"))
            path = (*section, *next(iter(parsed)))
        except (ValueError, StopIteration):
            continue
        if path != key:
            continue
        match = re.fullmatch(rf"({scalar})([ \t]*(?:#.*)?)", tail)
        if not match:
            raise ValueError("Selected key uses unsupported scalar syntax")
        matches.append(index)
        lines[index] = (
            prefix + name + equals + _scalar(value) + match[2] + (ending or "")
        )
    if len(matches) > 1:
        raise ValueError("Ambiguous selected configuration key")
    if not matches:
        if key in before:
            raise ValueError("Selected key uses inline or unsupported TOML syntax")
        table = key[:-1]
        headers = [index for path, index in sections if path == table]
        if len(headers) > 1:
            raise ValueError("Ambiguous selected configuration table")
        entry = f"{key[-1]} = {_scalar(value)}{newline}"
        if headers:
            index = headers[0] + 1
            if not lines[index - 1].endswith("\n"):
                lines[index - 1] += newline
            lines.insert(index, entry)
        else:
            suffix = "" if not text or text.endswith("\n") else newline
            lines.append(suffix + newline + f"[{'.'.join(table)}]{newline}" + entry)
    result = "".join(lines).encode("utf-8")
    expected = dict(before)
    expected[key] = value
    if _flatten(tomllib.loads(result.decode("utf-8"))) != expected:
        raise ValueError("TOML merge would change unrelated settings")
    return result


def _block(raw: bytes) -> tuple[int, int] | None:
    if b"fern:subagent-instructions:" in raw:
        raise ValueError("Obsolete Fern instruction markers are unsupported")
    counts = [raw.count(marker) for marker in (START, END)]
    if counts == [0, 0]:
        return None
    if counts != [1, 1]:
        raise ValueError("Instruction markers are unmatched or repeated")
    first = raw.index(START)
    last = raw.index(END)
    if last < first:
        raise ValueError("Instruction markers are reversed")
    return first, last + len(END)


def _atomic(path: Path, content: bytes) -> None:
    ensure_plain_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else None
    fd, temporary = tempfile.mkstemp(prefix=".fern-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(content)
        if mode is not None:
            os.chmod(temporary, mode)
        ensure_plain_path(path)
        os.replace(temporary, path)
        if path.read_bytes() != content:
            raise OSError("Resource readback differs from prepared content")
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def apply_resources(package: Path, root: Path, check: bool = False) -> list[dict]:
    """Copy bundled agents and merge config/rules, with bundled values taking priority."""
    package, root = Path(package), Path(os.path.abspath(root))
    assets = package / "assets/codex"
    codex = root / ".codex"
    results = []

    def report(name, status, path, reason=None):
        item = {"name": name, "status": status, "path": str(path)}
        if reason:
            item["reason"] = reason
        results.append(item)

    def failure(name, destination, error):
        report(
            name,
            "conflict" if isinstance(error, ValueError) else "failed",
            destination,
            str(error),
        )

    for role in ROLES:
        path = assets / "agents" / f"{role}.toml"
        name = f"agents/{role}.toml"
        destination = codex / name
        try:
            ensure_plain_path(path)
            ensure_plain_path(destination)
            incoming = path.read_bytes()
            parsed = tomllib.loads(incoming.decode("utf-8"))
            if parsed.get("name") != role or any(
                not isinstance(parsed.get(key), str) or not parsed[key].strip()
                for key in ("name", "description", "developer_instructions")
            ):
                raise ValueError("Invalid bundled custom agent identity")
            current = destination.read_bytes() if destination.exists() else None
            if current == incoming:
                report(name, "unchanged", destination)
            elif check:
                report(name, "missing" if current is None else "different", destination)
            else:
                _atomic(destination, incoming)
                report(name, "added" if current is None else "updated", destination)
        except (OSError, ValueError) as error:
            failure(name, destination, error)

    destination = codex / "config.toml"
    try:
        ensure_plain_path(assets / "config.fragment.toml")
        selected = _flatten(
            tomllib.loads((assets / "config.fragment.toml").read_text(encoding="utf-8"))
        )
    except (OSError, ValueError) as error:
        report("config", "failed", destination, str(error))
        selected = {}
    if selected:
        statuses = {}
        try:
            ensure_plain_path(destination)
            current = destination.read_bytes() if destination.exists() else b""
            parsed = _flatten(tomllib.loads(current.decode("utf-8")))
            for key, value in selected.items():
                present = key in parsed
                statuses[key] = (
                    "unchanged"
                    if present
                    and parsed[key] == value
                    and type(parsed[key]) is type(value)
                    else ("different" if present else "missing")
                    if check
                    else ("updated" if present else "added")
                )
            if not check:
                prepared = current
                for key, value in selected.items():
                    if statuses[key] != "unchanged":
                        prepared = _config_edit(prepared, key, value)
                if prepared != current:
                    _atomic(destination, prepared)
            for key, status in statuses.items():
                report("config:" + ".".join(key), status, destination)
        except (OSError, ValueError) as error:
            for key in selected:
                name = "config:" + ".".join(key)
                if statuses.get(key) == "unchanged":
                    report(name, "unchanged", destination)
                else:
                    failure(name, destination, error)

    destination = root / "AGENTS.md"
    try:
        ensure_plain_path(destination)
        ensure_plain_path(assets / "user-instructions.md")
        current = destination.read_bytes() if destination.exists() else b""
        newline = b"\r\n" if b"\r\n" in current else b"\n"
        asset = (
            (assets / "user-instructions.md")
            .read_bytes()
            .replace(b"\r\n", b"\n")
            .rstrip(b"\n")
        )
        incoming = START + newline + asset.replace(b"\n", newline) + newline + END
        span = _block(current)
        if span:
            first, last = span
            if current[first:last] == incoming:
                report(INSTRUCTIONS, "unchanged", destination)
            elif check:
                report(INSTRUCTIONS, "different", destination)
            else:
                _atomic(destination, current[:first] + incoming + current[last:])
                report(INSTRUCTIONS, "updated", destination)
        elif check:
            report(INSTRUCTIONS, "missing", destination)
        else:
            separator = (
                b""
                if not current
                else newline
                if current.endswith(b"\n")
                else newline * 2
            )
            _atomic(destination, current + separator + incoming + newline)
            report(INSTRUCTIONS, "added", destination)
    except (OSError, ValueError) as error:
        failure(INSTRUCTIONS, destination, error)
    return results
