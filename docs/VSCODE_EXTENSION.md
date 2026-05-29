# VS Code Extension Installation Guide

## 📦 Install from VS Code Marketplace

### Method 1: Search in VS Code

1. Open VS Code
2. Click Extensions icon (Ctrl+Shift+X)
3. Search for "AI Chat Backup"
4. Click "Install"

### Method 2: Command Line

```bash
code --install-extension yizebaba.ai-chat-backup
```

---

## 🔧 Install from VSIX File

### Download VSIX

```bash
# Download latest release
wget https://github.com/Yizebaba/claude-smart-backup/releases/latest/download/ai-chat-backup.vsix
```

### Install

**Method 1: VS Code UI**
1. Open VS Code
2. Extensions → ⋯ (More Actions) → Install from VSIX
3. Select the downloaded .vsix file

**Method 2: Command Line**
```bash
code --install-extension ai-chat-backup.vsix
```

---

## 🛠️ Build from Source

```bash
# Clone repository
git clone https://github.com/Yizebaba/claude-smart-backup.git
cd claude-smart-backup/vscode-extension

# Install dependencies
npm install

# Package extension
npm run package

# Install
code --install-extension ai-chat-backup-2.0.0.vsix
```

---

## ⚙️ Configuration

After installation, configure in VS Code settings:

```json
{
  "aiChatBackup.enabled": true,
  "aiChatBackup.timeInterval": 2,
  "aiChatBackup.messageThreshold": 200,
  "aiChatBackup.keepBackups": 2,
  "aiChatBackup.autoRestore": true
}
```

---

## 🎯 Usage

### Commands

- `AI Chat Backup: Backup Now` - Manual backup
- `AI Chat Backup: Restore Latest` - Restore from backup
- `AI Chat Backup: Show Status` - View backup status
- `AI Chat Backup: Configure` - Open settings

### Status Bar

Click the "$(database) AI Backup" icon in the status bar to view status.

---

## 🔍 Troubleshooting

### Extension Not Working

1. Check Python is installed: `python3 --version`
2. Check monitor.py exists in extension directory
3. View extension logs: Developer → Show Logs → Extension Host

### Backup Failed

1. Check disk space
2. Check permissions
3. View detailed logs in Output panel

---

## 📝 Supported Editors

- ✅ VS Code
- ✅ VS Code Insiders
- ✅ Cursor (VS Code fork)
- ✅ Windsurf (VS Code fork)
- ✅ Code - OSS

---

## 🌐 Language Support

The extension UI supports:
- English
- 中文 (Chinese)
- 日本語 (Japanese)
- 한국어 (Korean)
- Русский (Russian)
- Español (Spanish)
- Français (French)
- Deutsch (German)
- Português (Portuguese)
