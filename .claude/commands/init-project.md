---
description: Wizard de démarrage — transforme ce template en projet configuré (identité, équipe d'agents, commandes, hooks, MCP).
argument-hint: [aucun | --check | --dry-run | --reconfigure]
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion, Bash(git status:*), Bash(git rev-parse:*), Bash(git diff:*), Bash(ls:*), Bash(mkdir:*), Bash(rm:*), Bash(rmdir:*), Bash(find:*), Bash(date:*), Bash(python3:*)
---

# /init-project — Wizard de démarrage du template

Mode demandé : **${ARGUMENTS:-interactif}**

Tu n'es pas Pilote ici : tu es l'**installateur du template**. Tu ne délègues à
aucun sub-agent (la plupart vont être supprimés ou conservés selon les réponses,
les invoquer pendant leur propre sélection n'a pas de sens). Tu exécutes
toi-même, séquentiellement.

Ta source de vérité unique est **`.claude/wizard/catalog.json`**. Tu ne
codes en dur aucune liste d'agents, de commandes ou de hooks : tout vient du
catalogue. Si un composant a été ajouté au catalogue depuis la rédaction de
cette commande, tu le traites comme les autres, sans exception.

---

## Modes

| Argument | Comportement |
|----------|--------------|
| *(vide)* | Wizard interactif complet, puis application après confirmation. |
| `--check` | Valide la cohérence du catalogue et s'arrête. **Aucune modification.** |
| `--dry-run` | Déroule tout le dialogue et affiche le plan, puis s'arrête. **Aucune modification.** |
| `--reconfigure` | Repart de `.claude/wizard/state.json` : les réponses précédentes deviennent les valeurs par défaut. Permet d'ajouter un agent après coup. |

---

## Étape 0 — Garde-fous (toujours, quel que soit le mode)

1. Lis `.claude/wizard/catalog.json`. Absent ou illisible → **arrête-toi** et dis
   à l'utilisateur que le catalogue manque : sans lui le wizard n'a rien à appliquer.
2. Lance `git status --porcelain`. Si l'arbre n'est pas propre, **préviens** :
   le wizard supprime des fichiers, un arbre sale rend le retour en arrière
   pénible. Propose de commiter d'abord. N'insiste pas si l'utilisateur veut continuer.
3. Vérifie `.claude/wizard/state.json` :
   - présent **et** mode ≠ `--reconfigure` → dis que le projet a déjà été
     initialisé (donne la date et le profil enregistrés) et demande si
     l'utilisateur veut relancer en `--reconfigure` ou repartir de zéro. Attends la réponse.
   - absent → première initialisation, continue.

### Validation du catalogue (obligatoire en `--check`, silencieuse sinon sauf erreur)

Contrôle ces cinq invariants et rapporte tout écart :

1. **Ids uniques** et conformes au motif `<kind>.<slug>`.
2. **Chemins existants** : tout `path` / `paths` de `kind` ≠ `scaffold` pointe
   sur un fichier réellement présent.
3. **Dépendances résolues** : chaque entrée de `requires` et `recommends`
   désigne un id du catalogue.
4. **Tags déclarés** : chaque tag de composant existe dans la section `tags`.
5. **Profils clos** : pour chaque profil, tout composant inclus a ses `requires`
   inclus aussi, et tout composant `removable: false` est présent.

En `--check`, affiche le résultat sous forme de tableau (composant, invariant,
verdict) puis **arrête-toi là**. Ne modifie rien.

---

## Étape 1 — Identité du projet

Pose ces questions en texte libre (pas d'`AskUserQuestion`, ce sont des saisies
ouvertes). Une seule fois, groupées, pour ne pas hacher le dialogue :

- **Nom du projet** (obligatoire).
- **Stack principale** (ex. `Python/FastAPI`, `TypeScript/Next.js`, `C#/.NET 8`).
- **Phase actuelle** : `discovery`, `conception`, `build` ou `run`.
- **Description en une phrase** — ce que fait le produit. Elle alimentera le
  contexte projet du `CLAUDE.md` et du `README.md`.
- **Langue des livrables** (défaut : français) — appliquée aux ADR, specs, rapports.

En `--reconfigure`, propose les valeurs de `state.json` comme défauts : l'utilisateur
valide par Entrée ou corrige.

---

## Étape 2 — Choix du profil

Utilise `AskUserQuestion`. Construis **une option par profil du catalogue**, dans
l'ordre où ils y figurent :

- `label` = le `label` du profil,
- `description` = sa `description`, suivie du décompte réel des composants
  qu'il sélectionne (ex. « 11 agents, 9 commandes, 3 hooks »).

Ne code pas les profils en dur : s'il y en a plus de quatre dans le catalogue,
présente les trois les plus proches du contexte décrit à l'étape 1 plus
« Complet », et signale à l'utilisateur les profils non affichés.

---

## Étape 3 — Ajustements à la carte

Le profil est un point de départ, pas un verdict. Propose deux passes
d'ajustement, **groupées par tag** pour rester lisibles.

### 3a — Ajouter

Liste les composants du catalogue **hors** du profil retenu et `removable`.
Présente-les en `AskUserQuestion` avec `multiSelect: true`, une option par
composant : `label` = son `name`, `description` = son `summary`.

Si le nombre dépasse quatre (limite d'`AskUserQuestion`), fais plusieurs
questions successives regroupées par `kind` (agents, puis commandes, puis docs).

### 3b — Retirer

Liste les composants **du profil** qui sont `removable: true` et dont le tag
n'est pas `core`. Même format, question tournée « lesquels veux-tu retirer ? ».

Ne propose **jamais** un composant `removable: false` : ce sont les fondations
(Codie, Critik, Pilote, `/team-status`, `doc/reviews/`, `src/`, le glossaire).

---

## Étape 4 — Agents externes (MCP)

Pour chaque composant `kind: "mcp"` du catalogue, demande s'il doit être activé
(`AskUserQuestion`, `multiSelect: true`). Précise dans la `description` de chaque
option la variable d'environnement requise (`envVars`).

Trois issues par serveur, à retenir dans le plan :

- **Activé** → conservé dans `.mcp.json`, dossier `paths` conservé.
- **Conservé mais désactivé** → entrée gardée dans `.mcp.json` avec
  `"disabled": true`, dossier conservé. C'est le défaut pour un serveur non choisi
  quand l'utilisateur veut pouvoir l'activer plus tard.
- **Retiré** → entrée supprimée de `.mcp.json` **et** dossier `paths` supprimé.

Demande explicitement laquelle des deux dernières options s'applique aux serveurs
non retenus. Ne devine pas : supprimer `.claude/OtherAI/gpt/` est irréversible
côté working tree.

---

## Étape 5 — Hooks

Pour chaque composant `kind: "hook"`, demande s'il doit être **branché** dans
`.claude/settings.json`. Valeur par défaut = son `enabledByDefault`.

Rappelle dans la description ce que fait le hook (`summary`) et son `event`.
Un hook non branché mais conservé reste un fichier dans `.claude/hooks/` — dis-le,
c'est ce qui permet de l'activer plus tard sans réécrire le script.

---

## Étape 6 — Résolution et plan

### 6a — Clôture des dépendances

Calcule la sélection finale :

1. Pars de : composants du profil + ajouts (3a) − retraits (3b).
2. Ajoute **de force** tout composant `removable: false`.
3. Ferme transitivement les `requires` : si `/data-review` est retenu, `agent.data`
   l'est aussi. Répète jusqu'à stabilité.
4. Si une clôture réintroduit un composant que l'utilisateur venait de retirer
   en 3b, **dis-le explicitement** : « tu as retiré Data, mais `/data-review` le
   requiert — je garde Data, ou je retire aussi `/data-review` ? ». Tranche avec lui.
5. Vérifie les `recommends` : signale ceux qui manquent en **avertissement**, sans
   rien forcer. Exemple : `/review-changes` sans Sentinel fonctionne, mais la
   revue perd son volet sécurité — l'utilisateur doit le savoir.
6. **Composants liés aux MCP.** Les serveurs MCP ne figurent dans aucun profil
   (ils dépendent de clés d'API, pas du type de projet) : leur sélection vient
   de l'étape 4. Si au moins un serveur est retenu, ajoute
   `scaffold.doc-reviews-external` à la sélection — c'est là qu'atterrissent
   les contributions des agents externes. Si aucun ne l'est, écarte-le.
7. **Le wizard lui-même.** `command.init-project` fait partie de tous les
   profils. Ne le retire jamais à cette étape : sa suppression est proposée à
   l'étape 7.10, une fois l'initialisation réussie.

### 6b — Plan d'application

Affiche un plan clair **avant toute écriture**, en quatre listes :

| Section | Contenu |
|---------|---------|
| **Supprimé** | Chemins retirés, avec le composant qui les porte. |
| **Conservé** | Décompte par `kind` (ne liste pas les 40 chemins). |
| **Créé** | Dossiers `scaffold` manquants, `state.json`, rapport d'init. |
| **Réécrit** | `CLAUDE.md`, `README.md`, `.claude/settings.json`, `.mcp.json`, `team-charter.md`. |

En `--dry-run`, **arrête-toi ici**. Sinon, demande une confirmation explicite.
Une réponse ambiguë n'est pas une confirmation : redemande.

---

## Étape 7 — Application

Exécute dans cet ordre. Ne saute aucune étape ; si l'une échoue, arrête-toi et
dis exactement ce qui a été fait avant l'échec.

### 7.1 — Supprimer les composants non retenus

Pour chaque composant écarté, supprime son `path` et ses `paths`.
`kind: "scaffold"` écarté : ne supprime le dossier **que s'il est vide** — un
dossier qui contient du travail utilisateur n'est jamais effacé, signale-le à la place.

**Interdits absolus** : toucher à `.git/`, supprimer un composant `removable: false`,
supprimer un chemin absent du catalogue.

### 7.2 — Réécrire `.claude/settings.json`

Reconstruis l'objet `hooks` à partir des seuls hooks branchés, en groupant par
`event` et en reprenant le `matcher` du catalogue. Un `event` sans hook branché
reste présent avec un tableau vide (c'est la convention du template, elle
documente le point d'extension). Conserve les clés `//` de commentaire.

### 7.3 — Réécrire `.mcp.json`

Ne garde que les serveurs retenus. Un serveur conservé-mais-désactivé porte
`"disabled": true`. Conserve pour chaque serveur ses clés `//`, `//setup` et
`//model` : ce sont les instructions d'installation, elles restent utiles.
Si plus aucun serveur n'est retenu, écris un `.mcp.json` avec `mcpServers` vide
plutôt que de supprimer le fichier.

### 7.4 — Réécrire `CLAUDE.md`

`CLAUDE.md` contient des zones balisées :

```
<!-- wizard:begin <zone> -->
… contenu régénéré …
<!-- wizard:end <zone> -->
```

Réécris **uniquement l'intérieur** de ces zones. Tout ce qui est hors balises est
la doctrine du template (rôle de Pilote, règles de délégation, interdits) :
n'y touche pas — sauf pour retirer une règle qui référence un agent supprimé.

| Zone | À régénérer |
|------|-------------|
| `identity` | Nom, stack, phase, description, langue des livrables (étape 1). |
| `team-table` | Table des agents retenus dont le tag contient `core`, avec Rôle / Posture / Modèle lus dans le catalogue. |
| `specialists-table` | Table des agents retenus **sans** tag `core`. Si aucun, écris une ligne indiquant qu'aucun spécialiste n'est activé. |
| `commands-table` | Commandes retenues au tag `core`. |
| `specialists-commands-table` | Commandes retenues hors `core`. |
| `tree` | Arborescence effective, dossiers et fichiers retirés en moins. |
| `specialists-rules` | Règles « quand solliciter » — garde uniquement les paragraphes des spécialistes retenus. |

Une zone dont le contenu devient vide : remplace-la par une phrase explicite
(« Aucun spécialiste activé sur ce projet. ») plutôt que de laisser un trou.

### 7.5 — Réécrire `README.md`

Le `README.md` du template décrit le template. Après init, il doit décrire **le
projet**. Régénère-le à partir de l'identité (étape 1) et de la sélection :

- Titre = nom du projet, sous-titre = description en une phrase.
- Section « Équipe IA » = tables régénérées, mêmes sources que `CLAUDE.md`.
- Section « Commandes » = commandes retenues.
- Section « Démarrage » = variables d'environnement à définir (`envVars` des MCP
  retenus), puis `/team-status`.
- Retire la section « Démarrage rapide » du template (cloner, compléter, lancer
  le wizard) : elle n'a plus d'objet une fois le projet initialisé.
- Conserve la section « Personnaliser » en la réécrivant pour pointer vers
  `/init-project --reconfigure` et `.claude/wizard/README.md`.

### 7.6 — Mettre à jour `.claude/shared/team-charter.md`

La charte liste les membres par posture (§ 2.2, § 2.3, § 2.4). Régénère ces
listes à partir des agents réellement retenus et de leur `posture` dans le
catalogue. Ne touche pas au reste : les trois temps du débat, les niveaux
L1–L5 et les règles d'argumentation sont indépendants de la composition.

Si un niveau de structurance devient inatteignable (ex. L5 exige Devil et Devil
a été retiré), **signale-le** dans le rapport d'init et adapte la ligne du tableau.

### 7.7 — Créer les dossiers manquants

Pour chaque `scaffold` retenu et absent : crée-le avec un `.gitkeep`.
Vérifie que `runtime/` est bien ignoré par `.gitignore` ; sinon, ajoute-l'y.

### 7.8 — Écrire `.claude/wizard/state.json`

```json
{
  "initializedAt": "<date ISO du jour>",
  "catalogVersion": "<catalogVersion du catalogue>",
  "project": { "name": "…", "stack": "…", "phase": "…", "description": "…", "language": "…" },
  "profile": "<id du profil>",
  "selected": ["<ids retenus, triés>"],
  "removed": ["<ids écartés, triés>"],
  "hooksEnabled": ["<ids de hooks branchés>"],
  "mcpEnabled": ["<ids de serveurs activés>"],
  "mcpKeptDisabled": ["<ids conservés mais désactivés>"],
  "warnings": ["<recommends manquants, niveaux dégradés>"]
}
```

Obtiens la date par `date -I` — ne l'invente pas.

### 7.9 — Écrire le rapport d'initialisation

`doc/reviews/init-000-setup.md`, au format d'échange de la charte (§ 6) :
auteur `Wizard`, posture `Arbitre`, date, contexte `Initialisation du template`.
Contenu : profil retenu, composants écartés avec la raison (profil ou retrait
explicite), avertissements de l'étape 6a, et les actions restant à la charge de
l'utilisateur (variables d'environnement, politiques à compléter).

### 7.10 — Se retirer

`command.init-project` porte `selfRemoveAfterInit: true`. Demande à l'utilisateur
s'il veut supprimer `/init-project` maintenant.

Recommande de le **garder** : `--reconfigure` reste utile pour ajouter un agent
plus tard, et le fichier ne coûte que sa présence dans `.claude/commands/`.
Le catalogue et `.claude/wizard/` doivent être conservés dans tous les cas —
sans eux, `--reconfigure` ne peut plus rien faire.

---

## Étape 8 — Restitution

Termine par un récapitulatif court :

1. **Équipe constituée** — agents retenus, un par ligne, avec posture.
2. **À faire maintenant** — variables d'environnement à exporter, politiques à
   compléter (`requirements/test-policy.md`, `requirements/security-policy.md`),
   glossaire à amorcer.
3. **Première commande** — `/team-status` pour vérifier le branchement.
4. **Commit** — propose de commiter, avec un message décrivant le profil retenu.
   Ne commite pas sans accord.

Rappelle que `.mcp.json` et `.claude/settings.json` ne sont relus qu'au
**démarrage** de Claude Code : les hooks et serveurs MCP modifiés ne prennent
effet qu'après redémarrage de la session.

---

## Règles dures

- **Rien n'est écrit avant la confirmation de l'étape 6b.** Les étapes 0 à 6 sont
  en lecture seule, sans exception.
- **Le catalogue commande.** Aucune liste d'agents, de commandes ou de hooks n'est
  écrite en dur dans cette commande. Un composant ajouté au catalogue est pris en
  charge sans modifier ce fichier.
- **Jamais de suppression hors catalogue.** Un fichier que le catalogue ne
  référence pas n'est pas touché — c'est du travail utilisateur.
- **Jamais de suppression d'un `removable: false`.**
- **Pas de délégation.** Aucun `Task` : le wizard s'exécute en session principale.
- **Cohérence terminale.** Après application, aucun fichier conservé ne doit
  référencer un composant supprimé. Relis les commandes retenues et corrige les
  mentions orphelines (un `/review-changes` qui convoque un Sentinel supprimé
  doit être réécrit sans lui).
