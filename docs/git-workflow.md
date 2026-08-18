# git-workflow.md

15 words a sentence. The shared git and parallel-agent convention for every phase.

## Branch and worktree, per phase

Implement's Plan step creates the phase's branch and worktree, before Step 2 starts:

- Branch name: `phase-<N>-<slug>`, from the phase's own directory name under `spec/`.
- Enter a worktree for that branch. All of Implement's and Wrap's work for this phase happens there.

Wrap's Finish step decides the worktree's fate, matching its own four options:

- Merge or PR: merge the branch, keep the worktree's history, exit the worktree.
- Keep as-is: exit the worktree, leave the branch alone.
- Discard: exit the worktree and remove it, drop the branch.

## When to run agents in parallel

Already the pattern in every skill — canon, not new:

- Non-blocking research dispatch, while the interview keeps moving: Explore's frontier sub-agents.
- Batched dispatch for small, same-shape work: Implement batches same-shape trivial tasks into one dispatch, not one agent each.
- A fresh subagent per review, never the implementing context: every two-stage review in Implement, every Audit/Dogfood subagent in Wrap.

Phases run one at a time. Each phase's spec depends on the last one's actual, shipped outcome, not its plan.
