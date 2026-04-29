# Rapport d'itération NN — YYYY-MM-DD

> Consolidé par Scribe à partir des contributions de Testor, Critik, Sentinel,
> Devil et de l'arbitrage du Pilote.

---

## Synthèse exécutive

3 à 5 lignes. Ce que l'équipe peut retenir si elle ne lit que ça.

| Indicateur | Valeur | Tendance |
|------------|--------|----------|
| Couverture de tests globale | XX % | ↑ / → / ↓ |
| Findings sécurité ouverts (Critique + Élevé) | N | |
| ADR adoptés cette itération | N | |
| US livrées / promises | N / M | |
| Tests flaky détectés | N | |

---

## 1. Tests (Testor)

### Couverture
- Globale : `XX %` (objectif : `YY %`)
- Par module :
  - `src/foo` : XX %
  - `src/bar` : XX %
  - ...

### Modules sous le seuil
- ...

### Tests ajoutés / retirés / modifiés
- Ajoutés : N
- Retirés : N (raisons : ...)
- Modifiés : N

### Flaky tests
- ...

### Recommandations
- ...

---

## 2. Qualité code (Critik)

### Bloquants résolus dans l'itération
- ...

### Bloquants restants
- ...

### Dette technique introduite ou résorbée
- Introduite : ...
- Résorbée : ...

### Code smells récurrents observés
- ...

---

## 3. Sécurité (Sentinel — Opus)

### Findings résolus
- ...

### Findings ouverts (par sévérité)
- Critique : N
- Élevé : N
- Moyen : N
- Bas : N

### Surface d'attaque évoluée
- Nouveaux endpoints : ...
- Nouvelles dépendances : ...
- Nouvelles IO externes : ...

### Threat model mis à jour ?
- Oui / Non — référence : ...

---

## 4. Produit (Devil — Opus)

### Features livrées vs promises
- ...

### Hypothèses validées / invalidées
- Validées : ...
- Invalidées : ...

### Features livrées peu ou pas utilisées
- ...

### Recommandations de pivot ou d'arrêt
- ...

---

## 5. Décisions structurantes prises

| ADR | Sujet | Statut |
|-----|-------|--------|
| ADR-NNN | ... | Accepté |

---

## 6. Désaccords inter-agents

> Section importante. Les positions divergentes doivent être visibles ici, pas
> lissées. Le but est de les retrouver dans 6 mois.

- ...

---

## 7. Risques systémiques identifiés

> Risques qui apparaissent en croisant plusieurs rapports.

- ...

---

## 8. Priorités pour l'itération N+1 (arbitrage Pilote)

1. ...
2. ...
3. ...

---

## Annexes

- Rapport Testor brut : `doc/reviews/iteration-NN-tests.md`
- Rapport Critik brut : `doc/reviews/iteration-NN-code-review.md`
- Rapport Sentinel brut : `doc/reviews/iteration-NN-security.md`
- Rapport Devil brut : `doc/reviews/iteration-NN-product-challenge.md`
