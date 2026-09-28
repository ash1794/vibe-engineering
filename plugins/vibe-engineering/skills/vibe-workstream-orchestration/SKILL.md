---
name: vibe-workstream-orchestration
description: Runs a multi-phase project from an orchestrating main thread that plans, routes and verifies but does not build. Defines a few long-lived workstreams, each owning a file area end to end in its own worktree, and routes every follow-up to the owning agent instead of spawning a one-off. Covers base-SHA recording, rebase-before-commit, stale-checkout detection, and shared-machine hygiene (ports, processes, measurement noise). Use when a project spans several phases or sessions with three or more agents working at once.
user-invocable: true
---

# vibe-workstream-orchestration

`vibe-parallel-task-decomposition` answers "what can run at once?" This skill answers the next question: who owns what for the rest of the project, and what does the main thread do while they work? The main thread plans, routes and verifies. If it starts building, its context fills with detail and parallelism collapses. If it delegates reactively, every request becomes a new agent that needs a fresh brief, and nobody owns the result.

## When to Use This Skill

- A build runs over several phases (build, review, fix, QA) with three or more agents at once
- The task list is filling with agents that did one thing (commit, fix one CI failure, write a PR description)
- Agents are colliding: the same files, the same port, a branch moved under someone
- The main thread's context is filling with build output instead of decisions

## When NOT to Use This Skill

- One agent can do the work in one sitting
- A one-shot fan-out with no follow-ups (use `vibe-parallel-task-decomposition`)
- The work is all in one file or in tightly coupled files
- The harness can't message a running agent (define streams anyway, but expect to re-brief)

## Steps

1. **Define workstreams by file ownership.** Use three to eight streams, each owning a set of paths end to end. For each stream, write down: paths owned, acceptance criteria, gates it must pass, and paths it must not touch. Shared files (global styles, layout, config) get exactly one owner; other streams request changes to them through the orchestrator.

2. **Record the base.** Note the base commit SHA and branch for the phase. Each writing stream gets its own worktree (or clone) from that base. Read-only agents (reviewers, auditors) can share one.

3. **Brief once, for the whole phase.** Each brief contains the ownership map, the gates, the commit rule ("rebase onto the remote branch, rebuild, run gates, then push; never force"), and a bounded report format. Ask for conclusions, not file dumps.

4. **Owners do the whole loop.** Each stream builds, verifies, commits and pushes its own work. Don't spawn separate committer, fixer, or description-writer agents.

5. **Route, don't spawn.** Send each new request, review finding, or CI failure to the stream that owns the file, as a message to the running agent. Spawn a new agent only for a new file area or a new phase.

6. **Distrust every checkout.** Before building or committing, compare the working tree to the remote branch. A clean local build can depend on another agent's uncommitted edit in a shared tree, which CI won't have. If the main checkout is behind or dirty, find out which commit it matches before you reset it.

7. **Keep the machine fair.** Worktrees isolate files, not the machine. Give each agent a private port and a distinct server process. Record machine load alongside any timing measurement, and don't trust results taken under heavy load (`vibe-flake-root-cause`). Each agent stops the servers it started.

8. **Gate the combined head.** After the streams land, run the full gates on the integrated commit, not per stream. Route failures back to their owners. Then remove worktrees and stale branches. A subagent may not be able to remove its own worktree, so the orchestrator cleans up.

## Output Format

### Workstream Plan: [phase]
**Base**: [branch] @ [sha] · **Streams**: N · **Gates**: [list]

| Stream | Owns (paths) | Must not touch | Acceptance | Gates |
|--------|--------------|----------------|-----------|-------|
| WS1 routing | app/routes, lib/redirects | global styles | all old URLs redirect | build, route check |

### Routing Log
| Item | Source | Routed to | Status |
|------|--------|-----------|--------|
| CSS over budget on /x | perf gate | WS3 | fixed abc1234 |

### Integration
- Combined head: [sha] · gates: [pass/fail per gate]
- Worktrees removed: [list] · open items: [list]
