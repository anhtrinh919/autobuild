---
name: autobuild
description: Finds the open build phase and loads the next skill. Trigger when users start, resume, continue, or ask what comes next.
---

# Autobuild

Reads the branch, local Git config, committed documents, `backlog.md`, and `spec/`. Writes nothing itself.

Read `../../stack.md` first. Resolve `../../` paths against `${CLAUDE_PLUGIN_ROOT}`.

## Rules

Wiring only. Every skill it hands off to owns its own steps and gates.

## Step 1 — Read the project

Inspect the current branch, local Git config, committed documents, the working and committed `backlog.md`, and phase directories under `spec/`.

Read lifecycle statuses with `git show HEAD:<path>`, not an uncommitted working file.

Check these project states in order. Stop at the first match.

A local `autobuild.polish-action` Git config value, or a working or committed `polish-plan.md`, marks an interrupted Polish run. Name `autobuild:polish`.

A committed `state.json` or `.build-state.json`, a committed `specs/` directory with no PRD, or a `migrating` PRD, marks an older project. Name `autobuild:migrate`. It picks its own mode.

No `prd.md` marks a fresh idea. Name `autobuild:explore` in global mode.

A committed PRD whose status is missing or not `approved` names `autobuild:explore` in global mode.

Polish, older, fresh, and draft projects skip Steps 2 and 3.

Gate: exactly one state is chosen: polish, older, fresh, draft, or current.

## Step 2 — Find the open phase

Run this step only for a current project.

Read `prd.md`'s Roadmap. It lists every phase, in build order.

Each roadmap line names one exact `spec/<phase-id>` path. Never derive a phase path from its display name.

If old roadmap lines lack IDs, propose `phase-<N>-<slug>` IDs. Update them only after user approval.

When the open phase has a plan, read its base branch roadmap with `git show <base>:prd.md`. Otherwise read committed `HEAD:prd.md`.

A phase closes when its roadmap line has status `shipped`.

A roadmap line with no status closes only when the matching changelog has the exact heading `## <phase-id>`.

Walk the roadmap phases in order. The first phase not closed is open.

No `spec/<phase>/` directory for the open phase names `autobuild:explore` in per-phase mode.

Gate: exactly one phase is named open, or every phase in the roadmap is closed.

## Step 3 — Route inside the open phase

Run this step only when the current project has an open phase directory.

Check the open phase's directory in this order: `user-stories.md`, `contract.md`, then `plan.md`.

The first incomplete document names the next skill:

- committed `user-stories.md` missing or not `approved` → `autobuild:explore`, per-phase mode
- a quick-track phase skips the spec documents
- committed `contract.md` missing or not `approved` → `autobuild:spec`. A statusless contract counts as `approved` when committed `features.md` is `approved`
- `plan.md` missing → `autobuild:implement`
- committed `plan.md` status missing or not `verified` → `autobuild:implement`
- committed `plan.md` status is `verified` → `autobuild:wrap`

Gate: exactly one skill is named, matching the first gap found.

## Hand-off

An interrupted Polish run routes to `autobuild:polish`.

An older project routes to `autobuild:migrate`.

A fresh project routes to `autobuild:explore` in global mode.

A draft PRD routes to `autobuild:explore` in global mode.

Every phase closed means the roadmap is done. Say so, and stop.

Otherwise, say which phase is open and which document or directory is missing. Then call the Skill tool with the named skill's qualified id.

Gate: the Skill tool was called with the right qualified id, or the roadmap-done message appeared — never both.
