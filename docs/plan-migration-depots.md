# Plan de migration vers deux dépôts indépendants

**Chantier** : 1
**Date** : 2026-10-10
**Statut** : 🔴 **PLAN — aucune opération de migration n'a été exécutée**

> Ce document décrit ce que le propriétaire devra faire. **Je ne l'ai pas fait et
> je ne peux pas le faire** : la création de dépôts GitHub et la configuration
> Vercel/Railway dépassent mes capacités.

---

## 1. Réalité à garder en tête

Il n'y a **rien à découper**. Le dépôt actuel ne contient aucun code
applicatif. Le « plan de migration » consiste donc à :

1. **créer** deux dépôts vides ;
2. **transposer une seule donnée** vers le backend ;
3. laisser le dépôt `Relio` **intact**.

| Ce qui est transféré | Ce qui ne l'est pas |
|---|---|
| 1 fichier JSON (144 Ko) | Aucun code source |
| — | Aucun PDF, aucune image, aucun script |

---

## 2. Destination de chaque fichier

### 2.1 Fichiers suivis par Git (22)

| # | Chemin | Catégorie | Destination | Motif |
|---|---|---|---|---|
| 1 | `README.md` | D | **Relio** (inchangé) | Décrit ce dépôt |
| 2 | `.gitignore` | G | **Relio** + **recopié/adapté** dans les 2 nouveaux | Secrets et build |
| 3 | `source-progression-maths-3e.jpg` | E | **Relio** | Document source, traçabilité |
| 4 | `BEPC 04 juin 2025.pdf` | E | **Relio** 🔴 | Droits non établis |
| 5 | `BEPC 2026.pdf` | E | **Relio** 🔴 | Droits non établis |
| 6 | `BEPC-MATHS-CORRIGE-2025.pdf` | E | **Relio** 🔴 | Droits non établis |
| 7 | `bepc 2026 corriger.pdf` | E | **Relio** 🔴 | Droits non établis |
| 8 | `data/referentiel-maths-3e-cm-2025-2026.json` | E | **Backend** (seed, lecture seule) | Seule donnée applicative |
| 9 | `data/inventaire-questions-bepc-2025-2026.json` | E | **Relio** uniquement 🔴 | Contenu BEPC + non validé |
| 10 | `outils/generer-referentiel.py` | F | **Relio** | Chaîne de production |
| 11 | `outils/generer-inventaire-bepc.py` | F | **Relio** | Chaîne de production |
| 12 | `outils/valider-referentiel.mjs` | F | **Relio** | Contrôle qualité |
| 13 | `outils/valider-inventaire-bepc.mjs` | F | **Relio** | Contrôle qualité |
| 14 | `docs/progression-maths-3e-2025-2026.md` | D | **Relio** | Documentation |
| 15 | `docs/rapport-final-mission.md` | D | **Relio** | Rapport |
| 16 | `docs/rapport-controle-donnees.md` | D | **Relio** | Rapport |
| 17 | `docs/incoherences.md` | D | **Relio** | Rapport |
| 18 | `docs/integration-backoffice.md` | D | **Relio** | Proposition |
| 19 | `docs/analyse-bepc-2025-2026.md` | D | **Relio** | Analyse |
| 20 | `docs/couverture-programme-bepc.md` | D | **Relio** | Analyse |
| 21 | `docs/anomalies-documents-bepc.md` | D | **Relio** | Analyse |
| 22 | `docs/rapport-final-mission-2.md` | D | **Relio** | Rapport |

**Bilan : 21 fichiers sur 22 restent dans `Relio`. Un seul est copié.**

### 2.2 Nouveaux fichiers à créer par le propriétaire

| Dépôt | Fichier | Contenu |
|---|---|---|
| `relio-frontend` | `README.md` | Description,stack, commandes |
| `relio-frontend` | `.env.example` | `NEXT_PUBLIC_API_URL=` |
| `relio-backend` | `README.md` | Description, stack, seed |
| `relio-backend` | `.env.example` | `PORT=`, `DATABASE_URL=`, `CORS_ORIGINS=`, `NODE_ENV=` |
| `relio-backend` | `data/referentiel-*.json` | Copie du référentiel |
| `relio-backend` | `data/referentiel-*.sha256` | Empreinte d'intégrité |
| Les 2 | `.gitignore` | Adapté à chaque stack |

### 2.3 Fichiers NON transférés (hors dépôt)

| Fichier | Raison |
|---|---|
| `.env` | 🔴 **Secret.** Ne doit jamais quitter la machine ni être commité |
| `outils/__pycache__/*.pyc` | Cache Python, ignoré par Git |

---

## 3. Séquence d'exécution

> Chaque étape est **indépendante** et **réversible**. Aucune ne dépend d'une
> opération irréversible.

### Étape 0 — Prérequis

| # | Prérequis | Vérification |
|---|---|---|
| P1 | Accès au compte GitHub propriétaire | Action manuelle |
| P2 | Compte Vercel lié au compte GitHub | Action manuelle |
| P3 | Compte Railway lié au compte GitHub | Action manuelle |
| P4 | Décision D-ARCHI-1 (Fastify vs NestJS) | À trancher |
| P5 | Node.js 18+ et npm disponibles | Action manuelle |
| P6 | `Relio` sauvegardé (tag Git) | `git tag audit-chantier-1` |

> 🟢 **Étape 0 conseillée :** créer un tag Git `audit-chantier-1` sur `Relio`
> **avant toute opération**. Le dépôt est alors restaurable à l'identique.

### Étape 1 — Créer les deux dépôts *(propriétaire)*

| Action | Où | Résultat attendu |
|---|---|---|
| Créer `relio-backend` | GitHub, dépôt **privé** | Dépôt vide accessible |
| Créer `relio-frontend` | GitHub, dépôt **privé ou public** | Dépôt vide accessible |

> ⚠️ **Recommandation : `relio-backend` en PRIVÉ.** Il contiendra la donnée de
> seed et, plus tard, des profils d'élèves. **Le frontend peut rester public** :
> il ne contient aucune donnée.

### Étape 2 — Initialiser le backend

```bash
# LOCAL, à faire par le propriétaire
mkdir relio-backend && cd relio-backend
git init
git remote add origin https://github.com/<propriétaire>/relio-backend.git
mkdir data
cp ../Relio/data/referentiel-maths-3e-cm-2025-2026.json data/
sha256sum data/referentiel-maths-3e-cm-2025-2026.json > data/referentiel.sha256
```

**Contrôle** : le SHA-256 doit être `f766f412…`.

### Étape 3 — Initialiser le frontend

```bash
mkdir relio-frontend && cd relio-frontend
git init
git remote add origin https://github.com/<propriétaire>/relio-frontend.git
```

**Aucun fichier de `Relio` n'y est copié.**

### Étape 4 — Écrire le code

> 🔴 **Nécessite la validation du présent audit.** Le chantier 2 commencera ici.

Frontend : squelette Next.js. Backend : squelette API + moteur de
diagnostic en port pur, testable sans base.

### Étape 5 — Connecter les plateformes *(propriétaire)*

Voir `docs/plan-deploiement-vercel-railway.md`.

### Étape 6 — Vérifications post-migration

Voir § 7.

---

## 4. Adaptations de chemins nécessaires

| Source | Chemin d'origine | Destination | Adaptation |
|---|---|---|---|
| Référentiel | `data/referentiel-maths-3e-cm-2025-2026.json` | `relio-backend/data/…` | **Aucune** (chemin identique) |
| Scripts (restés en Relio) | `outils/*.py`, `outils/*.mjs` | — | **Aucune** — ils ne bougent pas |
| Adresse de l'API | — | `relio-frontend` | `.env.local` avec `NEXT_PUBLIC_API_URL` |
| Origines autorisées | — | `relio-backend` | `.env` avec `CORS_ORIGINS` |

> ✅ **Point favorable :** les scripts restent dans `Relio` et continue de
> fonctionner **sans aucune modification de chemin**. Aucun des 4 scripts ne
> référence un chemin qui change.

---

## 5. Dépendances à réinstaller

| Dépôt | Action |
|---|---|
| `Relio` | **Aucune** — les 4 scripts n'ont aucune dépendance externe |
| `relio-frontend` | `npm install` — dépendances déclarées dans le nouveau `package.json` |
| `relio-backend` | `npm install` — idem |

> 🟢 **Aucun `npm install` n'est nécessaire aujourd'hui** : ni `Relio` ni les
> nouveaux dépôts n'ont encore de manifeste.

**Environnements requis :** Python 3 (stdlib) et Node.js 18+ (builtins) pour les
scripts de `Relio`. C'est tout.

---

## 6. Risques de rupture

| # | Risque | Probabilité | Impact | Parade |
|---|---|---|---|---|
| M1 | **Fuite BEPC via le bundle frontend** | Moyenne | 🔴 Juridique | Respecter § 7 de `architecture-cible.md` ; aucun import de l'inventaire |
| M2 | Confusion « NestJS existe » → on ne part pas d'une base propre | Élevée | 🟡 | Le dire explicitement au propriétaire avant d'écrire du code |
| M3 | Copier l'inventaire « au cas où » dans le backend | Moyenne | 🟠 | Règle : le backend reçoit **le référentiel seul** |
| M4 | Le frontend ne démarre pas sans API → écran vide | Élevée | 🟢 | Prévoir un état de chargement et un message clair |
| M5 | Référentiel avec 3 réserves non arbitrées exposé à l'élève | Élevée | 🟠 | Reprendre les réserves mission 1 avant la mise en ligne |
| M6 | Objectifs de mission 3 non validés → questions hors programme | Élevée | 🟠 | Faire relire par un enseignant (décision D4 mission 3) |
| M7 | `Relio` modifié par inadvertance pendant la migration | Faible | 🟡 | Tag Git + discipline de copie en lecture seule |
| M8 | Dépôt créé en public par erreur (données élèves) | Faible | 🔴 | `relio-backend` en **privé** dès l'étape 1 |
| M9 | Pas de CI → régressions silencieuses | Élevée | 🟡 | Ajouter une CI minimale (tests + validateur) |
| M10 | Railway en free plan avec PostgreSQL éphémère | Moyenne | 🔴 | Vérifier le mode de persistance **avant** le lancement |

---

## 7. Vérifications après migration

### 7.1 Intégrité de la donnée

| # | Vérification | Attendu |
|---|---|---|
| V1 | SHA-256 du référentiel dans `relio-backend` | `f766f41240335955821bb3e00a27c618299ffbc6cf34c984622025ea15dbc4f0` |
| V2 | 14 leçons présentes | ✅ |
| V3 | Somme des `volume_horaire_h` | **98 h** |
| V4 | `status` | `valide_avec_reserves` |
| V5 | Le référentiel **dans Relio est inchangé** | `git diff` vide |

### 7.2 Absence de fuite BEPC

| # | Vérification | Attendu |
|---|---|---|
| V6 | `inventaire-*.json` absent du dépôt frontend | ✅ absent |
| V7 | `inventaire-*.json` absent du dépôt backend | ✅ absent |
| V8 | Aucun `*.pdf` dans l'un ou l'autre dépôt | ✅ absent |
| V9 | Aucun `*.pdf` dans `public/` du frontend | ✅ absent |
| V10 | Bundle frontend : `grep -ri "bepc"` | **Aucune transcription d'énoncé** |

### 7.3 Secrets

| # | Vérification | Attendu |
|---|---|---|
| V11 | `.env` commité ? | ❌ non |
| V12 | `.env` dans l'historique ? | ❌ non |
| V13 | Secrets dans un bundle frontend | ❌ aucun |
| V14 | `*.pem`, `*.key`, `credentials.json` | ❌ aucun |

### 7.4 Fonctionnel *(à faire après le chantier 2)*

| # | Vérification | Attendu |
|---|---|---|
| V15 | `GET /health` | `200` |
| V16 | `GET /referentiel/lecons` | 14 leçons |
| V17 | `GET /exercices/diagnostic` | 5 questions **originales** |
| V18 | Parcours complet mini-diagnostic | Fonctionnel de bout en bout |
| V19 | CORS : origine non autorisée | **Bloquée** |
| V20 | CORS : origine autorisée | **Acceptée** |

> ⚠️ V15–V20 sont **non applicables à ce chantier** : aucun code n'existe.

---

## 8. Procédure de retour arrière

> Le chantier 1 n'a **rien déplacé**. Le retour arrière est donc déjà acquis.

### 8.1 Retour arrière immédiat

| Situation | Action | Impact |
|---|---|---|
| Un dépôt a été mal configuré | Supprimer le dépôt GitHub | **Aucun** — `Relio` intact |
| Une donnée a été copiée à tort | `git revert` ou `git reset` dans le nouveau dépôt | **Aucun** sur `Relio` |
| Un secret a été poussé par erreur | Révoquer le secret **avant** toute autre chose | Révoquer ≠ supprimer l'historique |

> 🔴 **Si un secret est poussé par erreur, la rotation est prioritaire.**
> Supprimer le fichier ne suffit pas : il reste dans l'historique.

### 8.2 Restauration de `Relio`

`Relio` n'est modifié par aucune étape de ce plan. En cas de doute :

```bash
cd Relio
git status                 # doit être propre
git log --oneline -5
git checkout audit-chantier-1   # si le tag a été créé (étape 0)
```

### 8.3 Ce qui rend le plan réversible

| Garantie | Raison |
|---|---|
| Aucune suppression | Rien à perdre |
| Aucun déplacement | `Relio` reste la source |
| Aucune réécriture d'historique | Git reste fiable |
| Un seul fichier copié | Superficie minimale |
| Dépôts créés vides d'abord | Créer ≠ déplacer |

---

## 9. Actions manuelles réservées au propriétaire

> **Je n'ai exécuté aucune de ces opérations et je ne peux pas les exécuter.**

| # | Action | Où | Préalable | Preuve de succès |
|---|---|---|---|---|
| A1 | Créer `relio-backend` (privé) | GitHub | Compte propriétaire | Dépôt visible, vide |
| A2 | Créer `relio-frontend` | GitHub | Compte propriétaire | Dépôt visible |
| A3 | Copier le référentiel | Local + push | A1 | SHA-256 conforme à V1 |
| A4 | Configurer le projet Vercel | Vercel | A2 | URL de déploiement |
| A5 | Définir `NEXT_PUBLIC_API_URL` | Vercel | Backend déployé | Build vert |
| A6 | Créer le service Railway | Railway | A1 | Service actif |
| A7 | Créer la base PostgreSQL | Railway | A6 | Base créée, hors free éphémère |
| A8 | Définir `DATABASE_URL`, `CORS_ORIGINS` | Railway | A7 | API démarre |
| A9 | Vérifier les droits BEPC | Direction des Examens (CM) | — | Réponse écrite |
| A10 | Faire relire les questions par un enseignant | Interne | — | Validation écrite |
| A11 | **Révoquer et régénérer `GITHUB_TOKEN`** | GitHub | — | Ancien jeton invalide |
| A12 | Tag `audit-chantier-1` | Git local | — | Tag présent |

---

## 10. Ordre recommandé

```
0.  Relire ce plan + les 5 livrables
1.  Trancher D-ARCHI-1 (Fastify vs NestJS)
2.  Tag audit-chantier-1 sur Relio        ← point de retour arrière
3.  A11  révoquer GITHUB_TOKEN            ← sécurité, indépendant
4.  A1/A2  créer les 2 dépôts
5.  A3  copier le référentiel + SHA
6.  A6/A7  Railway + PostgreSQL
7.  A4/A5  Vercel + variables
8.  Écrire le backend (moteur de diagnostic)
9.  Écrire le frontend
10. Lancer les vérifications V1–V20
```

> Les étapes 8 et 9 relèvent du **chantier 2** et ne doivent pas commencer
> avant validation explicite du présent audit.

---

*Documents liés : `docs/audit-migration-architecture.md`,
`docs/architecture-cible.md`, `docs/plan-deploiement-vercel-railway.md`.*