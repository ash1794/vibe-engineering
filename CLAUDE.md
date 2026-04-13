# CLAUDE.md

Project notes for Claude Code (and any other AI agent) working in this repo.

## What this repo is

A Claude Code **marketplace** (`vibe-plugins`) that ships one **plugin** (`vibe-engineering`) containing 38 engineering-discipline skills. The same `SKILL.md` files also power OpenAI Codex via `.agents/skills/`.

```
vibe-engineering/                       # repo root = marketplace root
├── .claude-plugin/
│   └── marketplace.json                # marketplace: "vibe-plugins"
├── plugins/
│   └── vibe-engineering/               # plugin root
│       ├── .claude-plugin/plugin.json  # plugin: "vibe-engineering"
│       └── skills/                     # 38 SKILL.md files
└── .agents/skills -> ../plugins/vibe-engineering/skills  # Codex
```

Install flow users follow:
```
/plugin marketplace add ash1794/vibe-engineering
/plugin install vibe-engineering@vibe-plugins
```

## Plugin structure invariants — DO NOT BREAK THESE

These three rules are non-negotiable. Breaking any one produces either an **uninstallable repo** or a **recursive plugin-cache loop** (issue #1). `scripts/validate-skills.sh` enforces all three in CI — the build will fail if you violate them.

### 1. `.claude-plugin/marketplace.json` MUST exist at the repo root

Without it, `/plugin marketplace add` has nothing to catalog. The repo becomes uninstallable via any supported Claude Code flow. The `claude plugin add github:...` command advertised in older docs does not exist.

**History**: commit `50e13ad` deleted `marketplace.json` to work around the recursion bug below. It made the plugin uninstallable for a full release cycle. Don't repeat this.

### 2. The plugin directory MUST NOT be the repo root

The plugin must live in a subdirectory (we use `plugins/vibe-engineering/`), not alongside `marketplace.json`. If `plugin.json` sits next to `marketplace.json`, Claude Code's plugin cache copies the entire repo — including `marketplace.json` — into `~/.claude/plugins/cache/<marketplace>/<plugin>/`. The cached plugin directory then *also* looks like a marketplace, Claude Code re-enumerates it, and you get `cache/.../cache/...` recursion until `ENAMETOOLONG`.

This is the real root cause of issue #1. Removing `marketplace.json` was a workaround for a symptom, not a fix for the cause.

### 3. Marketplace name MUST differ from plugin name

Claude Code's plugin/marketplace registries index by name. Same-name collisions (`vibe-engineering` / `vibe-engineering`) create duplicate registry entries and amplify the recursion failure mode. Pick distinct names: we use marketplace `vibe-plugins` + plugin `vibe-engineering`. The GitHub repo name is irrelevant to either — it can still be `ash1794/vibe-engineering`.

## Validator

`scripts/validate-skills.sh` runs on every push and PR (`.github/workflows/validate.yml`). It checks:

- SKILL.md frontmatter and required sections on all 38 skills
- `plugin.json` version matches the plugin entry version in `marketplace.json`
- README skill count matches the actual count
- **The three invariants above** (`=== Plugin Structure Invariants ===` block)

Run locally:
```bash
bash scripts/validate-skills.sh
```

## When editing this repo

- **Skill edits** go in `plugins/vibe-engineering/skills/<name>/SKILL.md`
- **New skills** must start with the `vibe-` prefix and follow the template in README
- **Version bumps** must update `plugins/vibe-engineering/.claude-plugin/plugin.json`, `scripts/vibe-cli` (`VERSION=`), and the plugin entry in `.claude-plugin/marketplace.json` together. The validator enforces consistency between plugin.json and marketplace.json.
- **Never** move files back to the repo root. Never rename the marketplace to `vibe-engineering`. Both will fail CI.
