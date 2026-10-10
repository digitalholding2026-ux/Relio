# Plan de déploiement — Vercel (frontend) et Railway (backend)

**Chantier** : 1
**Date** : 2026-10-10
**Statut** : 🔴 **PLAN — aucun déploiement n'a été effectué. Rien n'est déployé.**

---

## 0. Avertissement sur la nature de ce document

> ⚠️ **Aucune application n'existe.** Les tableaux ci-dessous décrivent une
> **configuration prévue**, déduite de la stack recommandée dans
> `docs/architecture-cible.md`.
>
> Les commandes sont celles **attendues une fois le code écrit** — elles
> correspondent aux scripts standard des frameworks proposés. Elles n'ont pas pu
> être testées et **pourront demander des ajustements** une fois les dépendances
> figées.
>
> **Rien ici n'est « vérifié » au sens d'un déploiement réussi.**

---

## 1. Vercel — `relio-frontend`

### 1.1 Configuration prévue

| Paramètre | Valeur prévue | Source |
|---|---|---|
| Dépôt source | `relio-frontend` (GitHub) | Propriétaire doit le créer |
| Répertoire racine | `.` (racine du dépôt) | Standard Next.js |
| Framework | Next.js (détection automatique) | `architecture-cible.md` § 3.1 |
| Commande de build | `npm run build` | ⚠️ **Non vérifiée** — dépend du `package.json` à créer |
| Répertoire de sortie | **Géré automatiquement** par Vercel | Pas de configuration manuelle pour Next.js |
| Node.js | 20 LTS ou supérieur | ⚠️ À fixer dans `package.json` (`engines`) |
| Gestionnaire | npm | Choix à confirmer |

> ⚠️ **Aucune de ces valeurs n'est vérifiée** : elles décrivent le comportement
> attendu de Vercel avec Next.js, pas une configuration testée.

### 1.2 Variables d'environnement

| Variable | Valeur | Visibilité |
|---|---|---|
| `NEXT_PUBLIC_API_URL` | `https://<backend>.up.railway.app` | 🔓 **Publique** — c'est voulu |
| — | **Aucune autre** | — |

> 🔴 **Règle :** `NEXT_PUBLIC_*` est compilé **dans le bundle public**.
> Une seule variable est admise. **Y mettre une clé d'API IA serait une fuite.**

**Fichier `.env.local`** (non commité) :
```
NEXT_PUBLIC_API_URL=https://<backend>.up.railway.app
```

**Fichier `.env.example`** (commité, sans valeur) :
```
NEXT_PUBLIC_API_URL=
```

### 1.3 Stratégie de déploiement

| Élément | Configuration prévue |
|---|---|
| Branche de production | `main` |
| Prévisualisation | Automatique sur chaque Pull Request |
| Domaine | `*.vercel.app` fourni automatiquement |
| Domaine personnalisé | À configurer par le propriétaire |

> 🟢 **Les prévisualisations sont un avantage pédagogique concret** : elles
> permettent de faire relire une modification de questions par un enseignant
> **sans toucher à la production**.

### 1.4 Vérifications après déploiement

| # | Vérification | Attendu |
|---|---|---|
| V-F1 | Le build Vercel est vert | ✅ |
| V-F2 | L'URL `*.vercel.app` répond | HTTP 200 |
| V-F3 | `GET /health` du backend appelé depuis le navigateur | Réponse |
| V-F4 | Le bundle **ne contient aucun secret** | ❌ aucune clé |
| V-F5 | Le bundle **ne contient aucun contenu BEPC** | ❌ aucun énoncé |
| V-F6 | `grep -ri "NEXT_PUBLIC" .next/` | Seule l'URL d'API |
| V-F7 | Affichage correct sur mobile (375 px) | ✅ |

---

## 2. Railway — `relio-backend`

### 2.1 Configuration prévue

| Paramètre | Valeur prévue | Remarque |
|---|---|---|
| Dépôt source | `relio-backend` (GitHub) | — |
| Technologie | Node.js + TypeScript | `architecture-cible.md` § 3.2 |
| Commande de build | `npm run build` | ⚠️ **Non vérifiée** |
| Commande de démarrage | `npm start` | ⚠️ **Non vérifiée** |
| Port | **`$PORT`** fourni par Railway | 🚨 **Ne jamais coder un port en dur** |
| Région | À choisir | Côte d'Ivoire / France / Cameroun selon disponibilité |
| Healthcheck | `GET /health` | À configurer dans Railway |

> 🔴 **Point Railway le plus important :** le port est injecté par la plateforme.
> Une application qui écoute sur `3000` en dur **échouera**. Le code doit lire
> `process.env.PORT`.

### 2.2 Variables d'environnement

| Variable | Valeur | Visible client |
|---|---|---|
| `PORT` | ⚠️ **Fourni par Railway** | ❌ |
| `DATABASE_URL` | Chaîne de connexion PostgreSQL | ❌ |
| `CORS_ORIGINS` | `https://<frontend>.vercel.app` | ❌ |
| `NODE_ENV` | `production` | ❌ |
| `IA_PROVIDER_KEY` | ❌ **À ne pas créer maintenant** | ❌ |
| `IA_SERVICE` | ❌ **Vide tant que l'IA n'est pas branchée** | ❌ |

### 2.3 Persistance et base de données

> Le chantier demande de justifier, pas de supposer. Voici l'analyse.

| Besoin | Persistance requise | Justification |
|---|---|---|
| Servir le référentiel | ❌ Non | Artefact statique, 144 Ko |
| Mémoriser les réponses | ✅ **Oui** | Sans cela le profil est perdu |
| Mémoriser le profil de compétences | ✅ **Oui** | Construit sur plusieurs sessions |
| Historique de maîtrise | ✅ **Oui** | Doit évoluer dans le temps |

🚨 **Décisif :** Railway a un **système de fichiers éphémère**. Un stockage
fichier ou en mémoire perdrait les données à chaque redéploiement. **Une base
gérée est nécessaire dès le MVP.**

> ⚠️ **Point de vigilance commercially :** sur les offres gratuites, Railway
> fournit un PostgreSQL **éphémère**. **Les données d'élèves seraient
> supprimées.** Le propriétaire doit vérifier le mode de persistance
> **avant** toute mise en ligne.

### 2.4 CORS

| Élément | Valeur prévue |
|---|---|
| Méthode | Liste blanche explicite |
| Origines | `https://<frontend>.vercel.app` (+ domaines personnalisés) |
| Méthodes | `GET`, `POST` |
| En-têtes | `Content-Type`, `Authorization` |
| JWT en credentials | ⚠️ **Non en MVP** (auth anonyme) — à activer si comptes |
| **Jamais** | ❌ `Access-Control-Allow-Origin: *` |

**Conséquence à anticiper :** chaque prévisualisation Vercel obtient une URL
différente (`relio-frontend-xyz.vercel.app`). Une liste blanche stricte la
bloquera. **Décision à trancher :** accepter un motif `*.vercel.app` en
développement, ou déclarer les origines explicitement.

### 2.5 Endpoint de santé

| Élément | Valeur |
|---|---|
| Route | `GET /health` |
| Accès | Public (Railway en a besoin pour le healthcheck) |
| Réponse | `{ "status": "ok", "version": "…", "time": "…" }` |
| Interdit | Versions de dépendances, clés, variables d'environnement |

### 2.6 Vérifications après déploiement

| # | Vérification | Attendu |
|---|---|---|
| V-B1 | Les logs de démarrage ne contiennent **aucun secret** | ❌ aucune valeur |
| V-B2 | `GET /health` | HTTP 200 |
| V-B3 | `GET /referentiel/lecons` | **14 leçons** |
| V-B4 | Le SHA-256 du seed en base | `f766f412…` |
| V-B5 | CORS depuis l'origine autorisée | En-tête présent |
| V-B6 | CORS depuis une origine inconnue | **Bloquée** |
| V-B7 | `POST /diagnostics` avec payload valide | Réponse |
| V-B8 | `POST /diagnostics` avec payload invalide | HTTP 400, **pas** de stack trace |
| V-B9 | Un redéploiement conserve les données | ✅ **Critique** |

---

## 3. Variables d'environnement — synthèse

> 🔴 **Aucune valeur sensible n'apparaît dans ce document.**

| Dépôt | Variable | Sensible | À créer par |
|---|---|---|---|
| Frontend | `NEXT_PUBLIC_API_URL` | Non (publique) | Propriétaire sur Vercel |
| Backend | `PORT` | Non | Railway (automatique) |
| Backend | `DATABASE_URL` | ✅ **Oui** | Propriétaire sur Railway |
| Backend | `CORS_ORIGINS` | Non | Propriétaire sur Railway |
| Backend | `NODE_ENV` | Non | Propriétaire sur Railway |
| Backend | `IA_PROVIDER_KEY` | ✅ **Oui** | ⏸️ **Plus tard** |
| Backend | `IA_SERVICE` | Non | ⏸️ **Plus tard** |

---

## 4. Actions manuelles du propriétaire

> **Aucune de ces actions n'a été exécutée.** Je n'ai pas accès à Vercel,
> Railway, ni aux paramètres des comptes.

| # | Action | Où | Objectif | Infos requises | Prérequis | Résultat attendu | Preuve |
|---|---|---|---|---|---|---|---|
| **B1** | Créer `relio-backend` **privé** | GitHub | Dépôt isolé | Nom, visibilité | Compte | Dépôt vide | Page visible |
| **B2** | Créer `relio-frontend` | GitHub | Dépôt isolé | Nom, visibilité | Compte | Dépôt vide | Page visible |
| **B3** | Copier le référentiel + SHA | Local → Git | Donnée de seed | Fichier | B1 | Fichier + `.sha256` | `sha256sum` conforme |
| **B4** | Importer le projet Vercel | Vercel | Lier le dépôt | Repo, framework | B2 | Projet créé | Projet listé |
| **B5** | Définir `NEXT_PUBLIC_API_URL` | Vercel → Settings | Relier au backend | URL Railway | Backend déployé | Build vert | Build réussi |
| **B6** | Créer le service Railway | Railway | Héberger l'API | Repo | B1 | Service actif | Logs de démarrage |
| **B7** | **Créer PostgreSQL** | Railway | Persistance | Nom, région | B6 | Base créée | Panneau base |
| **B8** | ⚠️ **Vérifier la persistance** | Railway | Éviter la perte de données | Offre choisie | B7 | Base **non éphémère** | Type de volume affiché |
| **B9** | Copier `DATABASE_URL` | Railway | Connecter l'API | Chaîne de connexion | B7 | Variable présente | Variable listée |
| **B10** | Définir `CORS_ORIGINS` | Railway | Autoriser le frontend | URL Vercel | B4 | Variable présente | Requête acceptée |
| **B11** | Configurer le healthcheck | Railway | Supervision | `/health` | B6 | Actif | Statut « healthy » |
| **B12** | Définir la branche de production | Vercel + Railway | Déploiement auto | `main` | B4, B6 | Prod activée | URL stable |
| **B13** | Configurer le domaine personnalisé | Vercel | Identité | Domaine | B5 | Domaine actif | HTTPS valide |
| **B14** | Vérifier les droits BEPC | Administration | Lever le blocage | Courrier | — | Réponse écrite | ⚠️ **Non technique** |
| **B15** | Révoquer `GITHUB_TOKEN` | GitHub | Sécurité | — | — | Ancien jeton invalide | Régénération |

---

## 5. Risques de déploiement

| # | Risque | Impact | Parade |
|---|---|---|---|
| D1 | Port codé en dur | 🔴 Service qui ne démarre pas | Lire `process.env.PORT` |
| D2 | PostgreSQL éphémère en offre gratuite | 🔴 **Perte des profils d'élèves** | Vérifier l'offre (B8) |
| D3 | CORS bloquant les prévisualisations Vercel | 🟡 Préviews inutilisables | Motif `*.vercel.app` en dev, à trancher |
| D4 | URL d'API absente au build | 🔴 Build cassé | Variable définie **avant** le premier build |
| D5 | Secret IA dans `NEXT_PUBLIC_*` | 🔴 Fuite publique | Revue de code + grep sur le bundle |
| D6 | Contenu BEPC dans le bundle | 🔴 Problème juridique | Aucun import ; voir `architecture-cible.md` § 7 |
| D7 | Base et API dans des projets Railway différents | 🟡 `DATABASE_URL` non accessible | Même projet Railway, ou réseau privé |
| D8 | Healthcheck qui échoue | 🟡 Redéploiements en boucle | Réponse 200 immédiate, sans dépendance externe |

---

## 6. Ce qui n'a pas été fait

| Action | Statut | Raison |
|---|---|---|
| Créer les dépôts | ❌ Non fait | Hors de mes capacités |
| Configurer Vercel | ❌ Non fait | Hors de mes capacités |
| Configurer Railway | ❌ Non fait | Hors de mes capacités |
| Créer une base de données | ❌ Non fait | Hors de mes capacités |
| Définir des variables d'environnement | ❌ Non fait | Hors de mes capacités |
| Déployer quoi que ce soit | ❌ Non fait | Aucun code n'existe |
| Écrire le `package.json` | ❌ Non fait | Hors périmètre du chantier 1 |

> 🔴 **Aucune preuve de déploiement ne peut être produite à ce stade** — et
> c'est normal : il n'y a ni application, ni dépôt, ni compte configuré.

---

*Documents liés : `docs/audit-migration-architecture.md`,
`docs/architecture-cible.md`, `docs/plan-migration-depots.md`.*