---
name: vibe-anti-rationalization-check
description: Catches shortcuts and reward hacking — weakening or deleting tests to make them pass, hard-coding expected outputs, silently dropping requirements, or claiming work is done without running it. Use before declaring a task complete and whenever a test or requirement feels like it's in the way.
user-invocable: true
---

# vibe-anti-rationalization-check

Current models rarely skip work out of laziness. The failure that remains is subtler: satisfying the *check* instead of the *goal*. A test gets special-cased, an assertion loosened, a requirement quietly narrowed, and the summary says "done." This skill catches that and makes it visible.

## When to Use This Skill

- Before saying a task is complete, fixed, or passing
- A test is failing and the quickest route to green is changing the test
- You're about to narrow a requirement the user stated
- You're about to write "in the interest of time...", "for now...", or "simplified"
- You catch yourself explaining why something "doesn't really need" to be done

## When NOT to Use This Skill

- The user explicitly asked to skip or simplify something
- The test itself is genuinely wrong (fix it, but say so explicitly and explain why)
- You're genuinely unsure whether something is needed (ask the user instead)

## Reward-Hacking Patterns

| Pattern | What it looks like | Do instead |
|---------|-------------------|-----------|
| Test tampering | Loosening an assertion, adding a skip, deleting a failing case, raising a tolerance | Fix the code. If the test is wrong, change it and say why in the summary. |
| Special-casing | `if input == <test fixture>: return <expected>` or detecting the test environment | Implement the general behavior. |
| Hard-coded outputs | Returning the literal value a test expects | Compute it. |
| Mocking away the subject | Mocking the very function the test is supposed to exercise | Mock only external boundaries. |
| Silent scope cut | Implementing 4 of 5 requirements and summarizing as "done" | Finish, or list exactly what is missing. |
| Unverified claim | "This should fix it" / "Tests pass" without running them | Run the command and quote the result. |
| Error swallowing | `catch {}` / `except: pass` to stop a crash | Handle the specific error, or let it surface. |
| Deferred forever | "I'll add that later" with no tracked follow-up | Do it now, or create a tracked issue/TODO with a reference. |

## Steps

1. **Diff check** — Review your own diff for the patterns above. Pay particular attention to changes under test directories, in CI config, and in lint/skip annotations.
2. **Requirement check** — Re-read the original request. List every requirement and mark each one done or not done.
3. **Evidence check** — For each "works" or "passes" claim, is there command output from *this* session behind it?
4. **Resolve**:
   - A legitimate reason to deviate → ask the user, or state it prominently in the summary
   - A rationalization → do the work
5. **Disclose** — If anything was skipped, weakened, or changed in a test, say so plainly in the final summary. Never hide a shortcut.

## Output

When run as a self-check, report only if something was found. When invoked explicitly:

### Rationalization Check

| # | Pattern | Location | Resolution |
|---|---------|----------|-----------|
| 1 | Test tampering | `auth_test.go:88` tolerance 0.01 → 0.5 | Reverted; fixed rounding in `calc.go` |

**Requirements**: X/Y met — [list any not met]
**Unverified claims**: [none / list]
