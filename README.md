# vibe-engineering

A Claude Code plugin with 34 engineering discipline skills. Extracted from real-world multi-agent system development — not theoretical best practices, but patterns that survived 3 weeks of intensive production development.

> "Vibe coding" meets engineering rigor. Every skill here exists because skipping it caused real pain.

## What is this?

A Claude Code plugin with 34 skills that enforce engineering discipline across any project:

- **Research & Decision-Making** (4 skills) — Think before building
- **Quality Gates & Validation** (6 skills) — Catch issues before they ship
- **Learning & Knowledge Management** (5 skills) — Never solve the same problem twice
- **Parallel & Multi-Agent Development** (4 skills) — Scale your work safely
- **Testing Patterns** (5 skills) — Test what matters, not just what's easy
- **Deployment & Operations** (4 skills) — Ship with confidence
- **Communication & Process** (4 skills) — Stay focused, stay clear
- **Meta Skills** (2 skills) — Skill discovery and routing

## Installation

### Option 1: Install from GitHub (recommended)

```bash
claude plugin add github:ash1794/vibe-engineering
```

That's it. All 34 skills are now available in every Claude Code session.

### Option 2: Development / local testing

```bash
git clone https://github.com/ash1794/vibe-engineering.git
claude --plugin-dir ./vibe-engineering
```

### Option 3: Add as a marketplace source

If you want automatic updates when new skills are added:

```bash
# Add as a marketplace
claude plugin marketplace add ash1794/vibe-engineering

# Then install
claude plugin install vibe-engineering
```

## Quick Start

After installation, Claude automatically discovers vibe-engineering skills. The bootstrap skill teaches Claude to check for applicable skills before every action.

Explore available skills interactively:
```
/vibe-engineering:vibe-help
```

Invoke any skill directly:
```
/vibe-engineering:vibe-quality-loop
/vibe-engineering:vibe-research-before-design
/vibe-engineering:vibe-reflect-and-compound
```

## Skill Catalog

### Meta Skills
| Skill | Trigger | Purpose |
|-------|---------|---------|
| `vibe-using-vibe-engineering` | Every conversation start | Bootstrap: teaches Claude to check for applicable skills |
| `vibe-help` | "What skill should I use?" | Interactive skill router and discovery |

### Research & Decision-Making
| Skill | Trigger | Purpose |
|-------|---------|---------|
| `vibe-research-before-design` | Before any new feature/architecture | SOTA research before design proposals |
| `vibe-decision-journal` | After any architectural choice | ADR-style persistent decision logging |
| `vibe-devil-advocate-review` | Before shipping recommendations | 5-dimension adversarial challenge |
| `vibe-anti-rationalization-check` | When about to skip a step | Catches shortcut rationalization patterns |

### Quality Gates & Validation
| Skill | Trigger | Purpose |
|-------|---------|---------|
| `vibe-acceptance-gate` | After completing a task with criteria | PASS/FAIL validation against criteria |
| `vibe-quality-loop` | After any non-trivial implementation | Implement→Review→Test→Fix→Loop cycle |
| `vibe-spec-vs-code-audit` | When implementation claimed complete | Line-by-line spec compliance check |
| `vibe-doc-quality-gate` | After editing any technical doc | Fast 6-point document quality check |
| `vibe-requirements-validator` | When reviewing PRD/user stories | SMART criteria validation |
| `vibe-coverage-enforcer` | Before claiming code complete | Tiered coverage standard enforcement |

### Learning & Knowledge Management
| Skill | Trigger | Purpose |
|-------|---------|---------|
| `vibe-reflect-and-compound` | After feedback or failed attempts | Extract patterns, update learnings |
| `vibe-handover-doc` | End of long session | Generate session continuity document |
| `vibe-debugging-journal` | After resolving non-trivial bugs | Persistent bug pattern recording |
| `vibe-session-context-flush` | Context window approaching capacity | Smart context summarization |
| `vibe-pattern-library` | Same pattern implemented 3rd time | Record and suggest established patterns |

### Parallel & Multi-Agent Development
| Skill | Trigger | Purpose |
|-------|---------|---------|
| `vibe-parallel-task-decomposition` | Large task with independent subtasks | DAG analysis for safe parallelism |
| `vibe-cherry-pick-integration` | After parallel agents complete | Safe sequential integration |
| `vibe-wave-based-remediation` | 10+ issues to fix | Prioritized batch remediation |
| `vibe-async-task-queue` | Identifying non-blocking work | Cross-session persistent task queue |

### Testing Patterns
| Skill | Trigger | Purpose |
|-------|---------|---------|
| `vibe-golden-file-testing` | Snapshot/golden test implementation | Temporal normalization, update commands |
| `vibe-scenario-matrix` | Planning test coverage | Behavioral scenario acceptance matrix |
| `vibe-concurrent-test-safety` | Tests with shared mutable state | Race condition and cleanup auditing |
| `vibe-adversarial-test-generation` | After happy-path tests written | Edge case and failure mode generation |
| `vibe-fuzz-parser-inputs` | Implementing any parser | Fuzz test scaffolding and corpus |

### Deployment & Operations
| Skill | Trigger | Purpose |
|-------|---------|---------|
| `vibe-safe-deploy` | Before any deployment | Pre-flight checks, atomic deploy, rollback |
| `vibe-pre-commit-audit` | Before creating a commit | Secrets, TODOs, debug statements scan |
| `vibe-service-health-dashboard` | Checking running services | Multi-service health monitoring |
| `vibe-rollback-plan` | Before risky changes | Documented rollback runbook |

### Communication & Process
| Skill | Trigger | Purpose |
|-------|---------|---------|
| `vibe-structured-output` | Producing analysis or reports | Enforced Executive Summary format |
| `vibe-iteration-review` | End of development iteration | Quality grading and trend analysis |
| `vibe-scope-guard` | During implementation | Scope creep detection and redirection |
| `vibe-production-mindset` | Starting any implementation | "1 million users" quality check |

## Design Principles

1. **Born from pain, not theory** — Every skill exists because skipping it caused real problems
2. **When to use AND when NOT to use** — Every skill has explicit triggers and anti-triggers
3. **Composable** — Skills work independently or together
4. **Non-invasive** — Skills guide, they don't block. WARN, don't FAIL (unless critical)
5. **Cross-project** — No project-specific assumptions. Works with any language/framework

## How It Works

This is a standard Claude Code plugin. The `.claude-plugin/plugin.json` manifest registers it, and the `skills/` directory contains 34 skill definitions that Claude auto-discovers based on task context.

```
vibe-engineering/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── skills/                  # 34 skill definitions
│   ├── vibe-help/SKILL.md
│   ├── quality-loop/SKILL.md
│   ├── research-before-design/SKILL.md
│   └── ... (31 more)
└── README.md
```

Each skill has:
- **YAML frontmatter** with name, description, and invocation config
- **When to Use** — explicit triggers
- **When NOT to Use** — anti-triggers to prevent misapplication
- **Steps** — the actual workflow
- **Output Format** — structured output template

## Contributing

Found a pattern that keeps saving you? Turn it into a skill:

1. Fork this repo
2. Create `skills/your-skill-name/SKILL.md`
3. Follow the template (see any existing skill)
4. Include: When to Use, When NOT to Use, Steps, Output Format
5. Submit a PR

### Skill Template

```markdown
---
name: vibe-your-skill-name
description: One-line description of what this skill does and when to use it.
user-invocable: true
---

# vibe-your-skill-name

[One paragraph explaining the problem this skill solves]

## When to Use This Skill
- [Trigger 1]
- [Trigger 2]

## When NOT to Use This Skill
- [Anti-trigger 1]
- [Anti-trigger 2]

## Steps
1. [Step 1]
2. [Step 2]

## Output Format
[Template for structured output]
```

## Origin Story

These skills were extracted from building [nosaintsville-agent](https://github.com/ash1794/nosaintsville-agent) — an 11-agent personal assistant system with Go backend, React Native frontend, and 205+ test files. Every skill represents a pattern that emerged from real development pain, not a theoretical best practice document.

The extraction process analyzed 50+ session observations (310k+ tokens of development history), 15 project-specific skills, and 3 weeks of intensive development to identify 34 patterns that are genuinely generic and reusable across any project.

## License

MIT
