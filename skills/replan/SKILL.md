---
name: replan
description: Archives the current build and its docs, wipes accumulated context, and hands back a clean slate to pivot from. Trigger on /autobuild:replan, or whenever the user wants to change direction, pivot the idea, start over, or says this isn't working.
---

# Replan

- Step: one unit of work.
- Gate: the check at the end of a step.
- Pass a gate → move to the next step.
- Fail a gate → redo the step, using the gate's findings.
- Fail the same gate twice → stop, ask the user.

Read `${CLAUDE_PLUGIN_ROOT}/ladder.md` first — it shows where this skill sits in the whole stack.

A roadmap change alone is not a replan. That happens at Wrap's Finish, or at the next phase's Explore — no special handling needed here.

## Step 1 — Scope

Ask the user directly which this is. Never infer it:

- Total renew: the idea itself is wrong. Nothing carries forward but the original objective.
- Pivot: direction changes. Some real, validated pieces are worth carrying forward as raw material, not settled decisions.

Gate: the user picked one of the two, by name.

## Step 2 — Archive

Tag the current commit: `git tag archived-<date>`.

Move the whole project directory to a sibling path, `<project>-archived-<date>`, at the same parent level. Never a subfolder inside the live project.

Create a fresh, empty directory at the original path. Run `git init` there — new history, nothing carried over.

`CLAUDE.md`, `prd.md`, every `spec/<phase>/`, `backlog.md`, `changelog.md`, and `state.json` all move with the archive.

None of it exists at the fresh path. Old architecture, old decisions, and accumulated context can't poison a direction that isn't there to read.

Gate: the fresh path is empty except `.git`. The archived path has everything the live project had, tagged and dated.

## Step 3 — The slate

Total renew: call `autobuild:explore` (global), fresh. Carry forward only the original idea, as a note — not a settled decision to build from.

Pivot: call `autobuild:explore` (global), fresh. Carry forward whichever pieces the user marks as validated, as raw material for a new interview — reopened, not reused as-is.

Gate: the fresh path still has no `prd.md`. Nothing pre-loaded the interview.

## Step 4 — Log it

The fresh `changelog.md` opens with one `Pivoted` entry, naming the archived path and the reason.

Record positive facts only. A negating word stating a capability — "never fails," "nothing to install" — is not an exclusion.

Gate: the entry names what changed and why, in `changelog.md`'s own format.

## Step 5 — Close

Run `${CLAUDE_PLUGIN_ROOT}/scripts/update-state.py`. Commit.

Gate: the state script ran clean. The commit succeeded.

## Gate

Build only from the steps above.

Gate on the outcome: the archived path has everything the live project had, tagged and dated. The fresh path is empty except `.git` and one `changelog.md` entry.

Pass moves to `autobuild:explore` — call the Skill tool with that id, global mode. Fail returns to Step 1 with the findings.

Fix what it finds, once, then move on — it never runs a second time to confirm. Ask the user only if a finding itself is unclear.
