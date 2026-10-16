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
