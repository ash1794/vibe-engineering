---
name: vibe-quality-loop
description: Runs the Implement→Review→Test→Fix cycle until the work is actually clean, with evidence. Use after any non-trivial implementation and before claiming it is done.
user-invocable: true
---

# vibe-quality-loop

The quality loop prevents premature "done" declarations. Keep iterating until the review is clean and the tests pass, and show the evidence.

## When to Use This Skill

- After an implementation that touches more than a couple of files or any non-trivial logic
- After implementing a feature with tests
- Before creating a commit or PR on completed work

## When NOT to Use This Skill

- Single-line fixes or typo corrections
- Documentation-only changes (use `vibe-doc-quality-gate`)
- When the user says "just get it working, we'll clean up later"

## The Loop

```
Implement → Self-review diff → Run checks ─┬─ clean + green → EXIT
                ↑                           │
                └──────── Fix issues ←──────┘
```

## Steps

1. **Review the diff** — Read the whole diff as a reviewer would. If the harness has a built-in review command (for example `/code-review` in Claude Code or `/review` in Codex), run it. Otherwise check for:
   - Bugs: wrong conditions, off-by-one errors, unhandled error paths, broken edge cases
   - Leftovers: unused imports and variables, debug output, commented-out code
   - Consistency: does it match the naming and idioms of the surrounding code?
   - Scope: anything not requested (`vibe-scope-guard`)
   - Test integrity: were any tests weakened to pass? (`vibe-anti-rationalization-check`)

2. **Run the project's own checks** — Use what the repo defines (Makefile, `package.json` scripts, CI workflow) rather than guessing:
   - Full test suite, not just the tests you wrote
   - Linter, formatter, type checker
   - The race detector for concurrent code where the language has one (e.g., `go test -race`)

3. **Fix** only the issues found. Don't add features while fixing.

4. **Loop** back to step 1. Track the iteration count.

5. **Exit** when the review is clean and all checks pass. Quote the final check output. Don't paraphrase it.

## Stop Conditions

- After 5 iterations without converging, stop and report what's stuck rather than looping further.
- A failure that also happens on the base branch is pre-existing. Report it; don't "fix" it silently in this change.

## Output Format

### Quality Loop: [Feature Name]

**Iterations**: X · **Final status**: CLEAN / KNOWN_ISSUES

| Iteration | Issues found | Fixed |
|-----------|-------------|-------|
| 1 | [list] | [list] |

**Final checks**: `[command]` → [result]

**Remaining known issues** (if any):
- [issue deliberately deferred, with justification]
