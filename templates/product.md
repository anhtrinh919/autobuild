# product.md schema

20 words a sentence. 2 sentences a line. An agent or designer reads this to learn what runs today.

A living doc. It states what the product is right now, rewritten in place. History belongs in `changelog.md`.

Wrap and Polish rewrite it before they close. A section with nothing to say is skipped.

## Screens

One line per screen a user can reach:

- <screen> — <what a user does there> — <how they reach it>

## Data

One block per entity a user's work lives in:

- <entity> — <what it holds>
  - Fields: <the fields a later phase needs to know>
  - Links: <other entities, one or many>

## Interfaces

One line per way in or out: an endpoint, a command, a job, or an outside service.

- <interface> — <what it does> — <who or what calls it>

## Look

Where the current design lives: a design tool file, a token file, or a component folder. One line each.

- <source> — <what it holds>

## Settled choices

One line per technical choice a later phase must build on: stack, hosting, auth, storage.

- <choice> — <why later work depends on it>
