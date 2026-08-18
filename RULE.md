# RULE.md

Writing style and shared vocabulary for every autobuild skill file.

## Style

- Write in ASD-STE100. Keep sentences active and short.
- Keep each sentence to 20 words. Keep each line to 2 sentences.
- State a rule once. Skip the reasons behind it.
- Turn judgment into gates, ladders, and checklists.
- Give every list a hard budget, checked by character count.
- Keep gate and pitfall lists few and hard.
- When a fact goes over budget, stop and ask.
- Use plain, common words. Check the table below first.
- State what a skill does and when to trigger it. Keep steps out of the description.
- Name the concrete things a user says in the description, not just the slash command. A command-only trigger under-triggers.
- Give each step one self-check gate. Keep the skill's end gate separate.
- A step whose output is a real decision gets a second gate: show it, get the user's approval. A purely mechanical step keeps only its self-check.
- Use a mermaid graph only when a step's logic truly cycles. Write gate checklists for the rest.
- Write each gate as a count or a yes/no. A vague check is not a gate.
- A gate checks the step's output, not that the step ran. "It ran" or "it's committed" is not a gate.
- A finding outside a step's own scope is logged, not fixed here. It never blocks that step's gate.
- Open every skill file with the same step/gate definition, as a list, not prose. Repeat this block itself in each file — do not cite another skill for it:
  - Step: one unit of work.
  - Gate: the check at the end of a step.
  - Pass a gate → move to the next step.
  - Fail a gate → redo the step, using the gate's findings.
  - Fail the same gate twice → stop, ask the user.
- `implement/SKILL.md`'s copy of this block differs by design — its fix-loop rules on failures instead of stalling on them. Read it there, not here.
- A decision is felt if the user would notice it, wait on it, or feel boxed in by it. Ask only felt decisions.
- Decide plumbing decisions yourself. Record only the settled fact, not the alternatives you considered.
- A mechanism earns a sequence diagram when at least two hold:
  - more than one actor takes part
  - the next action depends on state, not just data
  - a loop runs with more than one exit
  - wrong order causes a real bug
- A felt finding is never auto-backlogged — one the user would notice, wait on, or feel boxed in by. Surface it; the user picks fix-now or backlog.
- One idea forced across several lines belongs in a list instead.
- An item with more than two fields is one block per item, not a single-line row.
- Open every schema doc with its own word cap and sentence cap, first line.
- Fit that cap to who reads the produced doc. An agent-only doc stays tight. A doc a specialist reads for context can run looser.
- A produced doc never says "similar to X" or "TBD." It repeats the real content every time.
- A produced doc records positive facts only — what a thing is, does, or will do. Never write "never X," "no X," or "out of scope." State this again at every step that writes doc content. One central definition is not enough — a one-off exclusion, recorded once, reads later as a permanent boundary.
- One state script, `scripts/update-state.py`, shared by every skill. Extend it when a new skill's own output needs tracking. Do not add a field for a skill that is not built yet.

## Vocabulary

| Shorthand | Plain term |
|---|---|
