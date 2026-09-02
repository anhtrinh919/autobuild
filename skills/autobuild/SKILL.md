---
name: autobuild
description: Finds the open build phase and loads the next skill. Trigger when users start, resume, continue, or ask what comes next.
---

# Autobuild

- Step: one unit of work.
- Gate: the check at the end of a step.
- Pass a gate → move to the next step.
- Fail a gate → redo the step, using the gate's findings.
- Fail the same gate twice → stop, ask the user.

Resolve every `../../` path from this `SKILL.md`. In Claude Code, that root is `${CLAUDE_PLUGIN_ROOT}`.

Read `../../ladder.md` first — it shows where this skill sits in the whole stack.

Read the project's `writing-rule.md` next — scaffold it from `../../writing-rule.md` if missing. It sets the prose style for every doc this skill writes.

Wiring only. Every skill it hands off to owns its own steps and gates.

## Step 1 — Read the project

Inspect the current branch, local Git config, committed documents, the working and committed `backlog.md`, and phase directories under `spec/`.

Read lifecycle statuses with `git show HEAD:<path>`, not an uncommitted working file.

Check these project states in order. Stop at the first match.

A local `autobuild.polish-action` Git config value, a Polish intake or Active polish block in the working or committed `backlog.md`, or a `polish-<timestamp>` branch marks an interrupted Polish run. Name `autobuild:polish`.

A committed `state.json` plus a committed statusless or `migrating` PRD marks an earlier Autobuild project when the state shape matches.

That state shape has `prd`, `changelog`, `backlog`, and `phases` keys. Name `autobuild:migrate` in upgrade mode.

A committed state whose routing mode is `legacy-snapshot` and an approved PRD marks a compatibility project.

A legacy signature plus no PRD marks an old-stack project.

A `migrating` PRD without compatible `state.json` also marks an old-stack project.

Legacy signatures are `.build-state.json` and `specs/`.

An old-stack project names `autobuild:migrate`.

No `prd.md`, and no old-stack signature, marks a fresh idea. Name `autobuild:explore` in global mode.

A committed PRD whose status is missing or not `approved` names `autobuild:explore` in global mode.

Polish, earlier Autobuild, old-stack, fresh, and draft projects skip Steps 2 and 3.

Gate: exactly one state is chosen: polish, earlier Autobuild, old-stack, fresh, draft, compatibility, or current.

## Step 2 — Find the open phase

Run this step only for a current or compatibility project.

Read `prd.md`'s Roadmap. It lists every phase, in build order.

Each roadmap line names one exact `spec/<phase-id>` path. Never derive a phase path from its display name.

If old roadmap lines lack IDs, propose `phase-<N>-<slug>` IDs. Update them only after user approval.

For a compatibility project, treat every phase before its recorded `through` boundary as closed.

When `phase` is null, scan only phases after `through` with current routing.

Otherwise test the recorded phase against the working `changelog.md`.

An absent exact heading makes that phase open and skips the remaining scan. A present heading limits the scan to later phases.

For current routing, read a plan's base branch changelog with `git show <base>:changelog.md`.

For current routing without a plan, read committed `HEAD:changelog.md`.

A phase closes only when that changelog has the exact heading `## <phase-id>`.

Walk the eligible roadmap phases in order. The first phase without that exact heading is open.

No `spec/<phase>/` directory for the open phase names `autobuild:explore` in per-phase mode.

Gate: exactly one phase is named open, or every phase in the roadmap is closed.

## Step 3 — Route inside the open phase

Run this step only when the current or compatibility project has an open phase directory.

Check the open phase's directory in this order: `user-stories.md`, the three spec docs, then `plan.md`.

When the open phase matches the compatibility snapshot, treat each recorded and still-present document as complete.

Apply the lifecycle-status rules to every other document. Later phases use lifecycle statuses for every document.

The first incomplete document names the next skill:

- committed `user-stories.md` missing or not `approved` → `autobuild:explore`, per-phase mode
- a spec document missing, or committed `features.md` not `approved` → `autobuild:spec`
- `plan.md` missing → `autobuild:implement`
- committed `plan.md` status missing or not `verified` → `autobuild:implement`
- committed `plan.md` status is `verified` → `autobuild:wrap`

Gate: exactly one skill is named, matching the first gap found.

## Step 4 — Hand off

An interrupted polish branch loads and follows `autobuild:polish`.

An earlier Autobuild project loads and follows `autobuild:migrate` in upgrade mode.

An old-stack project loads and follows `autobuild:migrate`.

A fresh project loads and follows `autobuild:explore` in global mode.

A draft PRD loads and follows `autobuild:explore` in global mode.

Every phase closed means the roadmap is done. Say so, and stop.

Otherwise, say which phase is open and which document or directory is missing. Load and follow the named qualified skill now.

Gate: the named skill loads, or the roadmap-done message appears. Exactly one outcome occurs.
