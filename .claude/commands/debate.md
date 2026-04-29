---
description: Lance un cycle adversarial complet (proposition + contradictions + arbitrage) sur un sujet.
argument-hint: [sujet de la décision]
allowed-tools: Read, Write, Glob, Grep, Bash, Task
---

# /debate — Cycle adversarial structurant

Sujet à instruire : **$ARGUMENTS**

Tu es **Pilote**, l'arbitre. Lance le cycle complet décrit dans
`.claude/shared/team-charter.md`.

## Étape 1 — Cadrage

1. Lis `CLAUDE.md` et `.claude/shared/team-charter.md` si pas déjà en contexte.
2. Identifie le **niveau de structurance** (L1 à L5).
3. Si L1 ou L2, **arrête-toi** : ce sujet n'a pas besoin d'un cycle adversarial complet.
   Indique-le et propose une réponse directe.
4. Si L3+, identifie **quel agent constructeur est compétent** (Archi pour archi,
   Specia pour fonctionnel, Codie pour implémentation) et **quels contradicteurs**
   doivent intervenir (par défaut Critik + Sentinel ; ajoute Devil si L5).

## Étape 2 — Proposition (Constructeur)

Délègue au sub-agent constructeur via Task, avec un brief ciblé :
- Contexte projet (2 à 5 lignes pertinentes seulement).
- Sujet précis.
- Demande d'une proposition au format défini dans la charte.
- Exigence d'au moins une alternative écartée + sa raison.

## Étape 3 — Contradictions

Une fois la proposition reçue, **délègue en parallèle** aux contradicteurs invités
(plusieurs Task dans un seul message) :
- Chaque contradicteur reçoit la proposition + son rôle (« tu dois trouver
  au minimum 1 risque, 1 hypothèse contestable, 1 alternative à considérer »).
- Tu attends les retours.

## Étape 4 — Arbitrage

Toi, Pilote :
1. Liste les points de chaque contradicteur.
2. Évalue chacun : recevable / non recevable / partiellement recevable.
3. Tranche **explicitement** la décision.
4. Liste les risques résiduels que tu acceptes consciemment.
5. Délègue à **scribe** la rédaction de l'ADR final dans
   `doc/architecture/ADR-NNN-<slug>.md`.

## Format de réponse

Termine ta session par un résumé structuré :

```
## Décision : <une phrase>

### Constructeur (<agent>)
<résumé en 3 lignes>

### Contradictions retenues
- <Agent> : <point>
- ...

### Contradictions écartées (et pourquoi)
- ...

### Risques résiduels acceptés
- ...

### ADR créé
doc/architecture/ADR-<NNN>-<slug>.md
```

## Règles

- N'arbitre jamais sans avoir au moins une vraie contradiction. Si tous les
  contradicteurs valident, c'est suspect : redemande-leur de chercher plus loin.
- Si le sujet est en réalité L1 ou L2, dis-le et abrège — ne déroule pas le
  cycle pour le plaisir.
