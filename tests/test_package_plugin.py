"""Portable release artifact content and Git provenance regression tests."""

import hashlib
import json
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

import yaml

from scripts.package_plugin import SCHEMA, package_plugin, source_files


class PackagePluginTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "repo"
        self.plugin = self.root / "skills/fern"
        self.manifest = self.plugin / ".codex-plugin/plugin.json"
        self.manifest.parent.mkdir(parents=True)
        self.native = {
            "name": "fern",
            "version": "0.2.0",
            "description": "Synthetic plugin",
            "author": {"name": "Example"},
            "license": "MIT",
            "repository": "https://example.com/repo",
            "homepage": "https://example.com",
            "keywords": ["workflow"],
            "skills": ["./first"],
            "interface": {
                "displayName": "Fern",
                "shortDescription": "Workflows",
                "capabilities": [],
                "defaultPrompt": ["First", "Second"],
                "logo": "./assets/logo.svg",
            },
        }
        self.write_manifest()
        self.add_skill("first")
        self.write("LICENSE", "Synthetic license\n")
        self.write("assets/logo.svg", "<svg/>\n")
        self.write(
            "README.md",
            "[First](first/SKILL.md) [Manifest](.codex-plugin/plugin.json)\n",
        )

    def write_manifest(self):
        self.manifest.write_text(json.dumps(self.native), encoding="utf-8")

    def write(self, relative, text):
        path = self.plugin / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))
        return path

    def add_skill(self, name):
        self.write(
            f"{name}/SKILL.md",
            f"---\nname: {name}\ndescription: >-\n  Use this synthetic workflow.\n---\n\nInstructions.\n",
        )
        self.write(f"{name}/references/deep/data.txt", "Complete resources\n")
        self.write(
            f"{name}/agents/openai.yaml",
            "interface:\n  display_name: Example\n  short_description: Synthetic workflow\npolicy:\n  allow_implicit_invocation: false\n",
        )

    def build(self, name="out", ref=None):
        return package_plugin(self.root, "fern", Path(self.temporary.name) / name, ref)

    def git(self, *args):
        return (
            subprocess.run(
                ["git", "-C", str(self.root), *args], capture_output=True, check=True
            )
            .stdout.decode()
            .strip()
        )

    def commit(self):
        self.git("add", ".")
        self.git(
            "-c",
            "user.name=Example",
            "-c",
            "user.email=example@example.com",
            "-c",
            "commit.gpgsign=false",
            "commit",
            "-m",
            "test: synthetic snapshot",
        )
        return self.git("rev-parse", "HEAD")

    def test_discovers_new_skill_and_preserves_complete_resources(self):
        self.add_skill("new-skill")  # Deliberately absent from native membership.
        self.write("first/__pycache__/cache.pyc", "exclude")
        self.write(".env.local", "exclude")
        self.write("build/output", "exclude")
        self.write("first/resources/.hidden", "retain")
        paths = self.build()
        with zipfile.ZipFile(paths[0]) as archive:
            self.assertIn("skills/new-skill/SKILL.md", archive.namelist())
            self.assertEqual(
                archive.read("skills/new-skill/references/deep/data.txt"),
                b"Complete resources\n",
            )
            self.assertEqual(
                archive.read("skills/first/agents/openai.yaml"),
                (self.plugin / "first/agents/openai.yaml").read_bytes(),
            )
            self.assertIn("skills/first/resources/.hidden", archive.namelist())
            self.assertNotIn(".codex-plugin/plugin.json", archive.namelist())
            self.assertFalse(
                any(
                    "cache.pyc" in name
                    or name.startswith("build/")
                    or name == ".env.local"
                    for name in archive.namelist()
                )
            )
            self.assertEqual(
                archive.read("README.md"),
                b"[First](skills/first/SKILL.md) [Manifest](plugin.json)\n",
            )
        build = json.loads(paths[2].read_bytes())
        self.assertEqual(build["skills"], ["first", "new-skill"])
        self.assertTrue(build["source"]["preview"])

    def test_converts_manifest_without_top_level_native_fields(self):
        paths = self.build()
        with zipfile.ZipFile(paths[0]) as archive:
            manifest = json.loads(archive.read("plugin.json"))
            self.assertEqual(manifest["$schema"], SCHEMA)
            for field in (
                "name",
                "version",
                "description",
                "author",
                "license",
                "repository",
                "homepage",
                "keywords",
            ):
                self.assertEqual(manifest[field], self.native[field])
            self.assertEqual(
                manifest["extensions"]["com.openai"]["interface"],
                self.native["interface"],
            )
            self.assertNotIn("interface", manifest)
            self.assertNotIn("skills", manifest)
            self.assertEqual(archive.read("assets/logo.svg"), b"<svg/>\n")

    def test_skill_names_and_bundled_resource_names_are_not_cache_filters(self):
        names = ("build", "dist", "venv", "credentials")
        for name in names:
            self.add_skill(name)
        self.write("first/references/build/instructions.txt", "required build resource")
        self.write(
            "first/references/credentials/instructions.txt",
            "required credential documentation",
        )
        self.write("assets/auth.json/icon.svg", "required icon")
        self.write(
            "first/references/credentials/auth.json", "exclude local credentials"
        )
        self.git("init")
        commit = self.commit()
        archives = []
        for output, ref in (("preview", None), ("exact", commit)):
            with self.subTest(ref=ref):
                paths = self.build(output, ref)
                archives.append(paths[0].read_bytes())
                with zipfile.ZipFile(paths[0]) as archive:
                    for name in names:
                        self.assertIn(f"skills/{name}/SKILL.md", archive.namelist())
                    self.assertEqual(
                        archive.read("skills/first/references/build/instructions.txt"),
                        b"required build resource",
                    )
                    self.assertEqual(
                        archive.read(
                            "skills/first/references/credentials/instructions.txt"
                        ),
                        b"required credential documentation",
                    )
                    self.assertIn("assets/auth.json/icon.svg", archive.namelist())
                    self.assertNotIn(
                        "skills/first/references/credentials/auth.json",
                        archive.namelist(),
                    )
        self.assertEqual(archives[0], archives[1])

    def test_reproducible_zip_and_complete_integrity_report(self):
        first = self.build("one")
        second = self.build("two")
        self.assertEqual(first[0].read_bytes(), second[0].read_bytes())
        self.assertEqual(first[2].read_bytes(), second[2].read_bytes())
        report = json.loads(first[2].read_bytes())
        digest = hashlib.sha256(first[0].read_bytes()).hexdigest()
        self.assertEqual(report["sha256"], digest)
        self.assertEqual(first[1].read_text(), f"{digest}  fern-0.2.0.zip\n")
        with zipfile.ZipFile(first[0]) as archive:
            self.assertEqual(archive.namelist(), sorted(archive.namelist()))
            self.assertEqual(set(report["entries"]), set(archive.namelist()))
            for entry in archive.infolist():
                self.assertEqual(entry.date_time, (1980, 1, 1, 0, 0, 0))
                self.assertEqual(
                    report["entries"][entry.filename],
                    hashlib.sha256(archive.read(entry)).hexdigest(),
                )

    def test_exact_ref_ignores_later_commits_worktree_and_untracked_files(self):
        self.git("init")
        commit = self.commit()
        original = (self.plugin / "first/SKILL.md").read_bytes()
        self.write("first/references/later.txt", "later commit")
        self.commit()
        self.write("first/SKILL.md", "malformed worktree")
        self.add_skill("untracked")
        paths = self.build(ref=commit)
        with zipfile.ZipFile(paths[0]) as archive:
            self.assertEqual(archive.read("skills/first/SKILL.md"), original)
            self.assertNotIn("skills/first/references/later.txt", archive.namelist())
            self.assertNotIn("skills/untracked/SKILL.md", archive.namelist())
        report = json.loads(paths[2].read_bytes())
        self.assertEqual(
            report["source"], {"mode": "git-ref", "commit": commit, "preview": False}
        )
        self.assertEqual(
            (self.plugin / "first/SKILL.md").read_text(), "malformed worktree"
        )

    def test_rejects_non_semver_versions(self):
        for version in ("1.2", "v1.2.3", "01.2.3", "1.2.3-01", "1.2.3+", "1.2.3\n"):
            with self.subTest(version=version):
                self.native["version"] = version
                self.write_manifest()
                with self.assertRaisesRegex(ValueError, "SemVer"):
                    self.build()

    def test_accepts_semver_prerelease_and_build(self):
        self.native["version"] = "1.2.3-rc.1+build.2"
        self.write_manifest()
        self.assertEqual(self.build()[0].name, "fern-1.2.3-rc.1+build.2.zip")

    def test_rejects_malformed_skill_or_agent_metadata(self):
        skill = self.plugin / "first/SKILL.md"
        original = skill.read_bytes()
        for data in (
            "No YAML",
            "---\nname: wrong\ndescription: Example\n---",
            "---\nname: first\ndescription: []\n---",
            "---\nname: first\ndescription: [\n---",
        ):
            with self.subTest(data=data):
                skill.write_text(data, encoding="utf-8")
                with self.assertRaises((ValueError, yaml.YAMLError)):
                    self.build()
        skill.write_bytes(original)
        self.write(
            "first/agents/openai.yaml",
            'policy:\n  allow_implicit_invocation: "false"\n',
        )
        with self.assertRaisesRegex(ValueError, "invocation"):
            self.build()

    def test_rejects_empty_plugin(self):
        (self.plugin / "first/SKILL.md").unlink()
        with self.assertRaisesRegex(ValueError, "no direct child skills"):
            self.build()

    def test_rejects_unmappable_components_and_missing_assets(self):
        self.native["mcpServers"] = {"example": {}}
        self.write_manifest()
        with self.assertRaisesRegex(ValueError, "Unsupported"):
            self.build()
        del self.native["mcpServers"]
        self.native["interface"]["logo"] = "assets/missing.svg"
        self.write_manifest()
        with self.assertRaisesRegex(ValueError, "Missing interface asset"):
            self.build()

    def test_rejects_traversal_selection_and_output_inside_plugin(self):
        with self.assertRaisesRegex(ValueError, "Invalid plugin name"):
            package_plugin(self.root, "../fern", Path(self.temporary.name) / "out")
        with self.assertRaisesRegex(ValueError, "outside the source"):
            package_plugin(self.root, "fern", self.plugin / "output")
        self.native["interface"]["logo"] = "../secret.svg"
        self.write_manifest()
        with self.assertRaisesRegex(ValueError, "Unsafe package path"):
            self.build()

    def test_rejects_existing_outputs_without_modifying_them(self):
        paths = self.build()
        original = [path.read_bytes() for path in paths]
        with self.assertRaisesRegex(ValueError, "already exists"):
            self.build()
        self.assertEqual([path.read_bytes() for path in paths], original)

    def test_rejects_ref_options_and_file_directory_collision(self):
        with self.assertRaisesRegex(ValueError, "not an option"):
            self.build(ref="--help")
        self.write("skills", "conflicts with portable skills directory")
        with self.assertRaisesRegex(ValueError, "File/directory collision"):
            self.build()

    def test_rejects_linked_resources(self):
        self.git("init")
        self.commit()
        oid = self.git("hash-object", "-w", "skills/fern/LICENSE")
        self.git(
            "update-index",
            "--add",
            "--cacheinfo",
            f"120000,{oid},skills/fern/first/link.txt",
        )
        tree = self.git("write-tree")
        commit = self.git(
            "-c",
            "user.name=Example",
            "-c",
            "user.email=example@example.com",
            "commit-tree",
            tree,
            "-m",
            "test: link",
        )
        with self.assertRaisesRegex(ValueError, "Linked or special Git source"):
            self.build(ref=commit)

    def test_rejects_case_colliding_directories(self):
        files, provenance = source_files(self.root, "fern", None)
        files.update({"assets/Icons/a.svg": b"one", "assets/icons/b.svg": b"two"})
        with patch(
            "scripts.package_plugin.source_files", return_value=(files, provenance)
        ):
            with self.assertRaisesRegex(ValueError, "Case collision"):
                self.build()

    def test_exact_ref_keeps_export_ignored_files_and_unsubstituted_bytes(self):
        self.write(
            ".gitattributes",
            "first/references/* export-ignore\nfirst/substitute.txt export-subst\n",
        )
        self.write("first/substitute.txt", "$Format:%H$\n")
        self.git("init")
        commit = self.commit()
        paths = self.build(ref=commit)
        with zipfile.ZipFile(paths[0]) as archive:
            self.assertEqual(
                archive.read("skills/first/references/deep/data.txt"),
                b"Complete resources\n",
            )
            self.assertEqual(
                archive.read("skills/first/substitute.txt"), b"$Format:%H$\n"
            )


if __name__ == "__main__":
    unittest.main()
