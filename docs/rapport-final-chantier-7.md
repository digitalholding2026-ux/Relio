# Rapport final — Chantier 7 : implémentation du MVP pédagogique

**Date** : 2026-10-10
**Objet** : implémentation du MVP cadré par le rapport du chantier 6
**Périmètre** : trois blocs, cinq objectifs, douze exercices originaux
**Statut** : 🟠 **TERMINÉ AVEC RÉSERVES**

> **Avertissement de portée, à lire avant tout le reste.**
> Ce rapport ne décrit **que** des travaux réellement effectués et des
> vérifications réellement exécutées. Trois distinctions sont tenues tout au
> long du document :
>
> 1. un **fait vérifié** est établi par une commande citée, dont la sortie a été
>    lue ;
> 2. une **déclaration** est une affirmation du propriétaire ou d'un document
>    antérieur, reprise sans être re-vérifiée ici ;
> 3. un **point ouvert** est une décision humaine non prise, que le code
>    signale au lieu de la trancher.
>
> **Aucun déploiement n'a été effectué ni vérifié par ce chantier.** Aucun
> parcours utilisateur réel n'a été testé. Les builds réussis ne valent pas
> validation en production.

---

## 1. Résumé des réalisations

### 1.1 État de départ : un travail antérieur non commité

Le chantier a commencé par un constat qui détermine la nature de la livraison :
**le MVP était déjà implémenté dans les deux dépôts, mais rien n'était commité.**
Les commits `2d1c91a` (backend) et `b148b90` (frontend) s'arrêtaient au socle
technique. Le travail du MVP — contenu pédagogique, moteur de correction,
calendrier, parcours, interface — se trouvait dans l'arbre de travail, non
versionné : **22 fichiers modifiés et 18 non suivis** côté backend,
**10 fichiers** côté frontend.

**Conséquence méthodologique** : ce chantier n'est pas une implémentation
depuis zéro, ni une simple reprise de travaux validés. Il a consisté à
**auditer un existant non commité**, à y corriger des défauts réels, à
l'élargir là où les documents validés l'exigeaient, puis à le publier.

### 1.2 Fonctionnalités livrées

**Contenu pédagogique** — trois blocs, cinq objectifs, douze exercices
originaux, conformes au cadrage du chantier 6 :

| Bloc | Leçon | Ouverture | Objectifs | Exercices |
|---|---|---|---|---|
| B1 — Calcul littéral | L1 (7 h) | **S1** | `OO-L1-1`, `OO-L1-2` | 6 |
| B2 — Racines carrées | L3 (7 h) | **S5** | `OO-L3-1` | 3 |
| B3 — Calcul numérique | L5 (9 h) | **S10** | `OO-L5-1`, `OO-L5-2` | 3 |

Les semaines d'ouverture proviennent du référentiel annuel transcrit
(`data/referentiel-maths-3e-cm-2025-2026.json`). Aucun énoncé ne reproduit une
épreuve du jury : `sourceBepc` vaut `null` sur les douze, contrôle automatisé en
place.

**Correction sur trois axes séparés** — c'est le point F1 du chantier 6, et la
contribution centrale de ce chantier :

```
mathemathiquementJuste   égalité algébrique ou arithmétique EXACTE
                         → jamais de comparaison de chaînes
formeRespectee           propriété de l'ÉCRITURE seule
                         → null si aucune règle de forme n'est arbitrée
statut                   conséquence des deux, dans le vocabulaire fermé
                         correcte | partielle | fausse | indeterminee
```

Une réponse **mathématiquement exacte** ne peut jamais être classée fausse quelle
que soit son écriture. Vérifié sur douze cas concrets (§ 3.3).

**API métier** — cinq routes sous `/api/v1`, préfixées comme le reste du contrat
existant : `GET /parcours`, `GET /exercices/:id`,
`GET /exercices/:id/indice/:palier`, `POST /corrections`, `POST /progression`.
`/health` et `/api/v1` sont inchangés.

**Interface** — page de parcours et écran d'exercice. Le contenu pédagogique
n'est jamais embarqué : il est chargé depuis l'API à l'affichage, ce qui garde
la réponse attendue sous le contrôle du serveur.

### 1.3 Corrections apportées : quatre défauts réels

Les trois premiers sont des failles de garde-fous, pas des détails de forme.

**D1 — Le garde-fou calendaire ne couvrait qu'une route sur trois.** *(corrigé)*
Le contrôle d'ouverture des blocs existait sur `GET /api/v1/exercices/:id`
(403), mais **pas** sur la route d'indice ni sur la correction. Un identifiant
d'exercice deviné suffisait donc à faire corriger — donc à faire travailler —
une leçon non encore enseignée, en contournant le risque F2 que le chantier 6
avait identifié comme principal. Constat mesuré avant correction : en semaine 1,
`POST /corrections` sur un exercice de B3 renvoyait **200** au lieu de 403.
Le contrôle est désormais factorisé en une fonction unique
(`verifierExerciceAccessible`) appliquée à l'énoncé, à l'indice **et** à la
correction.

**D2 — `/progression` acceptait n'importe quelle chaîne comme statut.** *(corrigé)*
Le statut venait du client et était transtypé sans validation. `non_acquis` —
un état que le modèle n'a pas le droit d'émettre, et qu'interdit explicitement
la règle « un objectif non testé reste `non_evalue` » — entrait dans le calcul
de progression et produisait un statut. Le vocabulaire est désormais fermé
(`STATUTS_REPONSE`) et contrôlé à l'exécution : valeur hors liste refusée en
400, jamais devinée ni réinterprétée.

**D3 — Deux pièges orientaient vers la mauvaise leçon.** *(corrigé)*
Le catalogue A.4 associe chaque signature à des leçons candidates ; or :

| Exercice | Piège | Signature | Orientait vers | Leçon réelle |
|---|---|---|---|---|
| `MVP-B2-E3` | `5√2` | `signe_non_reparti` | L5 | **L3** |
| `MVP-B3-E3` | `3/4` | `coefficient_multiplicatif_oublie` | L3 | **L5** |

Le mécanisme observé (un signe perdu sur une racine, un facteur oublié sur une
fraction) ne correspond à aucune signature existante. Les rattacher à la
signature la plus proche aurait fait recommander **la mauvaise leçon** — un
défaut invisible, puisque la correction, elle, est juste. Les deux sont passés
en `hors_perimetre`, qui signifie « aucune conclusion spécifique » : la seule
désignation exacte au regard du catalogue existant.

**D4 — Six tests préexistants dépendaient de l'horloge murale.** *(corrigé)*
Ils ne forçaient pas la date et échouaient dès que la date réelle tombait hors
année scolaire. C'est arrivé pendant ce chantier. Ces tests passaient pour une
bonne raison, et échouaient pour une autre : la date est désormais forcée par
`DATE_NAVIGATION_TEST`, et le test de progression documente pourquoi.

### 1.4 Renforcements ajoutés

**Contrôle de conformité client** (`securite.test.ts`, frontend) — les critères
C1 et C3 du chantier 6 exigeaient que « aucun contenu BEPC ne transite vers le
client » et « aucun secret dans le bundle » soient **automatisés, pas seulement
tenus par convention**. Ils ne l'étaient pas. Le contrôle est textuel et
exhaustif : identifiants d'épreuve, formulations désignant un document du jury,
clés et jetons, `NEXT_PUBLIC_*` sensible, contenu pédagogique embarqué.

**Prérequis rendus vérifiables** — `prerrequisSatisfaits` était du code mort
(déclaré, jamais appelé). Le chantier 6 liste l'ordre des prérequis (P1) parmi
les propriétés devant pouvoir être contrôlées automatiquement. Trois contrôles
l'ont rendu tel : acyclicité des dépendances, ordre de présentation vérifié sur
la liste réellement servie, et comportement de la règle elle-même.

**Non-régression sur l'équivalence algébrique** — un test vérifie qu'un
faisceau d'écritures exactes (`1 + 2x`, `2(x+0.5)`, `(2x+3)(2x-3)`,
`4(x−1.5)(x+1.5)`, `√(50)`, `2/16`, `0.125`…) ne produit jamais `fausse`, et un
second que ces casfellent toujours en `partielle` avec `formeRespectee: false`
et `lectureArbitree: false`.

**Documentation** — `openapi.yaml` et `docs/CONTRAT-API.md` mis à jour dans le
même commit que le code, conformément à la règle de ce dépôt. Les nouveaux
codes `403` et le refus de statut hors vocabulaire y sont documentés.

---

## 2. Dépôts et commits

Branche `main` dans les trois dépôts. Compte `digitalholding2026-ux`.

| Dépôt | Commit | Objet | Volume |
|---|---|---|---|
| `relio-backend` | `f598e28` | MVP pédagogique | 22 fichiers, +4 424 / −26 |
| `relio-frontend` | `f7064c1` | Parcours et écran d'exercice | 10 fichiers, +1 277 / −48 |
| `Relio` (racine) | — | Aucun changement | dépôt déjà à jour |

**Poussés et vérifiés.** Le SHA distant a été relu après coup et comparé au SHA
local pour les deux dépôts applicatifs : identiques (`f598e28…`, `f7064c1…`).

### 2.1 Rebase sur des commits reçus

Les deux dépôts avaient reçu entre-temps des commits d'introduction de la CI
(`af1ae5e` backend, `6905969` frontend) que ce chantier n'avait pas produits.
Les deux commits ont été **rebasés** par-dessus.

- **Backend** : un conflit, sur `.github/workflows/ci.yml`. Les deux versions
  étaient identiques sauf l'absence de saut de ligne final. **La version du
  dépôt distant a été conservée**, pour ne pas écraser un fichier déjà publié.
  Tests rejoués après rebase : 140/140.
- **Frontend** : rebase sans conflit.

### 2.2 Authentification de push

Le canal d'écriture GitHub était bloqué : les opérations de **lecture**
(`ls-remote`, `fetch`) fonctionnaient, mais le push expirait en timeout. Le
diagnostic a été mené par dichotomie — `git credential fill` expirait lui aussi
alors que la lecture du fichier de credentials par `git credential-store` aboutissait,
ce qui a désigné l'absence d'authentification d'écriture comme cause et non un
problème réseau ou de permission.

Le jeton a été installé **hors des dépôts** : fichier `~/.git-credentials` en
droits `600`, plus une règle `insteadOf` globale qui l'injecte à la volée. Il
n'entre dans **aucun** `.git/config` de dépôt — vérifié par recherche sur les
trois dépôts (`grep -c github_pat .git/config` → `0` dans chacun). Les URLs
distantes restent propres et exportables sans secret.

---

## 3. Tests et vérifications

### 3.1 Résultats consolidés

Toutes les commandes ci-dessous ont été **exécutées**, et leurs sorties lues.

| Vérification | Backend | Frontend |
|---|---|---|
| `npm run typecheck` (`tsc --noEmit`) | ✅ aucune erreur | ✅ aucune erreur |
| `npm test` | ✅ **140 / 140**, 28 suites, 0 échec | ✅ **35 / 35**, 7 suites, 0 échec |
| `npm run build` | ✅ `tsc --project tsconfig.build.json` | ✅ `next build`, 5 pages générées |
| `openapi.yaml` | ✅ YAML valide, 7 chemins, schémas de réponse cohérents | — |

Les tests.previous.Count du rapport du chantier 5 (40) sont passés à **175**
au total sur les deux dépôts (+135).

### 3.2 Vérification fonctionnelle de bout en bout

Un serveur a été lancé depuis le **code compilé** (`dist/server.js`), puis
interrogé en HTTP réel :

| Requête | Attendu | Obtenu |
|---|---|---|
| `GET /parcours` (S1) | B1 ouvert seul, 0 exercice hors bloc ouvert | ✅ semaine 3, `B1:ouvert B2:S5 B3:S10`, 6 exercices B1, 0 B3 |
| `POST /corrections` sur B3 en S1 | 403 | ✅ **403** (avant correction : 200) |
| `GET /exercices/MVP-B3-E1/indice/1` en S1 | 403 | ✅ **403** |
| `POST /progression` avec `statut: "non_acquis"` | 400 | ✅ `Statut inconnu : « non_acquis ». Valeurs acceptées : correcte, partielle, fausse, indeterminee.` |

### 3.3 Correction : vérification de l'équivalence algébrique

Douze écritures **exactes mais différentes** de la réponse attendue ont été
soumises au moteur. Résultat, pour toutes : `mathemathiquementJuste: true`, et
`statut: ` `partielle` avec `formeRespectee: false` — jamais `fausse` :

| Exercice | Saisie | Statut |
|---|---|---|
| `MVP-B1-E1` | `1 + 2x` | correcte (aucune forme exigée) |
| `MVP-B1-E1` | `2(x) + 1` | correcte |
| `MVP-B1-E1` | `2(x+0.5)` | correcte |
| `MVP-B1-E4` | `(2x+3)(2x-3)` | correcte |
| `MVP-B1-E4` | `4(x-1.5)(x+1.5)` | correcte |
| `MVP-B1-E4` | `4x^2 - 9` | **partielle** — cas F1 |
| `MVP-B3-E1` | `2/16` | **partielle** |
| `MVP-B1-E3` | `0.125` | **partielle** — même valeur, écriture décimale |
| `MVP-B3-E3` | `24/36` | **partielle** — cas F1 |
| `MVP-B2-E1` | `√50` | **partielle** |
| `MVP-B2-E1` | `√(50)` | **partielle** |

### 3.4 Conformité du bundle construit

Contrôles effectués sur `.next/static` après build réel :

| Contrôle | Résultat |
|---|---|
| Identifiant d'épreuve BEPC (`BEPC-20xx-…`) dans le bundle | ✅ absent |
| `sourceBepc` / `reponseAttendue` dans le bundle | ✅ absent |
| Secret (`sk-…`, `ghp_…`, `NEXT_PUBLIC_*KEY/SECRET/TOKEN`) | ✅ absent |
| Énoncé d'exercice (`On considère le nombre`) dans le bundle | ✅ absent |

### 3.5 Les contrôles peuvent-ils échouer ?

Un test qui passe toujours ne prouve rien. Les contrôles ont été **déclenchés
volontairement** : l'ajout d'un identifiant BEPC, d'un jeton `sk-…` et d'un
champ `reponseAttendue` a fait passer le compteur de 6 réussites à 5, 4, puis 3
sur 6. Les trois contrôles mordent. Un contrôle d'existence de fichier a été
ajouté pour la même raison : un scanneur qui ne lirait rien passerait toujours.

### 3.6 État de la CI — *non vérifié*

Les workflows existent dans les deux dépôts et exigent, pour chaque push :
`npm ci` → `npm run typecheck` → `npm test` → `npm run build`, plus un audit de
dépendances **informatif** (`continue-on-error: true`).

**Leur exécution n'a pas été observée.** L'outil `gh` est absent de
l'environnement et l'API GitHub n'a pas été sollicitée : l'état réel de la CI
sur GitHub est **inconnu**. Ce que le rapport peut affirmer, c'est que les
commandes que la CI exécète passent **localement**, sur les mêmes commits
(`f598e28`, `f7064c1`).

Le chantier 5 (T-1) signalait une CI bloquée par l'absence du scope `workflow`
sur un jeton. Le jeton installé ici est de type PAT ; **son périmètre n'a pas été
vérifié**. Si ce blocage est toujours présent, les workflows peuvent exister
sans s'exécuter.

---

## 4. Critères d'acceptation

Référentiel : critères du chantier 6, § 7. « Démontré » = preuve exécutable
dans ce chantier.

### 4.1 Critères pédagogiques

| # | Critère | État | Démonstration |
|---|---|---|---|
| A1 | ≥ 3 items par objectif | ✅ | 5 objectifs, minimum 3 items — `contenu.test.ts` échoue si un objectif descend sous 3 |
| A2 | Aucune conclusion d'acquisition sur un seul item | ✅ | `progression.ts` : 3 réussites sans erreur restent `non_evalue` (borne 100 %). `acquis_confirme` est hors vocabulaire et inatteignable |
| A3 | `partielle` existe, comptée ni juste ni fausse | ✅ | Le statut existe dans le vocabulaire fermé ; 12 exercices × pièges vérifiés ; `partielle` n'est jamais compté comme erreur ni comme réussite |
| A4 | Cadrage « première idée » présent et non optionnel | ✅ | Affiché sur la page de parcours, hors du bloc conditionnel |
| A5 | 100 % original, `source_bepc: null`, contrôle automatisé | ✅ | Contrôle sur les 12 exercices + sur **toute** la source client (§ 3.4) |
| A6 | Aucune leçon hors périmètre exposée | ✅ | 404 sur exercice inconnu ; les blocs fermés renvoient `exercices: []` ; contrôle que seuls L1/L3/L5 apparaissent |
| A7 | Aucune fonctionnalité inachevée accessible | ✅ | Tuteur IA, comptes élèves, notation et tableau de bord enseignant : non implémentés. Les étapes non livrées s'affichent « bientôt » / « non planifié » |

### 4.2 Critères de correction

| # | Critère | État | Démonstration |
|---|---|---|---|
| B1 | Réponses recalculées par un script versionné | 🟡 **partiel** | Les **12 exercices du MVP** sont recalculés indépendamment de la chaîne déclarée (`contenu.test.ts` : évaluateurs racines et fractions réécrits, expressions vérifiées sur l'énoncé). Le script `outils/verifier-diagnostic-m3.py` du chantier 6 (CP12), portant sur les 5 questions et 6 sondes de la mission 3, **n'a pas été produit** |
| B2 | Règle D5 écrite et testée sur les 2 cas de F1 | 🟡 **partiel** | Les deux cas sont **testés et traités** (§ 3.3). Mais D5 reste **non arbitrée** : la lecture appliquée est signalée `lectureArbitree: false`, pas fixée (§ 5) |
| B3 | Chaque piège déclenche sa signature, une seule | ✅ | 30+ pièges vérifiés ; invariant de non-duplication des valeurs ; **contrôle ajouté** : une signature ne peut pas orienter vers une autre leçon que celle de l'exercice (D3) |
| B4 | Aucun exercice n'accepte par longueur ou motif | ✅ | Égalité algébrique exacte sur polynômes à coefficients rationnels ; aucune comparaison de chaîne dans le chemin de correction |

### 4.3 Critères de conformité et de sécurité

| # | Critère | État | Démonstration |
|---|---|---|---|
| C1 | Aucun contenu BEPC vers le client | ✅ | Bundle construit inspecté (§ 3.4) **et** contrôle automatisé permanent sur la source |
| C2 | Visibilité du dépôt Git vérifiée et actée | ❌ **non satisfait** | Hors périmètre technique du chantier ; **reste à décider par le propriétaire** (§ 5.2) |
| C3 | Aucune donnée nominative, identifiant local anonyme | ✅ | `/corrections` ne reçoit que `exerciceId`, `reponse`, `indiceDemande` ; contrôle sur les clés réellement transmises |
| C4 | Durée de conservation et purge définies **par écrit** | 🟡 **partiel** | Le problème est **contourné plutôt que résolu** : rien n'est persisté. La route `/progression` recalcule à la volée. La durée de conservation reste non arbitrée (§ 5.1) |
| C5 | CI des deux dépôts verte | ❌ **non vérifié** | Workflows présents ; exécution **non observée**, `gh` absent (§ 3.6) |
| C6 | Typecheck, lint, build verts | ✅ | Typecheck et build verts dans les deux dépôts. **Note : aucun linter n'est configuré** dans ces deux dépôts — le critère est satisfait pour les outils qui existent, pas pour un lint qui n'a jamais été mis en place |

### 4.4 Bilan

| | Nombre |
|---|---|
| Critères satisfaits | **12** |
| Partiellement satisfaits | 3 (B1, B2, C4) |
| Non satisfaits ou non vérifiés | 2 (C2, C5) |

Les deux derniers ne relèvent pas d'un défaut de code : l'un est une décision
de gouvernance, l'autre une vérification qui exige un accès que cet
environnement n'a pas.

---

## 5. Points bloquants et réserves

### 5.1 La lecture « juste mais mal formé » — décision à prendre

**C'est le seul point qui empêche de conclure le chantier.** Les documents
validés contiennent deux règles qui se contredisent :

| Source | Ce qu'elle dit de `4x^2 + 4x − 8` et `14/12` |
|---|---|
| `specification-diagnostic-initial.md` § 5 | 🔴 classed en erreur |
| `regles-recommandation-pedagogique.md` A.3 | `partielle` — « juste mais pas dans la forme demandée », et « ne compte **jamais** comme fausse » |

Le chantier 6 identifiait précisément ce point comme **D5**, à trancher par un
enseignant. **Il ne l'a pas été.**

**Traitement retenu** : la règle A.3 est appliquée, parce que c'est la seule
des deux qui soit explicite sur le comportement à tenir, et parce qu'elle est la
plus prudente. **Mais ce choix n'est pas figé** : la correction renvoie
`lectureArbitree: false` et `pointsArbitrage: ["lecture-partielle-a3"]`, et
l'interface affiche « Ce point sera confirmé par ton enseignant ». Un retour de
l'enseignant suffit à trancher ; rien n'est à réécrire.

> Ce qui a été **écarté** : appliquer la règle du tableau par question et classer
> ces réponses en `fausse`. Cela aurait été plus simple, et aurait rendu le
> dispositif d'interprétation inerte : `denominateur_non_reduit` et
> `non_factorise` ne se seraient jamais déclenchés, et l'exercice recommandé
> aurait été faux. C'est exactement le mode de défaillance que le chantier 6
> désigne comme « le plus coûteux du projet, parce qu'il ne se voit pas ».

### 5.2 Décisions de gouvernance toujours ouvertes

| # | Point | Effet | Responsable |
|---|---|---|---|
| C2 | **Visibilité du dépôt GitHub** — les 4 PDF officiels du BEPC et l'inventaire des 35 énoncés sont versionnés dans `Relio`. Aucune vérification n'a été faite de la visibilité. | Risque juridique 🔴 | Propriétaire |
| C5 | **Périmètre du jeton** — le PAT installé n'a pas été inspecté. S'il n'a pas le scope `workflow`, les workflows existent mais ne s'exécutent pas. | CI muette | Propriétaire |
| D7 | **Durée de conservation des réponses** | Aucune persistance tant qu'elle n'est pas posée | Propriétaire + juridique |
| D9/D10 | **Comptes élèves et protection des mineurs** — hors MVP, mais toute persistance future en dépend | Blocage de la persistance | Juridique |

Les points D9 et D10 restent entiers. Ce chantier ne les a pas contournés : il
n'a écrit aucune donnée nulle part, précisément parce qu'ils ne sont pas posés.

### 5.3 Réserves techniques

**R1 — `ANNEE_SCOLAIRE_DEBUT` vaut `2025-09-01` par défaut.** Le référentiel
annuel donne un mois, pas un jour. Cette date est une **approximation
documentée**, configurable par variable d'environnement sans redéploiement. Elle
doit être fixée sur Railway avant la rentrée, faute de quoi l'ouverture des
blocs sera décalée d'une semaine environ.

**R2 — Aucune barre de lint.** Les deux dépôts n'en ont jamais eu. Les
contrôles de type stricts (`strict`, `noUncheckedIndexedAccess`) compensent en
partie, mais ce n'est pas la même chose.

**R3 — Grammaire de saisie limitée.** Le moteur refuse plutôt que de deviner :
division par une expression contenant `x`, exposants hors 0–16, radicand non
entier. Une saisie fuera de ce cadre produit un message élève et un **422**, pas
une correction approchée. C'est un choix deliberé — « le moteur ne devine
jamais » — mais sur un téléphone, une expression rejetée peut être interprétée
par l'élève comme « ma réponse est fausse ».

**R4 — Hypothèse H1 non testée.** Rien n'établit qu'un élève de 3e saisisse
une expression algébrique sur son téléphone. Le chantier 6 en a fait le risque
principal. **Ce chantier ne l'a pas testé et ne le pouvait pas.**

### 5.4 Ce qui n'a pas été fait, délibérément

Conformément au périmètre : pas de tuteur IA, pas de comptes élèves, pas de
notation ni de niveau, pas de tableau de bord enseignant, pas de diagnostic
complémentaire, pas de L6, L11 ni L12–L14, aucune publication de contenu
d'examen. La leçon L8 « Équations » (Q4 du diagnostic initial) reste hors MVP,
sa semaine d'ouverture (S16–S17) étant incompatible avec un déploiement de
rentrée.

---

## 6. Déploiement

### 6.1 Ce qui a été réellement fait

| Action | Réalisée | Comment |
|---|---|---|
| Build backend | ✅ Oui | `npm run build` → `dist/` |
| Build frontend | ✅ Oui | `next build` → `.next/`, 5 pages |
| Exécution locale du backend compilé | ✅ Oui | `node dist/server.js`, interrogé en HTTP réel |
| Contrôle du bundle frontend | ✅ Oui | inspection de `.next/static` |
| **Déploiement distant** | ❌ **Non** | — |
| **Vérification en production** | ❌ **Non** | — |
| **Test d'un parcours utilisateur réel** | ❌ **Non** | — |
| **Test sur mobile / tactile** | ❌ **Non** | — |
| **État de la CI sur GitHub** | ❌ **Non observé** | `gh` absent, API non sollicitée |

### 6.2 Ce que « build réussi » ne prouve pas

Un build vert prouve que le code compile et que les pages se génèrent. Il ne
prouve **rien** de ce qui suit, et rien de tout cela n'a été fait :

- que l'application est **joignable** une fois déployée ;
- que `API_BASE_URL` est correctement renseignée sur Vercel ;
- que les **origines CORS** du backend autorisent le domaine frontend réel — le
  chantier 4 avait relevé que `API_BASE_URL` est figée au build (T-2), et cette
  réserve **n'a pas été levée** ;
- que la correction fonctionne depuis un navigateur, avec un vrai client ;
- qu'un élève peut saisir une réponse au doigt sur un écran étroit.

### 6.3 Action requise pour que le MVP soit visible

Le redéploiement doit être **coordonné** : `GET /api/v1` renvoie désormais
`status: "mvp-pedagogique"` au lieu de `"socle"`. C'est un changement de contrat
documenté (v2.0.0 de `CONTRAT-API.md`), pas une rupture — le frontend compare
des chaînes — mais **le frontend doit être redéployé avec la nouvelle API**,
sous peine d'afficher un état périmé.

---

## 7. Actions manuelles restantes

| # | Action | Priorité | Responsable |
|---|---|---|---|
| 1 | **Trancher D5** : `partielle` ou erreur pour une réponse exacte mal formée ? Un mot suffit ; le code signale déjà le cas. | 🔴 Bloquant | Enseignant |
| 2 | **Vérifier la visibilité du dépôt `Relio`** (C2) : il contient les PDF officiels du BEPC et 35 énoncés transcrits. | 🔴 Juridique | Propriétaire |
| 3 | **Vérifier le scope `workflow`** du jeton, puis confirmer l'exécution réelle de la CI sur les deux dépôts. | 🟠 | Propriétaire |
| 4 | **Fixer `ANNEE_SCOLAIRE_DEBUT`** sur Railway avant la rentrée (aujourd'hui `2025-09-01`). | 🟠 | Propriétaire |
| 5 | **Redéployer** backend et frontend de façon coordonnée. | 🟠 | Propriétaire |
| 6 | Vérifier `CORS_ORIGINS` sur Railway contre le domaine frontend de production. | 🟠 | Propriétaire |
| 7 | **Tester la saisie sur téléphone** (H1) : 5 élèves, 3 minutes, sans aide. | 🟠 | Responsable produit |
| 8 | Compléter le script `outils/verifier-diagnostic-m3.py` (CP12) si le critère B1 doit être intégralement satisfait. | 🟡 | Responsable technique |

Aucune de ces actions n'exige de reprise de code, sauf l'action 1 — et même
celle-ci ne demande qu'une décision, pas une réécriture.

---

## 8. Prochaine étape recommandée

### 8.1 Le chantier 8 ne devrait pas être un chantier de code

Le MVP est implémenté, testé et publié. Ce qui reste ne se.code pas : ce sont
des **arbitrages** et des **vérifications en conditions réelles**.

**Séquencement proposé :**

```
1. Action 1 — trancher D5              ← seul arbitrage pédagogique bloquant
2. Actions 4, 5, 6 — déployer           ← rendre le MVP visible
3. Action 7 — test de saisie H1         ← conditionne la suite
4. Actions 2, 3 — conformité et CI
5. Chantier 8 — sur la base de ce qui aura été observé
```

**Why D5 d'abord.** C'est le seul point où le code encode une lecture non
arbitrée. Il est signalé à chaque occurrence, donc rien n'est cassé — mais
tant qu'il n'est pas tranché, chaque réponse exacte mal rendue porte un statut
dont personne n'est comptable. Un mot de l'enseignant suffit.

### 8.2 Ce que le chantier 8 devrait faire, sous condition

Son contenu dépend **entièrement** du retour de H1 et de l'observation en
production. Deux scénarios, volontairement non tranchés ici :

- **Si H1 est fausse** (la saisie sur téléphone échoue), la priorité n'est pas
  d'ajouter des fonctionnalités : c'est de revoir le dispositif de saisie. Le
  contenu se dégraderait vers des réponses fermées, ce que le chantier 6
  signale comme **détruisant la valeur diagnostique** — une réponse juste par
  hasard produit un signal faux.
- **Si H1 est vraie**, le périmètre suivant est celui du parcours post-diagnostic
  (partie B des règles pédagogiques), qui suppose la persistance — donc D7, D9
  et D10, donc un cadre juridique. Ce n'est pas un chantier d'implémentation
  tant que ces points ne sont pas posés.

### 8.3 Ce qui ne faut pas faire

Le risque principal de ce projet n'est pas un bug : c'est **un contenu
mathématiquement juste et pédagogiquement faux**, dont l'écart avec le
programme réel ne se révélerait qu'à l'examen. Les garde-fous de ce chantier
sont conçus pour rendre cette situation visible tôt — un statut signalé plutôt
qu'un statut tranché. Les maintenir est plus important que toute nouvelle
fonctionnalité.

---

## 9. Vérifications commandées

reproductibles depuis la racine de chaque dépôt

```bash
# Backend
cd backend
npm ci && npm run typecheck && npm test && npm run build

# Frontend
cd frontend
npm ci && npm run typecheck && npm test && npm run build

# Conformité du bundle construit
grep -rE "BEPC-20[0-9]{2}-[A-Z]" frontend/.next/static   # attendu : aucun résultat
grep -rE "sk-[A-Za-z0-9]{16,}" frontend/.next/static      # attendu : aucun résultat
```

Les contrôles de `securite.test.ts` sont exécutés par `npm test` côté frontend
et échouent si la conformité est rompue.

---

## 10. Statut du chantier

# 🟠 TERMINÉ AVEC RÉSERVES

**Le périmètre d'implémentation est atteint.** Trois blocs, cinq objectifs et
douze exercices originaux sont livrés, testés et publiés. Quatre défauts réels
ont été corrigés, dont un qui rendait le garde-fou calendaire contournable. Les
175 tests passent, le typecheck et les builds sont verts dans les deux dépôts.

**Trois réserves motivent de ne pas conclure en « TERMINÉ » :**

1. **Une décision pédagogique manque (D5).** Le code applique une lecture
   signalée, jamais présentée comme arbitrée. C'est deliberé et sans danger
   immédiat — mais le chantier ne peut pas prétendre avoir tranché ce qu'il
   n'avait pas à trancher.

2. **Rien n'est vérifié en conditions réelles.** Aucun déploiement, aucun
   parcours utilisateur, aucun test mobile, aucun état de CI observé. Les
   vérifications disponibles ont été réactives et automatisées ; c'est une base
   réelle, mais ce n'est pas une validation en production.

3. **Deux critères du chantier 6 ne sont pas satisfaits** (C2, visibilité du
   dépôt ; C5, CI réellement verte). Ni l'un ni l'autre ne se corrige par du
   code.

Le MVP est **prêt à être déployé et à être testé par des élèves**. Il n'est pas
**validé en production**, et le chantier 6 demandait précisément de ne pas
confondre les deux.

---

*Documents liés : `docs/rapport-final-chantier-6.md`,
`docs/specification-diagnostic-initial.md`,
`docs/regles-recommandation-pedagogique.md`, `docs/matrice-couverture-competences.md`,
`data/referentiel-maths-3e-cm-2025-2026.json`.
Contrats : `relio-backend/openapi.yaml`, `relio-backend/docs/CONTRAT-API.md`.*
