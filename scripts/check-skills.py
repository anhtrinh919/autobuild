#!/usr/bin/env python3
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parent.parent
claude = json.loads((root / ".claude-plugin/plugin.json").read_text())
assert "commands" not in claude, "legacy command creates a duplicate skill"
assert not (root / ".codex-plugin").exists(), "Codex manifest belongs in the Codex source repo"

skills = sorted((root / "skills").glob("*/SKILL.md"))
assert len(skills) == 8, f"expected 8 skills, found {len(skills)}"

for skill in skills:
    text = skill.read_text()
    assert f"name: {skill.parent.name}" in text, f"wrong name in {skill}"
    assert "update-state.py" not in text, f"obsolete state script referenced in {skill}"
    assert "${CLAUDE_PLUGIN_ROOT}" in text, f"{skill} does not name the Claude plugin root"
    if skill.parent.name not in {"autobuild", "migrate", "wrap"}:
        assert "`state.json`" not in text, f"obsolete state routing remains in {skill}"
    for relative in re.findall(r"`(\.\./\.\./[^`]+)`", text):
        assert (skill.parent / relative).resolve().exists(), f"missing {relative} from {skill}"

# Claude-native mechanisms, restored after the Codex port genericised them.
handoffs = {
    "implement": "`autobuild:wrap` — call the Skill tool with that id",
    "spec": "`autobuild:implement` — call the Skill tool with that id",
    "explore": "`autobuild:spec` — call the Skill tool with that id",
    "migrate": "`autobuild:autobuild` — call the Skill tool with that id",
    "replan": "`autobuild:explore` in global mode — call the Skill tool with that id",
    "wrap": "`autobuild:explore` for the next phase — call the Skill tool with that id",
}
for name, phrase in handoffs.items():
    text = (root / f"skills/{name}/SKILL.md").read_text()
    assert phrase in text, f"{name} does not hand off through the Skill tool"

implement_text = (root / "skills/implement/SKILL.md").read_text()
assert "Enter plan mode." in implement_text, "implement does not enter plan mode"
assert "Exit plan mode. This is the plan's approval gate." in implement_text, "implement does not gate on plan mode"

for name in ("explore", "spec", "polish"):
    text = (root / f"skills/{name}/SKILL.md").read_text()
    assert "`crawler`" in text, f"{name} does not dispatch crawler for research"

wrap_text = (root / "skills/wrap/SKILL.md").read_text()
assert "`dogfood`" in wrap_text, "wrap does not spawn dogfood for the running surface"
assert "`/browse`" in wrap_text, "wrap does not drive screens through /browse"
assert "`/browse`" in (root / "skills/spec/SKILL.md").read_text(), "spec does not walk trials through /browse"

router = (root / "skills/autobuild/SKILL.md").read_text()
for route in ("autobuild:migrate", "autobuild:explore", "autobuild:spec", "autobuild:implement", "autobuild:wrap", "roadmap is done"):
    assert route in router, f"router lacks {route}"

assert "status is `verified`" in router, "router does not guard unfinished implementation"
assert "exact heading `## <phase-id>`" in router, "router does not use exact phase closure"
assert "autobuild.polish-action" in router, "router cannot recover an interrupted polish action"
assert "Polish intake" in router, "router cannot recover polish collection"
assert "earlier Autobuild project" in router, "router cannot detect the previous Autobuild schema"
assert "compatibility project" in router, "router cannot preserve previous completion routing"
assert "recorded phase against the working `changelog.md`" in router, "compatibility routing changes old phase closure"
assert "recorded `through` boundary" in router, "compatibility leaks into later phases"
assert "recorded and still-present document" in router, "compatibility does not preserve the old snapshot"

migrate = (root / "skills/migrate/SKILL.md").read_text()
assert "Upgrade mode" in migrate, "migration lacks an in-place Autobuild upgrade"
assert "legacy-snapshot" in migrate, "upgrade changes previous completion behavior"
assert "Never stage a pre-existing diff" in migrate, "upgrade can absorb unrelated work"
assert "autobuild-migrate-untracked" in migrate, "upgrade cannot verify untracked files"
assert "current phase is none" in migrate, "upgrade cannot preserve a completed roadmap"
assert migrate.index("Keep their Git-local record") < migrate.index("commit only the migration") < migrate.index("remove the Git-local hash record"), "upgrade drops its recovery record before commit"

wrap = (root / "skills/wrap/SKILL.md").read_text()
assert "legacy-snapshot" in wrap, "wrap cannot recover a previous plan's base"

polish = (root / "skills/polish/SKILL.md").read_text()
assert "Plan: pending" in polish, "polish lacks recoverable pre-branch state"
assert "uncommitted plan resumes Step 4" in polish, "polish cannot recover an uncommitted plan"
assert "Write the action last" in polish, "polish action marker is not crash-safe"

ladder = (root / "ladder.md").read_text()
assert "## Subagent tiers" in ladder, "dispatch tiers are undocumented"
assert "parent session keeps its user-selected model" in ladder, "tiers can override the parent model"
for tier in ("mechanical", "standard", "deliberate", "flagship", "exceptional"):
    assert tier in ladder, f"tier mapping lacks {tier}"
assert "Sonnet 5" in ladder and "Opus 5" in ladder, "Claude tier mapping is missing"
assert "Codex" not in ladder, "Codex tier mapping belongs in the Codex source repo"

plan = (root / "skills/implement/schemas/plan.md").read_text()
assert "Tier: `standard`, `deliberate`, `flagship`, or `exceptional`" in plan, "tasks lack a durable tier"

implement = (root / "skills/implement/SKILL.md").read_text()
for phrase in ("writer subagent", "A plan without Tier uses standard", "must not commit", "Files do not overlap", "stop before editing when it finds an ungraded decision", "Use exceptional for an exceptional batch"):
    assert phrase in implement, f"implement lacks {phrase}"

research = (root / "skills/spec/schemas/research.md").read_text().splitlines()
assert research[0].endswith("sentence. 2 sentences a line."), "research schema lacks caps"
assert research[4].startswith("This phase's research only."), "research schema lacks phase scope"

assert not (root / "scripts/update-state.py").exists(), "obsolete state script remains"
assert not (root / "commands/autobuild.md").exists(), "legacy command remains"
print("Claude skill checks passed")
