<!-- wizard:begin header -->
# Project template — équipe IA multi-agents adversariale

> Squelette de projet pour Claude Code optimisé pour la qualité multi-aspect
> (doc, tests, sécurité, critique produit) via une équipe d'agents qui se
> challengent en mode adversarial, orchestrée par un chef de projet (Pilote).
<!-- wizard:end header -->

---

## Vue d'ensemble

<!-- wizard:begin tree -->
```
.
├── CLAUDE.md                 ← contexte projet + rôle Pilote (lu auto par Claude Code)
├── README.md                 ← ce fichier
├── .mcp.json                 ← serveurs MCP (Perplexity, GPT, Gemini)
├── .claude/                  ← TOUT le paramétrage IA, en un seul endroit
│   ├── settings.json           ← config technique (hooks)
│   ├── agents/                 ← sub-agents Claude (un .md par agent)
│   ├── commands/               ← commandes /slash
│   ├── hooks/                  ← scripts shell sur événements
│   ├── shared/                 ← team-charter, templates ADR/itération, doc agents externes
│   │   └── templates/
│   ├── wizard/                 ← catalogue des composants + état d'initialisation
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
<!-- wizard:end tree -->

> **Tout ce qui est IA est dans `.claude/`** — y compris les briefs pour les IA
> non-Anthropic (GPT/Gemini/Perplexity), regroupés sous `.claude/OtherAI/`.
> Pas de symlinks, pas de duplication, pas d'arbitrage technique.

---

## Démarrage rapide

<!-- wizard:begin quickstart -->
1. **Cloner ce template** dans un nouveau projet, puis retirer l'historique git
   du template si tu veux repartir d'un dépôt vierge.
2. **Lancer Claude Code** dans le répertoire racine.
3. **Lancer `/init-project`** — le wizard fait le reste :
   - il **mène un entretien de cadrage** : le problème résolu, pour qui, ce qui
     est hors sujet, les contraintes, le critère de réussite — puis il te restitue
     ce qu'il a compris et **fait contre-lire le besoin par Devil** avant d'aller
     plus loin ;
   - il te fait choisir la **politique d'élicitation** du projet : combien Claude
     te questionne avant de produire, pour toute la vie du projet ;
   - il renseigne l'identité du projet (nom, stack, phase, description) ;
   - il te fait choisir un **profil** (solo, web/SaaS, industrie-IoT, data, complet) ;
   - il te laisse **ajuster à la carte** les agents, commandes et hooks ;
   - il **supprime** ce que tu n'as pas retenu et régénère `CLAUDE.md`, ce
     `README.md`, `.claude/settings.json`, `.mcp.json` et la charte d'équipe.
4. **Définir les variables d'environnement** des serveurs MCP activés
   (`PERPLEXITY_API_KEY`, `OPENAI_API_KEY`, `GEMINI_API_KEY`), puis **redémarrer**
   Claude Code — `.mcp.json` et `settings.json` ne sont relus qu'au démarrage.
5. **Première commande** : `/team-status` pour vérifier que tout est branché.

> Le wizard est non destructif tant que tu n'as pas confirmé : `/init-project --dry-run`
> déroule tout le dialogue et affiche le plan sans rien écrire. `/init-project --check`
> se contente de valider la cohérence du catalogue.
>
> Besoin d'ajouter un agent trois semaines plus tard ? `/init-project --reconfigure`
> repart de tes réponses précédentes.
<!-- wizard:end quickstart -->

---

## Comment Claude te parle

Le template ne se contente pas d'organiser le débat **entre agents** : il cadre
aussi l'échange **entre toi et Claude**. Une demande n'est pas une spécification,
et l'essentiel des livrables ratés le sont pour avoir répondu trop vite à une
demande mal comprise.

Avant toute production, Pilote mène un **entretien de besoin** (le « Temps 0 » de
la charte) qui lève six zones d'ombre : intention, usage, périmètre, contraintes,
critère de succès, scénario d'échec. Il restitue ce qu'il a compris, le fait
valider, puis **Devil contre-lit le besoin** — pas la solution : une intention non
dite, un scope qui enfle, une hypothèse invérifiée.

La **profondeur** de cet entretien est un paramètre du projet, choisi à
l'initialisation parmi trois politiques :

| Politique | Ce qu'elle impose |
|-----------|-------------------|
| `minimal` | Un tour de questions, puis production sous hypothèses écrites en tête du livrable. |
| `gradue` | La profondeur suit le niveau L1–L5 : rien sur du trivial, entretien complet sur du structurant. |
| `approfondi` | Entretien systématique avant toute production. **Défaut du template.** |

La politique retenue est inscrite dans la zone `elicitation` de `CLAUDE.md` et se
change avec `/init-project --reconfigure`. Le détail de la doctrine — les six
zones, comment questionner, quand s'arrêter — est dans `CLAUDE.md` § 2.

---

## L'équipe IA

### Sub-agents Claude internes

#### Cœur de l'équipe

<!-- wizard:begin team-table -->
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
<!-- wizard:end team-table -->

#### Spécialistes (à solliciter selon besoin)

<!-- wizard:begin specialists-table -->
| Prénom | Rôle | Posture | Modèle |
|--------|------|---------|--------|
| **Data** | DBA — relationnel + time-series IoT | Constructeur | sonnet |
| **Ergo** | UX/UI — web + mobile (iOS/Android) | Mixte | sonnet |
| **Métier** | Domaine **industrie / IoT** | Constructeur | sonnet |
<!-- wizard:end specialists-table -->

### Agents externes (optionnels)

- **Gepetto** (OpenAI/GPT) — second avis algorithmique, brainstorming d'API.
- **Gemina** (Google Gemini) — analyse de gros corpus, contexte long.
- **Perci** (Perplexity) — recherche web sourcée, veille techno, CVE.

Détails et briefs dans `.claude/shared/external-agents.md` et `.claude/OtherAI/`.

---

## Commandes clés

### Cœur d'équipe

<!-- wizard:begin commands-table -->
| Commande | Quand l'utiliser |
|----------|------------------|
| `/team-status` | Diagnostic de l'équipe (à lancer en début de session) |
| `/init-project` | (Re)configurer l'équipe et l'arborescence depuis le catalogue |
| `/debate <sujet>` | Cycle adversarial complet sur une décision structurante |
| `/draft-us <besoin>` | Rédiger une US challengée par Devil |
| `/review-changes` | Critik + Sentinel + Testor passent sur les changements en cours |
| `/audit-security <périmètre>` | Sentinel audite, Critik signale les zones opaques |
| `/iteration-report <NN>` | Rapport consolidé fin d'itération |
<!-- wizard:end commands-table -->

### Spécialistes

<!-- wizard:begin specialists-commands-table -->
| Commande | Quand l'utiliser |
|----------|------------------|
| `/data-review <périmètre>` | Data audite la couche de persistance (schéma, requêtes, index) |
| `/ux-review <feature>` | Ergo audite l'UX d'un parcours, avec contre-vérif Devil + Specia |
| `/domain-check <sujet>` | Métier valide la conformité métier d'une US ou d'un design |
<!-- wizard:end specialists-commands-table -->

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

> **Le plus simple : `/init-project --reconfigure`.** Il régénère toutes les
> zones balisées de façon cohérente. Les manipulations ci-dessous restent
> valables pour ce que le wizard ne couvre pas.

- **Ajouter un composant au catalogue** : voir `.claude/wizard/README.md`. Tant
  qu'un agent, une commande ou un hook n'est pas déclaré dans
  `.claude/wizard/catalog.json`, le wizard l'ignore — il ne le proposera ni ne
  le supprimera.
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
