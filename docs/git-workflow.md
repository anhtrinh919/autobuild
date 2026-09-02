# git-workflow.md

15 words a sentence. The shared git and parallel-agent convention for every phase.

## Branch, per phase

Implement's Plan step creates the phase's branch, before Step 2 starts:

- Branch name: `phase-<N>-<slug>`, from the phase's own directory name under `spec/`.
- Base branch: the exact branch recorded in `plan.md` before phase branch creation.
- All of Implement's and Wrap's work for this phase happens on that branch.

Wrap's Finish step decides the branch's fate, matching its own four options:

- Merge: merge the complete phase branch into its recorded base. Keep its history.
- Pull request: push the complete phase branch. Open a pull request without merging locally.
- Keep as-is: leave the branch alone.
- Discard: require typed `discard`, then drop the branch.
