#!/usr/bin/env bash
# Validates all SKILL.md files for required structure and checks manifest consistency.
# Exit code 0 = all checks pass, 1 = failures found.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PLUGIN_ROOT="$REPO_ROOT/plugins/vibe-engineering"
SKILLS_DIR="$PLUGIN_ROOT/skills"
PLUGIN_JSON="$PLUGIN_ROOT/.claude-plugin/plugin.json"
MARKETPLACE_JSON="$REPO_ROOT/.claude-plugin/marketplace.json"
README="$REPO_ROOT/README.md"

errors=0
warnings=0

error() { echo "  ERROR: $1"; errors=$((errors + 1)); }
warn()  { echo "  WARN:  $1"; warnings=$((warnings + 1)); }

echo "=== Skill File Validation ==="
echo

# Collect all skill directories
skill_dirs=("$SKILLS_DIR"/*/SKILL.md)
skill_count=${#skill_dirs[@]}
echo "Found $skill_count skills"
echo

for skill_file in "${skill_dirs[@]}"; do
  skill_name="$(basename "$(dirname "$skill_file")")"
  echo "[$skill_name]"

  # Check YAML frontmatter exists
  if ! head -1 "$skill_file" | grep -q '^---$'; then
    error "Missing YAML frontmatter"
    continue
  fi

  # Extract frontmatter
  frontmatter=$(sed -n '/^---$/,/^---$/p' "$skill_file")

  # Check required frontmatter fields
  if ! echo "$frontmatter" | grep -q '^name:'; then
    error "Missing 'name' in frontmatter"
  fi
  if ! echo "$frontmatter" | grep -q '^description:'; then
    error "Missing 'description' in frontmatter"
  fi

  # Check required sections
  if ! grep -q '## When to Use' "$skill_file"; then
    error "Missing '## When to Use' section"
  fi
  if ! grep -q '## When NOT to Use' "$skill_file"; then
    warn "Missing '## When NOT to Use' section"
  fi

  # Check name starts with vibe- prefix
  fm_name=$(echo "$frontmatter" | grep '^name:' | head -1 | sed 's/^name: *//')
  if [[ -n "$fm_name" && ! "$fm_name" =~ ^vibe- ]]; then
    warn "Skill name '$fm_name' does not start with 'vibe-' prefix"
  fi

  echo "  OK"
done

echo
echo "=== Manifest Consistency ==="

# Check plugin.json version matches marketplace.json version
if [[ -f "$PLUGIN_JSON" && -f "$MARKETPLACE_JSON" ]]; then
  plugin_version=$(grep '"version"' "$PLUGIN_JSON" | head -1 | sed 's/.*: *"\(.*\)".*/\1/')
  marketplace_version=$(grep '"version"' "$MARKETPLACE_JSON" | head -1 | sed 's/.*: *"\(.*\)".*/\1/')

  if [[ "$plugin_version" != "$marketplace_version" ]]; then
    error "Version mismatch: plugin.json=$plugin_version, marketplace.json=$marketplace_version"
  else
    echo "  Versions match: $plugin_version"
  fi
fi

# Check README skill count matches actual count
if [[ -f "$README" ]]; then
  readme_count=$(grep -oP '\b\d+ (engineering discipline )?skills\b' "$README" | head -1 | grep -oP '^\d+')
  if [[ -n "$readme_count" && "$readme_count" -ne "$skill_count" ]]; then
    error "README claims $readme_count skills but found $skill_count skill directories"
  else
    echo "  Skill count matches: $skill_count"
  fi
fi

echo
echo "=== Plugin Structure Invariants ==="
# These three invariants, if any is broken, produce either an uninstallable
# repo or a recursive plugin-cache loop. See CLAUDE.md "Plugin structure
# invariants" and commit c5ffb98 for the incident history.

# Invariant 1: .claude-plugin/marketplace.json MUST exist at repo root.
# Without it, `/plugin marketplace add` has nothing to catalog — the
# plugin becomes uninstallable via any supported Claude Code flow.
if [[ -f "$MARKETPLACE_JSON" ]]; then
  echo "  [1/3] marketplace.json present at repo root"
else
  error "[1/3] $MARKETPLACE_JSON is missing — plugin would be uninstallable"
fi

# Invariant 2: plugin directory MUST NOT be the repo root (which is the
# marketplace root). If plugin.json sits next to marketplace.json, the
# plugin's cache copy contains marketplace.json, Claude Code re-enumerates
# it as a marketplace, and cache/.../cache/... recurses until ENAMETOOLONG.
if [[ -f "$REPO_ROOT/.claude-plugin/plugin.json" ]]; then
  error "[2/3] plugin.json found at repo root — move it into plugins/<name>/.claude-plugin/ to prevent recursive cache nesting"
elif [[ -f "$PLUGIN_JSON" && "$PLUGIN_ROOT" != "$REPO_ROOT" ]]; then
  echo "  [2/3] plugin lives in subdirectory (plugins/vibe-engineering/)"
else
  error "[2/3] plugin.json not found at $PLUGIN_JSON"
fi

# Invariant 3: marketplace name MUST differ from plugin name. Same-name
# collision confuses Claude Code's plugin/marketplace registries and was
# the amplifier for issue #1.
if [[ -f "$MARKETPLACE_JSON" && -f "$PLUGIN_JSON" ]]; then
  mp_name=$(grep -m1 '"name"' "$MARKETPLACE_JSON" | sed 's/.*: *"\(.*\)".*/\1/')
  pl_name=$(grep -m1 '"name"' "$PLUGIN_JSON" | sed 's/.*: *"\(.*\)".*/\1/')
  if [[ -z "$mp_name" || -z "$pl_name" ]]; then
    error "[3/3] could not extract names (marketplace='$mp_name', plugin='$pl_name')"
  elif [[ "$mp_name" == "$pl_name" ]]; then
    error "[3/3] marketplace name '$mp_name' collides with plugin name '$pl_name' — pick distinct names (e.g. 'vibe-plugins' / 'vibe-engineering')"
  else
    echo "  [3/3] names distinct: marketplace='$mp_name' plugin='$pl_name'"
  fi
fi

echo
echo "=== Summary ==="
echo "Skills: $skill_count | Errors: $errors | Warnings: $warnings"

if [[ $errors -gt 0 ]]; then
  echo "FAILED"
  exit 1
else
  echo "PASSED"
  exit 0
fi
