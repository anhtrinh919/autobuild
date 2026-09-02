---
name: implement
description: Turns a phase contract into tested code through an approved plan. Trigger when users ask to build, code, implement, or ship a phase.
---

# Implement

Per phase only. Reads `spec/<phase>/contract.md`, `spec/<phase>/features.md`, `spec/<phase>/design-brief.md`, `spec/<phase>/user-stories.md`, `spec/<phase>/research.md`, and `prd.md` — never another phase's `spec/`.

`design-brief.md` is a snapshot of the day it was written. The contract carries the phase forward, and the contract wins wherever the two disagree.

- Step: one unit of work.
- Gate: the check at the end of a step.
- Pass a gate → move to the next step.
- Fail a gate → redo the step, using the gate's findings.
- Grade a design decision behind a task's test first — door and reach, see Step 2.
- Fail the same gate twice with no decision ever graded → grade it now, the same way, as a backstop. Act on the grade.
- Stop and ask the user only for:
  - an irreversible or destructive action
  - a security-sensitive action
  - an action outside this workspace — merge, push, publish
  - a plan too broken to guess a path through
  - any decision Step 2's grading marks as reach

Resolve every `../../` path from this `SKILL.md`. In Claude Code, that root is `${CLAUDE_PLUGIN_ROOT}`.

Read `../../ladder.md` first — it shows where this skill sits in the whole stack.

Read the project's `writing-rule.md` next — scaffold it from `../../writing-rule.md` if missing. It sets the prose style for every doc this skill writes.

If committed `plan.md` has no status, set it to `building`.

An uncommitted `verified` status resumes Step 4 and finishes its commit.

A building plan resumes at Step 2 only when it names the base branch and the phase branch is active.

If either branch fact is missing, return to Step 1 and ask the user to confirm the base.

## Step 1 — Plan

Map the files first: which files get created, which get modified, and the one job each file does.

Break the work into tasks. Each task is one small file group, and can be finished and committed on its own.

Write every task in full — the exact paths, the real test code, the exact command, and its expected result. Never write "add error handling," "similar to Task N," or "TBD."

Check the plan against the contract, line by line: does every endpoint, rule, and field map to a task? Check every task's names and types against every other task: the same field or function must read the same everywhere.

Gate: grep the plan for "TBD", "TODO", "similar to", or "add appropriate" — zero hits.

Gate: every contract line maps to a task, checked one by one.

Assign each task a tier. Use standard unless its scope meets a higher tier's rule in `../../ladder.md`.

Show the complete plan to the user. Get approval before writing it or creating the branch.

Gate: the user approved the complete plan.

Record the current branch as the plan's base branch.

Follow `../../docs/git-workflow.md` to create this phase's branch before Step 2.

Once approved, write `spec/<phase>/plan.md`, following `../../skills/implement/schemas/plan.md`.

Set its status to `building`.

Record positive facts only. A negating word stating a capability — "never fails," "nothing to install" — is not an exclusion.

Gate: `spec/<phase>/plan.md` exists, and matches the approved plan.

## Step 2 — Build

Resuming after a break? Check `plan.md`'s tasks against the branch's git log — a task whose commit message is already there is done.

Start from the first task that is not done. A plan without Tier uses standard.

Use the task's recorded tier before dispatching. Update it before dispatch when new facts require escalation.

Use deliberate for unclear prior art or a first failed repair.

Use flagship for security, migration, concurrency, core data, public APIs, or three-system changes.

Use exceptional only after a direct flagship pass leaves a stated risk open. Record that escalation in the task block.

Before dispatching, grade every design decision by door and reach. A two-way door is cheap to undo.

A one-way door has dependent work. Reach changes what users see, do, pay for, or are permitted to do.

A reach decision stops and asks the user. Name no-reach choices and explain one-way choices in this turn.

For each uncommitted task, spawn a fresh writer subagent with no conversation history. Give it the task block, applicable contract facts, and exact allowed paths.

Tell it to change only its task's Files. It must not commit, switch branches, or change any other path.

Tell it to stop before editing when it finds an ungraded decision. The parent grades it and asks for reach.

Tell it to search prior art for general parts. It reports what it used or why nothing fit.

Tell it to name the break, write one failing test, run its exact Run command, and make the smallest passing change.

Tell it to refactor only while green. Add no new behavior.

Tell it to poll real async conditions, compute expected values independently, and test its own boundary.

Tell it to mutate the code once. It tries a wrong constant, branch, return, or skipped edge case.

The writer reports changed paths, mutation result, focused test output, exit codes, and new dependencies.

Reject work outside the task's Files. Check every reported result before accepting the task.

Run writers in parallel only when their Files do not overlap. Keep risky tasks in separate review cycles.

If writer subagents are unavailable, perform the same bounded task in this session. The parent session keeps every branch and commit action.

Batch two or more small, same-shape accepted tasks into one review cycle. Keep risky tasks in separate cycles.

Step 2 never reruns the full suite. That cost belongs to Step 3, once, at the end.

A task's test is hollow when expected values come from the code under test. Compute them independently.

A test that only detects an intentional constant change is hollow. Test the behavior that constant drives.

Gate: every mutation made at least one test fail. An uncaught mutation leaves the behavior unprotected or the test hollow.

Gate: any new dependency is a real, maintained package.

Spawn a fresh, read-only review subagent before committing each batch. Use deliberate for standard or deliberate batches.

Use flagship for a flagship batch. Use exceptional for an exceptional batch.

Point it at every batch task block and the uncommitted diff by file path.

The reviewer never re-runs the suite themselves. If something looks wrong, it runs one focused test — never the whole suite.

The reviewer trusts nothing you report. It reads the diff against the task's own text, and flags anything missing or extra.

Gate: no open review findings remain, on any task. Every diff matches only the task it belongs to.

The parent session directs repairs, reruns focused tests, and commits the reviewed batch. Only that commit marks its tasks done.

## Step 3 — Verify

Run the full test suite now, fresh — not a memory of an earlier run. Read the exit code.

A test failing here is a regression, not a RED step — trace it to its root cause. Check every layer the bad value passes through, not just where it surfaced.

Check the contract line by line against the code:

- every endpoint is reachable
- every business rule has a passing test
- every edge case from the contract is covered

Gate: zero tests fail. Every contract line is accounted for in the code.

## Step 4 — Review and close

Review the phase's full diff against `spec/<phase>/contract.md`.

Spawn a fresh, read-only subagent with no conversation history. Show it the contract, plan, and phase diff.

Use exceptional when any task uses exceptional. Otherwise use flagship when any task uses flagship.

Otherwise, use deliberate.

It checks:

- Every business rule in the contract has a test that passes.
- Every endpoint in the contract works end to end.
- Nothing in the diff is missing from the plan, or added beyond it.

Fix each finding once. Fail returns to Step 2 when a finding remains.

On pass, set the plan status to `verified`. Commit that status change.

Gate: zero review findings remain. The plan status is `verified`. The working tree is clean.

## Gate

Build only from the steps above.

Pass loads and follows `autobuild:wrap` now.

Fail Step 4 twice with no graded decision. Grade it under Step 2 before moving on.
