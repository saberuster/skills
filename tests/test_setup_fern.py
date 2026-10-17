"""Check Fern's portable resource contracts, without applying host settings."""

import shutil
import tempfile
import tomllib
import unittest
from pathlib import Path

import yaml
from markdown_it import MarkdownIt

from scripts.check_codex_skills import isolated_project, package_sha256
from scripts.skill_packages import skill_packages

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "skills/fern/setup-fern"
ASSETS = PACKAGE / "assets/codex"
ROLES = {
    "architect",
    "debugger",
    "docs_researcher",
    "reviewer",
    "validator",
    "visual_reviewer",
}


class SetupFernTests(unittest.TestCase):
    def test_custom_agents_have_standalone_identity_and_one_source(self):
        files = sorted((ASSETS / "agents").glob("*.toml"))
        self.assertEqual({path.stem for path in files}, ROLES)
        for path in files:
            with self.subTest(role=path.stem):
                agent = tomllib.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(agent["name"], path.stem)
                for key in ("description", "developer_instructions"):
                    self.assertIsInstance(agent[key], str)
                    self.assertTrue(agent[key].strip())
                self.assertFalse(
                    (ROOT / "agents" / path.name).exists(),
                    "Maintain custom agents inside the complete setup-fern package",
                )

    def test_config_fragment_owns_only_selected_agent_defaults(self):
        fragment = tomllib.loads(
            (ASSETS / "config.fragment.toml").read_text(encoding="utf-8")
        )
        self.assertEqual(
            fragment,
            {
                "agents": {
                    "max_concurrent_threads_per_session": 4,
                    "default_subagent_model": "gpt-6.1-sol",
                    "default_subagent_reasoning_effort": "high",
                }
            },
        )

    def test_skill_interface_metadata_is_separate_from_custom_agents(self):
        metadata_directory = PACKAGE / "agents"
        self.assertEqual(
            {path.name for path in metadata_directory.iterdir()}, {"openai.yaml"}
        )
        metadata = yaml.safe_load(
            (metadata_directory / "openai.yaml").read_text(encoding="utf-8")
        )
        self.assertIsInstance(metadata["interface"], dict)
        self.assertIsInstance(metadata["policy"]["allow_implicit_invocation"], bool)
        self.assertEqual(
            {path.suffix for path in (ASSETS / "agents").iterdir()}, {".toml"}
        )

    def test_user_instructions_can_be_embedded_in_a_managed_block(self):
        prompt = (ASSETS / "user-instructions.md").read_text(encoding="utf-8")
        tokens = MarkdownIt().parse(prompt)
        self.assertTrue(prompt.strip())
        headings = [token.tag for token in tokens if token.type == "heading_open"]
        self.assertEqual(headings[0], "h1")
        self.assertTrue(all(tag == "h2" for tag in headings[1:]))
        self.assertFalse(
            any(token.type in {"html_block", "html_inline"} for token in tokens),
            "The instruction asset must not contain deployment block markers",
        )

    def test_isolated_staging_keeps_the_package_and_resources_together(self):
        with tempfile.TemporaryDirectory(prefix="fern-package-") as temporary:
            root = Path(temporary)
            source = root / "skills/fern/setup-fern"
            shutil.copytree(PACKAGE, source)
            self.assertEqual(skill_packages(root), {"setup-fern": source})
            with isolated_project(root) as (project, home):
                staged = project / ".agents/skills/setup-fern"
                self.assertEqual(package_sha256(staged), package_sha256(source))
                for relative in (
                    "SKILL.md",
                    "agents/openai.yaml",
                    "references/baseline.md",
                    "references/codex-installation.md",
                    "assets/codex/config.fragment.toml",
                    "assets/codex/user-instructions.md",
                    *(f"assets/codex/agents/{role}.toml" for role in sorted(ROLES)),
                ):
                    with self.subTest(resource=relative):
                        self.assertTrue((staged / relative).is_file())
                self.assertFalse((home / ".codex/config.toml").exists())
                self.assertFalse((home / ".codex/agents").exists())


if __name__ == "__main__":
    unittest.main()
