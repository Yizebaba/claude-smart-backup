# AI 聊天备份 - 通用备份系统

🎯 **AI 编程助手的通用备份系统** - 智能触发、自动恢复、跨平台

[![许可证: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![平台](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-blue)](https://github.com/Yizebaba/claude-smart-backup)

## ✨ 功能特性

### 🤖 支持 10+ AI 工具

- ✅ **Claude Code**（CLI、桌面版、网页版）
- ✅ **Cursor**
- ✅ **Windsurf**
- ✅ **Cline**（VS Code 扩展）
- ✅ **Continue**（VS Code/JetBrains）
- ✅ **Aider**
- ✅ **GitHub Copilot Workspace**
- ✅ **Cody**（Sourcegraph）
- ✅ **Tabnine**
- ✅ **Amazon Q Developer**

### 💻 跨平台支持

- ✅ **Linux**（Ubuntu、Debian、Fedora、Arch 等）
- ✅ **macOS**（Intel 和 Apple Silicon）
- ✅ **Windows**（原生和 WSL）

### 🎯 智能触发（任意一个满足即备份）

- ⏰ **时间触发**：每 N 小时（默认：2）
- 💬 **消息触发**：新增 N 条消息（默认：200）
- ✅ **任务触发**：完成 N 个任务（默认：5）
- 🔄 **模型切换**：自动检测并恢复

### 🔄 模型切换自动恢复

当检测到模型切换时：
1. 备份旧模型数据
2. 恢复到新模型
3. 加载聊天记录、项目、工具
4. 创建通知文件
5. 重置所有计数器

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/Yizebaba/claude-smart-backup.git
cd claude-smart-backup

# 自动检测你的 AI 工具并安装
./install.sh
```

### 使用

```bash
# 查看状态
python3 monitor.py --status

# 列出支持的工具
python3 monitor.py --list-tools

# 手动检查
python3 monitor.py --check

# 作为守护进程运行
python3 monitor.py --daemon
```

## 📊 工作原理

### 自动检测

系统会自动检测你正在使用的 AI 工具：

```bash
$ python3 monitor.py --list-tools

📋 支持的 AI 工具：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Claude Code                  (模型切换: ✓)
✗ Cursor                       (模型切换: ✓)
✗ Windsurf                     (模型切换: ✓)
...

检测到：Claude Code
```

### 监控流程

```
启动监控
  ↓
每 5 分钟检查一次
  ↓
检查 4 个触发条件
  ↓
任意条件满足？
  ├─ 是 → 备份 → 重置计数器 → 继续
  └─ 否 → 继续
```

### 模型切换流程

```
检测到模型切换
  ↓
备份旧模型数据
  ↓
恢复到新模型
  ↓
创建通知
  ↓
新模型读取通知
  ↓
继续对话
```

## 🔧 配置

### 环境变量

```bash
# 指定 AI 工具（不设置则自动检测）
export AI_TOOL=cursor

# 触发阈值
export BACKUP_TIME_HOURS=2
export BACKUP_MESSAGE_THRESHOLD=200
export BACKUP_TASK_THRESHOLD=5

# 保留 N 个备份
export KEEP_BACKUPS=2

# 模型切换时自动恢复
export AUTO_RESTORE=true
```

### 配置文件

创建 `~/.ai-backup/config.json`：

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

## 🎯 使用场景

### 场景 1：频繁切换模型

```bash
# 系统自动监控
# 切换模型 → 自动备份和恢复
# 无缝过渡
```

### 场景 2：长对话保护

```bash
# 新增 200 条消息 → 自动备份
# 防止意外丢失
```

### 场景 3：项目开发

```bash
# 完成 5 个任务 → 自动备份
# 保护开发进度
```

## 📝 AI 工具特定说明

### Claude Code

- ✅ 完全支持
- ✅ 模型切换检测
- ✅ 项目会话
- ✅ Agents、Rules、Skills

### Cursor

- ✅ 完全支持
- ✅ 模型切换检测
- ✅ 工作区状态
- ⚠️ 需要 Cursor 0.30+

### Windsurf

- ✅ 完全支持
- ✅ 模型切换检测
- ✅ 对话历史

### Cline（VS Code）

- ✅ 任务历史备份
- ❌ 无模型切换检测
- ⚠️ 扩展特定

### Continue

- ✅ 完全支持
- ✅ 模型切换检测
- ✅ 会话历史

### Aider

- ✅ 聊天历史备份
- ✅ 模型切换检测
- ✅ 配置文件备份

### GitHub Copilot Workspace

- ✅ 工作区历史
- ❌ 无模型切换检测

### Cody（Sourcegraph）

- ✅ 完全支持
- ✅ 模型切换检测

### Tabnine

- ✅ 配置备份
- ❌ 无模型切换检测

### Amazon Q Developer

- ✅ 对话备份
- ❌ 无模型切换检测

## 🎓 高级用法

### 守护进程模式（systemd）

```bash
# 安装为 systemd 服务
./install.sh --daemon

# 管理服务
systemctl --user status ai-backup-monitor
systemctl --user restart ai-backup-monitor
journalctl --user -u ai-backup-monitor -f
```

### Cron 模式

```bash
# 每 10 分钟检查一次
./install.sh --cron
```

### 手动模式

```bash
# 完全手动控制
python3 monitor.py --check
```

## 📊 性能

- **CPU**：~0%（每 5 分钟检查一次）
- **内存**：~10MB（Python 进程）
- **磁盘**：每次备份 5-10MB

## 🔍 故障排除

### 问题 1：工具未检测到

```bash
# 列出检测到的工具
python3 monitor.py --list-tools

# 手动指定
export AI_TOOL=cursor
python3 monitor.py --status
```

### 问题 2：备份未触发

```bash
# 检查状态
python3 monitor.py --status

# 降低阈值
export BACKUP_MESSAGE_THRESHOLD=50
```

### 问题 3：模型切换未检测

```bash
# 检查工具是否支持
python3 monitor.py --list-tools

# 验证设置文件存在
ls -la ~/.cursor/settings.json  # 或你的工具配置
```

## 🤝 贡献

欢迎贡献！请：

1. Fork 仓库
2. 创建功能分支
3. 添加你的 AI 工具支持
4. 提交 Pull Request

### 添加新的 AI 工具

编辑 `monitor.py` 并添加到 `AIToolConfig.TOOLS`：

```python
"your-tool": {
    "name": "你的工具",
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

## 📄 许可证

MIT 许可证 - 查看 [LICENSE](LICENSE)

## 🙏 致谢

- 灵感来源于频繁切换模型的需求
- 感谢所有 AI 工具开发者
- 社区反馈和贡献

## 📚 相关项目

- [claude-backup](https://github.com/twilligon/claude-backup)
- [claude-conversation-extractor](https://github.com/ZeroSumQuant/claude-conversation-extractor)
- [claude-code-sync](https://github.com/perfectra1n/claude-code-sync)

## 🎯 路线图

- [ ] Web 管理界面
- [ ] 远程备份（S3、Google Drive）
- [ ] 备份加密
- [ ] 多用户支持
- [ ] 备份压缩
- [ ] 自定义触发条件
- [ ] Slack/Discord 通知

## 📧 联系

问题反馈：[GitHub Issues](https://github.com/Yizebaba/claude-smart-backup/issues)

---

**⭐ 如果这个项目对你有帮助，请给个 Star！**

---

## 🌐 其他语言

- [English](README.md)
- [日本語](README.ja.md)
- [한국어](README.ko.md)
- [Русский](README.ru.md)
- [Español](README.es.md)
- [Français](README.fr.md)
- [Deutsch](README.de.md)
- [Português](README.pt.md)

## 📦 VS Code 扩展

从 VS Code Marketplace 直接安装：

```bash
code --install-extension yizebaba.ai-chat-backup
```

查看 [VS Code 扩展指南](docs/VSCODE_EXTENSION.md) 了解详情。
