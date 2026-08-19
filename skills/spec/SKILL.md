---
name: spec
description: Writes a phase's design brief and contract from its user stories and the product PRD. Waits for real design before writing the contract. Trigger on /autobuild:spec, right after explore's per-phase gate passes, or whenever the user asks for a design brief, a data model, an API contract, or endpoints for the next phase.
---

# Spec

Per phase only. Reads `spec/<phase>/user-stories.md` and `prd.md` — never another phase's `spec/`.

- Step: one unit of work.
- Gate: the check at the end of a step.
- Pass a gate → move to the next step.
- Fail a gate → redo the step, using the gate's findings.
- Fail the same gate twice → stop, ask the user.

Read `${CLAUDE_PLUGIN_ROOT}/ladder.md` first — it shows where this skill sits in the whole stack.

## Step 1 — Ground

Dispatch a sub-agent. It looks at 2 to 3 real apps that solve this specific feature, not the whole product.

It reads app-store reviews, competitor help docs, and a demo walkthrough for each app. When a free trial exists, it walks the flow itself with `/browse`.

For each app, it counts the user's steps, and notes every decision point and point of friction.

Wait for it before writing anything. Ground the brief in what it found — never reconcile the brief against it after.

Gate: name 2 to 3 real comparable features, each with its step count and one friction point.

## Step 2 — Brief

Write `spec/<phase>/design-brief.md`, following `schemas/design-brief.md`.

Record positive facts only. Never write "never X" or "out of scope" into the doc.

Give the designer real context: the feature, why it matters to the user, the user stories it serves, and every screen this phase touches — its states, its primary action, and why it exists.

Include the real on-screen copy, not a placeholder.

Exclude palette, typography, mood, component choice, layout, and motion. Those are the designer's own call, not this brief's.

Gate: every user story maps to at least one screen in the brief. Nothing visual appears in the brief.

Gate: show the brief to the user. Get their approval.

## Step 3 — Design gate

Hand the brief to the user. Wait — nothing runs while you wait.

The user designs it: in this session with a design skill, or outside it with another tool. Either way, they hand back the result.

Gate: the design exists — mockups or images, handed back by the user.

## Step 4 — Contract

Write `spec/<phase>/contract.md`, following `schemas/contract.md`, from the design, the user stories, and `prd.md`.

Record positive facts only. Never write "never X" or "out of scope" into the doc.

This file, the design brief, and `prd.md` are the whole context a fresh session gets to build this phase.

Model the data model as one fact, one place — a value that can change lives in exactly one field, referenced by key, never copied.

Name endpoints as nouns, plural for a collection, hierarchical for a child. The HTTP method is the verb — never repeat it in the path.

Give every rule that can fail an error shape: a code, a message, and the field it points to.

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

Gate: all four hold.

## Step 5 — Reconcile

Check the contract against the user stories and the design:

- Every user story maps to at least one part of the data model or an endpoint.
- Every endpoint names the screen that calls it, or is marked internal.
- Every screen that needs data has an endpoint for it.
- Every screen is reachable from home, and can return.
- The data model matches what the endpoints actually send and receive.
- The contract adds nothing beyond what the stories and design call for.

Gate: all six hold. Fix any that do not before moving on.

Write `spec/<phase>/features.md`, following `schemas/features.md` — every business rule and endpoint in `contract.md`, translated to plain language. No API, no data model, no code.

Record positive facts only. Never write "never X" or "out of scope" into the doc.

Gate: every business rule and endpoint in `contract.md` traces to exactly one function in `features.md`.

Gate: show `features.md` to the user. Get their approval.

## Step 6 — Close

Run `${CLAUDE_PLUGIN_ROOT}/scripts/update-state.py`. Commit.

Gate: the state script ran clean. The commit succeeded.

## Gate

Build only from the steps above.

Gate on `spec/<phase>/contract.md` and `spec/<phase>/features.md`. Spawn a blind agent — it sees only the contract, `features.md`, and the user stories, never the interview or the design. It checks:

- Every user story is covered by the contract.
- Every endpoint has a matching screen, or is marked internal.
- Every business rule is checkable, not descriptive.
- Every business rule and endpoint has a matching, plain-language function in `features.md`.
- No negative or prohibition language appears anywhere in the contract or `features.md`.

Pass moves straight to `autobuild:implement` — call the Skill tool with that id. Fail returns to Step 4 with the findings.

Fail this gate twice → stop, ask the user.
