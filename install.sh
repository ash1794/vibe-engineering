#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$SCRIPT_DIR/skills"

usage() {
    echo "Usage: install.sh [--global|--project|--uninstall-global|--uninstall-project]"
    echo ""
    echo "Options:"
    echo "  --global              Install skills globally to ~/.claude/skills/"
    echo "  --project             Install skills to current project's .claude/skills/"
    echo "  --uninstall-global    Remove global skill symlinks"
    echo "  --uninstall-project   Remove project skill symlinks"
    echo ""
    echo "Skills are installed as symlinks, so updates to the source are automatic."
    exit 1
}

install_skills() {
    local target_dir="$1"
    local count=0

    mkdir -p "$target_dir"

    for skill_dir in "$SKILLS_DIR"/*/; do
        local skill_name=$(basename "$skill_dir")
        local target="$target_dir/$skill_name"

        if [ -L "$target" ]; then
            rm "$target"
        elif [ -d "$target" ]; then
            echo "  SKIP: $skill_name (directory exists, not a symlink — remove manually if you want to replace)"
            continue
        fi

        ln -s "$skill_dir" "$target"
        count=$((count + 1))
    done

    echo "Installed $count skills to $target_dir"
}

uninstall_skills() {
    local target_dir="$1"
    local count=0

    for skill_dir in "$SKILLS_DIR"/*/; do
        local skill_name=$(basename "$skill_dir")
        local target="$target_dir/$skill_name"

        if [ -L "$target" ]; then
            rm "$target"
            count=$((count + 1))
        fi
    done

    echo "Removed $count skill symlinks from $target_dir"
}

case "${1:-}" in
    --global)
        echo "Installing vibe-engineering skills globally..."
        install_skills "$HOME/.claude/skills"
        echo ""
        echo "Done! Skills are now available in all Claude Code sessions."
        echo "Try: /vibe-help"
        ;;
    --project)
        if [ ! -d ".git" ] && [ ! -f "CLAUDE.md" ]; then
            echo "Warning: Not in a project root (no .git or CLAUDE.md found)."
            read -p "Continue anyway? [y/N] " -n 1 -r
            echo
            [[ $REPLY =~ ^[Yy]$ ]] || exit 1
        fi
        echo "Installing vibe-engineering skills to current project..."
        install_skills ".claude/skills"
        echo ""
        echo "Done! Skills are now available in this project."
        echo "Note: Add '.claude/skills/*-vibe-*' to .gitignore if you don't want to commit symlinks."
        echo "Try: /vibe-help"
        ;;
    --uninstall-global)
        echo "Removing vibe-engineering skills from global install..."
        uninstall_skills "$HOME/.claude/skills"
        ;;
    --uninstall-project)
        echo "Removing vibe-engineering skills from current project..."
        uninstall_skills ".claude/skills"
        ;;
    *)
        usage
        ;;
esac
