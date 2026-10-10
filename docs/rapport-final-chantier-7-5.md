# Rapport final — Chantier 7.5 : tutoriel mathématique pas à pas et clavier intelligent

Date : 10 octobre 2026
Dépôts : `relio-backend`, `relio-frontend`, `Relio` (racine — documentation)

---

## 1. Audit de l'architecture initiale

L'audit a porté sur le **code réel de `main`** des deux dépôts, et non sur la
description des rapports 7, 7.2, 7.3 et 7.4. Il a été conduit avant toute
modification.

| Domaine | État constaté avant le chantier |
|---|---|
| Correction | `backend/src/contenu/correction.ts` — quatre axes séparés, verdict D5, `libelle` fourni par le serveur. Correct mais **un seul** message d'aide, toujours long |
| Reconnaissance d'erreur | 11 signatures fermées, reconnues par **comparaison de valeur** avec les pièges documentés de chaque exercice ; défaut `hors_perimetre` |
| `explication` vs `libelle` vs indices | `libelle` = phrase de verdict validée par l'enseignant. `explication` = aide unique, longue. Les trois paliers d'`indices` sont écrits par exercice et ne donnent jamais la réponse |
| Analyseur | `analyseur-expression.ts` : `+ − * / ^`, parenthèses, `x`, exposant entier 0–16. **La racine `√` est absente de cette grammaire** et traitée à part (`MOTIF_RACINE`). Les fractions n'existent que comme **chaîne `n/d`** |
| Progression | `POST /api/v1/progression` — calculée **sans persistance**, le client renvoie ses statuts |
| Persistance | **Aucune.** Ni base, ni identité, ni compte. Choix assumé et documenté : « la durée de conservation n'est pas arbitrée : on n'écrit rien » |
| Saisie | Un seul `<input type="text">`, `inputMode="text"`. Aucun clavier mathématique |
| Sécurité | La réponse attendue ne transite jamais vers le client ; garde d'accès au calendrier sur **toutes** les routes d'exercice |

**Deux conséquences structurantes**, qui ont dicté l'architecture du chantier :

1. Le tutorat devait être **déterministe et calculé côté serveur**. Un tuteur
   conversationnel est explicitement écarté par le cahier des charges.
2. La persistance ne pouvait pas être ajoutée côté serveur : cela reviendrait à
   décider seul, pour des élèves souvent mineurs, de la durée de conservation de
   leurs réponses — décision qui appartient au responsable du projet.

---

## 2. Parcours pédagogique avant / après

### Avant

Un premier échec déclenchait immédiatement le bloc complet :

> « Pour développer, il faut distribuer chaque terme dans les parenthèses, puis
> regrouper les termes qui se ressemblent. Par exemple : 2(x + 3) = 2x + 6, car
> le 2 se multiplie avec le x et avec le 3. Et si un terme est soustrait, le « − »
> change le signe de chaque terme entre parenthèses : 3(x − 4) = 3x − 12.
> Applique cette idée à ton exercice. »

L'élève n'avait rien cherché. Le second échec renvoyait **exactement le même
texte**.

### Après

Le premier échec renvoie une seule question ciblée sur l'erreur reconnue. Le
texte ne s'épaissit qu'après un nouvel essai réellement infructueux, et le
niveau 3 travaille enfin sur **les données de l'élève**.

Le verdict D5 est inchangé : le tutorat accompagne, il ne décide pas.

---

## 3. Les trois niveaux, sur des exemples réels

Exercice `MVP-B1-E1` — « A = 3(x + 2) − (x + 5) », réponse attendue `2x + 1`.
Élève saisit `4x + 1`. **Captures réelles, prises sur la production** (Railway,
après redéploiement).

### Niveau 1 — orienter *(origine : `signature`)*

> « As-tu distribué le signe « − » dans chaque terme entre parenthèses ? Que
> devient un terme précédé du « − » ? »
>
> *Action : Réessaie en tenant compte de cette question.*

Une question, aucune méthode, aucun exemple résolu, aucune réponse.

### Niveau 2 — expliquer une étape *(origine : `indice`, palier 2 existant)*

> « Pour développer, il faut distribuer chaque terme dans les parenthèses, puis
> regrouper les termes qui se ressemblent. 3(x + 2) donne 3x + 6. Pour (x + 5),
> le « − » change le signe des deux termes. »
>
> *Action : Applique cette étape à ton exercice, puis vérifie ton résultat.*

La règle arrive, mais toujours sur un exemple ou un indice **qui n'est pas la
réponse**.

### Niveau 3 — accompagner directement *(origine : `indice`, palier 3 existant)*

> « A = 3x + 6 − x − 5. Il ne reste plus qu'à regrouper. »
>
> *Action : Effectue cette dernière transformation, puis vérifie ta réponse.*

C'est le premier niveau qui cite l'expression de l'élève. Il s'arrête à la
dernière transformation utile : **la réponse n'est pas donnée**.

### Bilan de méthode, une fois le travail compris

Après `2x + 1`, en cas de réussite :

> « Tu y es arrivé après 2 essais. Voici la méthode à retenir. »
>
> **Méthode à retenir :** « Pour développer, il faut distribuer chaque terme
> dans les parenthèses, puis regrouper les termes qui se ressemblent. »

Le bilan est rendu **même sans aucune aide** : c'est une méthode à retenir, pas
une récompense.

### Réutilisation plutôt que duplication

Le contenu des niveaux n'est pas réécrit. Le niveau 2 et le niveau 3
reprennent **les indices existants de l'exercice** (paliers 2 et 3). Les
seules additions de contenu sont :

- `ORIENTATIONS_PAR_SIGNATURE` — une orientation courte par signature, sans
  exemple résolu, là où le message de 7.4 était trop long pour un premier échec ;
- `AIDES_PAR_OBJECTIF[].question` — une question d'orientation par objectif,
  utilisée quand **aucune cause n'est reconnue**, pour que l'élève ait quand même
  quelque chose à chercher.

---

## 4. Suivi des difficultés et limites de persistance

### Ce qui est enregistré

Par tentative : exercice, ordre, réponse saisie, statut D5, catégorie de
difficulté, niveau d'aide reçu, et si l'élève a réussi.

### Deux valeurs distinctes, à ne pas confondre

| Valeur | Signification |
|---|---|
| `null` | **Aucune erreur** : la réponse a été jugée juste |
| `erreur_non_identifiee` | Une erreur **est** constatée, mais le moteur ne sait pas laquelle |

Cette distinction est verrouillée par test. Afficher « difficulté inconnue » à
un élève qui a réussi aurait faussé le suivi que le chantier cherche justement à
fiabiliser.

### Prudence du suivi

Aucune signature du MVP ne reconnaît `denominateur_commun_incorrect` ni
`factorisation_incomplete`, pourtant listées au cahier des charges. **Elles ne
sont donc pas émises** : les attribuer serait un diagnostic que le moteur n'a pas
observé. `erreur_non_identifiee` prend leur place.

Une difficulté n'est dite **récurrente** qu'à partir de deux observations de
même catégorie. Un seul exercice réussi sans aide reste `donnee_insuffisante`.

Le vocabulaire de sortie ne contient **aucun état nommé « maîtrisé »**. Les
quatre états sont : `donnee_insuffisante`, `reussite_immediate`, `a_confirmer`,
`difficulte`.

### ⚠️ Limites de persistance — à lire explicitement

**Les tentatives ne sont conservées que dans le navigateur de l'élève**, sous la
clé `relio.observations.v1` (maximum 500 entrées).

Conséquences, qu'il ne faut pas minimiser :

- l'historique **disparaît** si l'élève vide les données du navigateur, navigue
  en navigation privée, ou change d'appareil ;
- il **n'est pas** partagé entre appareils ;
- il **n'est pas** exploitable par l'enseignant pour suivre une classe ;
- le serveur ne conserve **rien** : `POST /api/v1/suivi` est sans état, exactement
  comme `/api/v1/progression`, et la réponse le rappelle explicitement
  (`conservation`).

Ce choix est la solution **minimale** compatible avec l'architecture, pas une
solution de long terme. La décisions à arbitrer est listée au § 11.

**Aucune donnée superflue** n'est collectée : ni nom, ni identifiant d'élève, ni
date de naissance, ni identifiant d'appareil. Un test verrouille la liste
exacte des champs. Le journal est effaçable par l'élève en un bouton.

---

## 5. Conception du clavier et symboles réellement pris en charge

### Le problème mesuré

Le clavier système Android ne propose ni exposant, ni symbole racine, ni barre de
fraction sur la plupart des configurations de clavier français. L'élève devait
copier un caractère depuis une autre application.

### Règle structurante : n'insérer que ce que le moteur sait lire

Les symboles ont été **vérifiés par sonde sur les analyseurs de production**, et
non déduits du code. Résultat, contre-intuitif :

| Touche | Étiquette | Insère | Pourquoi |
|---|---|---|---|
| Division | `÷` | `/` | **`÷` est refusé** par la grammaire |
| Puissance 3 | `x³` | `^3` | **`³` est refusé** par la grammaire |
| Puissance 2 | `x²` | `^2` | `²` est accepté et normalisé |
| Moins | `−` | `−` | U+2212, normalisé par l'analyseur |
| Multiplié | `×` | `×` | U+00D7, normalisé par l'analyseur |
| Racine | `√` | `√` | Accepté **uniquement** par l'analyseur de racines |

Une touche insérant `÷` ou `³` aurait produit une réponse **refusée alors que
l'élève a écrit ce qu'il croit être juste** — le pire échec possible pour un
clavier. Le test `n'insère jamais un caractère refusé par la grammaire` verrouille
ce point.

`√` n'est **pas** proposée sur un exercice d'expression : l'analyseur d'expressions
la refuse. La proposer inviterait à composer une réponse rejetée.

### Touches présentes

- **Opérations** : `+` `−` `×` `÷` `=`
- **Algèbre** : `x`, parenthèses ouvrante et fermante, `x²`, `x³`, `xⁿ`
  (puissance générale)
- **Racines** : `√`, puis saisie du radicand, avec parenthèses
- **Fractions** : touche dédiée, insérant la barre de division — numérateur et
  dénominateur restent distincts, et sont écrits dans le format que
  l'analyseur rationnel lit déjà (`n/d`)
- **Contrôle** : retour arrière, effacement total, déplacement du curseur,
  validation, fermeture, bascule vers le clavier système

### Choix d'implémentation

**Aucune dépendance ajoutée.** Pas de bibliothèque de clavier : le composant
tient en ~130 lignes. Le poids de la page passe de 106 kB à 111 kB en
premier chargement, dont 5,35 kB pour la route d'exercice.

**Aucune couche AST parallèle.** Une seule chaîne, celle que le moteur analyse.
L'affichage lisible des fractions et des racines (`apercuLisible`) ne modifie
jamais la valeur envoyée. Une structure séparée aurait été une seconde vérité à
maintenir en cohérence avec l'analyseur.

**Le champ natif reste porteur de la saisie.** Le presse-papiers et le clavier
physique continuent de fonctionner, et le curseur ne « saute » pas après chaque
frappe.

**`inputMode="none"`** supprime le clavier système Android sans empêcher la
saisie au clavier physique. Un bouton « Clavier système » rend le comportement
habituel à l'élève.

**Accessibilité** : chaque touche porte un `aria-label` en français (un glyphe
seul comme `^2` ou `√` n'est pas lu utilement), le bloc est un `role="group"`
nommé, et la fermeture / réouverture passent par des boutons nommés.

**Ergonomie** : grille de 4 colonnes, touches d'au moins 44 px de côté,
clavier en `position: sticky` en bas de page — donc **il pousse le contenu au
lieu de le recouvrir**. Le champ actif et le bouton « Vérifier » restent
visibles, en permanence. Aucune animation.

---

## 6. Fichiers modifiés

### Backend (`relio-backend`, commit `d72b14c`)

| Fichier | Nature |
|---|---|
| `src/contenu/tutorat.ts` | **nouveau** — échelle d'aide, catégories de difficulté |
| `src/lib/suivi.ts` | **nouveau** — agrégation par objectif |
| `src/contenu/aides.ts` | orientations courtes, questions d'orientation, export de `orientationPourObjectif` |
| `src/contenu/correction.ts` | export de `formeDansLeMessage` (réutilisé, non dupliqué) |
| `src/routes/parcours.ts` | `tutorat` + `categorieDifficulte` sur `/corrections` ; nouvelle route `/suivi` |
| `src/routes/v1.ts` | documentation de la route |
| `test/tutorat.test.ts` | **nouveau** — 23 tests |
| `test/suivi.test.ts` | **nouveau** — 14 tests |
| `test/parcours.test.ts` | +13 tests de route |
| `test/api.test.ts` | liste des routes mise à jour |

### Frontend (`relio-frontend`, commit `cb24663`)

| Fichier | Nature |
|---|---|
| `src/lib/clavier.ts` | **nouveau** — logique d'insertion, jeu de touches, aperçu |
| `src/lib/observations.ts` | **nouveau** — journal local |
| `src/lib/tutorat.ts` | **nouveau** (fichier vide laissé par un chantier antérieur) — contrat d'affichage |
| `src/components/ClavierMath.tsx` | **nouveau** — composant clavier |
| `src/components/Exercice.tsx` | intégration tutorat, clavier, journal, suivi |
| `src/lib/parcours.ts` | types, `nbEchecs`, `chargerSuivi` |
| `src/app/globals.css` | styles clavier, tutorat, suivi |
| `src/lib/clavier.test.ts` | **nouveau** — 35 tests |
| `src/lib/observations.test.ts` | **nouveau** — 15 tests |
| `src/lib/tutorat.test.ts` | **nouveau** — 14 tests |
| `src/lib/parcours.test.ts` | contrat de requête mis à jour |

### Aucun changement de périmètre

Aucun nouvel exercice, aucune réponse attendue modifiée, aucun changement de
calendrier scolaire, aucun bloc ouvert, aucune règle D5 modifiée, aucun compte
utilisateur, aucune clé API exposée, aucune donnée d'élève en journal serveur.

---

## 7. Tests, typechecks et builds

| Contrôle | Résultat |
|---|---|
| Backend `npm test` | **261 / 261** (206 avant le chantier, +55) |
| Backend `npm run typecheck` | **OK** |
| Backend `npm run build` | **OK** |
| Frontend `npm test` | **107 / 107** (13 fichiers, +64) |
| Frontend `npm run typecheck` | **OK** |
| Frontend `npm run build` | **OK** — 111 kB premier chargement |

### Non-régression vérifiée par test automatisé

- les 12 exercices et 36 indices sont présents, avec leurs trois paliers ;
- les 5 verdicts D5 et les 4 statuts techniques sont inchangés — un test compare
  le verdict, le statut, le libellé et l'explication avant et après le tutorat ;
- les 36 indices ne donnent jamais la réponse attendue ;
- le bloc fermé reste protégé.

### Trois défauts réels trouvés et corrigés en cours de chantier

1. **« Ton résultat est juste » sur une réponse fausse.** Sur `MVP-B1-E5`, la
   saisie `2x − 7` est fausse *et* mal formée ; le tutorat annonçait la
   justesse. Corrigé par un garde sur `mathemathiquementJuste`. Test de
   régression ajouté.
2. **Le curseur n'avançait jamais** après une insertion au clavier — la saisie
   au milieu d'une expression était donc cassée. Corrigé dans `inserer()`.
3. **Une orientation affirmait une justesse inexistante.** Sur `MVP-B3-E1`,
   `1/2` hérite de la signature « dénominateur non réduit » par comparaison de
   valeur, alors que l'attendu est `1/8` et que la réponse est fausse. Le texte
   n'affirme plus la justesse.

---

## 8. Vérifications visuelles et mobiles — ce qui a et n'a pas été fait

### Réalisé : vérification sur la production, par appels HTTP

Le règlement du projet interdit de lancer un serveur local, Chromium ou
Playwright pour reproduire le parcours élève. **Cette règle a été respectée :
aucun navigateur n'a été lancé.** La vérification a donc porté sur les
services déployés.

| Vérification | Constat |
|---|---|
| Backend `/health` | `ok`, `environment: production` |
| Backend redéploiement | constaté par l'apparition de `/api/v1/suivi` (uptime passé de 3513 s à 17 s) |
| Échelle des trois niveaux | constatée par HTTP : niveaux 1, 2, 3 avec trois textes distincts |
| Catégorie de difficulté | `oubli_de_distribuer_un_facteur`, `reponse_illisible`, `null` sur réussite |
| Bilan de méthode | rendu après réussite, avec `resume` |
| Refus d'une catégorie inventée | HTTP 400, vocabulaire fermé renvoyé |
| Suivi par objectif | agrégation constatée, avec `difficultesRecurrentes` |
| Contenu et calendrier | 9 exercices ouverts (B1, B2), B3 fermé → **HTTP 403**, 0 exercice livré |
| Verdicts D5 | les 5 verdicts toujours produits |
| Frontend | `/`, `/parcours`, `/parcours/MVP-B1-E1` en **200** ; 9 liens d'exercices ; aucune page « Exercices indisponibles » |
| Frontend redéploiement | constaté par le nouveau CSS (`d376418…` contenant `clavier__grille`) et par le nouveau chunk de route contenant `relio.observations`, `inputMode` et `a_confirmer` |

### ⚠️ Non réalisé, et à faire valider sur téléphone réel

**Aucun test sur téléphone réel n'a été effectué.** Il n'y a pas d'appareil
Android dans l'environnement de travail, et le lancement d'un navigateur local
est interdit par le règlement du projet.

En conséquence, **les points suivants ne sont pas validés** et ne doivent pas
être présentés comme tels :

- la saisie au doigt sur un écran étroit ;
- le comportement exact de `inputMode="none"` sur les navigateurs Android — si
  un téléphone ne respecte pas cette valeur, **deux claviers pourrait
  s'afficher simultanément** ;
- le défilement et la visibilité du champ lorsque le clavier s'ouvre ;
- la taille réelle des touches au doigt.

### Procédure de vérification manuelle proposée

Sur un téléphone Android, en portrait, sur `https://relio-frontend-one.vercel.app/parcours/MVP-B1-E1` :

1. **Ouverture** — toucher le champ « Ta réponse ». Vérifier que le clavier
   mathématique s'affiche et que **le champ et le bouton « Vérifier » restent
   visibles**. Vérifier qu'**un seul** clavier apparaît.
2. **Saisie** — composer `3(x+2)` avec les touches `3`, `(`, `x`, `+`, `2`, `)`.
   Vérifier que les parenthèses s'insèrent bien au curseur.
3. **Correction au milieu** — placer le curseur au milieu de la saisie et appuyer
   sur `←` puis `+`. Vérifier que le caractère s'insère à la position voulue et
   que le curseur reste juste après.
4. **Suppression** — `⌫` efface le dernier caractère, `C` vide tout.
5. **Clavier masqué** — appuyer sur « Masquer le clavier », puis le rouvrir avec
   le bouton « Clavier mathématique ».
6. **Clavier système** — appui sur « Clavier système » : le clavier Relio doit
   disparaître et celui du téléphone apparaître.
7. **Progression du tutorat** — saisir `4x + 1` et « Vérifier » **tro fois de
   suite**. Vérifier que le premier retour est une question courte, que le
   deuxième explique une étape, que le troisième agit sur l'expression de
   l'exercice — et qu'aucun des trois n'affiche `2x + 1`.
8. **Succès** — saisir `2x + 1 ». Le verdict « Ta réponse est juste » doit
   apparaître, suivi du bloc « Méthode à retenir ».
9. **Suivi** — vérifier l'apparition du compteur de tentatives et du bouton
   « Effacer mon historique », puis que ce bouton vide bien le compteur.
10. **Exercice de racine** — ouvrir `MVP-B2-E1` : la touche `√` doit être
    présente. Sur `MVP-B1-E1`, elle doit être **absente**.
11. **Exercice de fraction** — ouvrir un exercice du bloc 3 (non ouvert en
    semaine 5) ou attendre son ouverture ; la touche `⅗` doit apparaître.

---

## 9. Commits et état du push

| Dépôt | Commit | Push |
|---|---|---|
| `relio-backend` | `d72b14c` — `feat(tutorat): accompagnement pas à pas et suivi des difficultés` | `main` poussé, `dd17de0..d72b14c` |
| `relio-frontend` | `cb24663` — `feat(clavier): clavier mathématique et affichage du tutorat` | `main` poussé, `bfaef2b..cb24663` |
| `Relio` (racine) | rapport de chantier | ce commit |

---

## 10. État du déploiement

| Élément | État |
|---|---|
| Code poussé | `git log` / `git ls-remote` — les trois dépôts |
| Backend redéployé | **confirmé par HTTP** : `/api/v1/suivi` présent, uptime 17 s après le push |
| Frontend redéployé | **confirmé par HTTP** : CSS et chunk de route du chantier 7.5 servis |
| Parcours élève testé par HTTP | `/`, `/parcours`, `/parcours/[id]`, `/corrections`, `/suivi`, garde 403 |
| Parcours élève testé sur téléphone | **non réalisé** — cf. § 8 |

Un push réussi n'est pas un déploiement : les deux ont été constatés séparément.

---

## 11. Limites restantes et décisions nécessaires

### À arbitrer par le responsable du projet

1. **Durée de conservation des réponses d'élèves.** C'est la décision qui
   bloque toute persistance durable. Tant qu'elle n'est pas prise, le suivi
   reste local à l'appareil et ne peut pas être exploité par un enseignant.
2. **Suivi de classe.** Suppose la décision ci-dessus, et probablement des
   comptes. Hors périmètre de ce chantier, qui ne les introduit pas.
3. **Message de saisie illisible.** Sur `$$$`, l'API renvoie « Caractère non
   reconnu : « $ ». », formulation technique héritée du moteur d'analyse.
   L'action d'aide qui l'accompagne est claire, mais le message lui-même gagnerait
   à être reformulé à la 3e. Non modifié ici : c'est un texte validé.
4. **Texte de 7.4 sur le dénominateur non réduit.** L'`explication` historique
   affirme encore « Ton calcul est juste », ce qui est faux quand la valeur est
   également fausse (cas `MVP-B3-E1`). **Le frontend n'affiche plus ce champ** —
   il affiche le tutorat — mais l'API l'expose toujours. Correction proposée,
   non appliquée : c'est un texte validé par l'enseignant.

### Limites techniques assumées

5. **Le suivi n'est pas une mesure de maîtrise.** Il indique le nombre d'aides
   dont l'élève a eu besoin. Il ne dit pas ce que l'élève retiendra demain.
6. **Une difficulté récurrente se mesure sur deux observations.** En dessous,
   le suivi s abstain. Sur douze exercices, le suivi peut donc rester muet
   longtemps.
7. **Le clavier ne couvre que ce que la grammaire sait lire.** Pas d'équation
   (`x^(2+3)` est refusé par le moteur), pas de racine dans une expression, pas
   d'exposant calculé. Le clavier ne prétend pas faire mieux que le moteur.
8. **Aucune vérification visuelle automatisée.** Le règlement du projet
   l'interdit et aucun téléphone n'est disponible. La procédure du § 8 reste à
   exécuter.

---

## 12. Conclusion

Le tutorat progresse réellement : les trois niveaux ont été constatés sur la
production avec trois textes distincts, et aucun ne publie la réponse attendue —
vérifié sur les douze exercices et sur toutes leurs réponses testées, à chaque
niveau. Le verdict D5 est intact. Le clavier insère des symboles que le moteur
sait réellement lire, ce qui exclut le pire scénario — une réponse rejetée parce
que la touche a inséré `³` ou `÷`.

Ce qui n'est **pas** acquis, et qui est dit tel quel : le suivi des difficultés
n'est conservé que sur l'appareil de l'élève, et aucune saisie au doigt n'a été
validée sur un téléphone réel.