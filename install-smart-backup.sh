#!/usr/bin/env bash
# 智能备份系统 - 一键安装

set -euo pipefail

echo "🎯 Claude Code 智能备份系统 - 安装向导"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "智能触发条件（任意一个满足即备份）："
echo "  1. ⏰ 时间：每 2 小时"
echo "  2. 💬 消息：新增 50 条消息"
echo "  3. ✅ 任务：完成 5 个任务"
echo "  4. 🔄 模型：检测到模型切换"
echo ""
echo "备份后自动重置所有计数器，从头开始计算"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 需要 Python 3"
    exit 1
fi

# 检查备份脚本
if [ ! -f ~/claude-backup.sh ]; then
    echo "❌ 备份脚本不存在: ~/claude-backup.sh"
    exit 1
fi

echo "✅ 环境检查通过"
echo ""

# 选择运行模式
echo "请选择运行模式："
echo ""
echo "1) 守护进程模式（推荐）"
echo "   - 后台持续运行"
echo "   - 每 5 分钟检查一次"
echo "   - 自动触发备份"
echo ""
echo "2) Cron 定时检查"
echo "   - 每 10 分钟检查一次"
echo "   - 轻量级，不占用资源"
echo ""
echo "3) 手动模式"
echo "   - 需要手动运行检查"
echo "   - 完全可控"
echo ""

read -p "请选择 (1/2/3): " mode

case $mode in
    1)
        echo ""
        echo "✅ 已选择：守护进程模式"
        echo ""

        # 创建 systemd service
        SERVICE_FILE=~/.config/systemd/user/claude-backup-monitor.service

        mkdir -p ~/.config/systemd/user

        cat > "${SERVICE_FILE}" <<EOF
[Unit]
Description=Claude Code Smart Backup Monitor
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 ${HOME}/smart-backup-monitor.py --daemon
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
EOF

        # 启用服务
        systemctl --user daemon-reload
        systemctl --user enable claude-backup-monitor.service
        systemctl --user start claude-backup-monitor.service

        echo "✅ 守护进程已启动！"
        echo ""
        echo "管理命令："
        echo "  查看状态: systemctl --user status claude-backup-monitor"
        echo "  查看日志: journalctl --user -u claude-backup-monitor -f"
        echo "  停止服务: systemctl --user stop claude-backup-monitor"
        echo "  重启服务: systemctl --user restart claude-backup-monitor"
        ;;

    2)
        echo ""
        echo "✅ 已选择：Cron 定时检查"
        echo ""

        CRON_JOB="*/10 * * * * /usr/bin/python3 ${HOME}/smart-backup-monitor.py --check >> ${HOME}/.claude-backups/monitor.log 2>&1"

        if crontab -l 2>/dev/null | grep -q "smart-backup-monitor.py"; then
            echo "⚠️  检测到已存在的监控任务，将先删除"
            crontab -l 2>/dev/null | grep -v "smart-backup-monitor.py" | crontab -
        fi

        (crontab -l 2>/dev/null; echo "${CRON_JOB}") | crontab -

        echo "✅ Cron 任务已安装！"
        echo ""
        echo "管理命令："
        echo "  查看任务: crontab -l"
        echo "  查看日志: tail -f ~/.claude-backups/monitor.log"
        echo "  删除任务: crontab -e (删除包含 smart-backup-monitor.py 的行)"
        ;;

    3)
        echo ""
        echo "✅ 已选择：手动模式"
        echo ""
        echo "使用方法："
        echo "  检查一次: python3 ~/smart-backup-monitor.py --check"
        echo "  查看状态: python3 ~/smart-backup-monitor.py --status"
        echo "  重置计数: python3 ~/smart-backup-monitor.py --reset"
        echo ""
        echo "💡 建议添加别名到 ~/.bashrc:"
        echo "  alias backup-check='python3 ~/smart-backup-monitor.py --check'"
        echo "  alias backup-status='python3 ~/smart-backup-monitor.py --status'"
        ;;

    *)
        echo "❌ 无效选项"
        exit 1
        ;;
esac

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 通用命令"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  查看状态: python3 ~/smart-backup-monitor.py --status"
echo "  手动检查: python3 ~/smart-backup-monitor.py --check"
echo "  重置计数: python3 ~/smart-backup-monitor.py --reset"
echo "  查看备份: ls -lh ~/.claude-backups/"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🎉 安装完成！"
