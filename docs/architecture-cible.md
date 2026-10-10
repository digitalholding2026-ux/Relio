# Architecture cible — `relio-frontend` et `relio-backend`

**Chantier** : 1
**Date** : 2026-10-10
**Statut** : 🔴 **PROPOSITION — rien de tout ceci n'est implémenté**

---

## 1. Point de départ : on crée, on ne sépare pas

L'audit (`docs/audit-migration-architecture.md`) a établi qu'il n'existe **aucun
code applicatif**. Les deux dépôts seront donc **créés à partir de zéro**.

La seule chose à « migrer » est **une donnée** : le référentiel annuel.

```
Relio (existant, préservé)          relio-frontend        relio-backend
──────────────────────────          ──────────────        ──────────────
2 JSON · 4 PDF · 1 JPG              (à créer)             (à créer)
13 docs · 4 scripts                 Next.js               Node + API
                                   ← reçoit : RIEN        ← reçoit : 1 JSON
```

---

## 2. Répartition des responsabilités

### 2.1 `relio-frontend` → Vercel

| Responsabilité | Détail |
|---|---|
| Interface utilisateur | Écrans, navigation, composants |
| Expérience mobile | Conception mobile-first (cible principale : élève sur téléphone) |
| Mini-diagnostic | Affichage des 5 questions, saisie des réponses |
| Affichage des exercices | Consigne, champs de réponse, indices graduels |
| Explications | Paliers d'indices (rappel → méthode → première étape) |
| Progression | Profil de compétences, historique |
| Récompense | Badges, retours d'effort |
| Communication | Client HTTP vers le backend, **et rien d'autre** |

**Ce que le frontend ne fait PAS :**
- ❌ Contenir une donnée pédagogique (voir § 7 — règle de sécurité)
- ❌ Détenir une clé d'API IA, de fournisseur ou de base de données
- ❌ Porter une logique métier (règles de diagnostic, moteur de recommandation)

### 2.2 `relio-backend` → Railway

| Responsabilité | Détail |
|---|---|
| API HTTP | Routes, validation des requêtes |
| Logique métier | Règles d'interprétation du diagnostic |
| Traitement des diagnostics | Calcul des hypothèses, déclenchement des sondes |
| Exercices et résultats | Stockage, restitution, suivi |
| **Moteur de recommandation pédagogique** | Application des règles de `regles-recommandation-pedagogique.md` |
| **Intégration fournisseur IA** | Appel au fournisseur, **clé côté serveur uniquement** |
| Persistance | Profils élèves, progression, réponses |
| Sécurité | CORS, authentification, validation, limitation de débit |

> Le moteur de recommandation est **dans le backend** : c'est une règle métier,
> pas une règle d'affichage. Elle doit être testable et versionnée.

---

## 3. Stack proposée — et pourquoi

> 🔴 **Aucune de ces technologies n'est installée.** Il n'existe aucun
> `package.json`. Ce sont des recommandations, pas un état.

### 3.1 Frontend : **Next.js (App Router) + TypeScript + Tailwind CSS**

| Critère | Évaluation |
|---|---|
| Compatibilité Vercel | ⭐ **Natif, configuration quasi nulle** — détection automatique du framework |
| Prévisualisations | ⭐ Automatiques : chaque PR obtient une URL de prévisualisation, ce qui est précieux pour une revue pédagogique |
| Simplicité de déploiement | ⭐ `vercel` détecte tout ; pas de `output: export` à gérer manuellement |
| Dépendances | ⚠️ Framework lourd (~300 Mo de `node_modules`), plus lent qu'un Vite pur |
| SSR | ⚠️ Inutile ici (application élèves, pas de SEO) — sera désactivé ou rendu dynamique |

**Pourquoi Next.js malgré le poids** : sur Vercel, il est le chemin le moins
frictofriction, et le mécanisme de prévisualisation par Pull Request est un
avantage réel quand les questions pédagogiques doivent être relues avant
publication. L'alternative Vite + React est plus légère mais demande une
configuration manuelle de déploiement.

> **Option alternative documentée :** Vite + React + React Router, déployé en
> statique pur. Choix pertinent si la performance sur réseau mobile prime
> sur la simplicité de déploiement. **Non retenue** pour le MVP.

### 3.2 Backend : **Node.js + TypeScript + Fastify + PostgreSQL**

> ⚠️ **Divergence assumée avec la proposition de mission 1.**
> `docs/integration-backoffice.md` propose **NestJS + Prisma + PostgreSQL**.
> Je propose **Fastify** et j'explique pourquoi — c'est une décision à arbitrer,
> pas un acquis.

| Critère | NestJS (proposé en mission 1) | Fastify (recommandé ici) | Verdict |
|---|---|---|---|
| Poids et boilerplate | Élevé (décorateurs, DI, modules) | **Faible** (plugins, handlers) | ✅ Fastify |
| Arborescence | Convention lourde | **Simple** | ✅ Fastify |
| Dépendances | ~180 | **~15** | ✅ Fastify |
| Compatible Railway | ✅ | ✅ | Égalité |
| Testabilité | Bonne (modules isolés) | Bonne (handlers isolés) | Égalité |
| Structures complexes (systèmes d'équations, moteur de recommandation) | ✅ Excellent out-of-the-box | ⚠️ À structurer soi-même | ✅ NestJS |
| Temps d'écriture par agent IA | ⚠️ Conventions à respecter | ✅ **Plus simple à générer correctement** | ✅ Fastify |
| Continuité avec le document existant | ✅ | ❌ | ⚠️ NestJS |

**Recommandation : Fastify**, pour trois raisons concrètes :
1. Le moteur de recommandation est **de la logique pure** (fonctions sur des
   règles), pas un domaine fortement couplé. Il n'a pas besoin d'un framework
   d'injection de dépendances.
2. Le volume de code backend du MVP est **modeste** : quelques routes, un moteur
   de règles, un accès base. NestJS serait surdimensionné.
3. **Moins de dépendances = moins de surface d'erreur**, ce qui compte quand le
   code sera largement rédigé par des agents.

> 🔴 **Décision requise (D-ARCHI-1).** Si le propriétaire souhaite s'en tenir à
> l'intention de la mission 1, **NestJS est défendable** — il faut simplement
> accepter une arborescence plus lourde. Ce qui est **non négociable** :
> PostgreSQL et TypeScript, justifiés ci-dessous.

### 3.3 TypeScript — pourquoi dans les deux dépôts

Le diagnostic manipule des structures imbriquées (question → objectif → leçon →
signatures d'erreur) et des **distracteurs** qui doivent rester synchronisés avec
la correction. En JavaScript pur, une faute de nom de champ ne serait détectée
qu'à l'exécution, chez un élève. **Le typage est ici une exigence
pédagogique, pas un goût d'ingénieur.**

### 3.4 PostgreSQL — la base est-elle vraiment nécessaire ?

> Le chantier demande de ne pas supposer qu'un backend nécessite une base.

**Analyse des besoins réels :**

| Besoin | Exige de la persistance ? |
|---|---|
| Servir le référentiel annuel | ❌ Non — artefact statique (144 Ko) |
| Servir la progression pédagogique | ✅ **Oui** — elle évolue et doit être à jour |
| Mémoriser les réponses d'un élève | ✅ **Oui** — sinon le profil se perd |
| Mémoriser le profil de compétences | ✅ **Oui** — construit sur plusieurs sessions |
| Évolution de l'historique de maîtrise | ✅ **Oui** |

**Conclusion : la persistance est un besoin réel**, et elle doit survivre au
redémarrage et au changement d'instance.

🚨 **Décisive : Railway a un système de fichiers éphémère.** Un stockage fichier
ou en mémoire perdrait le profil de l'élève à chaque redéploiement. **Une base
gérée est donc justifiée dès le MVP**, et pas seulement plus tard.

**PostgreSQL** est le choix par défaut de Railway, avec sauvegardes gérées, ce
qui limite les opérations manuelles.

### 3.5 Ce qui est Explicitement hors périmètre

| Sujet | Statut |
|---|---|
| Fournisseur d'IA | ⬜ **Aucun choisi.** Aucune clé, aucun appel. Le chantier 1 n'intègre rien. Le point d'insertion est prévu (`IA_SERVICE`) mais reste vide |
| Authentification | ⬜ **Non décidée.** Prévoir au minimum un mode anonyme pour le MVP |
| Base de données gérée | ⬜ À créer par le propriétaire sur Railway |
| Modèle de données Prisma/Drizzle | ⬜ À décider en chantier 2 |

---

## 4. Contrat entre les dépôts

### 4.1 Principe

> **Communication HTTP/REST, contrat écrit en OpenAPI 3.1, versionné dans le
> dépôt backend.**

Le frontend est un **client** du backend. Aucun accès direct à la base.

```
┌──────────────────────┐        HTTPS / JSON        ┌──────────────────────┐
│  relio-frontend      │  ───────────────────────▶  │  relio-backend       │
│  (Vercel, public)    │  ◀───────────────────────  │  (Railway)           │
│                      │                            │                      │
│  - aucun secret      │   CORS : origine frontend   │  - tous les secrets  │
│  - aucune donnée     │   uniquement               │  - toute la logique  │
│    pédagogique       │                            │  - la base           │
└──────────────────────┘                            └──────────────────────┘
                            │
                            ▼
                  ┌──────────────────────┐
                  │  PostgreSQL (Railway)│
                  └──────────────────────┘
```

### 4.2 Configuration de l'URL

| Frontend | Backend |
|---|---|
| `NEXT_PUBLIC_API_URL=https://<domaine-backend>.up.railway.app` | `CORS_ORIGINS=https://<domaine-frontend>.vercel.app` |
| ⚠️ Préfixe `NEXT_PUBLIC_` ⇒ **la valeur est publique dans le bundle**. C'est normal : une URL d'API n'est pas un secret. **Aucun autre secret ne doit jamais utiliser ce préfixe.** | ⚠️ Liste blanche explicite. Jamais `*`. |

> 🔴 **Règle absolue :** une variable d'environnement du frontend ne doit
> contenir **que** `NEXT_PUBLIC_API_URL`. Toute autre variable est un défaut de
> conception.

### 4.3 Variables d'environnement (noms uniquement, aucune valeur)

| Dépôt | Variable | Visible côté client | Rôle |
|---|---|---|---|
| frontend | `NEXT_PUBLIC_API_URL` | ✅ Oui (normal) | URL de base de l'API |
| backend | `PORT` | ❌ Non | Port d'écoute (Railway l'injecte) |
| backend | `DATABASE_URL` | ❌ Non | Connexion PostgreSQL |
| backend | `CORS_ORIGINS` | ❌ Non | Liste blanche d'origines |
| backend | `NODE_ENV` | ❌ Non | `production` |
| backend | `IA_PROVIDER_KEY` | ❌ Non | 🔒 **À créer uniquement le jour où l'IA est branchée. Pas avant.** |
| backend | `AI_SERVICE` | ❌ Non | Fournisseur d'IA — vide tant que non branché |

### 4.4 Contrat API — endpoints envisagés

> ⚠️ **Spécification de conception, non implémentée.** Les formes exactes seront
> fixées en chantier 2.

| Méthode | Route | Usage | Remarque |
|---|---|---|---|
| `GET` | `/health` | Sonde de disponibilité | **Doit rester public** et ne rien divulguer |
| `GET` | `/referentiel/lecons` | Liste des 14 leçons | Données neutres, public |
| `GET` | `/referentiel/lecons/{lecon_id}` | Détail d'une leçon | Données neutres, public |
| `GET` | `/exercices/diagnostic` | Questions de la mini-évaluation | ✅ **Contenu original uniquement** |
| `POST` | `/diagnostics` | Soumission des réponses | Retourne les hypothèses + sondes |
| `GET` | `/profil/{id}` | Profil de compétences | 🔒 **Authentifié** |
| `POST` | `/exercices/{id}/reponses` | Envoi d'une réponse | |
| `GET` | `/exercices/{id}/aide` | Indices graduels | Paliers 1–3 |

🚫 **Route interdite :** aucun endpoint ne doit exposer
`inventaire-questions-bepc-2025-2026.json` ni les PDF du BEPC.

### 4.5 Gestion des erreurs

| Classe | HTTP | Exemple |
|---|---|---|
| Erreur de validation | `400` | Réponse hors barème de réponses acceptées |
| Ressource absente | `404` | `lecon_id` inconnu |
| Non autorisé | `401` / `403` | Profil d'un autre élève |
| Conflit | `409` | Session de diagnostic déjà soumise |
| Erreur métier | `422` | Diagnostic incomplet |
| Panne amont (IA) | `503` | Fournisseur indisponible |
| Interne | `500` | **Jamais** de stack trace renvoyée au client |

**Règle :** toute réponse d'erreur suit le même schéma
`{ code, message, details? }`. Les messages destinés aux élèves sont rédigés en
français ; les détails techniques vont dans les logs serveur, jamais dans la
réponse.

### 4.6 Authentification

**Décision non prise.** Recommandation pour le MVP :

- **Phase 1 — anonyme** : un `pseudonyme` opaque généré côté client, stocké
  localement. Suffisant pour un diagnostic individuel.
- **Phase 2 — comptes** : seulement si le suivi enseignant ou le paiement
  apparaît.

> Cohérence avec la mission 3 : **aucune donnée personnelle** (nom, téléphone,
> e-mail) n'est collectée. Ne pas élargir ce périmètre sans décision explicite.

### 4.7 Partage des types

| Option | Retenue ? |
|---|---|
| Monorepo avec workspace | ❌ Refusée — contredit l'indépendance des 2 dépôts |
| Paquet npm partagé | ❌ Refusée — chaîne de supply-chain disproportionnée |
| **OpenAPI 3.1 + types générés** | ✅ **Retenue** |

**Le contrat OpenAPI est la source unique.** Le backend le publie (`/openapi.json`)
et le frontend en génère ses types. Une CI frontend échoue si le contrat a changé
de façon incompatible.

> **Pas de troisième dépôt.** Le schéma vit dans le dépôt backend, sa source de
> vérité.

### 4.8 Changements incompatibles

| Règle | Mise en œuvre |
|---|---|
| Versionner l'API | Préfixe de version (`/v1/…`) dès le premier jour |
| Ne jamais casser un contrat publié | Changement cassant ⇒ nouvelle version |
| Champs ajoutés | Rétrocompatibles, obligatoires ≠ |
| Champs supprimés ou renommés | Nouvelle version |
| Contrat informatif pour le frontend | Une CI échoue en cas de divergence |

---

## 5. Sécurité

| # | Mesure | Statut |
|---|---|---|
| S1 | **Aucune clé secrète dans le frontend** | À mettre en œuvre — seule `NEXT_PUBLIC_API_URL` |
| S2 | **Aucune clé privée dans Git** | ✅ `.gitignore` couvre `.env`, `*.pem`, `*.key`, `credentials.json`, `.netrc` |
| S3 | **Clés IA uniquement côté backend** | ✅ par conception — jamais dans `NEXT_PUBLIC_*` |
| S4 | **`.env.example` dans chaque dépôt** | ❌ À créer — documents les noms sans valeurs |
| S5 | **CORS en liste blanche** | À mettre en œuvre — jamais `*` |
| S6 | **Aucun contenu BEPC exposé publiquement** | 🔴 Règle critique — voir § 7 |
| S7 | **Fonctionnalités inachevées masquées** | À mettre en œuvre — drapeau `feature flag`, jamais d'endpoint accessible mais incomplet |
| S8 | **Validation de toute entrée côté backend** | À mettre en œuvre — ne jamais faire confiance au client |
| S9 | **Limitation de débit** | À mettre en œuvre sur `/diagnostics` et l'IA |
| S10 | **HTTPS partout** | ✅ Vercel et Railway le font par défaut |

### 5.1 Secret détecté pendant l'audit

| Élément | Valeur |
|---|---|
| Fichier | `.env` (non suivi par Git — ✅) |
| Variable | `GITHUB_TOKEN` |
| Longueur | 93 caractères |
| Utilisé par le code | ❌ Non |
| Présent dans l'historique Git | ❌ Non — vérifié par `git log --all` |

🟠 **Rotation recommandée.** Je ne peux pas révoquer ni régénérer ce jeton (accès
aux paramètres du compte). **La valeur n'est reproduite nulle part.**

---

## 6. Gestion des ressources pédagogiques

### 6.1 Règle centrale

> **Le backend est l'unique source de données à l'exécution.**
> Le frontend ne contient **aucune** donnée pédagogique.

| Donnée | Dépôt de production | Copié vers | Jamais dans |
|---|---|---|---|
| `data/referentiel-*.json` | Relio | **Backend** (seed) | ❌ Frontend |
| `data/inventaire-*.json` | Relio | **Aucun** | ❌ Frontend ❌ Backend |
| 4 PDF BEPC | Relio | **Aucun** | ❌ Partout |
| `source-progression-maths-3e.jpg` | Relio | **Aucun** | ❌ Partout |

### 6.2 Versionnement

Le backend stocke le référentiel avec son **SHA-256** et la version
`2025-2026`. Toute évolution passe par :

```
Relio : modification du générateur
   → régénération du JSON
   → validation (valider-referentiel.mjs)
   → commit dans Relio
   → copie vers le backend
   → vérification d'intégrité en CI backend
```

Le frontend ne connaît que `version` et interroge le backend pour le contenu.

### 6.3 Statut à ne pas perdre

| Donnée | Statut réel |
|---|---|
| Référentiel | `valide_avec_reserves` — 🔴 3 réserves non arbitrées |
| Inventaire BEPC | `analyse_provisoire_en_attente_de_validation_humaine` — 🔴 non validé |
| Objectifs mission 3 | 🔴 non validés par un enseignant |

> **Aucune de ces données ne doit être présentée comme « officielle ».**
> Si l'application les expose, elle doit le faire avec la même réserve que les
> documents d'origine.

---

## 7. 🚨 Règle de sécurité la plus importante

> **Aucun contenu BEPC ne doit transiter vers le client.**

Rappel de l'audit : l'inventaire contient les **énoncés, résultats et barèmes**
transcrits des corrigés officiels. Les droits **ne sont pas établis**.

- Le frontend Vercel est **public par défaut**.
- Un `import` de JSON dans un composant **compile le contenu dans le bundle**,
  public et immuable.
- Le mettre dans `public/` le rend **téléchargeable directement**.

**Conséquences directes :**

1. ❌ L'inventaire ne doit **jamais** être importé par le frontend.
2. ❌ Les PDF ne doivent **jamais** être copiés dans un dépôt public.
3. ❌ L'API ne doit **pas** exposer de route vers l'inventaire.
4. ✅ Seuls du **contenu original** et des **données pédagogiques neutres**
   (intitulés, volumes) peuvent atteindre le client.

**Point d'attention :** le titre « Ce sont des donnéesDerived des sujets officiels »
ne rend pas un contenu libre de droits. Une reformulation ne lève pas la
protection de la source.

---

## 8. Conséquences des choix

| Choix | Effet positif | Effet négatif | Net |
|---|---|---|---|
| Next.js sur Vercel | Déploiement quasi nul, prévisualisations gratuites | Dépendances lourdes, SSR inutile | ✅ Retenu |
| Fastify | ~15 dépendances, code simple à générer | Arborescence à structurer pour les domaines complexes | ✅ Retenu |
| TypeScript | Erreurs de champs détectées avant l'exécution | Compilateur, courbe d'apprentissage | ✅ Retenu |
| PostgreSQL Railway | Persistance garantie, sauvegardes gérées | Base à créer et payer même au MVP | ✅ Retenu (justifié) |
| OpenAPI comme contrat | Pas de troisième dépôt, types synchro | Génération de types à configurer | ✅ Retenu |
| Frontend sans données | Aucun risque de fuite BEPC | 1 appel réseau au démarrage | ✅ Retenu |

---

## 9. Décisions d'architecture requises

| # | Décision | Recommandation | Bloquant ? |
|---|---|---|---|
| **D-ARCHI-1** | Framework backend : Fastify ou NestJS ? | **Fastify**, sauf volonté de continuité avec la mission 1 | Oui (avant d'écrire le backend) |
| **D-ARCHI-2** | Confirmer Next.js ou basculer Vite + React ? | **Next.js** | Non |
| **D-ARCHI-3** | Authentification : anonyme ou comptes dès le MVP ? | **Anonyme** | Non |
| **D-ARCHI-4** | Fournisseur d'IA | **Aucun pour l'instant** — ne rien brancher avant les décisions pédagogiques | Oui pour toute functionality IA |
| **D-ARCHI-5** | Créer la base Railway maintenant ou au premier besoin ? | **Maintenant** — l'app doit persister dès le MVP | Oui |
| **D-ARCHI-6** | Faut-il retirer les PDF du dépôt Relio public ? | **Décision du propriétaire** — voir `rapport-final-chantier-1.md` | Non |

---

*Documents liés : `docs/audit-migration-architecture.md`,
`docs/plan-migration-depots.md`, `docs/plan-deploiement-vercel-railway.md`.*