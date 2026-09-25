# Platform Mapping: Claude Code · Codex · Gemini CLI

Skills in this repo describe **capabilities** ("read the file", "dispatch a subagent", "ask the user") rather than tool names, so the same `SKILL.md` works in all three agents. Use this table when a skill's wording needs translating. Tool names change between releases, so check the agent's own tool list (`/tools`, `/help`) if one doesn't match.

## Capabilities

| Capability | Claude Code | OpenAI Codex | Gemini CLI |
|------------|-------------|--------------|------------|
| Read files | `Read` | shell (`cat`, `sed -n`) | `read_file` |
| Edit / create files | `Edit`, `Write` | `apply_patch` | `replace`, `write_file` |
| Search files | `Grep`, `Glob` | shell (`rg`, `find`) | `search_file_content`, `glob` |
| Run commands | `Bash` | `shell` | `run_shell_command` |
| Web research | `WebSearch`, `WebFetch` | `web_search` (when enabled) | `google_web_search`, `web_fetch` |
| Ask the user a structured question | `AskUserQuestion` | plain-text question | plain-text question |
| Track a task plan | task/todo tools | `update_plan` | `write_todos` |
| Parallel subagents | `Agent` (optionally in a worktree) | subagents / cloud tasks where available | subagents where enabled |
| Persistent memory | `CLAUDE.md`, auto-memory | `AGENTS.md` | `GEMINI.md`, `save_memory` |
| Invoke a skill | `/vibe-engineering:<name>` or `/<name>` | `$<name>` | automatic (`activate_skill`); `/skills` to list |
| Code review command | `/code-review` | `/review` | — |

Where a capability is missing (for example no subagents), skills fall back to doing the work sequentially in the main session.

## Skill Discovery Paths

| Agent | Project | User-wide |
|-------|---------|-----------|
| Claude Code | plugin install (see README) | plugin install |
| OpenAI Codex | `.agents/skills/` | `~/.agents/skills/` |
| Gemini CLI | `.agents/skills/` or `.gemini/skills/` | `~/.agents/skills/` or `~/.gemini/skills/` |

`.agents/skills/` is the cross-tool path from the Agent Skills standard. This repo's `.agents/skills` symlink is read by both Codex and Gemini CLI.

## Portability Rules for Skill Authors

- `name` must match the skill's folder name, be lowercase alphanumerics with single hyphens, and be at most 64 characters (Agent Skills spec). `scripts/validate-skills.sh` enforces this.
- `description` must be at most 1024 characters. Say what the skill does and when to use it; it's the only part the agent sees before activating the skill.
- Don't hard-code model names (`model: sonnet`, "use GPT-5", …). Say "inherit the session's model" or describe the tier.
- Don't depend on one harness's tool names. Describe the capability and, if needed, give the Claude Code name as an example.
- Write guidance in calm, plain language. Current models follow instructions closely, and "ALWAYS/MUST/1% chance" phrasing causes over-triggering.
