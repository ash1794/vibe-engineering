---
name: vibe-coverage-enforcer
description: Enforce tiered test coverage standards — critical paths >=90%, business logic >=80%, general code >=70%. Use before claiming code is complete.
user-invocable: true
---

# vibe-coverage-enforcer

Coverage numbers don't guarantee quality, but low coverage guarantees surprise.

## When to Use This Skill

- Before claiming a feature is complete
- After writing tests, to verify coverage meets standards
- During periodic coverage health checks
- When deciding "do I need more tests?"

## When NOT to Use This Skill

- Prototype/spike code that will be rewritten
- Generated code (API clients, schema types)
- Configuration files
- When the user explicitly says coverage isn't a priority for this task

## Tiered Standards

Not all code needs the same coverage:

| Tier | Target | What's Included |
|------|--------|----------------|
| **Critical** | >=90% | Security, authentication, authorization, payment/billing, data integrity, encryption |
| **Business** | >=80% | Core business logic, API handlers, state management, validation |
| **General** | >=70% | Utilities, formatting, UI components, logging |
| **Exempt** | N/A | Generated code, test helpers, one-time scripts |

## Steps

1. **Run coverage** for the project:
   - Go: `go test -cover ./...` or `go test -coverprofile=coverage.out ./...`
   - JS/TS: `npm test -- --coverage`
   - Python: `pytest --cov`

2. **Classify packages/modules** into tiers

3. **Compare actual vs. target** for each package

4. **Report gaps**:

## Output Format

### Coverage Report

**Overall**: X% (target: varies by tier)

| Package/Module | Tier | Actual | Target | Status |
|---------------|------|--------|--------|--------|
| auth/ | Critical | 92% | 90% | ✓ |
| handlers/ | Business | 75% | 80% | ✗ (-5%) |
| utils/ | General | 68% | 70% | ✗ (-2%) |

### Action Required
1. `handlers/` needs +5% coverage — suggest testing: [specific untested functions]
2. `utils/` needs +2% coverage — suggest testing: [specific untested functions]

### Suggested Tests
```
[Specific test skeletons for uncovered code]
```
