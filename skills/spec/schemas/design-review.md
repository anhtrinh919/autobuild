# design-review.md schema

25 words a sentence. Up to 3 sentences a paragraph. A designer reads the gaps, and an agent reads the winners.

This phase's screens only. A decision here does not apply to any other phase.

Date it. Name the design files it reviews.

## Gaps

For the designer. One block per gap, grouped by screen.

- `<N>. <screen name>`
  - Missing: <the brief item the design has no answer for>
  - Wrong: <the rule under `What has to hold` the design works against, and how it does>

Use the brief's own words for each item. A designer reading this page has the brief open, not the contract.

Write for someone who was not here. Say which screen, which state, and what the user has to be able to do there.

## Winners

For the agent that writes the contract, and for the visual check in `implement`.

One line per divergence, as `<screen>, <item> — design | brief: <the settled answer, in one sentence>`.

A `brief` winner tells the visual check that the built screen differs from the design on purpose.

A `Winners` block reads like this:

```
- Turn list, empty state — design: the illustration and one line replace the brief's two lines.
- Composer, send control — brief: the control stays visible while a turn runs.
```
