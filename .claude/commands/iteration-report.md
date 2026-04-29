---
description: Produit le rapport consolidé de fin d'itération (tests, code, sécu, produit, doc).
argument-hint: [numéro d'itération, ex. 12]
allowed-tools: Read, Write, Glob, Grep, Bash(git log:*), Bash(git diff:*), Task
---

# /iteration-report — Rapport de fin d'itération

Itération concernée : **${ARGUMENTS:-itération courante}**

Tu es **Pilote**, l'arbitre de cette synthèse. Tu n'écris pas le rapport seul :
tu orchestres les agents puis tu fais consolider par Scribe.

## Étape 0 — Contexte

- Lis `doc/reviews/` pour repérer le dernier rapport d'itération.
- Récupère la liste des changements depuis : !`git log --oneline --since="2 weeks ago"`
- Identifie les périmètres modifiés.

## Étape 1 — Délégations parallèles

Lance **en parallèle** (un seul message, plusieurs Task) :

1. **testor** — État des lieux des tests
   - Brief ciblé : périmètre de l'itération + politique de tests.
   - Couverture globale et par module (chiffré).
   - Modules sous le seuil défini dans `requirements/test-policy.md`.
   - Tests ajoutés / retirés / modifiés.
   - Tests flaky détectés.
   - Sortie : section "Tests" du rapport.

2. **critik** — Bilan qualité / dette
   - Brief ciblé : commits de l'itération.
   - Code smells récurrents observés sur l'itération.
   - Modules dont la complexité a augmenté.
   - Conventions non respectées.
   - Sortie : section "Qualité code" du rapport.

3. **sentinel** — Bilan sécurité (Opus)
   - Brief ciblé : changements de surface (nouveaux endpoints, deps, IO).
   - Nouvelles surfaces exposées sur l'itération.
   - Nouvelles dépendances et leur évaluation.
   - Findings ouverts vs résolus.
   - Sortie : section "Sécurité" du rapport.

4. **devil** — Bilan produit (Opus)
   - Brief ciblé : US livrées + US prévues à l'origine.
   - Features livrées vs features promises.
   - Hypothèses validées ou invalidées par les retours.
   - Features livrées mais non utilisées (si métrique disponible, sinon
     posture critique sur l'utilité présumée).
   - Sortie : section "Produit" du rapport.

## Étape 2 — Synthèse arbitrée

Une fois les 4 retours reçus, toi Pilote :
- Identifie les **incohérences** entre rapports (ex. Testor dit couverture OK,
  Critik dit code mort dans le même module).
- Identifie les **risques systémiques** qui apparaissent en croisant les vues.
- Tranche les priorités pour l'itération suivante.

## Étape 3 — Consolidation par Scribe

Délègue à **scribe** la rédaction finale dans :
`doc/reviews/iteration-${ARGUMENTS:-NN}-$(date +%Y-%m-%d).md`

Brief à lui passer : « Consolide ces 4 rapports + mon arbitrage selon le
template `.claude/shared/templates/iteration-report.md`. Cite les sources, garde
les positions divergentes visibles, ne lisse pas les désaccords. »

## Étape 4 — Annonce

Termine ta session par :
- Le chemin du rapport produit.
- Les 3 priorités pour l'itération suivante.
- Les ADR à créer / mettre à jour s'il y en a.
