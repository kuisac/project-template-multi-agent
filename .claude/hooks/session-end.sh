#!/usr/bin/env bash
# Hook Stop — exécuté à la fin d'une session Claude Code.

set -euo pipefail

DATE_ISO="$(date +%Y-%m-%dT%H:%M:%S)"

echo ""
echo "─────────────────────────────────────────────"
echo "  Fin de session — $DATE_ISO"
echo "─────────────────────────────────────────────"

if [[ -d doc/architecture ]]; then
  PROPOSED_COUNT=$(grep -l "Statut.*Proposé" doc/architecture/ADR-*.md 2>/dev/null | wc -l | tr -d ' ')
  if [[ "${PROPOSED_COUNT:-0}" -gt 0 ]]; then
    echo "  📋 $PROPOSED_COUNT ADR(s) en statut Proposé — à arbitrer."
  fi
fi

if [[ -d doc ]]; then
  TODO_COUNT=$(grep -rIc "TBD\|FIXME\|À compléter" doc/ 2>/dev/null | grep -v ":0$" | wc -l | tr -d ' ')
  if [[ "${TODO_COUNT:-0}" -gt 0 ]]; then
    echo "  📝 $TODO_COUNT fichier(s) de doc avec TBD/FIXME en attente."
  fi
fi

echo "  💡 Lance '/team-status' à ta prochaine session pour le diagnostic."
echo "─────────────────────────────────────────────"

exit 0
