---
name: implement
description: Turns a phase contract into tested code through an approved plan. Trigger when users ask to build, code, implement, or ship a phase.
---

# Implement

Per phase only. Reads `spec/<phase>/contract.md`, `spec/<phase>/design.md`, `spec/<phase>/design/`, `spec/<phase>/user-stories.md`, `spec/<phase>/research.md`, `prd.md`, and `product.md` — never another phase's `spec/`. Writes `spec/<phase>/plan.md`, the acceptance tests, and the phase's code, on the phase branch.

Read `../../stack.md` first. Resolve `../../` paths against `${CLAUDE_PLUGIN_ROOT}`.

## Rules

`design.md`'s Source names what each screen has to look like. Its Decisions name each screen that differs from the design on purpose.

Grade a design decision behind a task's test first — door and reach, see Step 2.

Fail the same gate twice with no decision ever graded → grade it now, the same way, as a backstop. Act on the grade.

Stop and ask the user only for:

- an irreversible or destructive action
- a security-sensitive action
- an action outside this workspace — merge, push, publish
- a plan too broken to guess a path through
- any decision Step 2's grading marks as reach
- the direction check after the first batch, in Step 2

## Resume

If committed `plan.md` has no status, set it to `building`.

An uncommitted `verified` status resumes Step 5 and finishes its commit.

A building plan resumes at Step 2 only when it names the base branch and the phase branch is active.

If either branch fact is missing, return to Step 1 and ask the user to confirm the base.

## Step 1 — Plan

Enter plan mode.

Map the files first: which files get created, which get modified, and the one job each file does.

Name the end-to-end test tool and the acceptance test path. Reuse the project's own tool when one exists.

Break the work into tasks. Each task is one small file group, and can be finished and committed on its own.

Order the tasks so the first batch builds the thinnest end-to-end path through the phase's main story. Later tasks fill it in.

Write every task in full — the exact paths, the behaviour its test proves, the exact command, and its expected result. The writer writes the code. Never write "add error handling," "similar to Task N," or "TBD."

Check the plan against the contract, line by line: does every interface, rule, and field map to a task? A quick-track phase has no contract — check each acceptance criterion in `user-stories.md` instead. Check every task's names and types against every other task: the same field or function must read the same everywhere.

Assign each task a tier. Use standard unless its scope meets a higher tier's rule in `../../stack.md`.

Check the first two gate items below before you exit.

Exit plan mode. This is the plan's approval gate.

Record the current branch as the plan's base branch.

Follow `../../stack.md`'s Git section to create this phase's branch before Step 2.

Once approved, write `spec/<phase>/plan.md`, following `../../templates/plan.md`. Set its status to `building`.

Gate:
- the plan has zero hits for "TBD", "TODO", "similar to", or "add appropriate"
- every contract line maps to a task, checked one by one
- the user approved the complete plan, before any file was written or a branch created
- `spec/<phase>/plan.md` exists, and matches the approved plan

## Step 2 — Build

Resuming after a break? Check `plan.md`'s tasks against the branch's git log — a task whose commit message is already there is done.

Before the first task, write the acceptance tests. Skip this when the branch log already has the `acceptance tests` commit.

Spawn a fresh writer subagent at the standard tier, with no conversation history. Give it only `user-stories.md`, the plan's test tool and path, and — when they exist — `design.md`'s Decisions and the contract's interfaces.

It writes one end-to-end test per acceptance criterion, driven the way a user drives the product — a browser for screens, a real call for interfaces. It never reads the plan's tasks.

Run them. Every test fails for the missing behaviour, not for a broken setup. Commit them as `acceptance tests`.

These files are read-only for every code writer. A code writer never edits one to make it pass.

A broken acceptance test is plumbing when its fix keeps the story's promise — a wrong selector, setup, wait, or path. Fix it without asking: send a fresh acceptance-test writer the story and the failing output. Record the fix in `plan.md`.

Ask the user only when the fix would change what a story promises. Name the story and the choice in plain words, with your recommendation.

Start from the first task that is not done. A plan without Tier uses standard.

Use the task's recorded tier before dispatching. Update it before dispatch when new facts require escalation.

Use deliberate for unclear prior art or a first failed repair.

Use flagship for security, migration, concurrency, core data, public APIs, or three-system changes.

Use exceptional only after a direct flagship pass leaves a stated risk open. Record that escalation in the task block.

Before dispatching, grade every design decision by door and reach. A two-way door is cheap to undo.

A one-way door has dependent work. Reach changes what users see, do, pay for, or are permitted to do.

A reach decision stops and asks the user. Name no-reach choices and explain one-way choices in this turn.

For each uncommitted task, spawn a fresh writer subagent with no conversation history. Give it the task block, applicable contract facts, exact allowed paths, and every decision already settled for this task.

Tell it to change only its task's Files. It must not commit, switch branches, or change any other path.

Tell it to stop before editing when it finds an ungraded decision. The parent grades it and asks for reach.

Record each answer in the task's block, then respawn the writer with it. A settled decision reaches every later writer this way.

Tell it to search prior art for general parts. It reports what it used or why nothing fit.

Tell it to name the break, write one failing test, run its exact Run command, and make the smallest passing change.

Tell it to refactor only while green. Keep the behavior identical.

Tell it to poll real async conditions, compute expected values independently, and test its own boundary.

Tell it to mutate the code once. It tries a wrong constant, branch, return, or skipped edge case.

The writer reports changed paths, mutation result, focused test output, exit codes, and new dependencies.

Reject work outside the task's Files, and any change to an acceptance test. Check every reported result before accepting the task.

Run writers in parallel only when their Files do not overlap.

If writer subagents are unavailable, perform the same bounded task in this session. The parent session keeps every branch and commit action.

Step 2 never reruns the full suite. That cost belongs to Step 3, once, at the end.

A task's test is hollow when expected values come from the code under test. Compute them independently.

A test that only detects an intentional constant change is hollow. Test the behavior that constant drives. An uncaught mutation leaves the behavior unprotected or the test hollow.

No blind review runs per task. Step 3 reviews the whole phase once.

A load-bearing task is the exception — one at the flagship or exceptional tier. It gets its own blind review before any later task builds on it.

Use flagship for a flagship task. Use exceptional for an exceptional task.

Point that reviewer at the task block and the uncommitted diff by file path. It trusts nothing you report, and reads the diff against the task's own text. It flags anything missing or extra, and runs one focused test at most.

The parent session directs repairs, reruns focused tests, and commits accepted tasks in batches. Only that commit marks its tasks done.

After the first batch commits, show the user that path running — screenshots of each screen, or the command and its output. Ask one question: is this the right direction?

A redirect returns to Step 1 for every task it touches. Record the answer in `plan.md`.

Gate:
- every acceptance criterion has one failing acceptance test, committed
- every mutation made at least one test fail
- any new dependency is a real, maintained package
- no open review findings remain on any load-bearing task, and every diff matches only the task it belongs to
- the user confirmed the direction, or the plan was revised to match their redirect

## Step 3 — Verify

Run the full test suite now, fresh — not a memory of an earlier run. Read the exit code.

A test failing here is a regression, not a RED step — trace it to its root cause. Check every layer the bad value passes through, not just where it surfaced.

Check the contract line by line against the code. A quick-track phase checks each acceptance criterion instead:

- every interface is reachable
- every business rule has a passing test
- every edge case from the contract is covered

Spawn one blind agent to review the whole phase diff against its base branch. Use the plan's highest task tier, at deliberate or above.

Give it the plan, and the contract when one exists. It trusts nothing you report. It checks:

- every task's diff matches its own text
- nothing in the diff was never asked for by the plan
- no test takes its expected values from the code under test
- no risk the task's tier names is left open — security, data loss, a race

It runs one focused test at most, never the whole suite.

Fix each finding. Rerun the focused tests each fix touches, then the full suite once more.

Gate: zero tests fail, acceptance tests included. Every contract line is accounted for in the code. Zero review findings remain open.

## Step 4 — Product judge

Tests prove the code matches the plan. This step checks the product matches what the user wanted.

Skip this step when the phase shipped nothing a user runs.

Start the product. Seed data shaped like real use: empty, typical, and heavy — long text, many rows.

A story that calls the product's own agent gets one live call. Seed mock data for its other states.

Spawn a `dogfood` agent at the deliberate tier, with no conversation history. Give it only:

- `prd.md`'s Concept, North star, Target users, and Product principles
- this phase's stories and its `Not in this phase` list, in the user's words
- how to open the product, and which seeded data exists
- the phase's design files and recorded design decisions, when a design exists

Never give it the contract, the plan, the diff, or any test result. It judges the product, not the paperwork.

It plays each story's actor. It starts from the product's first screen, with no hints, and tries to finish the story.

It walks every screen it reaches at phone width (390px) and desktop width (1440px), with each seeded data set.

It judges each screen on three levels, in this order:

- Intent — in five seconds, can the actor tell what this screen is and what to do next? Does the walk deliver the story's outcome? Does it honour every product principle?
- Fidelity — do the hierarchy, primary action, copy, and states match the design? A recorded design decision that differs from the design is correct as built.
- Polish — spacing, alignment, colour, and type.

It reports each finding with its level, screen, state, width, screenshot path, and what a real user would say. It also lists every story it could not reach.

Grade each finding:

- Blocker — the actor cannot finish a story, or an intent check fails.
- Felt — the actor finishes, but a user would notice, wait, or feel lost.
- Polish — only a trained eye notices.

Fix every blocker and felt finding now. A fix that changes what users see, do, or pay is a reach decision — ask the user first.

Fix polish findings in one batch. Ask the user before logging one to `backlog.md` instead.

Rerun the focused tests each fix touches. Respawn the judge on the screens the fixes touched.

Gate: every story was walked or its gap was shown to the user. Zero blocker or felt findings remain open.

## Step 5 — Close

Set the plan status to `verified`. Commit that status change.

Step 3's review covers the whole diff. Wrap adds no second code review.

Gate: the plan status is `verified`. The working tree is clean.

## Hand-off

Pass moves straight to `autobuild:wrap` — call the Skill tool with that id.
