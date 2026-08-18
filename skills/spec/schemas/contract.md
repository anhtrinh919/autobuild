# contract.md schema

20 words a sentence. 2 sentences a line.

This file, the design brief, and `prd.md` are the whole brief a fresh session gets to build this phase.

## Data model

One entity per block. Each field with its type and the rule it follows.

Note every link to another entity, and whether it points to one row or many.

## Endpoints

One block per endpoint:

- `<METHOD> <path>` — <what it does> — <screen that calls it, or "internal">
- Who can call it: <role, or "any signed-in user">
- Sends: <field: type, required or optional>, one per line
- Returns, on success: <field: type>, one per line, with its status code
- On failure: <status code> — <what causes it>, one per line

## Sequence

Only for a mechanism that earns it — see Step 4's test in `SKILL.md`.

```mermaid
sequenceDiagram
    ...
```

One diagram per mechanism that earns it. Skip this section when nothing does.

## Business rules

One per line: the condition, and the result.

## Edge cases

One per line, tied to the rule or endpoint it belongs to: empty, error, boundary, and conflicting-write cases.
