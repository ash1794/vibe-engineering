---
name: vibe-research-before-design
description: Researches real projects, papers, and documented failures before proposing a new feature, architecture, or technology choice. Use for design decisions with multiple valid approaches, not for implementing an existing spec or fixing a known bug.
user-invocable: true
---

# vibe-research-before-design

Other people's documented failures count as observed failure. Before proposing a design, find out how others solved the same problem and where it broke for them.

## When to Use This Skill

- Designing a new feature, subsystem, or architecture
- Choosing between technologies, frameworks, or patterns
- Making a decision with long-term consequences that is expensive to reverse
- The user asks "how should we build X?"
- You're about to say "I recommend..." for a design choice

## When NOT to Use This Skill

- Implementing an already-designed spec (the research was done at design time)
- Fixing a bug with a known approach
- Routine or mechanical changes with one obvious correct solution
- The user has already chosen the technology and wants implementation
- The decision was already researched and recorded (check `vibe-decision-journal` first)

## Steps

1. **Frame the question** — What exactly is being decided? What are the hard constraints (scale, latency, cost, team skills, existing stack)?

2. **Decompose** into sub-problems that can be researched independently.

3. **Research each sub-problem** using whatever web search or research tool the harness provides. Run sub-problems in parallel (subagents) when the harness supports it. For each, find:

   | Requirement | Minimum |
   |-------------|---------|
   | Real projects or production systems | 2+, with a link |
   | Paper, post-mortem, or engineering write-up | 1+, with a link and year |
   | Mechanism | How it actually works, not marketing copy |
   | Known failures | What went wrong for others, and under what conditions |
   | Fit | How it maps to *our* constraints, specifically |

4. **Verify before citing** — Every source must be something you actually opened in this session. Don't quote adoption numbers (stars, downloads, users) from memory; either read them from the source or leave them out. If search is unavailable, say so and label the output "from prior knowledge, unverified."

5. **Synthesize** — Compare the options side by side, with the imported failures up front.

6. **Recommend** — Base the recommendation on the evidence and state your confidence. Name the condition that would change your mind.

7. **Record** — Log the decision and the rejected alternatives with `vibe-decision-journal`.

## Red Flags

| Thought | Reality |
|---------|---------|
| "I already know the best approach" | You know one approach. Research finds the others. |
| "This is too niche for research" | If someone built it, someone documented where it failed. |
| "Research will slow us down" | A rewrite is slower. |
| "Everyone uses X" | Popularity is not fitness for your constraints. |
| "I'll cite what I remember" | Unverified citations are the most common way research output goes wrong. |

## Output Format

### Research Summary
- **Decision**: [what we're deciding]
- **Constraints**: [key constraints]
- **Options evaluated**: X

### Comparison
| Criteria | Option A | Option B | Option C |
|----------|----------|----------|----------|
| Mechanism | | | |
| Known failures | | | |
| Fit with constraints | | | |

### Recommendation
[Evidence-based recommendation, confidence level, and what would change it]

### Sources
[Links actually opened, one line each on what they showed]
