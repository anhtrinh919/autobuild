# prd.md schema

20 words a sentence. 2 sentences a line.

```
# <one-line outcome>
```

## Concept

One paragraph. What this is, who it is for, why it matters now.

## North star

One line. What a user remembers or feels after using this.

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

One line per requirement that applies, each with a number, not an adjective. Skip a category with nothing to say.

- Performance: <a specific target, e.g. responds inside 2 seconds>
- Security: <a specific rule, e.g. passwords never stored in plain text>
- Reliability: <a specific target, e.g. 99.9% uptime>
- Scalability: <a specific ceiling, e.g. holds 1,000 concurrent users>
- Usability: <a specific target, e.g. a new user completes signup in under 2 minutes>

## Assumptions and constraints

One per line, each tagged.

- Assumption: <believed true, not yet verified>
- Constraint: <a hard limit — budget, technology, timeline>

## Roadmap

One phase per line, in build order.

- Phase <N> — <name>: <what it delivers> — <why it is next>

Slice by user-facing value, never by pipeline's-own-work-order, an output-class ladder, or a single artifact's property. Run the slice test on each phase: a user outside the team can say what changed. If the user calls the roadmap illogical, the axis is wrong, not the phase — reslice from a different axis, don't reorder within this one.

## When is done

Checkable criteria, one per line. Each names the real motivation it answers — a pain relieved, or a want satisfied — not a restated feature.

- <criterion>, because <the motivation>
