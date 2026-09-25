---
name: vibe-devil-advocate-review
description: Challenges a recommendation, design, or large change across 5 dimensions (consistency, completeness, actionability, alignment, risk), ideally from a fresh context or a different model. Use before shipping a significant recommendation, design document, or large feature branch.
user-invocable: true
---

# vibe-devil-advocate-review

Before shipping a recommendation, challenge it. Models still tend to agree with their own earlier reasoning and with the user. A reviewer that shares the author's context inherits the author's blind spots, so the review is strongest when the reviewer doesn't share them.

## When to Use This Skill

- Before sending a design document for approval
- Before shipping a recommendation that combines multiple inputs
- Before merging a large feature branch
- When you feel "too confident" about a solution
- User asks for a review or second opinion

## When NOT to Use This Skill

- Trivial changes (typo fixes, formatting)
- When the user explicitly says "just ship it"
- During brainstorming (don't kill ideas before they form)
- Small code changes (use `vibe-quality-loop`)

## Get an Independent Reviewer

In order of preference:
1. **A different model family** — for example, have Codex (GPT) review Claude's work, or Claude review Gemini's. Different training produces different blind spots.
2. **A fresh subagent** that gets only the artifact and the stated goals, not the conversation that produced them.
3. **Self-review** as a last resort. Explicitly assume the artifact is wrong and look for the evidence.

Give the reviewer the artifact, the goals and constraints, and this skill's 5 dimensions. Don't give it your own assessment.

## The 5 Dimensions

1. **Consistency** — Do all parts agree with each other? Any contradictions?
2. **Completeness** — What's missing? Unaddressed edge cases? Blind spots?
3. **Actionability** — Is every recommendation concrete and measurable? Could someone actually do it?
4. **Alignment** — Does it match the stated goals, constraints, and user needs?
5. **Risk** — What could go wrong? Second-order effects? Blast radius of failure?

## Steps

1. **Read the artifact** in full. Don't skim.
2. **For each dimension**, actively look for problems. Assume there are some.
3. **Verify each issue** — Keep only issues you can support with evidence (a quote, `file:line`, or a concrete failure scenario). Drop the ones you can't. Padding the list with speculative issues is as unhelpful as rubber-stamping.
4. **Score** each dimension 1–5 (1 = critical issues, 5 = solid)
5. **Verdict**: APPROVE / REVISE (with required changes) / REJECT (with blocking issues)

## Output Format

### Devil's Advocate Review
**Reviewer**: [different model / fresh subagent / self]

| Dimension | Score | Issues |
|-----------|-------|--------|
| Consistency | X/5 | [count] |
| Completeness | X/5 | [count] |
| Actionability | X/5 | [count] |
| Alignment | X/5 | [count] |
| Risk | X/5 | [count] |

### Critical Issues
1. [issue, evidence, concrete failure scenario]

### Warnings
1. [non-blocking concern]

### Verdict: APPROVE / REVISE / REJECT
[rationale]
