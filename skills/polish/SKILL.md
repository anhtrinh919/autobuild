---
name: polish
description: Drains backlog items batch by batch, each on its own approved plan. Trigger when users provide bugs or small fixes, or ask to clear the backlog.
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

`polish-plan.md` holds this run's whole state, at the project root. One field per line. It records:

- `Status: intake`, `planning`, or `draining`
- `Branch: <exact polish branch>`
- `Base: <exact base branch>`
- `Submitted items: <every handed-over item, unchanged>`
- one block per batch: `Batch <N>`, `Status: pending`, `approved`, or `drained`, its selected items, and its approved plan

`backlog.md` keeps one sentence and one bullet an item. This run's detail lives in `polish-plan.md`.

On direct invocation without recovery state, start Step 1.

On resume, check recovery state in this order:

- A local `autobuild.polish-action` Git config value resumes Step 6. Read its branch and base from `autobuild.polish-branch` and `autobuild.polish-base`.
- An intake plan resumes Step 1 on its recorded base. It has no branch to restore.
- Otherwise, read the planning or draining plan before branch state. Create its recorded branch from its base, or switch when it exists.
- Every batch drained, with a committed changelog heading and a clean tree, resumes Step 6.
- The first batch with `Status: approved` resumes Step 5.
- The first batch with `Status: pending` resumes Step 4.
- A polish branch without `polish-plan.md` is ambiguous. Stop and ask for its base and intended items; never create another branch.

No recovery state on a non-polish branch is a fresh run and starts Step 1.

## Step 1 — Collect

The user hands over items in whatever form they have them — pasted, an exported file, a `.md`, a URL. Read whatever's given.

`backlog.md` may not exist yet. Scaffold it from `../../skills/wrap/schemas/backlog.md` before logging the intake.

Before classifying an item, create `polish-plan.md`. Record `Status: intake`, the current base, and every submitted item unchanged.

Log each item as one sentence and one bullet in `backlog.md`, following `../../skills/wrap/schemas/backlog.md`.

Record positive facts only. A negating word stating a capability — "never fails," "nothing to install" — is not an exclusion.

Gate: `polish-plan.md` preserves every submitted item. Each appears in `backlog.md` once, as one sentence in the right category.

## Step 2 — Ground

For any item whose fix is unclear, dispatch `crawler` at the mechanical tier for a light pass. Give it no conversation history. If agents are unavailable, search in this thread. Look at 1 or 2 comparable cases, not a full teardown.

Gate: every item chosen for this run has a clear, checkable fix in mind.

## Step 3 — Batch

Pick the open backlog items this run drains. Split them into batches — each batch same-shape, non-conflicting, and shippable in one pass. Not a full phase.

Show the user one table before any batch is planned, one row an item: the item in plain words, who it affects and what it costs them, and its batch number.

Say in one line why each batch groups the way it does, and which batch runs first.

Ask the user to confirm the items and the split. Change no branch, code, or document before that answer.

Gate: the user confirmed every item and its batch.

Choose a free `polish-<YYYYMMDD-HHMMSS>` name. Use Vietnam time.

If that name exists, append `-2`, then increase the suffix until the name is free.

Set `polish-plan.md` to `Status: planning` while still on its recorded base. Record the branch, base, and every batch with its items and `Status: pending`.

Create or switch to the recorded branch from the recorded base. One branch carries every batch in this run.

Gate: the branch and `polish-plan.md` exist. Every confirmed item sits in exactly one pending batch.

## Step 4 — Plan one batch

Take the first batch with `Status: pending`. Plan only that batch.

Enter plan mode.

For each item, name the break and the first layer where behavior becomes incorrect.

Classify the fix as root-cause, symptom-patch, or heuristic. Name the exact file, fix, and failing test.

Check for interaction: does one item's fix change behavior another item's fix depends on. Order the batch to avoid it.

Gate: every item has one checkable root cause, classification, file, fix, and test.

Exit plan mode. This is the batch's approval gate.

Gate: the user approved every root cause and proposed fix, before any file changed.

Set `polish-plan.md` to `Status: draining`. Set this batch to `Status: approved` and record its approved plan. Commit that change with an `Autobuild-Base` trailer.

Gate: the committed batch block matches the approved plan and records the base.

## Step 5 — Drain that batch

Drain only the batch approved in Step 4.

For each item, follow Implement's own test-first method using the approved diagnosis.

New evidence that changes the root cause or fix returns the item to Step 4 for approval.

Grade a design decision by door and reach first, the same way. A reach decision stops here — ask the user, per Implement's own rule, before any fix.

No reach: write one failing test, and the smallest fix.

Run the mutation check before it counts as done.

Run the full test suite once, fresh, after the whole batch — not per item.

Close each drained item in `backlog.md`, rewritten to its closed form. Leave a not-done item open.

The first drained batch prepends one changelog entry, following `../../skills/wrap/schemas/changelog.md`. Use the exact branch name as its heading. Each later batch adds its lines to that same entry.

Record positive facts only. A negating word stating a capability — "never fails," "nothing to install" — is not an exclusion.

Report a table, one row per item in the batch: the original issue, what was done, and the outcome. Flag a not-done item clearly, in its own row, never folded into a done row.

Spawn a blind agent at the deliberate tier.

Use flagship for security, migration, concurrency, core data, public APIs, or three-system changes.

Show it this batch's block in `polish-plan.md`, the batch diff, changelog, and backlog. It checks:

- Every claimed fix has a matching diff.
- Every closed item is addressed.
- Every not-done item stays open.

Fix each finding once. Set this batch to `Status: drained` and commit all code and closure documents after the review passes.

Add `Autobuild-Base: <base-branch>` as the closure commit trailer.

Gate: zero tests and review findings remain. Every item has the correct state. The working tree is clean.

Return to Step 4 while a pending batch remains. Go to Step 6 once every batch is drained.

## Step 6 — Branch fate

Ask the user to merge, keep, or discard the polish branch. Merge into the recorded base only after approval.

After the user chooses, record the branch, base, and action in local Git config as `autobuild.polish-branch`, `autobuild.polish-base`, and `autobuild.polish-action`. Write the action last.

Before leaving the polish branch, remove `polish-plan.md` and commit that change. An absent file passes on resume.

Complete or verify the recorded action idempotently:

- Merge switches to the base and merges the branch. An already-merged branch passes.
- Keep switches to the base and leaves the branch intact.
- Discard requires the user to type `discard`, switches to the base, and deletes the branch. An absent branch passes.

After verification, unset all three local Git config values.

Gate: the requested branch action completed, the current branch is the recorded base, and no local polish config remains.

## Gate

Build only from the steps above.

Gate on the selected branch action. Pass ends this run. Fail returns to Step 5.
