#!/usr/bin/env bash
# Hook PostToolUse pour Write|Edit.
# Détecte des modifications sensibles et les signale dans le transcript.

set -euo pipefail

TARGET="${CLAUDE_TOOL_INPUT_PATH:-}"

if [[ -z "$TARGET" ]]; then
  exit 0
fi

# Alerte 1 — modification dans /doc/architecture/ qui ne suit pas le pattern ADR-NNN-*.md
if [[ "$TARGET" == doc/architecture/* ]]; then
  filename="$(basename "$TARGET")"
  if [[ ! "$filename" =~ ^ADR-[0-9]{3}-.+\.md$ ]] && [[ "$filename" != "threat-model.md" ]] && [[ "$filename" != "README.md" ]]; then
    echo "⚠️  Fichier dans doc/architecture/ qui ne suit pas la convention ADR-NNN-<slug>.md : $filename"
    echo "    → Pense à créer un vrai ADR via le template .claude/shared/templates/adr.md"
  fi
fi

# Alerte 2 — modification dans /src sans test associé visible
if [[ "$TARGET" == src/* ]]; then
  module="$(basename "$TARGET" | sed 's/\.[^.]*$//')"
  if ! grep -rq "$module" tests/ 2>/dev/null; then
    echo "⚠️  Modification dans $TARGET sans test associé évident pour le module '$module'."
    echo "    → Pilote, délègue à 'testor' pour vérifier la couverture."
  fi
fi

# Alerte 3 — ajout de dépendance dans package.json / requirements.txt / pyproject.toml etc.
case "$TARGET" in
  package.json|requirements.txt|pyproject.toml|Cargo.toml|go.mod|Gemfile)
    echo "⚠️  Modification de manifeste de dépendances ($TARGET)."
    echo "    → Pilote, délègue à 'sentinel' pour audit + 'archi' pour validation du choix."
    ;;
esac

exit 0
