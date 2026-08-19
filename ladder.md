# ladder.md

20 words a sentence. 2 sentences a line. Read this first, in every skill, to see where you sit.

```mermaid
flowchart TD
    migrate[migrate — once, from an old-stack project] --> prd
    migrate -.->|confirm| explore_g

    prd[(prd.md)]
    explore_g[explore — global] -->|writes| prd
    explore_p[explore — per-phase]
    prd -->|reads, reconciles| explore_p

    explore_p --> spec[spec] --> implement[implement] --> wrap[wrap]
    wrap -->|next phase| explore_p
    wrap -->|roadmap complete| done([roadmap done])

    prd -.->|reads| spec
    prd -.->|reads| implement
    prd -.->|reads| wrap

    explore_p -.->|pivot| replan[replan]
    spec -.->|pivot| replan
    implement -.->|pivot| replan
    wrap -.->|pivot| replan
    replan -.->|archive + fresh| explore_g

    backlog[(backlog.md)]
    wrap --> backlog
    explore_p -.->|reads| backlog
    polish[polish] <-.->|drains| backlog
```

Solid lines are the main loop. Dashed lines are on demand — a pivot, a drain, a one-time bridge.

Resuming after a break, or starting fresh? Call `autobuild:autobuild` — it reads `state.json` and hands off to whichever skill comes next.

Whatever's missing is next, build it, in this order.
