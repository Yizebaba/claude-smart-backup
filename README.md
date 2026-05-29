# AI Chat Backup - Universal Backup System

🎯 **Universal backup system for AI coding assistants** - Smart triggers, auto-restore, cross-platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-blue)](https://github.com/Yizebaba/claude-smart-backup)

## ✨ Features

### 🤖 Supports 10+ AI Tools

- ✅ **Claude Code** (CLI, Desktop, Web)
- ✅ **Cursor**
- ✅ **Windsurf**
- ✅ **Cline** (VS Code extension)
- ✅ **Continue** (VS Code/JetBrains)
- ✅ **Aider**
- ✅ **GitHub Copilot Workspace**
- ✅ **Cody** (Sourcegraph)
- ✅ **Tabnine**
- ✅ **Amazon Q Developer**

### 💻 Cross-Platform

- ✅ **Linux** (Ubuntu, Debian, Fedora, Arch, etc.)
- ✅ **macOS** (Intel & Apple Silicon)
- ✅ **Windows** (Native & WSL)

### 🎯 Smart Triggers (any one triggers backup)

- ⏰ **Time**: Every N hours (default: 2)
- 💬 **Messages**: New N messages (default: 200)
- ✅ **Tasks**: Completed N tasks (default: 5)
- 🔄 **Model Change**: Auto-detect and restore

### 🔄 Auto-Restore on Model Change

When model change is detected:
1. Backup old model data
2. Restore to new model
3. Load chat history, projects, tools
4. Create notification file
5. Reset all counters

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/Yizebaba/claude-smart-backup.git
cd claude-smart-backup

# Auto-detect your AI tool and install
./install.sh
```

### Usage

```bash
# Check status
python3 monitor.py --status

# List supported tools
python3 monitor.py --list-tools

# Manual check
python3 monitor.py --check

# Run as daemon
python3 monitor.py --daemon
```

## 📊 How It Works

### Auto-Detection

The system automatically detects which AI tool you're using:

```bash
$ python3 monitor.py --list-tools

📋 Supported AI Tools:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Claude Code                  (model change: ✓)
✗ Cursor                       (model change: ✓)
✗ Windsurf                     (model change: ✓)
...

Detected: Claude Code
```

### Monitoring Flow

```
Start monitoring
  ↓
Check every 5 minutes
  ↓
Check 4 trigger conditions
  ↓
Any condition met?
  ├─ Yes → Backup → Reset counters → Continue
  └─ No → Continue
```

### Model Change Flow

```
Detect model change
  ↓
Backup old model data
  ↓
Restore to new model
  ↓
Create notification
  ↓
New model reads notification
  ↓
Continue conversation
```

## 🔧 Configuration

### Environment Variables

```bash
# Specify AI tool (auto-detect if not set)
export AI_TOOL=cursor

# Trigger thresholds
export BACKUP_TIME_HOURS=2
export BACKUP_MESSAGE_THRESHOLD=200
export BACKUP_TASK_THRESHOLD=5

# Keep N backups
export KEEP_BACKUPS=2

# Auto-restore on model change
export AUTO_RESTORE=true
```

### Config File

Create `~/.ai-backup/config.json`:

```json
{
  "ai_tool": "cursor",
  "time_hours": 2,
  "message_threshold": 200,
  "task_threshold": 5,
  "keep_backups": 2,
  "auto_restore": true
}
```

## 🎯 Use Cases

### Case 1: Frequent Model Switching

```bash
# System monitors automatically
# Switches model → auto backup & restore
# Seamless transition
```

### Case 2: Long Conversations

```bash
# New 200 messages → auto backup
# Protect against accidental loss
```

### Case 3: Project Development

```bash
# Complete 5 tasks → auto backup
# Protect development progress
```

## 📝 AI Tool Specific Notes

### Claude Code

- ✅ Full support
- ✅ Model change detection
- ✅ Project sessions
- ✅ Agents, Rules, Skills

### Cursor

- ✅ Full support
- ✅ Model change detection
- ✅ Workspace state
- ⚠️ Requires Cursor 0.30+

### Windsurf

- ✅ Full support
- ✅ Model change detection
- ✅ Conversation history

### Cline (VS Code)

- ✅ Task history backup
- ❌ No model change detection
- ⚠️ Extension-specific

### Continue

- ✅ Full support
- ✅ Model change detection
- ✅ Session history

### Aider

- ✅ Chat history backup
- ✅ Model change detection
- ✅ Config file backup

### GitHub Copilot Workspace

- ✅ Workspace history
- ❌ No model change detection

### Cody (Sourcegraph)

- ✅ Full support
- ✅ Model change detection

### Tabnine

- ✅ Config backup
- ❌ No model change detection

### Amazon Q Developer

- ✅ Conversation backup
- ❌ No model change detection

## 🎓 Advanced Usage

### Daemon Mode (systemd)

```bash
# Install as systemd service
./install.sh --daemon

# Manage service
systemctl --user status ai-backup-monitor
systemctl --user restart ai-backup-monitor
journalctl --user -u ai-backup-monitor -f
```

### Cron Mode

```bash
# Check every 10 minutes
./install.sh --cron
```

### Manual Mode

```bash
# Full control
python3 monitor.py --check
```

## 📊 Performance

- **CPU**: ~0% (checks every 5 minutes)
- **Memory**: ~10MB (Python process)
- **Disk**: 5-10MB per backup

## 🔍 Troubleshooting

### Issue 1: Tool Not Detected

```bash
# List detected tools
python3 monitor.py --list-tools

# Manually specify
export AI_TOOL=cursor
python3 monitor.py --status
```

### Issue 2: Backup Not Triggered

```bash
# Check status
python3 monitor.py --status

# Lower thresholds
export BACKUP_MESSAGE_THRESHOLD=50
```

### Issue 3: Model Change Not Detected

```bash
# Check if tool supports it
python3 monitor.py --list-tools

# Verify settings file exists
ls -la ~/.cursor/settings.json  # or your tool's config
```

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add your AI tool support
4. Submit a pull request

### Adding New AI Tool

Edit `monitor.py` and add to `AIToolConfig.TOOLS`:

```python
"your-tool": {
    "name": "Your Tool",
    "config_dir": {
        "linux": "~/.config/your-tool",
        "darwin": "~/Library/Application Support/your-tool",
        "windows": "%APPDATA%/your-tool",
    },
    "history_file": "history.json",
    "settings_file": "settings.json",
    "supports_model_change": True,
}
```

## 📄 License

MIT License - see [LICENSE](LICENSE)

## 🙏 Acknowledgments

- Inspired by frequent model switching needs
- Thanks to all AI tool developers
- Community feedback and contributions

## 📚 Related Projects

- [claude-backup](https://github.com/twilligon/claude-backup)
- [claude-conversation-extractor](https://github.com/ZeroSumQuant/claude-conversation-extractor)
- [claude-code-sync](https://github.com/perfectra1n/claude-code-sync)

## 🎯 Roadmap

- [ ] Web UI for management
- [ ] Remote backup (S3, Google Drive)
- [ ] Backup encryption
- [ ] Multi-user support
- [ ] Backup compression
- [ ] Custom trigger conditions
- [ ] Slack/Discord notifications

## 📧 Contact

Issues: [GitHub Issues](https://github.com/Yizebaba/claude-smart-backup/issues)

---

**⭐ Star this repo if it helps you!**
