#!/usr/bin/env bash
# Hook SubagentStop — journalise la fin d'un sub-agent dans runtime/.

set -euo pipefail

LOG_DIR="runtime/agent-logs"
mkdir -p "$LOG_DIR"

DATE_ISO="$(date +%Y-%m-%dT%H:%M:%S)"
LOG_FILE="$LOG_DIR/subagent-$(date +%Y-%m-%d).log"

AGENT_NAME="${CLAUDE_SUBAGENT_NAME:-unknown}"
SESSION_ID="${CLAUDE_SESSION_ID:-unknown}"

echo "[$DATE_ISO] subagent=$AGENT_NAME session=$SESSION_ID stopped" >> "$LOG_FILE"
echo "✓ Sub-agent '$AGENT_NAME' a terminé. Log: $LOG_FILE"
