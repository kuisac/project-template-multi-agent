# Project template — équipe IA multi-agents adversariale

> Squelette de projet pour Claude Code optimisé pour la qualité multi-aspect
> (doc, tests, sécurité, critique produit) via une équipe d'agents qui se
> challengent en mode adversarial, orchestrée par un chef de projet (Pilote).

---

## Vue d'ensemble

```
.
├── CLAUDE.md                 ← contexte projet + rôle Pilote (lu auto par Claude Code)
├── README.md                 ← ce fichier
├── .mcp.json                 ← serveurs MCP (Perplexity, GPT, Gemini)
├── .claude/                  ← TOUT le paramétrage IA, en un seul endroit
│   ├── settings.json           ← config technique (hooks)
│   ├── agents/                 ← 9 sub-agents Claude
│   ├── commands/               ← 6 commandes /slash
│   ├── hooks/                  ← scripts shell sur événements
│   ├── shared/                 ← team-charter, templates ADR/itération, doc agents externes
│   │   └── templates/
│   └── OtherAI/                ← briefs pour IA externes (non Claude Code)
│       ├── gpt/                  ← Gepetto
│       ├── gemini/               ← Gemina
│       └── perplexity/           ← Perci
│
├── src/                      ← code applicatif
├── runtime/                  ← artefacts d'exécution (logs, builds locaux)
├── tests/                    ← tests unitaires, intégration, e2e
├── requirements/             ← pré-requis techniques
└── doc/
    ├── functional/             ← specs fonctionnelles, glossaire métier
    ├── technical/              ← specs techniques détaillées
    ├── architecture/           ← ADR + threat model + diagrammes C4
    ├── backlog/                ← user stories, epics, MoSCoW
    └── reviews/                ← rapports de revue par itération
        └── external/             ← contributions Gepetto/Gemina/Perci
```

> **Tout ce qui est IA est dans `.claude/`** — y compris les briefs pour les IA
> non-Anthropic (GPT/Gemini/Perplexity), regroupés sous `.claude/OtherAI/`.
> Pas de symlinks, pas de duplication, pas d'arbitrage technique.

---

## Démarrage rapide

1. **Cloner ce template** dans un nouveau projet.
2. **Compléter `CLAUDE.md`** : nom du projet, stack, phase.
3. **(Optionnel) Activer les MCP** : remplir un `.env` avec `PERPLEXITY_API_KEY`,
   éventuellement `OPENAI_API_KEY` / `GEMINI_API_KEY`, et activer les serveurs
   correspondants dans `.mcp.json` (passer `disabled` à `false`).
4. **Lancer Claude Code** dans le répertoire racine.
5. **Première commande recommandée** : `/team-status` pour vérifier que tout est branché.

---

## L'équipe IA

### Sub-agents Claude internes

#### Cœur de l'équipe

| Prénom | Rôle | Posture | Modèle |
|--------|------|---------|--------|
| **Pilote** | Chef de projet (toi en session normale, ou sub-agent invocable) | Arbitre | opus |
| **Archi** | Architecte logiciel | Constructeur | sonnet |
| **Specia** | Analyste fonctionnel / PO | Constructeur | sonnet |
| **Codie** | Développeur | Constructeur | sonnet |
| **Testor** | Ingénieur test & QA | Constructeur | sonnet |
| **Scribe** | Documentaliste / synthèse | Constructeur | sonnet |
| **Critik** | Reviewer code | **Contradicteur** | sonnet |
| **Sentinel** | Auditeur sécurité | **Contradicteur** | **opus** |
| **Devil** | Avocat du diable produit | **Contradicteur** | **opus** |

#### Spécialistes (à solliciter selon besoin)

| Prénom | Rôle | Posture | Modèle |
|--------|------|---------|--------|
| **Data** | DBA — relationnel + time-series IoT | Constructeur | sonnet |
| **Ergo** | UX/UI — web + mobile (iOS/Android) | Mixte | sonnet |
| **Métier** | Domaine **industrie / IoT** | Constructeur | sonnet |

### Agents externes (optionnels)

- **Gepetto** (OpenAI/GPT) — second avis algorithmique, brainstorming d'API.
- **Gemina** (Google Gemini) — analyse de gros corpus, contexte long.
- **Perci** (Perplexity) — recherche web sourcée, veille techno, CVE.

Détails et briefs dans `.claude/shared/external-agents.md` et `.claude/OtherAI/`.

---

## Commandes clés

### Cœur d'équipe

| Commande | Quand l'utiliser |
|----------|------------------|
| `/team-status` | Diagnostic de l'équipe (à lancer en début de session) |
| `/debate <sujet>` | Cycle adversarial complet sur une décision structurante |
| `/draft-us <besoin>` | Rédiger une US challengée par Devil |
| `/review-changes` | Critik + Sentinel + Testor passent sur les changements en cours |
| `/audit-security <périmètre>` | Sentinel audite, Critik signale les zones opaques |
| `/iteration-report <NN>` | Rapport consolidé fin d'itération |

### Spécialistes

| Commande | Quand l'utiliser |
|----------|------------------|
| `/data-review <périmètre>` | Data audite la couche de persistance (schéma, requêtes, index) |
| `/ux-review <feature>` | Ergo audite l'UX d'un parcours, avec contre-vérif Devil + Specia |
| `/domain-check <sujet>` | Métier valide la conformité métier d'une US ou d'un design |

---

## Le rôle de Pilote (chef de projet)

**En session normale**, c'est toi (Claude Code en session principale) qui joues
Pilote. Tu lis `CLAUDE.md` au démarrage, ce qui te donne ce rôle. Tu :

- Reçois la demande utilisateur.
- Évalues le niveau de structurance (L1 à L5).
- Délègues à un ou plusieurs sub-agents avec un brief ciblé.
- Arbitres quand les contradicteurs s'opposent aux constructeurs.
- Synthétises les retours pour l'utilisateur.

**Le sub-agent `pilote.md` est un complément optionnel** : tu peux l'invoquer
explicitement (« utilise pilote pour me proposer un plan ») quand tu veux
isoler un plan d'orchestration dans un contexte propre.

---

## Charte du débat

Lis `.claude/shared/team-charter.md`. C'est le document maître qui définit
comment l'équipe débat (constructeur → contradicteur → arbitre) et quels
niveaux de décision déclenchent quel niveau de cycle.

---

## Personnaliser

- **Renommer un agent** : édite le `name:` dans son frontmatter ET son fichier.
  Mets à jour les références dans les commandes (`debate.md`, etc.) et dans `CLAUDE.md`.
- **Ajouter un agent** : copie `.claude/agents/critik.md` (modèle de
  contradicteur) ou `.claude/agents/archi.md` (modèle de constructeur).
- **Changer le modèle d'un agent** : édite `model:` dans son frontmatter.
  Valeurs : `sonnet`, `opus`, `haiku`, ou `inherit` pour hériter de la session.
- **Désactiver un hook** : commente l'entrée correspondante dans `.claude/settings.json`.

---

## À compléter selon ton projet

- `requirements/test-policy.md` (seuil de couverture minimal, etc.).
- `requirements/security-policy.md` (référentiel sécu, OWASP ASVS niveau visé).
- `doc/architecture/threat-model.md` (à initialiser à la première itération).
- `doc/functional/glossary.md` (termes métier).
