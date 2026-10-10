# Rapport d'audit de fiabilité — Chantier 4

**Date** : 2026-10-10
**Fenêtre de test** : 2026-10-10, 10:32 → 10:37 UTC
**Périmètre** : `relio-frontend` (Vercel) et `relio-backend` (Railway) déployés
**Décision** : ⚠️ **ACCEPTABLE SOUS RÉSERVES** — voir § 1

> ⚠️ **Aucune modification n'a été poussée** pendant cet audit. Les trois
> dépôts sont inchangés (`git status` propre, HEAD identique à `origin/main`).
> Aucune fonctionnalité n'a été ajoutée.

---

## 1. Résumé exécutif et décision

### Décision : ⚠️ ACCEPTABLE SOUS RÉSERVES

Le socle est **sain pour ce qu'il est aujourd'hui** : aucune donnée d'élève, aucun
secret exposé, aucune surface d'attaque utilisateur, CORS correctement restreint,
contrôles statiques verts, en-têtes de sécurité présents.

**Mais trois réserves doivent être levées avant toute fonctionnalité destinée aux
élèves**, car le socle n'a pas encore la qualité de production qu'exigerait un
usage réel :

| # | Réserve | Pourquoi c'est bloquant avant la mise en production |
|---|---|---|
| R1 | 2 vulnérabilités npm (`postcss` élevée, `next` modérée) | Corrigeable sans rupture — **validé en laboratoire** |
| R2 | `API_BASE_URL` figée **au build**, pas au runtime | Piège opérationnel : changer la variable ne prend pas effet. Un basculement de backend casserait silencieusement la prod |
| R3 | **Aucun test automatisé, aucune CI, dans les deux dépôts** | Aucune garantie de non-régression sur le moteur de diagnostic |

**Ce qui n'est pas un problème** : aucune des vulnérabilités n'est exploitable par
un élève. `postcss` s'exécute à la **construction**, dans le conteneur Vercel, et
n'est pas livré au navigateur (vérifié : absent du bundle JS).

---

## 2. Tableau des contrôles

| # | Contrôle | Résultat | Preuve |
|---|---|---|---|
| **Frontend** ||||
| F1 | `API_BASE_URL` injectée au build ou lue au runtime | 🔴 **ÉCHEC** | URL sérialisée dans le payload RSC du HTML statique |
| F2 | Aucune clé privée exposée au navigateur | ✅ **Vérifié** | 6 chunks (472 Ko) scannés, 0 secret |
| F3 | Aucune variable `NEXT_PUBLIC_*` | ✅ **Vérifié** | 0 occurrence dans le bundle et le HTML |
| F4 | État succès | ✅ **Vérifié** | `GET /api/v1` → 200, contrat respecté |
| F5 | État erreur HTTP | ✅ **Vérifié** | 404 → « désynchronisé » ; non-2xx → « indisponible » |
| F6 | État indisponibilité réseau | ✅ **Vérifié** | `catch` → message explicite |
| F7 | État délai d'attente | ✅ **Vérifié** | `AbortController` à 5 000 ms |
| F8 | Aucun message technique sensible dans l'UI | ✅ **Vérifié** | Messages en français, orientés utilisateur |
| F9 | Pas de `eval` / `innerHTML` / `dangerouslySetInnerHTML` | ✅ **Vérifié** | 0 occurrence |
| F10 | Aucun stockage local ni cookie | ✅ **Vérifié** | `localStorage`/`sessionStorage`/`document.cookie` = 0 |
| F11 | Risques d'ergonomie mobile | 🟡 **Réserve** | Cibles tactiles ≈ 42 px (< 44 px recommandés) |
| F12 | Scripts test / typecheck / build | ✅ **Vérifié** | `typecheck` OK, `build` OK |
| F13 | Tests automatisés | 🔴 **Échec** | Aucun. Ni fichier, ni script |
| **Backend** ||||
| B1 | `GET /health` | ✅ **Vérifié** | HTTP 200, JSON, 138 ms |
| B2 | `GET /api/v1` | ✅ **Vérifié** | HTTP 200, JSON, version + statut |
| B3 | Route inconnue | ✅ **Vérifié** | HTTP 404, format d'erreur commun |
| B4 | Méthode non autorisée | ✅ **Vérifié** | `POST /health`, `DELETE /api/v1` → 404 |
| B5 | Corps JSON invalide | 🟡 **Réserve** | HTTP 400, mais message Fastify divulgué |
| B6 | CORS — origine autorisée | ✅ **Vérifié** | ACAO correct pour l'origine Vercel |
| B7 | CORS — origine inconnue | ✅ **Vérifié** | `evil.example.com` → **aucun** ACAO |
| B8 | CORS — attaque par suffixe | ✅ **Vérifié** | `…vercel.app.evil.com` → **aucun** ACAO |
| B9 | CORS — préflight | ✅ **Vérifié** | 204, méthodes et origine conformes |
| B10 | Pas de wildcard en production | ✅ **Vérifié** | Liste blanche stricte, `*` refusé au démarrage |
| B11 | Validation des variables au démarrage | ✅ **Vérifié** | `PORT`, `NODE_ENV`, `CORS_ORIGINS` validés |
| B12 | Aucun secret dans les réponses | ✅ **Vérifié** | Scan des réponses et en-têtes |
| B13 | Aucun secret dans les logs | ⚪ **NON VÉRIFIÉ** | Accès aux logs Railway non disponible |
| B14 | Routes ne divulguent pas l'interne | 🟡 **Réserve** | `server: railway-hikari` (niveau plateforme) |
| B15 | Gestion des erreurs | ✅ **Vérifié** | Format unique, pas de stack trace |
| B16 | Délais d'attente serveur | 🟡 **Réserve** | Aucun `requestTimeout` / `connectionTimeout` |
| B17 | Arrêt propre du serveur | ⚪ **NON VÉRIFIÉ** | `SIGTERM`/`SIGINT` présents dans le code, non testé |
| B18 | Dépendances | ✅ **Vérifié** | `npm audit` → 0 vulnérabilité |
| **Dépendances** ||||
| D1 | Identification des 2 vulnérabilités Vercel | ✅ **Vérifié** | `postcss@8.4.31` (élevée) via `next@15.5.27` (modérée) |
| D2 | Paquet direct ou transitif | ✅ **Vérifié** | **Transitif** — `postcss` n'est pas déclaré |
| D3 | Versions corrigées | ✅ **Vérifié** | `postcss > 8.5.22` → 8.5.29 disponible |
| D4 | Correction sans rupture testée | ✅ **Vérifié** | `overrides` → 0 vulnérabilité, build identique |
| D5 | `npm audit fix --force` lancé | ✅ **Non lancé** | Interdit et évité — proposerait `next@16` (rupture majeure) |
| D6 | Jeton historique dans `~/.git-credentials` | 🟡 **Réserve** | 1 entrée github.com, encore utilisée par `Relio` |
| **Divers** ||||
| X1 | Aucune fonctionnalité élève ajoutée | ✅ **Vérifié** | Aucun commit depuis `569b280` / `0b27b37` |
| X2 | Aucune base de données | ✅ **Vérifié** | Aucune configuration PostgreSQL |
| X3 | Aucune collecte de données d'élève | ✅ **Vérifié** | Aucun stockage, aucun cookie |
| X4 | Dépôt pédagogique intact | ✅ **Vérifié** | SHA-256 des 2 JSON inchangés |

---

## 3. Problèmes détaillés

### R1 — Deux vulnérabilités npm 🔴

| | |
|---|---|
| **Gravité** | 🔴 Élevée (Vercel), **risque réel faible** pour Relio |
| **Paquet** | `postcss` — **transitif**, dépendance de `next@15.5.27` |
| **Version installée** | `8.4.31` — plage vulnérable `<= 8.5.22` |
| **Preuve** | `npm audit` frontend → `2 vulnerabilities (1 moderate, 1 high)` |

**Détail des avis :**

| Avis | Nature |
|---|---|
| XSS via `</style>` non échappé dans la sortie CSS | Sérialisation CSS |
| Lecture arbitraire de fichier via `sourceMappingURL` | Fuite d'information |
| Correction incomplète du précédent | Contournement |
| Traversée de chemin via auto-chargement des source maps | Fuite d'information |

**Impact réel pour Relio — assessment honnête :**

| Facteur | Évaluation |
|---|---|
| `postcss` s'exécute-t-il chez l'élève ? | **Non.** Vérifié : absent des 6 chunks du bundle navigateur |
| Quand s'exécute-t-il ? | À la **construction**, dans le conteneur Vercel |
| Un élève peut-il fournir le CSS ? | **Non.** Le CSS est écrit par nous, dans le dépôt |
| Le CSS contient-il des `sourceMappingURL` ? | **Non** |
| Conclusion | **Aucun vecteur d'exploitation par un élève.** Le risque est théorique |

**Pourquoi le corriger quand même** : c'est une dette de chaîne d'approvisionnement, la
correction est **gratuite et sans rupture**, et Vercel continuera de le signaler.

**Correction proposée (la moins risquée) :** un `overrides` npm qui force
`postcss` en `^8.5.29`, **sans toucher à `next`**.

```json
{
  "overrides": { "postcss": "^8.5.29" }
}
```

**Validée en laboratoire** (copie jetable `/tmp/opencode/fixtest`, dépôts réels
intacts) :

| Contrôle | Avant | Après override |
|---|---|---|
| `npm audit` | 2 vulnérabilités | ✅ **0 vulnérabilité** |
| `next` installé | 15.5.27 | **15.5.27 — inchangé** |
| `postcss` installé | 8.4.31 | **8.5.29 (overridden)** |
| `npx tsc --noEmit` | OK | ✅ OK |
| `npm run build` | OK | ✅ OK — sortie identique (104 kB) |

**À proscrire** : `npm audit fix --force`.installera `next@16.4.0`, une **rupture
majeure** non analysée. Non lancé.

---

### R2 — `API_BASE_URL` figée au build 🔴

| | |
|---|---|
| **Gravité** | 🔴 Moyenne à élevée (opérationnelle) |
| **Preuve** | `\"baseUrl\":\"https://relio-backend-production-a2c3.up.railway.app\"` sérialisé dans le payload RSC du HTML servi |

**Mécanisme.** La page `/` est **prérendue statiquement** (`○ (Static) prerendered
as static content`). `process.env.API_BASE_URL` est donc évalué **au moment du
build**, puis figé dans le HTML. Ce n'est **pas** une lecture au runtime.

**Conséquence concrète.** Modifier `API_BASE_URL` dans le tableau de bord Vercel
**ne change rien** tant qu'un redéploiement n'a pas eu lieu. Pire : lors d'un
basculement d'un backend vers un autre, la prod continuerait de pointer vers
l'ancien service en affichant « Joignable » si l'ancien répond encore.

**Ce n'est pas une faille de sécurité** : une URL d'API n'est pas un secret, et
c'est le comportement voulu du nommage imposé au chantier 2.

**Corrections possibles (au choix) :**

| Option | Effet | Risque |
|---|---|---|
| **A. Documenter** que toute modification exige un redéploiement | Zéro | Aucun |
| B. Passer la page en rendu dynamique (`export const dynamic = 'force-dynamic'`) | Lecture réelle au runtime | Le build devient dynamique, légère perte |
| C. Exposer l'URL via `NEXT_PUBLIC_API_BASE_URL` | Runtime, mais **dans le bundle public** | Inutile ici |

**Recommandation : A**, et B seulement si le basculement d'API devient une
opération courante.

---

### R3 — Aucun test, aucune CI 🔴

| | |
|---|---|
| **Gravité** | 🔴 Élevée |
| **Preuve** | Aucun répertoire de test, aucun fichier `*.test.*` / `*.spec.*`, aucun script `test`, aucun `.github/workflows` |

Le contrôle de santé du backend tient dans un `curl`. Avant d'écrire le moteur de
diagnostic, il faut au minimum :

1. Un test de `buildApp()` via l'API `inject()` de Fastify — **sans ouvrir de
   port**, donc utilisable en CI sans déploiement.
2. Un test de `loadConfig()` : `PORT` invalide, `*` en production, origine malformée.
3. Un test de la fonction CORS : origine exacte, origine inconnue, origine avec
   suffixe piégé.
4. Une CI GitHub Actions exécutant `typecheck` + `build` + `npm audit` dans les
   deux dépôts.

Rappel : le chantier 1 avait identifié ce point (risque R8 « aucune CI »). Il
n'a pas été traité.

---

### R4 — Jeton GitHub historique toujours présent 🟡

| | |
|---|---|
| **Gravité** | 🟡 Moyenne |
| **Preuve** | `/config/.git-credentials` : 1 entrée, `https://<masquee>@github.com` |

**Constat.** L'entrée existe toujours. Elle est **encore utilisée** : le dépôt
`Relio` a `credential.helper = store` et l'accès lecture y fonctionne. Les dépôts
`frontend/` et `backend/` ont le helper **désactivé localement** (conséquence du
403 rencontré au chantier 2).

**Aucun secret n'est reproduit ici.**

**Nettoyage recommandé — sans casser `Relio` :**

1. **Vérifier** ce que ce jeton autorise encore :
   ```bash
   curl -s -H "Authorization: Bearer <JETON_STOCKE>" \
     https://api.github.com/repos/digitalholding2026-ux/Relio | grep permissions
   ```
   *(ne jamais l'envoyer dans un prompt ni un log)*
2. **Révoquer** le jeton si son périmètre est plus large que `Relio`.
3. **Configurer un `GIT_ASKPASS`** avant de supprimer l'entrée, sinon les pushes
   vers `Relio` cesseront de fonctionner :
   ```bash
   git config --global credential.helper ""   # désactiver 'store'
   # puis fournir GIT_ASKPASS qui lit une variable d'environnement
   ```
4. **Supprimer** l'entrée : `git credential reject` pour `github.com`.

⚠️ **L'ordre compte.** Supprimer l'entrée **avant** d'avoir configuré
`GIT_ASKPASS` casse les pushes vers `Relio`.

---

### R5 — Messages d'erreur 4xx divulguant Fastify 🟡

**Preuve :**
```
POST /api/v1  (JSON invalide)
→ 400 {"error":{"code":"BAD_REQUEST",
   "message":"Body is not valid JSON but content-type is set to 'application/json'"}}
```

Le gestionnaire renvoie les messages 4xx de Fastify tels quels. Cela **révèle la
technologie employée** (Fastify), sans information sensible.

**Correction** : dans `src/plugins/error-handler.ts`, remplacer le `error.message`
par un message générique pour les 4xx non explicitement `ApiError`.

---

### R6 — Cibles tactiles légèrement sous la norme mobile 🟢

`.bouton` : `padding: 0.6rem 1rem` + `font-size: 0.9rem` → hauteur ≈ **42 px**.
Les recommandations (WCAG 2.5.5 / Apple HIG).Retournent vers **44 px**.

**Impact réel :** gêne tactile légère, non bloquant. Le rendu mobile réel **n'a
pas été vérifié** (aucun navigateur).

---

### R7 — Points mineurs 🟢

| # | Constat | Preuve |
|---|---|---|
| L1 | `ApiError` est du **code mort** | Jamais appelé dans `src/routes/` |
| L2 | Aucun `requestTimeout` / `connectionTimeout` | Absence dans `src/` — surface *slowloris* ; risque faible sans base de données |
| L3 | `output: 'standalone'` inutile sur Vercel | `next.config.ts` — ignoré par Vercel ; peut égarer |
| L4 | `server: railway-hikari` dans les en-têtes | Divulgation d'infrastructure, niveau plateforme, pas contrôlable ici |
| L5 | Aucune route racine sur le backend | `GET /` → JSON 404 ;_visiter l'URL affiche du JSON brut |

---

## 4. Tests et commandes réellement exécutés

### 4.1 Tests HTTP — environnement de production, non destructifs

Toutes les requêtes sont des `GET`/`OPTIONS`, ou des requêtes de méthode non
supportée **sans effet de bord**. Aucun test de charge, aucun test destructif.

**Backend** — `https://relio-backend-production-a2c3.up.railway.app`

| URL / requête | Résultat |
|---|---|
| `GET /health` | **200** · 138 ms · JSON · `status:ok`, `environment:production`, `uptime:326s` |
| `GET /api/v1` | **200** · 137 ms · `apiVersion:v1`, `status:socle` |
| `GET /route-inexistante` | **404** · `{"error":{"code":"NOT_FOUND",…}}` |
| `GET /` | **404** |
| `POST /health` | **404** (méthode non supportée) |
| `DELETE /api/v1` | **404** |
| `POST /api/v1` corps invalide | **400** · message Fastify divulgué |
| `GET /health?debug=1&env=1` | **200** · paramètres **ignorés**, aucune fuite |

**CORS** (en-tête `Origin`)

| Origine testée | Résultat |
|---|---|
| `https://relio-frontend-one.vercel.app` | ✅ ACAO correct |
| `https://evil.example.com` | ✅ **aucun** ACAO — bloquée |
| `https://relio-frontend-one.vercel.app.evil.com` | ✅ **aucun** ACAO — attaque par suffixe bloquée |
| `https://relio-frontend-one.vercel.app/` | ⚠️ ACAO renvoyé avec barre finale — **artefact de curl** : un navigateur n'envoie jamais d'origine avec barre finale. Non exploitable |
| `OPTIONS /api/v1` (préflight) | ✅ **204** · méthodes `GET, POST, OPTIONS`, `max-age=600`, `Vary: Origin` |

**Frontend** — `https://relio-frontend-one.vercel.app`

| Contrôle | Résultat |
|---|---|
| `GET /` | **200** · 19 024 octets · `text/html` |
| `<html lang>` | `fr` ✅ |
| `<title>` | `Relio — Préparation BEPC Mathématiques` ✅ |
| Viewport mobile | `width=device-width, initial-scale=1` ✅ |
| En-têtes de sécurité | HSTS, `nosniff`, `X-Frame-Options: SAMEORIGIN`, `Referrer-Policy` ✅ |
| `powered-by` | absent ✅ |

**Scan du bundle navigateur** — 6 chunks, 472 Ko :

| Motif | Occurrences |
|---|---|
| `github_pat_`, `ghp_`, `sk-…`, `AKIA…`, clé privée | **0** |
| `NEXT_PUBLIC_*` | **0** |
| `DATABASE_URL`, `IA_PROVIDER_KEY` | **0** |
| `api_key`, `secret`, `OPENAI`, `ANTHROPIC` | **0** |
| `token` / `password` | 1 / 2 — **faux positifs** : `type="password"` de React et la sanitisation d'URL de Next |

### 4.2 Vérifications statiques — dépôts réels, aucune modification

| Dépôt | `npx tsc --noEmit` | `npm run build` | `npm audit` |
|---|---|---|---|
| `relio-backend` | ✅ 0 erreur | ✅ OK | ✅ 0 vulnérabilité |
| `relio-frontend` | ✅ 0 erreur | ✅ OK | 🟡 **2 vulnérabilités** |

### 4.3 Vérifications non effectuées

| Vérification | Raison |
|---|---|
| Affichage mobile réel | Aucun navigateur disponible |
| Flux de connexion exécuté dans un navigateur | L'endpoint répond et l'URL est présente dans le HTML, mais le `fetch` client n'a pas été observé |
| Comportement après hydratation | Idem |
| Logs du backend (B13) | Accès aux logs Railway non disponible |
| Arrêt propre `SIGTERM` (B17) | Nécessiterait un redéploiement |
| Preset Framework et version Node sur Vercel / Railway | Réglages de plateforme, non accessibles |
| Tenue en charge / limitation de débit | Test de charge exclu par le cahier des charges |

---

## 5. Corrections proposées, par priorité

| Prio | Correction | Dépôt | Effort | Risque |
|---|---|---|---|---|
| **P1** | Ajouter `overrides: { "postcss": "^8.5.29" }` | frontend | 1 ligne | **Faible** — validé en laboratoire |
| **P1** | Documenter que `API_BASE_URL` exige un redéploiement | frontend (README) | 1 paragraphe | Aucun |
| **P2** | Ajouter 3 tests `inject()` (routes, config, CORS) + CI GitHub Actions | backend | ~1 h | Aucun |
| **P2** | Remplacer les messages 4xx Fastify par un message générique | backend | ~5 lignes | Faible |
| **P3** | Nettoyer l'entrée `~/.git-credentials` (avec `GIT_ASKPASS` d'abord) | environnement | ~10 min | ⚠️ ** casse les pushes si mal ordonné** |
| **P3** | Supprimer `output: 'standalone'` de `next.config.ts` | frontend | 1 ligne | Aucun |
| **P3** | Utiliser ou retirer `ApiError` | backend | ~5 lignes | Aucun |
| **P4** | Configurer `requestTimeout` / `connectionTimeout` | backend | ~3 lignes | Faible |
| **P4** | Porter les boutons à 44 px de haut | frontend | ~2 lignes | Aucun |
| **P4** | Ajouter une route racine informative sur le backend | backend | ~5 lignes | Aucun |

**Aucune de ces corrections n'a été appliquée.**

---

## 6. Actions manuelles requérant votre intervention

| # | Action | Où | Pourquoi moi je ne peux pas |
|---|---|---|---|
| 1 | **Nettoyer `~/.git-credentials`** | Votre machine / compte GitHub | Nécessite de révoquer un jeton sur votre compte |
| 2 | Vérifier les paramètres Vercel (preset Next.js, Node 22) | Vercel | Aucune permission |
| 3 | Vérifier la version Node sur Railway (≥ 22) | Railway | Aucune permission |
| 4 | Relire les logs de production pour des fuites | Railway | Aucune permission sur les logs |
| 5 | Valider ce rapport avant toute correction | — | Décision |

**Note** : après application de P1, un **redéploiement** du frontend est
nécessaire pour que la correction entre en vigueur.

---

## 7. Confirmation — aucune fonctionnalité élève

| Élément | État |
|---|---|
| Fonctionnalité pédagogique | ❌ **Aucune ajoutée** |
| Diagnostic, exercices, tuteur IA | ❌ **Aucun** |
| Compte, authentification | ❌ **Aucun** |
| Base de données, persistance | ❌ **Aucune** |
| Collecte de données d'élève | ❌ **Aucune** — aucun cookie, aucun stockage local |
| Contenu BEPC dans le frontend | ❌ **Aucun** |
| Modification de l'architecture | ❌ **Aucune** |
| Modification de la production | ❌ **Aucune** |
| Correctif poussé | ❌ **Aucun** — les 3 dépôts sont inchangés |

**État des dépôts au terme de l'audit :**

| Dépôt | HEAD | État |
|---|---|---|
| `Relio` | `08b83fe` | Seul ce rapport ajouté |
| `relio-backend` | `0b27b37` | **Inchangé** |
| `relio-frontend` | `569b280` | **Inchangé** |

**Données pédagogiques** — empreintes identiques au début du chantier :
```
f766f412…  data/referentiel-maths-3e-cm-2025-2026.json
d74a68fb…  data/inventaire-questions-bepc-2025-2026.json
```

---

## 8. Recommandation

**Ne pas ajouter de fonctionnalité élève avant d'avoir levé R1 et R3.**

R1 est trivial et validé. R3 est le vrai sujet : le moteur de diagnostic est de la
logique métier — celle-là même qui sera réécrite après arbitrage pédagogique. Sans
tests ni CI, chaque modification devient une modification à l'aveugle.

Ordre suggéré :

1. **P1** — `overrides` postcss + documentation du redéploiement, puis redéploiement.
2. **P2** — tests `inject()` + CI sur les deux dépôts.
3. Ensuite seulement : trancher les décisions pédagogiques, puis écrire le moteur.

---

*Chantier 1 : `docs/audit-migration-architecture.md`, `docs/architecture-cible.md`,
`docs/plan-migration-depots.md`, `docs/plan-deploiement-vercel-railway.md`,
`docs/rapport-final-chantier-1.md`.*
*Chantier 2 : `docs/rapport-final-chantier-2.md`.*