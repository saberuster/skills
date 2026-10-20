"""Immutable tag builds and idempotent draft uploads with a fake GitHub boundary."""

import io
import json
import subprocess
import tempfile
import unittest
import urllib.error
import urllib.request
import zipfile
from pathlib import Path
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

import yaml

from scripts.release_plugin import (
    GitHub,
    SecureRedirect,
    draft_release,
    pages,
    parse_tag,
    prepare_release,
)


class FakeGitHub:
    def __init__(self, tag, commit):
        self.tag = tag
        self.commit = commit
        self.releases = []
        self.assets = {}
        self.content = {}
        self.calls = []
        self.tag_reads = 0
        self.moved_on_read = None
        self.annotated = False
        self.fail_listing = False

    def json(self, method, path, body=None):
        self.calls.append((method, path, body))
        parsed = urlsplit(path)
        route = parsed.path
        if method == "GET" and "/git/ref/tags/" in route:
            self.tag_reads += 1
            commit = "f" * 40 if self.moved_on_read == self.tag_reads else self.commit
            return {
                "object": {
                    "type": "tag" if self.annotated else "commit",
                    "sha": "a" * 40 if self.annotated else commit,
                }
            }
        if method == "GET" and "/git/tags/" in route:
            return {"object": {"type": "commit", "sha": self.commit}}
        if method == "GET" and route.endswith("/releases"):
            if self.fail_listing:
                raise RuntimeError("GitHub GET failed: HTTP 401")
            page = int(parse_qs(parsed.query)["page"][0])
            return self.releases[(page - 1) * 100 : page * 100]
        if method == "POST" and route.endswith("/releases"):
            release = {
                "id": 42,
                "tag_name": body["tag_name"],
                "draft": body["draft"],
                "html_url": "https://github.com/example/skills/releases/tag/"
                + self.tag,
            }
            self.releases.append(release)
            return dict(release)
        if method == "GET" and route.endswith("/assets"):
            page = int(parse_qs(parsed.query)["page"][0])
            return list(self.assets.values())[(page - 1) * 100 : page * 100]
        if method == "GET" and "/releases/" in route:
            release_id = int(route.rsplit("/", 1)[1])
            return dict(
                next(item for item in self.releases if item["id"] == release_id)
            )
        raise AssertionError(f"Unexpected GitHub request: {method} {path}")

    def download(self, path):
        self.calls.append(("GET-BYTES", path, None))
        return self.content[int(path.rsplit("/", 1)[1])]

    def upload(self, repo, release_id, path):
        self.calls.append(("UPLOAD", path.name, None))
        asset_id = max(self.assets.keys(), default=0) + 1
        asset = {"id": asset_id, "name": path.name, "state": "uploaded"}
        self.assets[asset_id] = asset
        self.content[asset_id] = path.read_bytes()
        return dict(asset)


class ReleasePluginTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "repo"
        self.root.mkdir()
        self.output = Path(self.temporary.name) / "dist"
        self.git("init", "--initial-branch=main")
        for key, value in (
            ("user.name", "Example"),
            ("user.email", "example@example.com"),
            ("commit.gpgsign", "false"),
            ("tag.gpgsign", "false"),
        ):
            self.git("config", key, value)
        for plugin, version in (("fern", "0.2.0"), ("another", "1.3.4")):
            directory = self.root / "skills" / plugin
            (directory / ".codex-plugin").mkdir(parents=True)
            (directory / ".codex-plugin/plugin.json").write_text(
                json.dumps({"name": plugin, "version": version, "skills": ["./task"]}),
                encoding="utf-8",
            )
            (directory / "task").mkdir()
            (directory / "task/SKILL.md").write_bytes(
                b"---\nname: task\ndescription: Synthetic test task.\n---\n\nDo the task.\n"
            )
        (self.root / "CHANGELOG.md").write_bytes(
            b"# Changelog\n\n## Unreleased\n\nFuture notes.\n\n## fern 0.2.0 - 2026-10-20\n\nFern release note.\n\n## another 1.3.4 - 2026-10-19\n\nAnother plugin note.\n"
        )
        self.commit = self.commit_all()
        self.tag = "fern/v0.2.0"
        self.git("tag", self.tag, self.commit)
        self.git("tag", "another/v1.3.4", self.commit)
        self.git("update-ref", "refs/remotes/origin/main", self.commit)
        self.client = FakeGitHub(self.tag, self.commit)

    def git(self, *args):
        return (
            subprocess.run(
                ["git", "-C", str(self.root), *args], check=True, capture_output=True
            )
            .stdout.decode()
            .strip()
        )

    def commit_all(self):
        self.git("add", ".")
        self.git("commit", "-m", "test: synthetic release source")
        return self.git("rev-parse", "HEAD")

    def prepare(self, tag=None):
        return prepare_release(self.root, tag or self.tag, self.commit, self.output)

    def draft(self):
        return draft_release(
            self.root, self.tag, self.commit, "example/skills", self.output, self.client
        )

    def mutations(self):
        return [
            call
            for call in self.client.calls
            if call[0] in {"POST", "UPLOAD", "PATCH", "DELETE"}
        ]

    def test_generic_prepare_accepts_two_plugins(self):
        for plugin, version in (("fern", "0.2.0"), ("another", "1.3.4")):
            with self.subTest(plugin=plugin):
                paths = prepare_release(
                    self.root,
                    f"{plugin}/v{version}",
                    self.commit,
                    Path(self.temporary.name) / plugin,
                )
                self.assertEqual(paths[0].name, f"{plugin}-{version}.zip")
                report = json.loads(paths[2].read_bytes())
                self.assertEqual(report["source"]["commit"], self.commit)
                self.assertFalse(report["source"]["preview"])

    def test_tag_parser_rejects_invalid_names_versions_and_extra_levels(self):
        for tag in (
            "fern/v01.2.3",
            "fern/v1.2",
            "fern/v1.2.3-01",
            "fern/v1.2.3/extra",
            "../fern/v1.2.3",
            "Fern/v1.2.3",
            "v1.2.3",
            "fern/v1.2.3\n",
        ):
            with self.subTest(tag=tag), self.assertRaisesRegex(ValueError, "Tag must"):
                parse_tag(tag)
        self.assertEqual(
            parse_tag("another/v1.2.3-rc.1+build.2"), ("another", "1.2.3-rc.1+build.2")
        )

    def test_manifest_version_and_identity_mismatch_fail_before_build(self):
        self.git("tag", "fern/v0.3.0", self.commit)
        with self.assertRaisesRegex(ValueError, "manifest"):
            self.prepare("fern/v0.3.0")
        self.assertFalse(self.output.exists())
        manifest = self.root / "skills/fern/.codex-plugin/plugin.json"
        manifest.write_text(
            json.dumps({"name": "wrong", "version": "0.2.0"}), encoding="utf-8"
        )
        commit = self.commit_all()
        self.git("tag", "-f", self.tag, commit)
        self.git("update-ref", "refs/remotes/origin/main", commit)
        with self.assertRaisesRegex(ValueError, "manifest"):
            prepare_release(self.root, self.tag, commit, self.output)

    def test_main_advance_and_worktree_changes_never_replace_event_source(self):
        skill = self.root / "skills/fern/task/SKILL.md"
        original = skill.read_bytes()
        skill.write_bytes(original + b"Later committed instructions.\n")
        newer = self.commit_all()
        self.git("update-ref", "refs/remotes/origin/main", newer)
        skill.write_bytes(b"Malformed uncommitted source")
        paths = self.prepare()
        with zipfile.ZipFile(paths[0]) as archive:
            self.assertEqual(archive.read("skills/task/SKILL.md"), original)
        self.assertEqual(
            json.loads(paths[2].read_bytes())["source"]["commit"], self.commit
        )

    def test_wrong_event_commit_and_unmerged_tag_are_rejected(self):
        (self.root / "later.txt").write_text("later", encoding="utf-8")
        newer = self.commit_all()
        with self.assertRaisesRegex(ValueError, "Tag and event"):
            prepare_release(self.root, self.tag, newer, self.output)
        self.git("tag", "-f", self.tag, newer)
        with self.assertRaisesRegex(ValueError, "origin/main"):
            prepare_release(self.root, self.tag, newer, self.output)

    def test_new_draft_has_three_verified_assets_and_never_publishes(self):
        self.prepare()
        result = self.draft()
        creates = [call for call in self.client.calls if call[0] == "POST"]
        self.assertEqual(len(creates), 1)
        self.assertTrue(creates[0][2]["draft"])
        self.assertEqual(creates[0][2]["target_commitish"], self.commit)
        self.assertIn("Fern release note.", creates[0][2]["body"])
        self.assertIn(self.commit, creates[0][2]["body"])
        self.assertNotIn("Future notes", creates[0][2]["body"])
        self.assertNotIn("Another plugin", creates[0][2]["body"])
        self.assertEqual(
            len([call for call in self.client.calls if call[0] == "UPLOAD"]), 3
        )
        self.assertEqual(len(result["assets"]), 3)
        self.assertTrue(result["draft"])
        self.assertTrue((self.output / "release-result.json").is_file())
        self.assertFalse(
            any(call[0] in {"PATCH", "DELETE"} for call in self.client.calls)
        )

    def test_existing_draft_rerun_is_noop_and_missing_asset_resumes(self):
        self.prepare()
        self.draft()
        self.client.calls.clear()
        self.draft()
        self.assertEqual(self.mutations(), [])
        missing_id = next(
            key
            for key, value in self.client.assets.items()
            if value["name"].endswith(".sha256")
        )
        missing_name = self.client.assets.pop(missing_id)["name"]
        del self.client.content[missing_id]
        self.client.calls.clear()
        self.draft()
        self.assertEqual(self.mutations(), [("UPLOAD", missing_name, None)])

    def test_mismatched_existing_asset_blocks_all_uploads_without_clobber(self):
        self.prepare()
        self.draft()
        ids = list(self.client.assets)
        del self.client.assets[ids[0]]
        self.client.content[ids[-1]] = b"different existing artifact"
        self.client.calls.clear()
        with self.assertRaisesRegex(ValueError, "Existing release asset differs"):
            self.draft()
        self.assertEqual(self.mutations(), [])
        self.assertEqual(self.client.content[ids[-1]], b"different existing artifact")

    def test_published_release_is_rejected_unchanged(self):
        self.prepare()
        self.client.releases.append({"id": 42, "tag_name": self.tag, "draft": False})
        with self.assertRaisesRegex(ValueError, "unpublished draft"):
            self.draft()
        self.assertEqual(self.mutations(), [])

    def test_listing_auth_failure_is_not_absence(self):
        self.prepare()
        self.client.fail_listing = True
        with self.assertRaisesRegex(RuntimeError, "401"):
            self.draft()
        self.assertEqual(self.mutations(), [])

    def test_remote_tag_movement_blocks_create_and_upload(self):
        self.prepare()
        self.client.moved_on_read = 2
        with self.assertRaisesRegex(ValueError, "Remote tag"):
            self.draft()
        self.assertEqual(self.mutations(), [])
        self.client.moved_on_read = None
        self.client.tag_reads = 0
        self.draft()
        del self.client.assets[next(iter(self.client.assets))]
        self.client.calls.clear()
        self.client.tag_reads = 0
        self.client.moved_on_read = 2
        with self.assertRaisesRegex(ValueError, "Remote tag"):
            self.draft()
        self.assertEqual(self.mutations(), [])

    def test_annotated_remote_tag_and_paginated_draft_discovery(self):
        self.prepare()
        self.client.annotated = True
        self.client.releases = [
            {"id": index + 100, "tag_name": f"other/v0.0.{index}", "draft": False}
            for index in range(100)
        ]
        self.client.releases.append(
            {
                "id": 42,
                "tag_name": self.tag,
                "draft": True,
                "html_url": "https://github.com/example/skills/releases/tag/test",
            }
        )
        self.draft()
        self.assertTrue(
            any("releases?per_page=100&page=2" in call[1] for call in self.client.calls)
        )
        self.assertFalse(any(call[0] == "POST" for call in self.client.calls))

    def test_tampered_prepared_artifact_fails_before_remote_requests(self):
        paths = self.prepare()
        paths[0].write_bytes(b"tampered")
        with self.assertRaisesRegex(ValueError, "Prepared artifact differs"):
            self.draft()
        self.assertEqual(self.client.calls, [])

    def test_rest_errors_propagate_and_redirects_do_not_leak_token(self):
        client = GitHub("synthetic-token")
        for code in (401, 403, 404, 500):
            with (
                self.subTest(code=code),
                patch.object(
                    client.opener,
                    "open",
                    side_effect=urllib.error.HTTPError(
                        "https://api.github.com/test",
                        code,
                        "failure",
                        {},
                        io.BytesIO(b"{}"),
                    ),
                ),
            ):
                with self.assertRaisesRegex(RuntimeError, f"HTTP {code}"):
                    client.json("GET", "/test")
        with patch.object(
            client.opener, "open", side_effect=urllib.error.URLError("network")
        ):
            with self.assertRaisesRegex(RuntimeError, "connection failed"):
                client.json("GET", "/test")
        with self.assertRaisesRegex(ValueError, "official"):
            client.request("GET", "https://example.com/test")
        request = urllib.request.Request(
            "https://api.github.com/asset",
            headers={"Authorization": "Bearer synthetic-token"},
        )
        redirect = SecureRedirect().redirect_request(
            request,
            None,
            302,
            "redirect",
            {},
            "https://release-assets.githubusercontent.com/file",
        )
        self.assertIsNone(redirect.get_header("Authorization"))
        with self.assertRaisesRegex(ValueError, "HTTPS"):
            SecureRedirect().redirect_request(
                request, None, 302, "redirect", {}, "http://example.com/file"
            )

    def test_rest_pagination_serialization_and_binary_upload_transport(self):
        client = GitHub("synthetic-token")
        items = [{"id": number} for number in range(100)]
        responses = [
            io.BytesIO(json.dumps(items).encode()),
            io.BytesIO(b'[{"id": 100}]'),
        ]
        with patch.object(client.opener, "open", side_effect=responses) as opened:
            self.assertEqual(
                len(list(pages(client, "/repos/example/skills/releases"))), 101
            )
            self.assertTrue(
                opened.call_args_list[1].args[0].full_url.endswith("page=2")
            )
            self.assertEqual(
                opened.call_args.args[0].get_header("Authorization"),
                "Bearer synthetic-token",
            )
        with patch.object(
            client.opener, "open", return_value=io.BytesIO(b'{"draft": true}')
        ) as opened:
            self.assertTrue(
                client.json("POST", "/repos/example/skills/releases", {"draft": True})[
                    "draft"
                ]
            )
            self.assertEqual(json.loads(opened.call_args.args[0].data), {"draft": True})
        asset = Path(self.temporary.name) / "fern-1.2.3+build.zip"
        asset.write_bytes(b"synthetic ZIP bytes")
        with patch.object(
            client.opener, "open", return_value=io.BytesIO(b'{"id": 1}')
        ) as opened:
            self.assertEqual(client.upload("example/skills", 42, asset), {"id": 1})
            request = opened.call_args.args[0]
            self.assertTrue(request.full_url.startswith("https://uploads.github.com/"))
            self.assertIn("%2Bbuild.zip", request.full_url)
            self.assertEqual(request.data, asset.read_bytes())
            self.assertEqual(request.get_header("Content-type"), "application/zip")

    def test_workflow_is_tag_only_pinned_and_token_scoped(self):
        workflow = (
            Path(__file__).resolve().parents[1] / ".github/workflows/release-plugin.yml"
        )
        data = yaml.load(workflow.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
        self.assertEqual(data["on"], {"push": {"tags": ["*/v*"]}})
        self.assertEqual(data["concurrency"]["cancel-in-progress"], "false")
        job = data["jobs"]["draft"]
        self.assertEqual(job["runs-on"], "ubuntu-24.04")
        self.assertEqual(job["if"], "github.event.deleted == false")
        self.assertEqual(job["timeout-minutes"], "15")
        for step in job["steps"]:
            if "uses" in step:
                self.assertRegex(step["uses"], r"@[0-9a-f]{40}$")
            if "GH_TOKEN" in step.get("env", {}):
                self.assertIn("release_plugin.py draft", step["run"])
        self.assertNotIn("GH_TOKEN", job["env"])
        checkout = job["steps"][0]["with"]
        self.assertEqual(checkout["ref"], "${{ github.sha }}")
        self.assertEqual(checkout["persist-credentials"], "false")


if __name__ == "__main__":
    unittest.main()
