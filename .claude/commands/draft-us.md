---
description: Specia rédige une user story complète, immédiatement challengée par Devil.
argument-hint: [besoin exprimé en langage naturel]
allowed-tools: Read, Write, Glob, Grep, Task
---

# /draft-us — Rédaction d'une US sous contradiction

Besoin : **$ARGUMENTS**

Tu es Pilote.

## Étape 1 — Cadrage

- Lis `doc/functional/glossary.md` si présent.
- Lis `doc/backlog/iteration-*.md` les plus récents pour comprendre le contexte produit.

## Étape 2 — Rédaction par Specia

Délègue à **specia** avec brief ciblé (besoin + contexte produit pertinent uniquement) :
- Reformule le besoin dans ses mots, pointe les ambiguïtés.
- Si besoin : pose 1 à 3 questions à l'utilisateur **avant** d'écrire la US.
  Si pas de réponse, fait des hypothèses **explicites**.
- Rédige une US complète :
  - Titre, rôle, action, bénéfice.
  - Critères d'acceptation Gherkin (au moins 3 scénarios : nominal, alternatif, erreur).
  - Priorité MoSCoW + justification.
  - Dépendances éventuelles.
  - Estimation grossière en complexité (S / M / L / XL).

## Étape 3 — Challenge par Devil (Opus)

Délègue à **devil**, en lui passant la US produite par Specia :
- Premortem obligatoire (3 raisons d'échec à 6 mois).
- Hypothèses contestables.
- Utilisateurs ignorés.
- Au moins une alternative plus simple (« faire moins »).
- Recommandation : construire / réduire / reporter / tester d'abord.

## Étape 4 — Arbitrage

Toi, Pilote :
- Si Devil recommande « construire tel quel », publie la US dans `doc/backlog/`.
- Si Devil propose une réduction de portée recevable, retourne à **specia** avec
  ce nouveau brief, puis publie la version réduite.
- Si Devil recommande « reporter / abandonner » et que tu juges sa contradiction
  recevable, **n'écris pas la US** : crée une note dans `doc/backlog/rejected/<slug>.md`
  qui explique pourquoi.

## Étape 5 — Vérification de testabilité

Avant publication finale, délègue à **testor** une micro-vérification :
« Les critères d'acceptation Gherkin de cette US sont-ils testables sans
ambiguïté ? Si non, lesquels poseraient problème et pourquoi ? »

Corrige avec Specia si nécessaire.

## Format final

```
## US créée : <titre>
Fichier : doc/backlog/<iteration>/<slug>.md
Priorité : Must | Should | Could
Estimation : S | M | L | XL

### Challenges retenus
- ...

### Challenges écartés
- ...
```
