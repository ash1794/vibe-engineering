---
name: vibe-parallel-task-decomposition
description: Analyzes large tasks for independent subtasks that can be safely parallelized. Produces a DAG-based dispatch plan with dependency ordering and maximum parallelism.
user-invocable: true
---

# vibe-parallel-task-decomposition

Large tasks are often collections of independent subtasks hiding behind a sequential mental model. Find the parallelism.

## When to Use This Skill

- Facing a task with 5+ subtasks
- Multiple files need changes that don't depend on each other
- Implementation plan has steps that could run concurrently
- User asks to "speed this up" or "parallelize"

## When NOT to Use This Skill

- Tasks with fewer than 3 subtasks
- All subtasks depend on each other sequentially
- Changes are all in the same file
- The overhead of coordination exceeds the benefit

## Steps

1. **List all subtasks** from the plan or requirements

2. **Build dependency graph** — For each pair of tasks, ask:
   - Do they modify the same file? → dependent
   - Does task B need output from task A? → dependent
   - Do they share mutable state? → dependent
   - Otherwise → independent (can parallelize)

3. **Group into batches**:
   - **Batch 0**: Tasks with no dependencies (run first, in parallel)
   - **Batch 1**: Tasks that depend only on Batch 0 (run after Batch 0, in parallel)
   - **Batch N**: Continue until all tasks assigned

4. **Set parallelism limit** — Use the harness's native parallelism (subagents, background tasks, workflows, or cloud tasks) and respect its concurrency limits. Past a handful of concurrent streams, the integration and review cost usually outweighs the speedup, so 3–5 is a sensible default unless the tasks are trivially independent.

5. **Isolate** — Give each parallel stream its own worktree or branch if the harness supports isolation, so streams can't overwrite each other's files. Integrate afterwards with `vibe-cherry-pick-integration`.

6. **Create dispatch plan**:

## Output Format

### Parallel Task Decomposition

**Total Tasks**: X
**Batches**: Y
**Max Parallelism**: Z agents
**Estimated Speedup**: ~Nx vs sequential

### Dependency Graph
```
Task A ──→ Task D
Task B ──→ Task D
Task C (independent)
Task D ──→ Task F
Task E (independent)
```

### Dispatch Plan

| Batch | Tasks | Parallelism | Dependencies |
|-------|-------|-------------|-------------|
| 0 | A, B, C, E | 4 | None |
| 1 | D | 1 | A, B |
| 2 | F | 1 | D |

### Per-Task Assignments
- **Task A**: [files], [description], [acceptance test]
- **Task B**: [files], [description], [acceptance test]

### Integration Order
After all batches complete, integrate in order: [A, B, C, E] → D → F
