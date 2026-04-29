# Security policy — politique sécurité du projet

> Document de référence pour Sentinel. Adapter au domaine et au niveau de
> criticité du projet.

---

## Référentiel cible

- **OWASP Top 10 (2021)** — couverture obligatoire pour tout projet exposant
  des endpoints web.
- **OWASP ASVS** — niveau visé : `[L1 | L2 | L3]` (à choisir selon criticité).
- **CWE Top 25** — référence transverse pour les findings code.

---

## Surfaces d'attaque suivies

À chaque itération, Sentinel maintient à jour `doc/architecture/threat-model.md`
avec :

- **Endpoints exposés** (HTTP, gRPC, WebSocket, queues, etc.).
- **Sources de données externes** (API tierces, fichiers utilisateurs, webhooks).
- **Secrets en circulation** (où ils sont stockés, qui y a accès, rotation).
- **Dépendances externes** (et leur niveau de confiance).
- **Comptes / rôles** d'authentification et leurs privilèges.

---

## Règles dures

### Secrets

- Aucun secret en clair dans le code, dans les commits, dans les logs, dans
  les messages d'erreur retournés à l'utilisateur.
- Stockage : variables d'environnement, vault dédié, ou équivalent.
- Rotation : politique à définir et journaliser dans le threat model.

### Authentification & autorisation

- Pas d'auth fait main si une lib éprouvée existe.
- AuthN et AuthZ explicitement testées (cf. `requirements/test-policy.md`).
- Principe de moindre privilège par défaut.

### Données utilisateur (PII)

- Inventaire des PII manipulées : à maintenir dans le threat model.
- Logs : aucune PII en clair. Si nécessaire, hashing irréversible.
- Backups : chiffrés au repos.

### Dépendances

- Toute nouvelle dépendance externe passe par Sentinel.
- Critères d'acceptation :
  - CVE ouverte récente : refus par défaut, dérogation justifiée si vraiment nécessaire.
  - Dernier commit upstream > 12 mois : signal d'alerte.
  - Mainteneur unique : signal d'alerte.
  - Alternative établie disponible : la préférer si dette équivalente.

### Supply chain

- Lockfile commité (`package-lock.json`, `poetry.lock`, etc.).
- CI vérifie l'intégrité du lockfile.
- Mise à jour des dépendances : itération dédiée au moins une fois par trimestre.

---

## Niveaux de sévérité

| Niveau | Définition | Délai max de remédiation |
|--------|------------|-------------------------|
| **Critique** | Exploit immédiat / fuite de données réaliste sans condition particulière | 24 à 48 h |
| **Élevé** | Exploit conditionnel mais plausible | Itération en cours |
| **Moyen** | Défense en profondeur affaiblie | 2 itérations |
| **Bas** | Hygiène / bonne pratique non respectée | À planifier |

Findings critiques ouverts en fin d'itération = blocker de mise en production.

---

## Audits récurrents

- **Chaque itération** : audit incrémental sur les changements via `/audit-security`.
- **Chaque trimestre** : audit complet du périmètre (`/audit-security all`).
- **Chaque mise à jour majeure de dépendances** : audit ciblé.

---

## Cas spécifiques selon domaine

> Compléter selon le projet :

- **Si projet manipule des paiements** : ajouter PCI-DSS.
- **Si projet manipule de la santé** : ajouter HDS / HIPAA selon juridiction.
- **Si projet est dans l'UE et traite des données personnelles** : RGPD, registre
  des traitements à maintenir hors `doc/`.
- **Si projet est exposé publiquement** : ajouter une politique de
  divulgation responsable (`SECURITY.md` à la racine).

### Spécifique industrie / IoT (contexte de ce template)

Le template suppose un projet à composante industrielle. Les exigences
suivantes s'ajoutent à OWASP :

- **Référentiel cybersécu OT** : IEC 62443 (parties 3-3 pour les exigences
  système, 4-2 pour les composants). Niveau de sécurité (SL) cible à
  documenter dans le threat model.
- **Segmentation IT/OT** : aucun chemin réseau direct depuis Internet vers
  les automates / capteurs. Bastion / DMZ / unidirectional gateway selon
  criticité.
- **Mises à jour firmware / configuration** : signature obligatoire,
  versioning, capacité de rollback, fenêtre de maintenance planifiée.
- **Authentification équipements** : pas d'identifiants par défaut en prod.
  Rotation des credentials techniques.
- **Logs OT séparés** : les événements de sécurité OT vont dans un store
  dédié, conservés selon la politique sectorielle (souvent ≥ 1 an).
- **Sûreté > sécurité informatique** : si un contrôle de sécurité informatique
  peut bloquer une fonction de sûreté (arrêt d'urgence, fail-safe), la
  sûreté gagne. À documenter et challenger explicitement avec Métier.
- **Risque supply chain** : vérifier que les composants OT (firmwares, libs
  embedded) ne sont pas dans des advisories CISA / ICS-CERT récents.
