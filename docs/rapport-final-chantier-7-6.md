# Rapport final — Chantier 7.6 : validation réelle sur Android et préparation du pilote pédagogique

Date : 11 octobre 2026
Rôle : ingénieur QA senior et responsable de fiabilité du produit
Dépôts : `relio-frontend`, `relio-backend`, `Relio` (racine — documentation)

> **Convention de lecture de ce rapport.** Chaque affirmation porte une mention :
> **Vérifié** (preuve obtenue dans cet environnement), **Rapporté** (déclaré par
> un autre intervenant), **À valider** (aucune preuve suffisante),
> **Décision requise** (arbitrage du responsable du projet).
>
> **Aucun test tactile n'a été réalisé.** Aucun téléphone Android, aucun
> émulateur, aucun `adb`, aucun `/dev/kvm` dans l'environnement d'exécution, et
> le règlement du projet interdit de lancer un navigateur local pour reproduire
> le parcours élève. Les tests A1 à A8 sont donc **À valider**, et la procédure
> est fournie au § 4.

---

## 1. Résumé exécutif

Relio est **fonctionnellement cohérent et correctement déployé**, et sa qualité
automatisée est bonne : 267 tests backend, 119 tests frontend, types et builds
verts, **CI GitHub verte sur la totalité des commits des deux dépôts**.

Mais la fiabilité **réellement perçue par un élève sur un téléphone Android n'est
pas établie**. Elle ne peut pas l'être dans cet environnement. C'est la réserve
majeure de ce rapport, et elle n'est pas contournable par un test supplémentaire
côté code.

Sur cette base, **trois défauts reproductibles ont été trouvés, corrigés et
déployés**. Deux d'entre eux ont été introduits par le chantier 7.5 lui-même —
et n'étaient pas détectables par les tests automatisés existants, précisément
parce qu'ils ne se manifeste qu'à l'usage du clavier ou dans le texte réellement
affiché :

| # | Défaut | Effet pour l'élève | Statut |
|---|---|---|---|
| 1 | La touche `=` insérait un caractère **toujours refusé** par la grammaire | Toute réponse terminée par `=` était rejetée avec un message technique | **Corrigé et déployé** |
| 2 | Un symbole inconnu renvoyait « Caractère non reconnu : « , ». » | Message incompréhensible, ne dit pas quoi corriger | **Corrigé et déployé** |
| 3 | La touche décimale étiquetée `,` insérait un `.` | L'élève ne voit pas ce qu'il a tapé | **Corrigé et déployé** |

Le premier est le plus important : le cahier des charges exige la touche `=`, et
le moteur ne l'accepte nulle part. La touche était donc **décorative** — ce que
le cahier des charges du chantier 7.5 interdit explicitement. Le test automatisé
qui aurait dû le révéler n'existait pas.

**Ce que Relio est, aujourd'hui, avec preuve :** un MVP pédagogique cohérent, dont
le tutorat progressif et le suivi local sont vérifiés **au niveau de l'API
déployée**, et dont l'ergonomie tactile reste **non vérifiée**.

---

## 2. État initial examiné

| Dépôt | Commit examiné au départ | État de l'arbre |
|---|---|---|
| `Relio` (racine) | `d66039f` — `docs(chantier-7.5): clavier en rangées et ouverture automatique` | propre |
| `relio-backend` | `d72b14c` — `feat(tutorat): accompagnement pas à pas et suivi des difficultés` | un fichier non suivi : `.tmp/probe.ts` |
| `relio-frontend` | `f6c904a` — `fix(clavier): ouverture automatique et disposition en rangées` | propre |

**Vérifié.** Le fichier `.tmp/probe.ts` était un reste de mon propre sondage de
symboles du chantier 7.5 (un outil de travail jetable), et non un travail en
cours de l'utilisateur. Il a été supprimé et ne fait pas partie du produit. Aucun
travail non commité n'a été écrasé.

Rapports 7.1 à 7.5 lus, en particulier le rapport du chantier 7.5 et ses
réserves déjà formulées (absence de test sur téléphone réel, limite de
persistance locale).

### Déploiements au moment de l'audit

| Service | Constat | Mention |
|---|---|---|
| Railway | `/health` → `ok`, `production`. `/api/v1/suivi` présent → commit `d72b14c` déployé | **Vérifié** |
| Vercel | CSS `clavier__rangee` et chunk de route contenant `Revenir au clavier mathématique` → commit `f6c904a` déployé | **Vérifié** |

Les déploiements correspondaient bien aux derniers commits. Un push n'a pas été
tenu pour un déploiement : les deux ont été constatés séparément.

### CI GitHub

Interrogation de l'API GitHub Actions (aucun `gh` disponible, appel HTTP en
lecture seule ; **aucun jeton n'est reproduit dans ce rapport**).

| Dépôt | Commits | Résultat |
|---|---|---|
| `relio-frontend` | `f6c904a`, `cb24663`, `bfaef2b`, `f6f85f2`, `f7064c1` (5 derniers sur 6) | `success` pour les 5 |
| `relio-backend` | `d72b14c`, `dd17de0`, `728a5fd`, `293d997`, `251f2a3` (5 derniers sur 9) | `success` pour les 5 |

**Vérifié** : aucun workflow en échec. La CI exécute typecheck, tests et build —
elle ne fait **pas** de test d'interface, ce qui explique que les trois défauts
ci-dessus aient pu passer.

---

## 3. Matrice de tests

| Test | Environnement | Résultat | Preuve / réserve |
|---|---|---|---|
| A1–A8 — tastilité Android | téléphone Android | **Non réalisé** | Aucun appareil, aucun `adb`, aucun `/dev/kvm`. **À valider** |
| B1 — scénario tutorat `MVP-B1-E1` | Railway, production | **Conforme** | 3 niveaux distincts observés par HTTP |
| B2 — règle D5 forme non respectée | Railway, production | **Conforme** | `resultat_juste_consigne_non_respectee` + aide progressive |
| B3 — exercice de racines | Railway, production | **Conforme** | `partiellement_correct` + aide progressive |
| B4 — aucune réponse fausse dite juste | Railway, production | **Conforme** | Contrôlé sur 6 saisies |
| B5 — messages compréhensibles | Railway, production | **Défaut trouvé, corrigé** | « Caractère non reconnu : « , ». » |
| C1 — libellés de suivi | source + bundle déployé | **Conforme** | Aucune affirmation de sauvegarde serveur |
| C2 — persistance locale à l'exécution | navigateur | **Non réalisé** | **À valider** (procédure § 7) |
| C3 — effacement de l'historique | navigateur | **Non réalisé** | **À valider** |
| D1 — tests backend | `npm test` | **267 / 267** | **Vérifié** |
| D2 — tests frontend | `npm test` | **119 / 119** | **Vérifié** |
| D3 — typecheck des deux dépôts | `tsc --noEmit` | **OK** | **Vérifié** |
| D4 — builds de production | `tsc --build`, `next build` | **OK** | **Vérifié** |
| D5 — 12 exercices, 36 indices | tests + production | **Conforme** | **Vérifié** |
| D6 — règles D5 | tests + production | **Conforme** | **Vérifié** |
| D7 — blocs fermés protégés | production | **Conforme** | `MVP-B3-E1` → HTTP 403 |
| D8 — 3 niveaux de tutorat | tests + production | **Conforme** | **Vérifié** |
| D9 — insertion/suppression clavier | tests (logique pure) | **Conforme** | 45 tests ; **rendu non vérifié** |
| D10 — réponse attendue absente du client | grep source + bundle déployé | **Conforme** | **Vérifié** |
| D11 — secrets dans le frontend | grep + `securite.test.ts` | **Conforme** | **Vérifié** |
| D12 — workflows CI | API GitHub Actions | **Verte** | **Vérifié** |

---

## 4. Tests Android réels

### Aucun test Android n'a été réalisé. **À valider.**

Inventaire de l'environnement, établi avant toute tentative :

| Moyen | Disponibilité |
|---|---|
| Téléphone Android | **aucun** |
| `adb` | **absent** |
| `emulator` / `avdmanager` | **absents** |
| `/dev/kvm` (émulateur) | **absent** — émulation Android impossible ici |
| Navigateur local | `chromium` présent, mais **interdit** par le règlement du projet pour reproduire le parcours élève |

Le règlement du projet a été respecté : **aucun navigateur n'a été lancé**.
Aucune affirmation de ce rapport ne repose sur un test tactile.

### Procédure de validation à exécuter par le responsable du projet

Adresse : `https://relio-frontend-one.vercel.app/parcours/MVP-B1-E1`
Préalable : un téléphone Android, réseau mobile si possible, portrait.

**A1 — Ouverture et visibilité**
1. Ouvrir la page, toucher le champ « Ta réponse ».
2. Le clavier mathématique doit apparaître **sans aucun bouton à presser**.
3. **Un seul** clavier doit être visible. *C'est le test le plus important : si
   deux claviers s'affichent, `inputMode="none"` n'est pas respecté par ce
   navigateur — le signaler immédiatement.*
4. Le champ de réponse et le bouton « Vérifier » restent visibles.

**A2 — Saisie élémentaire**
5. Composer `3(x+2)`. Vérifier l'insertion des parenthèses et opérateurs, et que
   le curseur reste après chaque touche.

**A3 — Modification au milieu**
6. Placer le curseur au milieu, utiliser `←` et `→`, insérer un caractère.
7. Le texte existant ne doit être ni écrasé ni décalé.

**A4 — Suppression**
8. `⌫` efface le dernier caractère, `C` vide le champ.
9. `⌫` sur un champ vide ne doit rien faire ni planter.

**A5 — Masquage et réouverture**
10. Appuyer sur « Masquer », puis **retoucher le champ** : le clavier doit
    réapparaître.
11. Répéter trois fois de suite : aucun blocage.

**A6 — Clavier système**
12. Appuyer sur « Clavier système » : le clavier du téléphone doit apparaître.
13. Saisir normalement, revenir par « Revenir au clavier mathématique ».
14. Vérifier l'absence de double clavier et que la saisie n'est pas perdue.

**A7 — Touches spécifiques**
15. `MVP-B1-E1` : `x²`, `x³`, `xⁿ`, parenthèses. `√` doit être **absente**.
16. `MVP-B2-E1` : `√` doit être présente et accepter `5√2`.
17. `=` doit **valider** la réponse au lieu d'insérer un caractère.
18. La touche décimale doit afficher le caractère qu'elle insère.
19. **Ne pas** tenter d'exercer un bloc fermé ; noter qu'il s'affiche « bientôt
    disponible ».

**A8 — Ergonomie**
20. En portrait sur écran étroit : taille des touches, espacement, lisibilité,
    défilement, absence de débordement horizontal.

---

## 5. Tutorat — résultats observés

**Vérifié par HTTP sur la production** (le contenu rendu par l'API est établi ;
le **rendu à l'écran reste à valider**).

### `MVP-B1-E1` — réponse attendue `2x + 1`

| Tentative | Verdict | Catégorie | Niveau | Aide observée |
|---|---|---|---|---|
| 1 — `4x + 1` | `incorrect` | `oubli_de_distribuer_un_facteur` | 1 (`signature`) | « As-tu distribué le signe « − » dans chaque terme entre parenthèses ? Que devient un terme précédé du « − » ? » |
| 2 — `4x + 1` | `incorrect` | idem | 2 (`indice`) | « Pour développer, il faut distribuer… 3(x + 2) donne 3x + 6… » |
| 3 — `4x + 1` | `incorrect` | idem | 3 (`indice`) | « A = 3x + 6 − x − 5. Il ne reste plus qu'à regrouper. » |
| 4 — `2x + 1` | `correct` | `null` | bilan | « Tu y es arrivé après 3 essais. Voici la méthode à retenir. » + résumé de méthode |

Conformité aux exigences de la Partie B :

- **Vérifié** — premier niveau : question courte et ciblée, aucune méthode
  complète, aucun exemple résolu.
- **Vérifié** — deuxième niveau : explication intermédiaire.
- **Vérifié** — troisième niveau : travaille sur l'expression de l'élève sans
  révéler `2x + 1`.
- **Vérifié** — les trois niveaux ne répètent pas le même texte.
- **Vérifié** — aucune réponse fausse annoncée comme juste.
- **Vérifié** — D5 préservé sur `MVP-B1-E4` : `resultat_juste_consigne_non_respectee`,
  l'élève est toldexplicitement que son calcul est juste.

### Exercice de racines — `MVP-B2-E1` (bloc 2 ouvert au moment du test)

| Saisie | Verdict | Niveau | Aide |
|---|---|---|---|
| `√(25×2)` | `partiellement_correct` | 1 | « Tu as bien décomposé le nombre sous la racine. Il reste à en extraire le carré parfait. » |
| `√(25×2)` (3ᵉ essai) | `partiellement_correct` | 3 | « Écris 50 sous la forme d'un carré parfait fois un nombre sans facteur carré : 50 = … × …. » |
| `5√2` | `correct` | bilan | bilan de méthode |

**Vérifié** : les trois niveaux progressent, et le niveau 3 travaille sur le
nombre de l'élève (`50`) sans donner `5√2`.

### Point signalé, non corrigé — **Décision requise**

Le libellé D5 du verdict `partiellement_correct` est identique quel que soit le
niveau d'aide, et il est long :

> « Ta réponse est partiellement correcte : tu as bien commencé le travail,
> mais il reste une étape pour le terminer. Continue jusqu'à obtenir une réponse
> qui ne peut plus être simplifiée. »

Sur un écran de téléphone, ce texte long est affiché **en plus** de l'aide
progressive, ce qui contre une partie du but du chantier 7.5. Je ne l'ai pas
modifié : c'est un texte validé par l'enseignant. Deux options, à trancher par le
responsable :

- raccourcir le libellé D5 pour `partiellement_correct` (par exemple : « Tu as
  bien commencé, il reste une étape. ») ;
- ou n'afficher le libellé D5 qu'aux niveaux 1 et 3, l'aide portant le niveau 2.

---

## 6. Suivi local — comportement et limites

### Ce qui est établi par le code et le bundle déployé

- **Vérifié** — le texte affiché est « *N tentatives enregistrées **sur cet
  appareil*** ». L'interface **n'affirme à aucun moment** que les données sont
  sauvegardées sur un serveur ni partagées avec un enseignant.
- **Vérifié** — aucune occurrence de « sauvegarde », « compte », « classe » ou
  « synchronisé » dans le texte destiné à l'élève.
- **Vérifié** — le stockage est `localStorage`, clé `relio.observations.v1`,
  borné à 500 entrées.
- **Vérifié** — un bouton « Effacer mon historique » appelle `effacerJournal()`,
  qui fait un `removeItem` de la clé.
- **Vérifié** — l'API `/api/v1/suivi` renvoie un champ `conservation` qui rappelle
  explicitement que rien n'est conservé côté serveur.
- **Vérifié** — le vocabulaire de suivi ne contient aucun état nommé « maîtrisé ».

### Ce qui reste **À valider** (nécessite un navigateur)

- que le compteur de tentatives **évolue réellement** à l'écran après une
  validation ;
- que le bouton d'effacement vide le compteur ;
- le comportement **après rechargement** de la page ;
- le comportement en navigation privée (stockage refusé).

### Limite à ne pas masquer

Le suivi est **local à l'appareil**. Il disparaît si l'élève vide les données du
navigateur, navigue en privé ou change d'appareil. Il n'est exploitable par aucun
enseignant. Ce n'est **ni un suivi de classe, ni une mesure de maîtrise
durable**. Une réussite après aide indique le nombre d'aides nécessaires, pas ce
que l'élève retiendra.

---

## 7. Défauts détectés et corrigés

### Défaut 1 — la touche `=` était décorative *(gravité : moyenne)*

- **Cause** : le cahier des charges du chantier 7.5 impose une touche `=`, mais
  aucune grammaire du MVP n'accepte `=`. La touche l'insérait donc toujours dans
  une réponse qui était refusée.
- **Preuve** : sur la production, `2x+1=` renvoyait `422` et
  « Caractère non reconnu : « = ». » — pour **tous** les exercices testés.
- **Correction** : `=` **valide la réponse**, comme la touche « Vérifier ». C'est
  le geste de l'élève sur son cahier. Aucun changement de l'analyseur, d'une règle
  D5 ou d'une réponse attendue.
- **Tests ajoutés** : `ne fait pas de « = » une touche décorative` et
  `n'insère jamais le caractère « = »` (frontend).

### Défaut 2 — message technique adressé à l'élève *(gravité : moyenne)*

- **Cause** : le chemin de refus de saisie renvoyait le message brut de
  l'analyseur.
- **Preuve** : `1,5x` → « Caractère non reconnu : « , ». » sur la production.
  C'est le défaut que le chantier 7.4 avait traité pour les messages de signe,
  resté présent sur ce chemin.
- **Correction** : `ExpressionRefusee` porte désormais le symbole en cause, et
  `messagePourErreur` le reformule en consigne. Le symbole — qui vient de la saisie
  de l'élève — est neutralisé avant affichage, pour ne pas permettre d'injecter
  du balisage dans la réponse HTTP. Les messages déjà compréhensibles, comme
  « Expression incomplète. », sont **conservés tels quels**.
- **Tests ajoutés** : 6 tests (message non technique, action donnée, absence de
  fuite technique, neutralisation du balisage).

### Défaut 3 — touche décimale étiquetée `,` insérant un `.` *(gravité : faible)*

- **Cause** : une seule touche pour tous les types de grandeur.
- **Preuve** : l'analyseur rationnel accepte `1,5` comme `1.5`, mais
  l'analyseur d'expressions **refuse** la virgule (`1,5x` est rejeté).
- **Correction** : la touche suit le type de grandeur — `.` sur les expressions et
  racines, `,` sur les exercices fractionnaires.
- **Tests ajoutés** : `n'insère jamais de virgule dans une expression` et
  `insère la virgule sur un exercice fractionnaire`.

### Défaut 4 — faux positif de non-fuite *(gravité : nulle, Hygiène)*

Des tests du frontend utilisaient `2x + 1`, `5√2` et `29/18` comme données
d'exemple : ce sont des **réponses attendues** du MVP. Elles n'étaient que dans
des fichiers de test, jamais dans le bundle, mais elles faisaient lever une alerte
à chaque audit de non-fuite. Remplacées par des valeurs hors périmètre.

**Vérifié après correction** : aucune réponse attendue du MVP ne subsiste dans
`src/`, ni dans le bundle déployé.

### Ce qui n'a **pas** été modifié

- les 12 exercices, les 36 indices et les réponses attendues ;
- les règles D5 et leurs libellés validés ;
- le calendrier scolaire et la protection des blocs ;
- l'absence de compte, de base de données et de collecte serveur ;
- le vocabulaire du suivi.

---

## 8. Non-régression — résultats exacts

| Contrôle | Avant chantier 7.6 | Après |
|---|---|---|
| Backend `npm test` | 261 / 261 | **267 / 267** (+6) |
| Frontend `npm test` | 119 / 119 | **119 / 119** (+3, retraits −3) |
| Backend `npm run typecheck` | OK | **OK** |
| Backend `npm run build` | OK | **OK** |
| Frontend `npm run typecheck` | OK | **OK** |
| Frontend `npm run build` | OK | **OK** — 111 kB premier chargement |

Contrôles de contenu et de protection, tous **Vérifiés** :

- 12 exercices et 36 indices présents, avec leurs trois paliers ;
- les 5 verdicts D5 et les 4 statuts techniques inchangés ;
- `MVP-B3-E1` (bloc 3, semaine 10, semaine courante 5) → **HTTP 403**, aucun
  exercice livré, aucune aide rendue ;
- aucune réponse attendue dans le code client ni dans le bundle déployé ;
- aucun secret dans le frontend ; seule variable lue : `API_BASE_URL`, publique
  par construction.

---

## 9. Git et déploiement

| Dépôt | Commit | Push | Déploiement |
|---|---|---|---|
| `relio-backend` | `e2c2e0e` — `fix(messages): reformuler le refus d'un symbole pour l'élève` | `d72b14c..e2c2e0e` | **Vérifié** — uptime 7 s après le push ; message reformulé observé en production |
| `relio-frontend` | `b4414f5` — `fix(clavier): la touche « = » termine la réponse au lieu d'être rejetée` | `f6c904a..b4414f5` | **Vérifié** — nouveau chunk de route contenant `Terminer et vérifier ma réponse` et `Point décimal` |
| `Relio` | ce rapport | après ce commit | sans effet sur les services |

Le push et le déploiement ont été constatés **séparément**, par observation de
l'uptime côté Railway et du contenu du bundle côté Vercel.

---

## 10. Protocole de pilote pédagogique

> **Le pilote n'a pas eu lieu.** Ce protocole est une préparation. Le responsable
> du projet organise la séance, les autorisations et le consentement des familles.

### Cadre

- **4 à 6 élèves** de 3e, un enseignant présent, 30 minutes.
- Un seul appareil par élève, de préférence **le téléphone personnel** : c'est le
  seul façon d'observer la saisie au doigt dans les conditions réelles.
- Deux exercices du bloc 1 (`MVP-B1-E1` et `MVP-B1-E4`), puis un du bloc 2
  (`MVP-B2-E1`).
- L'enseignant ne doit **pas** aider pendant les 5 premières minutes : on observe
  comment l'élève démarre seul.

### Ce qu'on cherche à observer

1. L'élève **sait-il par où commencer** ?
2. Sait-il **saisir et modifier** sa réponse au doigt ?
3. Comprend-il le **premier retour** de correction ?
4. **Utilise-t-il les indices** pour réfléchir, ou les ignore-t-il ?
5. Où **se bloque-t-il**, et à quel moment **abandonne-t-il** ?
6. La **méthode à retenir** est-elle comprise, ou lue et oubliée ?

### Grille d'observation

Une ligne par élève. Noter **O** (observé) ou **N** (non observé), et une remarque
courte. Ne pas noter de nom : utiliser un simple code (`A1`, `A2`…) dans la
feuille de séance.

| # | Point observé | A1 | A2 | A3 | A4 | A5 | A6 | Remarque courte |
|---|---|---|---|---|---|---|---|---|
| 1 | Tape sur le champ, clavier obtenu sans aide | | | | | | | |
| 2 | Comprend la disposition des touches sans explication | | | | | | | |
| 3 | Compose une expression avec `(` `)` | | | | | | | |
| 4 | **Réussit à corriger au milieu** de sa saisie | | | | | | | |
| 5 | Repère la touche `=` comme « j'ai fini » | | | | | | | |
| 6 | Lit le premier retour et **essaie à nouveau** | | | | | | | |
| 7 | Demande un indice de lui-même | | | | | | | |
| 8 | Lit l'indice et **l'applique** | | | | | | | |
| 9 | Deuxième retour plus compris que le premier | | | | | | | |
| 10 | Sait dire ce qu'il ne comprend pas | | | | | | | |
| 11 | Lit la méthode à retenir avant de passer à la suite | | | | | | | |
| 12 | Fin de l'exercice sans abandon | | | | | | | |

### Questions à poser à l'élève, en fin de séance

Réponses courtes, notées telles quelles :

1. « Montre-moi comment tu as commencé. »
2. « Quand le clavier s'est affiché, qu'est-ce qui t'a paru évident, et qu'est-ce
   qui t'a arrêté ? »
3. « Après avoir lu la première aide, qu'est-ce que tu as fait ensuite ? »
4. « Est-ce que le deuxième message t'a aidé plus que le premier ? »
5. « Si tu n'avais pas eu les aides, aurais-tu réussi ? »
6. « La méthode à retenir, tu pourrais la redire à quelqu'un ? »
7. « Qu'est-ce qui a été le plus pénible ? »
8. « Si tu devais changer une seule chose, ce serait quoi ? »

### Questions à poser à l'enseignant

1. « L'élève a-t-il su nommer ce qu'il cherche à faire ? »
2. « Le retour de l'application a-t-il demandé une reformulation ? »
3. « Un élève a-t-il buté sur une notion mathématique, ou sur l'interface ? »
4. « Le niveau 3 a-t-il été utile, ou trop tard ? »
5. « Le libellé « partiellement correct » est-il trop long sur un téléphone ? »

### Ce que le pilote doit décider — **Décision requise**

Ce protocole est conçu pour produire de quoi trancher quatre questions :

1. **Faut-il raccourcir le libellé D5 `partiellement_correct` ?** (§ 5)
2. **Faut-il accepter une réponse de la forme `A = 2x + 1` ?** Aujourd'hui, un
   élève qui écrit `A = 2x + 1` — ce qu'il fait sur son cahier — est refusé.
   Aucun exercice ne l'accepte. C'est un **friction réel** pour la cible, mais
   cela touche l'analyseur : cela demande une décision, pas un correctif.
3. **Quelle durée de conservation pour l'historique ?** Tant qu'elle n'est pas
   arbitrée, aucun suivi de classe n'est possible.
4. **Le suivi local est-il utile sans persistance durable ?** Le pilote peut le
   dire.

### Données du pilote

Ne relever **ni nom, ni date de naissance, ni coordonnées, ni identifiant
d'appareil**. Utiliser des codes. Ne créer aucun compte. Ne pas photographier les
écrans contenant une liste d'élèves. Le responsable du projet définira les
modalités de consentement.

---

## 11. Réserves restantes

| Réserve | Statut |
|---|---|
| Aucun test tactile sur téléphone Android | **À valider** — aucun appareil, aucun émulateur possible, navigateur local interdit |
| Ergonomie, taille des touches, défilement | **À valider** — procédure A8 fournie |
| Comportement de `inputMode="none"` sur Android | **À valider** — risque de **double clavier** ; test A1.3 |
| Rendu à l'écran du tutorat | **À valider** — le contenu de l'API est vérifié, son affichage non |
| Suivi local à l'exécution (compteur, effacement, rechargement) | **À valider** — établi par lecture du code et du bundle |
| Persistance des données d'élève | **Décision requise** — locale uniquement, aucune durée de conservation arbitrée |
| Suivi de classe, tableau de bord enseignant | **Hors périmètre** — dépend du pilote |
| Libellé D5 `partiellement_correct` trop long | **Décision requise** — texte validé par l'enseignant |
| Réponse de la forme `A = 2x + 1` refusée | **Décision requise** — touche l'analyseur |
| `explication` historique de 7.4 affirmant « Ton calcul est juste » | Signalé au chantier 7.5, toujours non corrigé — **non affiché** par le frontend, mais toujours exposé par l'API |
| CI | **Vérifiée** verte, mais ne couvre aucun test d'interface |

---

## 12. Prochaine recommandation

**Ne pas ouvrir un nouveau chantier.** La suite la plus utile est la
**validation tactile par le responsable du projet**, avec la procédure du § 4, sur
un seul appareil, en quinze minutes. Elle peut révéler un défaut bloquant — le
double clavier — qui rendrait tout le reste secondaire.

Deux points peuvent avancer **en parallèle**, sans développement :

1. **Répondre aux deux questions de l'enseignant** (libellé D5, écriture
   `A = 2x + 1`). Ce sont des arbitrages de contenu, pas de la technique.
2. **Fixer la durée de conservation** des données. C'est la décision qui bloque
   toute évolution du suivi.

Le pilote (§ 10) ne devrait être organisé qu'**après** ces deux points, parce que
sa valeur dépend entièrement de la qualité de l'aide affichée et de ce que l'on
peut conserver des observations.

Je ne lance aucun chantier supplémentaire : la suite vous appartient.

---

## Annexe — reproductibilité

```bash
# Backend
cd /config/Relio/backend && npm test && npm run typecheck && npm run build

# Frontend
cd /config/Relio/frontend && npm test && npm run typecheck && npm run build

# Production
BE="https://relio-backend-production-a2c3.up.railway.app"
FE="https://relio-frontend-one.vercel.app"
curl -s "$BE/health"
curl -s "$BE/api/v1"
curl -s "$BE/api/v1/parcours"
curl -s -X POST "$BE/api/v1/corrections" -H 'Content-Type: application/json' \
  -d '{"exerciceId":"MVP-B1-E1","reponse":"4x + 1","nbEchecs":0}'
curl -s -X POST "$BE/api/v1/suivi" -H 'Content-Type: application/json' \
  -d '{"observations":[]}'
curl -s -o /dev/null -w "%{http_code}\n" "$FE/parcours/MVP-B1-E1"
```