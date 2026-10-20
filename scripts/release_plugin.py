"""Build a tagged plugin and create or resume its GitHub draft release."""

import argparse
import hashlib
import json
import os
import re
import subprocess
import tempfile
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import quote, urlencode, urlsplit

try:
    from .package_plugin import NAME, ROOT, SEMVER, git, package_plugin
except ImportError:
    from package_plugin import NAME, ROOT, SEMVER, git, package_plugin


def parse_tag(tag):
    parts = tag.split("/v")
    if (
        len(parts) != 2
        or len(parts[0]) > 64
        or not NAME.fullmatch(parts[0])
        or not SEMVER.fullmatch(parts[1])
    ):
        raise ValueError("Tag must be <plugin>/v<strict-semver>")
    return tuple(parts)


def validate_source(root, tag, commit):
    """Resolve only the event commit; main is an ancestry check, never a source."""
    plugin, version = parse_tag(tag)
    if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", commit):
        raise ValueError("Event commit must be a full lowercase Git object ID")
    resolved = (
        git(root, "rev-parse", "--verify", f"{commit}^{{commit}}").decode().strip()
    )
    tagged = (
        git(root, "rev-parse", "--verify", f"refs/tags/{tag}^{{commit}}")
        .decode()
        .strip()
    )
    if resolved != commit or tagged != commit:
        raise ValueError("Tag and event commit do not match")
    try:
        git(root, "merge-base", "--is-ancestor", commit, "refs/remotes/origin/main")
    except subprocess.CalledProcessError as error:
        raise ValueError("Event commit must belong to fetched origin/main") from error
    native = json.loads(
        git(
            root,
            "cat-file",
            "blob",
            f"{commit}:skills/{plugin}/.codex-plugin/plugin.json",
        )
    )
    if native.get("name") != plugin or native.get("version") != version:
        raise ValueError(
            "Tagged plugin name/version do not match the committed manifest"
        )
    return plugin, version


def prepare_release(root, tag, commit, output_dir):
    plugin, _ = validate_source(root, tag, commit)
    return package_plugin(root, plugin, output_dir, commit)


def release_notes(root, plugin, version, commit):
    """Use only this plugin/version section from the immutable source commit."""
    summary = f"Portable {plugin} {version} plugin.\n\nSource commit: `{commit}`.\n"
    if not git(root, "ls-tree", "--name-only", commit, "--", "CHANGELOG.md").strip():
        return summary
    changelog = git(root, "cat-file", "blob", f"{commit}:CHANGELOG.md").decode("utf-8")
    heading = re.compile(
        rf"^## {re.escape(plugin)} {re.escape(version)} - [0-9]{{4}}-[0-9]{{2}}-[0-9]{{2}}\s*$",
        re.MULTILINE,
    )
    matches = list(heading.finditer(changelog))
    if len(matches) > 1:
        raise ValueError("Duplicate plugin/version changelog sections")
    if matches:
        section = changelog[matches[0].end() :]
        following = re.search(r"^## ", section, re.MULTILINE)
        if following:
            section = section[: following.start()]
        if section.strip():
            return section.strip() + f"\n\nSource commit: `{commit}`.\n"
    return summary


class SecureRedirect(urllib.request.HTTPRedirectHandler):
    """Keep the GitHub token off cross-host asset download redirects."""

    def redirect_request(self, request, fp, code, message, headers, newurl):
        if urlsplit(newurl).scheme != "https":
            raise ValueError("GitHub redirects must use HTTPS")
        redirected = super().redirect_request(
            request, fp, code, message, headers, newurl
        )
        if (
            redirected is not None
            and urlsplit(request.full_url).netloc != urlsplit(newurl).netloc
        ):
            redirected.remove_header("Authorization")
        return redirected


class GitHub:
    """Small github.com REST boundary; every HTTP or authentication error fails."""

    def __init__(self, token):
        if not token:
            raise ValueError("GH_TOKEN is required for draft release uploads")
        self.token = token
        self.opener = urllib.request.build_opener(SecureRedirect())

    def request(self, method, url, body=None, *, binary=False, content_type=None):
        parsed = urlsplit(url)
        if parsed.scheme != "https" or parsed.netloc not in {
            "api.github.com",
            "uploads.github.com",
        }:
            raise ValueError("Only official github.com API/upload hosts are supported")
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/octet-stream"
            if binary
            else "application/vnd.github+json",
            "X-GitHub-Api-Version": "2026-03-10",
            "User-Agent": "skills-plugin-release",
        }
        if body is not None:
            headers["Content-Type"] = content_type or "application/json"
        request = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            with self.opener.open(request, timeout=60) as response:
                data = response.read()
        except urllib.error.HTTPError as error:
            raise RuntimeError(f"GitHub {method} failed: HTTP {error.code}") from error
        except urllib.error.URLError as error:
            raise RuntimeError(f"GitHub {method} connection failed") from error
        return data if binary else json.loads(data)

    def json(self, method, path, body=None):
        return self.request(
            method,
            "https://api.github.com" + path,
            None if body is None else json.dumps(body).encode(),
        )

    def download(self, path):
        return self.request("GET", "https://api.github.com" + path, binary=True)

    def upload(self, repo, release_id, path):
        content_type = (
            "application/zip" if path.suffix == ".zip" else "application/octet-stream"
        )
        return self.request(
            "POST",
            f"https://uploads.github.com/repos/{repo}/releases/{release_id}/assets?"
            + urlencode({"name": path.name}),
            path.read_bytes(),
            content_type=content_type,
        )


def pages(client, path):
    page = 1
    while True:
        items = client.json("GET", f"{path}?per_page=100&page={page}")
        if not isinstance(items, list):
            raise ValueError("GitHub list response must be an array")
        yield from items
        if len(items) < 100:
            return
        page += 1


def check_remote_tag(client, repo, tag, commit):
    reference = client.json("GET", f"/repos/{repo}/git/ref/tags/{quote(tag, safe='')}")
    obj = reference["object"]
    for _ in range(10):
        if obj["type"] == "commit":
            if obj["sha"] != commit:
                raise ValueError("Remote tag no longer matches the event commit")
            return
        if obj["type"] != "tag" or not re.fullmatch(
            r"[0-9a-f]{40}|[0-9a-f]{64}", obj["sha"]
        ):
            raise ValueError("Unsupported remote tag object")
        obj = client.json("GET", f"/repos/{repo}/git/tags/{obj['sha']}")["object"]
    raise ValueError("Remote tag nesting exceeds supported depth")


def positive_id(value):
    if type(value) is not int or value <= 0:
        raise ValueError("GitHub object ID must be a positive integer")
    return value


def check_draft(release, tag):
    if release.get("draft") is not True or release.get("tag_name") != tag:
        raise ValueError("Release must still be an unpublished draft for this tag")
    return positive_id(release["id"])


def draft_release(root, tag, commit, repo, output_dir, client):
    """Verify all existing assets before adding anything; never replace assets."""
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*/[A-Za-z0-9][A-Za-z0-9_.-]*", repo):
        raise ValueError("Repository must be OWNER/REPO")
    plugin, version = validate_source(root, tag, commit)
    # Rebuild privately to prove that local artifacts still match the tag's bytes.
    with tempfile.TemporaryDirectory() as temporary:
        expected = package_plugin(root, plugin, temporary, commit)
        paths = [Path(output_dir) / path.name for path in expected]
        for path, built in zip(paths, expected, strict=True):
            if path.read_bytes() != built.read_bytes():
                raise ValueError(
                    f"Prepared artifact differs from tagged source: {path.name}"
                )
    base = f"/repos/{repo}"
    check_remote_tag(client, repo, tag, commit)
    matches = [
        release
        for release in pages(client, f"{base}/releases")
        if release.get("tag_name") == tag
    ]
    if len(matches) > 1:
        raise ValueError("Multiple releases already use this tag")
    release = matches[0] if matches else None
    if release is not None:
        release_id = check_draft(release, tag)
    else:
        check_remote_tag(client, repo, tag, commit)
        release = client.json(
            "POST",
            f"{base}/releases",
            {
                "tag_name": tag,
                "target_commitish": commit,
                "name": f"{plugin} {version}",
                "draft": True,
                "prerelease": "-" in version.split("+", 1)[0],
                "body": release_notes(root, plugin, version, commit),
            },
        )
        release_id = check_draft(release, tag)
    asset_path = f"{base}/releases/{release_id}/assets"
    assets = list(pages(client, asset_path))
    existing = {}
    for asset in assets:
        if asset["name"] in existing:
            raise ValueError("Duplicate release asset names")
        existing[asset["name"]] = asset
    missing = []
    for path in paths:
        asset = existing.get(path.name)
        if asset is None:
            missing.append(path)
            continue
        data = client.download(f"{base}/releases/assets/{positive_id(asset['id'])}")
        if asset.get("state") != "uploaded" or data != path.read_bytes():
            raise ValueError(f"Existing release asset differs: {path.name}")
    for path in missing:
        check_remote_tag(client, repo, tag, commit)
        check_draft(client.json("GET", f"{base}/releases/{release_id}"), tag)
        uploaded = client.upload(repo, release_id, path)
        if uploaded.get("name") != path.name or uploaded.get("state") != "uploaded":
            raise ValueError(f"Unexpected upload result: {path.name}")
        data = client.download(f"{base}/releases/assets/{positive_id(uploaded['id'])}")
        if data != path.read_bytes():
            raise ValueError(f"Uploaded asset verification failed: {path.name}")
    check_remote_tag(client, repo, tag, commit)
    check_draft(client.json("GET", f"{base}/releases/{release_id}"), tag)
    result = {
        "tag": tag,
        "commit": commit,
        "draft": True,
        "release_id": release_id,
        "url": release["html_url"],
        "assets": {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in paths
        },
    }
    (Path(output_dir) / "release-result.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("prepare", "draft"))
    parser.add_argument("--tag", required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("dist"))
    parser.add_argument("--repo", help="github.com OWNER/REPO; required for draft")
    args = parser.parse_args()
    try:
        if args.phase == "prepare":
            for path in prepare_release(ROOT, args.tag, args.commit, args.output_dir):
                print(path)
        else:
            if not args.repo:
                raise ValueError("--repo is required for draft")
            result = draft_release(
                ROOT,
                args.tag,
                args.commit,
                args.repo,
                args.output_dir,
                GitHub(os.environ.get("GH_TOKEN")),
            )
            print(json.dumps(result, indent=2))
    except (
        ValueError,
        OSError,
        KeyError,
        RuntimeError,
        subprocess.CalledProcessError,
    ) as error:
        parser.exit(1, f"Plugin release failed: {error}\n")


if __name__ == "__main__":
    main()
