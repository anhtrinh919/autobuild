---
name: explore
description: Researches and interviews users to create a PRD or phase stories. Trigger on product ideas, roadmaps, PRDs, stories, or new phases.
---

# Explore

Two modes.

Global runs once, for the whole product, and writes `prd.md`. Per-phase runs again, before each phase's spec work, and writes `spec/<phase>/user-stories.md`.

- Step: one unit of work.
- Gate: the check at the end of a step.
- Pass a gate → move to the next step.
- Fail a gate → redo the step, using the gate's findings.
- Fail the same gate twice → stop, ask the user.

Resolve every `../../` path from this `SKILL.md`, against `${CLAUDE_PLUGIN_ROOT}`.

Read `../../ladder.md` first — it shows where this skill sits in the whole stack.

Read the project's `writing-rule.md` next — scaffold it from `../../writing-rule.md` if missing. It sets the prose style for every doc this skill writes.

A draft or uncommitted approved PRD resumes global mode at its first incomplete step.

Draft or uncommitted approved phase stories resume per-phase mode at their first incomplete step.

## Step 1 — Ground

Dispatch two `crawler` agents at the standard tier, with no conversation history. Give each agent one search.

Each prompt names the product or phase, target users, known constraints, and exact research question.

The first search finds 3 to 5 real comparable products that people use today.

For each product, record strengths, weaknesses, and the gap it leaves.

The second search finds prior art: packages, services, platform features, or protocols that solve the same problem.

Global mode searches the product's core problem. Per-phase mode searches this phase's problem.

For each candidate, record weekly downloads, last release, size, licence, and remaining work.

If subagents are unavailable, run both searches separately in this thread. Wait for both results before Step 2.

Name the gap this idea could fill, from what it found. That gap grounds the interview, not a general impression of the market.

Per-phase mode also reads `prd.md` — the concept, north star, roadmap, and assumptions ground this phase's interview.

If a settled fact in `prd.md` no longer holds — the last phase shipped different from its roadmap line, an assumption proved false — correct it in place, now. This is a routine correction, not a pivot; a real change of direction belongs in `replan`, not here.

Per-phase mode also reads `backlog.md` at the project root, if one exists. It carries items a previous phase's wrap logged.

The two searches answer different questions. The first asks what people use. The second asks what this product or phase can integrate.

Gate: name at least 3 real comparable products, each with its gap.

Global mode carries the findings into the interview. Settled findings become PRD decisions.

Per-phase mode writes both searches to `spec/<phase>/research.md`.

Follow `../../skills/spec/schemas/research.md`. `spec` appends its findings to the per-phase file.

Gate: name what already solves the searched problem, or say nothing fits.

Gate: per-phase mode only — the answer is in `spec/<phase>/research.md`.

Gate: per-phase mode only — `prd.md` matches current reality, or was corrected.

## Step 2 — Grill the shape

Map the interview tree for the shape only:

- Global mode: concept, north star, target users.
- Per-phase mode: this phase's goal, and the actors it serves.

Ask the frontier in one round. The frontier is every decision whose prerequisites are already settled.

Split the frontier before you ask it. Ask only felt decisions — ones the user would notice, wait on, or feel boxed in by.

Decide plumbing decisions yourself — ones the user would never notice either way. Record each as a settled fact, not a question.

An item raised but not settled this round may still have real value. Ask about it in this round; log it to `backlog.md` only if the user says yes.

`backlog.md` may not exist yet. Scaffold it from `../../skills/wrap/schemas/backlog.md` before the first item lands.

Nothing with no future value gets written down at all.

Number each question. Give your recommended answer. Use this format:

> ❓ **Q1** - **<question title>**: <question body, may run multiple paragraphs, may include multiple choices>
>
> ➡️ <your recommended answer>

```mermaid
flowchart LR
    compute[Compute the frontier] --> fact{Needs a fact\nfrom outside?}
    fact -->|yes| dispatch[Search the web\nnon-blocking]
    fact -->|no| ask[Ask the frontier]
    dispatch -->|rest of frontier| ask
    ask --> wait[Wait for the user's answers]
    wait --> reshape[Answers reshape the tree]
    reshape --> empty{Frontier\nempty?}
    empty -->|no| compute
    empty -->|yes| confirm[Confirm shared understanding]
    confirm --> next([Step 3])
```

Search for any fact you would otherwise ask the user. Never ask for a fact you can verify.

Keep searching as new branches appear.

Gate: recompute the frontier — it returns zero items. Every shape item above is settled.

Name 2 to 6 decisions the interview never reached, that the draft still assumes. Route each as felt (ask now) or plumbing (record it).

The user says yes to the shared understanding.

## Step 3 — Shape

Write the settled shape, using only what it settled.

Record positive facts only. A negating word stating a capability — "never fails," "nothing to install" — is not an exclusion.

Global mode writes two things.

First, an announcement: what it does, who it is for, why it matters, in one paragraph — as if it already shipped.

Second, one sentence: for <user>, who <need>, this is a <kind of thing> that <key benefit>. Unlike <the closest alternative>, it <what's different>.

Per-phase mode writes one paragraph: what this phase delivers, and for whom.

If a sentence will not fill in cleanly, the tree is not actually settled yet. Go back to Step 2.

Gate: every claim traces to a settled decision, and nothing else does.

Gate: show it to the user. Get their approval.

Write it to disk now, before Step 4.

Global mode writes concept, north star, and target users into `prd.md`. Set its status to `draft`.

Per-phase mode writes Scope to `spec/<phase>/user-stories.md`. Set its status to `draft`.

A crash after this point does not lose the shape.

Gate: the shape's section exists on disk, and matches what was approved.

## Step 4 — Grill the features

Map the interview tree for everything the shape left open:

- Global mode: user stories, functional requirements, non-functional requirements, assumptions and constraints, roadmap, when it is done.
- Per-phase mode: this phase's user stories, in full.

Ask this frontier the same way — one round, split felt versus plumbing, looped until it's empty.

Per-phase mode folds in one question per backlog item:

- bring it into this phase
- propose it as a new roadmap phase
- leave it for later

Search for any fact you would otherwise ask the user. Never ask for a fact you can verify.

Keep searching as new branches appear.

Gate: recompute the frontier — it returns zero items. Every section above has one settled decision behind it.

Name 2 to 6 decisions the interview never reached, that the draft still assumes. Route each as felt (ask now) or plumbing (record it).

The user says yes to the shared understanding.

## Step 5 — Write

Write the rest of `prd.md` from the settled tree, following `../../skills/explore/schemas/prd.md`. Concept, north star, and target users are already there from Step 3.

Record positive facts only. A negating word stating a capability — "never fails," "nothing to install" — is not an exclusion.

Per-phase mode appends the stories to `spec/<phase>/user-stories.md`, following `../../skills/explore/schemas/user-stories.md`. The Scope section is already there from Step 3.

A feature-phase item approved in Step 4 gets appended to `prd.md`'s Roadmap section, as a new phase.

Every roadmap line names its exact `spec/<phase-id>` path. Phase IDs use lowercase kebab-case.

Gate: global mode only — all nine PRD sections exist. Each phase has one exact ID and directory.

Gate: per-phase mode only — Scope and Stories are present. Every settled story appears once.

Gate: show the doc to the user. Get their approval.

## Step 6 — Review and close

Create a review-only checklist from the approved decisions. Spawn a blind agent at the deliberate tier.

Use flagship when the document changes security, migration, concurrency, core data, public APIs, or three-system work.

Show it the approved decision checklist and the finished document. It checks:

- Every branch of the design tree appears in the doc.
- Every user story names an actor and an outcome, not a general capability.
- Global mode only: every section is present, grounded in a settled decision.
- Global mode only: every "When is done" criterion is checkable, and names a real motivation.
- Per-phase mode only: an approved feature-phase item appears once in `prd.md`'s Roadmap.
- No sentence in the doc excludes or forbids something. "Never fails" and "nothing to install" state a fact, not an exclusion.

Fix each finding once. Fail returns to Step 3 when a finding remains.

On pass, set the document status to `approved`.

Per-phase mode closes every folded-in backlog item. Rewrite each item instead of deleting it.

Commit the approved documents. Configure a remote only after the user approves its exact URL.

Gate: the status is `approved`. The working tree is clean. The remote matches the user's choice.

## Gate

Build only from the steps above.

Global pass moves to `autobuild:autobuild` — call the Skill tool with that id.

Per-phase pass moves to `autobuild:spec` — call the Skill tool with that id. Fail returns to Step 3 with the findings.
