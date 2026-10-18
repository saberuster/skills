"""Apply the bundled Fern resources to a project (Python 3.11+)."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

# Read-only checks must not create __pycache__ in the installed skill package.
sys.dont_write_bytecode = True

from resources import apply_resources  # noqa: E402

PACKAGE = Path(__file__).resolve().parents[1]
FAILURES = {"conflict", "failed", "different", "missing"}
RUNTIME = "File application only; fresh-session discovery, models and runtime support are not verified"


def parser():
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--project", type=Path, required=True)
    result.add_argument("--check", action="store_true", help="Compare without writing")
    return result


def install(args):
    root = Path(os.path.abspath(args.project))
    if not root.is_dir():
        raise ValueError("Project directory must already exist")
    return {
        "project": str(root),
        "check": args.check,
        "results": apply_resources(PACKAGE, root, check=args.check),
        "runtime": RUNTIME,
    }


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        report = install(args)
    except (OSError, ValueError) as error:
        report = {
            "project": os.path.abspath(args.project),
            "check": args.check,
            "results": [{"status": "failed", "detail": str(error)}],
            "runtime": RUNTIME,
        }
    print(json.dumps(report, indent=2))
    return int(any(item.get("status") in FAILURES for item in report["results"]))


if __name__ == "__main__":
    sys.exit(main())
