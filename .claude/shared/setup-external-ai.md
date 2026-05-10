# Setup des agents IA externes

Ce guide couvre l'activation de **Gepetto** (GPT), **Perci** (Perplexity) et **Gemina** (Gemini).
Configuration unique par poste de travail — les clés ne sont jamais commitées.

---

## Principe général

Les clés API sont stockées dans `.claude/settings.local.json` (gitignore).
Claude Code les injecte comme variables d'environnement au démarrage des serveurs MCP.

```
.mcp.json               ← déclaration des serveurs (versionné)
.claude/settings.local.json  ← clés API locales (gitignore, à créer par chaque dev)
```

**Après chaque modification de `settings.local.json` → redémarrer VS Code.**

---

## Prérequis communs

| Outil | Version minimale | Vérification |
|-------|-----------------|--------------|
| Python | 3.11+ | `python --version` |
| pip | — | `pip --version` |
| Node.js | 18+ | `node --version` |
| npx | inclus Node.js | `npx --version` |

---

## 1. Gepetto — OpenAI / GPT

**Rôle** : second avis algorithmique, contradicteur ou constructeur selon brief.
**Modèle par défaut** : `gpt-4.1` (configurable via `GEPETTO_MODEL`).

### Étape 1 — Obtenir la clé OpenAI

1. Aller sur [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Créer une clé → copier `sk-proj-...`

### Étape 2 — Installer les dépendances Python

```powershell
pip install -r .claude/OtherAI/gpt/requirements.txt
```

Contenu installé : `openai>=1.78.0`, `mcp>=1.9.0`

### Étape 3 — Renseigner la clé

Ouvrir `.claude/settings.local.json` et remplacer la valeur :

```json
"OPENAI_API_KEY": "sk-proj-VOTRE-CLE-ICI"
```

### Étape 4 — Changer le modèle (optionnel)

Pour utiliser un modèle différent de `gpt-4.1` :

```json
"GEPETTO_MODEL": "gpt-4o"
```

### Étape 5 — Redémarrer VS Code, puis tester

Dans Claude Code, demander :

> Utilise `ask_gepetto` pour me répondre "Gepetto opérationnel" avec le nom du modèle.

**En cas d'erreur `401`** : clé incorrecte ou non chargée → vérifier `settings.local.json` et redémarrer.
**En cas d'erreur `module not found`** : relancer `pip install -r .claude/OtherAI/gpt/requirements.txt`.

---

## 2. Perci — Perplexity

**Rôle** : recherche web sourcée, veille techno, CVE.
**Serveur MCP** : officiel Perplexity (`@perplexity-ai/mcp-server`), lancé via `npx` — pas d'installation manuelle.

### Étape 1 — Obtenir la clé Perplexity

1. Aller sur [perplexity.ai/settings/api](https://www.perplexity.ai/settings/api)
2. Créer une clé → copier `pplx-...`

### Étape 2 — Renseigner la clé

Ouvrir `.claude/settings.local.json` et remplacer :

```json
"PERPLEXITY_API_KEY": "pplx-VOTRE-CLE-ICI"
```

### Étape 3 — Redémarrer VS Code, puis tester

Dans Claude Code, demander :

> Via Perci (Perplexity MCP), cherche la version stable actuelle de Python.

**En cas d'erreur `npx` introuvable** : Node.js n'est pas installé ou pas dans le PATH.
**En cas d'erreur `401`** : clé incorrecte ou non chargée.

---

## 3. Gemina — Google Gemini

**Rôle** : analyse de gros corpus (jusqu'à 1M tokens), synthèse multi-documents.
**Serveur MCP** : pont Composio (`@composio/mcp gemini`).
**Statut** : désactivé par défaut dans `.mcp.json` (`"disabled": true`).

### Étape 1 — Obtenir la clé Gemini

1. Aller sur [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Créer une clé → copier la valeur

### Étape 2 — Obtenir la clé Composio

1. Aller sur [app.composio.dev](https://app.composio.dev) → Settings → API Keys
2. Créer une clé → copier la valeur

### Étape 3 — Renseigner les clés

Ouvrir `.claude/settings.local.json` et remplacer :

```json
"GEMINI_API_KEY": "VOTRE-CLE-GEMINI-ICI",
"COMPOSIO_API_KEY": "VOTRE-CLE-COMPOSIO-ICI"
```

### Étape 4 — Activer le serveur dans `.mcp.json`

Retirer la ligne `"disabled": true` du bloc `gemini-bridge` :

```json
"gemini-bridge": {
  "//": "Gemina — pont vers Google Gemini.",
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "@composio/mcp", "gemini"],
  "env": {
    "COMPOSIO_API_KEY": "${COMPOSIO_API_KEY}",
    "GEMINI_API_KEY": "${GEMINI_API_KEY}"
  }
}
```

### Étape 5 — Redémarrer VS Code, puis tester

Dans Claude Code, demander :

> Via Gemina (Gemini MCP), confirme que tu es opérationnel et indique le modèle utilisé.

**En cas d'erreur de connexion Composio** : vérifier que le compte Composio est actif et que la clé est correcte.

---

## Résumé des clés à configurer

| Agent | Variable | Source |
|-------|----------|--------|
| Gepetto (GPT) | `OPENAI_API_KEY` | platform.openai.com/api-keys |
| Gepetto (modèle optionnel) | `GEPETTO_MODEL` | — valeur ex. `gpt-4o` |
| Perci (Perplexity) | `PERPLEXITY_API_KEY` | perplexity.ai/settings/api |
| Gemina (Gemini) | `GEMINI_API_KEY` | aistudio.google.com/apikey |
| Gemina (Composio) | `COMPOSIO_API_KEY` | app.composio.dev |

---

## Sécurité

- `.claude/settings.local.json` est dans `.gitignore` — il ne sera jamais commité.
- Ne jamais coller une clé API dans le chat, un commit, ou un fichier versionné.
- En cas d'exposition accidentelle : **régénérer la clé immédiatement** sur le portail concerné.
