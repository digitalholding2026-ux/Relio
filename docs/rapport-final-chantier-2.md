# Rapport final — Chantier 2 : création du socle applicatif Relio

**Date** : 2026-10-10
**Statut global** : ✅ **Socle créé et poussé dans les deux dépôts**
🔴 **Fonctionnement en exécution et déploiement : NON VÉRIFIÉ**

---

## 1. Résumé exécutif

Les deux dépôts applicatifs contiennent maintenant un **socle technique minimal,
typé, documenté et buildable**, conforme aux décisions validées (Next.js +
TypeScript / Fastify + TypeScript).

**Aucune fonctionnalité pédagogique n'est implémentée, et c'est délibéré.** Le
backend expose exactement deux routes (`/health`, `/api/v1`) ; son champ `status`
vaut `socle`. Le frontend décrit un parcours **prévu** et affiche un état
explicite (« Bientôt », « Prévu », « Non planifié ») sur chaque élément.

**Les contrôles statiques passent** : `typecheck` et `build` sont verts dans les
deux dépôts. **Le comportement en exécution n'a pas été vérifié** — le chantier
interdisait tout test manuel en local, et le propriétaire n'a pas encore déployé.

Point de conception notable : **le build du frontend n'effectue aucun appel
réseau**. L'état de la connexion à l'API est vérifié côté navigateur, au clic.
Le déploiement Vercel ne peut donc pas échouer parce que l'API est indisponible.

---

## 2. Dépôts et commits modifiés

| Dépôt | Commit | Contenu |
|---|---|---|
| `digitalholding2026-ux/relio-frontend` | **`569b280`** | Socle Next.js + TypeScript |
| `digitalholding2026-ux/relio-backend` | **`0b27b37`** | Socle Fastify + TypeScript |
| `digitalholding2026-ux/Relio` | **`6d481a3`** *(inchangé)* | Ajout de ce rapport uniquement |

Les deux dépôts existaient déjà (créés par le propriétaire) et ne contenaient
que le commit d'initialisation. **Aucun dépôt n'a été créé par moi.**

Le dépôt pédagogique `Relio` n'a reçu **que ce rapport**. Aucune donnée
pédagogique n'a été modifiée — empreintes SHA-256 vérifiées identiques :

```
f766f412…  data/referentiel-maths-3e-cm-2025-2026.json
d74a68fb…  data/inventaire-questions-bepc-2025-2026.json
```

---

## 3. Fichiers importants créés

### Backend — `relio-backend`

| Fichier | Rôle |
|---|---|
| `src/server.ts` | Démarrage, ouverture du port, signaux `SIGTERM`/`SIGINT` |
| `src/app.ts` | Construction de l'instance Fastify **sans ouvrir de port** |
| `src/config.ts` | Lecture **et validation** de l'environnement |
| `src/lib/errors.ts` | Erreurs applicatives ↔ codes HTTP |
| `src/plugins/cors.ts` | CORS en liste blanche |
| `src/plugins/error-handler.ts` | Gestion centralisée des erreurs et du 404 |
| `src/routes/index.ts` | Point d'entrée des routes |
| `src/routes/health.ts` | Ré-exports publics |
| `src/routes/v1.ts` | `/health` et `/api/v1` |
| `openapi.yaml` | Spécification OpenAPI 3.1 |
| `docs/CONTRAT-API.md` | Contrat d'intégration lisible |
| `.env.example` | 4 variables, aucune valeur secrète |
| `package.json`, `tsconfig.json`, `tsconfig.build.json` | Build TypeScript |

### Frontend — `relio-frontend`

| Fichier | Rôle |
|---|---|
| `src/app/layout.tsx` | Layout racine, métadonnées, viewport |
| `src/app/page.tsx` | Page d'accueil — **composant serveur** |
| `src/app/globals.css` | Styles mobile-first, sans framework UI |
| `src/components/ApiStatus.tsx` | Vérification réelle de la connexion |
| `src/components/parcours.ts` | Étapes du parcours prévu |
| `src/lib/api.ts` | Client typé — ne fabrique jamais de réponse |
| `next.config.ts` | Configuration build + en-têtes de sécurité |
| `.env.example` | 1 variable, aucun secret |
| `package.json`, `tsconfig.json` | Build Next.js |

---

## 4. Architecture réellement implémentée

```
┌─────────────────────────────────┐        HTTPS / JSON        ┌──────────────────────────┐
│ relio-frontend (Vercel)        │  ────────────────────────▶  │ relio-backend (Railway) │
│                                │                            │                          │
│ page.tsx  (serveur)            │  GET /api/v1                │ routes/v1.ts             │
│   lit API_BASE_URL             │  GET /health                │ plugins/cors.ts          │
│   ↓ prop                      │                            │ plugins/error-handler.ts │
│ ApiStatus (client)             │                            │ config.ts (validation)   │
│   fetch() au clic              │                            │ server.ts (écoute PORT)  │
└─────────────────────────────────┘                            └──────────────────────────┘
       aucune donnée embarquée                                          aucune base de données
```

**Séparation `app.ts` / `server.ts`** : `buildApp()` construit sans écouter, ce
qui rend l'application testable sans ouvrir de port.

**Aucune base de données.** Rien dans les deux routes ne le justifie. Elle est
documentée comme étape ultérieure, avec la raison : le système de fichiers de
Railway est éphémère, un stockage fichier perdrait les profils d'élèves.

---

## 5. Vérifications effectuées — commandes et résultats

### Prévol

| Commande | Résultat |
|---|---|
| `git ls-remote` sur les 2 dépôts | Accessibles, 2 refs (branche `main`) |
| API GitHub — métadonnées des 2 dépôts | Public, `default_branch: main`, `push: true`, `admin: true`, non archivé |
| `git log --oneline` (local + distant) | 1 commit d'initialisation chacun, synchronisés |
| `git status` Relio | Propre — aucune collision |

**Découverte technique** : le premier push a échoué en **403**. Cause réelle —
`credential.helper=store` est configuré globalement avec un **ancien jeton** dans
`~/.git-credentials`, qui avait les droits sur `Relio` mais pas sur les nouveaux
dépôts. Le jeton fourni avait bien `admin` sur les trois. Correction : désactivation
du helper **uniquement** dans `backend/` et `frontend/`, sans casser le push de
`Relio`.

### Backend

| Commande | Résultat |
|---|---|
| `npm install` | 58 paquets — ⚠️ `EBADENGINE` : `cookie@2.0.1` (transitif) exige Node ≥ 22, environnement local en Node 20.20.2 |
| `npx tsc --noEmit` | **3 erreurs** → corrigées (typage du paramètre `error` dans `setErrorHandler`) |
| `npx tsc --noEmit` (2ᵉ passage) | ✅ **0 erreur** |
| `npm run build` | ✅ `dist/server.js` produit, cohérent avec `npm start` |

### Frontend

| Commande | Résultat |
|---|---|
| `npm install` | 29 paquets, aucune alerte |
| `npx tsc --noEmit` | **2 erreurs** → corrigées (variante `non-configure` du type `ApiState` sans champ `raison`) |
| `npx tsc --noEmit` (2ᵉ passage) | ✅ **0 erreur** |
| `npm run build` | ✅ Next.js 15.5.27 — 4 pages statiques générées, bundle 104 kB First Load |

**Les deux séries d'erreurs de typage étaient de vraies erreurs de code**, pas
des faux positifs : elles auraient livré un état `non-configure` affichant
`undefined`. Elles sont corrigées, pas contournées.

### Sécurité

| Contrôle | Résultat |
|---|---|
| Scan de secrets sur le contenu commité (2 dépôts) | ✅ **0 occurrence** |
| `git check-ignore` sur `.env`, `.env.local`, `node_modules`, `dist`, `.next` | ✅ Tous ignorés |
| Jeton dans une URL de remote ou un `.git/config` | ✅ **Aucune** |
| Contenu BEPC dans le code frontend | ✅ Aucun |
| Données d'élèves | ✅ Aucune |

---

## 6. Vérifications **non** effectuées, et pourquoi

| Vérification | Statut | Raison |
|---|---|---|
| Test manuel de l'application en local | ❌ **Non fait** | Interdit explicitement par le § 8 du cahier des charges |
| Réponse réelle de `GET /health` | ❌ **Non fait** | Implique de lancer le serveur |
| Réponse réelle de `GET /api/v1` | ❌ **Non fait** | Idem |
| Comportement CORS à l'exécution | ❌ **Non fait** | Idem |
| Affichage réel de la page sur mobile | ❌ **Non fait** | Nécessite un navigateur |
| Déploiement Vercel | ❌ **Non fait** | Aucune permission sur la plateforme |
| Déploiement Railway | ❌ **Non fait** | Aucune permission sur la plateforme |
| Base PostgreSQL | ❌ **Non faite** | Non nécessaire à ce socle |

> **Conséquence à assumer** : je peux affirmer que le code **compile** et que
> les fichiers sont **en place**. Je **ne peux pas** affirmer que l'API répond,
> que la page s'affiche correctement, ou qu'un déploiement fonctionne. Ces trois
> points sont `NON VÉRIFIÉ` jusqu'à votre intervention.

---

## 7. Risques de sécurité restants

| # | Risque | Gravité | Statut |
|---|---|---|---|
| S1 | **Droits sur les sujets et corrigés du BEPC non établis** | 🔴 Critique | Aucun contenu BEPC n'est importé dans les dépôts — la règle est documentée dans les deux README et dans le contrat |
| S2 | **PostgreSQL éphémère en offre Railway gratuite** | 🔴 Critique | Non encore configuré. À vérifier **avant** toute mise en ligne dès qu'une persistance sera ajoutée |
| S3 | Prévisualisations Vercel bloquées par une liste CORS stricte | 🟡 Moyen | Documenté dans le contrat § 7. Décision à trancher |
| S4 | `CORS_ORIGINS` vide → aucun appel navigateur accepté | 🟡 Moyen | Comportement voulu et journalisé en avertissement |
| S5 | **Jeton GitHub ancien dans `~/.git-credentials`** | 🟡 Moyen | Signalé. Ne concernait que les droits de push, pas les dépôts |
| S6 | Erreur de configuration au démarrage = service indisponible | 🟢 Faible | **Volontaire** : mieux vaut un échec net qu'un port faux |
| S7 | Stack trace renvoyée au client | 🟢 Faible | ✅ Empêché : journalisée serveur, message générique au client |
| S8 | Secret dans le bundle frontend | 🟢 Faible | ✅ Aucune variable `NEXT_PUBLIC_*` définie |

---

## 8. Actions manuelles que le propriétaire doit effectuer

### Backend — Railway

| # | Action | Valeur |
|---|---|---|
| M1 | Créer un service depuis `relio-backend` | — |
| M2 | Build Command | `npm run build` |
| M3 | Start Command | `npm start` |
| M4 | **Ne pas** définir `PORT` | Railway l'injecte |
| M5 | `NODE_ENV` | `production` |
| M6 | `CORS_ORIGINS` | `https://<frontend>.vercel.app` |
| M7 | Healthcheck Path | `/health` |
| M8 | ⚠️ Node.js 22 | Le paquet transitif `cookie@2.0.1` exige Node ≥ 22 |

### Frontend — Vercel

| # | Action | Valeur |
|---|---|---|
| M9 | Importer `relio-frontend` | Framework détecté : Next.js |
| M10 | Build Command | `npm run build` |
| M11 | `API_BASE_URL` | `https://<backend>.up.railway.app` |
| M12 | Environnements | Production, Preview **et** Development |
| M13 | Branche de production | `main` |

### Ordre

1. Déployer le **backend** (M1→M8).
2. Relever son URL publique.
3. Déployer le **frontend** (M9→M13) avec `API_BASE_URL` = URL du backend.
4. Ouvrir l'URL du frontend : l'encart « Connexion au service » doit indiquer
   **« Joignable »**, version `v1`, statut `socle`.

> Ce dernier point est **le premier test réel du système**. Si l'écran affiche
> « Indisponible », deux causes probables : `CORS_ORIGINS` mal renseigné côté
> Railway, ou `API_BASE_URL` incorrecte côté Vercel.

---

## 9. Écarts entre le plan et la réalisation

| # | Écart | Motif |
|---|---|---|
| E1 | **Fastify retenu**, conformément à la décision validée — le document d'audit du chantier 1 proposait aussi Fastify, alors que `integration-backoffice.md` disait NestJS | Décision validée appliquée. La contradiction de la mission 1 reste ouverte mais n'a pas bloqué |
| E2 | **`API_BASE_URL` sans préfixe `NEXT_PUBLIC_`** | Imposé par le cahier des charges. Conséquence : variable **serveur**, lue dans `page.tsx` et transmise par prop. C'est un choix correct ici — le build ne peut pas casser. Documenté dans le README et le contrat |
| E3 | Pas de PostgreSQL | Conforme : non nécessaire. Documenté comme étape ultérieure avec sa justification |
| E4 | `src/routes/health.ts` ne contient que des ré-exports | `health.ts` et `v1.ts` partagent les mêmes schémas de réponse ; éviter la duplication |
| E5 | `openapi.yaml` plutôt qu'un bundle de génération de clients | Le contrat est petit. Une génération automatique serait prématurée |

---

## 10. Critères d'acceptation

| # | Critère | Statut |
|---|---|---|
| 1 | Les deux dépôts correspondent aux URL attendues | ✅ **VALIDÉ** — vérifié via API GitHub |
| 2 | Le frontend utilise réellement Next.js + TypeScript | ✅ **VALIDÉ** — Next.js 15.5.27, build réussi, `tsconfig` strict |
| 3 | Le backend utilise réellement Fastify + TypeScript | ✅ **VALIDÉ** — Fastify 5, build réussi, `tsconfig` strict |
| 4 | Les changements sont poussés sur GitHub | ✅ **VALIDÉ** — `569b280` et `0b27b37` |
| 5 | Aucun secret dans les commits | ✅ **VALIDÉ** — scan sur le contenu commité, 0 occurrence |
| 6 | Aucun contenu BEPC ni donnée d'élève dans le frontend | ✅ **VALIDÉ** |
| 7 | Le contrat API est documenté et cohérent | ✅ **VALIDÉ** — `openapi.yaml` + `docs/CONTRAT-API.md`, routes identiques à celles implémentées |
| 8 | Contrôles statiques rapportés honnêtement | ✅ **VALIDÉ** — y compris les 5 erreurs de typage corrigées |
| 9 | Étapes manuelles documentées sans prétendre les avoir exécutées | ✅ **VALIDÉ** — § 8, et mention explicite dans les README |
| 10 | `Relio` intact, sauf le rapport | ✅ **VALIDÉ** — SHA-256 des 2 JSON inchangés |
| 11 | Limites clairement indiquées | ✅ **VALIDÉ** — avertissement en page d'accueil, `status: socle`, § 1 et § 6 |

**Critères complémentaires (hors liste imposée)**

| # | Critère | Statut |
|---|---|---|
| 12 | Les routes répondent réellement | 🔴 **NON VÉRIFIÉ** — pas de lancement de serveur |
| 13 | L'application s'affiche correctement sur mobile | 🔴 **NON VÉRIFIÉ** — pas de test navigateur |
| 14 | Les déploiements Vercel et Railway fonctionnent | 🔴 **NON VÉRIFIÉ** — aucune permission sur ces plateformes |
| 15 | CORS fonctionne à l'exécution | 🔴 **NON VÉRIFIÉ** |

> **Le chantier est terminé** au sens des critères imposés (1 à 11). Les points
> 12 à 15 sont explicitement **hors de ma portée** et restent à vérifier par le
> propriétaire après déploiement.

---

## 11. Prochaine étape proposée — **non exécutée**

**Commencer par le déploiement et le test de connexion**, avant toute
fonctionnalité.

1. Déployer le backend sur Railway (M1→M8), en **Node 22**.
2. Déployer le frontend sur Vercel (M9→M13).
3. Vérifier que l'écran affiche « Joignable », `v1`, `socle`.
4. **Signer d'ici là un petit contrat de vérification** : me confirmer le
   résultat du test 3, ou me transmettre les logs en cas d'échec.

**Ce que je ne propose PAS d'engager maintenant** : le moteur de diagnostic.
Il dépend d'objectifs pédagogiques validés par un enseignant, ce qui n'est pas
fait. L'écrire maintenant produirait du code correct mais ciblé au hasard.

**Décisions toujours ouvertes, à traiter avant le Chantier 3** :

| # | Décision | État |
|---|---|---|
| D1 | Droits sur les documents BEPC | 🔴 Ouvert — aucun contenu protégé n'est utilisé à ce stade |
| D2 | Faire relire les 5 questions par un enseignant | 🟡 Ouvert |
| D3 | Contenu attendu de la leçon 6 « Angles inscrits » | 🟡 Ouvert |
| D4 | Politique CORS pour les prévisualisations Vercel | 🟡 Ouvert |
| D5 | Offre Railway — persistance réelle ou éphémère | 🟡 Ouvert, à trancher **avant** la première persistance |

---

## 12. Statut du chantier

> ✅ Les livrables imposés sont présents dans les deux dépôts, poussés sur GitHub.
>
> 🔴 **Le Chantier 3 ne doit pas commencer** avant validation de ce rapport et
> résultat du test de connexion.

---

*Contrat d'intégration : `docs/CONTRAT-API.md` (dépôt backend).
Chantier 1 : `docs/audit-migration-architecture.md`, `docs/architecture-cible.md`,
`docs/plan-migration-depots.md`, `docs/plan-deploiement-vercel-railway.md`,
`docs/rapport-final-chantier-1.md`.*