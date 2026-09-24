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
    if skill.parent.name not in {"autobuild", "migrate"}:
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
assert "never reads the plan's tasks" in implement_text, "acceptance tests share an author with the code"
assert "Enter plan mode." in implement_text, "implement does not enter plan mode"
assert "Exit plan mode. This is the plan's approval gate." in implement_text, "implement does not gate on plan mode"

for name in ("explore", "spec", "polish"):
    text = (root / f"skills/{name}/SKILL.md").read_text()
    assert "`crawler`" in text, f"{name} does not dispatch crawler for research"

wrap_text = (root / "skills/wrap/SKILL.md").read_text()
assert "`dogfood`" in implement_text, "implement does not spawn dogfood as the product judge"
assert "Never give it the contract, the plan, the diff" in implement_text, "product judge sees the paperwork"
assert "`/browse`" in wrap_text, "wrap does not drive screens through /browse"
assert "`/browse`" in (root / "skills/spec/SKILL.md").read_text(), "spec does not walk trials through /browse"

router = (root / "skills/autobuild/SKILL.md").read_text()
for route in ("autobuild:migrate", "autobuild:explore", "autobuild:spec", "autobuild:implement", "autobuild:wrap", "roadmap is done"):
    assert route in router, f"router lacks {route}"

assert "status is `verified`" in router, "router does not guard unfinished implementation"
assert "exact heading `## <phase-id>`" in router, "router does not use exact phase closure"
assert "status `shipped`" in router, "router does not close phases by roadmap status"
assert "## Docs" in (root / "stack.md").read_text(), "living and snapshot docs are undefined"
assert "autobuild.polish-action" in router, "router cannot recover an interrupted polish action"
assert "working or committed `polish-plan.md`" in router, "router cannot recover polish collection"

migrate = (root / "skills/migrate/SKILL.md").read_text()
assert "Upgrade mode" in migrate, "migration lacks an in-place Autobuild upgrade"
assert "legacy-snapshot" in migrate, "upgrade cannot convert a compatibility project"
assert "remove `state.json`" in migrate, "upgrade leaves routing state behind"
assert "`state.json`, `.build-state.json`, or `specs/`" in router, "router cannot send older projects to migrate"
assert "Never stage a pre-existing diff" in migrate, "upgrade can absorb unrelated work"
assert "autobuild-migrate-untracked" in migrate, "upgrade cannot verify untracked files"
assert "current phase is none" in migrate, "upgrade cannot preserve a completed roadmap"
assert migrate.index("Keep their Git-local record") < migrate.index("commit only the migration") < migrate.index("remove the Git-local hash record"), "upgrade drops its recovery record before commit"

wrap = (root / "skills/wrap/SKILL.md").read_text()

polish = (root / "skills/polish/SKILL.md").read_text()
assert "Status: intake" in polish, "polish lacks recoverable pre-branch state"
assert "first batch with `Status: pending` resumes Step 4" in polish, "polish cannot recover an unplanned batch"
assert "first batch with `Status: approved` resumes Step 5" in polish, "polish cannot recover an approved batch"
assert "Write the action last" in polish, "polish action marker is not crash-safe"
assert polish.index("An intake plan resumes Step 1") < polish.index("Otherwise, read the planning or draining plan"), "polish restores a branch before checking intake status"
assert "Enter plan mode." in polish, "polish does not plan a batch in plan mode"
assert "Exit plan mode. This is the batch's approval gate." in polish, "polish does not gate a batch on plan mode"
assert "Ask the user to confirm the items and the split" in polish, "polish batches without the user's confirmation"
assert "who it affects and what it costs them" in polish, "polish confirmation omits item impact"
assert "Return to Step 4 while a pending batch remains" in polish, "polish drains every batch on one plan"
assert "changes the root cause or fix returns the item to Step 4" in polish, "polish can drift from the approved diagnosis"
assert "Before leaving the polish branch, remove `polish-plan.md`" in polish, "polish loses recovery before branch fate"

backlog = (root / "templates/backlog.md").read_text()
assert "Open entries: 30 words, 1 sentence, 1 bullet" in backlog, "backlog entries can expand beyond one line"
assert "## Polish intake" not in backlog and "## Active polish" not in backlog, "backlog still stores polish working state"

ladder = (root / "stack.md").read_text()
assert "## Subagent tiers" in ladder, "dispatch tiers are undocumented"
assert "parent session keeps its user-selected model" in ladder, "tiers can override the parent model"
for tier in ("mechanical", "standard", "deliberate", "flagship", "exceptional"):
    assert tier in ladder, f"tier mapping lacks {tier}"
assert "Sonnet 5" in ladder and "Opus 5" in ladder, "Claude tier mapping is missing"
assert "Codex" not in ladder, "Codex tier mapping belongs in the Codex source repo"

plan = (root / "templates/plan.md").read_text()
assert "Tier: `standard`, `deliberate`, `flagship`, or `exceptional`" in plan, "tasks lack a durable tier"

implement = (root / "skills/implement/SKILL.md").read_text()
for phrase in ("writer subagent", "A plan without Tier uses standard", "must not commit", "Files do not overlap", "stop before editing when it finds an ungraded decision", "Use exceptional for an exceptional batch"):
    assert phrase in implement, f"implement lacks {phrase}"

research = (root / "templates/research.md").read_text().splitlines()
assert research[2].endswith("sentence. 2 sentences a line."), "research schema lacks caps"
assert any(l.startswith("This phase's research only.") for l in research), "research schema lacks phase scope"

assert not (root / "scripts/update-state.py").exists(), "obsolete state script remains"
assert not (root / "commands").exists(), "legacy command folder remains"
assert (root / "templates/writing-rule.md").exists(), "writing-rule scaffold is missing"
for skill in skills:
    assert "/schemas/" not in skill.read_text(), f"{skill} points at an old schema folder"
print("Claude skill checks passed")
