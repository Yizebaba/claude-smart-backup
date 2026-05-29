#!/usr/bin/env python3
"""
AI Chat Backup Monitor - Universal backup system for AI coding assistants

Supports: Claude Code, Cursor, Windsurf, Cline, Continue, Aider, 
          Copilot Workspace, Cody, Tabnine, Amazon Q
Platforms: Linux, macOS, Windows
"""

import json
import os
import platform
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

# AI Tool Configurations
AI_TOOLS = {
    "claude-code": {
        "name": "Claude Code",
        "config_dir": "~/.claude",
        "history": "history.jsonl",
        "settings": "settings.json",
        "model_change": True,
    },
    "cursor": {
        "name": "Cursor",
        "config_dir": {
            "linux": "~/.config/Cursor/User",
            "darwin": "~/Library/Application Support/Cursor/User",
            "windows": "%APPDATA%/Cursor/User",
        },
        "history": "globalStorage/state.vscdb",
        "settings": "settings.json",
        "model_change": True,
    },
    "windsurf": {
        "name": "Windsurf",
        "config_dir": {
            "linux": "~/.config/Windsurf",
            "darwin": "~/Library/Application Support/Windsurf",
            "windows": "%APPDATA%/Windsurf",
        },
        "history": "conversations.json",
        "settings": "settings.json",
        "model_change": True,
    },
    "cline": {
        "name": "Cline (VS Code)",
        "config_dir": "~/.vscode/extensions/saoudrizwan.claude-dev-*",
        "history": "tasks.json",
        "settings": "settings.json",
        "model_change": False,
    },
    "continue": {
        "name": "Continue",
        "config_dir": "~/.continue",
        "history": "sessions.json",
        "settings": "config.json",
        "model_change": True,
    },
    "aider": {
        "name": "Aider",
        "config_dir": "~/.aider",
        "history": "chat_history.txt",
        "settings": ".aider.conf.yml",
        "model_change": True,
    },
    "copilot": {
        "name": "GitHub Copilot Workspace",
        "config_dir": {
            "linux": "~/.config/github-copilot",
            "darwin": "~/Library/Application Support/github-copilot",
            "windows": "%APPDATA%/github-copilot",
        },
        "history": "workspace_history.json",
        "settings": "settings.json",
        "model_change": False,
    },
    "cody": {
        "name": "Cody (Sourcegraph)",
        "config_dir": {
            "linux": "~/.config/cody",
            "darwin": "~/Library/Application Support/cody",
            "windows": "%APPDATA%/cody",
        },
        "history": "chat_history.json",
        "settings": "settings.json",
        "model_change": True,
    },
    "tabnine": {
        "name": "Tabnine",
        "config_dir": {
            "linux": "~/.config/TabNine",
            "darwin": "~/Library/Application Support/TabNine",
            "windows": "%APPDATA%/TabNine",
        },
        "history": "tabnine_config.json",
        "settings": "tabnine_config.json",
        "model_change": False,
    },
    "amazon-q": {
        "name": "Amazon Q Developer",
        "config_dir": {
            "linux": "~/.aws/amazonq",
            "darwin": "~/Library/Application Support/amazonq",
            "windows": "%APPDATA%/amazonq",
        },
        "history": "conversations.json",
        "settings": "settings.json",
        "model_change": False,
    },
}

def get_config_dir(tool_id):
    """Get config directory for a tool"""
    if tool_id not in AI_TOOLS:
        return None
    
    config = AI_TOOLS[tool_id]
    config_dir = config["config_dir"]
    
    if isinstance(config_dir, dict):
        system = platform.system().lower()
        config_dir = config_dir.get(system)
    
    if not config_dir:
        return None
    
    return Path(os.path.expanduser(os.path.expandvars(config_dir)))

def detect_tool():
    """Auto-detect AI tool"""
    for tool_id in AI_TOOLS:
        config_dir = get_config_dir(tool_id)
        if config_dir and config_dir.exists():
            return tool_id
    return None

def list_tools():
    """List all supported tools"""
    print("📋 Supported AI Tools:")
    print("━" * 60)
    for tool_id, config in AI_TOOLS.items():
        detected = "✓" if get_config_dir(tool_id) and get_config_dir(tool_id).exists() else "✗"
        model = "✓" if config["model_change"] else "✗"
        print(f"{detected} {config['name']:<30} (model: {model})")
    print("━" * 60)
    
    detected_tool = detect_tool()
    if detected_tool:
        print(f"\n✅ Detected: {AI_TOOLS[detected_tool]['name']}")
    else:
        print("\n⚠️  No AI tool detected")

def show_status(tool_id):
    """Show backup status"""
    state_file = Path.home() / ".ai-backup" / "state.json"
    
    if not state_file.exists():
        print("📊 No backup history")
        return
    
    try:
        state = json.loads(state_file.read_text())
        print("📊 Backup Status:")
        print("━" * 60)
        print(f"AI Tool: {AI_TOOLS.get(tool_id, {}).get('name', 'Unknown')}")
        print(f"Last backup: {datetime.fromtimestamp(state.get('last_backup_time', 0)).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total backups: {state.get('total_backups', 0)}")
        print(f"Messages: {state.get('message_count', 0)}")
        print("━" * 60)
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Chat Backup Monitor")
    parser.add_argument("--list-tools", action="store_true", help="List supported tools")
    parser.add_argument("--status", action="store_true", help="Show status")
    parser.add_argument("--tool", type=str, help="Specify AI tool")
    parser.add_argument("--daemon", action="store_true", help="Run as daemon")
    parser.add_argument("--check", action="store_true", help="Check once")
    
    args = parser.parse_args()
    
    if args.list_tools:
        list_tools()
        return
    
    tool_id = args.tool or os.environ.get("AI_TOOL") or detect_tool()
    
    if not tool_id:
        print("❌ No AI tool detected. Use --tool to specify.")
        print("\nRun with --list-tools to see supported tools.")
        sys.exit(1)
    
    if args.status:
        show_status(tool_id)
        return
    
    print(f"🎯 Monitoring: {AI_TOOLS[tool_id]['name']}")
    print("⚠️  Full backup functionality coming soon!")
    print("📝 This is a preview version showing tool detection.")

if __name__ == "__main__":
    main()
