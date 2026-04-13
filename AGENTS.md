# vibe-engineering

38 engineering discipline skills for AI-assisted development. Works with Claude Code and OpenAI Codex.

## Skills

Skills live in `plugins/vibe-engineering/skills/*/SKILL.md` (also symlinked at `.agents/skills/` for Codex discovery).

Each skill has YAML frontmatter with `name`, `description`, and `user-invocable: true`.

## Invocation

- **Claude Code**: `/skill-name` or implicit matching via description
- **Codex**: `$skill-name` or implicit matching via description

## Tool Mapping

Skills reference Claude Code tool names. Codex equivalents are documented in `references/codex-tools.md`.

## Project Conventions

- Skill names use the `vibe-` prefix (e.g., `vibe-quality-loop`)
- Each skill directory contains exactly one `SKILL.md` file
- Skills are cross-project — no language or framework assumptions
- The `vibe-cli` script in `scripts/` provides CI/CD integration

## Key Paths

| Path | Purpose |
|------|---------|
| `.claude-plugin/marketplace.json` | Marketplace catalog (`vibe-plugins`) |
| `plugins/vibe-engineering/.claude-plugin/plugin.json` | Claude Code plugin manifest |
| `plugins/vibe-engineering/skills/` | All 38 skill definitions |
| `.agents/skills/` | Symlink for Codex discovery |
| `scripts/vibe-cli` | CI/CD enforcement CLI |
| `references/codex-tools.md` | Tool name mapping across platforms |
