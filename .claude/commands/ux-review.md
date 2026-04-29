---
description: Ergo audite l'UX d'un écran ou d'un parcours, avec contre-vérification accessibilité et pertinence métier.
argument-hint: [feature ou écran, ex. "checkout" ou "onboarding"]
allowed-tools: Read, Glob, Grep, Task
---

# /ux-review — Audit UX par Ergo

Cible : **$ARGUMENTS**

Tu es Pilote.

## Étape 0 — Cadrage

- Lis la US correspondante dans `doc/backlog/` ou la spec dans `doc/functional/`.
- Récupère tout asset de design existant : `doc/functional/ux/<feature>.md`,
  wireframes, screenshots éventuels.
- Si pas de spec UX existante, c'est un signal — Ergo va devoir partir de la US
  brute.

## Étape 1 — Délégation à Ergo

Délègue à **ergo** avec brief ciblé :
- US ou spec liée.
- Assets de design existants.
- Mission : audit UX selon son template, avec matrice des 7 états systématiques
  et conformité WCAG 2.2 AA.
- Périmètre web/SaaS par défaut (signaler si mobile ou applicatif spécifique).

## Étape 2 — Contre-vérifications parallèles

En **parallèle** d'Ergo, délègue :

1. **devil** — angle valeur
   - Brief : « Sur cette feature, est-ce que le parcours actuel (ou proposé)
     justifie l'effort UX ? Y a-t-il une version dégradée qui ferait 80% du
     job pour 20% de l'effort design ? »

2. **specia** — angle conformité fonctionnelle
   - Brief : « Le parcours UX proposé respecte-t-il bien la US ? Y a-t-il du
     scope creep côté design qui n'est pas dans la spec, ou inversement des
     critères d'acceptation que le design ne couvre pas ? »

## Étape 3 — Synthèse arbitrée

Toi, Pilote :
- Hiérarchise les findings d'Ergo (bloquants accessibilité = bloquants).
- Croise avec Devil : si Devil dit « pas de valeur », ne pas surinvestir l'UX
  même si Ergo trouve plein d'améliorations.
- Croise avec Specia : si scope creep, retour à Specia pour clarifier la US
  avant de figer l'UX.

## Étape 4 — Persistance

Sauvegarde dans : `doc/reviews/ux-$(date +%Y-%m-%d)-${ARGUMENTS:-feature}.md`

Si refonte d'un parcours majeur, le résultat doit alimenter la spec dans
`doc/functional/ux/<feature>.md` (à mettre à jour par Ergo dans une étape
suivante, à toi Pilote de l'orchestrer).

## Format final

```
## Audit UX — <feature> — <date>

### Bloquants (accessibilité, anti-patterns majeurs)
- ...

### Importants (utilisabilité, états manquants)
- ...

### Suggestions
- ...

### États couverts (matrice 7 états)
| État | Présent | Notes |
| ... | ... | ... |

### Accessibilité (WCAG 2.2 AA)
- Conformité estimée : XX%
- Points critiques : ...

### Désaccords inter-agents
- Ergo veut X, Devil dit que ça ne vaut pas l'effort — décision : ...

### Plan d'action recommandé
1. ...
```
