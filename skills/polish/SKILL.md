---
name: polish
description: Drains backlog items in one shippable batch. Trigger when users provide bugs or small fixes, or ask to clear the backlog.
---

# Polish

- Step: one unit of work.
- Gate: the check at the end of a step.
- Pass a gate → move to the next step.
- Fail a gate → redo the step, using the gate's findings.
- Fail the same gate twice → stop, ask the user.

Resolve every `../../` path from this `SKILL.md`, against `${CLAUDE_PLUGIN_ROOT}`.

Read `../../ladder.md` first — it shows where this skill sits in the whole stack.

Read the project's `writing-rule.md` next — scaffold it from `../../writing-rule.md` if missing. It sets the prose style for every doc this skill writes.

Runs only when the user invokes it or Autobuild finds an interrupted polish run.

On direct invocation without recovery state, start Step 1.

On resume, check recovery state in this order:

- A local `autobuild.polish-action` Git config value resumes Step 6. Read its branch and base from `autobuild.polish-branch` and `autobuild.polish-base`.
- Otherwise, read the Active polish block before checking branch state. If it exists, create its recorded branch from its recorded base when the branch is missing, or switch to that branch when it exists.
- A committed matching changelog heading and clean tree resumes Step 6.
- A committed Active polish plan resumes Step 5.
- An Active polish block with a pending or uncommitted plan resumes Step 4.
- A Polish intake block resumes Step 1, which completes collection idempotently before continuing.
- A polish branch without recovery state is ambiguous. Stop and ask for its base and intended items; never create another branch.

No recovery state on a non-polish branch is a fresh run and starts Step 1.

## Step 1 — Collect

The user hands over items in whatever form they have them — pasted, an exported file, a `.md`, a URL. Read whatever's given.

`backlog.md` may not exist yet. Scaffold it from `../../skills/wrap/schemas/backlog.md` before recording the intake.

Before classifying an item, add a Polish intake block to `backlog.md`. Record the current base and every submitted item unchanged. On resume, use those recorded items.

Log each item to `backlog.md`, under Bugs, Improvements, or Feature phases, following `../../skills/wrap/schemas/backlog.md`.

Record positive facts only. A negating word stating a capability — "never fails," "nothing to install" — is not an exclusion.

Gate: the intake preserves every submitted item, and each appears in `backlog.md` once in the right category.

## Step 2 — Ground

For any item whose fix is unclear, dispatch `crawler` at the mechanical tier for a light pass. Give it no conversation history. If agents are unavailable, search in this thread. Look at 1 or 2 comparable cases, not a full teardown.

Gate: every item chosen for this batch has a clear, checkable fix in mind.

## Step 3 — Batch

Pick a group of open backlog items — same-shape, non-conflicting, each finishable and shippable together in one pass. Not a full phase.

Choose a free `polish-<YYYYMMDD-HHMMSS>` name. Use Vietnam time.

If that name exists, append `-2`, then increase the suffix until the name is free.

Replace the Polish intake with an Active polish block while still on its recorded base. Record the chosen branch, base, selected original items, and `Plan: pending`. Then create or switch to the recorded branch from the recorded base.

Gate: the branch and Active polish block exist. Every selected item can ship with the batch.

## Step 4 — Plan

For each item in the batch, name the exact file it touches and the exact fix — not "add error handling" or "similar to Item N."

Check for interaction: does one item's fix change behavior another item's fix depends on. Order the batch to avoid it.

Replace `Plan: pending` with the exact plan. Commit that block with an `Autobuild-Base` trailer.

Gate: every item names a real file and concrete fix. The plan commit exists.

## Step 5 — Drain

For each item, follow Implement's own test-first method. Name the break, and confirm it's a bug, not a design decision.

Grade a design decision by door and reach first, the same way. A reach decision stops here — ask the user, per Implement's own rule, before any fix.

No reach: write one failing test, and the smallest fix.

Run the mutation check before it counts as done.

Run the full test suite once, fresh, after the whole batch — not per item.

Close each drained item in `backlog.md`, rewritten to its closed form. Leave a not-done item open.

Prepend one changelog entry, following `../../skills/wrap/schemas/changelog.md`.

Use the exact branch name as its heading.

Record positive facts only. A negating word stating a capability — "never fails," "nothing to install" — is not an exclusion.

Report a table, one row per item in the batch: the original issue, what was done, and the outcome. Flag a not-done item clearly, in its own row, never folded into a done row.

Spawn a blind agent at the deliberate tier.

Use flagship for security, migration, concurrency, core data, public APIs, or three-system changes.

Show it the selected original items, diff, changelog, and backlog. It checks:

- Every claimed fix has a matching diff.
- Every closed item is addressed.
- Every not-done item stays open.

Fix each finding once. Commit all code and closure documents after the review passes.

Remove the Active polish block in the closure commit.

Add `Autobuild-Base: <base-branch>` as the closure commit trailer.

Gate: zero tests and review findings remain. Every item has the correct state. The working tree is clean.

## Step 6 — Branch fate

Ask the user to merge, keep, or discard the polish branch. Merge into the recorded base only after approval.

After the user chooses, record the branch, base, and action in local Git config as `autobuild.polish-branch`, `autobuild.polish-base`, and `autobuild.polish-action`. Write the action last.

Complete or verify the recorded action idempotently:

- Merge switches to the base and merges the branch. An already-merged branch passes.
- Keep switches to the base and leaves the branch intact.
- Discard requires the user to type `discard`, switches to the base, and deletes the branch. An absent branch passes.

After verification, unset all three local Git config values.

Gate: the requested branch action completed, the current branch is the recorded base, and no local polish config remains.

## Gate

Build only from the steps above.

Gate on the selected branch action. Pass ends this run. Fail returns to Step 5.
