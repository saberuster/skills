"""Static package checks; these do not test model behavior."""

import re
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


class PackageTests(unittest.TestCase):
    def test_skill_metadata(self):
        entries = list(SKILLS.glob("*/SKILL.md"))
        self.assertTrue(entries, "No skills found")
        for entry in entries:
            with self.subTest(path=entry.relative_to(ROOT)):
                parts = entry.read_text(encoding="utf-8").split("---", 2)
                self.assertEqual(parts[0], "")
                self.assertEqual(len(parts), 3)
                metadata = yaml.safe_load(parts[1])
                self.assertIsInstance(metadata, dict)
                self.assertEqual(metadata["name"], entry.parent.name)
                self.assertRegex(metadata["name"], r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
                self.assertLessEqual(len(metadata["name"]), 64)
                self.assertIsInstance(metadata["description"], str)
                self.assertTrue(metadata["description"].strip())
                self.assertLessEqual(len(metadata["description"]), 1024)
                self.assertTrue(parts[2].strip())
                ui = yaml.safe_load(
                    (entry.parent / "agents/openai.yaml").read_text(encoding="utf-8")
                )
                interface = ui["interface"]
                for key in ("display_name", "short_description", "default_prompt"):
                    self.assertIsInstance(interface[key], str)
                    self.assertTrue(interface[key].strip())
                self.assertGreaterEqual(len(interface["short_description"]), 25)
                self.assertLessEqual(len(interface["short_description"]), 64)
                self.assertIn("$" + metadata["name"], interface["default_prompt"])
                self.assertIsInstance(ui["policy"]["allow_implicit_invocation"], bool)

    def test_local_markdown_links(self):
        for path in ROOT.rglob("*.md"):
            if any(
                part in {".git", ".venv", ".ruff_cache", "__pycache__"}
                for part in path.relative_to(ROOT).parts
            ):
                continue
            for target in re.findall(
                r"(?<!!)\[[^\]]+\]\(([^)]+)\)", path.read_text(encoding="utf-8")
            ):
                link = urlsplit(target)
                if link.scheme or not link.path:
                    continue
                with self.subTest(path=path.relative_to(ROOT), target=target):
                    resolved = (path.parent / unquote(link.path)).resolve()
                    self.assertTrue(resolved.is_relative_to(ROOT))
                    self.assertTrue(resolved.exists(), "Missing local link target")

    def test_release_text_hygiene(self):
        for path in ROOT.rglob("*"):
            relative = path.relative_to(ROOT)
            if any(
                part in {".git", ".venv", ".ruff_cache", "__pycache__"}
                for part in relative.parts
            ):
                continue
            self.assertFalse(path.is_symlink(), str(relative))
            if not path.is_file():
                continue
            with self.subTest(path=relative):
                data = path.read_bytes()
                text = data.decode("ascii")
                self.assertNotIn(b"\r", data, "Use LF line endings")
                self.assertTrue(text.endswith("\n"))
                self.assertTrue(
                    all(line == line.rstrip() for line in text.splitlines())
                )


if __name__ == "__main__":
    unittest.main()
