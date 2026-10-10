# Analyse pédagogique des épreuves harmonisées BEPC 2025 et 2026 — Mathématiques

**Pays** : Cameroun · **Classe** : 3e · **Examen** : BEPC
**Sessions analysées** : 2025 et 2026
**Référentiel annuel de rattachement** : `REF-CM-FR-MATH-3E-2025-2026`
**Statut** : `analyse_provisoire_en_attente_de_validation_humaine`

> ⚠️ **Avertissement de portée.** Ces deux sessions ne représentent **PAS** la
> totalité du programme annuel. Elles portent sur **35 questions** et couvrent
> **13 des 14 leçons**. L'absence d'une notion dans ces sujets ne signifie ni
> qu'elle est absente du programme, ni qu'elle n'est pas évaluée au BEPC.

> 🔒 **Droits d'utilisation non vérifiés.** Sujets, figures et corrigés
> harmonisés sont publiés par la Direction des Examens, des Concours et de la
> Certification du Cameroun. Voir `docs/anomalies-documents-bepc.md`, point D-1.

---

## 1. Documents analysés

Les 4 documents ont été retrouvés dans le dépôt et sont **intégralement lisibles**.

| Session | Document | Fichier | Pages | Lisibilité |
|---|---|---|---|---|
| 2025 | Sujet | `BEPC 04 juin 2025.pdf` | 2 | Texte extractible |
| 2025 | Corrigé harmonisé national | `BEPC-MATHS-CORRIGE-2025.pdf` | 3 | **Numérisé** — rendu lisible par OCR |
| 2026 | Sujet | `BEPC 2026.pdf` | 2 | Texte extractible |
| 2026 | Corrigé harmonisé national | `bepc 2026 corriger.pdf` | 4 | **Numérisé et pivoté à 90°** — rendu lisible par OCR |

**Complétude** : 4 pages de sujets (2 + 2) et 7 pages de corrigés (3 + 4), soit
**11/11 pages lues**, sans page manquante. Les deux corrigés sont signés et datés
(Rose Eliane Lucien Douala, Président du Jury d'harmonisation — PLEG HE-IPN/MATHS ;
04/06/2025 et 03/06/2026).

### Traitement technique des corrigés

Les deux corrigés n'avaient **aucune couche texte** : ils sont des numérisations.
Ils ont été rendus lisibles par `pdftoppm` (300 dpi, niveaux de gris) puis
**Tesseract 5.5.0, modèle français**. Les pages du corrigé 2026 étant pivotées
à 90°, une rotation a été appliquée avant reconnaissance.

**L'OCR n'a pas été utilisé comme source de vérité.** Chaque valeur retenue a
été **vérifiée visuellement sur l'image**, car la reconnaissance automatique
s'est révélée défaillante sur les expressions mathématiques. Exemples concrets
d'erreurs OCR corrigées par relecture visuelle :

| Élément | Sortie OCR | Valeur réelle lue sur l'image |
|---|---|---|
| Sujet 2025, QCM E développé | `c)` | **`d)`** : 2x² + x − 28 |
| Sujet 2026, consigne | « Prendre **1 l** = 3,14 » | « Prendre **π** = 3,14 » |
| Sujet 2026, tableau de stats | `5; l 68° 652 1 6: 79° 11 1 1` | poids 55/60/62/65/70 ; effectifs 6/8/5/2/9 |
| Corrigé 2025, QCM | `CR ET` / `DR ET` | **`1. d)`** et **`2. b)`** |

---

## 2. Vue d'ensemble quantitative

| | 2025 | 2026 | Total |
|---|---|---|---|
| Questions inventoriées | 17 | 18 | **35** |
| Exercices et tâches | 9 | 9 | 18 |
| Partie A — ressources | 12,5 pt | 15 pt | — |
| Partie B — compétences | 7,5 pt | 5 pt | — |
| **Total barème** | **20 pt** | **20 pt** | — |

Les barèmes se recomptent **exactement** à partir des questions inventoriées et
concordent avec les totaux annoncés par les documents sources.

---

## 3. Analyse des sujets par notion

### Session 2025

**Partie A — Évaluation des ressources (12,5 pt)**

*Activités numériques (6,25 pt)*

| # | Question | Barème | Notion | Leçons | Résultat attendu |
|---|---|---|---|---|---|
| N1.1 | A = (3/2 + 5/4) × (3/2 − 5/4), fraction irréductible | 1 pt | Fractions, priorités | L5, L1 | **11/16** |
| N1.2a | B = (3√2 − 4)² sous forme a + b√2 | 0,75 pt | Calcul littéral, racines | L1, L3 | **34 − 24√2** |
| N1.2b | C = (3√2−4)(3√2+4) est un entier | 0,75 pt | Identité remarquable | L3, L1 | **C = 2** |
| N1.2c | D = (3√2−4)/(3√2+4) sans radical au dénominateur | 0,75 pt | Rationalisation | L3, L5 | **17 − 12√2** |
| N2.1 | Forme développée de E (QCM) | 1 pt | Calcul littéral | L1 | **d)** 2x² + x − 28 |
| N2.2 | Forme factorisée de E (QCM) | 1 pt | Factorisation | L1 | **b)** (x+4)(2x−7) |
| N2.3a | Condition d'existence de Q | 0,5 pt | Fraction rationnelle | L1 | **x ≠ −4 et x ≠ −7/2** |
| N2.3b | Simplifier Q | 0,5 pt | Simplification | L1 | **(2x−7)/(2x+7)** |

*Activités géométriques (6,25 pt)*

| # | Question | Barème | Notion | Leçons | Résultat attendu |
|---|---|---|---|---|---|
| G1.1 | (D) et (L) sont-elles perpendiculaires ? | 1 pt | Pente, orthogonalité | L10, L7 | **Faux** (2 × ½ = 1 ≠ −1) |
| G1.2 | u(−2;5) et v(5;2) sont-ils colinéaires ? | 1 pt | Colinéarité | L7, L9 | **Faux** (déterminant −29) |
| G2.1 | ABC rectangle en B, AB = 6, BC = 8 → AC | 1,25 pt | Pythagore | L4 | **10 cm** |
| G2.2 | tan(BAC) et mesure de l'angle | 1 pt | Tangente | L4 | **4/3 ; ≈ 53°** |
| G3 | Volume d'une pyramide à base carrée | 2 pt | Volume pyramide | L14 | **192 cm³** |

*Partie B — Évaluation des compétences (7,5 pt)*

| Tâche | Situation | Barème | Leçons | Résultat |
|---|---|---|---|---|
| T1 | Budget d'un orphelinat,il manque 100 000 FCFA | 2,25 pt | L8 | **3 000 000 FCFA** |
| T2 | Achats de riz et d'huile (système 2×2) | 2,25 pt | L12 | **non publié par le corrigé** |
| T3 | Comparaison de deux forfaits de transport | 2,25 pt | L8, L13 | **x > 5, soit 6 heures** |
| — | Présentation | 0,75 pt | — | 0,5 lisibilité + 0,25 orthographe |

### Session 2026

**Partie A — Évaluation des ressources (15 pt)**

*Activités numériques (7,5 pt)*

| # | Question | Barème | Notion | Leçons | Résultat attendu |
|---|---|---|---|---|---|
| N1.1 | A = 7/5 − (3/8)×(16/7) + 2/35, fraction irréductible | 1 pt | Fractions, priorités | L5, L1 | **3/5** |
| N1.2 | B = −5√128 + 3√72 − 7√32 sous forme a√2 | 1 pt | Réduction de radicaux | L3, L5 | **−50√2** |
| N2 | Poids moyen de 30 passagers | 2 pt | **Statistique** | L11 | **1880/30 ≈ 62,66 → 63 kg** |
| N3.1 | Développer et ordonner P(x) | 1 pt | Calcul littéral | L1 | **28x² − 11x − 30** |
| N3.2 | Factoriser P(x) | 1 pt | Différence de carrés | L1 | **(4x−5)(7x+6)** |
| N3.3a | Résoudre (4x−5)(7x+6) = 0 | 0,75 pt | Équation produit | L8 | **S = {5/4 ; −6/7}** |
| N3.3b | Condition d'existence de Q | 0,75 pt | Domaine de définition | L1, L8 | **x ≠ 5/4 et x ≠ −6/7** |

*Activités géométriques (7,5 pt)*

| # | Question | Barème | Notion | Leçons | Résultat |
|---|---|---|---|---|---|
| G1.1 | AB et BC (cos/sin 30°) | 2 pt | Triangle rectangle | L4 | **4√3 et 4** |
| G1.2 | Distance AF par Thalès | 1,25 pt | **Thalès** | L2 | **4√3/3** |
| G2.1 | Placer A, B, C dans le repère | 1 pt | Repère, coordonnées | L9, L7 | figure |
| G2.2 | Coordonnées de BA et BC | 1 pt | Coordonnées de vecteur | L9 | **(3;5) et (−5;7)** |
| G2.3 | Équation de (L) perpendiculaire à (BC) | 1 pt | Équation de droite | L10, L9 | **−5x + 7y + 18 = 0** |
| G2.4 | D(0;8) image de C par translation de BA | 0,75 pt | **Translation** | L9, L13 | **CD = BA** |
| G2.5 | Nature du quadrilatère ABCD | 0,5 pt | Parallélogramme | L13, L9 | **parallélogramme** |

*Partie B — Évaluation des compétences (5 pt)*

| Tâche | Situation | Barème | Leçons | Résultat |
|---|---|---|---|---|
| T1 | Prix riz et savon (système 2×2) | 1,5 pt | L12 | **21 500 et 18 000 FCFA** |
| T2 | Quantité de peinture pour un fût cylindrique | 1,5 pt | L14, L5 | **25 434 cm² → 0,25434 L** |
| T3 | Prix de 50 cornets (cône de révolution) | 1,5 pt | L14, L4 | **h = 12 ; 314 cm³ ; 7 850 FCFA** |
| — | Présentation | 0,5 pt | — | 0,5 lisibilité |

---

## 4. Analyse des corrigés harmonisés

Les corrigés apportent une information que les sujets ne donnent pas : une
**structure d'évaluation par critères** (C1 interprétation, C2 utilisation des
outils, C3 cohérence), et des **indicateurs de barème détaillés**question par question par
étape de raisonnement.

Structure observée :

| Session | Criteres employés | Niveaux d'indication |
|---|---|---|
| 2025 | C1, C2, C3 + Présentation | 0,25 pt le plus souvent ; C3 à 0,75 pt |
| 2026 | C1, C2, C3 + Présentation | idem |

Trois usages récurrents méritent d'être relevés pour le back-office :

1. **Tolérance de démarche.** Les deux corrigés portent la mention
   *« N.B : Apprécier toute autre démarche »* sur les exercices de numération.
   Le moteur pédagogique ne doit donc **pas** imposer une méthode unique.
2. **Tolérance d'arrondi.** Le corrigé 2026 accepte « toute valeur approchée
   de 4√3 ». Les résultats exacts ne sont pas exigés de façon stricte.
3. **Neutralisation d'une question.** Le corrigé 2025 annule la tâche 2 et
   accorde les points à tout candidat présent (voir § 6, D-2).

---

## 5. Ce que les deux sessions disent du programme

C'est le résultat le plus utile pour la préparation des élèves. Sur les 35
questions :

| Leçon du référentiel | Intitulé | Questions observées | Sessions |
|---|---|---|---|
| L1 | Calcul littéral | 11 | 2025, 2026 |
| L2 | Propriétés de Thalès dans un triangle | 1 | 2026 |
| L3 | Racines carrées | 4 | 2025, 2026 |
| L4 | Triangle rectangle | 4 | 2025, 2026 |
| L5 | Calcul numérique | 5 | 2025, 2026 |
| **L6** | **Angles inscrits** | **0** | **—** |
| L7 | Vecteurs | 3 | 2025, 2026 |
| L8 | Équations et inéquations dans ℝ | 4 | 2025, 2026 |
| L9 | Coordonnées de vecteurs | 6 | 2026 |
| L10 | Équations de droites | 2 | 2025, 2026 |
| L11 | Statistique | 1 | 2026 |
| L12 | Équations et inéquations dans ℝ × ℝ | 2 | 2025, 2026 |
| L13 | Applications affines | 3 | 2025, 2026 |
| L14 | Pyramides et cônes | 3 | 2025, 2026 |

### Trois enseignements

**Le calcul littéral est le cœur de l'épreuve.** 11 des 35 questions y
renvoient, dans les deux sessions. C'est aussi la leçon la mieux ancrée au
programme, ce qui est cohérent.

**Les notions «acies » apparaissent progressivement.** Thalès et la
statistique n'apparaissent qu'en 2026 ; les applications affines (translation,
parallélisme) sont surtout illustrées par un enchaînement coordonnées →
translation → parallélogramme, qui constitue en soi une progression
pédagogique cohérente.

**La géométrie des volumes est stable.** Pyramide à base carrée (2025) puis
cylindre et cône de révolution (2026) : les trois solides correspondent à la
leçon 14, « Pyramides et cônes ». À noter que le cylindre du sujet 2026
n'est pas explicitement au programme de la leçon 14 — voir D-5.

---

## 6. Divergences et incertitudes

Détail complet dans `docs/anomalies-documents-bepc.md`. Synthèse :

| Réf. | Constat | Traitement |
|---|---|---|
| **D-1** | Droits d'utilisation des documents non vérifiés | **Bloquant pour une republication** |
| **D-2** | Sujet 2025 T2 et corrigé ne concordent pas sur « savon / huile », et le corrigé ne publie **aucune solution** | Résultat laissé `null`, signalé |
| **D-3** | Corrigé 2026 : Q(x) a un numérateur (3x−7)(2x+1) distinct de P(x), jamais utilisé | Signalé, non corrigé |
| **D-4** | Corrigé 2026 écrit « 62,66 » pour 1880/30 = 62,666… | Écart mineur, sans incidence |
| **D-5** | Le cylindre du sujet 2026 ne relève pas explicitement de la leçon 14 | Association signalée comme couvrant |
| **D-6** | 5 associations de leçons portent une confiance « incertain » | Listées dans le tableau de couverture |
| **D-7** | L'OCR des corrigés est peu fiable sur les expressions | Toutes les valeurs recontrôlées visuellement |

---

## 7. Ce qui n'a pas été fait, et pourquoi

- **Aucune compétence officielle n'a été créée.** Le champ
  `competence_officielle` est vide sur les 35 questions. Un référentiel de
  compétences du BEPC n'a pas été fourni ; en déduire une aurait été un
  jugement sans source.
- **Le référentiel annuel n'a pas été modifié.** Ses identifiants sont
  uniquement *référencés* depuis l'inventaire.
- **Aucun exercice n'a été reconstruit.** L'inventaire décrit des questions
  existantes, il n'en fabrique pas.
- **Aucune extension au-delà de 2025-2026.** Deux sessions ne permettent pas
  d'inférer une tendance pluriannuelle.
- **Aucune publication automatique.** Le statut reste
  `analyse_provisoire_en_attente_de_validation_humaine`.

---

## 8. Utilisation possible par le moteur pédagogique

Sans publier le contenu des documents, l'inventaire permet déjà :

1. **Cibler les révisions** : `couverture_par_lecon` donne, par identifiant de
   leçon du référentiel, les questions observées — donc les notions à retravailler.
2. **Repérer les angles morts** : la leçon 6 n'est pas observée ; c'est un
   signal pour le responsable pédagogique, pas une conclusion.
3. **Entraîner sur des thèmes récurrents** : le calcul littéral (11 questions)
   est le premier champ d'entraînement naturel.
4. **S'entraîner sur les formats** : QCM, vrai/faux, système 2×2, inéquation,
   tâches en situation — tous documentés avec leur barème.

**Prérequis bloquant** : aucune de ces utilisations ne peut déboucher sur la
**reproduction** d'énoncés, de figures ou de corrigés dans l'application tant
que les droits d'utilisation ne sont pas établis (D-1). L'inventaire est, en
l'état, un outil d'analyse interne.

---

*Documents complémentaires : `data/inventaire-questions-bepc-2025-2026.json` (données),
`docs/couverture-programme-bepc.md` (tableau de couverture détaillé),
`docs/anomalies-documents-bepc.md` (anomalies et incertitudes).*
