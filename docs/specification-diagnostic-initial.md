# Spécification du diagnostic initial — mini-évaluation du MVP

**Mission** : 3 — Spécification pédagogique du diagnostic initial
**Version** : 1.0 — `specification_en_attente_de_validation`
**Date** : 2026-10-10
**Statut** : ⚠️ **AUCUN DÉVELOPPEMENT NE DOIT COMMENCER AVANT VALIDATION** (contrainte de mission)

---

## 1. Objet et périmètre

Premier contact de l'élève avec l'application : un diagnostic court qui produit
une **première hypothèse de niveau** et un **premier exercice adapté**, puis
propose un diagnostic plus complet.

**Ce que ce document spécifie** : le contenu, les corrections, la justification
pédagogique et les limites d'interprétation de la mini-évaluation.

**Ce qu'il ne spécifie pas** : l'architecture technique, le modèle de données,
l'interface détaillée. Ces éléments dépendent de décisions produit non prises.

---

## 2. Décision structurante : pourquoi des questions originales

Les 35 questions BEPC inventoriées en mission 2 ont des **réponses vérifiées à la
source** et constituent la meilleure base de calibrage disponible. Elles ne sont
toutefois **pas publiables** : les droits d'utilisation ne sont pas établis.

> **Règle appliquée :** les questions BEPC servent à **calibrer** (savoir *ce qui*
> est évalué, à quel niveau). Elles ne sont **pas** utilisées comme contenu élève.

**Les 5 questions de cette mini-évaluation sont donc originales.** Chacune est
identifiée `ORIG-` et vérifiée par calcul indépendant (§ 5).

**Aucune compétence officielle n'est inventée** : chaque question est rattachée à
un objectif opérationnel *déduit* (voir `docs/matrice-couverture-competences.md`).

---

## 3. Couverture et ce qu'elle ne couvre pas

| Leçon (documentée) | Objectif opérationnel (déduit) | Question |
|---|---|---|
| L5 — Calcul numérique (9 h) | `OO-L5-1`, `OO-L5-2` | Q1 |
| L1 — Calcul littéral (7 h) | `OO-L1-1` | Q2 |
| L1 — Calcul littéral (7 h) | `OO-L1-2` | Q3 |
| L8 — Équations dans ℝ (5 h) | `OO-L8-1` | Q4 |
| L3 — Racines carrées (7 h) | `OO-L3-1` | Q5 |

**Couverture : 4 leçons sur 14, soit 28 h sur 98 h déclarées (29 %).**

### Ce qui n'est délibérément pas dans la mini-évaluation

| Exclu | Raison |
|---|---|
| **Toute la géométrie** (L2, L4, L7, L9, L10) | Exige des figures — contrainte forte sur téléphone, et figures BEPC non réutilisables |
| **Statistique (L11)** | La seule question observée est **inexploitable** : elle se déduit d'un tableau du sujet, non reproductible. Un support original est à concevoir (décision produit n° 3) |
| **Angles inscrits (L6)** | 🔴 **Bloqué** — aucun objectif dérivable sans document source. Produire une question serait inventer du contenu pédagogique |
| **Systèmes (L12)**, **fonctions affines (L13)**, **pyramides (L14)** | Non prioritaires ; le corrigé 2026 n'y publie pas de méthode détaillée, on ne peut donc pas bien les calibrer |

**Cette mini-évaluation ne prétend pas situer l'élève sur les 14 leçons.** Elle
produit une hypothèse sur 4 axes, et le diagnostic complémentaire couvre le reste.

---

## 4. Critère de sélection : la valeur diagnostique

Une question n'est retenue que si **ses erreurs plausibles sont distinctes et
instructives**. Une question binaire sans raisonnement (QCM, vrai/faux) est
écartée : répondre juste par hasard donne un signal faux.

| Critère | Exigence |
|---|---|
| Discrimination | Chaque erreur fréquente correspond à une difficulté identifiable et différente |
| Autocorrection possible | L'élève peut détecter et corriger son erreur seul |
| Vérifiable | La correction a été contrôlée par calcul indépendant |
| Autonome | Réponse sans figure et sans donnée externe |
| Sans ambiguïté | Une seule lecture correcte de l'énoncé |

**Justification du refus de `2025-A-GEO-EX1-1` et `-2`** (malgré leur fiabilité) :
les réponses attendues sont toutes deux « Faux », avec une probabilité de 50 % de
réponse correcte par hasard. **Zéro valeur diagnostique.** Voir matrice, L7.

---

## 5. Les 5 questions originales

> **Toutes les réponses ci-dessous ont été recalculées indépendamment** lors de
> la rédaction (développement formel, fractions exactes). Elles ne sont pas
> recopiées d'une source.

---

### Q1 — Calcul numérique · `ORIG-M3-Q01` · sans figure · entrée : fraction

**Énoncé**
> Calcule le nombre suivant, puis donne le résultat sous forme **irréductible** :
> **A** = 5/6 + 7/12 − 1/4

**Correction**
```
5/6 = 10/12      1/4 = 3/12
A = 10/12 + 7/12 − 3/12 = 14/12 = 7/6
```
**Réponse attendue : 7/6** · Objectifs : `OO-L5-1`, `OO-L5-2`

**Pourquoi cette question** — C'est le point d'entrée le plus accessible, et le
seul item qui distingue une erreur de signe d'une erreur de réduction : deux
difficultés très différentes, une seule question.

**Ce que la réponse permet de conclure**

| Réponse | Conclusion |
|---|---|
| `7/6` | ✅ Aucune difficulté observée sur l'addition de rationnels |
| `14/12` | ⚠️ **Cas particulier** — résultat juste mais non réduit → difficulté sur `OO-L5-2` uniquement, pas sur `OO-L5-1` |
| `11/6`, `5/3` | 🔴 Difficulté probable sur les **signes** (`OO-L5-1`) |
| `20/12`, `24/12` | 🔴 Erreur probable de report de dénominateur |
| Non répondue | ⬜ Aucune conclusion — ne pas interpréter |

**Ce qu'elle ne permet pas de conclure** : rien sur les fractions en multiplication,
ni sur les nombres décimaux, ni sur le calcul littéral.

---

### Q2 — Calcul littéral · `ORIG-M3-Q02` · sans figure · entrée : texte avec touches x, ², −

**Énoncé**
> Développe et réduis l'expression :
> **E** = (x + 3)² − (x + 1)(x − 2)

**Correction**
```
(x + 3)²    = x² + 6x + 9
(x + 1)(x − 2) = x² − x − 2
E = x² + 6x + 9 − (x² − x − 2)
  = x² + 6x + 9 − x² + x + 2
  = 7x + 11
```
**Réponse attendue : 7x + 11** · Objectif : `OO-L1-1`

**Pourquoi cette question** — C'est l'item le plus discriminant du lot : il
superpose **deux** compétences (identité remarquable + distributivité) et, surtout,
**leur combinaison avec un signe soustracteur**, qui est l'erreur classique.
L'annulation des termes en x² ne peut pas être réussie par hasard.

**Ce que la réponse permet de conclure**

| Réponse | Conclusion |
|---|---|
| `7x + 11` | ✅ Maîtrise observée de la combinaison identité + distributivité |
| `5x + 7` | 🔴 **Erreur signature** : le signe `−` n'a pas été distribué sur `(x+1)(x−2)` → difficulté sur `OO-L1-1`, sous-précision « distributivité avec changement de signe » |
| `7x − 11` | 🔴 Erreur sur le terme constant après soustraction |
| `7x + 11 + x²` (terme non annulé) | 🔴 Erreur de collection des termes |
| Non répondue | ⬜ Aucune conclusion |

**Ce qu'elle ne permet pas de conclure** : rien sur la factorisation (Q3), ni sur
la résolution d'équations (Q4).

---

### Q3 — Factorisation · `ORIG-M3-Q03` · sans figure · entrée : texte

**Énoncé**
> Factorise l'expression suivante sous la forme d'un produit de facteurs du premier degré :
> **G** = (2x + 1)² − 9

**Correction**
```
G = (2x + 1)² − 3²                    (différence de deux carrés)
  = (2x + 1 − 3)(2x + 1 + 3)
  = (2x − 2)(2x + 4)
  = 4(x − 1)(x + 2)
```
**Réponses attendues : `(2x − 2)(2x + 4)`** — ou, à valeur algébrique égale,
**`4(x − 1)(x + 2)`** · Objectif : `OO-L1-2`

**Pourquoi cette question** — Elle est le **miroir de Q2** : même identité
remarquable, mais appliquée à la factorisation. Un élève qui réussit Q2 et échoue
Q3 n'a pas « raté le calcul littéral » de façon diffuse : il a raté **le passage
de la forme développée à la forme factorisée**, ce qui oriente immédiatement vers
une activité ciblée. **C'est le meilleur discriminant du lot.**

> ⚠️ **Les deux formes sont acceptées.** La correction doit comparer les
> **valeurs algébriques**, pas les chaînes de caractères. Voir § 6.

**Ce que la réponse permet de conclure**

| Réponse | Conclusion |
|---|---|
| `(2x − 2)(2x + 4)` ou `4(x − 1)(x + 2)` | ✅ Factorisation acquise |
| `4x² + 4x − 8` | 🔴 A développé mais **n'a pas factorisé** → ne sait pas « passer de l'autre côté » |
| `(2x − 4)(2x + 2)` | 🔴 Erreur signature : inversion des signes dans `(a − b)(a + b)` |
| `(2x + 1 − 3)(2x + 1 + 3)` | 🟡 **Réponse intermédiaire correcte, non achevée** → ne pas la compter juste ni fausse (voir règles § 4) |

**Ce qu'elle ne permet pas de conclure** : rien sur le développement (Q2), rien
sur le facteur commun.

---

### Q4 — Équations · `ORIG-M3-Q04` · sans figure · entrée : valeur de x

**Énoncé**
> Résous dans ℝ l'équation : **3(x − 2) + 4 = 5x + 8**

**Correction**
```
3(x − 2) + 4 = 5x + 8
3x − 6 + 4 = 5x + 8
3x − 2 = 5x + 8
− 2x = 10
x = − 5
```
**Vérification** : 3(−5 − 2) + 4 = −21 + 4 = −17 ; 5(−5) + 8 = −25 + 8 = −17 ✅

**Réponse attendue : x = −5** · Objectif : `OO-L8-1`

**Pourquoi cette question** — L'équation du premier degré est la compétence la
plus **transposable à toutes les situations** du BEPC (mise en équation en
Partie B, dans les deux sessions). Elle teste le passage du texte à l'algèbre, et
la réponse est **vérifiable par l'élève lui-même** en remplaçant — ce qui alimente
la boucle d'explication.

**Ce que la réponse permet de conclure**

| Réponse | Conclusion |
|---|---|
| `−5` | ✅ Résolution maîtrisée |
| `5` | 🔴 **Erreur signature** : perte du signe en passant de `−2x = 10` à `x` |
| `10` ou `10/2` | 🔴 Arrêt intermédiaire : l'élève ne termine pas la division |
| `−17` | 🔴 A calculé le membre de gauche et s'est arrêté |
| Pas de solution / « x = ±5 » | 🔴 Erreur de manipulation |

**Ce qu'elle ne permet pas de conclure** : rien sur les **inéquations** (L8 n'est
observé que par comparaison de coûts, jamais en tant qu'inéquation demandée), ni
sur les systèmes.

---

### Q5 — Racines carrées · `ORIG-M3-Q05` · sans figure · entrée : texte avec touche √

**Énoncé**
> Simplifie l'expression suivante sous la forme **a√2** (a entier relatif) :
> **B** = 2√50 − √8 + √18

**Correction**
```
√50 = √(25 × 2) = 5√2
√8  = √(4 × 2)  = 2√2
√18 = √(9 × 2)  = 3√2

B = 2 × 5√2 − 2√2 + 3√2 = 10√2 − 2√2 + 3√2 = 11√2
```
**Réponse attendue : 11√2** · Objectif : `OO-L3-1`

**Pourquoi cette question** — C'est le seul item sur les racines carrées, et il
teste trois extractions de carrés parfaits en une fois. Le coefficient **2 devant
√50** est le piège principal : il faut l'extraire avant de multiplier.

**Ce que la réponse permet de conclure**

| Réponse | Conclusion |
|---|---|
| `11√2` | ✅ Extraction correcte y compris le coefficient |
| `6√2` | 🔴 **Erreur signature** : le coefficient `2` devant √50 a été oublié → 5 − 2 + 3 |
| `9√2` | 🔴 √8 traité comme 4√2 (carré perfect faux) |
| `10√2`, `12√2` | 🔴 Erreur d'addition des coefficients après extraction |
| `11√3` | 🔴 Simplification menée sur la mauvaise base |
| `50√2` | 🔴 Aucune extraction des carrés parfaits |

**Ce qu'elle ne permet pas de conclure** : rien sur la **rationalisation** (non
observée en 2026), ni sur les racines de nombres non carrés parfaits.

---

## 6. Saisie des réponses sur téléphone

La saisie est le point critique : fractions, racines et exposants sont
hostiles au clavier d'un téléphone. **Spécification :**

| Élément | Spécification |
|---|---|
| **Fractions** (Q1) | Deux champs distincts **numérateur** et **dénominateur**. Pas de frappe du `/` — le séparateur est affiché. Clavier numérique uniquement, avec bouton `−` dédié |
| **Variable x** | Bouton dédié insérant `x` (pas de clavier) |
| **Exposant** | Bouton `²` (Q2) |
| **Racine** | Bouton `√` insérant `√(…)` avec parenthèses automatiques (Q5) |
| **Multiplication** | Implicite par accolade `{…}(…)` ; `×`, `*` et `·` acceptés en saisie |
| **Réponse à une équation** (Q4) | Un seul champ, valeur seule. `x = −5`, `x=-5` et `−5` acceptés |

### Normalisation des réponses

Avant toute comparaison : suppression des espaces, uniformisation des moins
(`−`, `–`, `-`), des puissances (`^`, `²`), des racines (`√(n)` → forme interne),
ajout des `*` implicites.

### Comparaison : égalité algébrique, pas égalité de texte

**Obligatoire pour Q2 et Q3.** `4(x-1)(x+2)` et `(2x-2)(2x+4)` sont différents
comme chaînes et égaux comme expressions. La spécification exige un
**évaluateur algébrique** qui compare après développement, et non une
comparaison de chaînes.

> **⚠️ Point de conception ouvert :** un évaluateur algébrique est une
> dépendance technique non triviale. **Alternative MVP** : lister les formes
> acceptées en dur par question et normaliser par expansion sur `x`. Décision
> technique à trancher (décision produit n° 5).

### Trois statuts de réponse, pas deux

| Statut | Définition | Exemple |
|---|---|---|
| ✅ `correcte` | Égale à une forme acceptée | `7/6` |
| 🟡 `partielle` | Juste mais non dans la forme demandée, ou étape intermédiaire correcte | `14/12` (Q1), `(2x+1−3)(2x+1+3)` (Q3) |
| 🔴 `fausse` | Autre chose | `11/6` |

**Le statut `partielle` est indispensable** : sans lui, une erreur de forme est
traitée comme une erreur de concept, et l'exercice recommandé serait le mauvais.

---

## 7. Traçabilité

Chaque question doit être traçable vers :

| Élément | Valeur |
|---|---|
| Identifiant | `ORIG-M3-Q01` … `ORIG-M3-Q05` |
| Objectif opérationnel | `OO-L1-1`, `OO-L5-1`… (⚠️ déduit, non officiel) |
| Leçon | `LEC-CM-MATH-3E-2025-2026-01`, `-03`, `-05`, `-08` |
| Origine du contenu | **Originale** — `origine: "originale"`, `source_bepc: null` |
| Statut de validation | `validation: "en_attente"` |
| Auteur / relecteur | À renseigner avant mise en production |

**Règle d'or** : aucune question ne porte `source_bepc` renseigné tant que les
droits ne sont pas établis. Ce contrôle doit être automatisé — il est trop
facile d'en copier une par inadvertance.

---

## 8. Ce que la mini-évaluation ne doit jamais produire

| Interdit | Raison |
|---|---|
| ❌ Un score en pourcentage (« vous avez 60 % ») | 5 items ne mesurent pas un niveau ; le score donne une fausse précision |
| ❌ Une mention de niveau (« niveau 3/5 ») | Idem |
| ❌ Une conclusion sur une leçon non testée | 10 des 14 leçons ne sont pas couvertes |
| ❌ Le mot « diagnostic » sans réserve | C'est une **hypothèse**, pas un bilan |
| ❌ Une conclusion de type « vous ne savez pas X » sur 1 item | 1 item = hypothèse, pas fait établi |

**Formulation retenue pour l'élève** (à valider) :
> « D'après tes 5 premières réponses, nous avons une **première idée** de tes
> acquis. Pour la confirmer, on peut faire quelques questions de plus. »

Le terme « première idée » est délibéré : il signale la prudence sans décourager.

---

## 9. Hypothèses explicites

| # | Hypothèse | Si elle est fausse |
|---|---|---|
| H1 | Un élève de 3e est en mesure de saisir une expression algébrique sur téléphone | Le périmètre doit être réduit à des réponses fermées (QCM) — **ce qui dégrade fortement la valeur diagnostique** |
| H2 | 5 questions suffisent à déclencher un premier exercice pertinent | Il faut descendre à 3 questions et accepter un signal encore plus faible |
| H3 | Les objectifs opérationnels déduits correspondent au contenu réel des leçons 1, 3, 5, 8 | Les questions ciblent le mauvais contenu — **validation pédagogique requise** |
| H4 | Les élèves n'ont pas encore fait la densité du programme (mini-éval en début d'année) | L'interprétation des « acquis » est faussée dans un sens ou dans l'autre |

---

*Documents liés : `docs/matrice-couverture-competences.md`,
`docs/regles-recommandation-pedagogique.md`.*