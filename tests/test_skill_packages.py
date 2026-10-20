"""Package identity and source-tree protections for standalone and nested skills."""

import tempfile
import unittest
from pathlib import Path

from scripts.check_claude_skills import expected_skills
from scripts.check_codex_skills import DiscoveryError, discover_expected
from scripts.skill_packages import skill_packages
from scripts.update_agent_support import source_hashes


class SkillPackageTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def package(self, relative):
        package = self.root / "skills" / relative
        package.mkdir(parents=True)
        (package / "SKILL.md").write_text("Synthetic source.\n", encoding="ascii")
        return package

    def test_standalone_and_nested_sources_have_unique_leaf_identities(self):
        direct = self.package("alpha")
        nested = self.package("fern/beta")
        self.assertEqual(skill_packages(self.root), {"alpha": direct, "beta": nested})

    def test_plugin_metadata_is_not_a_leaf_package(self):
        direct = self.package("alpha")
        nested = self.package("fern/beta")
        metadata = self.root / "skills/fern/.codex-plugin"
        metadata.mkdir()
        (metadata / "plugin.json").write_text("{}\n", encoding="ascii")
        self.assertEqual(skill_packages(self.root), {"alpha": direct, "beta": nested})

    def test_empty_top_level_placeholder_is_not_a_package(self):
        direct = self.package("alpha")
        placeholder = self.root / "skills/future-plugin"
        placeholder.mkdir()
        (placeholder / ".gitkeep").touch()
        self.assertEqual(skill_packages(self.root), {"alpha": direct})

    def test_placeholder_does_not_hide_incomplete_source(self):
        self.package("alpha")
        placeholder = self.root / "skills/future-plugin"
        placeholder.mkdir()
        marker = placeholder / ".gitkeep"
        marker.touch()
        for extra in ("README.md", "draft.py"):
            with self.subTest(extra=extra):
                path = placeholder / extra
                path.write_text("Draft.\n", encoding="ascii")
                with self.assertRaisesRegex(ValueError, "missing source SKILL.md"):
                    skill_packages(self.root)
                path.unlink()
        marker.write_text("Not an empty marker.\n", encoding="ascii")
        with self.assertRaisesRegex(ValueError, "missing source SKILL.md"):
            skill_packages(self.root)

    def test_placeholder_only_tree_has_no_source_skills(self):
        placeholder = self.root / "skills/future-plugin"
        placeholder.mkdir(parents=True)
        (placeholder / ".gitkeep").touch()
        with self.assertRaisesRegex(ValueError, "No source skills found"):
            skill_packages(self.root)

    def test_nested_placeholder_still_requires_a_skill_entry(self):
        self.package("fern/beta")
        placeholder = self.root / "skills/fern/missing"
        placeholder.mkdir()
        (placeholder / ".gitkeep").touch()
        with self.assertRaisesRegex(ValueError, "missing source SKILL.md"):
            skill_packages(self.root)

    def test_other_hidden_directories_still_require_a_skill_entry(self):
        self.package("fern/beta")
        (self.root / "skills/fern/.unknown").mkdir()
        with self.assertRaisesRegex(ValueError, "missing source SKILL.md"):
            skill_packages(self.root)

    def test_plugin_metadata_contents_still_reject_links(self):
        self.package("fern/beta")
        metadata = self.root / "skills/fern/.codex-plugin"
        metadata.mkdir()
        external = self.root / "external.json"
        external.write_text("{}\n", encoding="ascii")
        try:
            (metadata / "plugin.json").symlink_to(external)
        except OSError:
            self.skipTest("Host does not permit creating test symbolic links")
        with self.assertRaisesRegex(ValueError, "linked skill source"):
            skill_packages(self.root)

    def test_duplicate_leaf_name_is_rejected_by_all_source_consumers(self):
        self.package("alpha")
        self.package("fern/alpha")
        for consumer, error in (
            (skill_packages, ValueError),
            (discover_expected, DiscoveryError),
            (expected_skills, ValueError),
            (source_hashes, ValueError),
        ):
            with self.subTest(consumer=consumer.__name__):
                with self.assertRaisesRegex(error, "Duplicate source skill name"):
                    consumer(self.root)

    def test_nested_directory_without_entry_is_rejected(self):
        (self.root / "skills/fern/missing").mkdir(parents=True)
        with self.assertRaisesRegex(ValueError, "missing source SKILL.md"):
            skill_packages(self.root)

    def test_linked_container_is_rejected_before_source_is_read(self):
        external = self.root / "external/alpha"
        external.mkdir(parents=True)
        (external / "SKILL.md").write_text("External.\n", encoding="ascii")
        (self.root / "skills").mkdir()
        try:
            (self.root / "skills/fern").symlink_to(
                self.root / "external", target_is_directory=True
            )
        except OSError:
            self.skipTest("Host does not permit creating test symbolic links")
        with self.assertRaisesRegex(ValueError, "linked skill source"):
            skill_packages(self.root)


if __name__ == "__main__":
    unittest.main()
