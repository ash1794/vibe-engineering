---
name: vibe-scope-guard
description: Detects and redirects scope creep during implementation — unrequested features, drive-by refactors, premature abstraction, and over-engineering. Use while implementing, especially when a change is growing beyond the original request.
user-invocable: true
---

# vibe-scope-guard

The best code is the code you don't write. Frontier coding models tend to over-build: extra configurability, defensive layers, helpers "for later." Stay on what was asked.

## When to Use This Skill

- During any implementation task
- When you notice you're "improving" code that wasn't in the request
- When the diff is noticeably larger than the request implies
- When you're about to create an abstraction "for later"

## When NOT to Use This Skill

- During brainstorming (ideas should be unconstrained)
- When the user explicitly asks for broad improvements
- When the extra work is necessary for correctness (a bug in the code path you're changing)

## Scope Creep Signals

| Signal | Example | Response |
|--------|---------|----------|
| Unrequested features | "While I'm here, let me add caching" | Was caching requested? |
| Premature abstraction | "Let me create a generic helper for this" | Is there a second caller today? |
| Gold plating | "Comprehensive error messages for every case" | Only at system boundaries |
| Drive-by refactor | "This function could be cleaner" | Not in this change |
| Over-engineering | "Let me make this configurable" | Does anyone need to configure it? |
| Defensive sprawl | Validation and fallbacks for states that can't occur | Trust internal invariants; validate at the boundary |
| Documentation creep | "Docstrings on all these functions" | Only on what you changed |
| Test over-expansion | "Test every possible input" | Test boundaries and behaviors, not permutations |

## The Rule

**Three similar lines of code are better than a premature abstraction.**

Before adding anything not explicitly requested:
1. Was it requested? → No →
2. Is it required for the requested change to be correct? → No →
3. **Don't add it.** Mention it as a suggestion in the summary if it's worth the user's attention.

## Steps

When you detect scope creep:
1. **Stop** — Don't commit the extra work
2. **Revert** it if it's already written
3. **Note** it: "Also noticed: [X]. Not changed; want a follow-up?"
4. **If the user accepts** — do it as a separate, clearly labeled change

## Output

This skill mostly changes behavior rather than producing output. When invoked explicitly:

### Scope Audit
**Original request**: [what was asked]
**Scope additions detected**: X

| Addition | Requested? | Needed for correctness? | Action |
|----------|-----------|------------------------|--------|
| [extra work] | No | No | Removed; suggested as follow-up |
