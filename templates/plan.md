# plan.md schema

20 words a sentence. 2 sentences a line. An agent reads this — keep it exact, not descriptive.

A snapshot doc. Date it. It is never revised after its phase ships.

This phase's plan only. A decision here does not apply to any other phase.

## Status

`building` while any build or review work remains. `verified` only after the final review passes.

Base branch: `<exact branch name>`

Acceptance tests: `<tool>` — `<path>`

## Approach

One paragraph. The shape of the solution, and why the files break down this way.

## Files

One line per file:

- <path> — create or modify — <its one job>

## Tasks

One block per task, numbered, small enough to finish and commit on its own:

- `<N>. <task name>`
  - Files: <exact paths this task touches>
  - Tier: `standard`, `deliberate`, `flagship`, or `exceptional`
  - Test: <the behaviour the failing test proves, with its input and expected result>
  - Run: `<the exact command>` — expected: `<the exact failure message>`
  - Commit: `<the exact commit message>`

No "TBD", "similar to Task N", or "add appropriate handling." Every task carries its own facts. The writer writes the code.
