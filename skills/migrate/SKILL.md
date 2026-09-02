---
name: migrate
description: Migrates an old build-stack or earlier Autobuild project onto current schemas. Trigger when users bring an older project onto this stack.
---

# Migrate

- Step: one unit of work.
- Gate: the check at the end of a step.
- Pass a gate → move to the next step.
- Fail a gate → redo the step, using the gate's findings.
- Fail the same gate twice → stop, ask the user.

Resolve every `../../` path from this `SKILL.md`. In Claude Code, that root is `${CLAUDE_PLUGIN_ROOT}`.

Read `../../ladder.md` first — it shows where this skill sits in the whole stack.

Read the project's `writing-rule.md` next — scaffold it from `../../writing-rule.md` if missing. It sets the prose style for every doc this skill writes.

Two modes:

- Legacy mode maps `.build-state.json` or `specs/` into Autobuild.
- Upgrade mode updates an earlier Autobuild project in place.

Choose one mode in Step 1. Keep that mode through the final gate.

## Step 1 — Locate

In legacy mode, find a root with `.build-state.json` or `specs/` and no PRD.

If `.build-state.json` exists, read its `phase` and `step` fields.

If it is absent, list the directories under `specs/`. Ask the user which phase is current.

In upgrade mode, find a committed `state.json`, committed PRD, and `spec/` directory.

Validate that state has `prd`, `changelog`, `backlog`, and `phases` keys. Its PRD status is missing or `migrating`.

Recompute its phase booleans from files on disk. The earlier router refreshed those values before routing.

A working `migrating` PRD or routing mode `legacy-snapshot` marks an interrupted upgrade. Resume its first incomplete step.

Before the first edit, record `git status --short`, `git diff`, and `git diff --cached`.

List untracked files with `git ls-files --others --exclude-standard -z`. Hash each file without displaying it.

Store paths and hashes at the path from `git rev-parse --git-path autobuild-migrate-untracked`.

Reuse that record when resuming.

Before the first edit, stop when any change is staged or an existing edit overlaps routing metadata.

On resume, accept only staged routing-metadata hunks created by this upgrade. Stop when another staged hunk exists.

Use the earlier router's roadmap and changelog rules. The first phase without its changelog entry is current.

Every phase closed means the current phase is none.

When the current phase has a plan, record the current branch as base if it is `main` or `master`.

If that branch is neither, ask the user for the plan's base branch.

Gate: the mode and root are known. Upgrade mode names its current phase or confirms every phase closed.

Gate: upgrade mode knows the base when its current phase already has a plan.

Gate: legacy mode knows its current phase. It knows step state when `.build-state.json` exists.

## Step 2 — Map the constitution

In legacy mode, map:

- `mission.md` + `product.md` + `roadmap.md` → `prd.md`'s Concept, North star, Target users, and Roadmap
- `tech-stack.md`'s decisions → `prd.md`'s Assumptions and constraints, as `Constraint` entries

In legacy mode, give every roadmap phase an approved `phase-<N>-<slug>` ID and matching `spec/<phase-id>` path.

Rewrite each legacy line to Autobuild's word, sentence, and positive-fact rules. A structural copy is not a migration.

In upgrade mode, keep every PRD sentence except its routing metadata.

In upgrade mode, reuse an existing `spec/<name>` basename as that phase's exact ID. Give every other phase a kebab-case ID.

In upgrade mode, write each exact ID into its roadmap line. Keep every existing phase directory in place.

Set the migrated PRD status to `migrating` until the final review passes.

Gate: the PRD has nine sections, status `migrating`, and one exact ID per roadmap phase.

## Step 3 — Map the current phase

In legacy mode, map only the current phase named in Step 1.

Leave every other phase under `specs/` where it sits. A finished phase is already summed up in `prd.md`'s Roadmap and `changelog.md`. No later skill opens an old phase's own folder again (`RULE.md`), so migrating it a second time spends real cost for zero future reads.

In legacy mode, map:

- `requirements.md`'s User Stories → `user-stories.md`'s Stories
- `outcome-card.md`'s frozen contract → `user-stories.md`'s Scope and `prd.md`'s When-is-done
- `requirements.md`'s API Contracts and Data Model → `contract.md`
- `design-brief.md` (external track) → `design-brief.md`
- `plan.md` → `plan.md`

In legacy mode, derive `features.md` from the migrated contract, following `../../skills/spec/schemas/features.md`.

In legacy mode, set migrated user stories and features to `draft`.

In legacy mode, rewrite an existing `plan.md` to the current schema. Set its status to `building`.

In legacy mode, rewrite each line to Autobuild's word, sentence, and positive-fact rules.

In upgrade mode, keep every phase document's content, path, and status unchanged.

Add a `routing` object to `state.json` with mode `legacy-snapshot`.

Record `phase`, `through`, `present`, and `base`. Use exact phase IDs and document basenames.

`present` lists only current-phase documents found during recomputation. `base` is null when no current plan exists.

Set `through` to the current phase, or the last closed phase when none is current.

Use a null phase, empty document list, and null base when every phase is closed.

Gate: legacy mode maps each contract rule and endpoint to one current-phase feature.

Gate: upgrade mode preserves the earlier router's completion result for every existing phase document.

## Step 4 — Carry over the trail

In legacy mode, keep `backlog.md` item IDs and rewrite each item to its current cap.

In legacy mode, move `CHANGELOG.md` entries to `changelog.md`, one line each, sorted into their categories.

In upgrade mode, keep the backlog and each changelog entry's content.

In upgrade mode, rewrite only each phase heading to its exact `## <phase-id>` form.

Use the exact `## <phase-id>` heading for every migrated phase entry.

Gate: every backlog item and changelog entry survives. The same phases remain closed.

## Step 5 — Review and close

Spawn a fresh flagship, read-only review subagent with no conversation history.

In legacy mode, show it the PRD and current phase documents. It checks:

- Every section of every migrated doc meets its own word and sentence cap.
- No sentence that excludes or forbids something survived the migration. "Never fails" and "nothing to install" state a fact, not an exclusion.
- The current phase has a matching `spec/<phase>/` on this side. No older phase was migrated.

In upgrade mode, show it the original state, migration diff, and resulting route. It checks:

- Phase-document content, paths, and statuses remain unchanged.
- Snapshot completion produces the same next skill as the earlier router.
- The first open phase matches the earlier router, or both report the roadmap done.
- Every pre-existing dirty edit remains after the metadata commit.
- Every recorded untracked-file hash still matches.

Fix each finding once. Fail returns to Step 2 when a finding remains.

In legacy mode, set the PRD, user stories, and features to `approved`. Keep any plan `building`.

In upgrade mode, set the PRD to `approved`. Keep the compatibility snapshot in `state.json`.

In upgrade mode, stage only generated routing-metadata hunks. Never stage a pre-existing diff.

In upgrade mode, compare the untracked hashes. Keep their Git-local record until the migration commit succeeds.

In legacy mode, commit the migrated documents.

In upgrade mode, commit only the migration. Leave every pre-existing edit in the working tree.

After a successful upgrade commit, remove the Git-local hash record.

Gate: zero findings remain. Legacy mode ends clean. Upgrade mode preserves every prior edit.

## Gate

Build only from the steps above.

Pass loads and follows `autobuild:autobuild`. Fail returns to Step 2 with the findings.
