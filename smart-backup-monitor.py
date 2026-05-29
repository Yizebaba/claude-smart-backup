#!/usr/bin/env python3
"""
Claude Code 智能备份系统 - 多条件触发

触发条件（任意一个满足即备份）：
1. 时间：每 2 小时
2. 聊天记录：新增 N 条消息
3. 项目进度：完成 N 个任务
4. 模型切换：检测到模型变化

满足任意条件后：
- 自动备份
- 重置计数器
- 继续监控
"""

import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

# ============================================================
# 配置区域
# ============================================================

class BackupConfig:
    # 备份脚本路径
    BACKUP_SCRIPT = Path.home() / "claude-backup.sh"

    # Claude 目录
    CLAUDE_DIR = Path.home() / ".claude"
    HISTORY_FILE = CLAUDE_DIR / "history.jsonl"
    SETTINGS_FILE = CLAUDE_DIR / "settings.json"

    # 状态文件（记录上次备份状态）
    STATE_FILE = Path.home() / ".claude-backups" / "backup_state.json"

    # 触发条件
    TIME_INTERVAL_HOURS = 2          # 每 2 小时
    MESSAGE_THRESHOLD = 200          # 新增 200 条消息
    TASK_THRESHOLD = 5               # 完成 5 个任务

    # 保留备份数量
    KEEP_BACKUPS = 2

    # 模型切换后自动恢复
    AUTO_RESTORE_ON_MODEL_CHANGE = True


# ============================================================
# 状态管理
# ============================================================

class BackupState:
    def __init__(self):
        self.state_file = BackupConfig.STATE_FILE
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state = self._load_state()

    def _load_state(self) -> Dict:
        """加载状态"""
        if self.state_file.exists():
            try:
                return json.loads(self.state_file.read_text())
            except:
                pass
        return self._default_state()

    def _default_state(self) -> Dict:
        """默认状态"""
        return {
            "last_backup_time": 0,
            "last_message_count": 0,
            "last_task_count": 0,
            "last_model": None,
            "total_backups": 0,
        }

    def save(self):
        """保存状态"""
        self.state_file.write_text(json.dumps(self.state, indent=2))

    def reset_counters(self):
        """重置计数器（备份后调用）"""
        self.state["last_backup_time"] = time.time()
        self.state["last_message_count"] = self._get_current_message_count()
        self.state["last_task_count"] = 0  # 任务计数需要外部传入
        self.state["last_model"] = self._get_current_model()
        self.state["total_backups"] += 1
        self.save()

    def _get_current_message_count(self) -> int:
        """获取当前消息数量"""
        try:
            if BackupConfig.HISTORY_FILE.exists():
                return sum(1 for _ in open(BackupConfig.HISTORY_FILE))
            return 0
        except:
            return 0

    def _get_current_model(self) -> Optional[str]:
        """获取当前模型"""
        try:
            if BackupConfig.SETTINGS_FILE.exists():
                settings = json.loads(BackupConfig.SETTINGS_FILE.read_text())
                return settings.get("model")
            return None
        except:
            return None


# ============================================================
# 触发条件检查
# ============================================================

class TriggerChecker:
    def __init__(self, state: BackupState):
        self.state = state

    def check_time_trigger(self) -> tuple[bool, str]:
        """检查时间触发"""
        elapsed_hours = (time.time() - self.state.state["last_backup_time"]) / 3600
        if elapsed_hours >= BackupConfig.TIME_INTERVAL_HOURS:
            return True, f"时间触发：已过 {elapsed_hours:.1f} 小时"
        return False, ""

    def check_message_trigger(self) -> tuple[bool, str]:
        """检查消息数量触发"""
        current_count = self.state._get_current_message_count()
        last_count = self.state.state["last_message_count"]
        new_messages = current_count - last_count

        if new_messages >= BackupConfig.MESSAGE_THRESHOLD:
            return True, f"消息触发：新增 {new_messages} 条消息"
        return False, ""

    def check_task_trigger(self, completed_tasks: int) -> tuple[bool, str]:
        """检查任务完成触发"""
        if completed_tasks >= BackupConfig.TASK_THRESHOLD:
            return True, f"任务触发：完成 {completed_tasks} 个任务"
        return False, ""

    def check_model_trigger(self) -> tuple[bool, str]:
        """检查模型切换触发"""
        current_model = self.state._get_current_model()
        last_model = self.state.state["last_model"]

        if last_model and current_model and current_model != last_model:
            return True, f"模型切换：{last_model} → {current_model}"
        return False, ""

    def check_all_triggers(self, completed_tasks: int = 0) -> tuple[bool, list[str]]:
        """检查所有触发条件"""
        triggers = []

        # 检查各个条件
        checks = [
            self.check_time_trigger(),
            self.check_message_trigger(),
            self.check_task_trigger(completed_tasks),
            self.check_model_trigger(),
        ]

        for triggered, reason in checks:
            if triggered:
                triggers.append(reason)

        return len(triggers) > 0, triggers


# ============================================================
# 备份执行
# ============================================================

class BackupExecutor:
    @staticmethod
    def run_backup() -> bool:
        """执行备份"""
        try:
            env = os.environ.copy()
            env["KEEP_BACKUPS"] = str(BackupConfig.KEEP_BACKUPS)

            result = subprocess.run(
                [str(BackupConfig.BACKUP_SCRIPT)],
                env=env,
                capture_output=True,
                text=True,
                timeout=60,
            )

            return result.returncode == 0
        except Exception as e:
            print(f"❌ 备份失败: {e}")
            return False

    @staticmethod
    def restore_latest_backup() -> bool:
        """恢复最新备份"""
        try:
            backup_root = Path.home() / ".claude-backups"
            backups = sorted(backup_root.glob("backup_*"), reverse=True)

            if not backups:
                print("❌ 没有可用的备份")
                return False

            latest_backup = backups[0]
            claude_dir = BackupConfig.CLAUDE_DIR

            print(f"📦 恢复备份: {latest_backup.name}")

            # 恢复聊天记录
            history_src = latest_backup / "history.jsonl"
            if history_src.exists():
                import shutil
                shutil.copy2(history_src, claude_dir / "history.jsonl")
                print("  ✅ 聊天记录已恢复")

            # 恢复项目会话
            projects_src = latest_backup / "projects"
            if projects_src.exists():
                import shutil
                projects_dst = claude_dir / "projects"
                if projects_dst.exists():
                    shutil.rmtree(projects_dst)
                shutil.copytree(projects_src, projects_dst)
                print("  ✅ 项目会话已恢复")

            # 恢复配置
            settings_src = latest_backup / "settings.json"
            if settings_src.exists():
                import shutil
                shutil.copy2(settings_src, claude_dir / "settings.json")
                print("  ✅ 配置文件已恢复")

            # 恢复 agents
            agents_src = latest_backup / "agents"
            if agents_src.exists():
                import shutil
                agents_dst = claude_dir / "agents"
                for agent_file in agents_src.glob("*.md"):
                    shutil.copy2(agent_file, agents_dst / agent_file.name)
                print("  ✅ Agents 已恢复")

            # 恢复 rules
            rules_src = latest_backup / "rules"
            if rules_src.exists():
                import shutil
                rules_dst = claude_dir / "rules"
                if rules_dst.exists():
                    shutil.rmtree(rules_dst)
                shutil.copytree(rules_src, rules_dst)
                print("  ✅ Rules 已恢复")

            # 恢复 skills
            skills_src = latest_backup / "skills"
            if skills_src.exists():
                import shutil
                skills_dst = claude_dir / "skills"
                if skills_dst.exists():
                    shutil.rmtree(skills_dst)
                shutil.copytree(skills_src, skills_dst)
                print("  ✅ Skills 已恢复")

            return True
        except Exception as e:
            print(f"❌ 恢复失败: {e}")
            return False

    @staticmethod
    def create_model_change_notice(old_model: str, new_model: str) -> str:
        """创建模型切换通知文件"""
        notice = f"""# 🔄 模型切换通知

检测到模型切换：
- 旧模型: {old_model}
- 新模型: {new_model}
- 切换时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## ✅ 已自动执行的操作

1. **备份旧模型数据**
   - 聊天记录
   - 项目会话
   - 配置文件
   - Agents、Rules、Skills

2. **恢复到新模型**
   - 聊天记录已加载
   - 项目会话已恢复
   - 工具配置已同步
   - Agents、Rules、Skills 已恢复

## 📊 智能备份系统说明

你现在使用的是**智能自动备份系统**，具有以下功能：

### 触发条件（任意一个满足即备份）
- ⏰ 时间：每 2 小时
- 💬 消息：新增 200 条消息
- ✅ 任务：完成 5 个任务
- 🔄 模型切换：自动检测并备份

### 自动恢复机制
- 模型切换时自动备份旧数据
- 自动恢复聊天记录到新模型
- 自动恢复项目会话
- 自动恢复工具和配置

### 管理命令
- 查看状态: `python3 ~/smart-backup-monitor.py --status`
- 手动备份: `python3 ~/smart-backup-monitor.py --check`
- 查看备份: `ls -lh ~/.claude-backups/`

## 💡 提示

你可以继续之前的对话，所有上下文都已恢复。
"""
        notice_file = Path.home() / ".claude" / "MODEL_CHANGE_NOTICE.md"
        notice_file.write_text(notice)
        return str(notice_file)


# ============================================================
# 主监控循环
# ============================================================

class BackupMonitor:
    def __init__(self):
        self.state = BackupState()
        self.checker = TriggerChecker(self.state)
        self.executor = BackupExecutor()

    def log(self, *args):
        """日志输出"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}]", *args, flush=True)

    def run_once(self, completed_tasks: int = 0):
        """运行一次检查"""
        # 检查模型切换
        model_changed, model_reason = self.checker.check_model_trigger()

        if model_changed and BackupConfig.AUTO_RESTORE_ON_MODEL_CHANGE:
            self.log("🔄 检测到模型切换！")
            self.log(f"  - {model_reason}")

            # 先备份旧模型数据
            self.log("📦 备份旧模型数据...")
            if self.executor.run_backup():
                self.log("✅ 旧模型数据已备份")

                # 恢复到新模型
                self.log("🔄 恢复数据到新模型...")
                if self.executor.restore_latest_backup():
                    self.log("✅ 数据已恢复到新模型")

                    # 创建通知文件
                    old_model = self.state.state["last_model"]
                    new_model = self.state._get_current_model()
                    notice_file = self.executor.create_model_change_notice(old_model, new_model)
                    self.log(f"📄 已创建模型切换通知: {notice_file}")
                    self.log("💡 新模型已加载所有上下文，可以继续之前的对话")
                else:
                    self.log("❌ 数据恢复失败")

                self.state.reset_counters()
                self.log("🔄 计数器已重置")
            else:
                self.log("❌ 备份失败")
            return

        # 检查其他触发条件
        triggered, reasons = self.checker.check_all_triggers(completed_tasks)

        if triggered:
            self.log("🔔 触发备份条件:")
            for reason in reasons:
                self.log(f"  - {reason}")

            self.log("🚀 开始备份...")
            if self.executor.run_backup():
                self.log("✅ 备份成功")
                self.state.reset_counters()
                self.log("🔄 计数器已重置")
            else:
                self.log("❌ 备份失败")
        else:
            self.log("⏳ 未触发备份条件")

    def run_daemon(self, check_interval: int = 300):
        """守护进程模式（每 5 分钟检查一次）"""
        self.log("🎯 智能备份监控已启动")
        self.log(f"检查间隔: {check_interval} 秒")
        self.log(f"触发条件:")
        self.log(f"  - 时间: 每 {BackupConfig.TIME_INTERVAL_HOURS} 小时")
        self.log(f"  - 消息: 新增 {BackupConfig.MESSAGE_THRESHOLD} 条")
        self.log(f"  - 任务: 完成 {BackupConfig.TASK_THRESHOLD} 个")
        self.log(f"  - 模型切换: 自动检测并恢复")
        self.log(f"自动恢复: {'启用' if BackupConfig.AUTO_RESTORE_ON_MODEL_CHANGE else '禁用'}")
        self.log("")

        try:
            while True:
                self.run_once()
                time.sleep(check_interval)
        except KeyboardInterrupt:
            self.log("⏹️  监控已停止")


# ============================================================
# 命令行接口
# ============================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Claude Code 智能备份监控")
    parser.add_argument("--daemon", action="store_true", help="守护进程模式")
    parser.add_argument("--check", action="store_true", help="检查一次")
    parser.add_argument("--status", action="store_true", help="显示状态")
    parser.add_argument("--reset", action="store_true", help="重置计数器")
    parser.add_argument("--tasks", type=int, default=0, help="已完成任务数")

    args = parser.parse_args()

    monitor = BackupMonitor()

    if args.status:
        # 显示状态
        state = monitor.state.state
        print("📊 当前状态:")
        print(f"  上次备份: {datetime.fromtimestamp(state['last_backup_time']).strftime('%Y-%m-%d %H:%M:%S') if state['last_backup_time'] else '从未备份'}")
        print(f"  消息数量: {monitor.state._get_current_message_count()} (上次: {state['last_message_count']})")
        print(f"  当前模型: {monitor.state._get_current_model()}")
        print(f"  总备份次数: {state['total_backups']}")

    elif args.reset:
        # 重置计数器
        monitor.state.reset_counters()
        print("✅ 计数器已重置")

    elif args.check:
        # 检查一次
        monitor.run_once(args.tasks)

    elif args.daemon:
        # 守护进程模式
        monitor.run_daemon()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
