---
name: vibe-help
description: Routes to the right vibe-engineering skill for the current task and lists the full catalog. Use when the user asks which skill to use, asks what vibe-engineering can do, or is unsure how to approach a task.
user-invocable: true
---

# vibe-help

The vibe-engineering skill router. Skills are normally picked automatically from their descriptions; this skill is for when the user wants to browse, or isn't sure which one fits.

## When to Use This Skill

- User asks "what skill should I use?", "help", or "what can vibe-engineering do?"
- User is starting an unfamiliar type of task and wants a recommended workflow
- You are unsure which of two similar skills applies

## When NOT to Use This Skill

- A specific skill was already invoked, or obviously applies
- In the middle of executing another skill's workflow
- Trivially simple tasks (e.g., "fix this typo")

## How to Route

Ask what the user is trying to do (unless it's already clear), then recommend **one** starting skill and at most two follow-ups. Don't recite the whole catalog unless asked.

### "I'm about to build something new"
→ Before: `vibe-research-before-design`, then `vibe-requirements-validator` if there's a PRD
→ During: `vibe-scope-guard`, `vibe-production-mindset` (production code)
→ After: `vibe-quality-loop`, `vibe-acceptance-gate`

### "I need to fix bugs / issues"
→ 1–5 bugs: fix directly, then `vibe-reflect-and-compound` for any non-trivial one
→ 10+ bugs or findings: `vibe-gap-closure-loop`
→ Prevent recurrence: `vibe-adversarial-test-generation`

### "I'm reviewing code, a design, or docs"
→ Design or large change: `vibe-devil-advocate-review`
→ Spec compliance: `vibe-spec-sync --audit`
→ Docs: `vibe-doc-quality-gate` · Requirements: `vibe-requirements-validator`

### "I need to test something"
→ Planning: `vibe-scenario-matrix` · Coverage: `vibe-coverage-enforcer`
→ Edge cases: `vibe-adversarial-test-generation` · Parsers: `vibe-fuzz-parser-inputs`
→ Snapshots: `vibe-golden-file-testing` · Concurrency: `vibe-concurrent-test-safety`

### "I'm committing, deploying, or shipping"
→ Commit: `vibe-pre-commit-audit`, `vibe-spec-sync`
→ Deploy: `vibe-safe-deploy` · Risky change: `vibe-rollback-plan`
→ Running services: `vibe-service-health-dashboard`

### "I have a lot of parallel work"
→ Plan: `vibe-parallel-task-decomposition` → Integrate: `vibe-cherry-pick-integration`

### "Is this production-ready?"
→ Audit: `vibe-gap-analysis` → Close gaps: `vibe-gap-closure-loop`

### "I need to make or record a decision"
→ Research: `vibe-research-before-design` → Record: `vibe-decision-journal` → Challenge: `vibe-devil-advocate-review`

### "I want to capture what just happened"
→ Learnings, bugs, patterns: `vibe-reflect-and-compound`
→ Handing off to a person or another tool: `vibe-handover-doc`
→ End of sprint: `vibe-iteration-review`

### "Am I actually done?"
→ `vibe-acceptance-gate`, then `vibe-anti-rationalization-check`

## Full Catalog

| Area | Skills |
|------|--------|
| Research & decisions | `vibe-research-before-design`, `vibe-decision-journal`, `vibe-devil-advocate-review` |
| Quality gates | `vibe-acceptance-gate`, `vibe-quality-loop`, `vibe-anti-rationalization-check`, `vibe-spec-sync`, `vibe-doc-quality-gate`, `vibe-requirements-validator`, `vibe-coverage-enforcer` |
| Knowledge & continuity | `vibe-reflect-and-compound`, `vibe-handover-doc` |
| Parallel work | `vibe-parallel-task-decomposition`, `vibe-cherry-pick-integration` |
| Testing | `vibe-scenario-matrix`, `vibe-adversarial-test-generation`, `vibe-fuzz-parser-inputs`, `vibe-golden-file-testing`, `vibe-concurrent-test-safety` |
| Deployment & ops | `vibe-pre-commit-audit`, `vibe-safe-deploy`, `vibe-rollback-plan`, `vibe-service-health-dashboard` |
| Gap analysis | `vibe-gap-analysis`, `vibe-gap-closure-loop` |
| Process | `vibe-scope-guard`, `vibe-production-mindset`, `vibe-iteration-review` |
| Meta | `vibe-help` |

## Invocation

- **Claude Code**: `/vibe-engineering:<skill-name>` (plugin install) or `/<skill-name>`
- **OpenAI Codex**: `$<skill-name>`
- **Gemini CLI**: activated automatically from the description; `/skills` lists what's installed

## Output Format

**Recommended**: `vibe-[skill]` — [one line on why it fits]
**Then**: `vibe-[skill]`, `vibe-[skill]` (optional follow-ups)
