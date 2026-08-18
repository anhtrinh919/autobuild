# plan.md schema

20 words a sentence. 2 sentences a line. An agent reads this — keep it exact, not descriptive.

## Approach

One paragraph. The shape of the solution, and why the files break down this way.

## Files

One line per file:

- <path> — create or modify — <its one job>

## Tasks

One block per task, numbered, small enough to finish and commit on its own:

- `<N>. <task name>`
  - Files: <exact paths this task touches>
  - Test: the failing test's real code, in full
  - Run: `<the exact command>` — expected: `<the exact failure message>`
  - Then: the minimal code that makes it pass, in full
  - Commit: `<the exact commit message>`

No "TBD", "similar to Task N", or "add appropriate handling." Every task carries its own full content.
