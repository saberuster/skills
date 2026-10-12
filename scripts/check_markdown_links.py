"""Check local Markdown links and GitHub heading fragments without network calls.

CommonMark handles inline/reference links, images, escaping, and code blocks.
HTML links and custom HTML anchors are outside this check's scope.
"""

import argparse
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt
from markdown_it.rules_inline import autolink, image, link

ROOT = Path(__file__).resolve().parents[1]
IGNORED = {".git", ".venv", ".ruff_cache", "__pycache__", "node_modules"}


@dataclass(frozen=True)
class Finding:
    document: Path
    line: int
    target: str
    message: str


def make_parser():
    parser = MarkdownIt("commonmark").enable(["table", "strikethrough"])
    # Keep the parser's grammar; only attach source offsets for diagnostics.
    for name, original in (("link", link), ("image", image), ("autolink", autolink)):

        def with_location(state, silent, rule=original):
            start, count = state.pos, len(state.tokens)
            matched = rule(state, silent)
            if matched and not silent:
                for token in state.tokens[count:]:
                    if token.type in {"link_open", "image"}:
                        token.meta.setdefault(
                            "line_offset", state.src[:start].count("\n")
                        )
            return matched

        parser.inline.ruler.at(name, with_location)
    return parser


def heading_text(tokens):
    """Extract rendered heading text, including code and image alt text."""
    text = []
    for token in tokens or []:
        if token.type in {"text", "code_inline"}:
            text.append(token.content)
        elif token.type == "image":
            text.append(heading_text(token.children))
        elif token.type in {"softbreak", "hardbreak"}:
            text.append("\n")
    return "".join(text)


def heading_anchors(tokens):
    """Apply GitHub's heading rules and avoid collisions with earlier anchors.

    See GitHub Docs, Basic writing and formatting syntax, Section links.
    ASCII hyphens and underscores remain valid anchor characters.
    """
    anchors = set()
    for index, token in enumerate(tokens):
        if token.type != "heading_open":
            continue
        text = heading_text(tokens[index + 1].children).strip().lower()
        base = "".join(
            "-" if character == " " else character
            for character in text
            if character == " "
            or character in "-_"
            or (
                not character.isspace()
                and unicodedata.category(character)[0] not in {"P", "S", "C"}
            )
        )
        anchor, suffix = base, 0
        while anchor in anchors:
            suffix += 1
            anchor = f"{base}-{suffix}"
        anchors.add(anchor)
    return anchors


def markdown_documents(root):
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.suffix.lower() == ".md"
        and not any(part in IGNORED for part in path.relative_to(root).parts)
    )


def check_markdown_links(root=ROOT, documents=None):
    """Return findings; never read a document or target outside the root."""
    root = Path(root).resolve()
    parser = make_parser()
    parsed = {}

    def parse_document(path):
        path = path.resolve()
        if not path.is_relative_to(root):
            raise ValueError("Markdown document is outside repository")
        if path not in parsed:
            parsed[path] = parser.parse(path.read_text(encoding="utf-8-sig"))
        return parsed[path]

    findings = []
    for document in markdown_documents(root) if documents is None else documents:
        document = Path(document)
        if not document.is_absolute():
            document = root / document
        tokens = parse_document(document)
        for block in tokens:
            if block.type != "inline":
                continue
            for token in block.children or []:
                attribute = {"link_open": "href", "image": "src"}.get(token.type)
                if attribute is None:
                    continue
                target = token.attrGet(attribute) or ""
                line = (block.map[0] + 1 if block.map else 1) + token.meta.get(
                    "line_offset", 0
                )
                try:
                    url = urlsplit(target)
                    if url.scheme or url.netloc:
                        continue
                    # Split first: encoded # and ? can be literal filename characters.
                    local_path = unquote(url.path, encoding="utf-8", errors="strict")
                    fragment = unquote(url.fragment, encoding="utf-8", errors="strict")
                    if "\0" in local_path or "\\" in local_path:
                        raise ValueError("Invalid local link path")
                    resolved = (
                        (document.parent / local_path).resolve()
                        if local_path
                        else document.resolve()
                    )
                    if not resolved.is_relative_to(root):
                        raise ValueError("Local link target is outside repository")
                    if not resolved.exists():
                        raise ValueError("Missing local link target")
                    if fragment and resolved.suffix.lower() == ".md":
                        if fragment not in heading_anchors(parse_document(resolved)):
                            raise ValueError("Missing Markdown heading fragment")
                except (OSError, UnicodeError, ValueError, RuntimeError) as error:
                    findings.append(Finding(document, line, target, str(error)))
    return findings


def main(argv=None):
    arguments = argparse.ArgumentParser(description=__doc__)
    arguments.add_argument("--root", type=Path, default=ROOT)
    args = arguments.parse_args(argv)
    try:
        root = args.root.resolve()
        if not root.is_dir():
            raise ValueError("Repository root must be a directory")
        findings = check_markdown_links(root)
        for finding in findings:
            message = (
                f"{finding.document.relative_to(root)}:{finding.line}: "
                f"{finding.message}: {finding.target}"
            )
            print(message.replace("\n", "\\n").replace("\r", "\\r"))
        return 1 if findings else 0
    except (OSError, UnicodeError, ValueError, RuntimeError) as error:
        print(f"Markdown link check failed: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
