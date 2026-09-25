# vibe-engineering

29 engineering discipline skills for AI-assisted development. Works with Claude Code, OpenAI Codex, and Gemini CLI.

## Skills

Skills live in `plugins/vibe-engineering/skills/*/SKILL.md` (also symlinked at `.agents/skills/`, which Codex and Gemini CLI both read).

Each skill has YAML frontmatter with `name` (equal to its folder name) and `description`, following the Agent Skills standard. `user-invocable: true` is a Claude Code field that other agents ignore.

## Invocation

- **Claude Code**: `/vibe-engineering:<skill-name>` or implicit matching via description
- **Codex**: `$skill-name` or implicit matching via description
- **Gemini CLI**: implicit matching via description (`/skills` lists installed skills)

## Tool Mapping

Skills describe capabilities ("run the tests", "dispatch a subagent", "ask the user") rather than one agent's tool names. `references/platform-tools.md` maps each capability to Claude Code, Codex, and Gemini CLI.

## Project Conventions

- Skill names use the `vibe-` prefix (e.g., `vibe-quality-loop`) and match their folder name
- Each skill directory contains exactly one `SKILL.md` file
- Skills are cross-project, with no language or framework assumptions, and are model-neutral (no hard-coded model names)
- New skills must be listed in the README catalog and in `vibe-help`
- Run `bash scripts/validate-skills.sh` before committing
- The `vibe-cli` script in `scripts/` provides CI/CD integration

## Key Paths

| Path | Purpose |
|------|---------|
| `.claude-plugin/marketplace.json` | Marketplace catalog (`vibe-plugins`) |
| `plugins/vibe-engineering/.claude-plugin/plugin.json` | Claude Code plugin manifest |
| `plugins/vibe-engineering/skills/` | All 29 skill definitions |
| `.agents/skills/` | Symlink for Codex and Gemini CLI discovery |
| `scripts/vibe-cli` | CI/CD enforcement CLI |
| `references/platform-tools.md` | Capability mapping across agents |

See `CLAUDE.md` for the plugin-structure invariants that CI enforces.
