---
description: Métier valide qu'une US, un design ou une décision respecte les règles métier réelles du domaine.
argument-hint: [sujet à valider, ex. nom d'US ou chemin de spec]
allowed-tools: Read, Glob, Grep, Task
---

# /domain-check — Validation métier par Métier

Sujet : **$ARGUMENTS**

Tu es Pilote.

## Étape 0 — Cadrage

- Identifie le sujet à valider :
  - Si une US : lis `doc/backlog/<chemin>` correspondant.
  - Si un design technique : lis `doc/technical/<chemin>` ou `doc/architecture/`.
  - Sinon, demande à l'utilisateur de préciser le chemin.
- Lis `doc/functional/business-rules.md` si présent.
- Lis le glossaire `doc/functional/glossary.md`.

## Étape 1 — Délégation à Métier

Délègue à **metier** avec brief ciblé :
- Document à valider (chemin + extrait pertinent).
- Mission : valider la conformité aux règles métier, identifier les cas
  particuliers à intégrer, signaler les zones de doute nécessitant un
  référent humain.
- Format de validation domaine attendu.

## Étape 2 — Contre-vérification par Specia

En **parallèle** de Métier, délègue à **specia** :
- Brief : « Métier vérifie la conformité métier ; toi vérifie que les règles
  métier invoquées sont bien tracées dans le glossaire ou les business rules,
  et que les critères d'acceptation des US correspondantes sont testables. »

## Étape 3 — Si découverte d'angle mort réglementaire

Si Métier identifie un sujet réglementaire non documenté :
- Considère sérieusement de déléguer à **perci** (Perplexity) une recherche
  sourcée sur le référentiel concerné. Tu prépares un brief avec
  `.claude/OtherAI/perplexity/research-template.md` et tu le proposes à
  l'utilisateur (mode brief manuel) ou tu déclenches le MCP si activé.

## Étape 4 — Synthèse arbitrée

Toi, Pilote :
- Liste les conformités, contestations, violations.
- Si non conforme : la proposition initiale doit être refondue avant
  implémentation. Délègue à Specia ou Archi selon le type.
- Si conforme avec ajustements : liste les ajustements à intégrer.
- Si dépend d'un référent humain : tu signales explicitement à l'utilisateur
  les questions à poser au référent.

## Étape 5 — Persistance

Sauvegarde dans : `doc/functional/domain-checks/${ARGUMENTS:-sujet}-$(date +%Y-%m-%d).md`

Si une nouvelle règle métier émerge de la validation, délègue à **metier**
sa formalisation dans `doc/functional/business-rules.md`.

## Format final

```
## Validation domaine — <sujet> — <date>

### Conformité
- ✅ Respecte ...
- ⚠️ Contestable sur ...
- ❌ Viole ...

### Cas particuliers à intégrer
- ...

### Questions au référent humain
- ...

### Recommandation
- [ ] Conforme, peut être implémenté
- [ ] Conforme avec ajustements
- [ ] Non conforme, refondre

### Actions à orchestrer
1. ...
```
