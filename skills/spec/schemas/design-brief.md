# design-brief.md schema

35 words a sentence. Up to 5 sentences a paragraph. A designer reads this, not an agent — give it room.

Write for a designer who has read nothing else. They have not sat through the interview, they do not know the product's words, and they are not reading the code. A sentence that only makes sense to someone who was here is a sentence to rewrite.

This brief is a snapshot, dated on the day it is written. It stands as what was true then. The contract carries the phase forward, and the contract wins wherever the two disagree.

No style guide, layout, or design system. That call belongs to the designer, not this brief.

This phase's screens only. A choice here does not apply to any other phase.

## The product

What the product is, who uses it, and what it does for them. Where this phase sits in the roadmap, and what comes after it.

The first phase writes this in full — the designer is meeting the product here, and every later screen is drawn on the mental model this section builds. A later phase writes a paragraph, enough to place the phase in the whole.

A later phase writes it in full again when the roadmap pivots. A designer working from last month's model draws the wrong screen.

## This phase

What this phase adds, why it is next, and the problem it solves for the user. As many paragraphs as the feature needs.

What already runs, where this phase touches it. Check every one of those sentences against the running application, not against an earlier document. A phase before this one may have moved what an old doc describes.

## What the research found

From `research.md`, in the designer's terms. The comparable products, what each does well, and the friction a user hits in it.

Name what this design has to beat, and what it can take as settled because everyone does it the same way.

## What has to hold

The rules the design has to satisfy, as behaviour. What appears, what stays put, what the user can always reach, what they can always tell apart.

Behaviour, never style. How a thing moves, how fast, and on what curve is the designer's own call. What must not move is this brief's.

Write none of these when the phase has none. Write every one that the phase turns on.

## Screens

One block per screen — a real surface a user is on, not a state of one. A phase that changes one screen has one block, however many states it holds.

- `<N>. <screen name>` — <what this surface is, and why a user is on it>
  - Stories: <every user story this screen serves>
  - Criteria this screen answers: <one line per acceptance criterion, in the user's words>
  - States: <one line per state that needs a design decision — loading, empty, error, mid-flight, and the normal case>
  - Primary action: <what a user does here>
  - Copy: <every real string this screen shows, one per line, not a placeholder>
