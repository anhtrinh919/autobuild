# git-workflow.md

15 words a sentence. The shared git and parallel-agent convention for every phase.

## Branch, per phase

Implement's Plan step creates the phase's branch, before Step 2 starts:

- Branch name: `phase-<N>-<slug>`, from the phase's own directory name under `spec/`.
- All of Implement's and Wrap's work for this phase happens on that branch.

Wrap's Finish step decides the branch's fate, matching its own four options:

- Merge or PR: merge the branch into the base branch, keep its history.
- Keep as-is: leave the branch alone.
- Discard: drop the branch.
