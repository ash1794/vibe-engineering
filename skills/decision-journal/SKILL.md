---
name: vibe-decision-journal
description: Record architectural and technology decisions in ADR format for cross-session persistence. Use after making any significant design choice.
user-invocable: true
---

# vibe-decision-journal

Record decisions so future-you (or future-Claude) doesn't re-debate settled questions.

## When to Use This Skill

- After choosing a technology, framework, or pattern
- After making an architectural decision
- After deciding NOT to do something (negative decisions are valuable)
- When you realize "we keep coming back to this question"

## When NOT to Use This Skill

- Trivial implementation choices (variable naming, formatting)
- Decisions already documented in the project's ADR or design docs
- Temporary/reversible choices (which test to run first)

## Steps

1. **Capture the decision** in ADR format:

```
## Decision: [Short title]
**Date**: [Today]
**Status**: Accepted

### Context
[What situation prompted this decision? What constraints exist?]

### Decision
[What did we decide? Be specific.]

### Alternatives Considered
1. [Alternative A] — Rejected because [reason]
2. [Alternative B] — Rejected because [reason]

### Consequences
- [Positive consequence]
- [Negative consequence / trade-off]

### Affected Files
- [path/to/file.ext]
```

2. **Store it** — Use one of:
   - MCP memory (if available): `mcp__plugin_claude-mem_mcp-search__save_memory` with title "DECISION: [topic]"
   - Project file: append to `docs/decisions/` or `docs/adr/`
   - Memory file: append to Claude's auto-memory

3. **Cross-reference** — If this decision affects other decisions, note the connections.

## Output Format

Present the ADR to the user for confirmation before saving. Keep it concise — 10-20 lines max.
