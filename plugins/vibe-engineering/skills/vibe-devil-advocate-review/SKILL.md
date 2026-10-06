---
name: vibe-devil-advocate-review
description: Challenges a recommendation, design, large change, or any artifact submitted for hard review (spec, proposal, policy, plan) across 5 dimensions (consistency, completeness, actionability, alignment, risk), from the standards of a named senior expert in the artifact's domain and ideally from a fresh context or a different model. Searches assuming defects exist and reports only those that survive evidence. Panel mode runs several independent lenses in parallel on a release candidate, verifies every finding against the current head, and routes confirmed ones to file owners. Use before shipping a significant recommendation, design, large branch, or multi-agent release, or when asked to tear something apart, be brutally honest, or poke holes in it.
user-invocable: true
---

# vibe-devil-advocate-review

Before shipping a recommendation, challenge it. Models still tend to agree with their own earlier reasoning and with the user, and to read a capable-looking artifact as good. A reviewer that shares the author's context inherits the author's blind spots, so the review is strongest when the reviewer doesn't share them.

Two rules govern the whole review. **Search like a pessimist**: assume defects exist, and treat finding none as a sign the search wasn't hard enough yet. **Report like a scientist**: say only what survives as a real, evidenced defect. The first rule sets how hard you look; the second sets what you say. A manufactured finding is as damaging as flattery, because it teaches the author to discount the next real one.

## When to Use This Skill

- Before sending a design document for approval
- Before shipping a recommendation that combines multiple inputs
- Before merging a large feature branch
- When you feel "too confident" about a solution
- User asks for a review, a second opinion, or a brutally honest critique ("tear this apart", "poke holes in this", "what's wrong with this")
- Reviewing a non-code artifact for hard critique: a proposal, policy, plan, curriculum, or argument
- Reviewing your own draft before it ships

## When NOT to Use This Skill

- Trivial changes (typo fixes, formatting)
- When the user explicitly says "just ship it"
- During brainstorming (don't kill ideas before they form)
- Small code changes (use `vibe-quality-loop`)
- The user wants friendly proofreading or reassurance, not critique
- Prose that reads as machine-written but is otherwise sound (use `vibe-slop-filter`)

## Get an Independent Reviewer

In order of preference:
1. **A different model family** — for example, have Codex (GPT) review Claude's work, or Claude review Gemini's. Different training produces different blind spots.
2. **A fresh subagent** that gets only the artifact and the stated goals, not the conversation that produced them.
3. **Self-review** as a last resort. Explicitly assume the artifact is wrong and look for the evidence.

Give the reviewer the artifact, the goals and constraints, the expert lens below, and this skill's 5 dimensions. Don't give it your own assessment.

## Peg the Reviewer to an Expert

Skepticism without domain standards is contrarianism. Before writing a critical word, name the senior expert whose standards govern this artifact, and review from inside that person's judgment:

- **Code or architecture**: a principal engineer who has maintained systems at scale and is unimpressed by code that works in the demo and fails in six months.
- **Design**: a design lead who looks for the unspecified state, the edge case nobody drew, the accessibility gap.
- **Spec or requirements**: the engineer who will have to build from it and test against it.
- **Policy or process**: an institutional veteran who knows which clauses survive contact with real people and which become dead letters.
- **Proposal or argument**: a referee in the field who spots the unsourced claim and the conclusion the evidence doesn't support.
- **Curriculum or training**: a senior educator who sees missing scaffolding and assessments that don't measure the stated outcome.

If the artifact spans domains, name two or three lenses. If the right expert is genuinely unclear, ask one question first; reviewing from the wrong standard wastes the pass.

The expertise sits in the reviewer's chair; the charity is withheld from the author. Hold the work to the standard of the best in its field and treat every shortfall as a real defect, but don't invent errors or strawman it. Steelman what's there, then break it where it actually breaks.

## The 5 Dimensions

1. **Consistency** — Do all parts agree with each other? Any contradictions?
2. **Completeness** — What's missing? Unaddressed edge cases? Blind spots? Is it 30% finished presenting as done?
3. **Actionability** — Is every recommendation concrete and measurable? Could someone actually do it?
4. **Alignment** — Does it match the stated goals, constraints, and user needs?
5. **Risk** — What could go wrong? Second-order effects? Blast radius of failure?

## Steps

1. **Read the whole artifact before critiquing.** Don't skim, and don't react to the first half. Many of the sharpest findings are cross-document: an objective in section 1 that the test plan in section 6 never measures, a claim made early and contradicted late.
2. **For each dimension**, actively look for problems. Assume there are some.
3. **Order by what kills the artifact fastest**: structural integrity first, then whether the central idea holds, then the domain-specific failures only the expert would catch, and cosmetic issues last. Typos matter mostly as tells about rigor elsewhere.
4. **Ask what the artifact actually is.** Is it what it presents itself as? A research spike dressed as a deployment plan, a decision the author was meant to make quietly resolved by the template, another organization's voice on a problem that isn't theirs. This read often changes which findings matter.
5. **Verify each issue** — Keep only issues you can support with evidence (a quote, `file:line`, or a concrete failure scenario). "The design is weak" is not a finding; "Section 3 names the retry budget as the goal but nothing defines how it's measured" is. Drop what you can't support.
6. **Name genuine strengths in one line each.** Never manufacture a compliment, and don't dwell. If much of it is good, the review can be short.
7. **Score** each dimension 1–5 (1 = critical issues, 5 = solid)
8. **Verdict**: APPROVE / REVISE (with required changes) / REJECT (with blocking issues)

### Gate the Review Before Sending

Run your own review through the same standard:
- Did I find each issue, or need something to say? Strike anything that wouldn't survive the author asking "is that actually a problem?"
- Is every issue located and evidenced?
- Did I review from a real expert standard, or just lean negative?
- Did I read the whole artifact?
- If the work is good, did I say so plainly?

Three real defects and two named strengths beat ten findings, six of which are noise.

### Delivery

- Lead with the hardest finding. No "great work, but".
- End when the findings end. No reassuring close.
- If the user will add their own reflections afterwards, deliver the full review, then hand back explicitly and respond to what they add rather than repeating yourself.
- Match depth to stakes: a document going to leadership gets a deeper read than a quick gut check.

## Panel Mode (release candidates built by several agents)

One reviewer carries one set of blind spots, and unverified findings waste fix cycles. For a release or content lock:
1. **Freeze a head.** Every lens reviews the same commit.
2. **Run lenses in parallel**, each with a narrow brief and a bounded report format (`file:line`, severity). Pick lenses that fit the product, for example: editorial and tone, facts and privacy, UX and accessibility, engineering and performance.
3. **Verify separately.** A distinct stage reproduces each finding on the current head and drops stale or false ones (already fixed, or a rule firing on text that already complies).
4. **Dedupe and rank** P0–P2 across lenses.
5. **Route** each confirmed finding to the owner of the file (`vibe-workstream-orchestration`), then re-run only the affected lenses.

If the harness supports scripted workflows, run the panel as one: it verifies more rigorously than routing findings by hand.

## Output Format

### Devil's Advocate Review
**Reviewer**: [different model / fresh subagent / self]
**Expert lens**: [e.g. principal engineer, maintains payment systems at scale]

| Dimension | Score | Issues |
|-----------|-------|--------|
| Consistency | X/5 | [count] |
| Completeness | X/5 | [count] |
| Actionability | X/5 | [count] |
| Alignment | X/5 | [count] |
| Risk | X/5 | [count] |

### Critical Issues
1. [issue, location, evidence, concrete failure scenario]

### Warnings
1. [non-blocking concern, with location]

### What Holds Up
- [one line per genuine strength; omit the section if there are none]

### Verdict: APPROVE / REVISE / REJECT
[rationale]
