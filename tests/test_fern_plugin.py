"""Codex marketplace packaging; runtime loading is separate evidence."""

import json
import unittest
from pathlib import Path

from scripts.skill_packages import skill_packages

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "skills/fern"


class FernPluginTests(unittest.TestCase):
    def test_marketplace_resolves_to_the_maintained_plugin(self):
        catalog = json.loads(
            (ROOT / ".agents/plugins/marketplace.json").read_text("utf-8")
        )
        self.assertEqual(catalog["name"], "saberuster-skills")
        entries = [entry for entry in catalog["plugins"] if entry["name"] == "fern"]
        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertEqual(entry["source"], {"source": "local", "path": "./skills/fern"})
        self.assertEqual(entry["policy"]["installation"], "AVAILABLE")
        self.assertEqual(entry["policy"]["authentication"], "ON_INSTALL")
        source = (ROOT / entry["source"]["path"]).resolve()
        self.assertEqual(source, PLUGIN.resolve())
        manifest = json.loads((source / ".codex-plugin/plugin.json").read_text("utf-8"))
        self.assertEqual(manifest["name"], entry["name"])

    def test_plugin_contains_exactly_the_fern_leaf_sources(self):
        manifest = json.loads((PLUGIN / ".codex-plugin/plugin.json").read_text("utf-8"))
        self.assertRegex(
            manifest["version"], r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$"
        )
        self.assertEqual(manifest["license"], "MIT")
        self.assertEqual(
            (PLUGIN / "LICENSE").read_bytes(), (ROOT / "LICENSE").read_bytes()
        )
        self.assertIsInstance(manifest["skills"], list)
        self.assertTrue(manifest["skills"])
        self.assertEqual(len(manifest["skills"]), len(set(manifest["skills"])))
        declared = set()
        for relative in manifest["skills"]:
            self.assertIsInstance(relative, str)
            self.assertTrue(relative.startswith("./"))
            self.assertNotEqual(relative, "./")
            self.assertNotIn("..", Path(relative).parts)
            package = (PLUGIN / relative).resolve()
            self.assertTrue(package.is_relative_to(PLUGIN.resolve()))
            self.assertTrue((package / "SKILL.md").is_file(), relative)
            self.assertTrue((package / "agents/openai.yaml").is_file(), relative)
            declared.add(package)
        expected = {
            package.resolve()
            for package in skill_packages(ROOT).values()
            if package.parent == PLUGIN
        }
        self.assertEqual(declared, expected)
        self.assertTrue(expected)
        interface = manifest["interface"]
        self.assertEqual(interface["displayName"], "Fern")
        self.assertTrue(0 < len(interface["shortDescription"]) <= 30)
        self.assertIsInstance(interface["capabilities"], list)


if __name__ == "__main__":
    unittest.main()
