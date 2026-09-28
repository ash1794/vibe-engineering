---
name: vibe-flake-root-cause
description: Refuses "flaky" as a diagnosis. Turns an intermittent failure into a reproduction by isolating it from the environment, naming the variable that controls it, forcing that variable, and measuring before and after with enough runs to count. Separates real defects from environment contention with evidence, and never retries to green or widens a threshold. Use when a test, performance check, or deploy step fails intermittently or passes on rerun.
user-invocable: true
---

# vibe-flake-root-cause

"Flaky" ends an investigation without finding anything, and a retry-to-green hides real defects. An intermittent failure is a hypothesis: some variable you haven't controlled decides the outcome. Find it, force it, and prove the fix with counts.

## When to Use This Skill

- "It passed on rerun"
- A failure that shows up only in CI
- A threshold (performance, visual diff, timeout) that fails on some runs
- You're tempted to add a retry, raise a timeout, or loosen a tolerance

## When NOT to Use This Skill

- The failure reproduces every time (debug it directly)
- Race conditions visible in the test code itself (use `vibe-concurrent-test-safety`)
- The job died before any test ran (checkout, install, runner loss); a single re-run is fine there, but say so

## Steps

1. **Record the failure exactly.** Commit, environment, profile or device, the failing value, and the threshold. Keep the log.

2. **Run it alone, cleanly.** If it passes in isolation, treat it as contention until proven otherwise, and name the resource: CPU, a shared port, a shared database, disk, or network. Record machine load alongside every timing measurement.

3. **List candidate variables** and force each in turn. Common ones:
   - timing: network latency, font or asset arrival, animation frames
   - environment: CPU load, parallel agents or tests, shared ports and servers
   - data: ordering, time of day, random seeds, page or payload size
   - process mode: a server started in a mode the framework doesn't support in production

4. **Reproduce at a stated rate** before changing anything (for example "10 of 15 runs fail with fonts held back 600 ms"). No reproduction means no root cause yet, so keep looking or report it as unresolved.

5. **Fix the cause, not the symptom.** Then rerun the forced condition N times and report the new rate (for example "0 of 240 loads across 4 routes").

6. **Disclose any mitigation.** If you clip, retry, or quarantine anything, say what, why, and why it doesn't hide a defect. Never widen a threshold or budget to pass (`vibe-anti-rationalization-check`).

## Output Format

### Flake Investigation: [test/check]

**Symptom**: [value vs threshold, where, how often]
**Isolated run**: pass / fail · **Load at failure**: [value]

| Variable | Forced how | Failure rate |
|----------|-----------|--------------|
| font arrival | held back 600 ms | 10/15 |
| CPU load | run alone | 0/15 |

**Root cause**: [mechanism, in one or two sentences]
**Fix**: [change] · **After**: [0/N under the forced condition]
**Mitigations disclosed**: [none / list with reasons]
