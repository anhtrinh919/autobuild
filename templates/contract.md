# contract.md schema

20 words a sentence. 2 sentences a line.

A snapshot doc. Date it. It is never revised after its phase ships.

This file, `design.md`, `prd.md`, and `product.md` are the whole brief a fresh session gets to build this phase.

This phase's contract only. A decision here does not apply to any other phase.

Status: `draft` during Spec. Set `approved` only after its final review.

## Data model

One entity per block. Each field with its type and the rule it follows.

Note every link to another entity, and whether it points to one row or many.

## Interfaces

Every way in or out of the product this phase adds or changes: an HTTP endpoint, a command, a job, an event, or an outside service. One block each:

- `<name>` — <what it does> — <the screen or caller that uses it, or "internal">
- Who can call it: <role, or "any signed-in user">
- Takes: <field: type, required or optional>, one per line
- Gives, on success: <field: type>, one per line, with its status or exit code
- On failure: <code> — <what causes it>, one per line

Name an HTTP endpoint as a noun path — plural for a collection, nested for a child. The method is the verb.

## Sequence

Only for a mechanism that earns it — see Step 3's test in `SKILL.md`.

```mermaid
sequenceDiagram
    ...
```

One diagram per mechanism that earns it. Skip this section when nothing does.

## Business rules

One per line: the condition, and the result. A rule that can fail names its error: a code, a message, and the field it points to.

## Edge cases

One per line, tied to the rule, interface, or field it belongs to. Write every case a real user or a real outage can cause.

Check each against these prompts, and write the ones that apply:

- A field: empty, at its limit, past its limit, a duplicate.
- An action: repeated, or two at once.
- An outside dependency: slow, or down.
