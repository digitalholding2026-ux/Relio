# Relio — Référentiel pédagogique et documents techniques

**Cameroun · Préparation BEPC · Mathématiques 3e**

Ce dépôt est la **référence documentaire et pédagogique** de Relio. Il ne
contient **aucune fonctionnalité applicative** : ni frontend, ni backend, ni
moteur, ni intégration IA.

Les deux dépôts applicatifs sont indépendants :

| Dépôt | Contenu | Hébergement |
|---|---|---|
| [`digitalholding2026-ux/relio-frontend`](https://github.com/digitalholding2026-ux/relio-frontend) | Application Next.js | Vercel |
| [`digitalholding2026-ux/relio-backend`](https://github.com/digitalholding2026-ux/relio-backend) | API Fastify | Railway |

> Les dossiers `frontend/` et `backend/` sont des **emplacements réservés**,
> ignorés par Git. Ce dépôt ne les inclut jamais dans ses pushes.

---

## Données pédagogiques

| Fichier | Contenu | Statut |
|---|---|---|
| `data/referentiel-maths-3e-cm-2025-2026.json` | Progression annuelle : 14 leçons, 98 h, 3 trimestres, 30 semaines | `valide_avec_reserves` — 3 réserves non arbitrées |
| `data/inventaire-questions-bepc-2025-2026.json` | 35 questions BEPC 2025-2026, reliées aux leçons | 🔴 **provisoire — en attente de validation humaine** |

**Empreintes de référence (SHA-256)** — à vérifier après toute copie :

```
f766f41240335955821bb3e00a27c618299ffbc6cf34c984622025ea15dbc4f0  data/referentiel-maths-3e-cm-2025-2026.json
d74a68fb932a3a5a930997987bcbd6da2541166cc4252c4e573e2b8729607982  data/inventaire-questions-bepc-2025-2026.json
```

### 🔴 Droits d'utilisation

Les sujets et corrigés harmonisés du BEPC sont publiés par la Direction des
Examens, des Concours et de la Certification du Cameroun.

> **Les droits de reproduction ne sont pas établis.**
> Aucun énoncé, corrigé ou figure de ces documents ne doit être reproduit dans
> l'application ni publié. L'inventaire est un **outil d'analyse interne**.

Conséquence architecturale : **aucun contenu BEPC ne doit transiter vers le
client**, le frontend étant public par défaut sur Vercel.

### Documents sources conservés

| Fichier | Nature |
|---|---|
| `source-progression-maths-3e.jpg` | Document de progression annuelle d'origine |
| `BEPC 04 juin 2025.pdf` · `BEPC 2026.pdf` | Sujets officiels |
| `BEPC-MATHS-CORRIGE-2025.pdf` · `bepc 2026 corriger.pdf` | Corrigés harmonisés |

---

## Documentation conservée

Seuls les documents **courants** sont conservés. Les rapports d'étapes
antérieures ont été retirés de `docs/` le 2026-10-10 pour ne garder que l'état
utile ; ils restent consultables dans l'historique Git.

### Spécification pédagogique

| Fichier | Contenu | Statut |
|---|---|---|
| `docs/matrice-couverture-competences.md` | Couverture des 14 leçons ; objectifs documentés **vs déduits** ; questions BEPC et fiabilité | ⚠️ objectifs non validés |
| `docs/specification-diagnostic-initial.md` | Mini-évaluation du MVP : 5 questions originales, corrections, distracteurs, saisie mobile | ⚠️ non validée |
| `docs/regles-recommandation-pedagogique.md` | Règles d'interprétation, signatures d'erreurs, sondes, garde-fous, parcours | ⚠️ non validée |

> ⚠️ Ces trois documents reposent sur des **objectifs opérationnels déduits par
> un analyste**, jamais validés par un enseignant. Ils ne constituent pas une
> référence pédagogique opposable.

> 🔴 **Contenu unique :** ces documents sont le **seul exemplaire** des 26
> objectifs `OO-Lx-y`, des 5 questions `ORIG-M3-Q0n` et des 6 sondes
> `SONDE-M3-Sn`. Rien de tout cela n'existe ailleurs.

### Rapports techniques

| Fichier | Contenu |
|---|---|
| `docs/rapport-audit-fiabilite-chantier-4.md` | Audit de fiabilité après déploiement (2026-10-10) |
| `docs/rapport-final-chantier-5.md` | Corrections R1/R3/R5 + 40 tests (2026-10-10) |
| `docs/ci-workflows-chantier-5.md` | Contenu prêt à créer des workflows CI + contrôle du jeton GitHub |

---

## Outils de traitement

| Fichier | Rôle |
|---|---|
| `outils/generer-referentiel.py` | Génère le JSON du référentiel depuis la transcription |
| `outils/generer-inventaire-bepc.py` | Génère l'inventaire des questions BEPC |
| `outils/valider-referentiel.mjs` | Contrôle de cohérence du référentiel |
| `outils/valider-inventaire-bepc.mjs` | Contrôles qualité de l'inventaire |

**Aucune dépendance externe** : Python 3 (bibliothèque standard) et Node.js 18+
(`node:fs`, `node:url`, `node:path`). Aucun `npm install` nécessaire.

### Reproduire et vérifier

```bash
# Contrôles de cohérence (aucune écriture)
node outils/valider-referentiel.mjs     # attendu : code 2 (3 réserves documentées)
node outils/valider-inventaire-bepc.mjs # attendu : code 0

# Régénérer (ÉCRIT les données — à manier avec précaution)
python3 outils/generer-referentiel.py
python3 outils/generer-inventaire-bepc.py
```

Codes de sortie du validateur du référentiel :

| Code | Signification |
|---|---|
| `0` | Conforme |
| `1` | Anomalie bloquante |
| `2` | Contrôle passé, réserves à documenter — **état actuel** |

---

## Règles respectées

- **Aucune leçon inventée** — les 14 leçons et leurs volumes sont transcrits du document source.
- **Aucune compétence officielle inventée** — les champs `competences`, `prerequis`, `objectifs` existent dans le modèle mais restent **vides**, faute de document pédagogique de référence.
- **Aucune correction silencieuse** — les anomalies sont signalées, pas arbitrées.
- **Identifiants stables et techniques** — les intitulés ne servent jamais de clé.
- **Aucune dépendance IA** — JSON standard, aucun SDK, aucun appel réseau.
- **Aucune donnée d'élève collectée.**

---

## Points en attente d'arbitrage

| # | Point | Responsable |
|---|---|---|
| 1 | Droits de reproduction des documents BEPC | Propriétaire |
| 2 | Contenu attendu de la leçon 6 « Angles inscrits » — aucun objectif dérivable | Responsable pédagogique |
| 3 | Relecture des 5 questions du diagnostic par un enseignant | Responsable pédagogique |
| 4 | Les 3 réserves du référentiel (`docs/rapport-audit-fiabilite-chantier-4.md`) | Responsable pédagogique |
| 5 | Validation des objectifs opérationnels déduits | Responsable pédagogique |

---

## Confidentialité

`.env` est ignoré par Git et ne doit jamais être commité. Aucun jeton, aucune
clé d'API ne doit être écrit dans ce dépôt.

---

*Ce dépôt est la référence documentaire. Il reste distinct des dépôts
applicatifs, qui contiennent le code.*