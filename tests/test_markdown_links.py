"""Exercise link parsing and containment with isolated Markdown fixtures."""

import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from scripts.check_markdown_links import check_markdown_links, main


class MarkdownLinkTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.root = self.base / "repository"
        self.root.mkdir()

    def write(self, name, content=""):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
        return path

    def check(self, content):
        self.write("README.md", content)
        return check_markdown_links(self.root, ["README.md"])

    def test_inline_titles_parentheses_escapes_and_encoded_paths(self):
        self.write("guide (draft).md", "# Guide\n")
        self.write("hash#name.md", "# Hash\n")
        self.assertEqual(
            self.check(
                '[guide](<guide (draft).md> "Draft title")\n'
                "[escaped](guide\\%20\\(draft\\).md)\n"
                "[hash](hash%23name.md#hash)\n"
                "[query](hash%23name.md?mode=preview#hash)\n"
            ),
            [],
        )

    def test_missing_inline_reference_and_image_targets_are_reported(self):
        findings = self.check(
            "[inline](missing-inline.md)\n\n"
            "[reference][guide]\n\n"
            "![picture][image]\n\n"
            "[guide]: missing-reference.md\n"
            "[image]: missing-image.png\n"
        )
        self.assertEqual(
            [(item.line, item.target, item.message) for item in findings],
            [
                (1, "missing-inline.md", "Missing local link target"),
                (3, "missing-reference.md", "Missing local link target"),
                (5, "missing-image.png", "Missing local link target"),
            ],
        )

    def test_full_collapsed_shortcut_references_and_images(self):
        self.write("guide.md", "# Guide\n")
        self.write("image.png")
        self.assertEqual(
            self.check(
                "[full][ Guide ] [collapsed][] [shortcut]\n"
                "![full image][image] ![collapsed image][] ![shortcut image]\n\n"
                '[guide]: guide.md#guide "Guide title"\n'
                "[collapsed]: guide.md\n"
                "[shortcut]: guide.md\n"
                "[image]: image.png\n"
                "[collapsed image]: image.png\n"
                "[shortcut image]: image.png\n"
            ),
            [],
        )

    def test_code_examples_unused_definitions_and_external_links_are_ignored(self):
        self.assertEqual(
            self.check(
                "`[inline](missing.md)` and `![image](missing.png)`\n\n"
                "```markdown\n[missing](no.md)\n# Fake heading\n```\n\n"
                "    [indented](missing.md)\n\n"
                "[unused]: missing.md\n\n"
                "[web](https://example.invalid/missing.md#none)\n"
                "[network](//example.invalid/missing.md)\n"
                "[email](mailto:person@example.invalid)\n"
                "[custom](custom:resource)\n"
                "![remote](https://example.invalid/image.png)\n"
                "<https://example.invalid/missing.md>\n"
            ),
            [],
        )

    def test_same_document_headings_strip_formatting_and_decode_entities(self):
        self.assertEqual(
            self.check(
                "# Quick *Start*: `api_v1` &amp; ~~Old~~\n\n"
                "[jump](#quick-start-api_v1--old)\n\n"
                "Setext Heading\n--------------\n\n"
                "[setext](#setext-heading)\n"
            ),
            [],
        )

    def test_cross_file_headings_and_encoded_fragments(self):
        self.write("docs/guide.md", "# User Setup\n\n## Caf\u00e9\n")
        self.write(
            "docs/nested/index.md",
            "[parent](../guide.md#user-setup)\n[home](../../README.md#home)\n",
        )
        self.write(
            "README.md",
            "# Home\n[guide](docs/guide.md#user%2Dsetup)\n"
            "[unicode](docs/guide.md#caf%C3%A9)\n",
        )
        self.assertEqual(check_markdown_links(self.root), [])

    def test_duplicate_heading_suffixes_avoid_existing_anchor_collisions(self):
        self.assertEqual(
            self.check(
                "# Repeat\n# Repeat\n# Repeat-1\n# Repeat\n\n"
                "[one](#repeat) [two](#repeat-1)\n"
                "[explicit collision](#repeat-1-1) [three](#repeat-2)\n"
            ),
            [],
        )

    def test_missing_fragments_include_same_document_and_reference_links(self):
        self.write("guide.md", "# Existing\n")
        findings = self.check(
            "# Home\n[local](#gone) [other][target]\n\n[target]: guide.md#gone\n"
        )
        self.assertEqual([item.target for item in findings], ["#gone", "guide.md#gone"])
        self.assertTrue(
            all(
                item.message == "Missing Markdown heading fragment" for item in findings
            )
        )

    def test_code_headings_do_not_satisfy_a_fragment(self):
        findings = self.check("```markdown\n# Example\n```\n\n[jump](#example)\n")
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].message, "Missing Markdown heading fragment")

    def test_heading_link_labels_and_image_alt_text(self):
        self.write("image.png")
        self.assertEqual(
            self.check(
                "# [Linked *text*](#linked-text-icon) ![Icon](image.png)\n"
                "[jump](#linked-text-icon)\n"
            ),
            [],
        )

    def test_non_markdown_fragments_and_directory_links_check_only_paths(self):
        self.write("assets/icon.svg", "<svg/>\n")
        self.assertEqual(
            self.check("![icon](assets/icon.svg#view) [folder](assets/) [top](#)\n"),
            [],
        )

    def test_outside_paths_are_rejected_before_target_reads(self):
        outside = self.base / "outside.md"
        outside.write_text("# Outside\n", encoding="utf-8")
        self.write(
            "README.md",
            "[relative](../outside.md#outside)\n[encoded](%2E%2E/outside.md#outside)\n",
        )
        original = Path.read_text

        def guarded_read(path, *args, **kwargs):
            self.assertNotEqual(path.resolve(), outside.resolve())
            return original(path, *args, **kwargs)

        with patch.object(Path, "read_text", guarded_read):
            findings = check_markdown_links(self.root)
        self.assertEqual(len(findings), 2)
        self.assertTrue(
            all(
                item.message == "Local link target is outside repository"
                for item in findings
            )
        )

    def test_outside_source_document_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "document is outside repository"):
            check_markdown_links(self.root, [self.base / "outside.md"])

    def test_invalid_decoded_paths_are_reported(self):
        findings = self.check("[nul](file%00.md) [separator](..%5Coutside.md)\n")
        self.assertEqual(len(findings), 2)
        self.assertTrue(
            all(item.message == "Invalid local link path" for item in findings)
        )

    def test_symlink_escape_is_rejected(self):
        outside = self.base / "outside.md"
        outside.write_text("# Outside\n", encoding="utf-8")
        try:
            (self.root / "linked.md").symlink_to(outside)
        except OSError as error:
            self.skipTest(f"Creating symlinks is unavailable: {error}")
        findings = self.check("[escape](linked.md#outside)\n")
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].message, "Local link target is outside repository")

    def test_ignored_directories_do_not_add_false_failures(self):
        self.write("README.md", "# Home\n")
        self.write("node_modules/package/README.md", "[bad](missing.md)\n")
        self.write(".venv/README.md", "[bad](missing.md)\n")
        self.assertEqual(check_markdown_links(self.root), [])

    def test_cli_exit_codes_and_diagnostics(self):
        self.write("README.md", "[bad](missing.md)\n")
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            self.assertEqual(main(["--root", str(self.root)]), 1)
        self.assertIn(
            "README.md:1: Missing local link target: missing.md", stdout.getvalue()
        )
        self.write("README.md", "# Home\n")
        self.assertEqual(main(["--root", str(self.root)]), 0)
        with redirect_stderr(io.StringIO()) as stderr:
            self.assertEqual(main(["--root", str(self.root / "missing")]), 2)
        self.assertIn("Repository root must be a directory", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
