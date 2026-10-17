"""Generate one isolated reuse example into a new .blend file; no scene reset."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import scene_components as c


def example(variant):
    if variant == "courtyard":
        return (
            c.frame("canopy", 3.4, 4.6, 2.8)
            + c.place(c.table("prep", 2.2, 0.8, 0.9), (-3, 0, 0))
            + c.place(c.fence("fence", 5, 1.8, count=16), (0, 3, 0))
        )
    if variant == "workshop":
        benches = c.repeat(c.table("bench", 1.3, 0.65, 1.05), 3, (1.7, 0, 0))
        return (
            c.place(benches, (-2, -1, 0), (0, 1, 0))
            + c.place(c.frame("rack", 2.6, 1.2, 2.2, 0.08, 0.1), (2, 0, 0), (0, 1, 0))
            + c.place(c.fence("screen", 3, 1.4, count=10), (3, 0, 0), (0, 1, 0))
        )
    raise ValueError("Unknown example")


def main():
    import bpy

    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--variant", choices=["courtyard", "workshop"], required=True)
    p.add_argument("--output", required=True, type=Path)
    args = p.parse_args(
        sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    )
    if args.output.exists() or args.output.suffix.lower() != ".blend":
        raise ValueError("Expected a new .blend path")
    if bpy.data.filepath:
        raise ValueError("Run with --factory-startup, not an open source file")
    parts = example(args.variant)
    objects = c.build_blender(
        parts,
        "Environment",
        {"surface": (0.45, 0.25, 0.12, 1), "structure": (0.16, 0.09, 0.045, 1)},
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(args.output))
    print(
        "COMPONENT_EXAMPLE_OK",
        json.dumps(
            {
                "variant": args.variant,
                "objects": len(objects),
                "bounds": c.bounds(parts),
            }
        ),
    )


if __name__ == "__main__":
    main()
