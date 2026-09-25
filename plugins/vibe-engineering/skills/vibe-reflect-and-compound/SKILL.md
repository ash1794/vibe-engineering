---
name: vibe-reflect-and-compound
description: Captures reusable knowledge after work is done — learnings from feedback or failures, resolved bugs (symptom, root cause, prevention), and recurring code patterns — into the project's persistent memory file. Use after feedback, a non-trivial bug fix, a failed attempt, or the third repetition of a pattern.
user-invocable: true
---

# vibe-reflect-and-compound

Every problem solved should leave something behind that makes the next one cheaper. This skill records it in the one place the agent will actually read next session.

## When to Use This Skill

- After receiving feedback on your work (positive or negative)
- After resolving a non-trivial bug: it took more than ~10 minutes, was hard to reproduce, or had a surprising root cause
- After a failed attempt or an approach that had to be abandoned
- When you implement the same code pattern for the third time
- At the end of a complex task

## When NOT to Use This Skill

- After trivial tasks (typos, renames, obvious fixes)
- When nothing new was learned
- During active implementation (reflect after, not during)
- For architectural decisions (use `vibe-decision-journal`, which keeps ADRs in the repo)

## Where to Save

Write to the memory file the current agent loads automatically. A separate `LEARNINGS.md` that nothing loads is write-only.

| Agent | Loaded automatically |
|-------|---------------------|
| Claude Code | `CLAUDE.md` (project) or auto-memory, if enabled |
| OpenAI Codex | `AGENTS.md` |
| Gemini CLI | `GEMINI.md`, or the built-in memory tool |
| Shared across tools | `AGENTS.md`, imported or referenced from the others |

Keep the always-loaded file short. Put long entries in `docs/learnings/` (bugs, patterns, learnings) and add a one-line pointer to them in the memory file.

## Entry Types

### 1. Learning
```
- **[Pattern name]**: [actionable rule]. Applies when: [context]. Evidence: [what happened].
```
Be actionable and specific. Not "be careful with concurrency" but "run the race detector before committing code that touches `sessionCache`."

### 2. Bug
```
### [Category]: [short description] ([date])
Symptom: [what was observed]
Root cause: [the actual problem]
Why hard to find: [what misled the investigation]
Fix: [what changed] — Prevention: [test, lint rule, or guard added]
Files: [paths]
```
Categories: Concurrency, State, Validation, Integration, Environment, UI.

### 3. Pattern (only at the third occurrence)
```
### [Pattern name] — [category]
When to use: [situation]
Canonical example: [file:line]
Anti-pattern: [the common mistake]
```
Point to the canonical implementation in the codebase instead of copying code into the memory file.

## Steps

1. **Gather** — What happened? What was expected vs. what actually happened? What was the root cause?
2. **Extract** — What would have caught this earlier? Is it a recurring theme? Search existing entries first, and update or merge instead of duplicating.
3. **Write** the entry in the right format.
4. **Prune** — Keep at most ~30 active learnings in the always-loaded file. Merge similar ones, and move stale ones to `docs/learnings/archive.md`.
5. **Confirm** — Show the entry to the user before saving if it changes shared project instructions.

## Output Format

### Reflection: [context]

**Trigger**: [what prompted this]

**Entries**:
1. [Type] **[Name]**: [one-line summary]

**Saved to**: [file path(s)]
**Active learnings**: X/30
