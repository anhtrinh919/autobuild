---
name: migrate
description: Bridges an old claude-build project onto autobuild's schemas, once — every doc rewritten to autobuild's own style, never copied verbatim. Trigger on /autobuild:migrate, or whenever the user wants to bring an old build-stack project onto this stack.
---

# Migrate

- Step: one unit of work.
- Gate: the check at the end of a step.
- Pass a gate → move to the next step.
- Fail a gate → redo the step, using the gate's findings.
- Fail the same gate twice → stop, ask the user.

Read `${CLAUDE_PLUGIN_ROOT}/ladder.md` first — it shows where this skill sits in the whole stack.

## Step 1 — Locate

Find the old project's root — it has a `.build-state.json` or a `specs/` directory.

Read `.build-state.json`'s `phase` and `step` fields, to know how far the old build got.

Gate: the old project's root is found. Its `phase` and `step` are read.

## Step 2 — Map the constitution

Map:

- `mission.md` + `product.md` + `roadmap.md` → `prd.md`'s Concept, North star, Target users, and Roadmap
- `tech-stack.md`'s decisions → `prd.md`'s Assumptions and constraints, as `Constraint` entries

Rewrite every line to autobuild's own word and sentence caps, and its positive-facts-only rule. A structural copy is not a migration — old-stack prose was written under different rules.

Gate: `prd.md` exists, matches `schemas/prd.md`'s 9 sections, and every line meets its cap.

## Step 3 — Map the current phase

Map only the phase Step 1 read from `.build-state.json` — the old project's most recent one, done or in-flight.

Leave every other phase under `specs/` where it sits. A finished phase is already summed up in `prd.md`'s Roadmap and `changelog.md`. No later skill opens an old phase's own folder again (`RULE.md`), so migrating it a second time spends real cost for zero future reads.

For the current phase, map:

- `requirements.md`'s User Stories → `user-stories.md`'s Stories
- `outcome-card.md`'s frozen contract → `user-stories.md`'s Scope and `prd.md`'s When-is-done
- `requirements.md`'s API Contracts and Data Model → `contract.md`
- `design-brief.md` (external track) → `design-brief.md`
- `plan.md` → `plan.md`

Same rewrite discipline as Step 2. Every migrated line meets autobuild's own caps, not the old stack's.

Gate: the current phase has its matching `spec/<phase>/` directory. Each schema's sections are present, each line under its own cap.

## Step 4 — Carry over the trail

`backlog.md`'s items keep their `DF-N`/`T-N` ids, rewritten to `backlog.md`'s own word caps.

`CHANGELOG.md`'s entries move to `changelog.md`, one line each, sorted into its own categories.

Gate: every open backlog item and changelog entry survived the move, rewritten to spec.

## Step 5 — Reconstruct state

Build `state.json` from `.build-state.json`'s `phase` and `step` fields, matching whichever autobuild doc actually exists on disk.

Gate: `state.json` matches what's actually on disk, not what `.build-state.json` claimed.

## Step 6 — Close

Run `${CLAUDE_PLUGIN_ROOT}/scripts/update-state.py`. Commit.

Gate: the state script ran clean. The commit succeeded.

## Gate

Build only from the steps above.

Gate on `prd.md` and the current phase's migrated `spec/<phase>/`. Spawn a blind agent — it sees only the migrated docs, never the old-stack originals. It checks:

- Every section of every migrated doc meets its own word and sentence cap.
- No negative or prohibition language survived the migration.
- The current phase has a matching `spec/<phase>/` on this side. No older phase was migrated.