# `.claude/wizard/` — catalogue et état d'initialisation

Ce dossier contient ce que `/init-project` sait faire, et ce qu'il a fait.

| Fichier | Rôle |
|---------|------|
| `catalog.json` | **Source de vérité.** Tout composant que le wizard peut sélectionner, activer ou retirer. |
| `catalog.schema.json` | Schéma JSON du catalogue. Documente chaque champ et contraint les valeurs. |
| `state.json` | Écrit par `/init-project` après application. Absent tant que le projet n'a pas été initialisé. |

La règle qui gouverne l'ensemble : **le wizard ne connaît que le catalogue**.
Un agent présent dans `.claude/agents/` mais absent du catalogue ne sera ni
proposé, ni supprimé — il est invisible pour le wizard. C'est ce qui permet
d'ajouter des composants sans jamais toucher à la commande `/init-project`.

---

## Ajouter un agent

1. Crée sa fiche, par exemple `.claude/agents/oscar.md`. Le plus simple est de
   copier un agent de posture équivalente : `critik.md` pour un contradicteur,
   `archi.md` pour un constructeur.
2. Ajoute son entrée dans `components` :

```json
{
  "id": "agent.oscar",
  "kind": "agent",
  "name": "Oscar",
  "path": ".claude/agents/oscar.md",
  "role": "Ingénieur SRE / exploitation",
  "posture": "constructeur",
  "model": "sonnet",
  "tags": ["observability"],
  "requires": [],
  "removable": true,
  "summary": "Supervision, SLO, runbooks, post-mortems d'incident."
}
```

3. Le `model` doit correspondre au `model:` du frontmatter de la fiche —
   c'est cette valeur que les tables de `CLAUDE.md` afficheront.
4. Ajoute son id à l'`include` des profils concernés. S'il n'apparaît dans aucun
   profil, il reste accessible via l'ajout à la carte (étape 3a du wizard).
5. Incrémente `catalogVersion`.

## Ajouter une commande

Même principe, avec `kind: "command"` et les dépendances renseignées :

```json
{
  "id": "command.incident-review",
  "kind": "command",
  "name": "/incident-review",
  "path": ".claude/commands/incident-review.md",
  "tags": ["observability"],
  "requires": ["agent.oscar"],
  "recommends": ["agent.sentinel"],
  "removable": true,
  "summary": "Oscar conduit le post-mortem d'un incident, Sentinel challenge la cause racine."
}
```

**`requires` vs `recommends`** — la distinction porte tout le mécanisme :

- `requires` = la commande est **cassée** sans ce composant. Le wizard force sa
  sélection et prévient l'utilisateur s'il venait de le retirer.
- `recommends` = la commande **fonctionne en mode dégradé**. Le wizard émet un
  avertissement et n'impose rien.

Une commande dont un `requires` manque au catalogue fait échouer
`/init-project --check`. Lance-le après chaque ajout.

## Ajouter un hook

```json
{
  "id": "hook.pre-commit-lint",
  "kind": "hook",
  "name": "Lint avant écriture",
  "path": ".claude/hooks/pre-commit-lint.sh",
  "event": "PreToolUse",
  "matcher": "Bash(git commit:*)",
  "tags": ["quality"],
  "requires": [],
  "enabledByDefault": false,
  "removable": true,
  "summary": "Refuse un commit si le linter du projet échoue."
}
```

`event` et `matcher` sont recopiés tels quels dans `.claude/settings.json` par
l'étape 7.2 du wizard. `enabledByDefault: false` = le script est livré mais non
branché ; l'utilisateur l'active pendant le dialogue ou plus tard à la main.

## Ajouter un serveur MCP

```json
{
  "id": "mcp.sonar",
  "kind": "mcp",
  "name": "Sonar (analyse statique)",
  "server": "sonar",
  "paths": [".claude/OtherAI/sonar"],
  "envVars": ["SONAR_TOKEN"],
  "tags": ["external-ai", "quality"],
  "requires": [],
  "enabledByDefault": false,
  "removable": true,
  "summary": "Analyse statique déportée, rapports de qualité de code."
}
```

`server` doit correspondre exactement à la clé dans `mcpServers` de `.mcp.json`.
`paths` liste ce qui est supprimé **avec** le serveur si l'utilisateur choisit de
le retirer plutôt que de le désactiver.

## Ajouter ou modifier une politique d'élicitation

`elicitationPolicies` décrit **combien Claude questionne l'utilisateur avant de
produire**. C'est le seul réglage du catalogue qui ne porte pas sur des fichiers
mais sur un comportement.

```json
{
  "id": "prototype",
  "label": "Prototype — construire pour faire réagir",
  "description": "Sur un besoin flou, une maquette jetable vaut mieux qu'un questionnaire.",
  "rule": "**Politique d'élicitation : `prototype`.** Tu poses au plus deux questions, puis tu construis la plus petite chose montrable…"
}
```

Le champ `rule` est du Markdown **injecté tel quel** par l'étape 7.4 du wizard
dans la zone balisée `elicitation` de `CLAUDE.md`. Rédige-le à la deuxième
personne, adressé à Pilote — c'est lui qui le lira à chaque session.

`defaultElicitationPolicy` désigne la politique présélectionnée pendant le
dialogue. Elle doit correspondre à un `id` existant, sans quoi
`/init-project --check` échoue.

> Les six zones d'ombre, elles, ne sont **pas** paramétrables : elles vivent dans
> `CLAUDE.md` § 2, hors zone balisée, parce qu'elles relèvent de la doctrine du
> projet et non de sa configuration. Une politique règle la *profondeur* de
> l'entretien, jamais ce qu'on y cherche.

## Ajouter un profil

Un profil n'est qu'une liste d'ids. Deux invariants, tous deux vérifiés par
`/init-project --check` :

- **Clôture** : si tu inclus `command.data-review`, inclus aussi `agent.data`.
- **Socle** : tout composant `removable: false` doit figurer dans l'`include`.

```json
{
  "id": "embedded",
  "label": "Embarqué / firmware",
  "description": "Cibles contraintes en mémoire et en énergie. Pas d'UI, sécurité et tests au premier plan.",
  "include": ["agent.pilote", "agent.codie", "agent.critik", "…"]
}
```

Le profil `full` utilise `includeAll: true` : il prend tout le catalogue sans
qu'on ait à le maintenir à chaque ajout. Garde-le tel quel.

---

## Vérifier le catalogue

```
/init-project --check
```

Cinq invariants sont contrôlés : unicité et forme des ids, existence des
chemins, résolution des dépendances, déclaration des tags, clôture des profils.
Aucune modification n'est faite. Lance-le systématiquement après avoir édité
le catalogue — un chemin qui ne pointe nulle part se traduirait sinon par une
suppression manquée pendant une vraie initialisation.

## Reconfigurer un projet déjà initialisé

```
/init-project --reconfigure
```

Repart de `state.json` : les réponses précédentes deviennent les valeurs par
défaut, et le wizard ne propose que le delta. C'est la voie normale pour
ajouter un spécialiste six semaines après le démarrage.

`state.json` a vocation à être **commité** : il documente la composition de
l'équipe au même titre qu'un fichier de lock.

---

## Ce que le wizard ne fera jamais

- Toucher à `.git/`.
- Supprimer un composant `removable: false` — Pilote, Codie, Critik,
  `/team-status`, le glossaire, `src/`, `doc/reviews/`.
- Supprimer un fichier que le catalogue ne référence pas. Tout ce que tu ajoutes
  hors catalogue est du travail utilisateur, et reste intact.
- Supprimer un dossier `scaffold` non vide.
- Écrire quoi que ce soit avant ta confirmation explicite du plan.
