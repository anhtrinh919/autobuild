#!/usr/bin/env python3
"""Derive state.json from the project's own files. Never hand-edited.

Extend this as each new skill's own output needs tracking.
Do not add a field for a skill that isn't built yet.
"""
import json
from pathlib import Path

root = Path.cwd()

state = {
    "prd": (root / "prd.md").exists(),
    "changelog": (root / "changelog.md").exists(),
    "backlog": (root / "backlog.md").exists(),
    "phases": {},
}

spec_dir = root / "spec"
if spec_dir.is_dir():
    for phase_dir in sorted(p for p in spec_dir.iterdir() if p.is_dir()):
        state["phases"][phase_dir.name] = {
            "user_stories": (phase_dir / "user-stories.md").exists(),
            "design_brief": (phase_dir / "design-brief.md").exists(),
            "contract": (phase_dir / "contract.md").exists(),
            "plan": (phase_dir / "plan.md").exists(),
        }

(root / "state.json").write_text(json.dumps(state, indent=2) + "\n")
