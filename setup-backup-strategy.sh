#!/usr/bin/env bash
# Claude Code 智能备份策略 - 针对频繁换模型的用户
#
# 策略：
# 1. 保留最近 2 次备份（节省空间）
# 2. 触发时机：
#    - 手动触发（换模型前）
#    - 每天自动备份 1 次（凌晨 3 点）
#    - 可选：每次会话结束时备份（通过 hook）

set -euo pipefail

echo "🎯 Claude Code 智能备份策略配置"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "推荐策略（针对频繁换模型）："
echo ""
echo "1. 手动备份模式"
echo "   - 换模型前手动运行: ~/claude-backup.sh"
echo "   - 优点: 完全可控，只在需要时备份"
echo "   - 缺点: 需要记得手动执行"
echo ""
echo "2. 每日自动备份"
echo "   - 每天凌晨 3 点自动备份"
echo "   - 保留最近 2 次"
echo "   - 优点: 自动保护，不用担心忘记"
echo "   - 缺点: 可能备份时机不是最佳"
echo ""
echo "3. 混合模式（推荐）"
echo "   - 每天凌晨 3 点自动备份"
echo "   - 换模型前手动备份"
echo "   - 保留最近 2 次（自动删除旧的）"
echo "   - 优点: 既有自动保护，又可手动控制"
echo ""

read -p "请选择模式 (1/2/3): " mode

case $mode in
    1)
        echo ""
        echo "✅ 已选择：手动备份模式"
        echo ""
        echo "使用方法："
        echo "  换模型前: ~/claude-backup.sh"
        echo "  查看备份: ls -lh ~/.claude-backups/"
        echo ""
        echo "💡 提示：建议在 ~/.bashrc 添加别名："
        echo "  alias backup-claude='~/claude-backup.sh'"
        echo ""
        read -p "是否添加别名到 ~/.bashrc？(y/n): " add_alias
        if [ "$add_alias" = "y" ]; then
            echo "alias backup-claude='~/claude-backup.sh'" >> ~/.bashrc
            echo "✅ 别名已添加！重新加载 shell 后生效：source ~/.bashrc"
        fi
        ;;
    2)
        echo ""
        echo "✅ 已选择：每日自动备份"
        CRON_JOB="0 3 * * * KEEP_BACKUPS=2 ~/claude-backup.sh >> ~/.claude-backups/backup.log 2>&1"

        if crontab -l 2>/dev/null | grep -q "claude-backup.sh"; then
            echo "⚠️  检测到已存在的备份任务，将先删除"
            crontab -l 2>/dev/null | grep -v "claude-backup.sh" | crontab -
        fi

        (crontab -l 2>/dev/null; echo "${CRON_JOB}") | crontab -
        echo "✅ 定时任务已安装！"
        echo ""
        echo "配置："
        echo "  - 时间: 每天凌晨 3 点"
        echo "  - 保留: 最近 2 次"
        echo "  - 日志: ~/.claude-backups/backup.log"
        ;;
    3)
        echo ""
        echo "✅ 已选择：混合模式（推荐）"

        # 添加 cron 任务
        CRON_JOB="0 3 * * * KEEP_BACKUPS=2 ~/claude-backup.sh >> ~/.claude-backups/backup.log 2>&1"

        if crontab -l 2>/dev/null | grep -q "claude-backup.sh"; then
            echo "⚠️  检测到已存在的备份任务，将先删除"
            crontab -l 2>/dev/null | grep -v "claude-backup.sh" | crontab -
        fi

        (crontab -l 2>/dev/null; echo "${CRON_JOB}") | crontab -

        # 添加别名
        if ! grep -q "alias backup-claude" ~/.bashrc 2>/dev/null; then
            echo "alias backup-claude='~/claude-backup.sh'" >> ~/.bashrc
        fi

        echo "✅ 混合模式已配置！"
        echo ""
        echo "自动备份："
        echo "  - 时间: 每天凌晨 3 点"
        echo "  - 保留: 最近 2 次"
        echo ""
        echo "手动备份："
        echo "  - 命令: backup-claude"
        echo "  - 或: ~/claude-backup.sh"
        echo ""
        echo "💡 重新加载 shell: source ~/.bashrc"
        ;;
    *)
        echo "❌ 无效选项"
        exit 1
        ;;
esac

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 管理命令："
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  手动备份: ~/claude-backup.sh"
echo "  查看备份: ls -lh ~/.claude-backups/"
echo "  查看日志: tail -f ~/.claude-backups/backup.log"
echo "  恢复备份: cp -r ~/.claude-backups/backup_YYYYMMDD_HHMMSS/* ~/.claude/"
echo "  查看任务: crontab -l"
echo "  删除任务: crontab -e (删除包含 claude-backup.sh 的行)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
