# Business rules — règles métier

> Maintenu par **Métier**. Source de vérité métier du projet (industrie / IoT).
> Toute règle a une source citée et au moins un exemple concret.
> Toute évolution passe par un ADR.

**Domaine de ce projet** : `<à compléter — ex. supervision d'une ligne d'embouteillage>`
**Référentiels normatifs applicables** : `<à compléter — ex. ISO 9001, IEC 62443 SL2>`
**Dernière mise à jour** : YYYY-MM-DD

---

## 1. Conventions de mesure

### R-001 — Unités SI strictes en interne
**Énoncé** : Toutes les grandeurs physiques sont stockées en unités SI
(mètres, kilogrammes, secondes, kelvins, ampères, moles, candelas) et leurs
unités dérivées strictes (Pa pour pression, J pour énergie, W pour puissance).
Conversion vers unités d'usage uniquement à l'affichage.
**Source** : Bonne pratique interne — choix architectural daté du YYYY-MM-DD.
**Exemple** : Une pression saisie en bar par l'opérateur (ex. 2.5 bar) est
stockée comme 250 000 Pa et ré-affichée en bar.

### R-002 — Statut de mesure obligatoire
**Énoncé** : Toute mesure de capteur stockée a au minimum 4 champs :
timestamp UTC, valeur, unité (implicite si SI documentée), **statut**
(good / bad / uncertain / stale / forced — convention OPC UA).
**Source** : OPC UA Part 8 — Data Access.
**Exemple** : `(2026-04-17T14:32:01.123Z, 312.4, K, good)` pour une mesure
de température capteur.

---

## 2. Capteurs et télémétrie

### R-010 — Hystérésis sur seuils d'alarme
**Énoncé** : Tout seuil critique déclenchant une action automatique a une
hystérésis explicite, pour éviter les oscillations.
**Source** : Bonne pratique automatisme — IEC 60050-351 (vocabulaire
électrotechnique).
**Exemple** : Alarme haute température à 350 K, retour à la normale à
345 K (5 K d'hystérésis), pas à 350 K exactement.

### R-011 — Détection de capteur figé
**Énoncé** : Un capteur dont la valeur ne change pas pendant N échantillons
consécutifs (N à définir par capteur, typique 30 à 300 selon dynamique
attendue) est marqué `uncertain` jusqu'à reprise de variation.
**Source** : Bonne pratique télémétrie.
**Exemple** : Capteur de débit qui renvoie 12.5 m³/h pendant 10 minutes
alors que la pompe est en marche → suspect.

---

## 3. Équipements

### R-020 — États conventionnels
**Énoncé** : Les états d'un équipement de production suivent ISA-88 part 1 :
idle, starting, running, holding, suspending, suspended, resuming, stopping,
stopped, aborting, aborted, completing, complete.
**Source** : ISA-88 part 1 — Batch Control.
**Exemple** : Une cuve de mélange en `holding` attend une intervention
opérateur, n'est pas en panne (`aborted`).

---

## 4. Workflows de production / qualité / maintenance

> À enrichir par projet.

### R-030 — Traçabilité par lot
**Énoncé** : Toute production identifiée par un numéro de lot a une
traçabilité ascendante (matières premières utilisées) et descendante
(produits finis générés). Conservation : `<durée à fixer selon
réglementation sectorielle>`.
**Source** : `<à compléter — typique ISO 9001 § 8.5.2 + réglementation
sectorielle>`.

---

## 5. Sûreté de fonctionnement

### R-040 — Séparation contrôle / sécurité
**Énoncé** : La logique de sécurité (SIL/PL — IEC 61508 / ISO 13849) ne
partage **jamais** son code, sa CPU ou son chemin de communication avec la
logique de contrôle commande. Toute proposition qui les fusionne est rejetée
sans discussion.
**Source** : IEC 61508 part 3 + ISO 13849-1.
**Exemple** : L'arrêt d'urgence physique reste câblé même si l'IHM logiciel
expose un bouton « stop ».

---

## 6. Cybersécurité OT

### R-050 — Pas d'identifiants par défaut
**Énoncé** : Aucun équipement OT en production ne conserve les identifiants
par défaut du constructeur. Rotation à l'installation et journalisation.
**Source** : IEC 62443-3-3 SR 1.5.

---

## Historique

| Date | Règle | Changement | ADR |
|------|-------|------------|-----|
| YYYY-MM-DD | R-001 à R-050 | Création initiale | - |

