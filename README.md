

# vibe-engineering

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-blueviolet)](https://github.com/ash1794/vibe-engineering)
[![OpenAI Codex Skills](https://img.shields.io/badge/OpenAI%20Codex-Skills-10a37f)](https://developers.openai.com/codex/skills/)
[![Gemini CLI Skills](https://img.shields.io/badge/Gemini%20CLI-Skills-4285F4)](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/skills.md)
[![Skills](https://img.shields.io/badge/Skills-29-green)](https://github.com/ash1794/vibe-engineering)

**29 engineering discipline skills for Claude Code, OpenAI Codex & Gemini CLI + a CLI for CI/CD enforcement.** Extracted from real-world multi-agent system development: not theoretical best practices, but patterns that survived 3 weeks of intensive production development with 205+ test files, 11 agents, and 50+ session observations.

> "Vibe coding" meets engineering rigor. Every skill here exists because skipping it caused real pain, and every skill was re-checked in v2.0 against what current models and agent harnesses now handle on their own.

### Two commands. Instant engineering discipline.

```bash
/plugin marketplace add ash1794/vibe-engineering
/plugin install vibe-engineering@vibe-plugins
```

Your agent picks the right skill from its description: research before design, quality gates before shipping, evidence before claiming "done."

## What is this?

A skill collection in the open [Agent Skills](https://agentskills.io) format with 29 skills that enforce engineering discipline across any project, plus a lightweight CLI (`vibe-cli`) for CI/CD pipelines and automation:

- **Research & Decision-Making** (3 skills): think before building
- **Quality Gates & Validation** (7 skills): catch issues before they ship
- **Knowledge & Continuity** (2 skills): never solve the same problem twice
- **Parallel & Multi-Agent Development** (2 skills): scale your work safely
- **Testing Patterns** (5 skills): test what matters, not just what's easy
- **Deployment & Operations** (4 skills): ship with confidence
- **Gap Analysis & Remediation** (2 skills): audit and systematically close gaps
- **Process** (3 skills): stay focused, build to the right standard
- **Meta** (1 skill): skill routing

### What the skills *don't* do

Modern models and harnesses already handle some things well, and a skill that duplicates them only adds noise. v2.0 removed skills for context-window management (harnesses compact automatically), output formatting (models format well by default), always-on skill bootstrapping (skills trigger from their descriptions), and private task queues (use your issue tracker). See [CHANGELOG](CHANGELOG.md#200---2026-09-25) for the full list and migration.

## Installation

### Claude Code

From inside a Claude Code session:

```bash
# 1. Add the marketplace (one-time)
/plugin marketplace add ash1794/vibe-engineering

# 2. Install the plugin
/plugin install vibe-engineering@vibe-plugins
```

Later, pull updates with `/plugin marketplace update vibe-plugins`.

Local development (unpackaged, for testing plugin changes):

```bash
git clone https://github.com/ash1794/vibe-engineering.git
claude --plugin-dir ./vibe-engineering/plugins/vibe-engineering
```

All 29 skills are now available in every Claude Code session.

### OpenAI Codex & Gemini CLI

Both read skills from `.agents/skills/`, the cross-tool path in the Agent Skills standard, so one set of symlinks covers both:

```bash
# Clone once, symlink many times
git clone https://github.com/ash1794/vibe-engineering.git ~/src/vibe-engineering

# User-wide (available in all projects)
mkdir -p ~/.agents/skills
ln -s ~/src/vibe-engineering/plugins/vibe-engineering/skills/* ~/.agents/skills/

# Or per-project
mkdir -p .agents/skills
ln -s ~/src/vibe-engineering/plugins/vibe-engineering/skills/* .agents/skills/
```

Gemini CLI also accepts `~/.gemini/skills/` and `.gemini/skills/`. Run `/skills` in Gemini CLI to confirm the skills were discovered.

> **Upgrading from 1.x with symlinks?** Skill folders were renamed to match their `name` (e.g. `quality-loop/` → `vibe-quality-loop/`) and 9 skills were retired, so remove your old symlinks and re-run the `ln -s` command above.

## Quick Start

After installation, skills activate automatically when a task matches their description.

Find the right skill:
```
/vibe-engineering:vibe-help        # Claude Code
$vibe-help                         # Codex
```

Invoke any skill directly:
```
# Claude Code
/vibe-engineering:vibe-quality-loop
/vibe-engineering:vibe-research-before-design

# Codex
$vibe-quality-loop
$vibe-research-before-design
```

In Gemini CLI, skills are activated automatically from their descriptions, or you can ask for one by name.

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
vibe-spec-sync --audit ──→ Final verification: no remaining gaps
```

The CLI exposes the critical parts for automation:
- `vibe-cli decisions` → extract decisions from staged changes
- `vibe-cli spec-drift` → detect spec-code drift
- `vibe-cli coverage` → verify all coverage dimensions
- `vibe-cli pre-commit` → block commits with secrets/debug code

## Skill Catalog

### Meta
| Skill | Trigger | Purpose |
|-------|---------|---------|
| `vibe-help` | "What skill should I use?" | Skill router and full catalog |

### Research & Decision-Making
| Skill | Trigger | Purpose |
|-------|---------|---------|
| `vibe-research-before-design` | Before any new feature/architecture/tech choice | Research real projects, papers, and documented failures, with verified sources |
| `vibe-decision-journal` | After any architectural choice or before committing | Automatic decision extraction from diffs + ADR recording |
| `vibe-devil-advocate-review` | Before shipping recommendations or large changes | 5-dimension challenge, ideally by a fresh context or a different model |

### Quality Gates & Validation
| Skill | Trigger | Purpose |
|-------|---------|---------|
| `vibe-acceptance-gate` | After completing a task with criteria | PASS/FAIL validation against criteria, with evidence |
| `vibe-quality-loop` | After any non-trivial implementation | Review→Test→Fix loop until clean, using the repo's own checks |
| `vibe-anti-rationalization-check` | Before claiming done; when a test is "in the way" | Catches reward hacking: test tampering, special-casing, unverified claims |
| `vibe-spec-sync` | Before committing, or when implementation is claimed complete | Spec drift detection + approved write-back; `--audit` for full spec-vs-code check |
| `vibe-doc-quality-gate` | After editing any technical doc | Fast 6-point document quality check |
| `vibe-requirements-validator` | When reviewing PRD/user stories | SMART criteria validation |
| `vibe-coverage-enforcer` | Before claiming code complete | 3-dimension coverage: line + spec-to-test + spec-to-code |

### Knowledge & Continuity
| Skill | Trigger | Purpose |
|-------|---------|---------|
| `vibe-reflect-and-compound` | After feedback, a non-trivial bug, or a repeated pattern | Learnings, bug entries, and patterns written to the memory file your agent loads (CLAUDE.md / AGENTS.md / GEMINI.md) |
| `vibe-handover-doc` | Handing off to a person, another tool, or a future session | Cold-start handover doc with resume prompt |

### Parallel & Multi-Agent Development
| Skill | Trigger | Purpose |
|-------|---------|---------|
| `vibe-parallel-task-decomposition` | Large task with independent subtasks | DAG analysis and dispatch plan for the harness's native subagents |
| `vibe-cherry-pick-integration` | After parallel agents complete | Safe sequential integration of branches/worktrees |

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
| `vibe-pre-commit-audit` | Before creating a commit | Runs hooks/secret scanners first, then checks for secrets, debug code, TODOs |
| `vibe-safe-deploy` | Before any deployment | Pre-flight checks, atomic deploy, rollback |
| `vibe-rollback-plan` | Before risky changes | Documented rollback runbook |
| `vibe-service-health-dashboard` | Checking running services | Multi-service health monitoring |

### Gap Analysis & Remediation
| Skill | Trigger | Purpose |
|-------|---------|---------|
| `vibe-gap-analysis` | Before production launch or after major refactor | 17-dimension production readiness audit with parallel agents |
| `vibe-gap-closure-loop` | 10+ findings, bugs, or audit items | Prioritized waves → parallel fix streams → test gate → re-audit |

### Process
| Skill | Trigger | Purpose |
|-------|---------|---------|
| `vibe-scope-guard` | During implementation | Scope creep and over-engineering detection |
| `vibe-production-mindset` | Before declaring a production feature done | Production hardening checklist, scaled to real stakes |
| `vibe-iteration-review` | End of development iteration | Quality grading and trend analysis |

## Why vibe-engineering?

AI coding agents are far more capable than they were a year ago, but some failure modes persist: satisfying the test instead of the goal, over-building, claiming "done" without evidence, and agreeing with their own first idea. **vibe-engineering targets exactly those.**

| Without | With vibe-engineering |
|---------|----------------------|
| "Let me just build it" | Research existing solutions and their failures first (`vibe-research-before-design`) |
| "Tests pass, ship it" | Check coverage standards are met (`vibe-coverage-enforcer`) |
| "I'll remember the decision" | Extract it automatically from diffs (`vibe-decision-journal`) |
| "Good enough" | Loop until clean, with evidence (`vibe-quality-loop`) |
| "Spec is probably still accurate" | Detect drift and sync back (`vibe-spec-sync`) |
| Test loosened until it passed | Caught and disclosed (`vibe-anti-rationalization-check`) |
| Same bug investigated twice | Root cause saved to the agent's memory file (`vibe-reflect-and-compound`) |
| Self-review that agrees with itself | Review by a fresh context or another model (`vibe-devil-advocate-review`) |

## Design Principles

1. **Born from pain, not theory**: every skill exists because skipping it caused real problems
2. **Don't duplicate the model**: if current models or harnesses already do it well, it's not a skill
3. **When to use AND when NOT to use**: every skill has explicit triggers and anti-triggers
4. **Harness-neutral**: skills describe capabilities, not one tool's API, and never hard-code a model (see [`references/platform-tools.md`](references/platform-tools.md))
5. **Composable**: skills work independently or together
6. **Advisory first, enforcement when it matters**: skills guide; the CLI enforces in CI/CD

## How It Works

The repo is a Claude Code **marketplace** (`vibe-plugins`) that ships one plugin (`vibe-engineering`), whose `skills/` directory is also a standard Agent Skills collection for Codex and Gemini CLI:

- **Claude Code**: `.claude-plugin/marketplace.json` at the repo root catalogs the plugin; the plugin itself lives in `plugins/vibe-engineering/` with its own `.claude-plugin/plugin.json`
- **Codex & Gemini CLI**: `.agents/skills/` symlinks into the plugin's `skills/` directory; both discover skills from this standard path

```
vibe-engineering/                          # repo root = marketplace root
├── .claude-plugin/
│   └── marketplace.json                   # marketplace: "vibe-plugins"
├── plugins/
│   └── vibe-engineering/                  # plugin root
│       ├── .claude-plugin/plugin.json     # plugin: "vibe-engineering"
│       └── skills/                        # 29 skill definitions
│           ├── vibe-help/SKILL.md
│           ├── vibe-quality-loop/SKILL.md
│           ├── vibe-spec-sync/SKILL.md
│           └── ... (folder name == skill name)
├── .agents/
│   └── skills → ../plugins/vibe-engineering/skills  # Codex + Gemini CLI discovery
├── AGENTS.md                              # Codex / cross-tool project instructions
├── GEMINI.md                              # Gemini CLI project instructions (imports AGENTS.md)
├── references/
│   └── platform-tools.md                  # Capability mapping across Claude Code, Codex, Gemini CLI
├── scripts/
│   ├── vibe-cli                           # CLI for CI/CD enforcement
│   └── validate-skills.sh                 # Skill file validator
└── README.md
```

Each skill has:
- **YAML frontmatter** with `name` (matching its folder) and `description`
- **When to Use**: explicit triggers
- **When NOT to Use**: anti-triggers to prevent misapplication
- **Steps**: the actual workflow
- **Output Format**: structured output template

## Contributing

Found a pattern that keeps saving you? Turn it into a skill:

1. Fork this repo
2. Create `plugins/vibe-engineering/skills/vibe-your-skill-name/SKILL.md` (the folder name must equal `name`)
3. Follow the template below and the portability rules in [`references/platform-tools.md`](references/platform-tools.md)
4. Add it to the catalog in this README and in `vibe-help`
5. Run `bash scripts/validate-skills.sh`, then submit a PR

Before adding a skill, ask: *would a current frontier model do this well without being told?* If yes, it isn't a skill.

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

These skills were extracted from building an 11-agent personal assistant system with Go backend, React Native frontend, and 205+ test files.

**The numbers:**
- 50+ session observations analyzed (310k+ tokens of development history)
- 15 project-specific skills generalized into 38 universal patterns (v1.x)
- Consolidated to 29 in v2.0 after re-auditing each one against current Claude, GPT, and Gemini models
- Every skill represents a pattern that emerged from real pain — not a theoretical best practice document

## Also Check Out

- **[bart-coaching](https://github.com/ash1794/bart-coaching)** — Growth-oriented coaching hooks for Claude Code. Provides real-time technical depth insights, operational maturity nudges, and behavioral self-awareness mirrors with compound reflections across sessions. Pairs well with vibe-engineering for engineers who want both discipline tools and growth feedback.

## License

MIT — Use it, fork it, make it yours.
