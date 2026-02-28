---
name: vibe-quality-loop
description: Enforce the Implement→Review→Test→Fix→Loop cycle until work is clean. Use after any non-trivial implementation to prevent "good enough" exits.
user-invocable: true
---

# vibe-quality-loop

The quality loop prevents premature "done" declarations. You keep iterating until the work is actually clean.

## When to Use This Skill

- After any implementation that touches more than 3 files
- After implementing a feature with tests
- When you've made changes and want to verify quality
- Before creating a commit on completed work

## When NOT to Use This Skill

- Single-line fixes or typo corrections
- Documentation-only changes
- When the user says "just get it working, we'll clean up later"

## The Loop

```
┌─────────────┐
│  Implement   │
└──────┬──────┘
       v
┌─────────────┐
│ Self-Review  │ ← Read your own diff. Would you approve this PR?
└──────┬──────┘
       v
┌─────────────┐
│  Run Tests   │ ← ALL tests, not just the ones you wrote
└──────┬──────┘
       │
       ├── Tests pass + Review clean → EXIT (done!)
       │
       v
┌─────────────┐
│  Fix Issues  │ ← Fix what broke, don't add new features
└──────┬──────┘
       │
       └── Go back to Self-Review
```

## Steps

1. **Self-Review** — Read your entire diff. Check for:
   - Unused imports/variables
   - Hardcoded values that should be constants
   - Missing error handling at system boundaries
   - Functions over 50 lines
   - Any TODO without an issue reference

2. **Run Tests** — Run the full test suite, not just affected tests:
   - If Go: `go test ./...` and `go test -race ./...`
   - If JS/TS: `npm test` or equivalent
   - If Python: `pytest`
   - Note any failures

3. **Fix Issues** — Address ONLY the issues found. Don't add features.

4. **Loop** — Go back to step 1. Track iteration count.

5. **Exit** — When tests pass AND review is clean. Report iteration count.

## Output Format

### Quality Loop: [Feature Name]

**Iterations**: X
**Final Status**: CLEAN / KNOWN_ISSUES

| Iteration | Issues Found | Issues Fixed |
|-----------|-------------|-------------|
| 1 | [list] | [list] |
| 2 | [list] | [list] |

**Remaining Known Issues** (if any):
- [Issue that was deliberately deferred, with justification]
