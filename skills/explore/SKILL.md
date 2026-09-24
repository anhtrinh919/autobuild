---
name: explore
description: Researches and interviews users to create a PRD or phase stories. Trigger on product ideas, roadmaps, PRDs, stories, or new phases.
---

# Explore

Reads `prd.md`, `product.md`, and `backlog.md`; writes `prd.md`, or `spec/<phase>/user-stories.md` and `spec/<phase>/research.md`.

Read `../../stack.md` first. Resolve `../../` paths against `${CLAUDE_PLUGIN_ROOT}`.

## Rules

Global mode runs once, for the whole product, and writes `prd.md`. Per-phase mode runs again, before each phase's spec work, and writes `spec/<phase>/user-stories.md`.

Every round follows these rules:

- Ask only felt decisions. Decide plumbing yourself, and mark its node `settled` in the tree file.
- A question that needs an outside fact goes to a `crawler`. Ask the rest of the round while it runs.
- Number each question, and give your recommended answer, in this format:

> ❓ **Q1** - **<question title>**: <question body, may run multiple paragraphs, may include multiple choices>
>
> ➡️ <your recommended answer>

- End the round with one line: reply `ok` to accept every recommendation, or answer by number.
- An idea raised but not settled may still have value. Log it to `backlog.md` only if the user says yes. Scaffold that file from `../../templates/backlog.md` when missing.

## Resume

A draft or uncommitted approved PRD resumes global mode at its first incomplete step.

Draft or uncommitted approved phase stories resume per-phase mode at their first incomplete step.

An interview tree file resumes the interview at its first `open` node.

## Step 1 — Ground

Per-phase mode first proposes the phase's track, from its roadmap line and `product.md`. A quick proposal skips both searches, but still reads `prd.md`, `product.md`, and `backlog.md` below. When the interview changes the track to standard or deep, run the searches then.

Per-phase mode skips the prior-art search when `product.md`'s Settled choices already answer this phase's problem.

Per-phase mode records each comparable product's steps and friction too. Spec reuses them instead of searching again.

Dispatch two `crawler` agents at the standard tier, with no conversation history. Give each agent one search.

Each prompt names the product or phase, target users, known constraints, and exact research question.

The first search finds 3 to 5 real comparable products that people use today.

For each product, record strengths, weaknesses, and the gap it leaves.

The second search finds prior art: packages, services, platform features, or protocols that solve the same problem.

Global mode searches the product's core problem. Per-phase mode searches this phase's problem.

For each candidate, record its adoption signal, last release, size, licence, and remaining work.

If subagents are unavailable, run both searches separately in this thread. Wait for both results before the first question.

Name the gap this idea could fill, from what it found. That gap grounds the interview, not a general impression of the market.

Per-phase mode also reads `prd.md` and `product.md` — intent, principles, roadmap, and what runs today ground this phase's interview.

If a settled fact in `prd.md` no longer holds — the last phase shipped different from its roadmap line, an assumption proved false — correct it in place, now. This is a routine correction, not a pivot; a real change of direction belongs in `replan`, not here.

Per-phase mode also reads `backlog.md` at the project root, if one exists. It carries items a previous phase's wrap logged.

The two searches answer different questions. The first asks what people use. The second asks what this product or phase can integrate.

Global mode carries the findings into the interview. Settled findings become PRD decisions.

Per-phase mode writes both searches to `spec/<phase>/research.md`, following `../../templates/research.md`. `spec` appends its findings to the per-phase file.

Gate:

- name at least 3 real comparable products, each with its gap
- name what already solves the searched problem, or say nothing fits
- per-phase mode only: the answer is in `spec/<phase>/research.md`
- per-phase mode only: `prd.md` matches current reality, or was corrected

## Step 2 — Map the tree

Write the interview tree to the path from `git rev-parse --git-path autobuild-interview.md`. It stays out of commits, and survives a crash.

Global mode maps three levels:

- Trunk — the core: concept, north star, target users, and product principles.
- Branches — the shape: each major area of the product, the actor it serves, what it holds, its non-goals, its constraints, and where it sits in the roadmap.
- Leaves — the detail under each branch: its stories and criteria, rules, edge cases, targets, and when it is done.

Per-phase mode maps one level: this phase's goal, actors, track, stories, criteria, `Not in this phase` list, and one question per backlog item.

One line per node, indented under its parent: `open`, or `settled — <the answer>`.

Reread the file before every round, and update it after every answer. It is the only record of where the interview stands.

Gate: every node the known facts imply is in the file, under its parent.

## Step 3 — Trunk

Per-phase mode skips this step.

Ask the trunk questions in one round. Keep it to the few decisions every branch depends on.

Loop until every trunk node is settled.

Write the settled trunk:

- An announcement: what it does, who it is for, why it matters, in one paragraph — as if it already shipped.
- One sentence: for <user>, who <need>, this is a <kind of thing> that <key benefit>. Unlike <the closest alternative>, it <what's different>.

If a sentence will not fill in cleanly, the trunk is not settled yet. Ask again.

Write concept, north star, product principles, and target users into `prd.md`, following `../../templates/prd.md`. Set its status to `draft`.

Gate: every trunk node is settled, the user approved the announcement, and `prd.md` holds it.

## Step 4 — Branches

Per-phase mode skips this step.

Ask every branch question in one round. A long round is fine — the shape needs all of it at once.

Add every branch the answers reveal to the tree. Ask a follow-up round only for questions the answers opened.

Show the user the full branch list, in roadmap order.

Gate: every branch node is settled, and the user approved the branch list.

## Step 5 — Leaves

Global mode walks the branches one at a time, in roadmap order. One round asks every leaf question of one branch.

Loop on a branch until its leaves are exhausted — a fresh look at the branch finds no open question. Then move to the next branch.

Per-phase mode asks every node in its tree in one round, and settles everything there. Ask a follow-up round only for questions the answers opened.

Per-phase mode asks each backlog item one question:

- bring it into this phase
- propose it as a new roadmap phase
- leave it for later

Before closing, name 2 to 6 decisions the interview never reached, that the draft still assumes. Route each as felt (ask now) or plumbing (record it).

Then play the settled tree back to the user in plain words. Ask one question: does this match what you mean?

Gate: every node in the tree file is settled, and the user said yes to the shared understanding.

## Step 6 — Write

Global mode writes the rest of `prd.md` from the settled tree, following `../../templates/prd.md`. The trunk is already there from Step 3.

Every roadmap line names its exact `spec/<phase-id>` path. Phase IDs use lowercase kebab-case.

Per-phase mode writes `spec/<phase>/user-stories.md`, following `../../templates/user-stories.md`, with status `draft`. A feature-phase item approved in Step 5 gets appended to `prd.md`'s Roadmap, as a new phase.

Gate:

- global mode only: all ten PRD sections exist, and each phase has one exact ID and directory
- per-phase mode only: Scope, Track, Stories, and `Not in this phase` are present, and every settled story appears once
- every settled node in the tree file appears in the doc
- the user approved the doc

## Step 7 — Review and close

Create a review-only checklist from the approved decisions. Check the finished document against it yourself.

Global mode and a deep-track phase spawn a blind agent for this check instead, at the deliberate tier. Use flagship when the document changes security, money, existing user data, concurrency, or a public API.

The check covers:

- Every settled node of the interview tree appears in the doc.
- Every user story names an actor and an outcome, not a general capability.
- Global mode only: every section is present, grounded in a settled decision.
- Global mode only: every product principle is something a reviewer could check on a screen.
- Global mode only: every "When is done" criterion is checkable, and names a real motivation.
- Per-phase mode only: an approved feature-phase item appears once in `prd.md`'s Roadmap.
- Every limit in the doc was stated by the user or proven by research, and names its scope.

Fix each finding once. A finding that needs a user decision returns to its node in Step 5. Any other finding returns to Step 6.

On pass, set the document status to `approved`.

Per-phase mode closes every folded-in backlog item. Rewrite each item instead of deleting it.

Commit the approved documents. Delete the interview tree file. Configure a remote only after the user approves its exact URL.

Gate: the status is `approved`. The working tree is clean. The remote matches the user's choice.

## Hand-off

Global pass moves to `autobuild:autobuild` — call the Skill tool with that id.

Per-phase pass moves to `autobuild:spec` — call the Skill tool with that id. A quick-track phase moves to `autobuild:implement` instead.
