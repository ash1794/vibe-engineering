# vibe-engineering

38 engineering discipline skills for AI-assisted development. Works with Claude Code and OpenAI Codex.

## Skills

Skills live in `skills/*/SKILL.md` (also symlinked at `.agents/skills/` for Codex discovery).

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
| `skills/` | All 38 skill definitions |
| `.agents/skills/` | Symlink for Codex discovery |
| `.claude-plugin/plugin.json` | Claude Code plugin manifest |
| `scripts/vibe-cli` | CI/CD enforcement CLI |
| `references/codex-tools.md` | Tool name mapping across platforms |
