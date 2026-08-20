---
name: wrap
description: Verifies, audits, dogfoods, and finishes a phase's code, then logs what shipped and what didn't. Trigger on /autobuild:wrap, right after implement's gate passes, or whenever the user asks to review, test, merge, or ship a phase.
---

# Wrap

Per phase, for verify, audit, dogfood, and finish. Reads the phase's diff, `spec/<phase>/contract.md`, `spec/<phase>/user-stories.md`, and `prd.md` — never another phase's `spec/`.

Writes to `changelog.md` and `backlog.md` at the project root — shared across every phase.

- Step: one unit of work.
- Gate: the check at the end of a step.
- Pass a gate → move to the next step.
- Fail a gate → redo the step, using the gate's findings.
- Fail the same gate twice → stop, ask the user.

Read `${CLAUDE_PLUGIN_ROOT}/ladder.md` first — it shows where this skill sits in the whole stack.

## Step 1 — Verify

Run the full test suite now, fresh — not a memory of an earlier run.

Gate: zero tests fail.

## Step 2 — Audit

Spawn a code-review subagent over the phase's full diff. Never review your own code.

Fix every HIGH finding now. A MEDIUM or LOW finding, or one outside this phase's stories, needs the user's OK before it goes to `backlog.md`, instead of blocking here.

A felt MEDIUM or LOW finding is never auto-backlogged — one the user would notice, wait on, or feel boxed in by. Surface it; the user picks fix-now or backlog.

Gate: zero HIGH findings remain unresolved.

## Step 3 — Dogfood

Skip this step if the phase shipped no running surface to click through.

Default tier: mechanical. One scripted hit per new endpoint or screen, deterministic and automated.

A curl per endpoint. A headless render, checked for console errors, per screen. Pass or fail, no agent judgment.

Gate: every new endpoint and screen was hit. Every hit passed.

Full tier — agentic, driven live through `/browse` — applies only when:

- a flow spans multiple steps an outside check can't observe
- correctness is genuinely visual or interaction-only: drag-and-drop, layout, animation
- `prd.md`'s Roadmap shows this is the final phase
- the user asks for it directly

Spawn a dogfood subagent for the full tier. It drives the running app through `/browse`, blind to the repo, and reports what it walked, what broke, and what it never reached.

Derive either tier's checks from this phase's own stories, not from the shipped code.

Fix every break on a user story's path now. A rough edge outside this phase's stories needs the user's OK before it goes to `backlog.md`, instead.

Same felt-impact fork as Audit — a felt rough edge is never silently backlogged. Surface it; the user picks fix-now or backlog.

Gate: every user story for this phase was walked or hit. Nothing on its path is broken.

## Step 4 — Finish

Present four options, and only these four:

- merge to the base branch
- push and open a pull request
- keep the branch as it is
- discard this work

Discard needs a typed "discard" back before it runs.

Follow `docs/git-workflow.md` for the worktree's fate, matching the choice above.

Gate: show the four options. Get the user's choice.

Gate: if merged, the base branch's tests pass — run fresh, not assumed.

## Step 5 — Docs

Skip this step if the work was discarded.

Append one changelog entry for this phase to `changelog.md`, following `schemas/changelog.md`. Append any backlog item logged during Audit or Dogfood to `backlog.md`, following `schemas/backlog.md`.

Record positive facts only. A negating word stating a capability — "never fails," "nothing to install" — is not an exclusion.

Gate: the changelog entry names what changed, in the categories the schema gives. Every item logged during this run appears in the backlog, once each.

## Step 6 — Close

Run `${CLAUDE_PLUGIN_ROOT}/scripts/update-state.py`. Commit.

Gate: the state script ran clean. The commit succeeded.

## Gate

Build only from the steps above.

Gate on the phase's final diff, `changelog.md`, and `backlog.md`.

Spawn a blind agent — it sees only those, never the audit or the dogfood report. It checks:

- The changelog entry matches what the diff actually did.
- Every backlog entry names a real, specific gap, not a vague worry.
- A fresh read of the diff turns up no HIGH finding.
- No sentence in the changelog or backlog excludes or forbids something. "Never fails" and "nothing to install" state a fact, not an exclusion.

Check `prd.md`'s Roadmap for what comes next. Pass moves to `autobuild:explore` for the next phase — call the Skill tool with that id — or ends the roadmap if this was the last one. Fail returns to Step 2 with the findings.

Fail this gate twice → stop, ask the user.
