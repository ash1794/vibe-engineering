---
name: vibe-adversarial-test-generation
description: Generate edge case and failure mode test cases after happy-path tests are written. Covers boundary values, nil inputs, concurrency, resource exhaustion, and malformed data.
user-invocable: true
---

# vibe-adversarial-test-generation

Happy-path tests prove your code works. Adversarial tests prove it doesn't break.

## When to Use This Skill

- After writing happy-path tests for a feature
- Before claiming test coverage is complete
- When preparing for a security review
- When "it works on my machine" needs to become "it works everywhere"

## When NOT to Use This Skill

- Before happy-path tests exist (write those first)
- For throwaway/prototype code
- When the function is trivially simple (e.g., getters/setters)

## Adversarial Categories

### 1. Boundary Values
- Zero, one, max, max+1 for all numeric inputs
- Empty string, single char, max-length string
- Empty array, single element, very large array
- Exactly at threshold values

### 2. Nil/Null/Undefined
- nil pointer as receiver
- nil arguments to every parameter
- nil nested fields in structs
- Returning nil where non-nil expected

### 3. Type Edge Cases
- Unicode: emoji, RTL text, zero-width chars, combining chars
- Strings: newlines, tabs, null bytes, control characters
- Numbers: NaN, Infinity, -0, very large, very small
- Dates: leap year, DST transitions, timezone boundaries, epoch

### 4. Concurrency
- Two goroutines calling the same function
- Read during write
- Close during use
- Cancel during operation

### 5. Resource Exhaustion
- Very large inputs (10MB string, 1M element slice)
- Disk full simulation
- Network timeout simulation
- Memory pressure

### 6. Malformed Input
- Invalid JSON/YAML/XML
- Truncated input (cut off mid-field)
- Wrong types (string where int expected)
- Extra fields, missing required fields
- SQL injection patterns, XSS payloads (for external inputs)

## Steps

1. **Read the function under test** -- understand inputs, outputs, side effects
2. **For each input parameter**, generate adversarial values from each category
3. **For each adversarial input**, determine expected behavior:
   - Should it return an error? (most common)
   - Should it handle gracefully? (fallback behavior)
   - Should it panic? (almost never the right answer)
4. **Write the tests** as table-driven test cases
5. **Run them** and fix any unexpected panics or wrong error handling

## Output Format

### Adversarial Tests: [Function Name]

**Tests Generated**: X
**Categories Covered**: Y/6

| # | Category | Input | Expected | Actual |
|---|----------|-------|----------|--------|
| 1 | Nil input | nil | ErrNilInput | PASS |
| 2 | Empty string | "" | ErrEmpty | PANIC! |

### Issues Found
1. [Function] panics on nil input (should return error)
