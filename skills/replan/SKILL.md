---
name: replan
description: Archives a build and opens a clean path for a pivot. Trigger when users change direction, renew, pivot, or start over.
---

# Replan

Reads the live project's docs and history, archives them, and writes a fresh `changelog.md` entry.

Read `../../stack.md` first. Resolve `../../` paths against `${CLAUDE_PLUGIN_ROOT}`.

## Rules

A roadmap change alone is not a replan. That happens at Wrap's Finish, or at the next phase's Explore — no special handling needed here.

## Step 1 — Scope

Ask the user directly which this is. Never infer it:

- Total renew: the idea itself is wrong. Nothing carries forward but the original objective.
- Pivot: direction changes. Some real, validated pieces are worth carrying forward as raw material, not settled decisions.

Gate: the user picked one of the two, by name.

## Step 2 — Archive

Resolve the exact live and archive paths. Show both to the user. Require the user to type `archive` before changing either path.

Tag the current commit: `git tag archived-<date>`.

Move the whole project directory to a sibling path, `<project>-archived-<date>`, at the same parent level. Never a subfolder inside the live project.

Create a fresh, empty directory at the original path. Run `git init` there — new history, nothing carried over.

`AGENTS.md`, `CLAUDE.md`, `prd.md`, `product.md`, every `spec/<phase>/`, `backlog.md`, and `changelog.md` all move with the archive.

None of it exists at the fresh path. Old architecture, old decisions, and accumulated context can't poison a direction that isn't there to read.

Gate: the user typed `archive`. The resolved archive target did not already exist. The fresh path is empty except `.git`. The archived path has everything the live project had, tagged and dated.

## Step 3 — The slate

Total renew carries only the original idea as a note, not a settled decision.

Pivot carries only pieces the user marks as validated, as raw material for a new interview.

Gate: the fresh path still has no `prd.md`. Nothing pre-loaded the interview.

## Step 4 — Log it

The fresh `changelog.md` opens with one `Pivoted` entry, naming the archived path and the reason.

Gate: the entry names what changed and why, in `changelog.md`'s own format.

## Step 5 — Close

Commit the fresh changelog.

Gate: the commit succeeded.

## Hand-off

Gate on the outcome: the archived path has everything the live project had, tagged and dated. The fresh path is empty except `.git` and one `changelog.md` entry.

Pass moves to `autobuild:explore` in global mode — call the Skill tool with that id. Fail returns to Step 1 with the findings.
