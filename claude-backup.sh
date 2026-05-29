#!/usr/bin/env bash
# Claude Code 自动备份脚本 - 保持最近 N 次备份，自动轮转
#
# 功能：
# 1. 备份聊天记录 (history.jsonl)
# 2. 备份项目会话 (projects/)
# 3. 备份配置文件 (settings.json, agents/, rules/, skills/)
# 4. 保持最近 N 次备份，自动删除旧的
# 5. 支持定时自动备份（通过 cron）

set -euo pipefail

# ============================================================
# 配置区域
# ============================================================

# 备份保留数量（默认保留最近 2 次）
KEEP_BACKUPS=${KEEP_BACKUPS:-2}

# 备份目录
CLAUDE_DIR="${HOME}/.claude"
BACKUP_ROOT="${HOME}/.claude-backups"

# 时间戳格式
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# 当前备份目录
BACKUP_DIR="${BACKUP_ROOT}/backup_${TIMESTAMP}"

# 日志（先创建目录）
mkdir -p "${BACKUP_ROOT}"
LOG_FILE="${BACKUP_ROOT}/backup.log"

# ============================================================
# 函数定义
# ============================================================

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "${LOG_FILE}"
}

# 创建备份目录
init_backup_dir() {
    mkdir -p "${BACKUP_DIR}"
    mkdir -p "${BACKUP_ROOT}"
    log "📦 创建备份目录: ${BACKUP_DIR}"
}

# 备份聊天记录
backup_history() {
    if [ -f "${CLAUDE_DIR}/history.jsonl" ]; then
        cp "${CLAUDE_DIR}/history.jsonl" "${BACKUP_DIR}/history.jsonl"
        local size=$(du -h "${CLAUDE_DIR}/history.jsonl" | cut -f1)
        log "✅ 备份聊天记录: ${size}"
    else
        log "⚠️  聊天记录不存在"
    fi
}

# 备份项目会话
backup_projects() {
    if [ -d "${CLAUDE_DIR}/projects" ]; then
        cp -r "${CLAUDE_DIR}/projects" "${BACKUP_DIR}/projects"
        local size=$(du -sh "${CLAUDE_DIR}/projects" | cut -f1)
        log "✅ 备份项目会话: ${size}"
    else
        log "⚠️  项目会话目录不存在"
    fi
}

# 备份配置文件
backup_config() {
    # settings.json
    if [ -f "${CLAUDE_DIR}/settings.json" ]; then
        cp "${CLAUDE_DIR}/settings.json" "${BACKUP_DIR}/settings.json"
        log "✅ 备份配置文件: settings.json"
    fi

    # agents
    if [ -d "${CLAUDE_DIR}/agents" ]; then
        mkdir -p "${BACKUP_DIR}/agents"
        cp -r "${CLAUDE_DIR}/agents"/*.md "${BACKUP_DIR}/agents/" 2>/dev/null || true
        local count=$(ls -1 "${BACKUP_DIR}/agents"/*.md 2>/dev/null | wc -l)
        log "✅ 备份 agents: ${count} 个"
    fi

    # rules
    if [ -d "${CLAUDE_DIR}/rules" ]; then
        cp -r "${CLAUDE_DIR}/rules" "${BACKUP_DIR}/rules"
        log "✅ 备份 rules"
    fi

    # skills
    if [ -d "${CLAUDE_DIR}/skills" ]; then
        cp -r "${CLAUDE_DIR}/skills" "${BACKUP_DIR}/skills"
        log "✅ 备份 skills"
    fi
}

# 清理旧备份（保留最近 N 次）
cleanup_old_backups() {
    log "🧹 清理旧备份（保留最近 ${KEEP_BACKUPS} 次）"

    # 列出所有备份目录，按时间排序
    local backups=($(ls -1dt "${BACKUP_ROOT}"/backup_* 2>/dev/null || true))
    local total=${#backups[@]}

    if [ ${total} -le ${KEEP_BACKUPS} ]; then
        log "📊 当前备份数: ${total}，无需清理"
        return
    fi

    # 删除多余的备份
    local to_delete=$((total - KEEP_BACKUPS))
    log "📊 当前备份数: ${total}，需要删除: ${to_delete} 个"

    for ((i=KEEP_BACKUPS; i<total; i++)); do
        local old_backup="${backups[$i]}"
        log "🗑️  删除旧备份: $(basename ${old_backup})"
        rm -rf "${old_backup}"
    done
}

# 生成备份摘要
generate_summary() {
    local backup_size=$(du -sh "${BACKUP_DIR}" | cut -f1)
    local total_size=$(du -sh "${BACKUP_ROOT}" | cut -f1)

    cat > "${BACKUP_DIR}/BACKUP_INFO.txt" <<EOF
备份时间: ${TIMESTAMP}
备份大小: ${backup_size}
总备份大小: ${total_size}
保留策略: 最近 ${KEEP_BACKUPS} 次

备份内容:
- 聊天记录 (history.jsonl)
- 项目会话 (projects/)
- 配置文件 (settings.json)
- Agents (agents/*.md)
- Rules (rules/)
- Skills (skills/)

恢复方法:
  cp -r ${BACKUP_DIR}/* ~/.claude/
EOF

    log "📄 生成备份摘要"
}

# 显示统计信息
show_stats() {
    log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log "📊 备份统计"
    log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    local backup_size=$(du -sh "${BACKUP_DIR}" | cut -f1)
    local total_size=$(du -sh "${BACKUP_ROOT}" | cut -f1)
    local backup_count=$(ls -1d "${BACKUP_ROOT}"/backup_* 2>/dev/null | wc -l)

    log "本次备份大小: ${backup_size}"
    log "总备份大小: ${total_size}"
    log "备份数量: ${backup_count}"
    log "备份位置: ${BACKUP_DIR}"
    log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# ============================================================
# 主流程
# ============================================================

main() {
    log "🚀 开始备份 Claude Code"

    # 检查 Claude 目录
    if [ ! -d "${CLAUDE_DIR}" ]; then
        log "❌ Claude 目录不存在: ${CLAUDE_DIR}"
        exit 1
    fi

    # 创建备份目录
    init_backup_dir

    # 执行备份
    backup_history
    backup_projects
    backup_config

    # 生成摘要
    generate_summary

    # 清理旧备份
    cleanup_old_backups

    # 显示统计
    show_stats

    log "✅ 备份完成！"
}

# 运行主流程
main "$@"
