# AUDIT COMPLET — RELIO

**Date de l'audit :** 2026-10-11
**Périmètre :** 3 dépôts Git — `digitalholding2026-ux/Relio` (racine), `relio-backend`, `relio-frontend`
**Méthode :** lecture des sources, exécution réelle des builds et des suites de tests, requêtes HTTP contre les déploiements publics, grep exhaustif.
**Règle appliquée :** uniquement des faits constatés. Aucune recommandation, aucune proposition de chantier.

---

## 1. RÉSUMÉ EXÉCUTIF

1. Trois dépôts Git distincts et fonctionnels, clonés et vérifiés. Le dépôt racine ignore `/frontend/` et `/backend/`.
2. Le backend expose **8 routes** Fastify, toutes fonctionnelles, sans base de données, sans authentification, sans rate limiting.
3. Le frontend expose **4 routes** Next.js : `/`, `/parcours`, `/parcours/[id]`, `/design-system`. `/design-system` renvoie **404 en production** (prérendue en erreur).
4. Builds : `next build` ✅ (24,4 s), `tsc --project` ✅, `tsc --noEmit` ✅ sur les deux dépôts, `npm ci` ✅ sans vulnérabilité sur les deux.
5. Tests exécutés : **307 backend / 100 % passent**, **119 logique + 136 UI frontend / 100 % passent**. Aucun test désactivé, aucun `.skip`.
6. Les deux déploiements publics répondent en HTTP 200 (Railway et Vercel). Le backend en production renvoie `status: "mvp-pedagogique"` et `anneeScolaire.debut: "2026-09-07"`.
7. Le design system (14 composants, ~1 100 lignes, 300 lignes de tests) **n'est utilisé nulle part hors de sa propre page de catalogue**.
8. Aucun secret n'est exposé côté client. 7 motifs de secret sont vérifiés automatiquement par un test d'architecture.
9. Aucun contrôle automatique n'existe sur le CSS applicatif : les contrôles a11y et de budget CSS ne s'appliquent qu'au design system.
10. Le backend ne persiste rien : aucune dépendance base de données, aucun `DATABASE_URL` lu.
11. Le dépôt racine documente 16 rapports de chantier ; 10 d'entre eux ne sont pas référencés par son README, qui décrit un état antérieur.
12. `POST /api/v1/suivi` est implémentée, testée et annoncée par l'API, mais absente de `openapi.yaml` et de `docs/CONTRAT-API.md`.
13. Le `README.md` du backend décrit un « socle vide » : 12 de ses affirmations sont contredites par son propre code.
14. Le budget CSS réel est de 6,98 Ko gzip pour un seuil de 30 Ko ; le script de contrôle existe mais n'est branché ni dans la CI ni dans le build.
15. Aucun `TODO`, `FIXME` ou `HACK` dans le code des deux dépôts. Aucun code commenté laissé en place.

---

## 2. TABLEAU « ÉTAT PAR MODULE »

| Module | État | Preuve | Remarque |
|---|---|---|---|
| **Racine — données** | 🟢 Fichier présent | `data/referentiel-…json` 43 364 o, `data/inventaire-…json` 94 874 o | SHA-256 du README **recalculés : exacts** |
| **Racine — outils** | 🟢 Fonctionnels | `node outils/valider-referentiel.mjs` → code 2 ; `valider-inventaire-bepc.mjs` → code 0 | Codes conformes à ce qu'annonce le README |
| **Racine — docs** | 🟡 16 fichiers, périmés | 10 rapports non listés dans le README | README décrit l'état avant le chantier 6 |
| **Racine — PDF sources** | 🟡 Versionnés publiquement | 4 PDF, 2,03 Mo + 1 JPG 384 Ko | Droits de reproduction déclarés « non établis » par le README lui-même |
| **Racine — CI** | 🔴 Absente | `ls .github` → inexistant | Aucune automatisation sur le dépôt racine |
| **Backend — config** | 🟢 | `src/config.ts` valide 4 var au démarrage, exit si invalide | `ANNEE_SCOLAIRE_DEBUT` et `DATE_NAVIGATION_TEST` lues mais absentes de `.env.example` |
| **Backend — CORS** | 🟢 | `src/plugins/cors.ts` liste blanche, journalisée | `maxAge: 600`, `credentials: false`, méthodes GET/POST/OPTIONS |
| **Backend — gestion d'erreurs** | 🟢 | `src/plugins/error-handler.ts` neutralise les 4xx Fastify | Le 404 réinjecte method + url bruts dans le message |
| **Backend — rate limiting** | 🔴 Absent | Aucune dépendance, aucun code | — |
| **Backend — authentification** | 🔴 Absente | Aucun header lu dans `src/routes/` | — |
| **Backend — schémas JSON** | 🔴 Absents | `grep 'schema:' src/routes/` → 0 | `openapi.yaml` déclare des schémas non appliqués |
| **Backend — base de données** | 🔴 Inexistante | `grep pg\|prisma\|sqlite\|mysql\|redis` → 0 occurrence | `DATABASE_URL` commentée dans `.env.example` |
| **Backend — parcours (6 routes)** | 🟢 | `src/routes/parcours.ts` 476 l., 53 tests | Garde calendrier appliquée par un point unique |
| **Backend — moteur de calcul** | 🟢 | `algebre.ts`, `analyseur-expression.ts` (491 l.) en `bigint` exact | Aucune comparaison de chaînes |
| **Backend — correction 4 axes + D5** | 🟢 | `contenu/correction.ts` 504 l., 23 tests | `tutorat.ts` 579 l., échelle d'aide déterministe, aucune IA |
| **Backend — progression** | 🟢 | `lib/progression.ts` 144 l., 15 tests | Fonction pure, sans persistance |
| **Backend — suivi** | 🟢 | `lib/suivi.ts` 221 l., 14 tests | Fonction pure, sans persistance |
| **Backend — documentation API** | 🔴 Incohérente | `openapi.yaml` ne contient pas `/suivi` ; `README.md` obsolète sur 12 points | §4.2 du contrat décrit un 422 que le code ne produit pas |
| **Frontend — `/`** | 🟢 | Rendue 200, 20 520 o de HTML | Sections « parcours » et « fonctionnalités » en **données en dur** |
| **Frontend — `/parcours`** | 🟢 | Serveur, `force-dynamic`, appelle `GET /api/v1/parcours` | Texte utilisateur : « Le service de exercices n'est pas configuré » (faute d'accord) |
| **Frontend — `/parcours/[id]`** | 🟢 | Rendue dynamique, appelle 4 endpoints | `params.id` non validé ; pas de `notFound()` |
| **Frontend — `/design-system`** | 🔴 404 en production | Requête réelle : HTTP 404 ; `.next/server/app/design-system.html` = `<html id="__next_error__">` | Page prérendue en erreur au build ; la garde env ne s'exécute pas dessus |
| **Frontend — design system** | 🔴 Non adopté | `grep 'components/ds' src/` → 1 seul fichier : le catalogue lui-même | 14 composants + 17 CSS orphelins d'usage applicatif |
| **Frontend — `globals.css`** | 🟡 851 l., deux systèmes coexistent | 2 déclarations `.bouton` (l.303 et l.477) ; la 2ᵉ écrase la 1ʳᵉ | `.bouton` n'utilise **aucune** variable `--relio-*` de `tokens.css` |
| **Frontend — `ClavierMath`** | 🟡 | `onPointerDown` sans `onClick` (`ClavierMath.tsx:188`) | Les 25 touches sont inopérantes au clavier physique |
| **Frontend — `Exercice.tsx`** | 🟡 463 l., non testée | Aucun test de rendu sur aucun des 4 composants métier | Journal localStorage + envoi intégral à `/suivi` |
| **Frontend — API client** | 🟢 | `lib/api.ts` 13 tests, `lib/parcours.ts` 17 tests | `cache: 'no-store'` sur les 6 requêtes ; timeouts 5 s et 8 s |
| **Frontend — journal local** | 🟢 | `lib/observations.ts` 15 tests | `relio.observations.v1`, plafond 500, effaçable par l'élève |
| **Frontend — secrets client** | 🟢 | 5 lectures de `process.env`, toutes côté serveur | `next.config.ts` → `env: {}`, `poweredByHeader: false` |
| **Frontend — en-têtes HTTP** | 🟡 | 3 en-têtes posés ; HSTS ajouté par Vercel en prod | **Aucune CSP**, aucun `Permissions-Policy` |
| **Frontend — build** | 🟢 | First Load JS partagé : 103 Ko ; `/` = 107 Ko | Aucune police distante, aucune image bitmap, aucun script tiers |
| **Frontend — CSS** | 🟢 / 🟡 | 30,8 Ko bruts → **6,98 Ko gzip** pour 30 Ko de budget | Script de contrôle **non branché** dans la CI |
| **Frontend — CI** | 🟡 | `ci.yml` : typecheck + tests + build, `npm audit` en `continue-on-error` | Aucun lint, aucun test e2e, aucun test de rendu applicatif, pas de Dependabot |
| **Déploiement** | 🟢 En ligne | Railway `/health` 200 ; Vercel `/` 200 | Uptime backend observé : 2 416 s (≈ 40 min) au moment de l'audit |

---

## 3. SECTION 1 — CARTOGRAPHIE DES DÉPÔTS

### 3.1 Dépôt racine `Relio`

**État Git :** 25 commits, branche `main`, tous datés du **2026-10-10** (fenêtre ~11:00 → 23:46 UTC). Dernier commit : `6630a9d docs(chantier-7.7): rapport final, clavier, verdicts et écritures`. Working tree propre.

**Arborescence (hors `.git`) :**

```
/config/Relio/
├── README.md                          154 l. — dépôt documentaire : aucun code applicatif, 2 JSON de données, 4 PDF sources, 4 scripts
├── .gitignore                          36 l. — ignore /frontend/ et /backend/ (l.12-13)
├── data/
│   ├── referentiel-maths-3e-cm-2025-2026.json      43 364 o — 3 trimestres, 9 mois, 30 semaines, 14 leçons (98 h), 14 régulations, 1 révision, 44 entrées de séquence
│   └── inventaire-questions-bepc-2025-2026.json   94 874 o — 35 questions (17 en 2025, 18 en 2026), couverture par leçon, contrôles
├── docs/                               16 fichiers .md — 3 spécifications pédagogiques + 13 rapports de chantier
├── outils/
│   ├── generer-referentiel.py         13 939 o — Python 3 stdlib ; transcrit en dur le tableau de progression du JPG source
│   ├── generer-inventaire-bepc.py     46 032 o — Python 3 stdlib ; métadonnées des 2 sessions + 35 questions ; écrit le JSON
│   ├── valider-referentiel.mjs        13 668 o — Node ESM (node:fs/url/path) ; clés étrangères, somme des volumes horaires, découpage
│   └── valider-inventaire-bepc.mjs    12 274 o — Node ESM ; sources, leçons, barèmes recalculés (20 pt/session)
├── BEPC 04 juin 2025.pdf              247 397 o
├── BEPC 2026.pdf                      326 256 o
├── BEPC-MATHS-CORRIGE-2025.pdf        723 182 o
├── bepc 2026 corriger.pdf             720 116 o
└── source-progression-maths-3e.jpg    384 414 o
```

**Exécution réelle des validateurs (lecture seule) :**

| Script | Code de sortie | Attendu d'après README:105-106 | Conforme |
|---|---|---|---|
| `valider-referentiel.mjs` | 2 | 2 | ✅ |
| `valider-inventaire-bepc.mjs` | 0 | 0 | ✅ |

**Empreintes SHA-256 des 2 JSON** : recalculées, **identiques** à celles publiées dans `README.md:31-32`.

**Dépendances :** aucune. Python 3 stdlib et Node 18+ (`node:fs`, `node:url`, `node:path` uniquement).

**Scripts npm :** aucun (`package.json` n'existe pas à la racine).

### 3.2 Dépôt `relio-backend`

**État Git :** HEAD `e425722 fix(tutorat): deux messages restaient dans l'ancien registre`. Working tree propre.

**Arborescence :**

```
/config/Relio/backend/
├── package.json          31 l.  — 2 dépendances prod, 3 dev
├── openapi.yaml         536 l.  — OpenAPI 3.1, 7 routes documentées
├── tsconfig.json                 — strict, noUncheckedIndexedAccess, ESM NodeNext
├── tsconfig.build.json  135 o
├── .env.example          32 l.  — 4 variables actives, 2 commentées
├── README.md            180 l.
├── .github/workflows/ci.yml  69 l.
├── docs/CONTRAT-API.md  296 l.  — contrat d'intégration, version 2.0.0
├── src/                          — 4 431 lignes au total
│   ├── server.ts         56 l.  — point d'entrée, arrête le process sur ConfigError, SIGTERM/SIGINT, écoute 0.0.0.0:PORT
│   ├── app.ts            35 l.  — construit Fastify sans ouvrir de port (testable via app.inject), trustProxy, niveau de log
│   ├── config.ts         88 l.  — lecture + validation stricte de PORT, HOST, NODE_ENV, CORS_ORIGINS
│   ├── plugins/
│   │   ├── cors.ts       49 l.  — liste blanche depuis CORS_ORIGINS ; origine inconnue → callback(null, false)
│   │   └── error-handler.ts 65 l.  — ApiError / 4xx Fastify neutralisés / 500 générique + 404 commun
│   ├── routes/
│   │   ├── index.ts      17 l.  — enregistre health, v1, parcours
│   │   ├── health.ts      9 l.  — ré-export pur de v1.ts (import redondant dans index.ts)
│   │   ├── v1.ts         81 l.  — /health, /api/v1, 8 endpoints annoncés
│   │   └── parcours.ts  476 l.  — les 6 routes métier + gardes calendrier + validation manuelle des corps
│   ├── lib/
│   │   ├── algebre.ts                 118 l.  — rationnels exacts sur bigint
│   │   ├── analyseur-expression.ts    491 l.  — lexer Unicode, parseur descendant, polynômes exacts, DEGRE_MAX=16
│   │   ├── analyseur-reponse.ts       330 l.  — saisie → objet-valeur typé (forme conservée)
│   │   ├── calendrier.ts             110 l.  — position dans l'année scolaire (30 semaines), ouverture des blocs
│   │   ├── errors.ts                   40 l.  — classe ApiError, ErrorCode, toApiErrorBody
│   │   ├── progression.ts             144 l.  — règle des trois ; jamais de non_acquis, jamais de niveau global
│   │   └── suivi.ts                   221 l.  — difficultés par objectif,fk regroupement par exercice, nb d'aides
│   └── contenu/
│       ├── types.ts                  126 l.  — modèle + vocabulaire fermé STATUTS_REPONSE
│       ├── blocs.ts                  105 l.  — 3 blocs, 5 objectifs, semaines d'ouverture S1/S5/S10
│       ├── exercices.ts              337 l.  — 12 exercices (6 B1, 3 B2, 3 B3), pièges documentés
│       ├── correction.ts             504 l.  — 4 axes (justesse, forme, achèvement, verdict D5), message élève
│       ├── aides.ts                  285 l.  — textes d'aide par objectif et par signature, sans identifiant technique
│       ├── tutorat.ts                579 l.  — échelle d'aide déterministe 3 niveaux, 8 catégories de difficulté
│       ├── egalite.ts                141 l.  — extraction du membre réponse dans « A = 2x + 1 »
│       └── signatures.ts              48 l.  — 12 signatures d'erreur + leçons candidates
└── test/                              — 4 602 lignes, 13 fichiers, 307 tests
    ├── api.test.ts          322 l. / 27 tests   ├── parcours.test.ts       916 l. / 53 tests
    ├── tutorat.test.ts      454 l. / 29 tests   ├── decision-d5.test.ts    372 l. / 23 tests
    ├── aides.test.ts        377 l. / 24 tests   ├── correction.test.ts     331 l. / 23 tests
    ├── egalite.test.ts      229 l. / 26 tests   ├── algebre.test.ts        186 l. / 20 tests
    ├── langage-simple.test.ts 295 l. / 14 tests ├── suivi.test.ts          188 l. / 14 tests
    ├── contenu.test.ts      526 l. / 20 tests   ├── calendrier.test.ts     263 l. / 19 tests
    └── progression.test.ts  143 l. / 15 tests
```

**Volumétrie :** 37 fichiers `.ts`, 3 `.json`, 2 `.md`, 1 `.yml`. 4 431 lignes de code applicatif, 4 602 lignes de tests, 69 lignes de CI.

**Dépendances de production (2) :**

| Paquet | Version | Rôle |
|---|---|---|
| `fastify` | `^5.2.0` | Serveur HTTP, routeur, logger Pino intégré |
| `@fastify/cors` | `^10.0.1` | En-têtes CORS en liste blanche |

**Dépendances de développement (3) :** `@types/node ^22.10.2` (types), `tsx ^4.19.2` (exécution TS + runner de test), `typescript ^5.7.2` (compilateur).

**Scripts npm (5) — effet réel :**

| Script | Commande | Effet observé |
|---|---|---|
| `build` | `tsc --project tsconfig.build.json` | ✅ exit 0, produit `dist/` |
| `dev` | `tsx watch src/server.ts` | Rechargement à chaud |
| `start` | `node dist/server.js` | Démarre depuis le build |
| `test` | `node --import tsx --test test/*.test.ts` | ✅ **307 tests, 307 passent, 0 échec** |
| `typecheck` | `tsc --noEmit` | ✅ exit 0 |

**Versions :** Node `v20.20.2` (local), npm `10.8.2`, TypeScript `5.7.x` (résolu par `^5.7.2`), Fastify `5.2.x` (résolu par `^5.2.0`). La CI utilise Node 22.

### 3.3 Dépôt `relio-frontend`

**État Git :** HEAD `0b36123 fix(clavier): le clavier ne recouvre plus le texte de l'application`. Working tree propre.

**Arborescence :**

```
/config/Relio/frontend/
├── package.json           990 o   — 3 dépendances prod, 7 dev
├── next.config.ts        1086 o   — 33 l.
├── tsconfig.json          614 o   — strict + noUncheckedIndexedAccess
├── vitest.config.mts                — 37 l.
├── DESIGN_SYSTEM.md               — 10 284 o
├── README.md                       — 8 931 o
├── .env.example          1591 o   — 1 seule variable
├── .github/workflows/ci.yml   71 l.
├── scripts/verifier-poids-css.mjs  60 l. — budget 30 Ko gzip
└── src/                            — 9 694 lignes au total
    ├── app/
    │   ├── layout.tsx              29 l. — lang="fr", metadata, viewport, importe tokens.css puis globals.css
    │   ├── globals.css            851 l. — feuille APPLICATIVE (voir §5)
    │   ├── page.tsx               184 l. — accueil serveur, force-dynamic, 4 sections, ApiStatus
    │   ├── parcours/
    │   │   ├── page.tsx            74 l. — serveur, force-dynamic, délègue à ParcoursServeur
    │   │   └── [id]/page.tsx       52 l. — serveur, params non validés, passe exerciceId
    │   └── design-system/
    │       ├── page.tsx            45 l. — garde NODE_ENV/DESIGN_SYSTEM_ENABLED → notFound()
    │       ├── PageDesignSystem.tsx 564 l. — 'use client', catalogue visuel
    │       └── design-system.module.css 249 l. — seule feuille à breakpoints 768px
    ├── components/
    │   ├── ApiStatus.tsx           96 l. — sonde GET /api/v1 au navigateur
    │   ├── ClavierMath.tsx        199 l. — clavier custom, onPointerDown
    │   ├── Exercice.tsx           463 l. — écran d'exercice complet, 6 useState
    │   ├── ParcoursServeur.tsx     97 l. — rendu serveur des blocs
    │   ├── parcours.ts             48 l. — 5 étapes marketing EN DUR
    │   └── ds/                            — 14 composants + 14 .module.css + base + tests + barrel
    ├── design/
    │   ├── tokens.ts              304 l. — source de vérité TS (palettes, échelles, OMBRES, RUPTURES)
    │   ├── tokens.css             191 l. — ~90 variables --relio-*, 3 modes
    │   ├── contraste.ts            85 l. — WCAG 2.1 : versRgb, luminanceRelative, rapportContraste
    │   ├── setup.ts                15 l. — afterEach(cleanup)
    │   ├── tokens.test.ts         278 l. / 21 tests
    │   └── accessibilite.test.ts  196 l. / 11 tests (statiques, DOSSIER = src/components/ds)
    ├── hooks/
    │   ├── useHauteurClavierSysteme.ts      93 l. — visualViewport → --relio-clavier-systeme
    │   └── useHauteurClavierSysteme.test.tsx 136 l. / 6 tests
    └── lib/
        ├── api.ts             97 l. / 13 tests   — GET /api/v1, timeout 5 s, AbortController
        ├── parcours.ts       231 l. / 17 tests   — 5 endpoints, DELAI_MS = 8000
        ├── clavier.ts        464 l. / 47 tests   — logique pure, 3 dispositions de touches
        ├── observations.ts   233 l. / 15 tests   — journal localStorage, plafond 500
        ├── tutorat.ts        112 l. / 14 tests   — types + libellés, aucun appel réseau
        ├── navigation.test.ts 230 l. / 7 tests   — test d'architecture (scanne src/)
        └── securite.test.ts   164 l. / 6 tests   — test d'architecture (scanne le dépôt)
```

**Volumétrie :** 27 `.tsx`, 22 `.ts`, 18 `.css`, 2 `.md`, 2 `.json`, 1 `.yml`, 1 `.mjs` (hors `package-lock.json`). 9 694 lignes dans `src/`, 59 dans `scripts/`, 69 dans `.github/`.

**Dépendances de production (3) :**

| Paquet | Version | Rôle |
|---|---|---|
| `next` | `^15.1.3` (résolu **15.5.27**) | Framework, App Router, rendu serveur |
| `react` | `^19.0.0` | Bibliothèque de rendu |
| `react-dom` | `^19.0.0` | Rendu DOM |

Aucune librairie UI, aucun framework CSS, aucune police distante, aucun script tiers. `overrides: { postcss: ^8.5.29 }` au niveau racine.

**Dépendances de développement (7) :** `@testing-library/react ^16.3.3`, `@types/node ^22.10.2`, `@types/react ^19.0.2`, `@types/react-dom ^19.0.2`, `jsdom ^26.1.0`, `tsx ^4.19.2`, `typescript ^5.7.2`, `vitest ^4.1.11`.

**Scripts npm (6) — effet réel :**

| Script | Commande | Effet observé |
|---|---|---|
| `dev` | `next dev` | Serveur de développement |
| `build` | `next build` | ✅ exit 0, 4 routes générées |
| `start` | `next start` | Démarre depuis le build |
| `test` | `test:logique && test:ui` | ✅ 119 + 136 = 255 tests, 255 passent |
| `test:logique` | `node --import tsx --test src/lib/*.test.ts` | ✅ 22 suites, 119 tests, 0 échec |
| `test:ui` | `vitest run` | ✅ 4 fichiers, 136 tests, 0 échec |
| `typecheck` | `tsc --noEmit` | ✅ exit 0 |
| `verifier:poids` | `node scripts/verifier-poids-css.mjs` | Mesure 6,98 Ko gzip < 30 Ko → exit 0. **Non branché dans la CI ni dans `build`** |

**Versions :** Node `v20.20.2` (local), npm `10.8.2`, TypeScript `5.7.x`, **Next.js 15.5.27** (constaté dans la sortie du build), **React 19**. La CI utilise Node 22. Le `package.json` exige `node >= 20`.

---

## 4. SECTION 2 — ÉTAT FONCTIONNEL DU FRONTEND

**Il n'existe aucun `route.ts`, aucun `route.js`, aucun `middleware.ts` et aucune Server Action dans `src/`.** Les seules routes sont les 4 pages ci-dessous.

### 4.1 `/` — Accueil (`src/app/page.tsx`, 184 l.)

| | |
|---|---|
| **Type** | Composant serveur, `export const dynamic = 'force-dynamic'` (l.44) |
| **Affiche réellement** | Header dégradé bleu `.entete` avec logo « R », `<h1>`, sous-titre, 4 mots-clés en pastilles · lien `<Link href="/parcours" class="bouton bouton--principal">` (l.91) · bandeau `.avertissement` (l.97) · section « Le parcours » rendant `PARCOURS.map` (l.117-132) · section « État des fonctionnalités », 4 entrées en dur (l.8-33) · section « Connexion au service » avec `<ApiStatus>` (l.167) · footer |
| **Source des données du parcours** | **Fichier en dur `src/components/parcours.ts`** — 5 étapes, dont 3 marquées « Disponible » (l.125-127). Aucun lien avec l'API |
| **Appelle l'API** | `process.env.API_BASE_URL` lue **serveur** (l.55), normalisée (l.35-39) → composant client `ApiStatus` → `GET ${baseUrl}/api/v1` (timeout 5 s) |
| **En cas d'erreur** | URL vide → « Non configuré / API non configurée — `API_BASE_URL` n'est pas définie sur ce déploiement » (`ApiStatus.tsx:37-43`). Réseau/CORS → « Impossible de joindre l'API. Vérifiez `API_BASE_URL` et la configuration CORS du backend. » (`api.ts:90-94`) |
| **État** | **Fonctionnelle.** Réserve : `force-dynamic` désactive la mise en cache ; la section « Le parcours » affiche un statut qui ne dépend d'aucune donnée réelle |

### 4.2 `/parcours` — Liste des blocs (`src/app/parcours/page.tsx`, 74 l.)

| | |
|---|---|
| **Type** | Serveur, `force-dynamic` (l.20) |
| **Affiche** | `.entete--interne` · bandeau d'avertissement · `<ParcoursServeur baseUrl>` qui rend `parcours.blocs`, filtre sur `disponible` (l.29) et lie chaque exercice vers `/parcours/[id]` · footer avec lien retour |
| **Appelle l'API** | `GET /api/v1/parcours` (`parcours.ts:143`), timeout 8 s |
| **En cas d'erreur** | URL vide → « **Le service de exercices n'est pas configuré sur ce déploiement.** » (l.139) — **faute d'accord dans un texte livré à l'utilisateur**. Réseau → « Impossible de joindre le service d'exercices. ». Timeout → « Le service ne répond pas. Réessaie dans un instant. » (l.150-152). Rendu : carte `role="status"` « Exercices indisponibles » (`ParcoursServeur.tsx:19-26`) |
| **État** | **Fonctionnelle.** Bloc fermé → `<p role="note">` (l.68), rôle ARIA **inexistant** (voir §6) |

### 4.3 `/parcours/[id]` — Exercice (`src/app/parcours/[id]/page.tsx`, 52 l.)

| | |
|---|---|
| **Type** | Serveur, `await params` (l.23). **Pas** de `force-dynamic`. Route 100 % dynamique à la demande (`prerender-manifest.json` → `dynamicRoutes: []`) |
| **Affiche** | Header « Exercice » + `<Exercice baseUrl exerciceId>` + lien retour |
| **Appelle l'API** | Côté client : `GET /api/v1/exercices/{encodeURIComponent(id)}` (`parcours.ts:161`), puis selon l'action `GET .../indice/:palier`, `POST /api/v1/corrections`, `POST /api/v1/suivi`. Tous en timeout 8 s, `cache: 'no-store'` |
| **En cas d'erreur** | « Chargement de l'exercice… » (l.237-243) puis « Cet exercice n'est pas disponible pour le moment. » + lien retour (`Exercice.tsx:226-235`) |
| **État** | **Fonctionnelle.** `params.id` n'est pas validé : un identifiant arbitraire part dans l'URL encodée. Aucun `notFound()` |

### 4.4 `/design-system` — Catalogue (`src/app/design-system/page.tsx`, 45 l.)

| | |
|---|---|
| **Garde** | l.41-43 : `if (NODE_ENV === 'production' && DESIGN_SYSTEM_ENABLED !== 'on') notFound()` |
| **État** | **CASSÉE en production.** Vérifié par requête réelle : `https://relio-frontend-one.vercel.app/design-system` → **HTTP 404**. Vérifié dans le build : `.next/server/app/design-system.html` commence par `<html id="__next_error__">`, et `prerender-manifest.json` liste `/design-system` dans les routes prérendues. La page ayant été **prérendue en erreur au moment du build**, poser `DESIGN_SYSTEM_ENABLED=on` en production ne suffit pas sans forcer le rendu dynamique |
| **Note** | `PageDesignSystem.tsx` est `'use client'` (l.1) : la garde ne peut s'exécuter que sur un rendu dynamique |

### 4.5 Composants applicatifs

| Composant | Chemin | Rôle réel | Props | Importé par | État |
|---|---|---|---|---|---|
| `ApiStatus` | `components/ApiStatus.tsx` | Sonde `GET /api/v1` après rendu navigateur | `{ baseUrl: string }` | `app/page.tsx:167` | ✅ utilisé |
| `ClavierMath` | `components/ClavierMath.tsx` | Clavier mathématique ; applique l'action au `<input>` natif via RefObject puis `requestAnimationFrame` | `typeReponse`, `onChange`, `onValider`, `onFermer`, `onSysteme`, `champId`, `champRef` | `components/Exercice.tsx:451` | ✅ utilisé |
| `Exercice` | `components/Exercice.tsx` | Écran d'exercice complet, 6 `useState` | `{ baseUrl: string; exerciceId: string }` | `app/parcours/[id]/page.tsx:39` | ✅ utilisé |
| `ParcoursServeur` | `components/ParcoursServeur.tsx` | Rendu serveur des blocs, filtre `disponible` | `{ baseUrl: string }` | `app/parcours/page.tsx:61` | ✅ utilisé |
| `PARCOURS` / `Ton` / `Etape` | `components/parcours.ts` | 5 étapes marketing en dur | — | `app/page.tsx:4,117` | ✅ utilisé |

### 4.6 Composants du design system — usage hors `/design-system`

`grep -rn "components/ds" src/` → **1 seul fichier** : `PageDesignSystem.tsx:26-39`.

| Composant | Props | Utilisé hors `/design-system` | État |
|---|---|---|---|
| `Bouton` (99 l.) | `variante`, `taille`, `children`, `icone`, `chargement`, `pleineLargeur` | AUCUN | orphelin applicatif |
| `BoutonIcone` (48 l.) | `nom`, `label` (obligatoire), `variante`, `taille` | AUCUN | orphelin applicatif |
| `Carte` (52 l.) | `variante`, `sansOmbre`, `bordure`, `padding` | AUCUN | orphelin applicatif |
| `Champ` / `ZoneTexte` (158 l.) | `label` (obligatoire), `erreur`, `aide`, `requis`, `enveloppe` | AUCUN | orphelin applicatif |
| `Pastille` (34 l.) | `ton`, `children`, `compacte` | AUCUN | orphelin applicatif |
| `Puce` (46 l.) | `children`, `active`, `fixe` | AUCUN | orphelin applicatif |
| `Avatar` (59 l.) | `nom`, `taille`, `className` | AUCUN | orphelin applicatif |
| `Icone` (93 l.) | `nom`, `titre`, `taille` | AUCUN | orphelin applicatif |
| `BarreProgression` (76 l.) | `valeur`, `label`, `ton`, `afficherValeur`, `live` | AUCUN | orphelin applicatif |
| `AnneauProgression` (99 l.) | `valeur`, `taille`, `epaisseur`, `ton`, `label` | AUCUN | orphelin applicatif |
| `EtatVide` (61 l.) | `titre`, `description`, `icone`, `action`, `onAction` | AUCUN | orphelin applicatif |
| `Feuille` (140 l.) | `ouverte`, `titre`, `onFermer`, `pied`, `fermeAuFond` | AUCUN | orphelin applicatif |
| `Squelette` (71 l.) | `largeur`, `hauteur`, `rond`, `lignes` | AUCUN | orphelin applicatif |
| `BasculeTheme` (97 l.) | aucune | AUCUN | orphelin applicatif |
| `FournisseurNotification` | `{ children }` | **0 occurrence dans tout `src/`** | **code mort** |
| `ZoneNotification` | aucune | **0 occurrence** | **code mort** |
| `useNotifications` | — | **0 occurrence hors test** | **code mort** |
| `ds/index.ts` (barrel, 27 l.) | — | **jamais importé** (le catalogue importe chaque fichier directement) | **code mort** |

**Constat factuel :** les 14 composants du design system sont importés à **100 % par la seule route `/design-system`**. Aucun n'est utilisé par l'accueil, le parcours ou l'exercice.

---

## 5. SECTION 3 — ÉTAT FONCTIONNEL DU BACKEND

### 5.1 Routes exposées (8, toutes enregistrées dans `src/routes/index.ts:13-17`)

| # | Méthode + chemin | Code | Entrée attendue | Sortie produite | Erreurs gérées |
|---|---|---|---|---|---|
| 1 | `GET /health` | `v1.ts:40` | aucune | 200 `{ status, name, version, environment, uptimeSeconds, timestamp }` | aucune |
| 2 | `GET /api/v1` | `v1.ts:61` | aucune | 200 `{ name, apiVersion, status, documentation, endpoints[8] }` | aucune |
| 3 | `GET /api/v1/parcours` | `parcours.ts:210` | aucune ; date via `DATE_NAVIGATION_TEST` ou `new Date()`, année via `ANNEE_SCOLAIRE_DEBUT` | 200 `{ version, anneeScolaire{debut,semaine,dansAnneeScolaire,anneeTerminee}, message, blocs[] }` | 500 si `DATE_NAVIGATION_TEST` invalide (l.52-54) |
| 4 | `GET /api/v1/exercices/:id` | `parcours.ts:213` | `params.id` ; validé par `exerciceAccessible()` | 200 `{ id, blocId, rang, objectifs, enonce, consigne, typeReponse, formeDemandee, nbIndices, origine }` — **aucun champ `reponseAttendue`** | 400 (id vide), 403 (bloc fermé, code `BAD_REQUEST`), 404 (inconnu) |
| 5 | `GET /api/v1/exercices/:id/indice/:palier` | `parcours.ts:220` | `params.id`, `params.palier` en `Number` | 200 `{ palier, texte }` | 400, 403, **404** si palier hors bornes (0, 4, `abc`) — 404 et non 400 |
| 6 | `POST /api/v1/corrections` | `parcours.ts:242` | body `{ exerciceId, reponse, indiceDemande?, nbEchecs? }`, casté sans schéma Fastify | 200 `{ exerciceId, objectifId, mathemathiquementJuste, formeRespectee, achevement, statut, verdict, libelle, signatureErreur, leconsCandidates, explication, indice, lectureArbitree, pointsArbitrage, categorieDifficulte, tutorat{...} }` · **422** `{ erreurSaisie, message, exerciceId, categorieDifficulte, tutorat }` — **format plat, pas `{error:{code,message}}`** | 400, 403, 404, 422 |
| 7 | `POST /api/v1/progression` | `parcours.ts:329` | body `{ reponses? }` ; chaque item `{ exerciceId, statut }`, `statut` hors vocabulaire fermé → 400 avec la liste des valeurs | 200 `{ objectifs[], avertissement }` | 400, 403, 404 |
| 8 | `POST /api/v1/suivi` | `parcours.ts:393` | body `{ observations? }` ; validation exhaustive : `rang` obligatoire entier 1..50, `reponse` obligatoire ≤ 200 car, `statut` et `categorie` contrôlés, `niveauAide` ∈ {1,2,3} | 200 `{ objectifs[], avertissement, conservation }` | 400, 403, 404 |
| — | route inconnue | `error-handler.ts:57-64` | — | 404 `{ error: { code: 'NOT_FOUND', message: "Route inconnue : GET /xyz" } }` — **réinjecte method et url bruts** | — |

**Validation :** entièrement manuelle. `grep "schema:" src/routes/` → **0**. Aucun schéma JSON Schema n'est passé aux routes, alors que `openapi.yaml` en déclare.

**Codes HTTP effective** : 200, 400, 403, 404, 422, 500. Le `SERVICE_UNAVAILABLE` (503) est déclaré dans `errors.ts:12` mais **jamais émis**.

### 5.2 Couverture des tests par route

| Route | Couverte | Nombre de tests |
|---|---|---|
| `GET /health` | ✅ `api.test.ts` | 5 |
| `GET /api/v1` | ✅ `api.test.ts` | 3 |
| 404 route inconnue | ✅ `api.test.ts` | 2 |
| Erreurs contrôlées / JSON invalide | ✅ `api.test.ts` | 3 |
| CORS | ✅ `api.test.ts` | 5 |
| `loadConfig` | ✅ `api.test.ts` | 8 |
| `GET /api/v1/parcours` | ✅ `parcours.test.ts` | 4 |
| `GET /api/v1/exercices/:id` | ✅ `parcours.test.ts` | 4 |
| `GET .../indice/:palier` | 🟡 partiel | 1 (paliers 1→3 uniquement) |
| `POST /api/v1/corrections` | ✅ `parcours.test.ts` | 8 + 11 (tutorat) |
| `POST /api/v1/progression` | ✅ `parcours.test.ts` | 7 |
| `POST /api/v1/suivi` | ✅ `parcours.test.ts` | 8 |

**Aucune route n'est entièrement non couverte.** Branches d'erreur **non** couvertes :

| Branche | Emplacement | Constat |
|---|---|---|
| 404 sur palier hors bornes | `parcours.ts:226` | aucun test de `/indice/0`, `/indice/4`, `/indice/abc` |
| 500 sur `DATE_NAVIGATION_TEST` invalide | `parcours.ts:52-54` | aucun test |
| Longueur de `reponse` > 200 car dans `/suivi` | `parcours.ts:444` | `rang` est testé, pas la longueur |
| `ConfigError` au démarrage de `server.ts` | `server.ts:15-19` | **`server.ts` n'est importé par aucun test** |
| Arrêt gracieux SIGTERM/SIGINT | `server.ts:25-37` | non testé |

### 5.3 Middlewares présents

**Présents :**

| Middleware | Fichier | Effet réel |
|---|---|---|
| CORS | `plugins/cors.ts` | Liste blanche issue de `CORS_ORIGINS` ; origine inconnue → `callback(null, false)` (réponse servie **sans** en-tête CORS, pas d'erreur HTTP) ; requête sans en-tête `Origin` toujours acceptée ; `methods: GET, POST, OPTIONS`, `credentials: false`, `maxAge: 600` ; log `warn` si liste vide |
| Gestion d'erreurs | `plugins/error-handler.ts` | `ApiError` → statut + message applicatif ; 4xx Fastify → statut conservé, message **remplacé** par un générique, journalisé en `info` ; reste → 500 `INTERNAL_ERROR` « Erreur interne du serveur. », journalisé en `error` ; `setNotFoundHandler` pour le 404 |
| Logger | `app.ts:21-28` | Logger **Pino natif de Fastify**, niveau selon `NODE_ENV`. **Ce n'est pas un middleware de requête** : rien ne journalise les accès HTTP |

**Absents (vérifié par grep sur `package.json` et `src/`/ `test/`) :**

| Contrôle | État |
|---|---|
| **Rate limiting** | 🔴 **Absent.** Aucune dépendance, aucun code |
| **Authentification** | 🔴 **Absente.** Aucun header lu dans `src/routes/`, aucun token, aucune session |
| **Helmet / en-têtes de sécurité** | 🔴 **Absent.** Aucune dépendance |
| **Validation par schéma** | 🔴 **Absente** |
| **Compression** | 🔴 **Absente** |

La seule limite protecting le CPU est le `bodyLimit` par défaut de Fastify (1 Mo). Les routes 4, 5 et 6 exécutent un parseur récursif (`analyseur-expression.ts`, `DEGRE_MAX = 16`, `deepness` gardé à 64).

### 5.4 Connexion base de données

**Elle n'existe pas.** Recherche exhaustive insensible à la casse de `pg`, `prisma`, `sqlite`, `mysql`, `redis`, `DATABASE_URL`, `knex`, `typeorm`, `sequelize`, `mongoose` sur `src/`, `test/` et `package.json` → **0 occurrence**.

- Dépendances de production : `fastify` et `@fastify/cors` uniquement.
- `DATABASE_URL` apparaît **commentée** dans `.env.example:32` et mentionnée dans `README.md:78`. Elle n'est lue par aucun code.
- Le code est explicitement sans état : commentaires à `parcours.ts:322-328` et `:374-380`, et les réponses contiennent les champs `avertissement` / `conservation` qui l'annoncent au client.
- `README.md:146-160` justifie l'absence de base et avertit que Railway fournit un PostgreSQL éphémère sur les offres gratuites.

### 5.5 Variables d'environnement attendues (noms uniquement)

| Variable | Lue dans le code | Emplacement | Défaut |
|---|---|---|---|
| `PORT` | ✅ | `config.ts:83` | `3000` |
| `HOST` | ✅ | `config.ts:84` | `0.0.0.0` |
| `NODE_ENV` | ✅ | `config.ts:80`, `v1.ts:45` | `development` |
| `CORS_ORIGINS` | ✅ | `config.ts:85` | `[]` |
| `ANNEE_SCOLAIRE_DEBUT` | ✅ | `parcours.ts:44` | `2026-09-07` |
| `DATE_NAVIGATION_TEST` | ✅ | `parcours.ts:49` | absente |
| `npm_package_version` | ✅ | `v1.ts:44` | `0.1.0` |
| `IA_PROVIDER_KEY` | ❌ | `.env.example:29`, commentée | — |
| `DATABASE_URL` | ❌ | `.env.example:32`, commentée | — |

**Écarts :**
- **Documentées et utilisées :** `PORT`, `HOST`, `NODE_ENV`, `CORS_ORIGINS` ✅
- **Documentées mais non utilisées :** `IA_PROVIDER_KEY`, `DATABASE_URL` (les deux commentées)
- **Utilisées mais absentes de `.env.example` :** `ANNEE_SCOLAIRE_DEBUT` et `DATE_NAVIGATION_TEST`. La première est documentée dans `CONTRAT-API.md:233-235` avec un avertissement sur une éventuelle valeur périmée ; la seconde, si définie en production, **figerait la date pour toute l'application**.
- `NODE_ENV` est lu à deux endroits par deux chemins distincts (`config.ts:80` avec validation, `v1.ts:45` sans).

### 5.6 Santé du service

| Contrôle | Résultat |
|---|---|
| `GET https://relio-backend-production-a2c3.up.railway.app/health` | **HTTP 200**, 143 o, 154 ms |
| Corps de la réponse | `{"status":"ok","name":"relio-backend","version":"0.1.0","environment":"production","uptimeSeconds":2416,"timestamp":"2026-10-11T00:25:15.452Z"}` |
| `GET /api/v1` | HTTP 200 · `status: "mvp-pedagogique"` · 8 endpoints listés |
| `GET /api/v1/parcours` | HTTP 200 · `anneeScolaire.debut: "2026-09-07"`, `semaine: 5`, `dansAnneeScolaire: true` |
| `GET https://relio-frontend-one.vercel.app/` | **HTTP 200**, 20 520 o, 871 ms |
| `GET https://relio-frontend-one.vercel.app/design-system` | **HTTP 404** |
| En-têtes du backend | `x-railway-request-id`, `x-hikari-trace`, `x-railway-edge`. **Aucun en-tête `ratelimit*`, aucun `www-authenticate`** — vérifié sur `POST /api/v1/suivi` sans authentification |
| Date de la dernière vérification | **2026-10-11 00:25 UTC** (dans cette session). La dernière vérification **antérieure** documentée dans les rapports date du chantier 7.7 |

**Le déploiement correspond au code audité** : `status: mvp-pedagogique`, `debut: 2026-09-07`, `/api/v1/suivi` présent dans la liste des endpoints.

---

## 6. SECTION 4 — LOGIQUE MÉTIER EXISTANTE

### 6.1 Backend — `src/lib/`

| Module | Lignes | Responsabilité | Fonctions exportées |
|---|---|---|---|
| `algebre.ts` | 118 | Arithmétique rationnelle exacte sur `bigint`, aucun `Number` dans le calcul | `rationnel`, `ZERO`, `UN`, `estEgal`, `somme`, `oppose`, `produit`, `quotient`, `estEntier`, `versNombre`, `versChaine`, `pgcdEntiers`, `estCarreParfait`, `racineCarreeEntiere`, `facteursPremiers` |
| `analyseur-expression.ts` | 491 | Lexer Unicode (normalise `− × · ² √` et les espaces insécables), parseur descendant récursif, évaluation en polynôme exact, comparaison algébrique | `analyserExpression`, `versPolynome`, `versPolynomeVerifie`, `sontAlgebriquementEgales`, `comparerPolynomes`, `estProduitDeFacteurs`, `nombreDeTermes`, `DEGRE_MAX = 16`, `polynomeNul` |
| `analyseur-reponse.ts` | 330 | Transforme une saisie en **objet-valeur typé** (rationnelle / expression / racine) en conservant la **forme écrite**, pour séparer justesse, forme et interprétation | `analyserRationnel`, `analyserExpressionReponse`, `analyserRacine`, `normaliserRacine`, `sontEgales`, `decrire`, `estIrreductible` |
| `calendrier.ts` | 110 | Positionnement dans l'année scolaire et ouverture des blocs | `positionnerDansLAnnee`, `blocDisponible`, `semainesAvantOuverture`, `NOMBRE_SEMAINES = 30`, `DEBUT_ANNEE_DEFAUT = '2026-09-07'` |
| `errors.ts` | 40 | Erreur applicative typée et correspondance HTTP | `ApiError`, `toApiErrorBody`, `ErrorCode`, `ApiErrorBody` |
| `progression.ts` | 144 | Statut par objectif selon la **règle des trois**. Deux invariants : `non_evalue` jamais dégradé, `acquis_confirme` jamais émis | `evaluerObjectif`, `evaluerProgression`, `prerequisAtteints`, `STATUTS_OBJECTIF` |
| `suivi.ts` | 221 | Difficultés par objectif,fk ; regroupement par exercice ; nombre d'aides avant réussite. Fonction pure, sans persistance. L'ordre des tentatives est reconstruit depuis `rang` pour survivre à un désordre d'envoi | `suivreObjectif`, `suivreProgression`, `Observation`, `SuiviObjectif` |

### 6.2 Backend — `src/contenu/`

| Module | Lignes | Responsabilité | Exports principaux |
|---|---|---|---|
| `types.ts` | 126 | Modèle de données + vocabulaire fermé `STATUTS_REPONSE` avec garde `estStatutReponse` | `Exercice`, `Bloc`, `Objectif`, `Indice`, `Piege`, `Correction` |
| `blocs.ts` | 105 | 3 blocs, 5 objectifs opérationnels, semaines d'ouverture S1/S5/S10 | `BLOCS`, `OBJECTIFS`, `trouverObjectif`, `trouverBloc`, `prerrequisSatisfaits` |
| `exercices.ts` | 337 | Les **12 exercices** originaux du MVP (6 en B1, 3 en B2, 3 en B3), avec énoncé, consigne, réponse attendue, 3 indices et 3-4 pièges documentés | `EXERCICES`, `trouverExercice`, `exercicesDuBloc` |
| `correction.ts` | 504 | Cœur du système : correction sur **4 axes** (justesse, forme, achèvement, verdict D5), recherche de piège, message élève, échappement du symbole inconnu | `corriger`, `jugerForme`, `formeDemandee`, `messagePourErreur`, `VERDICTS` |
| `aides.ts` | 285 | Textes d'aide par objectif et par signature, **sans identifiant technique** | `AIDES_PAR_OBJECTIF`, `AIDES_PAR_SIGNATURE`, `orientationPourObjectif`, `questionPourObjectif`, `aidePour` |
| `tutorat.ts` | 579 | Échelle d'aide **déterministe** à 3 niveaux. **Aucune IA, aucun appel externe** | `construireTutorat`, `niveauPourNbEchecs`, `normaliserNbEchecs`, `categoriePour`, `CATEGORIES_DIFICULTE` (8 valeurs), `NB_ECHECS_MAX = 20` |
| `egalite.ts` | 141 | Extraction du membre réponse dans une égalité écrite à la façon du cahier (`A = 2x + 1`) | `separerEgalite`, `membreReponse` |
| `signatures.ts` | 48 | Catalogue fermé des **12 signatures d'erreur** + leçons candidates | `SIGNATURES`, `estSignatureValide`, `LEÇONS_CANDIDATES` |

### 6.3 Implémenté vs déclaré

| Capacité | État | Preuve |
|---|---|---|
| Logique de **parcours** | ✅ Implémentée | `calendrier.ts`, `blocs.ts`, garde `exerciceAccessible()` à `parcours.ts:177-189` appliquée par **toutes** les routes |
| Logique de **correction / diagnostic** | ✅ Implémentée | `correction.ts` 504 l. + `analyseur-expression.ts` 491 l. + `analyseur-reponse.ts` 330 l. ; 4 axes ; verdict D5 |
| Logique de **scoring / progression** | ✅ Implémentée | `progression.ts` 144 l., règle des trois, 15 tests. **Sans niveau global, sans pourcentage, sans `acquis_confirme`** |
| Logique de **suivi des difficultés** | ✅ Implémentée | `suivi.ts` 221 l., 14 tests. **Fonction pure, sans persistance** |
| Logique de **tutorat** | ✅ Implémentée | `tutorat.ts` 579 l., 29 tests ; échelle déterministe à 3 niveaux, **aucun appel IA** |
| **Persistance** | 🔴 Non implémentée | 0 dépendance base de données ; réponses porteuses des champs `avertissement` / `conservation` |
| **Authentification / comptes élèves** | 🔴 Non implémentée | Aucun contrôle d'identité nulle part |
| **Tuteur IA** | 🔴 Non implémentée | `IA_PROVIDER_KEY` commentée dans `.env.example:29` ; aucun SDK, aucun appel réseau dans `src/` |
| **Recommandation pédagogique** (diagnostic initial, sondes `SONDE-M3-S1..S6`) | 🔴 Déclaré seulement | `docs/specification-diagnostic-initial.md` et `docs/regles-recommandation-pedagogique.md` décrivent une mini-évaluation de 5 questions et 6 sondes ; **0 occurrence de `SONDE-M3-` et de `ORIG-M3-Q0n` dans `frontend/` et `backend/`** |
| **Suites d'exercices BEPC** | 🔴 Déclaré seulement | `data/inventaire-questions-bepc-2025-2026.json` (35 questions) **n'est importé par aucun code** ; `lib/securite.test.ts` interdit explicitement tout identifiant d'épreuve BEPC dans `src/` |

### 6.4 Frontend — `src/lib/`

| Module | Lignes | Responsabilité | Utilisé par |
|---|---|---|---|
| `api.ts` | 97 | Client `GET /api/v1`, timeout 5 s, `AbortController`, ne fabrique jamais de réponse | `ApiStatus.tsx:4` ✅ |
| `parcours.ts` | 231 | Client des 5 routes du parcours, timeout 8 s, `cache: 'no-store'` | `ParcoursServeur.tsx:3`, `Exercice.tsx:21-29` ✅ |
| `clavier.ts` | 464 | Logique pure : insertion/retrait/effacement/fraction au curseur, 3 dispositions de touches (9/8/8 rangées), `apercuLisible` | `ClavierMath.tsx:42-53`, `Exercice.tsx:8-13` ✅ |
| `observations.ts` | 233 | Journal `localStorage`, validation de forme stricte, plafond 500 | `Exercice.tsx:14-20` ✅ |
| `tutorat.ts` | 112 | Types + libellés de niveau ; **aucun appel réseau** | `Exercice.tsx:30-36` ✅ |

**Tests associés :** `api.test.ts` 13, `parcours.test.ts` 17, `clavier.test.ts` 47, `observations.test.ts` 15, `tutorat.test.ts` 14, `navigation.test.ts` 7, `securite.test.ts` 6 = **119 tests**.

**Contraintes verrouillées par les tests :** aucune donnée identifiante dans le journal (`observations.test.ts:73`), le client n'expose que les types attendus sans score ni niveau (`parcours.test.ts:281`), aucun champ `reponseAttendue` transporté (`parcours.test.ts:255`), aucune clé ni secret sur 7 motifs (`securite.test.ts:115`), tout lien interne pointe vers une route qui existe (`navigation.test.ts:145`).

---

## 7. SECTION 5 — UX/UI — ÉTAT RÉEL

### 7.1 Écrans utilisables de bout en bout aujourd'hui

| Écran | Utilisable de bout en bout | Dépendance externe |
|---|---|---|
| `/` | ✅ Oui | Aucune — la page se rend sans API ; seule la carte « Connexion au service » dépend du réseau |
| `/parcours` | ✅ Oui, si le backend est joignable et CORS autorisé | `GET /api/v1/parcours` |
| `/parcours/[id]` | ✅ Oui : chargement, saisie, clavier mathématique, correction, verdicts, indices, tutorat, suivi local | 4 endpoints |
| `/design-system` | 🔴 **Non** en production (404) | — |

**Parcours nominal vérifié** : `/` → bouton « Voir le parcours » → `/parcours` → blocs et exercices ouverts (B1 disponible en semaine 5) → `/parcours/MVP-B1-E1` → saisie → correction → verdict → tutorat.

### 7.2 Écrans qui sont des maquettes, placeholders ou tests

- **Section « Le parcours » de l'accueil** (`page.tsx:117-132`) : 5 étapes **en dur** dans `components/parcours.ts`, dont 3 marquées « Disponible » (l.125-127). Aucune de ces données ne vient de l'API. Elles ne reflètent pas l'état réel du service.
- **Section « État des fonctionnalités » de l'accueil** (`page.tsx:8-33`) : 4 entrées en dur.
- **`/design-system`** : catalogue de composants, fermé en production.
- **Pas d'écran de connexion, pas de compte, pas d'espace enseignant, pas de page d'erreur 404 applicative, pas de page `error.tsx`, pas de `loading.tsx`, pas de `not-found.tsx` personnalisé** — vérifié : aucun de ces fichiers n'existe dans `src/app/`.

### 7.3 Cohérence visuelle

**Couleurs dominantes (système applicatif, `globals.css` `:root` l.1-20) :**

| Variable | Valeur |
|---|---|
| `--fond` | `#f7f8fc` (gris très froid) |
| `--surface` | `#ffffff` |
| `--texte` | `#14161f` |
| `--texte-doux` | `#4d5468` |
| `--bordure` | `#e2e5ef` |
| `--primaire` | `#2b4bd8` (bleu) |
| `--primaire-sombre` | `#1e37a8` |
| `--primaire-doux` | `#eef1fe` |
| `--rayon` | `14px` (unique) |

**Couleurs du design system (`design/tokens.ts`) :** indigo `#1E2A78`, accent orange `#F97316`, vert `#16A34A`, fond sable `#FAF7F2`. **Palette différente.**

**Typographie :** `system-ui` — **aucune police distante**, aucun `@font-face`. Échelle typographique applicative en valeurs ad hoc (`clamp(1.5rem, 6vw, 2.1rem)` pour le titre, `0.72rem`, `0.76rem`, `0.82rem` pour les petits textes). Le design system dispose d'une échelle complète (`--relio-taille-xs: 12px` … base 16 px) **non utilisée par l'application**.

**Mise en page :** classes globales BEM maison dans `globals.css` (~45 classes), conteneur `max-width: 46rem`.

**Les deux systèmes divergent explicitement :**

| | Design system | Feuille applicative |
|---|---|---|
| Nommage | `--relio-fond`, `--relio-texte` | `--fond`, `--surface`, `--texte` |
| Palette | indigo `#1E2A78` + orange | bleu `#2b4bd8`, pas d'orange |
| Fond | sable `#FAF7F2` | gris froid `#f7f8fc` |
| Typo | échelle de tokens | valeurs ad hoc |
| Rayons | 8 / 12 / 16 / 24 / 9999 | unique `--rayon: 14px` |
| Mode sombre | oui (3 déclarations) | **non** |
| Économie de données | oui (`[data-economie='on']`) | non |
| Contrôle automatisé | oui (`accessibilite.test.ts`, `tokens.test.ts`) | **aucun** |

**Preuve chiffrée de l'absence de couplage :** `grep "var(--relio" src/app/globals.css` → **2 occurrences seulement**, et ce sont `--relio-clavier-systeme` (l.782-783), une variable publiée par le hook JavaScript et **absente de `tokens.css`**. Les ~90 variables `--relio-*` de `tokens.css` sont donc **chargées sur toutes les pages et utilisées sur aucune page applicative**.

**Conséquence sur le mode sombre :** `tokens.css:117-163` déclare un mode sombre complet ; `globals.css` ne consomme aucune de ces variables. Un élève en mode sombre système voit une page **claire** (fond `#f7f8fc`) alors que `layout.tsx:16-19` annonce `themeColor: #0B1020` en `prefers-color-scheme: dark`.

### 7.4 `globals.css` — contenu et usage

**Chemin :** `src/app/globals.css` — **851 lignes**.
**Importé par :** `src/app/layout.tsx:3` — **unique importation**, donc **chargé sur toutes les pages**, y compris `/design-system`.
**Poids dans le build :** 30,8 Ko bruts (`.next/static/css/c5b3424d1cf8f1d7.css` = 13,6 Ko → **3,45 Ko gzip**).

**Contenu :**
1. l.1-20 — 16 tokens CSS en dur dans `:root`
2. l.22-38 — reset (`box-sizing`, marges, `font-family: system-ui`, `line-height: 1.6`, `-webkit-font-smoothing`)
3. l.40-333 — ~45 classes BEM (`.page`, `.conteneur`, `.entete*`, `.section*`, `.grille`, `.carte`, `.etape*`, `.badge*`, `.etat-api*`, `.avertissement`, `.actions`, `.bouton*`, `.pied`)
4. l.356-568 — `.lien`, `.entete--interne`, `.bouton--principal`, `.objectifs`, `.message-ferme`, `.exercice*`, `.indices`, `.verdict*` (5 variantes)
5. l.570-738 — `.clavier*`, `.exercice__apercu`, `.tutorat*`, `.suivi*`
6. l.740-851 — `.exercice--saisie` en colonne contrainte, `.exercice__zone`, `.exercice__composeur`, media query `max-height: 700px`

**Défaut vérifié dans le CSS compilé :** `.bouton` est déclaré **deux fois** — l.303 (`background: var(--primaire)`, `color: #fff`, `border-radius: 10px`) puis l.477 (`min-height: 48px`, `border: 1px solid var(--bordure)`, `background: var(--surface)`, `color: var(--texte)`). La seconde écrase la première.

> Vérification directe sur `.next/static/css/c5b3424d1cf8f1d7.css` :
> - offset **7357** : `.bouton{…border:1px solid var(--primaire);background:var(--primaire);color:#fff;border-radius:10px…}`
> - offset **8275** : `.bouton--principal{background:var(--primaire);color:#fff;border-color:var(--primaire)}`
> - offset **9647** : `.bouton{min-height:48px;padding:0 1.1rem;border-radius:var(--rayon);border:1px solid var(--bordure);background:var(--surface);color:var(--texte)…}`

Spécificité égale (0,1,0) ; le dernier déclarant gagne. Le bouton `class="bouton bouton--principal"` de l'accueil (`page.tsx:91`) s'affiche donc **blanc au repos**, et `.bouton--principal:hover` (l.382) le **repaint en bleu au survol**.

### 7.5 Mobile — 360 / 390 / 768 px

**Il n'existe que DEUX media queries de largeur dans tout le code applicatif :** `min-width: 34rem` = **544 px** (`globals.css:145`) et `min-width: 768 px` (`design-system.module.css:239`, `/design-system` uniquement). Les `RUPTURES = { sm: 360, md: 420, lg: 768 }` déclarées dans `tokens.ts:256` **ne sont consommées par aucun CSS**.

| Largeur | Comportement constaté |
|---|---|
| **360 px** | `.conteneur` → `padding: 1rem 1rem 3rem`, largeur utile **328 px**. `.grille` → **1 colonne** (< 544 px). `.entete__titre` = `clamp(1.5rem, 6vw, 2.1rem)` → 24 px (plancher). Touche de clavier : `(328 − 16 − 16 − 18) / 4` ≈ **69,5 px** de large, `min-height: 44px`. Hauteur clavier expression = 9 rangées × 44 px + gaps + padding ≈ **452 px** ; sous `max-height: 700px` (écran 360×640) ≈ **420 px**, ce qui laisse ~220 px de contenu. Le commentaire `globals.css:585-586` annonce « environ 80 px » par touche : **l'estimation documentée est optimiste de 13 %** (69,5 px réels). Le commentaire `l.744-748` annonce « 453 px, 187 px restants » : recalculé, **~220 px** restent |
| **390 px** | Rendu **strictement identique** à 360 px : `.conteneur` reste à `padding: 1rem` (390 < 544), `.grille` reste à 1 colonne. Largeur utile **358 px**, touche ≈ **79,5 px**. La mise en page est **binaire**, pas adaptative : aucun ajustement entre 360 et 543 px |
| **768 px** | `.grille` passe à **2 colonnes** (544 px franchi), `.conteneur` à `padding: 1.5rem 1.5rem 3.5rem`, largeur utile **688 px**. **Comportement dégradé** : `.exercice--saisie` conserve `height: calc(100dvh - var(--relio-clavier-systeme))` (l.782), ce qui impose une hauteur de **1 024 px pour une seule carte** alors que le contenu (énoncé + composeur + clavier ≈ 600 px) ne le justifie pas ; `.exercice__zone` (l.788-794) devient une zone de défilement inutile |

**Mesure du clavier système :** `useHauteurClavierSysteme.ts:70` calcule `max(0, innerHeight − visualViewport.height − visualViewport.offsetTop)`, l'arrondit (l.78) et le publie dans `--relio-clavier-systeme`, consommé par `globals.css:782-783` en `height` **et** `max-height`. **Cohérence confirmée.** 6 tests couvrent ce hook.

**Ce qui n'existe nulle part :** aucune règle pour l'orientation paysage, aucune pour `hover: none`, aucune pour `prefers-contrast`, aucune pour l'impression, aucune pour les largeurs > 46rem.

### 7.6 Design system utilisé hors de `/design-system` ?

**Non.** Réponse nette et vérifiée :

- **Composants `ds/` :** `grep -rn "components/ds" src/` → **1 seul fichier**, `PageDesignSystem.tsx:26-39`.
- **`design/tokens.ts` (TypeScript) :** importé uniquement par `PageDesignSystem.tsx:40-48` et par les tests.
- **`design/contraste.ts` :** importé uniquement par `PageDesignSystem.tsx:50` et `tokens.test.ts`. `accessibilite.test.ts:25` fixe `DOSSIER = src/components/ds` : **les contrôles de contraste et de 44 px ne s'appliquent jamais à `globals.css`**.
- **`design/tokens.css` (variables CSS) :** importé globalement par `layout.tsx:2` — mais **utilisé nulle part** dans `globals.css` (2 occurrences de `--relio-clavier-systeme`, qui n'est pas un token de `tokens.css`).

Le catalogue consomme 14 composants + ~1 100 lignes de CSS + 300 lignes de tests ; **aucun n'est repris par l'application**, qui utilise à la place `.bouton`, `.carte`, `.lien`, `.badge` de `globals.css`.

**Preuve directe :** `next.config.ts` n'expose rien ; `layout.tsx` ne monte **ni `FournisseurNotification`, ni `ZoneNotification`, ni `BasculeTheme`**. Le design system est livré **sans point d'entrée applicatif**.

---

## 8. SECTION 6 — ACCESSIBILITÉ — ÉTAT RÉEL

*(Hors composants du design system. Aucun correctif n'a été appliqué.)*

### 8.1 Contraste des textes

Ratios recalculés avec la formule WCAG 2.1 implémentée dans `src/design/contraste.ts` sur les couleurs de `globals.css` :

| Paire | Ligne | Ratio | Verdict AA |
|---|---|---|---|
| texte `#14161f` / fond `#f7f8fc` | l.33-34 | **17,00:1** | ✅ AAA |
| texte-doux `#4d5468` / fond `#f7f8fc` | l.125 | **7,11:1** | ✅ AAA |
| texte-doux `#4d5468` / surface `#fff` | l.264 | **7,54:1** | ✅ AAA |
| blanc / primaire `#2b4bd8` | l.307 | **6,77:1** | ✅ AA |
| blanc / primaire-sombre `#1e37a8` | l.56-57 | **9,69:1** | ✅ AAA |
| primaire-sombre / primaire-doux | l.222-223 | **8,61:1** | ✅ AAA |
| succes `#14663f` / `#e7f6ee` | l.212-213 | **6,27:1** | ✅ AA |
| alerte `#9a2b2b` / `#fdeeee` | l.218 | **6,77:1** | ✅ AA |
| attente `#8a5312` / `#fff4e2` | l.207-208 | **5,80:1** | ✅ AA |
| sous-titre `rgba(255,255,255,.88)` composé `#e6e9fa` / `#2b4bd8` | l.89 | **5,61:1** | ✅ AA |
| mot-clé blanc sur `rgba(255,255,255,.16)` composé `#4d68de` | l.102-107 | **4,83:1** | ✅ AA |
| **`bordure #e2e5ef` / surface `#fff`** | l.133 `.carte`, **l.458 `.exercice__saisie`**, **l.623 `.clavier__touche`** | **1,26:1** | ❌ **sous 3:1** |

**Point de rupture :** `globals.css` ne dispose que d'**une seule catégorie de bordure** (`#e2e5ef`, 1,26:1), utilisée **aussi** pour le champ de saisie et les touches du clavier. Le design system a résolu exactement ce problème avec deux tokens (`--relio-bordure` décorative / `--relio-bordure-forte` 3,48:1, `tokens.ts:27-36`) ; `globals.css` ne l'a pas repris.

**Autres constats :** `.etat-api__url` = 12,2 px (l.270) ; `.badge` = 11,5 px (l.199) ; `.pied` = 13,1 px (l.342). Les couleurs sont conformes ; ce sont les tailles qui sont petites.

**Le contenu applicatif n'a pas de mode sombre** (voir §7.3).

### 8.2 Taille des cibles tactiles

| Élément | Ligne | Valeur | vs 44 px |
|---|---|---|---|
| `.exercice-lien` | l.414 | `min-height: 44px` | ✅ |
| `.clavier__touche` | l.616 | `min-height: 44px` | ✅ |
| `.bouton` (2ᵉ décl.) | l.478 | `min-height: 48px` | ✅ |
| `.exercice__saisie` | l.455 | `min-height: 52px` | ✅ |
| `.mot-cle` | l.102-109 | `padding .2rem .7rem`, font `0.8rem` → **≈ 27 px** | non interactif |
| `.badge` | l.193-204 | `padding .12rem .6rem`, font `0.72rem` → **≈ 23 px** | non interactif |
| **`.lien`** | l.362-365 | `text-decoration: underline`, **aucun `min-height`, aucun `padding`** | ❌ **≈ 20 px de haut** |

**Rupture :** tous les liens de navigation secondaires utilisent `.lien` **nu** : `parcours/page.tsx:66` « Retour à l'accueil », `parcours/[id]/page.tsx:44` « Retour au parcours », `Exercice.tsx:230` « Retour au parcours ». C'est le chemin de secours principal quand l'exercice échoue.

### 8.3 Labels, rôles ARIA, focus visible

**Ce qui est correct :**
- `page.tsx:82,108,136,158` : 4 `<section aria-labelledby>` avec `<h2 id>` correspondant
- `Exercice.tsx:308` : `<label htmlFor="reponse">` + `<input id="reponse">`
- `ClavierMath.tsx:168` : `role="group" aria-label="Clavier mathématique"` ; l.183 : `aria-label={touche.aria}` sur chaque touche ; l.184 : `aria-controls={champId}`
- `Exercice.tsx:386-392` : `role="status" aria-live="polite"` sur le verdict ; l.340 : `aria-live="polite"` sur l'aperçu
- `<html lang="fr">` (`layout.tsx:26`), `<main>` présent sur les 3 pages applicatives

**Ce qui casse :**

| Constat | Emplacement |
|---|---|
| **`role="note"` n'existe pas en ARIA** — utilisé **3 fois** ; ignoré par les lecteurs d'écran, donc les bandeaux d'avertissement ne sont **pas annoncés** | `page.tsx:97`, `parcours/page.tsx:50`, `ParcoursServeur.tsx:68` |
| **Aucun `outline` sur `.bouton`, `.lien`, `.lien-bouton`, `.badge`, `.verdict`, `.etat-api`.** Le focus clavier sur ces éléments repose **entièrement** sur l'outline par défaut du navigateur | `globals.css` ne contient que 3 règles `outline` : `.exercice__saisie:focus` (l.466), `.clavier__touche:focus-visible` (l.666) |
| `.exercice__saisie:focus` est un `:focus` et **non** `:focus-visible` : le contour bleu de 2 px apparaît **à la souris** ; décalage de 1 px vs 2 px ailleurs | `globals.css:466` |
| **Deux régions live concurrentes** : `<p role="status">` pour l'erreur de saisie **et** `<section role="status">` pour la correction | `Exercice.tsx:376-383` et `:385-392` |
| Emoji `👉` littéral dans un `<p>`, non décoratif (`aria-hidden` absent), sera lu comme « index pointant vers la droite » | `Exercice.tsx:409` |
| `className="icone"` posée par le composant `Icone` — **cette classe n'existe dans aucune feuille de style** de tout `src/` | `ds/Icone.tsx:74` |
| **Aucun skip-link** dans `layout.tsx` ; le `<header>` de la page précède le `<main>` sans mécanisme de saut | `layout.tsx` |

### 8.4 Navigation clavier — où ça casse

**`ClavierMath.tsx:188` n'écoute que `onPointerDown`.** Les 25 touches sont des `<button type="button">` ; Enter et Espace déclenchent un événement `click`, et **aucun `onClick` n'existe sur ces touches**. Les touches « Masquer » et « Clavier système » (`.clavier__touche--fermer` / `--systeme`) passent **également** par `onPointerDown` → également inopérantes.

> Conséquence : **aucune touche du clavier mathématique n'est actionnable au clavier physique, ni avec un commutateur d'accès, ni avec une technologie d'assistance.** Seuls le champ `<input>` natif et les autres éléments de la page sont utilisables au clavier. Le commentaire `l.185-187` justifie `onPointerDown` pour le comportement tactile Android.

**Autres ruptures :**
- `ClavierMath.tsx:163-165` : un `useEffect` appelle `.focus()` sur le champ au montage → un utilisateur clavier est **ramené au champ à chaque rendu de la rangée**.
- `ds/Feuille.tsx:51-78` implémente un **focus trap correct** (gestion Shift+Tab, restitution du focus l.102, blocage du scroll l.95-97) — mais **`Feuille` n'est montée nulle part**.

---

## 9. SECTION 7 — PERFORMANCE ET POIDS

### 9.1 Poids par route (mesuré par `next build`)

```
Route (app)                                 Size  First Load JS
┌ ƒ /                                     1.41 kB      107 kB
├ ○ /_not-found                             993 B      104 kB
├ ○ /design-system                         10.6 kB      113 kB
├ ƒ /parcours                               160 B      106 kB
└ ƒ /parcours/[id]                         5.76 kB      112 kB
+ First Load JS shared by all              103 kB
  ├ chunks/255-….js                        46.5 kB
  ├ chunks/4bd1-….js                        54.2 kB
  └ other shared chunks                    1.94 kB
```

- **Temps de compilation :** 24,4 s. 4 pages générées (3 statiques, 2 dynamiques).
- `/` et `/parcours` sont en `ƒ` (dynamiques) grâce à `force-dynamic` ; `/design-system` est en `○` (statique) — c'est ce qui produit le 404 en production.
- Le poids de la page la plus lourde (`/parcours/[id]`) est de 5,76 kB de code propre.

### 9.2 CSS

| Fichier | Brut | gzip |
|---|---|---|
| `42947774f408bb39.css` (modules du design system) | 17,2 Ko | 3,53 Ko |
| `c5b3424d1cf8f1d7.css` (`tokens.css` + `globals.css`) | 13,6 Ko | 3,45 Ko |
| **Total** | **30,8 Ko** | **6,98 Ko** |

Budget déclaré : **30 Ko gzip**. Marge restante : **23,02 Ko**.
`DESIGN_SYSTEM.md:209` annonce « 6,8 Ko » : valeur périmée d'environ 0,2 Ko (mesure réelle : 6,98 Ko).
**Le script `verifier:poids` n'est exécuté ni par `ci.yml`, ni par `build`, ni par `test`** — vérifié par grep. `DESIGN_SYSTEM.md:214-215` affirme qu'il est « branché dans la CI après le build » : **c'est faux**.

### 9.3 Nombre de requêtes par écran

| Écran | Requêtes |
|---|---|
| `/` | 1 requête applicative (`GET /api/v1`) + N sous-ressources Next.js (1 CSS + chunks JS) |
| `/parcours` | 1 (`GET /api/v1/parcours`) + sous-ressources |
| `/parcours/[id]` | 1 au chargement (`GET /api/v1/exercices/:id`), puis **1 par action** : `GET .../indice/:palier`, `POST /api/v1/corrections`, et `POST /api/v1/suivi` **à chaque nouvelle tentative** |

Toutes les requêtes applicatives utilisent `cache: 'no-store'` (`api.ts:48`, `parcours.ts:125`).

### 9.4 Images, polices, scripts tiers

| Élément | Constat |
|---|---|
| Images bitmap dans `src/` | **Aucune** — vérifié par `accessibilite.test.ts:143` (test automatisé) |
| Polices distantes | **Aucune** — `font-family: system-ui` ; vérifié par `accessibilite.test.ts:153` |
| Scripts tiers | **Aucun.** 0 dépendance externe au-delà de Next/React |
| Polices distantes / CDN | Aucune |

### 9.5 Connexion lente — fallbacks

**Des fallbacks existent et sont codés :**

| Situation | Comportement | Emplacement |
|---|---|---|
| `API_BASE_URL` vide | Carte « Non configuré / API non configurée » | `ApiStatus.tsx:37-43`, `parcours.ts:139` |
| Délai dépassé (5 s / 8 s) | « Le service ne répond pas. Réessaie dans un instant. » + carte `role="status"` | `parcours.ts:150-152`, `ParcoursServeur.tsx:19-26` |
| Erreur réseau | « Impossible de joindre l'API. Vérifiez `API_BASE_URL` et la configuration CORS du backend. » | `api.ts:90-94` |
| Exercice indisponible | « Cet exercice n'est pas disponible pour le moment. » + lien retour | `Exercice.tsx:226-235` |
| Réponse illisible (422) | Carte dédiée avec message élève | `Exercice.tsx:376-383` |

**Réserves :** `/` et `/parcours` sont en `force-dynamic` : **tout le HTML est rendu côté serveur à chaque requête**. Un backend lent bloque le rendu de la page (le composant `ParcoursServeur` est un composant serveur `async` — `GET /api/v1/parcours` est attendu avant l'envoi du HTML, avec un délai de 8 s). L'écran « Chargement de l'exercice… » (`Exercice.tsx:237-243`) est le seul fallback côté client. **Aucun squelette de chargement n'est utilisé sur ces écrans** — le composant `Squelette` du design system existe mais n'est monté nulle part. **Aucun mécanisme de retry automatique.**

---

## 10. SECTION 8 — SÉCURITÉ — ÉTAT RÉEL

### 10.1 Secrets exposés côté client

`grep -rn "NEXT_PUBLIC\|process.env" src/` → 10 résultats, dont **8 sont des commentaires ou des tests**. Lectures réelles :

| Fichier:ligne | Variable | Contexte |
|---|---|---|
| `app/page.tsx:55` | `API_BASE_URL` | composant **serveur** |
| `app/parcours/page.tsx:32` | `API_BASE_URL` | composant **serveur** |
| `app/parcours/[id]/page.tsx:24` | `API_BASE_URL` | composant **serveur** |
| `app/design-system/page.tsx:38` | `DESIGN_SYSTEM_ENABLED` | serveur |
| `app/design-system/page.tsx:39` | `NODE_ENV` | serveur |

- **Aucune variable `NEXT_PUBLIC_`** dans le code.
- **Aucune clé, aucun token, aucun mot de passe** : motif vérifié automatiquement par `lib/securite.test.ts:115-126` sur **7 motifs** (`sk-`, `ghp_`, `AIza`, `Bearer`, `NEXT_PUBLIC_*KEY|SECRET|TOKEN|PASSWORD`, `apiKey`/`api_key`/`secretKey`/`accessToken`).
- `next.config.ts:27` : `env: {}` — surface d'exposition explicitement vide. `poweredByHeader: false` (l.29).

**Backend :** `IA_PROVIDER_KEY` et `DATABASE_URL` sont **commentées** dans `.env.example` et **non lues**. `README.md:158` et `.env.example:6` portent l'interdiction de commiter un secret.

### 10.2 En-têtes HTTP

| En-tête | Frontend (prod) | Source |
|---|---|---|
| `X-Content-Type-Options: nosniff` | ✅ présent | `next.config.ts:32-41` |
| `X-Frame-Options: SAMEORIGIN` | ✅ présent | `next.config.ts:34-41` |
| `Referrer-Policy: strict-origin-when-cross-origin` | ✅ présent | `next.config.ts:33-41` |
| `Strict-Transport-Security: max-age=63072000; includeSubDomains; preload` | ✅ présent | **ajouté par Vercel**, pas par le code |
| `Content-Security-Policy` | ❌ **absent** | aucune déclaration dans `next.config.ts` |
| `Permissions-Policy` | ❌ **absent** | idem |

**Constat :** l'application effectue des `fetch` vers une URL arbitraire venant de `API_BASE_URL` ; en l'absence de CSP, `connect-src` n'offre aucun rempart.

**Backend :** aucun en-tête de sécurité posé par le code (pas de `helmet`). Les en-têtes observés en production (`x-railway-request-id`, `x-hikari-trace`, `x-railway-edge`) sont posés par Railway.

### 10.3 Requêtes sortantes

**Six points de sortie réseau, tous via `fetch` :**

| # | URL | Méthode | Déclenchement | Timeout | Corps envoyé |
|---|---|---|---|---|---|
| 1 | `${API_BASE_URL}/api/v1` | `GET` | `ApiStatus.tsx:24`, au montage et au clic « Revérifier » | 5 000 ms | aucun |
| 2 | `${API_BASE_URL}/api/v1/parcours` | `GET` | `ParcoursServeur.tsx:17` (**serveur**) | 8 000 ms | aucun |
| 3 | `${API_BASE_URL}/api/v1/exercices/{id}` | `GET` | `Exercice.tsx:118` | 8 000 ms | aucun |
| 4 | `${API_BASE_URL}/api/v1/exercices/{id}/indice/{palier}` | `GET` | `Exercice.tsx:193` | 8 000 ms | aucun |
| 5 | `${API_BASE_URL}/api/v1/corrections` | **POST** | `Exercice.tsx:147` | 8 000 ms | `{ exerciceId, reponse, indiceDemande, nbEchecs }` |
| 6 | `${API_BASE_URL}/api/v1/suivi` | **POST** | `Exercice.tsx:171` | 8 000 ms | `{ observations: [...] }` — **le journal local complet, sans filtre** |

**Données transmises (#5) :** identifiant d'exercice, **la réponse brute saisie par l'élève** (tronquée à 200 caractères, `Exercice.tsx:158`), nombre d'indices demandés, nombre d'échecs consécutifs. Aucun nom, aucun identifiant, aucun horodatage. Verrouillé par `lib/parcours.test.ts:213`.

**Données transmises (#6) :** `lireJournal()` en entier, sans filtre ni plafond supplémentaire. Contenu par entrée (`observations.ts:41-51`) : `exerciceId`, `rang`, `reponse` (≤ 200 car), `statut`, `categorie`, `niveauAide`, `reussiteApresAides`. Ces champs permettent de **reconstituer l'historique complet des réponses de l'élève**.

**Constat sur l'affichage :** `page.tsx:177-180` affiche « Aucune donnée personnelle n'est collectée, et **tes réponses ne sont pas conservées**. » La seconde phrase est **factuellement fausse pour le client** : les réponses sont conservées dans `localStorage` (jusqu'à 500 entrées) **et transmises au serveur à chaque tentative**. Elle est vraie pour le serveur seul (« rien n'est conservé côté serveur », ce que confirme l'absence de base de données).

**CORS :** les appels #1, #3, #4, #5, #6 partent du navigateur vers une origine tierce ; le backend doit envoyer `Access-Control-Allow-Origin`. En cas de refus, **le navigateur masque l'erreur réelle** — le message utilisateur affiché est générique (`api.ts:88-89` le reconnaît dans un commentaire).

**Aucun proxy ni route handler** : le navigateur parle directement à l'API. Pas de SSRF possible depuis le serveur ; en revanche l'URL du backend est **affichée explicitement à l'écran** (`ApiStatus.tsx:83`).

### 10.4 Validation des entrées utilisateur

| Couche | État |
|---|---|
| Backend — schémas JSON Schema / Fastify | 🔴 **Absent** (`grep "schema:" src/routes/` → 0) |
| Backend — validation manuelle | ✅ **Présente et détaillée** sur les 6 routes métier : types, plages (`rang` 1..50), vocabulaire fermé (`statut`, `categorie`, `niveauAide`), longueur (`reponse` ≤ 200 car), bornes (`palier`), bornes d'accès calendrier |
| Frontend — validation de la saisie | ✅ `lib/clavier.ts` : `SAISIE_MAX` borné, insertion au curseur contrôlée |
| Frontend — validation des données re-lues du `localStorage` | ✅ `observations.ts:126-140` : une entrée illisible est **ignorée, pas devinée** |

**Constat :** `indiceDemande` dans `POST /api/v1/corrections` n'est **ni typé ni borné** (`parcours.ts:261-262`) ; s'il n'est pas un nombre, il passe silencieusement à `null`. `nbEchecs` est normalisé (non-nombre/NaN → 0, `Math.trunc`, borné à 20) et ne peut jamais provoquer d'erreur (`tutorat.ts:209-214`).

### 10.5 Stockage local

`grep -rn "localStorage\|sessionStorage\|document.cookie\|indexedDB" src/` → 11 résultats, 3 fichiers. **Aucune utilisation de `sessionStorage`, `document.cookie` ni `indexedDB`.**

| Clé | Définition | Contenu | État |
|---|---|---|---|
| `relio.observations.v1` | `observations.ts:54` | Tableau d'observations : réponses de l'élève, statut, catégorie, rang, niveau d'aide. Plafond **500** (`TENTATIVES_MAX`), via `.slice(-500)` l.167 | **Seule clé réellement utilisée par l'application.** Versionnée, validée à la relecture, effaçable par l'élève (`Exercice.tsx:291-301`), écriture tolérante à l'échec (quota / navigation privée, l.175-181) |
| `relio.theme` | `ds/Theme.tsx:32` | `'clair'` \| `'sombre'` | **Jamais écrit en production** : seul `BasculeTheme` l'écrit, monté uniquement sur `/design-system` |
| `relio.economie` | `ds/Theme.tsx:33` | `'on'` \| `'off'` | idem |

**Pas de chiffrement, pas d'expiration, pas de consentement explicite.** Choix documenté dans `observations.ts:1-32`.

### 10.6 Données de mineurs — collecte et consentement

| Élément | État |
|---|---|
| Données identifiantes collectées | **Aucune.** Pas de nom, prénom, date de naissance, âge, classe, téléphone, e-mail, localisation, identifiant unique, photo. Verrouillé par `observations.test.ts:73` et `securite.test.ts:123` |
| Données de **comportement** collectées | **Oui** : chaque réponse saisie, le statut du verdict, la catégorie d'erreur, le niveau d'aide, le rang de la tentative — stockées localement et **transmises au serveur à chaque tentative** via `POST /api/v1/suivi` |
| Bandeau de consentement | **Absent.** Aucune bannière, aucun dialogue, aucune case à cocher |
| Base légale / mention | **Absente.** Aucun texte de politique de confidentialité dans l'application |
| Mineurs | Le produit vise la classe de 3e (13-15 ans). `docs/regles-recommandation-pedagogique.md` contient une table de minimisation de données ; `docs/rapport-final-chantier-7.md:369` liste « D9/D10 — Comptes élèves et **protection des mineurs** » comme **hors MVP** |
| Partage à un tiers | **Aucun** — 0 dépendance externe |

### 10.7 Authentification

**Elle n'existe pas.** `grep` sur tout `src/` : pas de session, pas de cookie, pas de JWT, pas d'en-tête `Authorization`, pas de `middleware.ts`. Côté backend : aucun header n'est lu dans `src/routes/`, aucune dépendance d'authentification, aucun contrôle d'identité.

| Conséquence constatée | Emplacement |
|---|---|
| Le seul contrôle d'accès du dépôt est `DESIGN_SYSTEM_ENABLED` | `design-system/page.tsx:41` |
| La clé `localStorage` est **globale au navigateur** : n'importe qui utilisant le même téléphone peut **lire et effacer l'historique** d'un autre élève | `observations.ts:54`, `Exercice.tsx:295` |
| `POST /api/v1/suivi` accepte un journal complet de n'importe quel contenu, sans authentification ni limitation de débit | `parcours.ts:393` |

Vérifié en production : `POST /api/v1/suivi` sans aucun en-tête d'authentification → **aucun `www-authenticate`, aucun `ratelimit*`** dans la réponse.

### 10.8 « Sécurisation de l'ancienne authentification GitHub » — ce qui reste ouvert

Cette réserve est documentée dans **trois** rapports successifs du dépôt racine, sous les identifiants **R4 / D6** :

| Fichier | Ligne | Contenu |
|---|---|---|
| `docs/rapport-audit-fiabilite-chantier-4.md` | 81 | « **D6** \| Jeton historique dans `~/.git-credentials` \| 🟡 **Réserve** \| 1 entrée github.com, encore utilisée par `Relio` » |
| `docs/rapport-audit-fiabilite-chantier-4.md` | 203-208 | « **R4 — Jeton GitHub historique toujours présent 🟡** » ; preuve : 1 entrée `https://<masqué>@github.com` dans `/config/.git-credentials` |
| `docs/rapport-final-chantier-5.md` | 239 | « Entrées \| **1** — `https://<IDENTIFIANT_MASQUE>@github.com` » |
| `docs/rapport-final-chantier-5.md` | 260-261 | « **Supprimer l'entrée locale ne révoque PAS le jeton.** » |
| `docs/rapport-final-chantier-5.md` | 314 | « **CI GitHub Actions activée** \| `ÉCHEC` \| Jeton sans scope `workflow` ; `total_count: 0` » |
| `docs/ci-workflows-chantier-5.md` | 244-252 | « **Jeton encore valide ?** \| 🔴 **OUI — actif (HTTP 200)** » ; « ce jeton n'avait d'accès qu'à `Relio`. C'est **faux aujourd'hui** : il a [plus de droits] » |
| `docs/ci-workflows-chantier-5.md` | 281-284 | « **Révocation du jeton** \| Le rend inutilisable, **où qu'il soit** » ; « **Nettoyer le fichier local ne révoque RIEN sur GitHub.** » |
| `docs/ci-workflows-chantier-5.md` | 296 | « 1. **RÉVOQUER le jeton sur GitHub** ← étape prioritaire » |

**État factuel au 2026-10-11 :**

1. **Aucun des trois rapports ne constate la résolution de cette réserve.** Elle est rejouée en « à faire » dans les trois documents.
2. La procédure de révocation est explicitement formulée **trois fois** et n'a pas été exécutée, ou du moins n'a pas été reportée dans un rapport.
3. Le contrôle d'accès GitHub a été **reconfiguré le 2026-10-11** dans le cadre de l'installation des dépôts de cet audit : `credential.helper=store` est configuré globalement et une entrée `github.com` existe dans `~/.git-credentials` (mode 600). Un contrôle d'accès `ls-remote` sur les trois dépôts succeeds. **La portée exacte de ce jeton (scopes) n'a pas été inspectée** et n'est pas vérifiable depuis l'environnement : voir « Zones d'ombre ».
4. Aucun secret n'est **versionné dans un dépôt** : `.gitignore` exclut `.env`, `.env.*`, `*.pem`, `*.key`, `credentials.json`, `.netrc` dans les trois dépôts. `securite.test.ts` verrouille l'absence de secret dans `src/`.

**Point connexe non traité :** les **4 PDF BEPC originaux (2,03 Mo) et le JPG source (384 Ko) sont versionnés dans le dépôt racine GitHub public**, alors que `README.md:40-45` déclare que « les droits de reproduction ne sont pas établis » et que ces contenus sont un « outil d'analyse interne ». La réserve juridique **R3** est signalée (`docs/rapport-final-chantier-7-1.md:395`, « Juridique », **non vérifiée**) et n'est traitée dans aucun rapport ultérieur. `docs/rapport-final-chantier-6.md:398` la classe 🔴 Critique (« fuite vers le client »).

---

## 11. SECTION 9 — TESTS — ÉTAT RÉEL

### 11.1 Nombre total de tests par suite

**Exécution réelle le 2026-10-11.**

| Dépôt | Suite | Commande | Résultat |
|---|---|---|---|
| backend | unique | `npm test` = `node --import tsx --test test/*.test.ts` | ✅ **307 tests, 307 passent, 0 échec, 0 annulé, 0 ignoré, 0 todo** — 66 suites, 12,4 s |
| frontend — logique | `test:logique` | `node --import tsx --test src/lib/*.test.ts` | ✅ **119 tests, 119 passent, 0 échec, 0 ignoré** — 22 suites, 6,9 s |
| frontend — UI | `test:ui` | `vitest run` | ✅ **136 tests, 136 passent, 0 échec** — 4 fichiers, 15,4 s |
| **Total** | | | **562 tests, 562 passent** |

**Typecheck :** `tsc --noEmit` ✅ exit 0 sur les deux dépôts. **Build :** `next build` ✅ exit 0 ; `tsc --project tsconfig.build.json` ✅ exit 0. **`npm ci` :** 0 vulnérabilité sur les deux dépôts.

### 11.2 Détail backend (307 tests, 13 fichiers)

| Fichier | Tests | Ce qu'il couvre |
|---|---|---|
| `api.test.ts` | 27 | `/health`, `/api/v1`, routes inconnues, erreurs contrôlées, CORS, `loadConfig`. Vérifie aussi que `/api/v1` renvoie **exactement** les 8 routes réelles (`l.113-130`) |
| `parcours.test.ts` | 53 | Les 6 routes métier + calendrier + D5 + tutorat |
| `tutorat.test.ts` | 29 | Échelle d'aide, verdicts préservés, catégories, refus de symbole |
| `egalite.test.ts` | 26 | Égalité « A = … » : acceptation, refus, non-régression |
| `aides.test.ts` | 24 | Aucun identifiant technique, exactitude des exemples, progression des indices |
| `correction.test.ts` | 23 | Axes 1/2/3, signatures, robustesse |
| `decision-d5.test.ts` | 23 | Les 4 cas D5 + équivalences + prudence + invariants |
| `algebre.test.ts` | 20 | Rationnels, analyse d'expressions, analyse de réponses |
| `contenu.test.ts` | 20 | Périmètre du MVP + **recalcul indépendant des 12 réponses attendues** avec le moteur de production (`l.381`) — contre-vérification réelle |
| `calendrier.test.ts` | 19 | Positionnement, année 2026-2027, ouverture des blocs |
| `progression.test.ts` | 15 | Règle des trois, multi-objectifs, prérequis |
| `suivi.test.ts` | 14 | Absence de donnée, réussite après aide, récurrence, ordre des tentatives, absence de PII |
| `langage-simple.test.ts` | 14 | Langage élève : pas de terme technique, messages courts, jamais « faux » si juste |

### 11.3 Détail frontend (255 tests, 11 fichiers)

| Fichier | Tests | Ce qu'il couvre |
|---|---|---|
| `lib/clavier.test.ts` | 47 | Opérations curseur, fraction, 3 dispositions, invariant « chaque rangée = exactement 4 colonnes », `apercuLisible` |
| `components/ds/composants.test.tsx` | 42 | Le catalogue complet : 14 composants, attributs ARIA, `role="dialog"`, Échap, focus trap de `Feuille` |
| `design/tokens.test.ts` | 21 | Contrastes, **parité TS↔CSS** (relit `tokens.css` et compare chaque variable), échelles croissantes, base 4 px, 44 px tactile, aucune police externe |
| `lib/parcours.test.ts` | 17 | Les 4 fonctions réseau, encodage d'`id`, timeout, et 2 garde-fous : « ne transporte aucun champ de réponse attendue », « n'expose que les types attendus, sans score ni niveau » |
| `lib/observations.test.ts` | 15 | Champs stockés, « ne contient aucun champ identifiant », numérotation, série d'échecs, stockage indisponible, quota, entrée illisible ignorée, JSON corrompu, plafond, effacement, clef versionnée |
| `lib/api.test.ts` | 13 | URL vide, contrat valide, URL exacte, `no-store`, 404/500, contrat invalide, panne réseau, `AbortError`, délai borné, « ne lève jamais » |
| `lib/tutorat.test.ts` | 14 | Repli sur `explication`, jamais de reformulation, « ne dit jamais “maîtrisé” », aucun score/pourcentage |
| `design/accessibilite.test.ts` | 11 | **Tests statiques** (lecture des `.module.css`, `DOSSIER = src/components/ds`) : 44 px, anneau de focus, animations, images, polices distantes, couleurs brutes |
| `lib/navigation.test.ts` | 7 | **Test d'architecture** : lien vers `/parcours`, route existante, chargement API, « tout lien interne pointe vers une route qui existe », aucun lien vers une fonctionnalité non implémentée |
| `lib/securite.test.ts` | 6 | **Test d'architecture** : surface non vide, pas d'identifiant BEPC, pas de formulation de sujet, pas de clé/secret (7 motifs), `API_BASE_URL` pas `NEXT_PUBLIC_` |
| `hooks/useHauteurClavierSysteme.test.tsx` | 6 | Clavier fermé/ouvert, `offsetTop`, API absente, jamais de hauteur négative |

### 11.4 Ce qui n'est pas testé

| Zone | Cible | Constat |
|---|---|---|
| 🔴 **Aucun test de rendu applicatif** | `Exercice.tsx` (463 l.) | Jamais monté. Aucune vérification de l'affichage du verdict, du tutorat, du clavier, du suivi |
| 🔴 **Aucun test de rendu** | `ClavierMath.tsx` (199 l.) | Jamais monté. **Le défaut `onPointerDown` sans `onClick` (§8.4) n'aurait pas été détecté** : un test « la touche insère le caractère » l'aurait détecté |
| 🔴 **Aucun test de rendu** | `ApiStatus.tsx`, `ParcoursServeur.tsx` | Jamais montés. Le rendu des états d'erreur n'est vérifié nulle part |
| 🔴 **Aucun test de route** | les 4 `page.tsx` et `layout.tsx` | Zéro |
| 🔴 **Aucune couverture du CSS applicatif** | `globals.css` (851 l.) | `accessibilite.test.ts` ne teste que `src/components/ds`. **Les défauts de bordure 1,26:1 et de double déclaration `.bouton` sont hors de portée de tout test** |
| 🔴 **Aucune couverture du design system dans l'app** | `src/components/ds/` | Les 42 tests prouvent que les composants **marchent**, pas qu'ils sont **utilisés**. Aucun test ne détecte qu'ils sont orphelins |
| 🔴 **Aucun test responsive** | 360/390/768 px | `jsdom` n'applique pas les CSS — reconnu par `accessibilite.test.ts:5-16`. Aucun navigateur réel n'est lancé |
| 🔴 **Aucun test de bout en bout / e2e** | — | Ni Playwright, ni Cypress, ni aucun runner de navigateur |
| 🔴 **Aucune couverture de mesure** | — | Vitest n'a pas de `coverage` configuré ; `npm audit` ne mesure pas la couverture du code |
| 🟡 Branches d'erreur backend | voir §5.2 | 404 sur palier hors bornes, 500 sur date invalide, longueur > 200 car, `ConfigError`, SIGTERM |
| 🟡 `BasculeTheme` | `ds/Theme.tsx` | Absent de `composants.test.tsx` (15 describes, Theme absent) |
| 🟡 Garde `/design-system` | `design-system/page.tsx:41-43` | Le bug de prérendu 404 n'est couvert par rien |
| 🟡 `verifier-poids-css.mjs` | le script | Aucun test ne vérifie le calcul gzip |

### 11.5 Tests qui passent / échouent / sont désactivés

| | Nombre |
|---|---|
| Passent | **562** |
| Échouent | **0** |
| Désactivés (`.skip`, `.todo`, `.only`) | **0** |
| Annulés | **0** |

### 11.6 Commandes pour les lancer

```bash
# backend
cd backend && npm ci && npm test && npm run typecheck && npm run build

# frontend
cd frontend && npm ci && npm test && npm run typecheck && npm run build
cd frontend && npm run verifier:poids        # contrôle manuel, non branché

# dépôt racine (validation des données)
node outils/valider-referentiel.mjs          # attend le code 2
node outils/valider-inventaire-bepc.mjs      # attend le code 0
```

### 11.7 CI — ce qu'elle fait et ne fait pas

**Frontend — `.github/workflows/ci.yml` (71 l.) :**

Déclenchement : `push` sur `main` **et** `pull_request` vers `main` (l.8-11). `concurrency` avec annulation (l.13-15). `env: NEXT_TELEMETRY_DISABLED: '1'` (l.17).

*Job `verify` (l.19-56) — bloquant :*

| # | Étape | Commande |
|---|---|---|
| 1 | Récupérer le code | `actions/checkout@v4` |
| 2 | Installer Node 22 | `actions/setup-node@v4`, `cache: npm` |
| 3 | Installer les dépendances | **`npm ci`** |
| 4 | Vérifier les types | **`npm run typecheck`** |
| 5 | Tests automatisés | **`npm test`** (= `test:logique` + `test:ui`) |
| 6 | Build de production | **`npm run build`** |

*Job `audit` (l.58-71) — **informatif** :* `continue-on-error: true`, `npm audit --audit-level=high`. **Ne bloque pas la fusion.**

**Ce que la CI ne fait pas :**

1. ❌ `npm run verifier:poids` n'est **pas exécuté** → le budget CSS de 30 Ko **n'est pas gardé**
2. ❌ Aucun lint : ni ESLint, ni Biome, ni Prettier. **Aucune configuration de linter n'existe dans le dépôt**
3. ❌ Aucun test d'accessibilité réelle : ni `axe-core`, ni Lighthouse. Le contrôle est **statique** et ne couvre que `src/components/ds`
4. ❌ Aucun test e2e, aucun test de rendu applicatif
5. ❌ `npm audit` est en `continue-on-error` → n'bloque pas
6. ❌ Aucun Dependabot ni configuration de mise à jour automatique
7. ❌ Aucun cache `.next`, aucun `next build --profile`, aucun rapport de bundle → **la dérive de poids JS n'est pas mesurée**
8. ❌ Pas de `permissions:` déclaré sur le job → permissions par défaut du dépôt
9. ❌ Aucun scan de secrets (`gitleaks`/`trufflehog`) au-delà du motif de `securite.test.ts`

**Backend — `.github/workflows/ci.yml` (69 l.) :** typecheck + tests + build sur Node 22, plus `npm audit` informatif (`continue-on-error`).

**Dépôt racine :** ❌ **aucune CI** — `ls .github` → inexistant. Aucun des 4 scripts de `outils/` n'est exécuté automatiquement.

**État de la CI d'après les docs :** `docs/rapport-final-chantier-7-6.md:24` et `:121` affirment « CI verte sur la totalité des commits des deux dépôts » ; `docs/rapport-final-chantier-7-7.md:286-287` citent les exécutions `success` pour les commits `e425722` (backend) et `0b36123` (frontend). **Ces affirmations n'ont pas pu être vérifiées depuis l'environnement** (voir « Zones d'ombre »). Les **fichiers `.github/workflows/ci.yml` existent bien** dans les deux dépôts applicatifs — ce qui contredit `docs/rapport-final-chantier-5.md:5` et `:314` (« workflows NON activés »).

---

## 12. SECTION 10 — DÉPLOIEMENT

### 12.1 Où et comment

| Composant | Plateforme | Domaine |
|---|---|---|
| Frontend | **Vercel** | `https://relio-frontend-one.vercel.app` |
| Backend | **Railway** | `https://relio-backend-production-a2c3.up.railway.app` |

Aucun domaine personnalisé (`.cm`, `.com` de marque) n'apparaît dans aucun document.

### 12.2 Vérification en ligne — effectuée le 2026-10-11

| URL | HTTP | Taille | Temps | Contenu notable |
|---|---|---|---|---|
| `…railway.app/health` | **200** | 143 o | 154 ms | `status: ok`, `environment: production`, `uptimeSeconds: 2416` |
| `…railway.app/api/v1` | **200** | — | — | `status: "mvp-pedagogique"`, 8 endpoints dont `/api/v1/suivi` |
| `…railway.app/api/v1/parcours` | **200** | — | — | `debut: "2026-09-07"`, `semaine: 5`, `dansAnneeScolaire: true`, bloc B1 `disponible: true` |
| `…vercel.app/` | **200** | 20 520 o | 871 ms | HTML complet, `lang="fr"` |
| `…vercel.app/design-system` | **404** | — | — | Page fermée en production (comportement attendu de la garde) |

**Conclusion factuelle : le déploiement en production correspond au code audité.** Le backend en production renvoie `mvp-pedagogique`, la date `2026-09-07` corrigée au chantier 7.2, et expose `/api/v1/suivi`. Le HEAD local du backend est `e425722`, le dernier commit du rapport de chantier 7.7.

### 12.3 Comment se fait le déploiement

- **Automatique par les plateformes.** `docs/ci-workflows-chantier-5.md:67,144` : « Aucun deploiement automatique : Vercel et Railway gerent les leurs. » Autrement dit, chaque `push` sur `main` déclenche la reconstruction chez Vercel et Railway.
- **Configuration requise côté Vercel** (documentée dans `docs/rapport-final-chantier-7-1.md:337-347`) : variable `API_BASE_URL`.
- **Configuration requise côté Railway** : `CORS_ORIGINS`, `ANNEE_SCOLAIRE_DEBUT`, `NODE_ENV=production`, `PORT` (injecté par Railway).

### 12.4 Dernière mise en production

**Non déterminable avec certitude depuis l'environnement.** Éléments factuels :

- Le HEAD local du backend est `e425722`, le dernier commit du chantier 7.7, et la production renvoie exactement les valeurs de ce code → **la production est au moins au niveau du commit `e425722`**.
- `docs/rapport-final-chantier-7-7.md` est le dernier rapport ; il annonce du code « livré, testé, poussé et déployé vérifié » (§8).
- `uptimeSeconds: 2416` (≈ 40 min) au moment de l'audit : **le conteneur Railway a redémarré récemment** — que ce soit pour un redéploiement ou pour un redémarrage de plateforme, le moteur n'est pas distingué.
- Le HEAD local du frontend est `0b36123`, le dernier commit du design system.

### 12.5 Rollback

**Mécaniquement possible, non documenté, non testé.** Aucun script de rollback, aucun tag Git dans les trois dépôts (`git tag` ne retourne rien), aucune politique de versionnement. Un retour à un commit antérieur suivi d'un push déclencherait un redéploiement automatique chez Vercel et Railway. **Ce mécanisme n'a jamais été exercé** — aucun incident de déploiement n'est documenté.

### 12.6 État de la configuration de production — point d'attention

Trois valeurs distinctes de `ANNEE_SCOLAIRE_DEBUT` coexistent dans la documentation, sans arbitrage documenté :

| Source | Valeur citée |
|---|---|
| `docs/rapport-final-chantier-7-2.md:190` | « Si elle vaut encore `2026-09-05` dans Railway… » |
| `docs/rapport-final-chantier-7.md:454` | « Fixer `ANNEE_SCOLAIRE_DEBUT` sur Railway avant la rentrée (aujourd'hui `2025-09-01`) » |
| **Production réelle, vérifiée le 2026-10-11** | **`2026-09-07`** ✅ |

La valeur observée en production est correcte. La divergence documentaire n'a pas d'effet actuel mais reste non résolue dans les documents.

---

## 13. SECTION 11 — DOCUMENTATION EXISTANTE

### 13.1 Fichiers .md présents

#### Dépôt racine — `README.md` (154 l.)

Présente Relio comme le dépôt **documentaire et pédagogique** (Cameroun, BEPC, Maths 3e), « sans aucune fonctionnalité applicative ». Pointe vers les deux dépôts applicatifs. Inventorie 2 fichiers de données avec SHA-256, les documents sources (PDF/JPG), 6 documents de `docs/`, 4 scripts d'outils. Énonce 5 points en attente d'arbitrage. **Aucune section Roadmap, aucun état d'avancement, aucun badge, aucun changelog, aucune version produit.**

Assertions notablement **vérifiées exactes** : SHA-256 des 2 JSON (recalculés), codes de sortie des validateurs (exécutés), « 14 leçons, 98 h, 3 trimestres, 30 semaines » (JSON vérifié), « 35 questions BEPC » (`questions_inventoriees: 35`), champs `competences`/`prerequis`/`objectifs` vides (vérifié).

#### Dépôt racine — `docs/` (16 fichiers, tous modifiés le 2026-10-10)

| Fichier | Lignes | Résumé |
|---|---|---|
| `matrice-couverture-competences.md` | 416 | Établit que le référentiel annuel ne contient **aucune** compétence, objectif ou prérequis (0/0/0 sur 14 leçons) et en déduit **26 objectifs opérationnels `OO-Lx-y`**. Conclut qu'aucune question BEPC n'est publiable (droits) et chiffre la couverture par leçon. Signale des lacunes (ex. `OO-L1-3`). Statut : `specification_provisoire_en_attente_de_validation_pedagogique` |
| `specification-diagnostic-initial.md` | 370 | Spécifie une mini-évaluation de **5 questions originales**, justifiant le choix plutôt que BEPC (droits non établis). Contient énoncés, corrections, distracteurs, règles de saisie mobile. Pose des limites explicites et des hypothèses. **⚠️ « AUCUN DÉVELOPPEMENT NE DOIT COMMENCER AVANT VALIDATION »** |
| `regles-recommandation-pedagogique.md` | 351 | Principe directeur : « le système produit des hypothèses, jamais des verdicts ». Définit **11 signatures d'erreur**, **6 sondes `SONDE-M3-S1..S6`**, le parcours post-diagnostic et les garde-fous. Inclut une table de minimisation de données (ne pas collecter nom, téléphone, e-mail, localisation). Même avertissement « AUCUN DÉVELOPPEMENT AVANT VALIDATION » |
| `rapport-audit-fiabilite-chantier-4.md` | 430 | Audit de fiabilité des deux déploiements. Verdict ⚠️ **ACCEPTABLE SOUS RÉSERVES** avec 4 réserves (R1 vulnérabilités npm, R2/R3, R4 jeton GitHub historique). Documente CORS, absence de secret, en-têtes. Signale **3 contrôles NON VÉRIFIÉS** (logs Railway, réglages plateforme) |
| `rapport-final-chantier-5.md` | 400 | Correction des vulnérabilités `postcss`/`next`, documentation du comportement au build de `API_BASE_URL`, **40 tests ajoutés** (13 frontend + 27 backend). Neutralisation de la divulgation d'erreurs Fastify en 4xx, vérifiée en production. **🔴 Échec explicite de la mise en place de la CI (scope `workflow` manquant)** |
| `ci-workflows-chantier-5.md` | 508 | Contenu intégral prêt à copier de **deux workflows CI**. Documente le blocage : PAT sans scope `workflow`, avec le message d'erreur GitHub exact. Contient la procédure de contrôle/révocation du jeton dans `~/.git-credentials` et une section « Sécurité du jeton » (A1-A5) |
| `rapport-final-chantier-6.md` | 543 | Cadrage du MVP à partir des documents existants, **sans développement**. Recalcule indépendamment 11 réponses (24 contrôles, 24 succès). Conclut qu'aucune validation pédagogique n'est acquise. Liste les conditions bloquantes (B1…C5, **R-3 fuite de contenu BEPC vers le client**, 🔴 Critique) |
| `rapport-final-chantier-7.md` | 571 | Implémentation du MVP : 3 blocs, 5 objectifs, **12 exercices**, moteur de correction à 4 axes + règle D5. **Aucun déploiement ni parcours utilisateur testé par ce chantier.** Liste 5 commits, l'installation d'un PAT dans `~/.git-credentials`, et les conditions non satisfaites (C5 périmètre du jeton, **D9/D10 comptes élèves**) |
| `rapport-final-chantier-7-1.md` | 467 | Correction du bouton « Voir le parcours » (deux défauts distincts : force-dynamic et cible du lien) et création d'une section contrat API. **⚠️ Aucun contrôle effectué en production** (ni Vercel ni Railway accessibles). Actions manuelles Vercel/Railway documentées (§8) |
| `rapport-final-chantier-7-2.md` | 312 | Correction de la date de début d'année scolaire (`2026-09-05` → `2026-09-07`) dans le code, les tests et le contrat API. Établit l'absence d'accès Railway. **La correction n'est effective en production que si Railway est reconfiguré/redéployé** |
| `rapport-final-chantier-7-3.md` | 381 | Application de la décision pédagogique **D5** (« juste mais pas dans la forme demandée »), confirmée par l'enseignant, dans le moteur de correction. **Seul rapport avec vérification HTTP directe** contre Railway et Vercel. Vérifie le CORS sur le domaine Vercel. **🟢 TERMINÉ** |
| `rapport-final-chantier-7-4.md` | 331 | Audit des messages affichés aux élèves : **16 messages sur 45 contenaient des identifiants techniques**. Correction et vérification par appels HTTP après redéploiement Railway. Les 36 indices étaient déjà conformes. **🟢 TERMINÉ** |
| `rapport-final-chantier-7-5.md` | 499 | Tutorat pas à pas (3 niveaux) + clavier mathématique limité à la grammaire du moteur. Audit préalable du code réel de `main` plutôt que sur la parole des rapports antérieurs. Documente que le suivi des difficultés est **local à l'appareil, sans persistance** |
| `rapport-final-chantier-7-6.md` | 528 | QA senior : 267 tests backend, 119 tests frontend, **CI GitHub verte sur la totalité des commits des deux dépôts**. **Aucun test tactile possible** (pas d'Android, pas d'émulateur, pas de `/dev/kvm`). **Trois défauts reproductibles** trouvés/corrigés/déployés ; protocole de pilote pédagogique fourni (§4) |
| `rapport-final-chantier-7-7.md` | 336 | Clavier mobile (9 rangées × 44 px = 453 px = 71 % d'un écran 360×640) et `position: sticky` qui ne réservait pas de place. Passage en colonne contrainte à 3 zones + mesure du clavier système via `visualViewport`. Verdicts « partie » raccourcis de **169 à 49 caractères** ; **3 consignes d'exercice modifiées** (« seule modification de contenu ») |
| `rapport-design-system.md` | 332 | Design system : tokens en double source (TS + CSS) empêchés de diverger par test, 14 composants de base, contrastes AA, cibles 44 px, page `/design-system` fermée en production. CSS de production 6,8 Ko gzip pour un budget de 30 Ko, 249 tests. Signale que le contrôle du poids CSS **n'est pas branché en CI**. **§10 : ⚠️ Partiel** |

#### Dépôt backend — 2 fichiers

| Fichier | Lignes | Résumé |
|---|---|---|
| `README.md` | 180 | Se présente comme un « socle technique » **sans aucune fonctionnalité pédagogique**, exposant « deux routes », avec `status: socle`. Documente la stack, 4 variables, 4 règles de validation au démarrage, les commandes npm et la procédure Railway. §Persistance justifie l'absence de base ; §Sécurité liste 6 mesures. **🔴 OBSOLÈTE sur 12 points (voir §13.2)** |
| `docs/CONTRAT-API.md` | 296 | Contrat d'intégration frontend↔backend **v2.0.0**, backend Railway consommé par frontend Vercel via `API_BASE_URL` lue côté serveur. §3 liste **7 routes** ; §4 fixe le format de réponse et le format d'erreur `{error:{code,message}}` avec 5 codes HTTP ; §7 les règles CORS ; §11 exige de définir `ANNEE_SCOLAIRE_DEBUT` ; §13 documente l'arbitrage D5 ; §9 et §12 listent ce qui n'existe pas. **🔴 8 écarts avec le code réel (voir §13.2)** |

#### Dépôt frontend — 2 fichiers

| Fichier | Lignes | Résumé |
|---|---|---|
| `README.md` | 246 | Architecture, stack, commandes, arborescence. Contient un encadré 🔴 « `API_BASE_URL` est figée AU BUILD, pas au runtime » avec « Constat mesuré en production le 2026-10-10 ». **🟡 PÉRIMÉ** : décrit un bug corrigé depuis par `force-dynamic` (`prerender-manifest.json` ne contient plus que `/_not-found` et `/design-system`) |
| `DESIGN_SYSTEM.md` | 210 | Tokens, échelles, 14 composants, règles de contraste, budget CSS, page `/design-system` fermée en production. **🟡 2 écarts** : annonce « 6,8 Ko » (réel : 6,98 Ko) et affirme que `verifier:poids` est « branché dans la CI après le build » — **il ne l'est nulle part** |

### 13.2 Documentation obsolète ou contradictoire avec le code réel

| # | Document | Affirmation | Réalité du code |
|---|---|---|---|
| **1** | `backend/README.md:5` | « **Aucune fonctionnalité pédagogique n'est implémentée** » | 6 routes métier, 12 exercices, moteur de correction, progression, suivi |
| **2** | `backend/README.md:14` | « L'API expose **deux routes** » | **8 routes** |
| **3** | `backend/README.md:15` | « Le champ `status` de `/api/v1` vaut `socle` » | `mvp-pedagogique` (`v1.ts:7`) |
| **4** | `backend/README.md:11-12` | « pas de gestion d'exercices », « pas de moteur de diagnostic » | `contenu/exercices.ts` 337 l., `lib/analyseur-expression.ts` 491 l., `lib/progression.ts`, `lib/suivi.ts` |
| **5** | `backend/README.md:100-116` | Arborescence : **7 fichiers** | **22 fichiers** ; `src/lib/` et `src/contenu/` sont **absents** de l'arborescence |
| **6** | `backend/README.md:53-58` | 4 variables d'environnement | **6 lues** ; `ANNEE_SCOLAIRE_DEBUT` et `DATE_NAVIGATION_TEST` absentes |
| **7** | `backend/README.md:86-91` | 4 commandes | 5 scripts ; **`npm test` est absent du README** |
| **8** | `backend/openapi.yaml:78` | Exemple de `/api/v1` avec `status: socle` | Le code renvoie `mvp-pedagogique`, et le **schéma du même fichier** énumère `[mvp-pedagogique]` (l.295) — **contradiction interne au fichier** |
| **9** | `backend/openapi.yaml:80-86` | Exemple `endpoints` : 2 entrées | Le code en renvoie **8** |
| **10** | `backend/openapi.yaml` | **`POST /api/v1/suivi` est absente** | Elle existe (`parcours.ts:393`), est annoncée par `/api/v1` (`v1.ts:75`) et a **8 tests** |
| **11** | `backend/openapi.yaml:195-198` | `requestBody` de `/corrections` : `exerciceId`, `reponse`, `indiceDemande` | `nbEchecs` est **accepté et exploité** (`parcours.ts:268`, `tutorat.ts:209`) mais non documenté |
| **12** | `backend/openapi.yaml:352-397` | Schéma `Correction` | Ni `categorieDifficulte` ni `tutorat` n'y figurent, alors que le code les renvoie (`parcours.ts:316-317`) |
| **13** | `backend/openapi.yaml:250-251` | Réponse 200 de `/progression` sans `content`/`schema` | Le schéma `ProgressionObjectif` **existe** en `components` (l.482-500) mais **n'est référencé par aucune route** — composant mort |
| **14** | `backend/openapi.yaml:500-536` | Réponses `NotFound` et `InternalError` définies | **Jamais référencées** par une route (qui déclare `'404': description: …` en texte libre) — réponses orphelines |
| **15** | `backend/openapi.yaml:5` | `info.version: 1.0.0` | `docs/CONTRAT-API.md:3` déclare « Version du document : **2.0.0** » |
| **16** | `backend/docs/CONTRAT-API.md:51-59` | §3 liste 7 routes | `/api/v1/suivi` manque |
| **17** | `backend/docs/CONTRAT-API.md:116` | Le **422** renvoie `error.code: BAD_REQUEST` | Le code renvoie `{erreurSaisie, message, exerciceId, categorieDifficulte, tutorat}` — **pas** la forme `{error:{code,message}}`. **Un frontend conforme au contrat obtient `undefined` sur `body.error.code`** |
| **18** | `backend/docs/CONTRAT-API.md:145` | §5 liste les codes 502/503 | Aucun code ne produit 503 ; `SERVICE_UNAVAILABLE` n'est jamais émis |
| **19** | `backend/docs/CONTRAT-API.md:197` | §9 « Correction sur **trois** axes » | Le code expose **quatre** axes (`correction.ts:4-24`) |
| **20** | `backend/docs/CONTRAT-API.md:93-97` | §4.1 : exemple `/api/v1` avec 2 endpoints | Le code en renvoie 8 |
| **21** | `backend/docs/CONTRAT-API.md:258` | §12 : `lectureArbitree: false` est un point ouvert | **Inatteignable** : les 12 exercices ont tous `regleFormeArbitree: true` |
| **22** | `frontend/DESIGN_SYSTEM.md:214-215` | « Le contrôle du CSS est automatisé : `npm run verifier:poids`, **branché dans la CI après le build** » | **Absent de `ci.yml`**, absent de `build`, absent de `test`. Le budget CSS **n'est pas gardé automatiquement** |
| **23** | `frontend/DESIGN_SYSTEM.md:209` | CSS 6,8 Ko gzip | Mesure réelle : **6,98 Ko** |
| **24** | `frontend/README.md:60-90` | « 🔴 `API_BASE_URL` est figée AU BUILD, pas au runtime », « ○ (Static) prerendered as static content » | Bug **corrigé** depuis par `force-dynamic`. Le `prerender-manifest.json` actuel ne contient plus que `/_not-found` et `/design-system` |
| **25** | `Relio/README.md:59-61` | « Les rapports d'étapes antérieures ont été retirés de `docs/` le 2026-10-10 » | **10 rapports postérieurs** à ce nettoyage sont présents dans `docs/` (chantiers 6, 7, 7.1→7.7, design-system), commités le même jour. Le README n'en référence **aucun** |
| **26** | `Relio/README.md:85` | Renvoie à `ci-workflows-chantier-5.md` (« contrôle du jeton GitHub ») — CI 🔴 non activée | `rapport-final-chantier-7-6.md:24,121` et `rapport-final-chantier-7-7.md:286-287` déclarent la CI **verte** ; les fichiers `.github/workflows/ci.yml` existent bien dans les deux dépôts |
| **27** | `Relio/docs/rapport-design-system.md:287-292` | Le contrôle du poids CSS « n'est pas branché dans la CI » pour cause de jeton sans scope `workflow` | Même incohérence que `chantier-5`, alors que `chantier-7-6` déclare la CI verte. Le rapport design-system est horodaté **après** `chantier-7-6` (23:25 vs 22:59 UTC) |
| **28** | `Relio/README.md:75-77` | « Contenu unique : **le seul exemplaire** des 26 objectifs `OO-Lx-y` […] Rien de tout cela n'existe ailleurs » | **117 occurrences de `OO-Lx-y` dans `frontend/`+`backend/`**, dont 5 objectifs distincts dans `backend/src/contenu/blocs.ts` (`OO-L1-1`, `OO-L1-2`, `OO-L3-1`, `OO-L5-1`, `OO-L5-2`). **L'affirmation est fausse pour ces 5 objectifs sur 26.** Confirmée pour `ORIG-M3-Q0n` et `SONDE-M3-Sn` (0 occurrence hors docs) |
| **29** | `Relio/docs/specification-diagnostic-initial.md:6` et `regles-recommandation-pedagogique.md:6` | « ⚠️ **AUCUN DÉVELOPPEMENT NE DOIT COMMENCER AVANT VALIDATION** (contrainte de mission) » | Le chantier 7 a implémenté le MVP 3 blocs / 12 exercices sur la base de cette spécification non validée. `rapport-final-chantier-6.md:7` maintient « 🔴 AUCUNE VALIDATION PÉDAGOGIQUE N'EST ACQUISE ». **La contrainte a été contournée par les faits ; rien dans les docs n'enregistre cette décision** |
| **30** | `Relio/docs/rapport-final-chantier-7.md:367` (réserve C5) | « les workflows existent mais ne s'exécutent pas » si le jeton n'a pas le scope | `chantier-7-6` et `7-7` constatent des exécutions `success`. Périmé, non signalé |
| **31** | `Relio/docs/rapport-final-chantier-7-2.md:190` vs `rapport-final-chantier-7.md:454` | `ANNEE_SCOLAIRE_DEBUT` = `2026-09-05` vs `2025-09-01` | **Trois valeurs distinctes** pour la même variable à travers les docs, sans arbitrage. La production réelle renvoie `2026-09-07` (vérifié) |
| **32** | `Relio/docs/rapport-final-chantier-7-1.md:395` | R3 « Visibilité du dépôt GitHub (contenus officiels du BEPC versionnés) — non vérifiée », **juridique** | Les **4 PDF BEPC (2,03 Mo)** sont versionnés dans le dépôt racine, alors que `README.md:40-45` qualifie ces contenus d'« outil d'analyse interne » avec « droits de reproduction non établis ». **Réserve signalée, jamais traitée** |
| **33** | `Relio/docs/rapport-final-chantier-6.md:73,544` | `rapport-final-mission-3.md` « 🔴 Retiré du dossier de travail », récupérable « depuis l'historique Git (`fb7fbeb^`) » | Le document source de la spécification n'est plus accessible que par l'historique Git, alors que `README.md:75-77` qualifie les docs de « Contenu unique […] Rien de tout cela n'existe ailleurs » |
| **34** | Dates | Commits datés du 2026-10-10 UTC | `rapport-design-system.md:3`, `rapport-final-chantier-7-6.md:3`, `rapport-final-chantier-7-7.md:3` affichent « 11 octobre 2026 ». Décalage non tranché |

**Bilan quantification :** 12 affirmations du `README.md` backend contredites par son propre code · 10 écarts entre `openapi.yaml` et le code · 8 écarts entre `CONTRAT-API.md` et le code · 4 écarts dans la documentation frontend · 10 contradictions dans la documentation racine.

**Documents dont les affirmations ont été vérifiées exactes :** SHA-256 et codes de sortie du README racine ; structure du référentiel (14 leçons, 98 h, 3 trimestres, 30 semaines) ; inventaire (35 questions) ; champs de compétences vides ; en-têtes de sécurité mesurés en production au chantier 4 ; conformité CORS.

---

## 14. SECTION 12 — DETTE TECHNIQUE VISIBLE

*(Constat factuel, sans jugement.)*

### 14.1 TODO / FIXME / HACK

**Backend :** `grep -i "TODO|FIXME|HACK|XXX|BUG:|@deprecated|@ts-ignore|eslint-disable"` sur `src/`, `test/`, `docs/`, `.github/`, `README.md`, `openapi.yaml`, `.env.example` → **0 occurrence**.

**Frontend :** `grep -i "todo|fixme|hack|xxx|@deprecated|workaround"` sur `src/` → **0 occurrence**.

Les 5 résultats sur « plus tard » du frontend sont du texte d'interface ou des commentaires. La dette est portée autrement, sous forme de commentaires `⚠️` (ex. `correction.ts:40`, `tutorat.ts:245-249`, `exercices.ts:155-159`, `README.md:158`) et par les sections « Ce qui n'existe pas encore » et « Points laissés ouverts » de `CONTRAT-API.md` (§9 et §12).

### 14.2 Code commenté laissé en place

**Aucun, dans les deux dépôts.** Le grep des lignes commentées ne révèle que de la documentation de conception en français, pas de listings commentés. `console.*` → **0 occurrence**. `alert(` → **0**. `debugger` → **0**.

### 14.3 Exports morts ou orphelins — backend

**12 exports ne sont consommés que par la suite de tests :**

`prerrequisSatisfaits` (`blocs.ts:101`), `prerequisAtteints` (`progression.ts:129`), `decrire` (`analyseur-reponse.ts:303`), `sontAlgebriquementEgales` (`analyseur-expression.ts:459`), `versNombre` (`algebre.ts:70`), `estCarreParfait` (`algebre.ts:84`), `racineCarreeEntiere` (`algebre.ts:89`), `nombreDeTermes` (`analyseur-expression.ts:486`), `categoriePourSignature` (`tutorat.ts:181`), `SEMAINE_DEBUT` (`blocs.ts:20`), `NOMBRE_SEMAINES` (`calendrier.ts:28`), `separerEgalite` (`egalite.ts:71`).

**5 symboles totalement orphelins (0 référence dans tout le dépôt) :**

| Symbole | Emplacement | Constat |
|---|---|---|
| `LECTURE_PARTIELLE` | `contenu/correction.ts:77` | Exporté, 0 référence |
| `polynomeNul` | `lib/analyseur-expression.ts:321` | Exporté, 0 référence |
| `FormeReponse` | `contenu/types.ts:124` | Type exporté, 0 référence — vestige d'un modèle antérieur |
| `ValeurAttendueCalculee` | `contenu/types.ts:126` | Alias `= Valeur`, 0 référence |
| `SERVICE_UNAVAILABLE` | `lib/errors.ts:12` | Membre de l'union `ErrorCode`, **jamais émis** |

**Fichiers `src/` jamais importés : aucun.** Les 22 fichiers sont atteignables depuis `server.ts`.

**Documentation morte dans `openapi.yaml` :** composants `NotFound` et `InternalError` (l.500-536) et schéma `ProgressionObjectif` (l.482-500) sont définis mais **référencés par aucune route**.

**Imports redondants :** `routes/index.ts:2` importe `health.ts` pour `registerHealthRoutes`, et `:3` importe `v1.ts` pour `registerV1Routes` — or `health.ts` est un ré-export de `v1.ts`. Le même module est chargé par deux chemins.

**Code mort en `openapi.yaml` :** `formeDemandee` n'est pas dans `required` (l.326) alors que le code le renvoie toujours (`parcours.ts:72`).

### 14.4 Exports morts ou orphelins — frontend

**4 composants/hook React client sans aucun consommateur :**

| Symbole | Emplacement | Poids |
|---|---|---|
| `FournisseurNotification` | `components/ds/Toast.tsx:54` | — |
| `ZoneNotification` | `components/ds/Toast.tsx:95` | — |
| `useNotifications` | `components/ds/Toast.tsx:86` | — |
| **Total `Toast.tsx` + `Toast.module.css`** | | **122 + 81 lignes** |

**1 fichier mort :** `components/ds/index.ts` (barrel, 27 l.) — jamais importé, le catalogue importe chaque fichier directement.

**Fonctions et constantes sans consommateur applicatif :**

`libelleCategorie` (`lib/tutorat.ts:98`) et `LIBELLE_CATEGORIE` (`:85`) ; `nombreTentatives` (`lib/observations.ts:194`) ; `touchesPour` (`lib/clavier.ts:434`) et `largeurRangee` (`:447`) ; `TOKENS` (`design/tokens.ts:266`), `variablesCss` (`:282`), `INTERLIGNAGES` (`:194`), `POLICE` (`:206`), `OMBRES` (`:225`), `RUPTURES` (`:256`) ; `IconeProps` (`ds/Icone.tsx:52`) ; ré-export `Verdict` (`lib/tutorat.ts:113`).

**Soit ≈ 18 symboles exportés sans consommateur, dont 203 lignes de composant mort.**

**Conséquences fonctionnelles de ces exports morts :**

- `Exercice.tsx:133` utilise `totalTentatives()` là où `nombreTentatives()` existe ; le libellé affiché (`Exercice.tsx:287`) dit « N tentatives enregistrées **sur cet exercice** » alors que le nombre est **global à l'appareil**.
- `Exercice.tsx:153` reçoit `correction.categorieDifficulte` mais **ne l'affiche jamais** (`libelleCategorie` n'est pas importé). La promesse « aucune clé technique affichée à l'élève » est respectée par simple non-utilisation, pas par la fonction prévue.
- `RUPTURES` (360/420/768) n'est consommée par **aucun media query**.
- `OMBRES` du token TS n'est jamais vérifiée contre `tokens.css` : la page `/design-system` affiche les ombres via `var(--relio-ombre-${nom})` en CSS (`PageDesignSystem.tsx:278`).

**Fichiers applicatifs jamais importés : aucun.** `src/lib/navigation.test.ts` et `src/lib/securite.test.ts` **n'ont pas de module source** : ce sont des tests d'architecture qui analysent statiquement le dépôt.

### 14.5 Duplications manifestes

| Duplication | Emplacements | Nature |
|---|---|---|
| **Système de style complet** | `design/tokens.css` (191 l., ~90 variables `--relio-*`) **vs** `globals.css:1-20` (16 variables `--*`) | Deux palettes, deux échelles typographiques, deux systèmes de rayons divergents. `globals.css` n'utilise **aucune** variable `tokens.css` |
| **Double déclaration `.bouton`** | `globals.css:303-314` **et** `globals.css:477-487` | La seconde écrase la première ; vérifié dans le CSS compilé (offsets 7357 vs 9647). Effet observable : le bouton principal de l'accueil s'affiche **blanc au repos, bleu au survol** |
| Double lecture de `NODE_ENV` | `backend/src/config.ts:80` (avec validation) et `backend/src/routes/v1.ts:45` (sans) | Deux chemins de lecture distincts pour la même variable |
| Deux chemins d'import du même module | `backend/src/routes/index.ts:2` et `:3` | `health.ts` ré-exporte `v1.ts` |
| Test de contraste dupliqué en deux versions | `design/contraste.ts` (85 l.) existe, mais **aucun contrôle n'est appliqué à `globals.css`** | L'outil est là, le contrôle n'est branché que sur `src/components/ds` |

### 14.6 Dépendances non utilisées ou redondantes

**Vérification :** les **5 dépendances de production** (2 backend + 3 frontend) sont **toutes réellement importées**. Les **10 dépendances de développement** (3 backend + 7 frontend) sont **toutes utilisées** par les runners, le compilateur ou la configuration.

**`npm audit` : 0 vulnérabilité** sur les deux dépôts après `npm ci` (2026-10-11). `overrides: { postcss: ^8.5.29 }` est en place dans le `package.json` frontend depuis le chantier 5.

**Aucun redondant constaté.** Les seules Redondances sont des **exports** (§14.3, §14.4), pas des dépendances.

### 14.7 Points d'incohérence relevés à la lecture du code

| Constat | Emplacement |
|---|---|
| Branches de `forme-non-arbitree` **inatteignables** : les 12 exercices ont tous `regleFormeArbitree: true` | `correction.ts:392-405`, `exercices.ts` |
| Deux branches `else if` consécutives (`tutorat.ts:189-191`) renvoient **le même** `niveau: 'a_confirmer'` — la première condition est avalée par la seconde quant au résultat |
| Casts de contournement `AIDES_PAR_OBJECTIF[objectifId as ObjectifId]` | `tutorat.ts:285`, `tutorat.ts:396` |
| Fonction nommée `Sajouter` (capital S) au milieu de fonctions en camelCase | `analyseur-expression.ts:327` |
| Un commentaire contient le mot anglais « trusting » au milieu d'une phrase française | `suivi.ts:99-100` |
| `Icone.tsx:74` pose `className="icone"` — **cette classe n'existe dans aucune feuille de style** de tout `src/` | `ds/Icone.tsx:74` |
| `BoutonIcone.module.css:9` déclare un `min-height` mais **ne compose pas `cible`** (`base.module.css`) | `ds/BoutonIcone.module.css` |
| Un composant `use client` (`PageDesignSystem.tsx`) est rendu par une page serveur dont la garde d'environnement s'exécute avant — la garde ne peut donc pas s'appliquer au HTML prérendu | `design-system/` |
| Faute d'accord dans un texte livré à l'utilisateur : « Le service de exercices n'est pas configuré » | `lib/parcours.ts:139` |
| Texte affiché factuellement inexact : « tes réponses ne sont pas conservées » alors qu'elles sont dans `localStorage` (500 entrées) et transmises au serveur à chaque tentative | `app/page.tsx:177-180` |
| `src/lib/` importe `src/contenu/` (types) — le sens de dépendance inverse la séparation annoncée | `suivi.ts:29`, `progression.ts:26`, `types.ts:9`, `correction.ts:503`. Tous des `import type`, donc **erasés à la compilation** — aucun cycle runtime |
| Valeur d'exemple `.env.example` pointant le backend vers le port **3000**, qui est aussi le port par défaut de `next dev` | `frontend/.env.example` |
| `DESIGN_SYSTEM_ENABLED` lue en production mais **absente de `.env.example`** | `frontend/design-system/page.tsx:38` |

---

## 15. TABLEAU FINAL « CE QUI EXISTE / CE QUI MANQUE / CE QUI EST FRAGILE »

### 15.1 Ce qui existe (vérifié)

| Domaine | Élément | Preuve |
|---|---|---|
| Infra | 3 dépôts Git séparés, working trees propres | `git status` vide sur les trois |
| Infra | Deux déploiements en ligne et alignés sur le code | HTTP 200 sur Railway et Vercel, `status: mvp-pedagogique`, `debut: 2026-09-07` |
| Infra | CI GitHub Actions présente et exécutée dans les 2 dépôts applicatifs | `.github/workflows/ci.yml` dans les deux |
| Backend | 8 routes Fastify, toutes fonctionnelles et testées | `src/routes/` + 307 tests |
| Backend | Moteur algébrique exact en `bigint`, sans flottants | `algebre.ts`, `analyseur-expression.ts` 491 l. |
| Backend | Correction à 4 axes avec décision pédagogique D5 confirmée par l'enseignant | `correction.ts` 504 l., `decision-d5.test.ts` 23 tests |
| Backend | Tutorat déterministe à 3 niveaux, **aucune IA, aucun appel externe** | `tutorat.ts` 579 l., 29 tests |
| Backend | 12 exercices originaux avec 3 indices et 3-4 pièges documentés chacun | `exercices.ts` 337 l., contre-vérifiés par `contenu.test.ts:381` |
| Backend | Progression par objectif, règle des trois, sans niveau global | `progression.ts` 144 l., 15 tests |
| Backend | Contrôle d'accès calendrier appliqué par un point unique | `parcours.ts:177-189` |
| Backend | Validation stricte de la configuration au démarrage (refus de démarrer si invalide) | `config.ts` 88 l., 8 tests |
| Backend | Neutralisation des messages d'erreur Fastify en 4xx, vérifiée en production | `error-handler.ts`, `rapport-final-chantier-5.md:288` |
| Backend | Audit des messages affichés aux élèves : 16/45 corrigés, **aucune clé technique exposed** | `rapport-final-chantier-7-4.md`, `aides.test.ts` 24 tests |
| Backend | Confinement du contenu BEPC au serveur | `lib/securite.test.ts` (test d'architecture) |
| Frontend | 4 routes rendues, parcours nominal complet de bout en bout | Build + vérification en ligne |
| Frontend | Clavier mathématique à 9 rangées, ouverture automatique, mesure du clavier système | `ClavierMath.tsx`, `useHauteurClavierSysteme.ts` + 6 tests |
| Frontend | Journal local validé, plafonné à 500, effaçable par l'élève | `observations.ts` 233 l., 15 tests |
| Frontend | `cache: 'no-store'` sur les 6 requêtes ; timeout sur chacune | `api.ts:25,48`, `parcours.ts:115,125` |
| Frontend | Tests d'architecture verrouillant les liens internes, l'absence de secret, l'absence de contenu BEPC | `navigation.test.ts` 7, `securite.test.ts` 6 |
| Frontend | Budget CSS respecté avec large marge : **6,98 Ko gzip / 30 Ko** | `verifier-poids-css.mjs`, mesure sur le build |
| Frontend | Aucune image bitmap, aucune police distante, aucun script tiers | `accessibilite.test.ts:143,153` |
| Frontend | Erreurs de réseau traitées avec des messages compréhensibles pour l'élève | 5 états distincts, tous rendus |
| Design system | 14 composants, tokens TS↔CSS empêchés de divergir par test, contrastes AA, cibles 44 px, focus trap correct | 300 lignes de tests, 0 échec |
| Données (racine) | Référentiel annuel (14 leçons, 98 h, 3 trimestres, 30 semaines) et inventaire BEPC (35 questions), **SHA-256 vérifiés** | Recalculés : exacts |
| Données (racine) | 4 validateurs exécutables, **codes de sortie conformes à la documentation** | `exit 2` et `exit 0` constatés |
| Docs (racine) | 16 rapports de chantier, chronologie complète de 25 commits | `git log` du 2026-10-10 |

### 15.2 Ce qui manque (vérifié absent)

| Domaine | Élément manquant | Preuve de l'absence |
|---|---|---|
| Backend | **Toute base de données** | `grep pg\|prisma\|sqlite\|mysql\|redis\|DATABASE_URL` → 0 ; dépendances prod = 2 |
| Backend | **Toute persistance** | 0 écriture ; champs `avertissement`/`conservation` dans les réponses |
| Backend | **Authentification** | Aucun header lu dans `src/routes/`, aucune dépendance |
| Backend | **Rate limiting** | Aucune dépendance, aucun code ; aucun en-tête `ratelimit*` en production |
| Backend | **Validation par schéma** | `grep "schema:"` → 0 ; `openapi.yaml` déclare des schémas non appliqués |
| Backend | **CSP / en-têtes de sécurité applicatifs** | Aucune dépendance (`helmet` absent), aucun header posé par le code |
| Backend | Compression | Aucune dépendance |
| Frontend | **Adoption du design system** | `grep "components/ds"` → 1 fichier, le catalogue lui-même |
| Frontend | **Aucun test de rendu applicatif** | 0 test sur `Exercice.tsx` (463 l.), `ClavierMath.tsx`, `ApiStatus.tsx`, `ParcoursServeur.tsx` |
| Frontend | **Aucun test e2e**, aucun runner de navigateur | Ni Playwright ni Cypress dans les dépendances |
| Frontend | **Aucune couverture de code mesurée** | `coverage` non configuré dans `vitest.config.mts` |
| Frontend | **CSP** | Absente de `next.config.ts` |
| Frontend | `error.tsx`, `loading.tsx`, `not-found.tsx`, `middleware.ts` | Aucun de ces fichiers dans `src/app/` |
| Frontend | Branchement de `verifier:poids` | Absent de `ci.yml`, `build` et `test` |
| Frontend | Linter | Aucune configuration ESLint/Biome/Prettier |
| Frontend | Dependabot | Aucune configuration |
| Produit | **Diagnostic initial / mini-évaluation de 5 questions** | Décrit dans 2 docs ; `ORIG-M3-Q0n` → 0 occurrence dans le code |
| Produit | **6 sondes `SONDE-M3-S1..S6`** | Décrites dans `regles-recommandation-pedagogique.md` ; **0 occurrence** dans le code |
| Produit | **Suites d'exercices BEPC** | 35 questions inventoriées ; **aucune importée** ; contenu BEPC interdit dans `src/` par `securite.test.ts` |
| Produit | **Comptes élèves, protection des mineurs** | « D9/D10 — hors MVP » (`rapport-final-chantier-7.md:369`) |
| Produit | **Tuteur IA** | `IA_PROVIDER_KEY` commentée ; aucun SDK, aucun appel réseau |
| Produit | **Consentement, politique de confidentialité** | Aucun texte dans l'application |
| Produit | Espace enseignant, suivi de classe | N'existe nulle part |
| Produit | Validation pédagogique des objectifs | Les 2 spécifications portent « AUCUN DÉVELOPPEMENT AVANT VALIDATION » ; aucune trace de validation dans les docs |
| Dépôt racine | **CI** | `ls .github` → inexistant |
| CI | Exécution de `verifier:poids` | Absent de `ci.yml` |
| CI | Audit de dépendances bloquant | `continue-on-error: true` |

### 15.3 Ce qui est fragile (constaté)

| Fragilité | Manifestation concrète | Gravité pour l'utilisateur final |
|---|---|---|
| **Clavier mathématique inutilisable au clavier physique** | `ClavierMath.tsx:188` n'écoute que `onPointerDown`, aucun `onClick` sur des `<button type="button">`. **Les 25 touches, y compris « Masquer » et « Clavier système », sont inopérantes au clavier, au commutateur et à la technologie d'assistance** | 🔴 Bloquant pour l'accessibilité. **Non testé** : aucun test de rendu ne l'aurait détecté |
| **Bouton principal de l'accueil mal rendu** | Double déclaration `.bouton` (`globals.css:303` et `:477`) ; la seconde écrase la première. Vérifié dans le CSS compilé (offsets 7357 vs 9647). Résultat : **blanc au repos, bleu au survol** | 🔴 Visible immédiatement sur la page d'accueil |
| **Champ de saisie et touches du clavier à 1,26:1 de contraste** | `#e2e5ef` sur `#fff`, seule bordure de `globals.css`. Le design system a résolu le problème (`--relio-bordure-forte` 3,48:1) sans que `globals.css` le reprenne | 🔴 Champ de saisie non repérable |
| **`/design-system` renvoie 404 en production** | Vérifié par requête réelle (HTTP 404) et dans le build (`<html id="__next_error__">`). Page **prérendue en erreur** ; poser `DESIGN_SYSTEM_ENABLED=on` ne suffit pas | 🟠 Le design system n'est de toute façon pas utilisé par l'application |
| **`role="note"` inexistant en ARIA, 3 fois** | `page.tsx:97`, `parcours/page.tsx:50`, `ParcoursServeur.tsx:68`. Les lecteurs d'écran **ignorent** ces bandeaux d'avertissement | 🟠 L'élève ne peut pas être averti |
| **Texte affiché inexact** | « tes réponses ne sont pas conservées » (`page.tsx:177-180`) alors que le `localStorage` conserve 500 réponses et que le journal complet est envoyé au serveur à chaque tentative | 🟠 Engagement de véracité de l'interface |
| **Conséquence de l'absence d'authentification** | La clé `localStorage` est globale au navigateur : n'importe qui sur le même téléphone peut **lire et effacer l'historique d'un autre élève** | 🟠 Partage de poste |
| **API sans authentification ni limitation de débit** | `POST /api/v1/suivi` accepte un journal complet de n'importe quel contenu ; `POST /api/v1/corrections` exécute un parseur récursif. Seule limite : `bodyLimit` 1 Mo (défaut Fastify) | 🟠 Exposition CPU et de données |
| **`/suivi` absente de toute la documentation d'API** | Absente d'`openapi.yaml` et du §3 de `CONTRAT-API.md`, alors qu'elle est implémentée, annoncée et a 8 tests. **§4.2 décrit un 422 au format `{error:{code}}` que le code ne produit pas** → un frontend conforme au contrat casse sur les réponses illisibles | 🟠 Intégration |
| **`README.md` du backend obsolète sur 12 points** | Annonce « socle », « deux routes », `status: socle`, 7 fichiers, aucune fonctionnalité pédagogique | 🟠 Le document d'accueil du repo décrit un produit inexistant |
| **Valeurs d'environnement critiques absentes de `.env.example`** | `ANNEE_SCOLAIRE_DEBUT` et `DATE_NAVIGATION_TEST` (backend) lues mais non documentées. **`DATE_NAVIGATION_TEST`, si définie en production, figerait la date pour toute l'application.** `DESIGN_SYSTEM_ENABLED` (frontend) idem | 🟠 Configuration d'opérateur |
| **Budget CSS non gardé automatiquement** | `verifier:poids` n'est ni dans la CI, ni dans `build`, ni dans `test`. `DESIGN_SYSTEM.md:214` affirme le contraire | 🟡 Un dépassement passerait la CI verte |
| **Mise en page binaire, non adaptative** | Un seul breakpoint de largeur (544 px). Rien entre 360 et 543 px. À 768 px, `.exercice--saisie` impose `100dvh` pour une carte de ~600 px de contenu | 🟡 Confort tablette |
| **Erreurs d'accessibilité non corrigées, hors design system** | Aucune vérification automatique ne porte sur `globals.css` (851 l.). Le 44 px n'est appliqué qu'aux composants `ds/`. Les `.lien` de navigation mesurent ~20 px de haut | 🟡 Cibles tactilles des liens de retour |
| **`src/lib` dépend de `src/contenu`** | Le sens de dépendance inverse la séparation annoncée. `import type` uniquement → aucun cycle runtime aujourd'hui, mais la frontière est franchie | 🟡 Structurel |
| **Documentation racine en retard de 10 rapports** | Le README ne référence ni le chantier 6, ni 7, ni 7.1→7.7, ni le design system. Il décrit un état antérieur au 2026-10-10 | 🟡 Traçabilité |
| **Réserve R4 / D6 jamais close** | Jeton GitHub « actif (HTTP 200) », périmètre plus large que le dépôt `Relio`, signalé dans 3 rapports successifs ; la procédure de révocation est écrite 3 fois et n'a pas été exécutée ni reportée | 🔴 Voir « Zones d'ombre » |
| **4 PDF BEPC versionnés publiquement** | 2,03 Mo de contenus officiels du BEPC dans un dépôt GitHub public, alors que le README déclare leurs « droits de reproduction non établis ». Réserve R3 🔴 Critique, signalée et jamais traitée | 🔴 Juridique |
| **Spécification contournée** | 2 documents portent « AUCUN DÉVELOPPEMENT NE DOIT COMMENCER AVANT VALIDATION » ; le chantier 7 a implémenté le MVP sur cette base. Rien n'enregistre la décision | 🟠 Traçabilité |

---

## 16. ZONES D'OMBRE

Ce que l'audit **n'a pas pu vérifier**, et pourquoi.

| # | Non vérifiable | Raison |
|---|---|---|
| **1** | **Comportement sur un téléphone réel (360×640 px, Android)** | Aucun appareil, aucun émulateur, aucun `/dev/kvm` dans l'environnement. `docs/rapport-final-chantier-7-6.md` constate la même impossibilité. Toutes les mesures 360/390/768 px de ce rapport sont des **calculs à partir du CSS et des dimensions de grille**, pas des rendus. L'effet réel du clavier système Android sur la disposition **n'est pas vérifié**. Les commentaires de `globals.css:585-586` (« environ 80 px ») et `:744-748` (« 453 px, 187 px restants ») **ne correspondent pas** aux valeurs recalculées (69,5 px ; ~220 px restants) — l'écart peut venir de la mesure réelle, du modèle de clavier de l'appareil, ou d'une erreur de calcul ; **non départageable ici** |
| **2** | **Les 6 questions de `specification-diagnostic-initial.md` et les 6 sondes `SONDE-M3-S1..S6`** | Ce sont des documents de spécification, pas du code. Leur conformité à un référentiel officiel **n'est pas vérifiable** : le référentiel annuel déclare **0 compétence, 0 objectif, 0 prérequis** sur ses 14 leçons. Aucun enseignant n'a validé (`rapport-final-chantier-6.md:7`) |
| **3** | **Droits de reproduction des contenus BEPC** | Question juridique. Le README déclare lui-même « non établis ». `docs/rapport-final-chantier-7-1.md:395` la classe « non vérifiée ». **Seul un conseil juridique peut trancher** |
| **4** | **État réel de la CI GitHub (historique des exécutions)** | L'API GitHub n'a pas été interrogée pour l'historique des exécutions. Les affirmations des rapports 7.6/7.7 (« CI verte sur la totalité des commits ») sont **rapportées, pas confirmées**. Ce qui est **vérifié** : les **fichiers `.github/workflows/ci.yml` existent** dans les deux dépôts, et **le contenu du script de test est cohérent avec le contenu des tests** |
| **5** | **Scope exact du jeton GitHub d'accès** | L'API GitHub `/user` et `/user/installations` n'ont pas été interrogées. Les scopes (`repo`, `workflow`, `admin:org`, etc.) sont **inconnus**. Le message d'erreur historique cité dans `ci-workflows-chantier-5.md:220` indique un PAT **sans scope `workflow`**, mais cela date du chantier 5 et ne peut être reconfirmé ici |
| **6** | **Revocation de l'ancien jeton (réserve R4/D6)** | **Impossible à vérifier depuis un environnement fermé.** L'audit peut constater que les rapports la signalent comme non résolue, mais **la révocation se constate sur l'interface GitHub, pas depuis le dépôt**. De même, la portée de l'entrée `~/.git-credentials` créée lors du présent audit **n'a pas été inspectée** — c'est précisément le point que les rapports 7.7 et ultérieurs Hébergent |
| **7** | **Logs de production Railway** | `docs/rapport-audit-fiabilite-chantier-4.md:68-69` : « B13 Aucun secret dans les logs ⚪ **NON VÉRIFIÉ** \| Accès aux logs Railway non disponible ». L'audit reproduit cette limite : aucune lecture de logs n'a été possible. Un secret écrit en log par une route de correction resterait invisible ici |
| **8** | **Accessibilité réelle avec un lecteur d'écran** | `jsdom` n'implémente ni l'arbre d'accessibilité, ni les rôles, ni la navigation clavier d'un navigateur réel. Les constats « `role="note"` ignoré », « focus par défaut non stylé », « emoji lu littéralement » sont déduits de la **spécification ARIA et de l'absence de règle CSS**, pas d'un test avec NVDA/JAWS/VoiceOver |
| **9** | **Performance réelle (Core Web Vitals, LCP, INP, TTFB mesurés)** | Les poids sont exacts (sortie de `next build`, fichiers du bundle), mais **aucune mesure d'exécution** : pas de Lighthouse, pas de test de charge, pas de navigateur. Le temps de réponse frontend mesuré (871 ms pour `/`) est **une mesure réseau ponctuelle**, pas une métrique de performance |
| **10** | **Date exacte de la dernière mise en production** | `uptimeSeconds: 2416` (≈ 40 min) indique un redémarrage récent du conteneur, sans permettre de distinguer un redéploiement d'un redémarrage de plateforme. **Aucune API Vercel/Railway interrogée.** Le code en production correspond au HEAD local, mais l'instant du déploiement est indéterminable |
| **11** | **Rollback** | Aucun mécanisme n'a jamais été exercé. Il n'y a **aucun tag Git** dans les trois dépôts et **aucune politique de versionnement** documentée. La faisabilité d'un rollback (push sur `main` → redéploiement automatique) est **déduite** du fonctionnement déclaré de Vercel/Railway, pas testée |
| **12** | **Comportement de l'application en cas de perte réseau ou d'API indisponible** | Les fallbacks existent dans le code, mais **aucun test de rendu** ne les valide. `jsdom` avec `fetch` mocké ne reproduit pas le comportement d'un navigateur face à un vrai échec CORS (que le navigateur masque, comme le reconnaît `api.ts:88-89`) |
| **13** | **Données du `data/` de la racine** | `data/referentiel-maths-3e-cm-2025-2026.json` et `data/inventaire-questions-bepc-2025-2026.json` sont **transcrits manuellement** dans le code (`backend/src/contenu/blocs.ts` : 5 objectifs `OO-Lx-y`, 3 `leconId`). **Aucun contrôle automatisé ne vérifie que le code et les JSON restent synchronisés.** Une divergence serait silencieuse |
| **14** | **Exactitude du contenu des PDF BEPC** | `BEPC-MATHS-CORRIGE-2025.pdf` est décrit dans le code comme « **NUMÉRISÉ (scan sans couche texte) — rendu lisible par OCR** » (`generer-inventaire-bepc.py:50`). L'inventaire a été produit par OCR ; **l'exactitude arithmétique des 35 questions inventoriées n'a pas été revérifiée** dans cette session. Le rapport du chantier 5 corrige deux erreurs de compte ; **rien n'exclut d'autres écarts** |
| **15** | **Cohérence des documents du design system avec le code** | `DESIGN_SYSTEM.md` (10 284 o) et `rapport-design-system.md` (332 l.) n'ont été lus **qu'en partie** (résumé et contradictions principales). Une lecture ligne à ligne n'a pas été faite |

---

## 17. STATUT GLOBAL

# 🟡

**Justification :** l'existant est solide et vérifié — 562 tests passent, les builds et les types sont propres sur les deux dépôts, les deux déploiements sont en ligne et alignés sur le code, le moteur de correction exact et le tutorat déterministe sont largement couverts. Les deuxCEP et les deuxPDF sont néanmoins des risques ouverts et documentés (jeton, droits BEPC), et la validation pédagogique — condition posée par deux spécifications — n'est acquise nulle part dans les documents.
**Ce qui pèse dans le jaune plutôt que dans le vert :** un défaut fonctionnel d'accessibilité avéré (le clavier mathématique est inopérant au clavier physique, et aucun test ne le détecte), un bug de rendu visible sur la page d'accueil (double déclaration `.bouton`), et une documentation d'API qui décrit un contrat de 422 que le code ne respecte pas.
**Ce qui l'empêche d'être rouge :** aucune vulnérabilité de dépendance (`npm audit` : 0), aucun secret exposé côté client (7 motifs vérifiés automatiquement), aucune injection de contenu BEPC dans le bundle (test d'architecture vert), aucune base de données ni authentification à compromettre, et aucune régression détectée dans 562 tests.

---

## ANNEXE — COMMANDES D'AUDIT EXÉCUTÉES

```bash
# Installation
(cd backend  && npm ci)      # 0 vulnérabilité
(cd frontend && npm ci)      # 0 vulnérabilité

# Backend
(cd backend && npm run typecheck)   # tsc --noEmit → exit 0
(cd backend && npm test)           # 307 tests, 307 pass, 0 fail — 12,4 s
(cd backend && npm run build)      # tsc --project → exit 0

# Frontend
(cd frontend && npm run typecheck) # tsc --noEmit → exit 0
(cd frontend && npm run test:logique)  # 119 tests, 119 pass — 6,9 s
(cd frontend && npm run test:ui)       # vitest : 136 tests, 136 pass — 15,4 s
(cd frontend && npm run build)          # next build → exit 0, 24,4 s, 4 routes
(cd frontend && npm run verifier:poids) # 6,98 Ko gzip < 30 Ko → exit 0

# Dépôt racine (lecture seule)
node outils/valider-referentiel.mjs       # exit 2 (attendu)
node outils/valider-inventaire-bepc.mjs   # exit 0 (attendu)
sha256sum data/*.json                      # identiques au README

# Production (2026-10-11 ~00:25 UTC)
curl https://relio-backend-production-a2c3.up.railway.app/health          # 200, 143 o, 154 ms
curl https://relio-backend-production-a2c3.up.railway.app/api/v1          # 200, mvp-pedagogique, 8 endpoints
curl https://relio-backend-production-a2c3.up.railway.app/api/v1/parcours  # 200, 2026-09-07, semaine 5
curl https://relio-frontend-one.vercel.app/                                 # 200, 20 520 o, 871 ms
curl https://relio-frontend-one.vercel.app/design-system                    # 404
curl -X POST -H 'content-type: application/json' -d '{}' \
     https://relio-backend-production-a2c3.up.railway.app/api/v1/suivi      # pas de 401, pas de 429

# Contrôle de l'ordre de cascade dans le CSS compilé
node -e "const c=require('fs').readFileSync('.next/static/css/c5b3424d1cf8f1d7.css','utf8'); \
  const re=/\.bouton\{/g;let m;while((m=re.exec(c)))console.log(m.index,c.slice(m.index,m.index+80))"
```

**Fichiers modifiés pendant cet audit :** aucun dans les trois dépôts. Seul fichier créé : `/config/Relio/AUDIT_RELIO.md` (non commité). Aucune commande de commit ni de push n'a été exécutée.