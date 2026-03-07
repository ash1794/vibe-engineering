# vibe-engineering

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-blueviolet)](https://github.com/ash1794/vibe-engineering)
[![Skills](https://img.shields.io/badge/Skills-38-green)](https://github.com/ash1794/vibe-engineering)

**38 engineering discipline skills for Claude Code + a CLI for CI/CD enforcement.** Extracted from real-world multi-agent system development — not theoretical best practices, but patterns that survived 3 weeks of intensive production development with 205+ test files, 11 agents, and 50+ session observations.

> "Vibe coding" meets engineering rigor. Every skill here exists because skipping it caused real pain.

### One command. Instant engineering discipline.

```bash
claude plugin add github:ash1794/vibe-engineering
```

Claude automatically discovers and applies the right skill for every task — research before design, quality gates before shipping, structured debugging before guessing, test coverage before claiming "done."

## What is this?

A Claude Code plugin with 38 skills that enforce engineering discipline across any project, plus a lightweight CLI (`vibe-cli`) for CI/CD pipelines and automation:

- **Research & Decision-Making** (5 skills) — Think before building
- **Quality Gates & Validation** (7 skills) — Catch issues before they ship
- **Learning & Knowledge Management** (5 skills) — Never solve the same problem twice
- **Parallel & Multi-Agent Development** (4 skills) — Scale your work safely
- **Testing Patterns** (5 skills) — Test what matters, not just what's easy
- **Deployment & Operations** (4 skills) — Ship with confidence
- **Gap Analysis & Remediation** (2 skills) — Audit and systematically close gaps
- **Communication & Process** (4 skills) — Stay focused, stay clear
- **Meta Skills** (2 skills) — Skill discovery and routing

## Installation

### Option 1: Install from GitHub (recommended)

```bash
claude plugin add github:ash1794/vibe-engineering
```

That's it. All 38 skills are now available in every Claude Code session.

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

## CLI: `vibe-cli`

The `vibe-cli` CLI wraps critical skills into CI/CD-friendly commands with proper exit codes and JSON output. No dependencies — pure bash.

### Setup

```bash
# Make it available system-wide (optional)
ln -s $(pwd)/scripts/vibe-cli /usr/local/bin/vibe-cli

# Or run directly from the repo
./scripts/vibe-cli help
```

### Commands

```bash
vibe-cli pre-commit          # Scan staged changes for secrets, debug code, disabled tests
vibe-cli coverage            # Run test coverage and report against tier targets
vibe-cli spec-drift          # Detect spec-code drift from staged changes
vibe-cli decisions           # Extract decisions from staged diff
vibe-cli validate            # Validate skill files and manifests
vibe-cli hook install        # Install as git pre-commit hook
vibe-cli hook uninstall      # Remove git pre-commit hook
```

### Exit Codes

| Code | Meaning |
|------|---------|
| `0` | All checks passed |
| `1` | Blocking issues (CI should fail) |
| `2` | Warnings only (non-blocking) |

### JSON Output

Every command supports `--json` for machine-readable output:

```bash
vibe-cli pre-commit --json
# {"status":"fail","blockers":1,"warnings":3,"findings":[...]}

vibe-cli coverage --json --spec docs/spec.md
# {"status":"pass","tool":"pytest","line_coverage":85,"spec_to_test":{"total":12,"covered":8}}

vibe-cli spec-drift --json --spec docs/spec.md
# {"status":"drift_detected","drift_items":3,"spec":"docs/spec.md","items":[...]}

vibe-cli decisions --json
# {"status":"decisions_found","count":4,"files_changed":7,"decisions":[...]}
```

### CI/CD Integration

**GitHub Actions:**
```yaml
- name: Vibe pre-commit check
  run: ./scripts/vibe-cli pre-commit --json

- name: Coverage check
  run: ./scripts/vibe-cli coverage --spec docs/spec.md
```

**GitLab CI:**
```yaml
vibe-checks:
  script:
    - ./scripts/vibe-cli pre-commit
    - ./scripts/vibe-cli coverage --spec docs/spec.md
```

**Pre-commit hook (automatic):**
```bash
# Install once — blocks commits with secrets, debug code, etc.
./scripts/vibe-cli hook install
```

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `VIBE_OUTPUT=json` | Same as `--json` |
| `VIBE_SPEC=<path>` | Default spec path for spec-drift/coverage |
| `VIBE_TEST_DIR=<path>` | Default test directory |
| `NO_COLOR=1` | Disable colored output |

## The Spec-Code-Test Loop

Four skills form a connected workflow that keeps spec, tests, and code in sync:

```
Code changes
    ↓
vibe-decision-journal ──→ Extract decisions from diffs
    ↓
vibe-spec-sync ──→ Update spec to reflect approved decisions
    ↓
vibe-adversarial-test-generation ──→ Generate spec-driven tests with req:ID traceability
    ↓
vibe-coverage-enforcer ──→ Verify 3 dimensions (line + spec-to-test + spec-to-code)
    ↓
vibe-spec-vs-code-audit ──→ Final verification: no remaining gaps
```

The CLI exposes the critical parts for automation:
- `vibe decisions` → extract decisions from staged changes
- `vibe spec-drift` → detect spec-code drift
- `vibe coverage` → verify all coverage dimensions
- `vibe pre-commit` → block commits with secrets/debug code

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
| `vibe-decision-journal` | After any architectural choice or before committing | Automatic decision extraction from diffs + manual ADR recording |
| `vibe-devil-advocate-review` | Before shipping recommendations | 5-dimension adversarial challenge |
| `vibe-start-informed` | Before proposing any feature/architecture | Research real projects and failures before designing |
| `vibe-anti-rationalization-check` | When about to skip a step | Catches shortcut rationalization patterns |

### Quality Gates & Validation
| Skill | Trigger | Purpose |
|-------|---------|---------|
| `vibe-acceptance-gate` | After completing a task with criteria | PASS/FAIL validation against criteria |
| `vibe-quality-loop` | After any non-trivial implementation | Implement→Review→Test→Fix→Loop cycle |
| `vibe-spec-vs-code-audit` | When implementation claimed complete | Line-by-line spec compliance check |
| `vibe-spec-sync` | Before committing or after approving decisions | Bidirectional spec-code sync with drift detection |
| `vibe-doc-quality-gate` | After editing any technical doc | Fast 6-point document quality check |
| `vibe-requirements-validator` | When reviewing PRD/user stories | SMART criteria validation |
| `vibe-coverage-enforcer` | Before claiming code complete | 3-dimension coverage: line + spec-to-test + spec-to-code |

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
| `vibe-adversarial-test-generation` | After happy-path tests written | Edge case + spec-driven test generation with req:ID traceability |
| `vibe-fuzz-parser-inputs` | Implementing any parser | Fuzz test scaffolding and corpus |

### Deployment & Operations
| Skill | Trigger | Purpose |
|-------|---------|---------|
| `vibe-safe-deploy` | Before any deployment | Pre-flight checks, atomic deploy, rollback |
| `vibe-pre-commit-audit` | Before creating a commit | Secrets, TODOs, debug statements scan |
| `vibe-service-health-dashboard` | Checking running services | Multi-service health monitoring |
| `vibe-rollback-plan` | Before risky changes | Documented rollback runbook |

### Gap Analysis & Remediation
| Skill | Trigger | Purpose |
|-------|---------|---------|
| `vibe-gap-analysis` | Before production launch or after major refactor | 17-dimension production readiness audit with parallel agents |
| `vibe-gap-closure-loop` | After gap analysis with 10+ findings | Autonomous loop: dependency analysis → parallel fix agents → test gate → repeat |

### Communication & Process
| Skill | Trigger | Purpose |
|-------|---------|---------|
| `vibe-structured-output` | Producing analysis or reports | Enforced Executive Summary format |
| `vibe-iteration-review` | End of development iteration | Quality grading and trend analysis |
| `vibe-scope-guard` | During implementation | Scope creep detection and redirection |
| `vibe-production-mindset` | Starting any implementation | "1 million users" quality check |

## Why vibe-engineering?

Without discipline skills, AI coding assistants make the same mistakes humans do — skip research, ship without tests, rationalize shortcuts, lose context across sessions. **vibe-engineering catches these patterns automatically.**

| Without | With vibe-engineering |
|---------|----------------------|
| "Let me just build it" | Research existing solutions first (`vibe-research-before-design`) |
| "Tests pass, ship it" | Check coverage standards are met (`vibe-coverage-enforcer`) |
| "I'll remember the decision" | Extract it automatically from diffs (`vibe-decision-journal`) |
| "Good enough" | Loop until clean (`vibe-quality-loop`) |
| "Spec is probably still accurate" | Detect drift and sync back (`vibe-spec-sync`) |
| "This is simple, no need for..." | Catch rationalization in real-time (`vibe-anti-rationalization-check`) |
| Debug by guessing | Systematic root cause analysis (`vibe-debugging-journal`) |
| Context lost between sessions | Auto-generated handover docs (`vibe-handover-doc`) |

## Design Principles

1. **Born from pain, not theory** — Every skill exists because skipping it caused real problems
2. **When to use AND when NOT to use** — Every skill has explicit triggers and anti-triggers
3. **Composable** — Skills work independently or together
4. **Advisory first, enforcement when it matters** — Skills guide; CLI enforces in CI/CD
5. **Cross-project** — No project-specific assumptions. Works with any language/framework

## How It Works

This is a standard Claude Code plugin. The `.claude-plugin/plugin.json` manifest registers it, and the `skills/` directory contains 38 skill definitions that Claude auto-discovers based on task context.

```
vibe-engineering/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── skills/                  # 38 skill definitions
│   ├── vibe-help/SKILL.md
│   ├── quality-loop/SKILL.md
│   ├── spec-sync/SKILL.md
│   ├── decision-journal/SKILL.md
│   ├── gap-analysis/SKILL.md
│   └── ... (33 more)
├── scripts/
│   ├── vibe-cli           # CLI for CI/CD enforcement
│   └── validate-skills.sh # Skill file validator
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
description: Performs [action] for [context]. Use when [trigger condition].
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

These skills were extracted from building [nosaintsville-agent](https://github.com/ash1794/nosaintsville-agent) — an 11-agent personal assistant system with Go backend, React Native frontend, and 205+ test files.

**The numbers:**
- 50+ session observations analyzed (310k+ tokens of development history)
- 15 project-specific skills generalized into 38 universal patterns
- 3 weeks of intensive multi-agent development
- Every skill represents a pattern that emerged from real pain — not a theoretical best practice document

## Related Projects

- [nosaintsville-agent](https://github.com/ash1794/nosaintsville-agent) — The 11-agent personal assistant system where these skills were born

## License

MIT — Use it, fork it, make it yours.
