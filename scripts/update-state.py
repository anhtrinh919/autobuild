#!/usr/bin/env python3
"""Write `state.json` from what is on disk.

Every skill's Close step runs this. It reads the project root, and records
which of the four root documents are there, and which document each phase in
`spec/` holds. `autobuild:autobuild` reads the result to route the next skill.

Run it from the project root, or give the root as the one argument.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# The root documents the ladder writes, and the name each one takes in state.
ROOT = {"prd": "prd.md", "changelog": "changelog.md", "backlog": "backlog.md"}

# One phase's documents, in the order the ladder writes them.
PHASE = {
    "user_stories": "user-stories.md",
    "design_brief": "design-brief.md",
    "contract": "contract.md",
    "features": "features.md",
    "plan": "plan.md",
}


def read(root: Path) -> dict:
    """What this project holds, as `state.json` records it."""
    held: dict = {name: (root / one).is_file() for name, one in ROOT.items()}
    phases = sorted(
        (one for one in (root / "spec").glob("*/") if one.is_dir()),
        key=lambda one: [
            int(part) if part.isdigit() else part
            for part in one.name.replace("-", ".").split(".")
        ],
    )
    held["phases"] = {
        one.name: {name: (one / doc).is_file() for name, doc in PHASE.items()}
        for one in phases
    }
    return held


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    if not (root / "spec").is_dir():
        print(f"No spec/ under {root}.", file=sys.stderr)
        return 1
    held = read(root)
    (root / "state.json").write_text(json.dumps(held, indent=2) + "\n")
    for name, one in held["phases"].items():
        missing = [doc for doc, there in one.items() if not there]
        print(f"{name}: {'complete' if not missing else 'wants ' + ', '.join(missing)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
