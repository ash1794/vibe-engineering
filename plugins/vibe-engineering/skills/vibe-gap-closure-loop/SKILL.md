---
name: vibe-gap-closure-loop
description: Closes a large backlog of findings (a gap analysis, an audit, or 10+ bugs) in prioritized waves. Loops through triage, dependency analysis, parallel fix streams, a test gate, and re-audit until the target is met.
user-invocable: true
---

# vibe-gap-closure-loop

When you have 50 findings, don't fix them in random order. Triage them into priority waves, fix each wave in parallel streams where dependencies allow, and don't start the next wave until tests pass.

## When to Use This Skill
- After `vibe-gap-analysis` produced a gap report
- After any audit, review, or `vibe-spec-sync` audit that produced 10+ findings
- A backlog of 10+ bugs or tech-debt items
- Production readiness sprints

## When NOT to Use This Skill
- Fewer than 5 findings (just fix them directly)
- Findings that need architectural redesign (use `vibe-research-before-design` first)
- All findings are in one file (a single focused pass is simpler)

## Arguments

```
/vibe-gap-closure-loop [dimensions] [--target N] [--gap-file PATH]
```

- `dimensions`: Which gap-analysis dimensions to close (default: all with open findings)
- `--target`: Target score per dimension (default: `95`)
- `--gap-file`: Path to the findings (default: latest `docs/plans/gap-analysis-*.md`, or ask)

## Autonomy

Follow the harness's permission mode. Under an autonomous or auto-approve mode, run the loop without stopping between phases. Otherwise, confirm the wave plan once before Step 3, then continue. Always stop and ask before destructive operations (migrations on real data, force-pushes, deleting files outside the findings' scope).

## Step 1: Triage into Waves

Assign every finding a priority:
- **P0 — Blocker**: security vulnerability, data-loss risk, breaks core functionality
- **P1 — High**: wrong behavior, significant UX issue, missing critical feature
- **P2 — Medium**: incomplete implementation, minor bugs, documentation gaps
- **P3 — Low**: polish, optimization (candidates for deferral to the backlog)

Wave 0 = all P0, Wave 1 = P1, and so on. **Don't start wave N+1 until wave N passes the test gate.**

## Step 2: Dependency Analysis & Streams

Within the current wave, build a dependency graph:
- Security findings block everything else
- Schema/migration changes block feature work on those tables
- "Add X to Y" depends on Y existing
- Test-infrastructure changes block test-dependent findings
- Trivial fixes have no dependencies, so batch them together

Group into **parallel streams** (use `vibe-parallel-task-decomposition` for large waves):
- 3–7 related findings per stream, sized for one agent session
- **No two streams touch the same files** (the main source of integration conflicts)
- A stream that depends on another stream's output moves to the next iteration

## Step 3: Dispatch Streams

If the harness supports subagents, dispatch one per stream in parallel, ideally in isolated worktrees. Otherwise, run the streams sequentially yourself. Let the subagents inherit the session's model unless the user specified one.

Stream prompt:
```
You are closing findings for [project].

Stream: [name]
Findings: [IDs with full descriptions]

For each finding:
1. Read the relevant source files
2. Implement the fix described
3. Add or adjust a test that fails before the fix and passes after
4. Run the project's test command

Commit with: fix([area]): close [finding IDs]
Do NOT commit if tests fail. Do NOT weaken or delete existing tests to make them pass.
Return: findings closed, findings not closed (with reason), commit hashes.
```

## Step 4: Test Gate

After all streams return:
1. Integrate the stream branches (`vibe-cherry-pick-integration` if they were isolated)
2. Run the **full** test suite and linters
3. Fix failures directly (often interactions between streams)
4. Commit any remaining fixes

## Step 5: Iteration Summary

Write `docs/plans/closure/iteration-N-summary.md`: streams, findings closed, commit hashes, cumulative progress, remaining open findings, and test results.

## Step 6: Check Target

- Re-audit the target dimensions (`vibe-gap-analysis --dim N`) or re-check the findings list
- All targets met → **DONE**: commit and report
- Otherwise → next wave or next iteration, back to Step 2

## Limits

- **Max iterations**: 5 per invocation
- **Max parallel streams**: whatever the harness handles well; 3–5 is a sensible default
- **Max findings per stream**: 7
- **Escalate**: a finding that fails to close after 2 iterations gets flagged for human review, not retried indefinitely

## Output Format

### Gap Closure: [project]

**Findings**: X total · **Closed**: Y · **Deferred**: Z · **Escalated**: W

| Wave | Priority | Findings | Status |
|------|----------|----------|--------|
| 0 | P0 | 3 | Complete |
| 1 | P1 | 12 | In progress (8/12) |
| 2 | P2 | 25 | Pending |
| 3 | P3 | 10 | Deferred to backlog |

| Stream | Findings | Commits | Tests after |
|--------|----------|---------|-------------|
| Security | C-1, C-2, H-1 | abc123 | PASS |

### Escalated to Human Review
- [finding] — [why it didn't close]
