---
description: Audit sécurité complet par Sentinel sur un périmètre, avec rapport actionnable.
argument-hint: [périmètre, ex. "src/auth" ou "all"]
allowed-tools: Read, Glob, Grep, Bash(git ls-files:*), Task
---

# /audit-security — Audit sécurité par Sentinel (Opus)

Périmètre : **${ARGUMENTS:-all}**

> Note : Sentinel tourne en Opus. L'audit est plus lent mais plus fiable.

## Étape 0 — Cadrage

Tu es Pilote.
- Lis `requirements/security-policy.md` si présent (sinon, base-toi sur OWASP Top 10 2021 + ASVS L2).
- Lis `doc/architecture/threat-model.md` si présent.
- Identifie la liste des fichiers concernés :
  - Si `$ARGUMENTS == all` ou vide : !`git ls-files src/ requirements/ | head -200`
  - Sinon : !`git ls-files $ARGUMENTS`

## Étape 1 — Délégation à Sentinel

Délègue à **sentinel** avec ce brief ciblé :
- Périmètre exact (liste des fichiers).
- Référentiel à utiliser.
- Threat model en référence.
- Exigence de findings classés par sévérité (Critique / Élevé / Moyen / Bas)
  avec scénario d'exploit pour chacun.
- Mise à jour du threat model si nouveau vecteur identifié.

## Étape 2 — Contre-vérification par Critik

En **parallèle** de Sentinel, délègue à **critik** un brief restreint :
« Sur le même périmètre, identifie les zones de code où la complexité ou
l'opacité augmente le risque qu'un défaut de sécurité passe inaperçu en
relecture humaine. »

Ce n'est pas un audit sécurité — c'est un signal d'auditabilité que tu (Pilote)
recoupes avec les findings de Sentinel.

## Étape 3 — Synthèse arbitrée

Toi, Pilote :
- Liste les findings Sentinel par sévérité.
- Croise avec les zones d'opacité de Critik (un finding moyen dans une zone
  opaque devient prioritaire).
- Distingue : remédiations à planifier maintenant vs. risques à journaliser
  pour suivi.

## Étape 4 — Persistance

Sauvegarde dans :
`doc/reviews/security-$(date +%Y-%m-%d)-${ARGUMENTS:-all}.md`

Si un ADR sécuritaire s'impose (changement de modèle d'auth, rotation de
politique de secrets…), délègue à **scribe** sa rédaction.

## Format de sortie en console

```
## Findings sécurité — <date>
- Critiques : N
- Élevés : N
- Moyens : N
- Bas : N

### Top 3 actions immédiates
1. ...
2. ...
3. ...

### Rapport complet
doc/reviews/security-<date>.md
```
