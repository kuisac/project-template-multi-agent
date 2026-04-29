---
description: Data audite la couche de persistance (schéma + requêtes + migrations + index) sur un périmètre.
argument-hint: [périmètre, ex. "src/repositories" ou un nom de feature]
allowed-tools: Read, Glob, Grep, Bash(git ls-files:*), Bash(git diff:*), Task
---

# /data-review — Audit data par Data

Périmètre : **${ARGUMENTS:-tous les changements récents touchant à la persistance}**

Tu es Pilote.

## Étape 0 — Cadrage

- Identifie les fichiers concernés :
  - Si périmètre fourni : !`git ls-files $ARGUMENTS 2>/dev/null | head -50`
  - Sinon, fichiers de migration et requêtes modifiés récemment :
    !`git diff --name-only HEAD~10 HEAD 2>/dev/null | grep -iE 'migration|repository|model|schema|sql|prisma|alembic' | head -30`
- Lis `doc/architecture/threat-model.md` section dépendances DB si pertinent.
- Lis les ADR existants liés au stockage (`doc/architecture/ADR-*data*.md`,
  `*storage*`, `*db*`).

## Étape 1 — Délégation à Data

Délègue à **data** avec ce brief ciblé :
- Liste des fichiers à auditer.
- Contexte : phase du projet, volumes estimés si connus, ADR de stockage en référence.
- Mission : audit de la couche de persistance sur le périmètre, format de note de
  modélisation pour les findings structurels, format d'audit pour les findings
  ponctuels.
- Sujets à couvrir explicitement : modèle, requêtes (N+1, plans), index,
  migrations (réversibilité, sûreté prod), événements (si projet event-driven).

## Étape 2 — Délégations parallèles complémentaires

En **parallèle** de Data, délègue :

1. **sentinel** — angle sécurité data
   - Brief : « Sur les mêmes fichiers que Data audite, identifie les risques
     d'injection (SQL/NoSQL), les expositions de données sensibles, les requêtes
     qui logguent des PII. »

2. **critik** — angle qualité
   - Brief : « Sur les mêmes fichiers, évalue la lisibilité des migrations
     et des requêtes, l'usage approprié de l'ORM (sur-utilisation, pièges). »

## Étape 3 — Synthèse arbitrée

Toi, Pilote :
- Croise les findings de Data avec ceux de Sentinel et Critik.
- Hiérarchise : bloquants prod (perfs, sécurité), importants itération,
  suggestions long terme.
- Si une décision structurante émerge (changement de modèle, introduction d'un
  cache, refonte de requête critique), prépare un cycle `/debate` séparé.

## Étape 4 — Persistance

Sauvegarde dans : `doc/reviews/data-$(date +%Y-%m-%d).md`

Si Data identifie un besoin de refonte structurelle, délègue à **scribe**
la rédaction d'un ADR dans `doc/architecture/`.

## Format final

```
## Audit data — <date>
**Périmètre** : ...

### Bloquants (perf prod, intégrité, sécu)
- [Source: Data|Sentinel|Critik] description

### Importants
- ...

### Migration : risques identifiés
- ...

### Index proposés
- ...

### Suggestions
- ...

### Décisions structurantes à débattre
- ... (si applicable, ouvrir /debate)
```
