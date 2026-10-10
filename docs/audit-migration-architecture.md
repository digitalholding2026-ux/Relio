# Audit technique — état réel du dépôt et préparation de la séparation

**Chantier** : 1 — Audit technique et préparation de la séparation frontend/backend
**Dépôt audité** : `https://github.com/digitalholding2026-ux/Relio.git`
**Date de l'audit** : 2026-10-10
**Commit audité** : `fc4ce44`
**Statut** : audit factuel — **aucune migration n'a été entreprise**

---

## 1. Conclusion en une ligne

> **Le dépôt ne contient aucun code applicatif.** Ni frontend, ni backend, ni
> maquette. Il contient 2 fichiers de données pédagogiques, 4 documents sources,
> 13 documents d'analyse et 4 scripts de traitement de données sans dépendance.

**Conséquence directe** : la « séparation frontend/backend » ne consiste pas à
répartir du code existant, mais à **créer deux dépôts à partir de zéro** en
n'y transposant que les données de référence. Tout le reste est à écrire.

---

## 2. Réponse aux trois questions fondamentales

| Question | Réponse | Preuve |
|---|---|---|
| **Existe-t-il un frontend ?** | 🔴 **NON.** Zéro fichier. | Aucun `package.json`, `tsconfig.json`, `index.html`, `src/`, `.jsx`, `.tsx`, `.vue`, `.css` dans les 22 fichiers suivis par Git |
| **Existe-t-il un backend ?** | 🔴 **NON.** Zéro fichier. | Aucun `package.json`, fichier de schéma, conteneur, ni code serveur |
| **Existe-t-il une maquette ?** | 🔴 **NON.** | Aucun composant, aucun prototype, aucun storybook. Les documents de spécification sont du texte, pas du code |

### 2.1 Le piège à documenter : NestJS + Prisma + PostgreSQL

`docs/integration-backoffice.md:37` affirme :

> « Le backend du projet est **NestJS + Prisma + PostgreSQL**. »

**Cette affirmation décrit une intention, pas une implémentation.** Le même
document se présente comme « Document de travail — à valider » (ligne 3) et
qualifie son schéma Prisma de « Proposition de modèle » (ligne 38). Il cite
en outre `npx tsx tools/import-referentiel.ts` (ligne 180), **fichier qui
n'existe pas dans le dépôt**.

**Vérification effectuée** : recherche de `*.prisma`, `*.ts`, `tsconfig*.json`,
`nest-cli.json`, `src/`, `prisma/`, `node_modules/` → **0 résultat**.

> ⚠️ **La stack « NestJS + Prisma + PostgreSQL » ne doit pas être traitée comme
> un acquis technique dans le chantier 2.** C'est une décision proposée, jamais
> implémentée, et qu'aucune ligne de code ne valide.

---

## 3. Inventaire quantitatif

| Catégorie | Nombre | Poids |
|---|---|---|
| Fichiers suivis par Git | **22** | 2,8 Mo |
| Documents Markdown (`docs/*.md`) | 13 | 188 Ko |
| Fichiers de données JSON | 2 | 144 Ko |
| Scripts Python | 2 | ~1 000 lignes |
| Scripts Node.js | 2 | ~630 lignes |
| Documents PDF (sujets/corrigés BEPC) | 4 | **2,0 Mo** |
| Image source (progression annuelle) | 1 | 376 Ko |
| **Code applicatif** | **0** | **0 Ko** |

**Répartition du volume : 73 % du dépôt est constitué des 4 PDF du BEPC**,
documents dont les droits de reproduction ne sont pas établis (§ 7).

---

## 4. Classification détaillée (catégories A à J)

Légende — **État réel** : `existe et fonctionne` / `existe, non exécuté` /
`proposition écrite` / `non vérifié`

### A. Code frontend réel

| Chemin | Fonction | Catégorie | État réel | Destination |
|---|---|---|---|---|
| — | — | — | — | — |

🟢 **VIDE. Aucun fichier.** Non pas « peu de code » mais **aucun fichier**.
Vérification : aucun fichier `.ts`, `.tsx`, `.js`, `.jsx`, `.vue`, `.svelte`,
`.css`, `.scss`, `.html` parmi les 22 fichiers suivis.

### B. Code backend réel

| Chemin | Fonction | Catégorie | État réel | Destination |
|---|---|---|---|---|
| — | — | — | — | — |

🟢 **VIDE. Aucun fichier.**
`docs/integration-backoffice.md` (catégorie D) **mentionne** NestJS/Prisma mais ne
contient aucun code exécutable.

### C. Maquettes ou prototypes

| Chemin | Fonction | Catégorie | État réel | Destination |
|---|---|---|---|---|
| — | — | — | — | — |

🟢 **VIDE.** ⚠️ `docs/specification-diagnostic-initial.md` spécifie 5 questions
et 6 sondes **en texte Markdown**, avec énoncés et corrections. **Ce n'est pas
une maquette** : il n'existe aucun écran, aucun composant, aucun rendu. C'est une
spécification rédigée.

### D. Spécifications et documentation

| Chemin | Fonction | Dépendances | État réel | Destination |
|---|---|---|---|---|
| `README.md` | Description du dépôt, procedures de reproduction | — | À jour sauf 3 valeurs (corrigées, § 9) | **Reste** dans Relio |
| `docs/progression-maths-3e-2025-2026.md` | Rendu lisible du référentiel | JSON référentiel | Rédigé | **Reste** dans Relio |
| `docs/rapport-final-mission.md` | Rapport mission 1 | — | Rédigé | **Reste** dans Relio |
| `docs/rapport-controle-donnees.md` | Contrôle mission 1 | JSON référentiel | Rédigé | **Reste** dans Relio |
| `docs/incoherences.md` | Écarts du document source | — | Rédigé | **Reste** dans Relio |
| `docs/integration-backoffice.md` | **Proposition** d'intégration back-office | — | ⚠️ **Proposition, non implémentée** | **Reste** dans Relio |
| `docs/analyse-bepc-2025-2026.md` | Synthèse BEPC | Inventaire | Rédigé | **Reste** dans Relio |
| `docs/couverture-programme-bepc.md` | Couverture 14 leçons | Inventaire | Rédigé | **Reste** dans Relio |
| `docs/anomalies-documents-bepc.md` | 10 anomalies | Inventaire | Rédigé | **Reste** dans Relio |
| `docs/rapport-final-mission-2.md` | Rapport mission 2 | — | Rédigé | **Reste** dans Relio |
| `docs/matrice-couverture-competences.md` | Matrice compétences | Inventaire + référentiel | Rédigé, non validé | **Reste** dans Relio |
| `docs/specification-diagnostic-initial.md` | Spécification mini-diagnostic | Matrice | Spécification, non validée | **Reste** dans Relio |
| `docs/regles-recommandation-pedagogique.md` | Règles d'interprétation | Spécification | Spécification, non validée | **Reste** dans Relio |
| `docs/rapport-final-mission-3.md` | Rapport mission 3 | — | Rédigé | **Reste** dans Relio |
| `README.md` | *(déjà listé)* | | | |

**Note importante :** les 4 documents de mission 3
(`matrice`, `specification`, `regles`, `rapport-final-mission-3`) sont
**explicitement non validés** par un enseignant. Ils ne sont pas des
spécifications opposables.

### E. Données et ressources pédagogiques

| Chemin | Fonction | Dépendances | État réel | Destination |
|---|---|---|---|---|
| `data/referentiel-maths-3e-cm-2025-2026.json` | Référentiel annuel, 14 leçons, 120 h | Généré par `generer-referentiel.py` | ✅ Existant, `valide_avec_reserves` | **Copie → backend** (donnée de seed) |
| `data/inventaire-questions-bepc-2025-2026.json` | 35 questions BEPC + corrigés | Généré par `generer-inventaire-bepc.py` | ⚠️ `analyse_provisoire_en_attente_de_validation_humaine` | **Reste dans Relio** — voir § 7 |
| `BEPC 04 juin 2025.pdf` | Sujet officiel 2025 (244 Ko) | — | ✅ Présent | **Reste dans Relio** — droits |
| `BEPC 2026.pdf` | Sujet officiel 2026 (320 Ko) | — | ✅ Présent | **Reste dans Relio** — droits |
| `BEPC-MATHS-CORRIGE-2025.pdf` | Corrigé harmonisé 2025 (708 Ko) | — | ✅ Présent | **Reste dans Relio** — droits |
| `bepc 2026 corriger.pdf` | Corrigé harmonisé 2026 (704 Ko) | — | ✅ Présent | **Reste dans Relio** — droits |
| `source-progression-maths-3e.jpg` | Document source de la progression | — | ✅ Présent | **Reste dans Relio** (traçabilité) |

### F. Scripts et outils

| Chemin | Fonction | Dépendances | État réel | Destination |
|---|---|---|---|---|
| `outils/generer-referentiel.py` | Génère le JSON référentiel depuis la transcription | **Stdlib Python** (`json`, `os`, `unicodedata`) — zéro paquet externe | ✅ Exécutable | **Reste dans Relio** (voir § 8.3) |
| `outils/generer-inventaire-bepc.py` | Génère l'inventaire BEPC | **Stdlib Python** (`json`, `os`) — zéro paquet externe | ✅ Exécutable | **Reste dans Relio** |
| `outils/valider-referentiel.mjs` | Contrôle cohérence référentiel | **Node builtins** (`node:fs`, `node:url`, `node:path`) — zéro paquet | ✅ **Exécuté, code de sortie 2** | **Reste dans Relio** |
| `outils/valider-inventaire-bepc.mjs` | Contrôles qualité inventaire | **Node builtins** — zéro paquet | ✅ **Exécuté, code de sortie 0** | **Reste dans Relio** |

> **Constat remarquable :** ces 4 scripts n'utilisent **aucune dépendance
> externe**. Ni `package.json`, ni `requirements.txt`, ni installation. Ils sont
> exécutables tels quels sur n'importe quel environnement Python 3 / Node 18+.
> C'est un atout majeur pour la CI et pour le developpement par agents.

### G. Configuration et dépendances

| Chemin | Fonction | État réel |
|---|---|---|
| `.gitignore` | Ignore `.env`, `node_modules/`, `__pycache__/`, `dist/`… | ✅ Correct et actif |
| `package.json` | — | ❌ **Absent** |
| `package-lock.json` / `pnpm-lock.yaml` / `yarn.lock` | — | ❌ **Absents** |
| `tsconfig.json` | — | ❌ **Absent** |
| `next.config.js`, `vite.config.ts`, `index.html` | — | ❌ **Absents** |
| `vercel.json`, `railway.json`, `Dockerfile`, `docker-compose.yml` | — | ❌ **Absents** |
| `requirements.txt`, `pyproject.toml` | — | ❌ **Absents** |
| `.github/` (CI) | — | ❌ **Absent — aucune CI** |
| `.env.example` | — | ❌ **Absent** (recommandé, § 7) |

**Gestionnaire de dépendances : AUCUN.** Aucun gestionnaire n'est installé ni
utilisé, car il n'y a aucune dépendance à gérer.

### H. Tests existants

| Élément | Constat |
|---|---|
| Framework de test | ❌ **Aucun** (pas de Jest, Vitest, Playwright, pytest) |
| Fichiers de test | ❌ **Aucun** (aucun `*.test.*`, `*.spec.*`, `test_*.py`, `tests/`) |
| Couverture | ❌ Non mesurable |
| CI | ❌ **Aucune** (pas de `.github/workflows`) |

⚠️ **Nuance importante :** les 2 fichiers `valider-*.mjs` **ne sont pas des
tests**. Ce sont des **contrôles d'intégrité de données** : ils relisent un JSON
et vérifient sa cohérence interne (barèmes, clés étrangères, unicité). Ils ne
testent **aucune ligne de code applicatif** — il n'y en a pas.

Ils constituent néanmoins un **point d'entrée CI naturel** pour le dépôt
backend, puisqu'ils fonctionnent déjà sans aucune installation.

### I. Fichiers générés, temporaires ou potentiellement obsolètes

| Chemin | Nature | Suivi par Git | Destination |
|---|---|---|---|
| `outils/__pycache__/generer-inventaire-bepc.cpython-314.pyc` | Cache Python 3.14 | ❌ Non (ignoré par `.gitignore`) | Supprimer localement, **ne pas transférer** |
| — | Aucun autre artefact de build | — | — |

**Aucun dossier `node_modules/`, `dist/`, `build/`, `.next/`** : rien à nettoyer.

### J. Secrets potentiels et configurations sensibles

| Élément | Constat | Risque |
|---|---|---|
| `.env` | **Présent sur le disque**, 436 octets, permissions `600` | 🟡 Voir ci-dessous |
| `.env` suivi par Git | ❌ **NON suivi** | ✅ Correct |
| `.env` dans un commit | ❌ **AUCUN** (`git log --all -- .env` → vide) | ✅ Correct |
| `.env.example` | ❌ Absent | 🟡 À créer pour documenter les noms de variables |

**Contenu de `.env`** (structure seule, **aucune valeur reproduite**) :
8 lignes de commentaire + **1 variable : `GITHUB_TOKEN`** (93 caractères).

| Point | Conclusion |
|---|---|
| Utilisé par le code du dépôt ? | ❌ **Non** — `GITHUB_TOKEN` n'est référencé par aucun script |
| Rôle probable | Authentification des opérations Git |
| Exposure | Faible en dépôt, **mais le secret est présent en clair sur le disque de travail** |

🟠 **Recommandation : rotation conseillée.** Un jeton d'accès GitHub en clair
dans un répertoire de travail peut avoir été exposé par une sauvegarde, un
historique de shell ou un journal. **La valeur n'est pas reproduite dans ce
document.** Le propriétaire devrait :
1. révoquer le jeton actuel sur GitHub ;
2. en générer un nouveau ;
3. vérifier qu'il n'apparaît dans aucun historique Git — **vérifié : il n'y
   apparaît pas**.

> ⚠️ **Je n'ai ni révoqué, ni régénéré, ni modifié ce jeton** : cela.sort du
> périmètre de mes capacités (accès aux paramètres du compte).

---

## 5. Stack technique réellement détectée

| Élément | Information |
|---|---|
| **Application frontend** | 🔴 **N'existe pas** |
| **Application backend** | 🔴 **N'existe pas** |
| **Langage** | Python 3 (scripts de données) · Node.js 18+ (validateurs) · aucun langage applicatif |
| **Framework** | 🟡 **Aucun détecté.** « NestJS » n'est qu'une mention dans un document |
| **Gestionnaire de dépendances** | 🟡 **Aucun** — aucun `package.json`, aucun manifeste |
| **Point d'entrée** | 🟡 `outils/generer-referentiel.py`, `outils/generer-inventaire-bepc.py` (scripts ponctuels, pas des serveurs) |
| **Commande de construction** | 🔴 **Non définie** — aucun manifeste, donc aucune commande de build n'existe |
| **Commande de démarrage** | 🔴 **Non définie** — aucun serveur ne démarre |
| **Dépendances importantes** | 🔴 **Aucune** (scripts stdlib uniquement) |
| **État de fonctionnement** | 🟡 Scripts vérifiés **exécutés avec succès** ; aucune application à faire fonctionner |
| **Hébergement envisagé** | 🟡 Vercel / Railway : **mentionnés nulle part** dans le dépôt — ce sont des objectifs du chantier, pas un existant |

### 5.1 Vérifications exécutées

| Commande | Résultat |
|---|---|
| `find` sur 22 fichiers suivis | Aucun fichier applicatif |
| Recherche `*.prisma`, `*.ts`, `tsconfig*`, `nest-cli.json`, `src/`, `prisma/`, `node_modules/` | **0 résultat** |
| `node outils/valider-referentiel.mjs` | **Code de sortie 2** — 3 réserves attendues (documentées, non bloquantes) |
| `node outils/valider-inventaire-bepc.mjs` | **Code de sortie 0** — 0 erreur, 0 réserve |
| `git log --diff-filter=D` | Aucune suppression de fichier dans l'historique |
| `git log --all -- .env` | **Aucun** commit contenant `.env` |
| Contrôle SHA-256 du référentiel | `f766f412…` — **inchangé depuis la mission 2** |

---

## 6. Historique Git et dépendances entre fichiers

6 commits, tous sur `main`, auteur unique, tous datés du 2026-10-10.

| Commit | Nature | Fichiers |
|---|---|---|
| `54b200b` | `Add files via upload` (interface web GitHub) | `Document de maths.jpg` |
| `7760f44` | `feat(referentiel)` — mission 1 | `.gitignore`, `README.md`, JSON référentiel, 4 docs, 2 scripts Python/Node |
| `0f5e1fe` | `docs:` — rapport mission 1 | `README.md`, `docs/rapport-final-mission.md` |
| `90121f7` | `Add files via upload` | **Les 4 PDF du BEPC** |
| `4394ce0` | `docs(bepc)` — mission 2 | `README.md`, JSON inventaire, 4 docs, 2 scripts |
| `fc4ce44` | `docs(bepc)` — corrections mission 2 | 3 docs |

**Graphe de dépendances réelles :**

```
source-progression-maths-3e.jpg
        └──▶ outils/generer-referentiel.py
                  └──▶ data/referentiel-*.json   ◀── figé
                                │
                                ├──▶ outils/valider-referentiel.mjs
                                │
                                └──▶ outils/generer-inventaire-bepc.py
                                            │ (lit le référentiel)
                                            ▼
4 PDF BEPC ───────────────────────▶ data/inventaire-*.json ◀── figé
                                            │
                                            └──▶ outils/valider-inventaire-bepc.mjs
```

**Contrôle de non-régression :** l'inventaire **lit** le référentiel mais ne le
**modifie** jamais (contrainte vérifiée en mission 2, `git diff` vide).
Les 2 JSON sont des **artefacts figés**, régénérables mais versionnés.

**Une incohérence détectée :** les 4 PDF (`90121f7`) ont été ajoutés **après**
les scripts de génération, alors que `generer-inventaire-bepc.py` en dépend
logiquement. L'ordre des commits ne reflète pas la chaîne de production — sans
conséquence pratique, mais à connaître.

---

## 7. Risque juridique — droits sur les documents BEPC 🔴

**C'est le risque le plus élevé du chantier, et il conditionne l'architecture.**

| Point | Constat |
|---|---|
| Nature | Sujets et corrigés harmonisés publiés par la Direction des Examens, des Concours et de la Certification du Cameroun |
| Droits | 🔴 **NON ÉTABLIS** — anomalie D-1 de la mission 2, jamais levée |
| Conséquence 1 | Les énoncés **ne peuvent pas être affichés aux élèves** |
| Conséquence 2 | Les figures **ne peuvent pas être reproduites** |
| Conséquence 3 | ⚠️ **Les données dérivées ne doivent pas non plus atteindre le frontend** |

### 7.1 Le piège architectural à éviter

`data/inventaire-questions-bepc-2025-2026.json` contient les **énoncés, les
résultats et les barèmes** transcrits des corrigés officiels.

> 🚨 **Si ce fichier est embarqué dans le bundle frontend, il constitue une
> republication de contenu protégé** — exactement ce que la mission 2 a interdit.
> Le `frontend` sur Vercel est **public par défaut**. Le placer dans
> `public/`, l'importer dans un composant, ou le `fetch`er sans authentification
> exposerait le contenu.

**Règle d'architecture impérative :**

> **Aucun contenu BEPC ne transite vers le client.** Le frontend ne reçoit que
> du contenu original ou du contenu pedagogique neutre (intitulés de leçons,
> volumes horaires). Le backend ne sert les données BEPC qu'à un public
> autorisé, ou ne les sert pas du tout tant que les droits ne sont pas établis.

### 7.2 Les PDF sont dans le dépôt public

Les 4 PDF (2,0 Mo) sont **suivis par Git** et pushés sur GitHub. Ils sont donc
potentiellement consultables publiquement. **Les retirer est une décision du
propriétaire** — je ne supprime rien et ne réécris pas l'historique.

---

## 8. Stratégie de partage des données pédagogiques

### 8.1 Contraintes

- Ne pas dupliquer inutilement les données pédagogiques entre les deux dépôts.
- Ne pas créer un troisième dépôt de code partagé sans justification.
- Le référentiel (`98 h` de leçons, 3 trimestres, 30 semaines) est **lu** par
  l'application.
- L'inventaire BEPC ne doit **pas** atteindre le frontend.

### 8.2 Options comparées

| Option | Avantages | Inconvénients | Verdict |
|---|---|---|---|
| **A. Le backend sert les données** (recommandée) | Source unique à l'exécution ; rien ne se duplique ; contrôle d'accès centralisé ; cohérent avec l'architecture 2 dépôts | Le backend doit embarquer les données (léger : 144 Ko) | ✅ **Retenue** |
| **B. Copier le JSON dans chaque dépôt** | Autonomie ; pas d'appel réseau | Duplication ; divergence progressive ; 🚨 **risque de fuite BEPC dans le bundle frontend** | ❌ Rejetée |
| **C. Paquet npm partagé** | Types partagés, versionnés | Vecteur de supply-chain ; publication à gérer ; complexité disproportionate | ❌ Rejetée pour le MVP |
| **D. Troisième dépôt de données** | Séparation nette | Déploiement, versions, CI supplémentaires pour 144 Ko | ❌ Rejetée |

### 8.3 Décision recommandée

> **Le dépôt `Relio` reste la source de production et d'audit.**
> Le **backend** reçoit une **copie en lecture seule** du référentiel, comme
> donnée de seed versionnée. Le **frontend ne contient aucune donnée
> pédagogique** : il les requête via l'API.

Les 4 scripts restent dans `Relio` car ils forment la chaîne de production
documentée. Le backend n'en a pas besoin à l'exécution.

> **Option alternative documentée :** déplacer `outils/` vers le backend pour que
> sa CI valide le seed. **Non recommandé** — cela duplique les scripts et
> scatterait la chaîne de production. Préféré : le backend stocke le SHA-256 du
> JSON de seed et la CI vérifie l'intégrité.

---

## 9. Modifications effectuées pendant cet audit

**Aucune modification pédagogique n'a été faite.** Les 2 fichiers JSON sont
intacts (SHA-256 identiques au début et à la fin de l'audit).

| Fichier | Modification | Justification |
|---|---|---|
| `README.md` | `14/14 pages` → `11/11 pages` | Valeur périmée : la correction de mission 2 n'avait pas propagé au README |
| `README.md` | `9 anomalies` → `10 anomalies` (× 2) | Idem |
| `docs/matrice-couverture-competences.md` | `99 h` → `98 h` | 🔴 **Erreur de la mission 3 que j'ai corrigée** — la somme réelle des `volume_horaire_h` est 98 h |
| `docs/rapport-final-mission-3.md` | `28 h / 99 h` → `28 h / 98 h`, `28 %` → `29 %` | Idem |
| `docs/specification-diagnostic-initial.md` | `28 h sur 99 h` → `28 h sur 98 h`, `28 %` → `29 %` | Idem |

> **Les trois dernières lignes sont une erreur que j'ai introduite en mission 3**
> et que j'ai détectée lors de cet audit en confrontant mes chiffres au
> référentiel. Je le signale explicitement plutôt que de la corriger en silence.

**Aucune suppression. Aucun déplacement. Aucune réécriture d'historique.**

---

## 10. Synthèse des risques

| # | Risque | Gravité | Statut |
|---|---|---|---|
| R1 | **Droits BEPC non établis** — contenu protégé à ne pas exposer publiquement | 🔴 Critique | Ouvert — bloque l'architecture frontend |
| R2 | **Confusion NestJS implémenté / proposé** — risque de croire le backend existant | 🔴 Critique | Documenté, dissipé (§ 2.1) |
| R3 | Aucune base de code à migrer — le chantier 2 est une **création**, pas une découpe | 🔴 Critique | Documenté |
| R4 | `GITHUB_TOKEN` en clair sur le disque | 🟡 Moyen | Rotation recommandée |
| R5 | Référentiel `valide_avec_reserves` — 3 réserves non arbitrées | 🟡 Moyen | Ouvert (mission 1, arbitre : responsable pédagogique) |
| R6 | Inventaire BEPC provisoire, non validé humainement | 🟡 Moyen | Ouvert |
| R7 | Objectifs opérationnels de mission 3 non validés par un enseignant | 🟡 Moyen | Ouvert |
| R8 | Aucun test, aucune CI | 🟡 Moyen | À traiter en chantier 2 |
| R9 | 2,0 Mo de PDF protégés dans un dépôt public | 🟡 Moyen | Décision du propriétaire |
| R10 | Aucune donnée pédagogique dans le frontend → lenteur au démarrage | 🟢 Faible | Acceptable (144 Ko) |

---

## 11. Points non vérifiés

| Point | Statut |
|---|---|
| Le propriétaire souhaite-t-il réellement NestJS ? | ❓ **Non vérifié** — document de mission 1, jamais arbitré |
| Existe-t-il du travail hors de ce dépôt (Figma, autre branche, autre machine) ? | ❓ **Non vérifié** — seul `main` a été examiné ; aucune branche distante supplémentaire |
| Les 3 réserves du référentiel ont-elles été arbitrées depuis ? | ❓ **Non vérifié** — le validateur retourne toujours le code 2 |
| Le token `GITHUB_TOKEN` est-il encore valide ? | ❓ **Non vérifié** — et volontairement non testé |
| Les 4 documents de mission 3 ont-ils été relus par un enseignant ? | ❓ **Non vérifié** |
|Existe-t-il des fils Git / commits non poussés ? | ✅ Vérifié : working tree propre avant modification |

---

## 12. Ce qu'il faut retenir pour le chantier 2

1. **Il n'y a rien à « séparer »** : tout reste à créer.
2. **Le dépôt Relio reste intact** comme référence pédagogique et documentaire.
3. **Une seule donnée franchit la frontière** : le référentiel, vers le backend.
4. **Les PDF et l'inventaire BEPC ne franchissent pas la frontière** (droits).
5. **Le frontend ne contient aucune donnée pédagogique** — règle de sécurité.
6. **Rien n'a été décidé sur la stack applicative** : NestJS est une proposition.

---

*Documents liés : `docs/architecture-cible.md`,
`docs/plan-migration-depots.md`, `docs/plan-deploiement-vercel-railway.md`,
`docs/rapport-final-chantier-1.md`.*