---
description: Diagnostique l'état de l'équipe IA (agents disponibles, dette de doc, dernier débat, charge de chacun).
allowed-tools: Read, Glob, Bash(ls:*), Bash(find:*), Bash(date:*), Bash(grep:*)
---

# /team-status — État de l'équipe IA

Tu es Pilote. Tu produis un rapport synthétique sur l'état de fonctionnement de
l'équipe IA. Pas de délégation — c'est un diagnostic en lecture directe.

## 1. Inventaire des agents

Liste les agents définis :
- Sub-agents Claude : !`ls -1 .claude/agents/ 2>/dev/null`
- Commandes disponibles : !`ls -1 .claude/commands/ 2>/dev/null`
- Hooks actifs : !`ls -1 .claude/hooks/ 2>/dev/null`
- Briefs externes : !`find .claude/OtherAI -name "*.md" 2>/dev/null`

## 2. Activité récente

- Derniers ADR : !`ls -t doc/architecture/ADR-*.md 2>/dev/null | head -5`
- Dernières revues : !`ls -t doc/reviews/*.md 2>/dev/null | head -5`
- US en cours : !`ls -t doc/backlog/iteration-*.md 2>/dev/null | head -3`

## 3. Dette de documentation

Détecte :
- Les fichiers `.md` contenant `TBD`, `TODO`, `À compléter` (signal de doc abandonnée).
- Les ADR au statut `Proposé` depuis plus de 7 jours (décisions en suspens).
- Les répertoires `doc/` vides (zones grises non documentées).

Utilise : !`grep -rIn 'TBD\|TODO\|À compléter\|FIXME' doc/ 2>/dev/null | head -20`

## 4. Équilibre constructeur / contradicteur

Compte sur les 5 derniers rapports de revue :
- Combien d'interventions de Critik / Sentinel / Devil ?
- Y a-t-il des décisions structurantes prises **sans** trace de contradiction ?
  (Cherche des ADR récents qui ne mentionnent qu'un seul contributeur — c'est
  un signal d'alerte selon la charte.)

## 5. Format de sortie

```
# État de l'équipe IA — <date>

## Agents disponibles
- Cœur d'équipe : Pilote, Archi, Specia, Codie, Testor, Scribe (Sonnet) | Sentinel, Devil (Opus) — 9/9
- Spécialistes : Data, Ergo, Métier (Sonnet) — 3/3
- Externes briefés : Gepetto (template), Gemina (template), Perci (template)
- Commandes : N
- Hooks : N

## Activité récente
- Dernier ADR : ADR-NNN — <date>
- Dernière revue : <date>
- Itération en cours : NN

## Alertes
🟡 N décisions structurantes sans contradicteur signé
🟠 N ADR en statut Proposé depuis > 7 jours
🔴 N TODO/TBD persistants

## Recommandations
1. ...
2. ...
```

## Règles

- Ce rapport est descriptif, pas prescriptif. Ne propose pas de changement
  d'organisation — pointe les signaux faibles.
- Si tout va bien, dis-le sobrement. Pas de félicitations.
