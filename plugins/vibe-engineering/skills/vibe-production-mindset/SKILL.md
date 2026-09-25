---
name: vibe-production-mindset
description: Checks production-bound code for observability, error handling at system boundaries, input validation, graceful degradation, and resource management, scaled to the project's real stakes. Use before declaring a production feature done.
user-invocable: true
---

# vibe-production-mindset

The gap between "works on my machine" and "works in production" is where incidents live. The goal is to avoid under-engineering the critical paths, not to add every hardening pattern to every feature. Pair it with `vibe-scope-guard`.

## When to Use This Skill

- Implementing API endpoints, data processing, or user-facing features that will run in production
- Before declaring a production feature "done"
- When the user cares about production quality

## When NOT to Use This Skill

- Prototypes or spikes explicitly marked as throwaway
- Internal scripts that run once
- Test code (different quality criteria)
- When the user says "just get it working"

## Calibrate First

Before running the checklist, establish the stakes and the conventions:
- **What already exists?** Use the project's existing logger, metrics, retry, and validation libraries. Don't introduce a second one.
- **What's the real scale and blast radius?** An internal admin tool and a public payments API need different answers.
- Only flag an item if it applies at *this* project's scale. A missing circuit breaker is not a gap in a service with one dependency and ten users.

## The Checklist

### 1. Observability
- [ ] Logs at key decision points use the project's structured logger
- [ ] Request/correlation IDs are propagated, if the project already uses them
- [ ] Metrics for key operations, if the project has a metrics pipeline

### 2. Error Handling at System Boundaries
- [ ] External calls (HTTP, DB, queues) have timeouts
- [ ] Retries with backoff where the operation is idempotent
- [ ] Specific handling for expected failures (not found, permission denied, conflict)
- [ ] Errors carry enough context to debug, and no secrets

### 3. Input Validation
- [ ] External input is validated before processing
- [ ] Size limits on strings, arrays, and uploads
- [ ] Parameterized queries and output encoding (injection, XSS)
- [ ] Authentication before authorization, and authorization on every access path

### 4. Graceful Degradation (only where dependencies justify it)
- [ ] Defined behavior when a dependency is down
- [ ] Graceful shutdown (drain in-flight work)
- [ ] Health check, if the deploy target uses one

### 5. Resource Management
- [ ] Connections, files, and handles are closed or returned to the pool
- [ ] Goroutines, threads, and tasks have bounded lifetimes
- [ ] No unbounded in-memory growth (caches, queues, buffers)

## Steps

1. **Calibrate** (above)
2. **Read the implementation**
3. **Run the checklist**, skipping items that don't apply
4. **Flag gaps** with `file:line` and a specific fix that uses existing project conventions

## Output Format

### Production Readiness: [Feature Name]

**Stakes**: [e.g., public API, ~10k req/min] · **Overall**: READY / NEEDS_WORK / NOT_READY

| Category | Status | Gaps |
|----------|--------|------|
| Observability | ✓/◐/✗/n/a | [count] |
| Error Handling | ✓/◐/✗/n/a | [count] |
| Input Validation | ✓/◐/✗/n/a | [count] |
| Graceful Degradation | ✓/◐/✗/n/a | [count] |
| Resource Management | ✓/◐/✗/n/a | [count] |

### Critical Gaps
1. [gap with file:line and the fix]
