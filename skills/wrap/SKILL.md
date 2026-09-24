---
name: wrap
description: Audits a built phase, shows it to the user, refreshes the living docs, and finishes the branch. Trigger when users ask to review, demo, merge, finish, or ship a phase.
---

# Wrap

Per phase only. Reads the phase diff, contract, and plan. Writes `changelog.md`, `backlog.md`, `prd.md`, `product.md`, and this phase's demo screenshots.

Read `../../stack.md` first. Resolve `../../` paths against `${CLAUDE_PLUGIN_ROOT}`.

## Rules

Keeps every living doc in `../../stack.md`'s Docs section current. It never edits a snapshot.

Implement already ran the full suite and the product judge. Wrap reruns neither.

## Resume

Compare the exact phase heading in current `HEAD` and the resolved base branch.

If current `HEAD` has it and the base lacks it, resume at Step 5. Skip Steps 1 through 4.

If the working tree has an uncommitted heading, resume at Step 3.

## Step 1 — Audit

This audit grades the whole phase diff: code quality, risk, and scope.

Spawn a blind agent at the deliberate tier. Point it at the phase's full diff, the plan, and the contract when one exists.

It also flags anything in the diff that the plan never asked for, and any contract line with no code.

Use flagship for security, migration, concurrency, core data, public APIs, or three-system changes.

Fix every HIGH finding now. A MEDIUM or LOW finding, or one outside this phase's stories, needs the user's OK before it goes to `backlog.md`, instead of blocking here.

A felt MEDIUM or LOW finding is never auto-backlogged — one the user would notice, wait on, or feel boxed in by. Surface it; the user picks fix-now or backlog.

Gate: zero HIGH findings remain unresolved.

## Step 2 — Show the user

Skip this step if the phase shipped nothing a user runs.

Walk every story through the phase branch's running product with `/browse`. Screenshot each step the actor takes.

Save the screenshots to `spec/<phase>/demo/`, named `<story>-<step>.png`.

Show them to the user in story order, one line per step. Ask one question: is this what you wanted?

Each change the user asks for is a felt finding. Fix it now with Implement's test-first method, then show that story again.

A change too big for this phase goes to `backlog.md` as a feature-phase item, with the user's OK.

Gate: the user confirmed every story, or moved its change to `backlog.md`.

## Step 3 — Refresh the living docs

Rewrite each living doc to match what shipped. Do this directly, with no review loop.

Prepend one phase entry to `changelog.md`, following `../../templates/changelog.md`.

Use the exact phase ID as its heading: `## <phase-id>`.

Append approved Audit or runtime items to `backlog.md`, following `../../templates/backlog.md`.

`backlog.md` may not exist yet. Scaffold it from `../../templates/backlog.md` before the first item lands.

- `prd.md` — set this phase's roadmap status to `shipped`. Correct any settled fact the phase proved wrong. A change to the Concept, North star, or Product principles needs the user's approval.
- `product.md` — rewrite each section this phase changed, following `../../templates/product.md`. Scaffold it when missing.
- `README.md`, anything under `docs/`, and other shipped docs — fix what no longer matches.

Gate: the exact phase heading exists. Every approved item appears once. Every living doc matches what the diff shipped. This phase's roadmap status is `shipped`.

## Step 4 — Close

Commit the living-doc updates on the phase branch.

Gate: the closure commit exists. The working tree is clean.

## Step 5 — Finish

Present four options, and only these four:

- merge to the base branch
- push and open a pull request
- keep the branch as it is
- discard this work

Discard needs a typed "discard" back before it runs.

Follow `../../stack.md`'s Git section for the branch's fate, matching the choice above.

Gate:
- the selected action completed
- a pull-request choice returned its URL
- if merged, the base branch's tests pass — run fresh, not assumed

## Hand-off

Every step above passed.

After a merge, check the Roadmap. Move to `autobuild:explore` for the next phase — call the Skill tool with that id — or end the roadmap.

After a pull request, keep, or discard action, stop.
