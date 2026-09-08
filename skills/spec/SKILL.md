---
name: spec
description: Writes a phase's design brief and contract. Trigger on phase stories, design briefs, data models, API contracts, or endpoint planning.
---

# Spec

Per phase only. Reads `spec/<phase>/user-stories.md` and `prd.md` — never another phase's `spec/`.

- Step: one unit of work.
- Gate: the check at the end of a step.
- Pass a gate → move to the next step.
- Fail a gate → redo the step, using the gate's findings.
- Fail the same gate twice → stop, ask the user.

Resolve every `../../` path from this `SKILL.md`, against `${CLAUDE_PLUGIN_ROOT}`.

Read `../../ladder.md` first — it shows where this skill sits in the whole stack.

Read the project's `writing-rule.md` next — scaffold it from `../../writing-rule.md` if missing. It sets the prose style for every doc this skill writes.

A draft, statusless, or uncommitted approved `features.md` resumes at the first incomplete step.

## Step 1 — Ground

Dispatch one `crawler` at the standard tier, with no conversation history. It finds real products that solve this feature.

Its prompt includes the phase scope, user stories, target users, known constraints, and exact research question.

It reads their app-store reviews and competitor help docs for each one.

Walk a free trial's own flow yourself with `/browse`, where one exists. A `crawler` reads about a product; `/browse` uses it.

For each app, count the user's steps, and note every decision point and point of friction.

If subagents are unavailable, research in this thread. Wait for the findings before writing anything.

Ground the brief in those findings. Never reconcile the brief against research after writing it.

Write the findings to `spec/<phase>/research.md`, following `../../skills/spec/schemas/research.md`. Append to what `explore` left there rather than writing over it. A finding that stays in this session cannot be checked by the brief, by the contract, or by anyone reading either one later.

Gate: name every real comparable feature found, each with its step count and one friction point.

Gate: `spec/<phase>/research.md` exists, and every finding in it carries a source.

## Step 2 — Brief

Write `spec/<phase>/design-brief.md`, following `../../skills/spec/schemas/design-brief.md`.

Record positive facts only. A negating word stating a capability — "never fails," "nothing to install" — is not an exclusion.

Give the designer real context: the feature, why it matters to the user, the user stories it serves, and every screen this phase touches — its states, its primary action, and why it exists.

Include the real on-screen copy, not a placeholder.

Exclude palette, typography, mood, component choice, layout, and motion. Those are the designer's own call, not this brief's.

Every sentence about what already runs is checked against the running application before it is written. An earlier document describes what was true when it was written, and a phase since then may have moved it.

Gate: every acceptance criterion in `user-stories.md` appears under some screen in the brief. A story maps by its criteria, one by one, never by its title alone.

Gate: every screen block is a real surface. Two blocks naming one screen are one screen, and its states belong inside it.

Gate: nothing visual appears in the brief.

Gate: every string under `Copy` names the thing that shows it and the state it shows in.

Gate: every sentence the brief states about what already runs was checked against the running application.

Gate: show the brief to the user. Get their approval.

## Step 3 — Design gate

Hand the brief to the user. Wait — nothing runs while you wait.

The user designs it: in this session with a design skill, or outside it with another tool. The user puts the mockups or images in `spec/<phase>/design/`.

Walk the brief against the design, one item at a time: every screen, every state, every criterion, and every rule under `What has to hold`.

Sort each mismatch into one of two kinds:

- Gap — the design has no answer for the item, or contradicts a rule the brief states.
- Divergence — the design answers the item another way, or better than the brief asked.

Write every gap to `spec/<phase>/design-review.md`, following `../../skills/spec/schemas/design-review.md`. The user sends it to the designer.

Record positive facts only. A negating word stating a capability — "never fails," "nothing to install" — is not an exclusion.

Wait for the new design — nothing runs while you wait. Walk the brief against it again.

Ask the user about each divergence on its own: does the design win here, or the brief? Never ask about several at once.

Record every answer in `design-review.md`, one line per item, with its winner.

`design-brief.md` is frozen from here. Step 4 writes the contract from the design and these recorded winners.

Gate: the design exists in `spec/<phase>/design/`. Every brief item was walked against it, one by one.

Gate: `design-review.md` holds every divergence with its winner, and zero open gaps.

## Step 4 — Contract

Write `spec/<phase>/contract.md`, following `../../skills/spec/schemas/contract.md`, from the design, the winners recorded in `design-review.md`, the user stories, and `prd.md`.

Record positive facts only. A negating word stating a capability — "never fails," "nothing to install" — is not an exclusion.

This file, the design brief, and `prd.md` are the whole context a fresh session gets to build this phase.

Model the data model as one fact, one place — a value that can change lives in exactly one field, referenced by key, never copied.

Name endpoints as nouns, plural for a collection, hierarchical for a child. The HTTP method is the verb — never repeat it in the path.

Give every rule that can fail an error shape: a code, a message, and the field it points to.

Sweep every field, action, and external dependency through its Edge cases categories, per `../../skills/spec/schemas/contract.md`. Write one line per category that applies.

A mechanism earns a sequence diagram when at least two hold:

- More than one actor takes part.
- The next action depends on state, not just data.
- A loop runs with more than one exit.
- Wrong order causes a real bug — a race, a double-write, a lost update.

Check every rule below before moving on:

- Every field lives in one place, not copied.
- Every endpoint states who can call it, what it sends, what it returns, and a status code per outcome.
- Every rule states a condition, a result, and an error shape if it can fail.
- Every diagrammed mechanism earns it by the test above.
- Every field, action, and dependency has an Edge cases line for each category that applies to it.

Gate: all five hold.

## Step 5 — Reconcile

Check the contract against the user stories and the design:

- Every user story maps to at least one part of the data model or an endpoint.
- Every endpoint names the screen that calls it, or is marked internal.
- Every screen that needs data has an endpoint for it.
- Every screen is reachable from home, and can return.
- The data model matches what the endpoints actually send and receive.
- The contract adds nothing beyond what the stories and design call for.

Gate: all six hold. Fix any that do not before moving on.

Write `spec/<phase>/features.md`, following `../../skills/spec/schemas/features.md` — every business rule and endpoint in `contract.md`, translated to plain language. No API, no data model, no code.

Set its status to `draft`.

Record positive facts only. A negating word stating a capability — "never fails," "nothing to install" — is not an exclusion.

Gate: every business rule and endpoint in `contract.md` traces to exactly one function in `features.md`.

Gate: show `features.md` to the user. Get their approval.

## Step 6 — Review and close

Spawn a blind agent at the deliberate tier.

Use flagship when the contract includes security, migration, concurrency, core data, public APIs, or three-system work.

Show it only the contract, features, and user stories. It checks:

- Every user story is covered by the contract.
- Every endpoint has a matching screen, or is marked internal.
- Every business rule is checkable, not descriptive.
- Every business rule and endpoint has a matching, plain-language function in `features.md`.
- Every field, action, and dependency has an Edge cases line for each category that applies to it.
- No sentence in the contract or `features.md` excludes or forbids something. "Never fails" and "nothing to install" state a fact, not an exclusion.

Fix each finding once. Fail returns to Step 4 when a finding remains.

On pass, set the features status to `approved`. Commit the phase documents.

Gate: zero review findings remain. Features are `approved`. The working tree is clean.

## Gate

Build only from the steps above.

Pass moves straight to `autobuild:implement` — call the Skill tool with that id. Fail returns to Step 4 with the findings.
