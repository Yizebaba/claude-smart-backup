# Claude Smart Backup

🎯 智能备份系统 - 为 Claude Code 设计的多条件触发备份解决方案

## ✨ 特性

### 智能触发条件（任意一个满足即备份）

- ⏰ **时间触发** - 每 2 小时
- 💬 **消息触发** - 新增 200 条消息
- ✅ **任务触发** - 完成 5 个任务
- 🔄 **模型切换** - 自动检测并恢复

### 🔄 模型切换自动恢复

当检测到模型切换时，系统会自动：

1. **备份旧模型数据**
   - 聊天记录
   - 项目会话
   - 配置文件
   - Agents、Rules、Skills

2. **恢复到新模型**
   - 自动加载聊天记录
   - 自动恢复项目会话
   - 自动同步工具配置
   - 自动恢复 Agents、Rules、Skills

3. **创建通知文件**
   - 告知新模型已恢复的内容
   - 说明智能备份系统的功能

4. **重置计数器**
   - 所有计数器归零
   - 重新开始监控

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/claude-smart-backup.git
cd claude-smart-backup

# 一键安装
./install-smart-backup.sh
# 选择: 1) 守护进程模式（推荐）
```

### 使用

```bash
# 查看状态
python3 smart-backup-monitor.py --status

# 手动检查
python3 smart-backup-monitor.py --check

# 重置计数器
python3 smart-backup-monitor.py --reset
```

## 📊 工作原理

### 监控流程

```
启动监控
  ↓
每 5 分钟检查一次
  ↓
检查 4 个触发条件
  ↓
任意一个满足？
  ├─ 是 → 执行备份 → 重置计数器 → 继续监控
  └─ 否 → 继续监控
```

### 模型切换流程

```
检测到模型切换
  ↓
备份旧模型数据
  ↓
恢复到新模型
  ↓
创建通知文件
  ↓
新模型读取通知
  ↓
继续之前的对话
```

## 🎯 使用场景

### 场景 1: 频繁换模型

```bash
# 系统自动监控
# 换模型时自动备份和恢复
# 无缝切换，无需手动操作
```

### 场景 2: 长对话保护

```bash
# 新增 200 条消息时自动备份
# 防止意外丢失对话
```

### 场景 3: 项目开发

```bash
# 完成 5 个任务时自动备份
# 保护开发进度
```

## 🔧 配置

### 调整触发阈值

编辑 `smart-backup-monitor.py`：

```python
class BackupConfig:
    TIME_INTERVAL_HOURS = 2          # 时间间隔（小时）
    MESSAGE_THRESHOLD = 200          # 消息阈值
    TASK_THRESHOLD = 5               # 任务阈值
    KEEP_BACKUPS = 2                 # 保留备份数量
    AUTO_RESTORE_ON_MODEL_CHANGE = True  # 模型切换自动恢复
```

### 推荐配置

**频繁换模型用户**：
```python
TIME_INTERVAL_HOURS = 2
MESSAGE_THRESHOLD = 200
TASK_THRESHOLD = 5
KEEP_BACKUPS = 2
```

**普通用户**：
```python
TIME_INTERVAL_HOURS = 4
MESSAGE_THRESHOLD = 300
TASK_THRESHOLD = 10
KEEP_BACKUPS = 2
```

## 📝 文件说明

- `smart-backup-monitor.py` - 智能监控脚本（核心）
- `claude-backup.sh` - 备份执行脚本
- `install-smart-backup.sh` - 一键安装脚本
- `setup-backup-strategy.sh` - 策略配置脚本

## 🎓 高级功能

### 守护进程模式

```bash
# 使用 systemd（推荐）
./install-smart-backup.sh
# 选择: 1) 守护进程模式

# 管理命令
systemctl --user status claude-backup-monitor
systemctl --user restart claude-backup-monitor
journalctl --user -u claude-backup-monitor -f
```

### Cron 定时模式

```bash
# 每 10 分钟检查一次
./install-smart-backup.sh
# 选择: 2) Cron 定时检查
```

### 手动模式

```bash
# 完全手动控制
python3 smart-backup-monitor.py --check
```

## 📊 性能影响

- **CPU**: 几乎为 0（每 5 分钟检查一次）
- **内存**: ~10MB（Python 进程）
- **磁盘**: 每次备份 ~5-10MB

## 🔍 故障排除

### 问题 1: 守护进程未启动

```bash
systemctl --user status claude-backup-monitor
journalctl --user -u claude-backup-monitor -n 50
```

### 问题 2: 未触发备份

```bash
python3 smart-backup-monitor.py --status
# 检查触发条件是否合理
```

### 问题 3: 模型切换未检测

```bash
cat ~/.claude/settings.json
# 确保 model 字段存在
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 开发

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/claude-smart-backup.git
cd claude-smart-backup

# 测试
python3 smart-backup-monitor.py --status
python3 smart-backup-monitor.py --check
```

## 📄 许可证

MIT License

## 🙏 致谢

- 感谢 [Claude Code](https://claude.ai/code) 提供的强大 AI 编程工具
- 灵感来源于频繁换模型的实际需求

## 📚 相关项目

- [claude-backup](https://github.com/twilligon/claude-backup) - Claude.ai 聊天备份
- [claude-conversation-extractor](https://github.com/ZeroSumQuant/claude-conversation-extractor) - 对话提取工具
- [claude-code-sync](https://github.com/perfectra1n/claude-code-sync) - 跨机器同步

## 🎯 路线图

- [ ] 支持自定义触发条件
- [ ] 支持远程备份（S3、Google Drive）
- [ ] 支持备份加密
- [ ] 支持 Web 管理界面
- [ ] 支持多用户

## 📧 联系

如有问题或建议，请提交 [Issue](https://github.com/YOUR_USERNAME/claude-smart-backup/issues)

---

**⭐ 如果这个项目对你有帮助，请给个 Star！**
