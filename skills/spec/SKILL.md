---
name: spec
description: Designs a phase and writes its contract. Trigger on phase stories, designs, design handoffs, data models, API contracts, or interface planning.
---

# Spec

Per phase only. Reads `user-stories.md`, `prd.md`, and `product.md`; writes `research.md`, `design.md`, and `contract.md` under `spec/<phase>/` — never another phase's `spec/`.

Read `../../stack.md` first. Resolve `../../` paths against `${CLAUDE_PLUGIN_ROOT}`.

## Resume

A draft, or an uncommitted approved `contract.md`, resumes at the first incomplete step.

## Step 1 — Ground

Skip this step, unless the track is deep, or `research.md` has no step count for any comparable product. Read the track in `user-stories.md`; explore already researched this phase.

Dispatch one `crawler` at the standard tier, with no conversation history. It finds real products that solve this feature.

Its prompt includes the phase scope, user stories, target users, known constraints, and exact research question.

It reads their app-store reviews and competitor help docs for each one.

Walk a free trial's own flow yourself with `/browse`, where one exists. A `crawler` reads about a product; `/browse` uses it.

For each comparable product, count the user's steps, and note every decision point and point of friction.

If subagents are unavailable, research in this thread. Wait for the findings before writing anything.

Ground the design and contract in those findings.

Write the findings to `spec/<phase>/research.md`, following `../../templates/research.md`. Append to what `explore` left there rather than writing over it.

Gate:
- Name every real comparable feature found, each with its step count and one friction point.
- `spec/<phase>/research.md` exists, and every finding in it carries a source.

## Step 2 — Design

Skip this step when the phase changes no screen.

Ask the user one question: where does the design happen?

- Here — in this session, with a design tool or design skill. Write no handoff. Design straight from the stories, `prd.md`'s principles, `product.md`'s Look, and `research.md`.
- Outside — a human designer or a fresh design agent. Write the Handoff section of `spec/<phase>/design.md`, following `../../templates/design.md`.

For an outside design, capture the current screens this phase touches with `/browse`. Save them to `spec/<phase>/design/current/`.

Wait for the design — nothing runs while you wait. Record where it lives in `design.md`'s Source section.

Walk the design against the stories, one item at a time: every screen, state, acceptance criterion, product principle, and expected file.

Sort each mismatch into one of two kinds:

- Gap — the design has no answer for the item, or works against a principle or criterion.
- Divergence — the design answers the item another way, or better than the stories asked.

Fix a gap in the design tool, for a design made here. Write it to `design.md`'s Review section, for an outside design.

Walk the new design again. Ask the user about each divergence on its own: does the design win here, or the stories?

Record every answer in `design.md`'s Decisions section, with its winner.

Gate:
- An outside Handoff copies every acceptance criterion under some screen, and lists every file it expects back.
- Every item was walked against the design, one by one. Zero gaps remain. Every divergence has a recorded winner.
- Show the design to the user. Get their approval.

## Step 3 — Contract

Write `spec/<phase>/contract.md`, following `../../templates/contract.md`, from the design, the winners in `design.md`'s Decisions section, the user stories, and `prd.md`.

This file, `design.md`, `prd.md`, and `product.md` are the whole context a fresh session gets to build this phase.

Model the data model as one fact, one place — a value that can change lives in exactly one field, referenced by key, never copied.

Give every rule that can fail an error shape: a code, a message, and the field it points to.

Write every edge case a real user or a real outage can cause, using the prompts in `../../templates/contract.md`.

A mechanism earns a sequence diagram when at least two hold:

- More than one actor takes part.
- The next action depends on state, not just data.
- A loop runs with more than one exit.
- Wrong order causes a real bug — a race, a double-write, a lost update.

Check every rule below before moving on:

- Every field lives in one place, not copied.
- Every interface states who can call it, what it takes, what it gives, and a code per outcome.
- Every rule states a condition, a result, and an error shape if it can fail.
- Every diagrammed mechanism earns it by the test above.
- Every edge case a real user or outage can cause has a line.

Gate: all five hold.

## Step 4 — Reconcile

Check the contract against the user stories and the design:

- Every user story maps to at least one part of the data model or an interface.
- Every interface names the screen or caller that uses it, or is marked internal.
- Every screen that needs data has an interface for it.
- Every screen is reachable from home, and can return.
- The data model matches what the interfaces actually take and give.
- The contract adds nothing beyond what the stories and design call for.

Set the contract's status to `draft`.

Gate: all six hold. Fix any that do not before moving on.

## Step 5 — Review and close

Check the contract against the user stories yourself.

A deep-track phase spawns a blind agent for this check instead, at the flagship tier. Show it only the contract and user stories.

The check covers:

- Every user story is covered by the contract.
- Every interface has a matching screen or caller, or is marked internal.
- Every business rule is checkable, not descriptive.
- Every edge case a real user or outage can cause has a line.
- Every limit in the doc was stated by the user or proven by research, and names its scope.

Fix each finding once. Fail returns to Step 3 when a finding remains.

On pass, tell the user, in plain words, what the product will do after this phase. One line per business rule the user would notice. Name no field, interface, or code.

Get their approval, then set the contract status to `approved`. Commit the phase documents.

Gate: zero review findings remain. The user approved the summary. The contract is `approved`. The working tree is clean.

## Hand-off

Pass moves straight to `autobuild:implement` — call the Skill tool with that id. Fail returns to Step 3 with the findings.
