---
name: replan
description: Archives a build and opens a clean path for a pivot. Trigger when users change direction, renew, pivot, or start over.
---

# Replan

- Step: one unit of work.
- Gate: the check at the end of a step.
- Pass a gate → move to the next step.
- Fail a gate → redo the step, using the gate's findings.
- Fail the same gate twice → stop, ask the user.

Resolve every `../../` path from this `SKILL.md`. In Claude Code, that root is `${CLAUDE_PLUGIN_ROOT}`.

Read `../../ladder.md` first — it shows where this skill sits in the whole stack.

Read the project's `writing-rule.md` next — scaffold it from `../../writing-rule.md` if missing. It sets the prose style for every doc this skill writes.

A roadmap change alone is not a replan. That happens at Wrap's Finish, or at the next phase's Explore — no special handling needed here.

## Step 1 — Scope

Ask the user directly which this is. Never infer it:

- Total renew: the idea itself is wrong. Nothing carries forward but the original objective.
- Pivot: direction changes. Some real, validated pieces are worth carrying forward as raw material, not settled decisions.

Gate: the user picked one of the two, by name.

## Step 2 — Archive

Resolve the exact live and archive paths. Show both to the user. Require the user to type `archive` before changing either path.

Gate: the user typed `archive`. The resolved archive target does not exist.

Tag the current commit: `git tag archived-<date>`.

Move the whole project directory to a sibling path, `<project>-archived-<date>`, at the same parent level. Never a subfolder inside the live project.

Create a fresh, empty directory at the original path. Run `git init` there — new history, nothing carried over.

`AGENTS.md`, `CLAUDE.md`, `prd.md`, every `spec/<phase>/`, `backlog.md`, and `changelog.md` all move with the archive.

None of it exists at the fresh path. Old architecture, old decisions, and accumulated context can't poison a direction that isn't there to read.

Gate: the fresh path is empty except `.git`. The archived path has everything the live project had, tagged and dated.

## Step 3 — The slate

Total renew carries only the original idea as a note, not a settled decision.

Pivot carries only pieces the user marks as validated, as raw material for a new interview.

Gate: the fresh path still has no `prd.md`. Nothing pre-loaded the interview.

## Step 4 — Log it

The fresh `changelog.md` opens with one `Pivoted` entry, naming the archived path and the reason.

Record positive facts only. A negating word stating a capability — "never fails," "nothing to install" — is not an exclusion.

Gate: the entry names what changed and why, in `changelog.md`'s own format.

## Step 5 — Close

Commit the fresh changelog.

Gate: the commit succeeded.

## Gate

Build only from the steps above.

Gate on the outcome: the archived path has everything the live project had, tagged and dated. The fresh path is empty except `.git` and one `changelog.md` entry.

Pass loads and follows `autobuild:explore` in global mode. Fail returns to Step 1 with the findings.

Fix what it finds, once, then move on — it never runs a second time to confirm. Ask the user only if a finding itself is unclear.
