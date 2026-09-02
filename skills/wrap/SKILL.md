---
name: wrap
description: Verifies, audits, checks, and finishes a phase. Trigger when users ask to review, test, merge, finish, or ship a phase.
---

# Wrap

Per phase, for verification, audit, runtime checks, and finish. Reads the phase diff, contract, stories, and `prd.md`.

Writes to `changelog.md` and `backlog.md` at the project root — shared across every phase.

- Step: one unit of work.
- Gate: the check at the end of a step.
- Pass a gate → move to the next step.
- Fail a gate → redo the step, using the gate's findings.
- Fail the same gate twice → stop, ask the user.

Resolve every `../../` path from this `SKILL.md`. In Claude Code, that root is `${CLAUDE_PLUGIN_ROOT}`.

Read `../../ladder.md` first — it shows where this skill sits in the whole stack.

Read the project's `writing-rule.md` next — scaffold it from `../../writing-rule.md` if missing. It sets the prose style for every doc this skill writes.

When a plan lacks its base, inspect committed `state.json` for a `legacy-snapshot` routing object.

Use its base only when its phase matches this phase, `present` lists `plan.md`, and the working plan exists.

Compare the exact phase heading in current `HEAD` and the resolved base branch.

If current `HEAD` has it and the base lacks it, resume at Step 7. Skip Steps 1 through 6.

If the working tree has an uncommitted heading, resume at the first incomplete step from Step 4.

## Step 1 — Verify

Run the full test suite now, fresh — not a memory of an earlier run.

Gate: zero tests fail.

## Step 2 — Audit

Spawn a fresh deliberate, read-only review subagent with no conversation history. Point it at the phase's full diff.

Use flagship for security, migration, concurrency, core data, public APIs, or three-system changes.

Fix every HIGH finding now. A MEDIUM or LOW finding, or one outside this phase's stories, needs the user's OK before it goes to `backlog.md`, instead of blocking here.

A felt MEDIUM or LOW finding is never auto-backlogged — one the user would notice, wait on, or feel boxed in by. Surface it; the user picks fix-now or backlog.

Gate: zero HIGH findings remain unresolved.

## Step 3 — Check the running surface

Skip this step if the phase shipped no running surface.

Derive deterministic checks from this phase's stories. Use one scripted hit per new endpoint or screen.

Use curl for endpoints. Use an existing project-native render or route check for screens.

Inspect an existing screenshot when the project already produces one. Add no browser dependency for this step.

If a screen has no existing check, mark its stories unverified. Add no test tool for this step.

Show every unverified story to the user. Continue only when the user accepts that coverage gap.

Read only running output: status codes, logs, rendered output, or existing screenshots.

A story that calls the product's agent needs one live call. Seed mock data for its other states.

Call the real agent once, to confirm the call itself works — not to confirm every state.

Fix every break on a user story's path now. Ask before logging an unrelated rough edge to `backlog.md`.

A felt rough edge is never silently backlogged. The user picks fix-now or backlog.

Gate: every checkable story passed. The user accepted each unverified story.

## Step 4 — Docs

Prepend one phase entry to `changelog.md`, following `../../skills/wrap/schemas/changelog.md`.

Use the exact phase ID as its heading: `## <phase-id>`.

Append approved Audit or runtime items to `backlog.md`, following `../../skills/wrap/schemas/backlog.md`.

`backlog.md` may not exist yet. Scaffold it from `../../skills/wrap/schemas/backlog.md` before the first item lands.

Record positive facts only. A negating word stating a capability — "never fails," "nothing to install" — is not an exclusion.

Gate: the exact phase heading exists. Every approved item appears once.

## Step 5 — Sweep

Read every doc this phase's diff could make stale: `README.md`, anything under `docs/`, and other shipped docs.

Fix what no longer matches what shipped. Do this directly, with no review loop.

Gate: every doc read matches what the diff shipped.

## Step 6 — Close

Commit the changelog, backlog, and documentation updates on the phase branch.

Gate: the closure commit exists. The working tree is clean.

## Step 7 — Finish

Present four options, and only these four:

- merge to the base branch
- push and open a pull request
- keep the branch as it is
- discard this work

Discard needs a typed "discard" back before it runs.

Follow `../../docs/git-workflow.md` for the branch's fate, matching the choice above.

Gate: the selected action completed. A pull-request choice returned its URL.

Gate: if merged, the base branch's tests pass — run fresh, not assumed.

## Gate

Every step above passed. Verify and runtime checks already caught what needed catching.

After a merge, check the Roadmap. Load and follow `autobuild:explore` for the next phase, or end it.

After a pull request, keep, or discard action, stop.
