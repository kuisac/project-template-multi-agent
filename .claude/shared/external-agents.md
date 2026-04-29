# Agents externes — Gepetto, Gemina, Perci

> Comment intégrer des IA non-Anthropic dans le cycle adversarial de l'équipe,
> soit via MCP (intégration directe dans Claude Code), soit via brief manuel.

---

## Pourquoi des agents externes ?

Trois raisons concrètes :

1. **Diversité de biais** — Claude, GPT, Gemini ont été entraînés différemment.
   Quand Critik valide un design et que Gepetto le challenge, le désaccord est
   informatif. Quand les deux le valident, la confiance est plus forte qu'un
   double-check Claude/Claude.

2. **Capacités spécifiques** — Gemini gère 1M tokens de contexte (utile pour
   analyser un gros corpus en une passe). Perplexity sait sourcer ses
   affirmations (utile pour la veille techno, les CVE). GPT a souvent des prompts
   plus directs sur l'architecture logicielle classique.

3. **Hygiène épistémique** — un projet entièrement piloté par une seule famille
   de modèles hérite de ses angles morts. Avoir au moins un avis externe sur
   les décisions L4 / L5 est une bonne pratique.

---

## Les trois agents externes

### Gepetto — OpenAI / GPT

**Rôle** : second avis algorithmique. Bon pour relire un design d'API, contester
une approche d'algorithmie, proposer une variante d'implémentation.
**Posture** : variable selon le brief — peut être constructeur (proposer une
solution alternative) ou contradicteur (challenger une proposition d'Archi).
**Modèle recommandé** : `gpt-5` (ou meilleur disponible) pour les sujets de
fond, `gpt-5-mini` pour le brainstorming.
**Brief template** : `.claude/OtherAI/gpt/brief-template.md`

### Gemina — Google Gemini

**Rôle** : analyse de gros corpus. Idéale quand il faut lire 200 fichiers, un
PDF de 800 pages, ou consolider plusieurs rapports en une synthèse.
**Posture** : plutôt constructeur (synthétiseur), mais peut être contradicteur
sur la cohérence inter-documents (« ces deux specs se contredisent »).
**Modèle recommandé** : `gemini-2.5-pro` pour la qualité, `gemini-2.5-flash`
pour le débit.
**Brief template** : `.claude/OtherAI/gemini/brief-template.md`

### Perci — Perplexity

**Rôle** : recherche web sourcée. Utile pour veille technologique, vérification
de CVE, comparaison d'écosystèmes, état de l'art.
**Posture** : informateur neutre. Ses retours alimentent les décisions des
autres agents — il n'arbitre jamais.
**Modèle recommandé** : `sonar-pro` (Perplexity).
**Brief template** : `.claude/OtherAI/perplexity/research-template.md`

---

## Mode A — Intégration MCP (recommandé à terme)

Tu déclares les serveurs MCP dans `.mcp.json` à la racine du projet. Claude
Code les charge au démarrage et les expose comme des outils.

### Perplexity (officiel Anthropic-compatible)

```bash
claude mcp add perplexity \
  --env PERPLEXITY_API_KEY="$PERPLEXITY_API_KEY" \
  -- npx -y @perplexity-ai/mcp-server
```

Ou en `.mcp.json` :

```json
{
  "mcpServers": {
    "perplexity": {
      "command": "npx",
      "args": ["-y", "@perplexity-ai/mcp-server"],
      "env": { "PERPLEXITY_API_KEY": "${PERPLEXITY_API_KEY}" }
    }
  }
}
```

### GPT et Gemini

Plusieurs options :

- **Composio Tool Router** — expose GPT et Gemini comme outils MCP via une
  URL HTTP unique. Setup :
  ```bash
  claude mcp add --transport http composio "https://mcp.composio.dev/.../sse" \
    --headers "X-API-Key:$COMPOSIO_API_KEY"
  ```
- **Serveur MCP communautaire multi-providers** — projets type `proxima` ou
  `claude-octopus` qui multiplexent plusieurs LLM. À évaluer selon ton seuil
  de confiance vis-à-vis du tiers.
- **Serveur MCP fait maison** — un petit serveur Node ou Python qui appelle
  l'API OpenAI/Gemini et expose des outils nommés `ask_gepetto`, `ask_gemina`.
  Plus de contrôle, plus de maintenance.

### Restriction d'accès par sub-agent

Une fois les serveurs MCP en place, tu peux restreindre l'accès dans le
frontmatter d'un sub-agent. Exemple : autoriser uniquement Sentinel à
appeler Perplexity pour les vérifs CVE.

```yaml
---
name: sentinel
tools: Read, Glob, Grep, Bash, mcp__perplexity__search
---
```

---

## Mode B — Brief manuel (le plus simple à démarrer)

Si tu n'as pas encore configuré MCP, tu peux faire collaborer les agents
externes manuellement. Workflow piloté par Pilote :

1. **Pilote demande à un agent Claude** de générer un brief structuré pour
   l'agent externe (en utilisant les templates dans `.claude/OtherAI/`).
2. **L'utilisateur colle le brief** dans l'interface de l'IA externe (ChatGPT,
   Gemini app, Perplexity).
3. **L'utilisateur récupère la réponse** et la colle dans
   `doc/reviews/external/<date>-<agent>.md`.
4. **Pilote intègre cette réponse** dans le cycle adversarial en cours
   (typiquement via `/debate` qui prendra la réponse en compte comme
   contradiction signée par Gepetto/Gemina/Perci).

L'avantage : zéro config, zéro coût supplémentaire si tu utilises déjà ces
outils en SaaS. L'inconvénient : friction de copier/coller, pas de boucle
fermée automatique.

---

## Règle d'or pour les agents externes

**Chaque IA externe doit lire la charte de l'équipe avant de répondre.**

Concrètement, tout brief doit commencer par :

> Tu vas répondre dans le cadre d'une équipe IA contradictoire dont la charte
> est ci-dessous. Lis-la avant de formuler ta réponse, puis identifie clairement
> ta posture (constructeur ou contradicteur) et le format attendu.
>
> [coller ici le contenu de `.claude/shared/team-charter.md`]

Sans ce préambule, GPT va valider poliment, Gemini va être exhaustif sans
prendre parti, Perplexity va sourcer sans tranchant. Avec, ils savent qu'ils
sont attendus sur un format précis et une posture précise.

---

## Quand appeler qui ?

| Situation | Agent externe à privilégier | Pourquoi |
|-----------|-----------------------------|----------|
| Décision L4 d'architecture critique | Gepetto en contradicteur d'Archi | Diversité de biais sur le design |
| Audit de 200+ fichiers d'un legacy | Gemina | Contexte long |
| Vérifier qu'une dépendance n'a pas de CVE récente | Perci | Web sourcé |
| Veille sur l'état de l'art d'un domaine | Perci | Recherche temps réel |
| Brainstorming d'API avant figer le contrat | Gepetto + Archi en parallèle | Comparer 2 approches |
| Synthèse multi-rapports d'audit | Gemina ou Scribe | Selon volume |
| Décision L5 produit avec impact business | Devil + Gepetto en contradicteur | Diversité d'angles produit |

---

## Persistance des contributions externes

Toute contribution d'un agent externe va dans `doc/reviews/external/` :

```
doc/reviews/external/
  YYYY-MM-DD-gepetto-<sujet>.md
  YYYY-MM-DD-gemina-<sujet>.md
  YYYY-MM-DD-perci-<sujet>.md
```

Format minimal :

```
# Contribution externe — <Agent> — <date>
**Sujet** : ...
**Posture** : Constructeur | Contradicteur | Informateur
**Brief utilisé** : .claude/OtherAI/<agent>/brief-template.md (version <hash ou date>)

## Réponse brute
<copier-coller exact>

## Synthèse pour l'équipe
<reformulation par Pilote ou Scribe pour intégration au cycle>
```
