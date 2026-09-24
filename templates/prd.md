# prd.md schema

20 words a sentence. 2 sentences a line.

```
# <one-line outcome>
```

A living doc. It always states the product as intended today, rewritten in place.

Status: `draft` during Explore or `migrating` during Migrate. Set `approved` after final review.

## Concept

One paragraph. What this is, who it is for, why it matters now.

## North star

One line. What a user remembers or feels after using this.

## Product principles

Three to seven rules a reviewer can judge a screen against. Each names something a user feels, not a feature.

- <principle> — <what honouring it looks like on a screen>

## Target users

One entry per actor:

- <actor> — <their one real need>

## User stories

Global scope only. Each phase's own stories live in `spec/<phase>/user-stories.md`, not here. Group by actor.

- As <actor>, I can <specific action>, so that <specific outcome>.
  - Given <a starting condition>, when <the action>, then <the result>.

One to three criteria per story. Each story stands alone, delivers real value on its own, is small enough for one phase, and is testable.

## Functional requirements

Grouped by feature. Each requirement is a rule, not a description.

- <feature>: <the specific behavior or rule, stated so a reader can tell if the build follows it>
  - Edge cases: <empty, error, and boundary states this rule must handle>

## Non-functional requirements

One line per target the user stated or research proved, each with a number, not an adjective. Skip the section when none exists.

- <category: performance, security, reliability, scale, or usability>: <the target, with its number>

## Assumptions and constraints

One per line, each tagged.

- Assumption: <believed true, not yet verified>
- Constraint: <a hard limit — budget, technology, timeline>
- Non-goal: <what the user chose to leave out of the whole product, and why>

Write a constraint or non-goal only when the user stated it or research proved it.

## Roadmap

One phase per line, in build order. Each line owns one exact phase ID, directory, and status.

- [phase-<N>-<slug>] `planned` <name>: <what it delivers> — <why it is next>

Status is `planned` until Wrap ships the phase, then `shipped`. The router reads only this status.

The phase directory is `spec/<phase-id>`. Use lowercase kebab-case. Never derive it later.

The first phases deliver the core promise — the one thing the product fundamentally does — end to end, as thin as it can run.

Every phase after that is one vertical slice — one thing the product can do, or the user can.

Slice by user-facing value, never by pipeline's-own-work-order, an output-class ladder, or a single artifact's property. Run the slice test on each phase: a user outside the team can say what changed. If the user calls the roadmap illogical, the axis is wrong, not the phase — reslice from a different axis, don't reorder within this one.

## When is done

Checkable criteria, one per line. Each names the real motivation it answers — a pain relieved, or a want satisfied — not a restated feature.

- <criterion>, because <the motivation>
