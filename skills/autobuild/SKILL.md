---
name: autobuild
description: Finds where a build stands — no docs yet, mid-phase, or between phases — and hands off to the right skill to start it or pick it up again. Trigger on /autobuild, or whenever the user wants to start a new build, resume one, continue where they left off, or asks what's next.
---

# Autobuild

- Step: one unit of work.
- Gate: the check at the end of a step.
- Pass a gate → move to the next step.
- Fail a gate → redo the step, using the gate's findings.
- Fail the same gate twice → stop, ask the user.

Read `${CLAUDE_PLUGIN_ROOT}/ladder.md` first — it shows where this skill sits in the whole stack.

Wiring only. Every skill it hands off to owns its own steps and gates.

## Step 1 — Read state

Run `${CLAUDE_PLUGIN_ROOT}/scripts/update-state.py`, then read `state.json` at the project root.

A `.build-state.json` file, or a `specs/` directory, with no `prd.md` → an old-stack project. Tell the user to run `autobuild:migrate` first, and stop.

No `prd.md`, and no old-stack signature → a fresh idea, not a resume. Call `autobuild:explore`, global mode.

Gate: `state.json` is current. `prd.md`'s existence, and the old-stack signature, are both checked.

## Step 2 — Find the open phase

Read `prd.md`'s Roadmap. It lists every phase, in build order.

A phase is closed once `changelog.md` holds its entry. Walk the roadmap in order; the first phase without one is open.

No `spec/<phase>/` directory yet for the open phase → call `autobuild:explore`, per-phase mode, for it.

Gate: exactly one phase is named open, or every phase in the roadmap is closed.

## Step 3 — Route inside the open phase

Check the open phase's directory against `state.json`, in this order: `user-stories.md`, then `design-brief.md` + `contract.md` + `features.md`, then `plan.md`.

The first missing doc names the next skill:

- `user-stories.md` missing → `autobuild:explore`, per-phase mode
- `design-brief.md`, `contract.md`, or `features.md` missing → `autobuild:spec`
- `plan.md` missing → `autobuild:implement`
- every doc present → `autobuild:wrap`

Gate: exactly one skill is named, matching the first gap found.

## Step 4 — Hand off

Every phase closed, with none left in the roadmap → the roadmap is done. Say so, and stop.

Otherwise, say which phase is open and which doc is missing. Then call the Skill tool with the named skill's qualified id.

Gate: the Skill tool was called with the right qualified id, or the roadmap-done message was given — never both.
