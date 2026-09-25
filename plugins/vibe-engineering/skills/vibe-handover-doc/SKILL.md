---
name: vibe-handover-doc
description: Writes a handover document so another person, another agent, or a different tool can pick up multi-session work cold. Use when handing work to someone else, switching tools, or pausing work that will not resume in the same session.
user-invocable: true
---

# vibe-handover-doc

Within one session, the harness handles continuity: context compaction, session resume, and memory files. A handover doc is for the moment that breaks: a different person, a different agent tool, or a fresh session days later. Write it for a reader who has none of your context.

## When to Use This Skill

- Handing work to a teammate or another agent
- Switching tools mid-project (for example, Claude Code to Codex or Gemini CLI)
- Pausing multi-session work that won't resume via session resume
- User says "save progress", "let's continue tomorrow", or "write this up for X"

## When NOT to Use This Skill

- To free up context in the current session (the harness compacts automatically; if you want to compact early, use its own command)
- Short sessions with trivial tasks
- Work that is fully committed, tested, and described in the PR (the PR is the handover)
- A current handover doc already exists (update it instead)

## Steps

1. **Capture state from the repo, not from memory**:
   - Branch, last commit, `git status` (uncommitted changes?)
   - Test status: run the suite and record pass/fail, don't guess
   - Open PR, CI state, unresolved review threads

2. **Document completed work** — What was done, key decisions (link `vibe-decision-journal` entries), problems solved and how.

3. **Document remaining work** — What's left, what's blocked and on what, known issues introduced, and approaches already tried and rejected (so the next person doesn't retry them).

4. **Write a resume prompt** — A self-contained prompt the next session can be started with: branch, files to read first, the next concrete task, and how to verify it.

5. **Save** to `docs/handover/YYYY-MM-DD-<topic>.md` (or `docs/HANDOVER.md` for a single rolling doc), and commit it if the next reader will work from a fresh clone.

## Output Format

### Handover: [Feature/Project Name]
**Date**: [today] · **Branch**: [branch] · **Last commit**: [sha]
**Tests**: [pass/fail counts, command used]

### Completed
- [x] [task]

### Remaining
- [ ] [task] — [notes]
- [ ] [task] — blocked by [X]

### Decisions & Dead Ends
- [decision] — [rationale / DEC-ID]
- Tried [approach], rejected because [reason]

### Known Issues
- [issue] — [impact]

### Resume Prompt
> [Self-contained prompt: context, branch, files to read first, next step, how to verify.]
