"""Locate standalone packages and packages grouped under a workflow container."""

import re
from pathlib import Path


def skill_packages(root):
    """Return unique leaf names mapped to actual, unlinked package directories."""
    tree = Path(root) / "skills"
    if not tree.is_dir():
        raise ValueError("Source skill tree is missing")

    def check_tree(path):
        if path.is_symlink() or getattr(path.lstat(), "st_file_attributes", 0) & 0x400:
            raise ValueError(f"Refusing linked skill source: {path}")
        if path.is_dir():
            for child in path.iterdir():
                check_tree(child)

    check_tree(tree)
    packages = {}

    def add(directory):
        if not (directory / "SKILL.md").is_file():
            raise ValueError(
                f"{directory}: missing source SKILL.md; directory has no SKILL.md"
            )
        name = directory.name
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            raise ValueError(f"Invalid source skill name: {name}")
        if name in packages:
            raise ValueError(f"Duplicate source skill name: {name}")
        packages[name] = directory

    for directory in sorted(tree.iterdir()):
        if not directory.is_dir():
            continue
        if (directory / "SKILL.md").is_file():
            add(directory)
        else:
            children = [p for p in sorted(directory.iterdir()) if p.is_dir()]
            if not children:
                add(directory)
            for child in children:
                add(child)
    if not packages:
        raise ValueError("No source skills found")
    return dict(sorted(packages.items()))
