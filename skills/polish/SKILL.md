---
name: polish
description: Drains the backlog — collects new tickets from any source, groups them into one small shippable batch, and ships it. Trigger on /autobuild:polish, or whenever the user hands over a batch of bugs or tickets, wants to clear the backlog, or asks to knock out some small fixes.
---

# Polish

- Step: one unit of work.
- Gate: the check at the end of a step.
- Pass a gate → move to the next step.
- Fail a gate → redo the step, using the gate's findings.
- Fail the same gate twice → stop, ask the user.

Read `${CLAUDE_PLUGIN_ROOT}/ladder.md` first — it shows where this skill sits in the whole stack.

Never auto-fired. The user invokes this directly, whenever they want the backlog drained — not part of the phase loop.

## Step 1 — Collect

The user hands over tickets in whatever form they have them — pasted, an exported file, a `.md`, a URL. Read whatever's given.

Log each item to `backlog.md`, under Bugs, Improvements, or Feature phases, following `schemas/backlog.md`.

Record positive facts only. Never write "never X" or "out of scope" into the doc.

Gate: every item handed over appears in `backlog.md`, once each, in the right category.

## Step 2 — Ground

For any item whose fix isn't obvious, do a light research pass. Look at 1 or 2 comparable cases, not a full teardown — the same discipline as Spec's Ground, scaled down.

Gate: every item chosen for this batch has a clear, checkable fix in mind.

## Step 3 — Batch

Pick a small group of open backlog items — same-shape, non-conflicting, each finishable and shippable together in one pass. Not a full phase.

Gate: every item in the batch touches different files, or the same file in a way that doesn't conflict.

## Step 4 — Drain

Work on a `polish-<date>` branch.

For each item, follow Implement's own TDD method. Name the break, write one failing test, then the smallest fix.

Run the mutation check before it counts as done.

Run the full test suite once, fresh, after the whole batch — not per item.

Commit. Close each drained item in `backlog.md` — rewritten to its closed form, not deleted. Append one changelog entry, following `schemas/changelog.md`.

Record positive facts only. Never write "never X" or "out of scope" into either doc.

Gate: zero tests fail. Every item in the batch is closed in `backlog.md`, and named in the changelog.

## Step 5 — Close

Run `${CLAUDE_PLUGIN_ROOT}/scripts/update-state.py`. Merge the `polish-<date>` branch. Commit.

Gate: the state script ran clean. The commit succeeded.

## Gate

Build only from the steps above.

Gate on the diff, `changelog.md`, and `backlog.md`. Spawn a blind agent — it sees only those, never the original tickets. It checks:

- Every item the changelog claims was drained has a real, matching change in the diff.
- Every closed backlog item is actually addressed by the diff.
- No negative or prohibition language appears in the changelog or backlog.

Pass ends this run — polish has no next skill to call. Fail returns to Step 4 with the findings.

Fail this gate twice → stop, ask the user.
