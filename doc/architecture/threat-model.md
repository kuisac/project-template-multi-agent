# Threat model — `<nom du projet>`

> Document maintenu par Sentinel. Mis à jour à chaque itération qui modifie la
> surface d'attaque. Référencé par tout audit `/audit-security`.

**Dernière mise à jour** : YYYY-MM-DD
**Mainteneur** : Sentinel
**Référentiel** : OWASP Top 10 (2021), ASVS niveau `[L1 | L2 | L3]`

---

## 1. Actifs à protéger

| Actif | Sensibilité | Localisation | Propriétaire |
|-------|-------------|--------------|--------------|
| Données utilisateur (PII) | Élevée | DB principale | ... |
| Secrets applicatifs | Critique | Vault / env | ... |
| Code source | Moyenne | Git | ... |
| Logs applicatifs | Moyenne | ... | ... |
| Sauvegardes | Élevée | ... | ... |

---

## 2. Acteurs hostiles plausibles

| Acteur | Motivation | Capacité estimée |
|--------|------------|------------------|
| Utilisateur authentifié malveillant | Élévation de privilège, accès données tierces | Faible à moyenne |
| Attaquant externe non authentifié | Vol de données, déni de service | Moyenne |
| Insider (ancien employé / contributeur) | Sabotage, exfiltration | Élevée |
| Attaquant supply chain | Injection via dépendance compromise | Élevée |

---

## 3. Surfaces d'attaque

### 3.1. Endpoints exposés

| Endpoint | Auth requise | Données manipulées | Notes |
|----------|--------------|--------------------|----|
| ... | ... | ... | ... |

### 3.2. Dépendances externes

| Dépendance | Version | Confiance | Dernière vérification CVE |
|------------|---------|-----------|---------------------------|
| ... | ... | ... | YYYY-MM-DD |

### 3.3. IO externes (fichiers, webhooks, API tierces)

- ...

### 3.4. Secrets en circulation

| Secret | Localisation | Rotation | Accès |
|--------|--------------|----------|-------|
| ... | ... | ... | ... |

---

## 4. Scénarios d'attaque identifiés

### Scénario S-001 : `<titre>`

- **Acteur** : ...
- **Vecteur** : ...
- **Étapes** :
  1. ...
  2. ...
  3. ...
- **Impact** : ...
- **Mitigation actuelle** : ...
- **Mitigation cible** : ...
- **Statut** : `Identifié` | `Mitigé partiellement` | `Mitigé` | `Accepté`

---

## 5. Décisions de risque acceptées

| ID | Risque | Raison de l'acceptation | Date | ADR lié |
|----|--------|------------------------|------|---------|
| R-001 | ... | ... | YYYY-MM-DD | ADR-NNN |

---

## 6. Historique des changements significatifs

| Date | Changement | Auteur |
|------|------------|--------|
| YYYY-MM-DD | Création initiale | Sentinel |
