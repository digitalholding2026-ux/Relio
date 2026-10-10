# Rapport final — Chantier 1 : audit technique et préparation de la séparation

**Dépôt** : `https://github.com/digitalholding2026-ux/Relio.git`
**Date** : 2026-10-10
**Statut global** : ✅ **Audit terminé et poussé** · 🔴 **Chantier 2 bloqué en attente de validation**

---

## 1. Résumé exécutif

**Le dépôt Relio ne contient aucun code applicatif.** Ni frontend, ni backend,
ni maquette, ni prototype. Il contient **2 fichiers de données pédagogiques**,
**4 documents sources protégés**, **13 documents d'analyse** et **4 scripts de
traitement sans aucune dépendance**.

**Conséquence majeure :** il n'existe rien à « séparer ». Le chantier 2 ne sera
pas une découpe, ce sera une **création de deux dépôts à partir de zéro**, à
laquelle on transposera **un seul fichier** — le référentiel annuel.

Trois points demandent une attention immédiate :

1. 🔴 **`docs/integration-backoffice.md` affirme que « le backend est NestJS +
   Prisma + PostgreSQL ». C'est faux au sens opérationnel** : il n'y a aucun
   code. C'est une proposition non implémentée, et c'est le principal risque de
   malentendu pour le chantier 2.
2. 🔴 **Les droits sur les sujets et corrigés du BEPC ne sont pas établis.** Ce
   qui contraint l'architecture : aucun contenu BEPC ne doit atteindre le
   frontend, qui est public par défaut sur Vercel.
3. 🟡 **Un jeton `GITHUB_TOKEN` est présent en clair** sur le disque de travail.
   Non commité, non présent dans l'historique — mais une rotation est conseillée.

---

## 2. État initial constaté

| Mesure | Valeur constatée |
|---|---|
| Fichiers suivis par Git | 22 |
| Poids total | 2,8 Mo (dont **2,0 Mo de PDF protégés**) |
| `package.json` | ❌ **Absent** |
| `tsconfig.json` | ❌ **Absent** |
| `index.html` | ❌ **Absent** |
| Dockerfile / `vercel.json` / `railway.json` | ❌ **Absents** |
| Fichiers `.ts` / `.tsx` / `.js` / `.jsx` / `.css` | **0** |
| Fichiers `.prisma` | **0** |
| Répertoires `src/`, `prisma/`, `node_modules/` | **0** |
| Framework de test | ❌ Aucun |
| CI (`.github/`) | ❌ Aucune |
| Gestionnaire de dépendances | **Aucun** |
| Commande de build | 🔴 **Non définie** |
| Commande de démarrage | 🔴 **Non définie** |

---

## 3. Documents produits

| # | Fichier | Contenu |
|---|---|---|
| 1 | `docs/audit-migration-architecture.md` | État réel, inventaire A→J, stack, historique, risques |
| 2 | `docs/architecture-cible.md` | Responsabilités, stack justifiée, contrat API, sécurité |
| 3 | `docs/plan-migration-depots.md` | Destination de chaque fichier, séquence, retour arrière |
| 4 | `docs/plan-deploiement-vercel-railway.md` | Configuration prévue Vercel/Railway, 15 actions manuelles |
| 5 | `docs/rapport-final-chantier-1.md` | Ce rapport |

---

## 4. Observations vérifiées

| # | Observation | Preuve |
|---|---|---|
| O1 | Aucun code applicatif | Recherche exhaustive sur les 22 fichiers suivis |
| O2 | NestJS/Prisma/PostgreSQL n'est qu'une **mention dans un document** | `*.prisma`, `*.ts`, `tsconfig*`, `src/`, `prisma/` → **0 résultat** |
| O3 | 4 scripts sans aucune dépendance externe | Imports : `json`, `os`, `unicodedata` / `node:fs`, `node:url`, `node:path` |
| O4 | `valider-referentiel.mjs` **exécuté**, code de sortie **2** | 3 réserves attendues et documentées |
| O5 | `valider-inventaire-bepc.mjs` **exécuté**, code de sortie **0** | 0 erreur, 0 réserve |
| O6 | `.env` **non suivi** et **absent de l'historique** | `git ls-files`, `git log --all -- .env` → vide |
| O7 | 4 PDF **suivis par Git** (2,0 Mo) | `git ls-files "*.pdf"` → 4 fichiers |
| O8 | Référentiel **inchangé** | SHA-256 `f766f412…` identique avant/après |
| O9 | Somme réelle des volumes horaires = **98 h** | Somme des 14 `volume_horaire_h` |
| O10 | Aucune suppression dans l'historique | `git log --diff-filter=D` → vide |
| O11 | `source-progression-maths-3e.jpg` = renommage de `Document de maths.jpg` | `git log --follow` |
| O12 | Aucune CI | Absence de `.github/` |

---

## 5. Modifications effectuées pendant ce chantier

**Aucune modification pédagogique. Aucun déplacement. Aucune suppression.
Aucune réécriture d'historique.**

| Fichier | Modification | Nature |
|---|---|---|
| `README.md` | `14/14 pages` → `11/11 pages` ; `9 anomalies` → `10` (×2) | Valeurs périmées non propagées en mission 2 |
| `docs/matrice-couverture-competences.md` | `99 h` → `98 h` | 🔴 **Erreur de mission 3 que j'ai détectée et corrigée** |
| `docs/rapport-final-mission-3.md` | `28 h / 99 h` → `28 h / 98 h` ; `28 %` → `29 %` | Idem |
| `docs/specification-diagnostic-initial.md` | `28 h sur 99 h` → `98 h` ; `28 %` → `29 %` | Idem |
| `README.md`, `docs/*` | Ajout des 5 livrables du chantier 1 | Objet du chantier |
| `.gitignore`, `data/*.json` | **Inchangés** | Contraintes respectées |

> **Transparence :** les trois corrections « 99 h → 98 h » sont **une erreur que
> j'ai introduite en mission 3**. Je l'ai trouvée en confrontant mes chiffres
> au référentiel (O9) et je la signale explicitement plutôt que de la corriger
> en silence. Le README disait déjà 98 h : c'est lui qui avait raison.

---

## 6. Opérations NON effectuées

| Opération | Statut | Raison |
|---|---|---|
| Créer `relio-frontend` / `relio-backend` | ❌ **Non fait** | Hors de mes capacités (pas d'accès à la création de dépôts) |
| Configurer Vercel | ❌ **Non fait** | Hors de mes capacités |
| Configurer Railway | ❌ **Non fait** | Hors de mes capacités |
| Créer une base de données | ❌ **Non fait** | Hors de mes capacités |
| Définir des variables d'environnement | ❌ **Non fait** | Hors de mes capacités |
| Modifier les paramètres Git | ❌ **Non fait** | Contrainte du chantier |
| Déployer quoi que ce soit | ❌ **Non fait** | Aucun code n'existe |
| Écrire du code applicatif | ❌ **Non fait** | Contrainte du chantier |
| Révoquer `GITHUB_TOKEN` | ❌ **Non fait** | Nécessite un accès au compte GitHub |
| Supprimer les PDF du dépôt | ❌ **Non fait** | Décision du propriétaire |
| Lancer la migration | ❌ **Non fait** | Contrainte explicite du chantier |

---

## 7. Éléments incertains

| # | Incertitude | Statut |
|---|---|---|
| I1 | Le propriétaire souhaite-t-il vraiment NestJS ? | ❓ Non tranché — document de mission 1 vs recommandation Fastify |
| I2 | Existe-t-il du travail hors de ce dépôt ? | ❓ Non vérifié — seul `main` examiné |
| I3 | Les 3 réserves du référentiel sont-elles arbitrées ? | ❓ Non — le validateur retourne toujours 2 |
| I4 | Le jeton `GITHUB_TOKEN` est-il encore valide ? | ❓ Non vérifié — **et volontairement non testé** |
| I5 | Les 4 documents de mission 3 ont-ils été relus par un enseignant ? | ❓ Non vérifié |
| I6 | Les commandes de build/start proposées | ❓ **Non vérifiées** — aucun `package.json` |
| I7 | L'offre Railway retention des données | ❓ Non vérifiée — **à confirmer avant mise en ligne** |
| I8 | Les droits BEPC | ❓ Non établis — bloque l'usage public |

---

## 8. Risques restants

| # | Risque | Gravité | Responsable |
|---|---|---|---|
| R1 | **Fuite de contenu BEPC via le bundle frontend** | 🔴 Critique | Architecte — respecter la règle du § 7 de l'architecture cible |
| R2 | **Confusion « NestJS implémenté »** | 🔴 Critique | Responsable projet — à dissiper avant d'écrire |
| R3 | Aucun code à migrer → le chantier 2 est une création | 🔴 Critique | Anticipé |
| R4 | PostgreSQL éphémère → perte des profils d'élèves | 🔴 Critique | Propriétaire — vérifier l'offre Railway |
| R5 | Droits BEPC non établis | 🔴 Critique | Propriétaire — démarche administrative |
| R6 | Questions de mission 3 non validées par un enseignant | 🟡 Moyen | Responsable pédagogique |
| R7 | 3 réserves du référentiel non arbitrées | 🟡 Moyen | Responsable pédagogique |
| R8 | `GITHUB_TOKEN` en clair sur le disque | 🟡 Moyen | Propriétaire — rotation |
| R9 | 2,0 Mo de PDF protégés dans un dépôt public | 🟡 Moyen | Propriétaire — décision |
| R10 | Aucune CI, aucun test | 🟡 Moyen | Chantier 2 |

---

## 9. Tableau de statut final

| Élément | Statut | Preuve | Action restante |
|---|---|---|---|
| Examination de la structure du dépôt | `VÉRIFIÉ` | `find` + `git ls-files` — 22 fichiers | — |
| Recherche de code frontend | `VÉRIFIÉ` | 0 fichier `.ts/.tsx/.js/.jsx/.css/.html` | — |
| Recherche de code backend | `VÉRIFIÉ` | 0 `*.prisma`, `*.ts`, `src/`, `prisma/` | — |
| Recherche de configuration | `VÉRIFIÉ` | `package.json`, `tsconfig.json`, Dockerfiles, CI absents | — |
| Historique Git analysé | `VÉRIFIÉ` | 6 commits, aucun fichier supprimé | — |
| Exécution du validateur référentiel | `VÉRIFIÉ` | Code de sortie **2**, 3 réserves | Arbitrage pédagogique |
| Exécution du validateur inventaire | `VÉRIFIÉ` | Code de sortie **0** | — |
| Analyse du `.env` | `VÉRIFIÉ` | Non suivi, absent de l'historique, 1 variable | Rotation (A11) |
| Contrôle d'intégrité du référentiel | `VÉRIFIÉ` | SHA-256 `f766f412…` inchangé | — |
| Correction du volume horaire (99 h → 98 h) | `RÉALISÉ MAIS NON VÉRIFIÉ` | Somme recalculée sur les 14 leçons | Contrôle du responsable pédagogique |
| Inventaire des 22 fichiers | `VÉRIFIÉ` | Destination explicite pour chacun | — |
| Destinations par dépôt définies | `VÉRIFIÉ` | `plan-migration-depots.md` § 2 | — |
| Stack proposée et justifiée | `RÉALISÉ MAIS NON VÉRIFIÉ` | Argumentaire documenté, **aucun code** | Arbitrage D-ARCHI-1 |
| Contrat API spécifié | `RÉALISÉ MAIS NON VÉRIFIÉ` | 9 routes décrites, **non implémentées** | Chantier 2 |
| Configuration Vercel préparée | `RÉALISÉ MAIS NON VÉRIFIÉ` | Valeurs prévues, **non testées** | Actions B4, B5 |
| Configuration Railway préparée | `RÉALISÉ MAIS NON VÉRIFIÉ` | Valeurs prévues, **non testées** | Actions B6 à B11 |
| Procédure de retour arrière | `VÉRIFIÉ` | `Relio` intact, tag proposé | Créer le tag |
| Exécution des scripts de génération | `NON APPLICABLE` | Écrirait les données — non lancé | — |
| Tests automatisés | `NON APPLICABLE` | Aucun code applicatif | Chantier 2 |
| Commit des 5 livrables | `VÉRIFIÉ` | Voir § 10 | — |
| Push vers `origin/main` | `VÉRIFIÉ` | Voir § 10 | — |
| Migration frontend/backend | `À FAIRE` | Non commencée | Après validation |
| Création des deux dépôts | `BLOQUÉ` | Hors de mes capacités | Propriétaire — A1, A2 |
| Configuration Vercel / Railway | `BLOQUÉ` | Hors de mes capacités | Propriétaire — B4 à B11 |
| Écriture du code applicatif | `À FAIRE` | Aucun code | Chantier 2 |
| Droits BEPC | `BLOQUÉ` | Démarche administrative | Propriétaire — B14 |
| Rotation du jeton GitHub | `BLOQUÉ` | Nécessite un accès au compte | Propriétaire — A11 |
| Fonctionnement de l'application | `NON APPLICABLE` | **L'application n'existe pas** | Chantier 2 |

---

## 10. Commit et push

| Élément | Valeur |
|---|---|
| Branche | `main` |
| Commit | *(voir message de fin de session)* |
| Push | `origin/main` |
| Fichiers ajoutés | 5 documents du chantier 1 |
| Fichiers modifiés | 4 documents (`README.md` + 3 de mission 3) |
| Fichiers supprimés | **0** |
| Contenu pédagogique modifié | **0** |

---

## 11. Recommandation pour le chantier 2

### 11.1 Ce qui est prêt

L'audit est **complet et factuel**. Le propriétaire dispose de :
- l'inventaire exact de ce qui existe ;
- une destination explicite pour chacun des 22 fichiers ;
- une architecture cible justifiée ;
- un plan de migration réversible ;
- deux plans de déploiement.

### 11.2 Les 4 décisions à trancher **avant** d'écrire une ligne

| # | Décision | Pourquoi c'est bloquant |
|---|---|---|
| **1** | 🔴 **Droits BEPC** | Détermine si le contenu du jury peut être montré. Détermine l'architecture frontend |
| **2** | 🔴 **Fastify ou NestJS ?** | Détermine toute l'arborescence backend. Recommandé : Fastify, mais l'intention de la mission 1 dit NestJS |
| **3** | 🟡 **Faire relire les 5 questions par un enseignant** | Les corrections sont vérifiées **par calcul**, pas par un didacticien |
| **4** | 🟡 **Contenu de la leçon 6 « Angles inscrits »** | Bloqué : aucun objectif dérivable sans document source. Toute question serait inventée |

### 11.3 Séquence recommandée

```
1. Trancher les 4 décisions ci-dessus
2. Taguer Relio en audit-chantier-1        ← point de retour arrière
3. Révoquer GITHUB_TOKEN                    ← sécurité, indépendant du reste
4. Créer les 2 dépôts (backend en PRIVÉ)
5. Copier le référentiel + SHA-256
6. Railway + PostgreSQL (vérifier la persistance !)
7. Vercel + NEXT_PUBLIC_API_URL
8. Écrire le backend : moteur de diagnostic EN PORT PUR, testable sans base
9. Écrire le frontend
10. Lancer les vérifications V1 à V20
```

### 11.4 Une réserve de méthode

Tout l'**，diagnostic** de la mission 3 repose sur des **objectifs opérationnels
déduits par un analyste**, jamais validés par un enseignant. **Le backend ne
devrait pas encoder ces règles en dur avant la relecture pédagogique** : les
règles de recommandation sont exactement le type de code qu'il faut pouvoir
réécrire après arbitrage.

> C'est la raison pour laquelle je recommande de commencer le backend par le
> **moteur de recommandation en fonctions pures**, testables sans base de
> données ni serveur : c'est la partie qui sera amenée à changer le plus souvent.

---

## 12. Statut du chantier

> ✅ **Les 5 livrables obligatoires sont présents, cohérents entre eux, commités
> et poussés.**
>
> 🔴 **Le chantier est arrêté ici.** Aucune migration n'a été engagée, aucun
> dépôt créé, aucune fonctionnalité ajoutée.
>
> **Le chantier 2 ne commencera qu'après validation explicite du présent
> rapport par le propriétaire du projet.**

---

*Documents liés : `docs/audit-migration-architecture.md`,
`docs/architecture-cible.md`, `docs/plan-migration-depots.md`,
`docs/plan-deploiement-vercel-railway.md`.*