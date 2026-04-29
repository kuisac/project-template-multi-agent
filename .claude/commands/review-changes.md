---
description: Lance une revue multi-agents (Critik + Sentinel + Testor) sur les changements en cours.
argument-hint: [optionnel : périmètre, ex. "src/auth"]
allowed-tools: Read, Glob, Grep, Bash(git status:*), Bash(git diff:*), Bash(git log:*), Task
---

# /review-changes — Revue multi-agents

Périmètre : **${ARGUMENTS:-tous les changements non commités}**

## Étape 0 — État du dépôt

- Statut git : !`git status --short`
- Diff : !`git diff --stat HEAD`

## Étape 1 — Délégations parallèles

Tu es Pilote. Délègue **en parallèle** (mêmes message, plusieurs Task) aux trois
sub-agents :

1. **critik** — revue qualité / lisibilité / dette
   - Brief ciblé : les fichiers modifiés ci-dessus + leur diff.
   - Format : son template de rapport.
   - Doit produire au minimum 1 bloquant + 1 important + 1 suggestion (ou justifier qu'il n'y en a pas).

2. **sentinel** — audit sécurité
   - Brief ciblé : les fichiers modifiés + le threat model si pertinent.
   - Format : son template de rapport.
   - Focus : nouveaux endpoints, nouvelles dépendances, nouveaux logs, nouvelles IO.

3. **testor** — couverture des tests
   - Brief ciblé : les fichiers modifiés + les tests associés.
   - Doit indiquer : couverture estimée du code modifié, cas non couverts, qualité des assertions.

## Étape 2 — Synthèse

Une fois les trois retours reçus :
1. Liste les **bloquants** consolidés (toutes sources confondues).
2. Liste les **importants**.
3. Propose un plan d'action **dans l'ordre** : bloquants d'abord, puis importants.
4. Si un agent a contredit un autre, signale-le explicitement.

## Étape 3 — Persistance

Sauvegarde la synthèse dans :
`doc/reviews/review-$(date +%Y-%m-%d-%H%M).md`

## Format final

```
# Revue de changements — <date>
**Périmètre** : ...

## Bloquants (à corriger avant merge)
- [Source] [path:lignes] description

## Importants
- ...

## Suggestions
- ...

## Désaccords inter-agents
- ...

## Plan d'action recommandé
1. ...
2. ...
```
