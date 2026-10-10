# Matrice de couverture — compétences et leçons (diagnostic initial)

**Mission** : 3 — Spécification pédagogique du diagnostic initial du MVP
**Date** : 2026-10-10
**Sources** : `data/referentiel-maths-3e-cm-2025-2026.json` (référentiel annuel, **non modifié**),
`data/inventaire-questions-bepc-2025-2026.json` (inventaire BEPC 2025/2026)
**Statut** : `specification_provisoire_en_attente_de_validation_pedagogique`

---

## 0. Avertissement déterminant — à lire avant tout le reste

**Le référentiel annuel ne contient aucune compétence, aucun objectif et aucun
prérequis.** Vérification faite sur les 14 leçons :

| Champ du référentiel | Éléments renseignés |
|---|---|
| `competences` | **0** |
| `objectifs` | **0** |
| `prerequis` | **0** |
| `exercices_ids` | **0** |
| `corriges_ids` | **0** |
| `references_bepc` | **0** |

La note de conformité du fichier l'indique explicitement : *« Aucune compétence,
prérequis, exercice ou corrigé n'a été renseigné : aucun document de référence
pédagogique n'a été fourni. »*

**Conséquence directe sur cette mission.** La demande portait sur « les compétences
documentées, lorsqu'elles sont disponibles ». **Elles ne le sont pas, pour aucune
des 14 leçons.** Cette matrice ne peut donc pas être construite sur des
compétences officielles. Elle est construite sur deux niveaux explicitement
séparés :

| Niveau | Statut | Usage autorisé |
|---|---|---|
| **Leçon** (intitulé, volume horaire, trimestre) | ✅ **DOCUMENTÉ** — transcrit du tableau de progression officiel | Base fiable de la matrice, utilisable pour le pilotage |
| **Objectif opérationnel** (OO) | ⚠️ **DÉDUIT** par l'analyste à partir des questions BEPC observées | Usage interne de conception, **à valider par l'équipe pédagogique** |

> **Aucun objectif opérationnel de ce document ne constitue une compétence
> officielle.** Ils sont une déduction analytique, marquée comme telle dans
> chaque section, et aucun ne doit être présenté à l'élève, aux parents ou à
> l'administration comme relevant d'un texte officiel.

**Le champ `references_bepc` du référentiel reste vide par choix** : la mission 2
a produit les correspondances dans un fichier séparé plutôt que d'écrire dans le
référentiel. Cette matrice s'appuie donc sur l'inventaire, pas sur le référentiel.

---

## 1. Vue d'ensemble

| Rang | Leçon (documenté) | h | Trim. | Q. BEPC | Fiabilité | Tier de couverture |
|---|---|---|---|---|---|---|
| L1 | Calcul littéral | 7 | T1 | **11** | 9 confirmées / 2 incertaines | 🟢 Solide |
| L2 | Propriétés de Thalès dans un triangle | 7 | T1 | 1 | 1 confirmée | 🟡 Fragile |
| L3 | Racines carrées | 7 | T1 | 4 | 4 confirmées | 🟢 Correct |
| L4 | Triangle rectangle | 11 | T1 | 4 | 4 confirmées | 🟢 Correct |
| L5 | Calcul numérique | 9 | T1 | 5 | 3 confirmées / 2 incertaines | 🟢 Correct |
| L6 | **Angles inscrits** | 5 | T2 | **0** | — | 🔴 **Nulle** |
| L7 | Vecteurs | 7 | T2 | 3 | 1 confirmée / 2 incertaines | 🟡 Fragile |
| L8 | Équations et inéquations dans ℝ | 5 | T2 | 4 | 4 confirmées | 🟢 Correct |
| L9 | Coordonnées de vecteurs | 7 | T2 | 6 | 5 confirmées / 1 incertaine | 🟢 Solide |
| L10 | Équations de droites | 7 | T2 | 2 | 2 confirmées | 🟡 Fragile |
| L11 | **Statistique** | 7 | T3 | 1 | 1 confirmée | 🔴 **Nulle** |
| L12 | Équations et inéquations dans ℝ×ℝ | 7 | T3 | 2 | 2 confirmées | 🟡 Fragile |
| L13 | Applications affines | 5 | T3 | 3 | 2 confirmées / 1 incertaine | 🟡 Fragile |
| L14 | Pyramides et cônes | 7 | T3 | 3 | 3 confirmées | 🟡 Fragile |

**Volume horaire total : 98 h déclarées sur les leçons** (le référentiel annonce
120 h annuelles ; l'écart de 21 h est réparti sur régulation et révision — cohérent
avec les totaux par trimestre déjà validés en mission 1).

**Répartition des 49 associations question↔leçon :** 41 confirmées (84 %), 8 incertaines (16 %).

### Trois lectures

1. **Le calcul littéral est le cœur du diagnostic** : 11 questions observées sur 49
   liens, très largement au-dessus des autres leçons. C'est le point d'entrée
   naturel du parcours.
2. **Deux leçons sont des angles morts** : L6 (5 h, **0 question**) et L11
   (7 h, **1 question**). Ce sont 12 h de programme, soit 12 % du volume des
   leçons, sans signal exploitable.
3. **Le tiers du programme n'est qu'éclairé** : L2, L7, L10, L12, L13, L14
   reposent sur 1 à 3 questions chacun, dont plusieurs associations incertaines.

---

## 2. LeConstraint majeure : aucune question BEPC n'est publiable

L'inventaire porte l'avertissement suivant, inchangé depuis la mission 2 :

> « **NON VÉRIFIÉS.** Les sujets, figures et corrigés harmonisés sont des documents
> publiés par la Direction des Examens, des Concours et de la Certification du
> Cameroun. Leur reproduction, republication ou exploitation commerciale dans
> l'application n'est pas autorisée en l'état. »

**Il en découle une règle structurante pour tout le MVP :**

| Usage des questions BEPC | Statut |
|---|---|
| Référence interne de calibrage (savoir *ce qui* est évalué, à quel niveau) | ✅ **Autorisé** |
| Base de validation de la difficulté et de la pertinence diagnostic | ✅ **Autorisé** |
| **Affichage à l'élève dans l'application** | ❌ **Interdit en l'état** |
| **Reproduction d'énoncés, figures ou corrigés** | ❌ **Interdit en l'état** |

**Il faut assumer une tension réelle** : le contenu le plus fiable du projet — les
corrigés harmonisés nationaux, dont les 35 résultats ont été revérifiés à la
source — est précisément le contenu qu'on ne peut pas montrer. **La mini-évaluation
livrée en mission 3 est donc entièrement composée de questions originales**,
explicitement identifiées comme telles, dont les réponses ont été vérifiées par
calcul independent (voir `docs/specification-diagnostic-initial.md`).

Les questions BEPC servent de **calibrage** : elles disent quels savoir-faire
l'examen valorise et à quel niveau de difficulté.

---

## 3. Détail par leçon

Légende : ✅ DOCUMENTÉ (référentiel) · ⚠️ DÉDUIT (analyste)

---

### L1 — Calcul littéral · 7 h · T1 · 🟢 Solide

**OO déduits :**
- ⚠️ `OO-L1-1` Développer une expression algébrique (distributivité, identités remarquables)
- ⚠️ `OO-L1-2` Factoriser une expression (différence de deux carrés, mise en facteur commun)
- ⚠️ `OO-L1-3` Simplifier une fraction rationnelle et poser sa condition d'existence

**Questions BEPC observées (11) :**
`2025-NUM-EX01-1`, `2025-NUM-EX01-2a`, `2025-NUM-EX01-2b`, `2025-NUM-EX02-1`,
`2025-NUM-EX02-2`, `2025-NUM-EX02-3a`, `2025-NUM-EX02-3b`, `2026-NUM-EX01-1`,
`2026-NUM-EX03-1`, `2026-NUM-EX03-2`, `2026-NUM-EX03-3b`
*Fiabilité : 9 confirmées. Incertaines : `2025-NUM-EX01-1` (fraction rattachée au
littéral par extension), `2026-NUM-EX01-1` (idem).*

**Lacune :** `OO-L1-3` (condition d'existence) n'est observé qu'en 2025 et n'a
jamais été réobservé en 2026 — signal possiblement saisonnier, à ne pas surinterpréter.

**Besoin en questions originales :** 🟢 **Priorité 1** — le socle du diagnostic
initial. Questions originales fournies : **Q2** (`OO-L1-1`) et **Q3** (`OO-L1-2`).

---

### L2 — Propriétés de Thalès dans un triangle · 7 h · T1 · 🟡 Fragile

**OO déduits :**
- ⚠️ `OO-L2-1` Utiliser le théorème de Thalès pour calculer une longueur dans un triangle

**Questions BEPC observées (1) :** `2026-GEO-EX01-2` (AF = 4√3/3) — *confirmée*

**Lacune :** une seule observation sur deux sessions. Le corrigé 2026 montre un
usage maîtrisé (AE/AB = AF/AC, résultat exact et cohérent), mais **rien ne permet
de dire si Thalès est « fragile » ou simplement « peu sollicité »**.

**Besoin en questions originales :** 🟡 Priorité 2. Géométrie = figure nécessaire,
donc contrainte d'affichage sur téléphone. À traiter dans le diagnostic complémentaire.

---

### L3 — Racines carrées · 7 h · T1 · 🟢 Correct

**OO déduits :**
- ⚠️ `OO-L3-1` Simplifier une expression contenant des racines carrées (√a√b = √ab, extraction des carrés parfaits)
- ⚠️ `OO-L3-2` Rationaliser le dénominateur d'une fraction

**Questions BEPC observées (4) :** `2025-NUM-EX01-2a` (B = 34−24√2),
`2025-NUM-EX01-2b` (C = 2), `2025-NUM-EX01-2c` (D = 17−12√2), `2026-NUM-EX01-2` (B = −50√2)
*Fiabilité : 4 confirmées. Incertaine : rattachement de `2025-NUM-EX01-2c` (rationalisation) à L5.*

**Lacune :** les deux sessions n'utilisent que la forme `a√2` — **la racine d'un
nombre non carré parfait et la conjugaison ne sont pas observées**.

**Besoin en questions originales :** 🟢 Priorité 1. Question originale fournie (Q5).

---

### L4 — Triangle rectangle · 11 h · T1 · 🟢 Correct

**Volume le plus élevé du programme (11 h) et 4 observations.**

**OO déduits :**
- ⚠️ `OO-L4-1` Appliquer le théorème de Pythagore (calcul d'hypoténuse ou de côté)
- ⚠️ `OO-L4-2` Utiliser cos/sin/tan dans un triangle rectangle
- ⚠️ `OO-L4-3` Reconnaître et utiliser un théorème des hauteurs / configuration du cercle circonscrit

**Questions BEPC observées (4) :** `2025-GEO-EX02-1` (AC = 10), `2025-GEO-EX02-2` (tan = 4/3),
`2026-GEO-EX01-1` (AB = 4√3, BC = 4), `2026-B-T3` (génératrice d'un cône)
*Fiabilité : 4 confirmées.*

**Lacune :** le théorème des hauteurs n'apparaît dans aucune des deux sessions.

**Besoin en questions originales :** 🟡 Priorité 2. Figure obligatoire → diagnostic complémentaire.

---

### L5 — Calcul numérique · 9 h · T1 · 🟢 Correct

**OO déduits :**
- ⚠️ `OO-L5-1` Calculer sur les nombres rationnels (somme commun dénominateur, produit, signe)
- ⚠️ `OO-L5-2` Rédiger un résultat sous forme irréductible

**Questions BEPC observées (5) :** `2025-NUM-EX01-1` (11/16), `2025-NUM-EX01-2c` (17−12√2),
`2026-NUM-EX01-1` (3/5), + 2 autres
*Fiabilité : 3 confirmées, 2 incertaines (rattachement au littéral par extension).*

**Lacune :** aucune observation de calcul en base 10, ni de conversion d'unités
(un point soulevé par la mission 2 sur `2026-B-T2`).

**Besoin en questions originales :** 🟢 Priorité 1. Question originale fournie (Q1).

---

### L6 — Angles inscrits · 5 h · T2 · 🔴 **AUCUNE COUVERTURE**

**Aucune question BEPC ne se rattache à cette leçon** dans les deux sessions
(constat établi et documenté en mission 2, anomalie D-9).

**OO déduits :** **AUCUN.** Aucun ne peut être proposé sans source, car le seul
intitulé disponible est « Angles inscrits » — trop court pour en déduire des
objectifs opérationnels sans risque d'inventer.

**Lacune :** 🔴 **la plus grave de la matrice.** 5 h de programme, aucune
configuration circulaire dans les deux sujets, aucun objectif dérivable.

**Besoin en questions originales :** 🔴 **Priorité 1 mais bloqué.** Produire ces
questions exige de savoir *quel* contenu de la leçon 6 est attendu. **Décision
pédagogique requise avant rédaction** (cf. rapport final, décision n° 2). Toute
question produite ici serait de l'invention de contenu pédagogique.

---

### L7 — Vecteurs · 7 h · T2 · 🟡 Fragile

**OO déduits :**
- ⚠️ `OO-L7-1` Caractériser l'orthogonalité de deux droites
- ⚠️ `OO-L7-2` Reconnaître deux vecteurs colinéaires

**Questions BEPC observées (3) :** `2025-GEO-EX01-1` (Faux), `2025-GEO-EX01-2` (Faux),
`2026-GEO-EX02-1` (placement de points)
*Fiabilité : **1 confirmée, 2 incertaines.** Seule la première est fiable.*

**Lacune :** les deux réponses sont « Faux » à des questions vrai/faux — **le
corrigé ne montre pas le raisonnement attendu**. Un élève peut répondre « Faux »
par hasard (50 %). **Ces deux items ont une valeur diagnostique faible**, ce qui
justifie de ne pas les retenir pour la mini-évaluation malgré leur fiabilité.

**Besoin en questions originales :** 🟡 Priorité 2. Figure obligatoire.

---

### L8 — Équations et inéquations dans ℝ · 5 h · T2 · 🟢 Correct

**OO déduits :**
- ⚠️ `OO-L8-1` Résoudre une équation du premier degré
- ⚠️ `OO-L8-2` Résoudre une inéquation du premier degré
- ⚠️ `OO-L8-3` Déduire la condition d'existence d'une fraction rationnelle

**Questions BEPC observées (4) :** `2025-B-T1` (budget 3 000 000 FCFA),
`2025-B-T3` (x > 5), `2026-NUM-EX03-3a` (S = {5/4 ; −6/7}), `2026-NUM-EX03-3b`
*Fiabilité : 4 confirmées.*

**Lacune :** les deux sessions ne contiennent **aucune inéquation demandée
explicitement** (`2025-B-T3` se formulait par comparaison de coûts) et **aucun
problème de mise en équation autonome** — les deux questions observées sont
toujours intégrées à une situation.

**Besoin en questions originales :** 🟢 Priorité 1. Question originale fournie (Q4).

---

### L9 — Coordonnées de vecteurs · 7 h · T2 · 🟢 Solide

**OO déduits :**
- ⚠️ `OO-L9-1` Calculer les coordonnées d'un vecteur
- ⚠️ `OO-L9-2` Représenter des points dans un repère orthonormé

**Questions BEPC observées (6) :** `2025-GEO-EX01-2`, `2026-GEO-EX02-1`, `2026-GEO-EX02-2`,
`2026-GEO-EX02-3`, `2026-GEO-EX02-4`, `2026-GEO-EX02-5`
*Fiabilité : 5 confirmées, 1 incertaine.*

**Lacune :** la leçon apparaît **uniquement en 2026** (5 des 6 liens), en
blocage complet sur un exercice unique. Signal possible d'un changement de
programme d'une année sur l'autre — **à faire confirmer, pas à conclure**.

**Besoin en questions originales :** 🟡 Priorité 2. Placement = figure.

---

### L10 — Équations de droites · 7 h · T2 · 🟡 Fragile

**OO déduits :**
- ⚠️ `OO-L10-1` Reconnaître l'équation d'une droite passant par deux points
- ⚠️ `OO-L10-2` Caractériser la perpendicularité par les coefficients Directors

**Questions BEPC observées (2) :** `2025-GEO-EX01-1` (Faux), `2026-GEO-EX02-3` (−5x+7y+18 = 0)
*Fiabilité : 2 confirmées. L'une des deux est un vrai/faux sans raisonnement publié.*

**Lacune :** aucune résolution d'équation de droite par le calcul (trouver a et b
en passant par deux points) n'est observée.

**Besoin en questions originales :** 🟡 Priorité 2. Figure obligatoire.

---

### L11 — Statistique · 7 h · T3 · 🔴 **COUVERTURE INEXPLOITABLE**

**Question BEPC observée (1) :** `2026-NUM-EX02` (poids moyen = 63 kg) — *confirmée*

**Lacune :** 🔴 **cette unique observation est inexploitable pour le MVP, pour
une raison technique et non pédagogique.** La question suppose la lecture d'un
**tableau de statistiques figurant dans le sujet**, que nous ne pouvons pas
reproduire (droits sur les figures). De plus, en lecture seule la question est
quasi impossible : elle se déduit d'un tableau, pas d'un calcul mental.

**Elle ne peut donc pas servir de modèle à une question originale** : il faut
reconstruire un support de données original.

**Besoin en questions originales :** 🔴 **Priorité 1.** Un tableau de données
original + question de moyenne pondérée. **Support à concevoir** (décision n° 3).

---

### L12 — Équations et inéquations dans ℝ×ℝ · 7 h · T3 · 🟡 Fragile

**OO déduits :**
- ⚠️ `OO-L12-1` Résoudre un système de deux équations à deux inconnues

**Questions BEPC observées (2) :** `2026-B-T1` (2x+y = 61 000 ; x+3y = 75 500 → x = 21 500, y = 18 000), `2025-B-T2`
*Fiabilité : 2 confirmées — **mais `2025-B-T2` est la question annulée par le jury
(anomalie D-2, aucune solution publiée).** Elle ne peut servir que de contexte.

**Lacune :** aucune résolution par combinaison linéaire n'est publiée en détail ;
le corrigé 2026 donne le résultat sans montrer la méthode.

**Besoin en questions originales :** 🟡 Priorité 2. Un système original, avec
**correction détaillée obligatoire** — c'est la lacune des lacunes ici.

---

### L13 — Applications affines · 5 h · T3 · 🟡 Fragile

**OO déduits :**
- ⚠️ `OO-L13-1` Modéliser une situation par une fonction affine
- ⚠️ `OO-L13-2` Représenter graphiquement une fonction affine

**Questions BEPC observées (3) :** `2025-B-T3`, `2026-GEO-EX02-4`, `2026-GEO-EX02-5`
*Fiabilité : 2 confirmées, 1 incertaine (modélisation par fonctions affines).*

**Lacune :** **aucune question ne demande explicitement de construire ou de
représenter une fonction affine.** Les trois liens sont des rattachements par
analogie (translation, parallélogramme, comparaison de forfaits).

**Besoin en questions originales :** 🟡 Priorité 2. La représentation graphique
est peu adaptée au téléphone ; privilégier une version algébrique.

---

### L14 — Pyramides et cônes · 7 h · T3 · 🟡 Fragile

**OO déduits :**
- ⚠️ `OO-L14-1` Calculer le volume d'une pyramide
- ⚠️ `OO-L14-2` Calculer l'aire d'une surface (latérale + base) pour un besoin de revêtement
- ⚠️ `OO-L14-3` Calculer le volume d'un cône de révolution

**Questions BEPC observées (3) :** `2025-GEO-EX03` (pyramide V = 192 cm³),
`2026-B-T2` (fût cylindrique), `2026-B-T3` (cône, h = 12, V = 314)
*Fiabilité : 3 confirmées. Anomalie D-5 : le **cylindre** ne relève pas de
l'intitulé « Pyramides et cônes ».*

**Lacune :** une des trois questions relève d'une forme qui n'est pas dans
l'intitulé de la leçon. **La leçon n'a que 2 observations valides.**

**Besoin en questions originales :** 🟡 Priorité 2. Volume de pyramide = question
sans figure possible si les dimensions sont données en clair → **bonne
candidate pour le diagnostic complémentaire**.

---

## 4. Synthèse des besoins en questions originales

| Priorité | Leçon | Manque | Statut de production |
|---|---|---|---|
| 🔴 **P0** | **L11 Statistique** | Support de données original (moyenne pondérée) | À concevoir — **décision requise** |
| 🔴 **P0** | **L6 Angles inscrits** | Objectifs de contenu non définissables sans source | 🔴 **Bloqué — décision pédagogique requise** |
| 🟢 P1 | L1 Calcul littéral | Socle du diagnostic | ✅ **Fourni** (Q2, Q3) |
| 🟢 P1 | L5 Calcul numérique | Fractions, forme irréductible | ✅ **Fourni** (Q1) |
| 🟢 P1 | L3 Racines carrées | Simplification d'expressions | ✅ **Fourni** (Q5) |
| 🟢 P1 | L8 Équations | Résolution du 1er degré | ✅ **Fourni** (Q4) |
| 🟡 P2 | L2, L4, L7, L9, L10, L12, L13, L14 | Coverage géométrie / systèmes / fonctions | À produire au diagnostic complémentaire |

**Besoins transversaux non couverts par la mini-évaluation :**
inéquations, systèmes avec méthode détaillée, mise en équation, fonctions affines,
géométrie (toutes leçons à figure), statistiques, pyramides et cônes.

---

## 5. Limites de cette matrice

1. **Aucune compétence officielle n'a été utilisée ni créée.** Tout le contenu
   pédagogique est déduit de questions observées sur deux sessions.
2. **Deux sessions ne sont pas le programme.** L'absence de L6 ne prouve rien
   sur son poids réel dans l'examen.
3. **Les objectifs opérationnels sont des hypothèses de conception**, à valider
   par l'équipe pédagogique avant tout affichage à l'élève.
4. **Aucune question de cette matrice n'est publiable** tant que les droits sur
   les documents BEPC ne sont pas établis.
5. **La fiabilité « confirmée » signifie « correspondance vérifiée avec la
   source », pas « question bien conçue »** — les items vrai/faux en sont le
   contre-exemple (L7).

---

*Documents liés : `docs/specification-diagnostic-initial.md`,
`docs/regles-recommandation-pedagogique.md`, `data/inventaire-questions-bepc-2025-2026.json`.*