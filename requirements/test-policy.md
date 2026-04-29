# Test policy — politique de tests du projet

> Document lu par Testor à chaque rapport d'itération et par Codie avant tout
> commit. Adapter les seuils au contexte.

---

## Seuils minimaux

| Indicateur | Seuil bloquant | Cible |
|------------|----------------|-------|
| Couverture globale (lignes) | 60 % | 80 % |
| Couverture des modules métier (`src/domain/`, `src/services/`) | 75 % | 90 % |
| Couverture des modules d'infrastructure (`src/infra/`) | 40 % | 70 % |
| Tests flaky tolérés en `main` | 0 | 0 |
| Tests désactivés (`@skip`, `xtest`, `it.skip`) | 0 | 0 |

Un seuil **bloquant** non atteint empêche la clôture de l'itération sans ADR
qui justifie l'écart.

---

## Pyramide attendue

- **Tests unitaires** : 70 % du nombre total. Rapides (< 100 ms unité), isolés.
- **Tests d'intégration** : 25 %. Vérifient les frontières (DB, API tierces, IO).
- **Tests e2e** : 5 %. Parcours utilisateurs critiques uniquement.

Si la pyramide s'inverse (plus d'e2e que d'unitaires), c'est un signal d'alerte
signalé dans le rapport d'itération de Testor.

---

## Cas obligatoirement couverts

Pour toute fonction publique :
- Chemin nominal.
- Au moins un cas d'erreur métier attendu.
- Au moins un cas limite (vide, nul, négatif, débordant) si applicable.

Pour tout endpoint exposé :
- Authentification valide.
- Authentification invalide.
- Autorisation refusée (si applicable).
- Payload malformé.
- Payload valide nominal.

---

## Conventions

- Un fichier de test par module, nommé `<module>.test.<ext>` (ou convention du langage).
- Nommage des tests : `should <comportement attendu> when <condition>` (langue au choix mais une seule).
- Pas de `sleep()` arbitraire pour synchroniser. Utiliser des mécanismes d'attente
  conditionnelle. Si vraiment impossible, justifier en commentaire.
- Pas de mock du code testé (auto-validation).
- Fixtures dans `tests/_fixtures/`, helpers dans `tests/_helpers/`.

---

## Tests de mutation (recommandé)

Si l'écosystème du projet le permet (Stryker pour JS, mutmut pour Python, etc.),
intégrer des tests de mutation au moins en CI nightly. Score cible : 60 %+.

C'est un excellent signal pour distinguer une couverture fictive (lignes
exécutées sans assertion réelle) d'une couverture utile.
