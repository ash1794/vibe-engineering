# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.5.1] - 2026-04-13

### Fixed
- **Plugin is installable again.** Restored `.claude-plugin/marketplace.json` so users can actually add the repo as a marketplace and install the plugin. The previous "fix" that removed `marketplace.json` made the plugin uninstallable via any supported Claude Code flow.
- **Root cause of the earlier recursion bug (#1) properly addressed.** The plugin now lives in `plugins/vibe-engineering/` instead of at the repo root, so the plugin's cache copy no longer contains `marketplace.json`. This was the real source of the `cache/.../cache/...` nesting loop — not the marketplace file itself.

### Changed
- Repo restructured as a marketplace hosting one plugin:
  - `.claude-plugin/marketplace.json` at repo root (marketplace: `vibe-plugins`)
  - `plugins/vibe-engineering/.claude-plugin/plugin.json` (plugin: `vibe-engineering`)
  - `plugins/vibe-engineering/skills/` (all 38 skill definitions)
- Marketplace name is `vibe-plugins` (not `vibe-engineering`) to avoid the name collision with the plugin it hosts.
- `.agents/skills` symlink repointed to `../plugins/vibe-engineering/skills` so Codex discovery still works.
- README install instructions rewritten to the correct `/plugin marketplace add` + `/plugin install` syntax. The old `claude plugin add github:...` command never existed.
- `scripts/validate-skills.sh` updated for the new layout.

### Install

```bash
/plugin marketplace add ash1794/vibe-engineering
/plugin install vibe-engineering@vibe-plugins
```

## [1.5.0] - 2026-03-12

### Added
- OpenAI Codex compatibility — skills now discoverable by both Claude Code and Codex
- `.agents/skills/` symlink for Codex skill discovery
- `AGENTS.md` — project instructions for Codex (equivalent of CLAUDE.md)
- `references/codex-tools.md` — tool name mapping between Claude Code and Codex
- Codex installation instructions in README

### Changed
- README updated to reflect dual-platform support (Claude Code + Codex)
- Project description now references both platforms

## [1.4.0] - 2026-03-07

### Added
- `vibe-spec-sync` skill — bidirectional spec-code sync with drift detection and approved decision write-back
- `vibe-cli` (`scripts/vibe-cli`) — CI/CD-friendly wrapper with exit codes and JSON output
  - `vibe-cli pre-commit` — scan for secrets, debug code, disabled tests
  - `vibe-cli coverage` — run coverage with spec-to-test dimension
  - `vibe-cli spec-drift` — detect spec-code drift from staged changes
  - `vibe-cli decisions` — extract decisions from staged diffs
  - `vibe-cli hook install/uninstall` — git pre-commit hook management
- Spec-driven test generation mode in `vibe-adversarial-test-generation` with `# req:[ID]` traceability markers
- Three-dimension coverage in `vibe-coverage-enforcer` (line + spec-to-test + spec-to-code)
- Automatic decision extraction from staged diffs in `vibe-decision-journal` (Mode 1)
- Session sweep mode in `vibe-decision-journal` (Mode 3)
- Decision deduplication and supersession tracking

### Changed
- `vibe-decision-journal` — expanded from manual ADR recording to 3-mode system (automatic extraction, explicit, session sweep) with JSONL storage and deduplication
- `vibe-adversarial-test-generation` — expanded from edge-case-only to dual-mode (adversarial + spec-driven) with requirement traceability
- `vibe-coverage-enforcer` — expanded from line-coverage-only to 3-dimension coverage reporting
- README updated with CLI documentation, spec-code-test loop, and new skill descriptions

## [1.3.0] - 2026-03-06

### Added
- Enhanced README with skill catalog tables, design principles, and origin story
- Skill validation script (`scripts/validate-skills.sh`)
- CHANGELOG (this file)

### Fixed
- Synced marketplace.json version (1.2.0 -> 1.3.0) and skill count (34 -> 37) with plugin.json

## [1.2.0] - 2026-03-02

### Changed
- Aligned all skills with official Claude Code best practices

## [1.1.0] - 2026-03-02

### Added
- `vibe-gap-analysis` skill — 17-dimension production readiness audit
- `vibe-gap-closure-loop` skill — autonomous gap remediation loop

## [1.0.1] - 2026-03-02

### Added
- `vibe-start-informed` skill — research real projects before designing

### Fixed
- Corrected marketplace.json schema for proper parsing

## [1.0.0] - 2026-03-01

### Added
- Initial release with 34 engineering discipline skills
- Claude Code plugin format with plugin.json manifest
- Marketplace distribution support via marketplace.json
- MIT license
