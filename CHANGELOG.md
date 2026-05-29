# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-05-30

### Added
- 智能触发备份系统
  - 时间触发（每 2 小时）
  - 消息触发（新增 200 条）
  - 任务触发（完成 5 个）
  - 模型切换触发
- 模型切换自动恢复功能
  - 自动备份旧模型数据
  - 自动恢复到新模型
  - 自动加载聊天记录、项目、工具配置
  - 创建通知文件告知新模型
- 自动重置机制
  - 备份后所有计数器归零
- 三种运行模式
  - 守护进程模式（systemd）
  - Cron 定时模式
  - 手动模式
- 完整的安装脚本
  - 一键安装
  - 交互式配置
- 状态管理
  - 查看当前状态
  - 手动重置计数器

### Features
- 基于实际工作进度的智能备份
- 模型切换无缝衔接
- 完全自动化，无需手动操作
- 资源占用极低
- 支持自定义配置

### Documentation
- 完整的 README
- 详细的配置说明
- 故障排除指南

## [2.0.0] - 2026-05-30

### 🎉 Major Update: Universal AI Tool Support

#### Added
- **Multi-tool support**: 10+ AI coding assistants
  - Claude Code
  - Cursor
  - Windsurf
  - Cline (VS Code)
  - Continue
  - Aider
  - GitHub Copilot Workspace
  - Cody (Sourcegraph)
  - Tabnine
  - Amazon Q Developer

- **Cross-platform support**
  - Linux (all distributions)
  - macOS (Intel & Apple Silicon)
  - Windows (Native & WSL)

- **Auto-detection**
  - Automatically detect which AI tool is being used
  - Platform-specific path resolution
  - Graceful fallback

#### Changed
- Renamed `smart-backup-monitor.py` to `monitor.py`
- Generalized configuration system
- Updated README with multi-tool documentation

#### Breaking Changes
- Configuration file location changed to `~/.ai-backup/`
- Environment variable `AI_TOOL` for manual tool selection

### Migration Guide

If upgrading from v1.x:

```bash
# Backup old state
cp ~/.claude-backups/backup_state.json ~/.ai-backup/state.json

# Update environment
export AI_TOOL=claude-code
```
