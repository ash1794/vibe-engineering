# Tool Mapping: Claude Code ↔ Codex

Skills in this repository use Claude Code tool names. When running under Codex, use these equivalents.

## Core Tools

| Claude Code | Codex | Notes |
|-------------|-------|-------|
| `Read` | `read_file` | Read file contents |
| `Write` | `write_file` | Create or overwrite a file |
| `Edit` | `edit_file` | Apply targeted edits to a file |
| `Glob` | `glob` | Find files by pattern |
| `Grep` | `grep` | Search file contents with regex |
| `Bash` | `shell` | Execute shell commands |
| `Agent` | (subagent dispatch) | Launch parallel sub-tasks |
| `WebFetch` | `web_search` / `web_fetch` | Fetch web content |
| `Skill` | `activate_skill` | Invoke a skill by name |

## Behavioral Differences

- **File creation**: Claude Code's `Write` overwrites; Codex's `write_file` behaves similarly. Both require reading first for existing files.
- **Search**: Claude Code's `Grep` wraps ripgrep. Codex's `grep` may have different flag support — prefer simple patterns.
- **Subagents**: Claude Code uses `Agent` tool with `subagent_type`. Codex uses its own task dispatch. Skills that reference `Agent` should be adapted to the platform's parallel execution model.
- **Skill invocation**: Claude Code uses `/skill-name`, Codex uses `$skill-name` or implicit matching.

## In Practice

Most skills only use `Read`, `Edit`, `Write`, `Bash`, `Grep`, and `Glob` — all of which have direct Codex equivalents. Skills that dispatch subagents (like `vibe-gap-analysis`) may need platform-specific adaptation.
