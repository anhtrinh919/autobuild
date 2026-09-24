# design.md schema

30 words a sentence. Up to 4 sentences a paragraph. A designer reads the Handoff and Review. An agent reads the Source and Decisions.

A snapshot of this phase's design, dated. A decision here does not apply to any other phase.

## Source

Where the design lives. One line each:

- <design tool file link, or `spec/<phase>/design/<file>`> — <which screens and states it holds>

## Handoff

Write this section only when the design happens outside this session. Skip it when the design happens here in a design tool.

Write for a designer, or a fresh design agent, who has read nothing else. They were not in the interview and do not know the product's words.

### The product

Five lines at most, drawn from `prd.md`: what the product is, who uses it, its north star, and its product principles.

### This phase

What this phase adds, and the problem it solves for the user. Copy every story and acceptance criterion from `user-stories.md` word for word. Copy its `Not in this phase` list.

### What exists

The current look, which the design matches unless a story needs a change:

- Screens: <the screens this phase touches, from `product.md`>
- Screenshots: `spec/<phase>/design/current/<screen>-<state>.png`, captured from the running product
- Look: <every source in `product.md`'s Look section — tokens, components, a design tool file>

A first phase has no current look. Say so, and name the product principles the look must carry.

### What to beat

From `research.md`: the friction a user hits in comparable products, and what every comparable does the same way.

### Screens

One block per screen — a real surface a user is on, not a state of one:

- `<N>. <screen name>` — <what a user does here, and why>
  - Criteria: <every acceptance criterion this screen answers>
  - States: <one line per state: normal, empty, loading, error, mid-action>
  - Primary action: <what a user does here>
  - Content: <realistic sample data — the longest name, a typical count, a heavy count>
  - Copy: <one line per string, as `<what shows it>, <when> — <the string>`>

Write the real string, never a placeholder. Mark a string an earlier phase settled.

### Deliver

- Formats: <one image or frame per screen, per state, at each width the product runs on — phone 390px and desktop 1440px by default>
- Names: `<screen>-<state>-<width>.png` in `spec/<phase>/design/`, or one design tool link
- Expected files: <the full list, so the review can count them>

Layout, hierarchy, and visual detail are the designer's call, within the current look.

## Review

For the designer. One block per gap, grouped by screen, using the Handoff's own words:

- `<N>. <screen name>`
  - Missing: <the criterion, state, or delivered file the design has no answer for>
  - Wrong: <the product principle or criterion the design works against, and how>

## Decisions

For the contract and the product judge. One line per divergence between the design and the stories, with its winner:

- `<screen>, <item> — design | stories: <the settled answer, in one sentence>`

A `stories` winner tells the product judge that the built screen differs from the design on purpose.
