# Anomalies, ambiguïtés et incertitudes — Documents BEPC 2025-2026

**Analyse** : `data/inventaire-questions-bepc-2025-2026.json`
**Documents** : sujets et corrigés harmonisés BEPC Mathématiques, sessions 2025 et 2026

> **Aucune anomalie n'a été corrigée dans les documents sources.** Elles sont
> signalées ici. Les données produites distinguent explicitement ce qui est
> établi par les documents de ce qui est un choix de l'analyste.

---

## 1. Tableau de synthèse

| Réf. | Gravité | Objet | Type |
|---|---|---|---|
| **D-1** | 🔴 **Bloquante** | Droits d'utilisation non vérifiés | Juridique |
| **D-2** | 🟠 **Majeure** | Sujet 2025 T2 / corrigé : divergence savon-huile, aucune solution | Divergence |
| **D-3** | 🟡 Moyenne | Corrigé 2026 : Q(x) au numérateur inutilisé | Divergence |
| **D-4** | 🟢 Mineure | Corrigé 2026 : « 62,66 » pour 1880/30 | Divergence |
| **D-5** | 🟡 Moyenne | Le cylindre ne relève pas de l'intitulé de la leçon 14 | Association |
| **D-6** | 🟡 Moyenne | 8 associations de leçons incertaines | Incertitude |
| **D-7** | 🟡 Moyenne | OCR peu fiable sur les expressions mathématiques | Méthode |
| **D-8** | 🟢 Mineure | Intitulé « Exercice 1 » non unique dans une session | Modélisation |
| **D-9** | 🟢 Mineure | Leçon 6 non observée dans les deux sessions | Constat |

---

## D-1 — Droits d'utilisation non vérifiés 🔴

**Constat.** Les quatre documents sont des publications de la **Direction des
Examens, des Concours et de la Certification de la République du Cameroun**,
signées par le Président du Jury d'harmonisation. Leur statut de droit n'a
pas été vérifié : le dépôt GitHub ne contient aucune mention de licence.

**Risque.** La mission interdit de republier les sujets, figures et corrigés
avant vérification des droits. Or ces documents sont précisément le matériau
pédagogique le plus attractif pour l'application.

**Ce qui est établi.** L'analyse interne (correspondance questions ↔ leçons,
identification des notions récurrentes) **n'implique aucune reproduction** et
peut se poursuivre.

**Ce qui est bloqué.** Toute reproduction, totale ou partielle, d'énoncés, de
figures, de barèmes ou de corrigés dans une application distribuée.

**Action requise.** Vérifier auprès du Ministère des Enseignements Secondaires
les conditions de réutilisation, notamment : usage commercial, reproduction
numérique, citation, et durée de l'autorisation.

---

## D-2 — Divergence sujet / corrigé 2025, tâche 2 🟠

**Constat.**

Le **sujet 2025** (tâche 2) écrit, sans ambiguïté :

> « Les dons en nature constitués de sacs de riz et de **cartons d'huile** ont
> été achetés en deux temps chez le même vendeur : 1er temps, 3 sacs de riz et
> 2 cartons d'huile pour 146 000 FCFA ; 2ème temps, 2 sacs de riz et 2 cartons
> d'huile pour 111 000 FCFA. Combien ont coûté un sac de riz et un carton
> d'huile ? »

Le **corrigé 2025** écrit :

> « Tâche 2 : Déterminons le coût d'un sac de riz et d'un **carton de savon**.
> **N.B : Compte tenu de la présence dans le libellé de la tâche 2 d'une
> coquille faisant allusion à un carton de savon au lieu d'un carton d'huile,
> ce qui est de nature à perturber les candidats, attribuer 2,25 pts à tout
> candidat présent.** »

**Analyse.** Le corrigé évoque une coquille dans un énoncé qui, dans la version
numérisée dont nous disposons, ne présente **pas** cette coquille. Deux lectures
sont possibles, et **aucune n'est confirmée** :

1. le sujet numérisé est une version **corrigée** postérieure à celle visée par
   le corrigé harmonisé ;
2. le corrigé a été rédigé sur une autre version du sujet.

**Point critique.** Le corrigé **ne publie aucune solution** pour cette tâche :
il annule la question et attribue les points. Il est donc impossible de
transcrire un résultat de référence.

**Traitement appliqué.** Dans l'inventaire :
- `resultat_attendu` = `null` ;
- `resultat_non_publie` = `true` ;
- `methode` = « NON PUBLIÉE » ;
- `divergence_signalee` décrit la situation en détail.

**Aucun résultat n'a été calculé de notre côté.** Le système
3r + 2h = 146 000 et 2r + 2h = 111 000 admet une solution, mais elle ne
figure dans aucune source et n'a donc pas été retenue.

> ⚠️ **Point d'attention pour le moteur pédagogique.** Une correction
> automatique de cette question produirait un résultat que **le jury national
> n'a jamais validé**. Cette question doit être traitée comme non corrigible
> tant que la situation n'est pas tranchée.

---

## D-3 — Corrigé 2026 : Q(x) au numérateur inutilisé 🟡

**Constat.** Le sujet 2026, exercice 3, question 3, définit :

```
Q(x) = (3x − 7)(2x + 1) / ((4x − 5)(7x + 6))
```

où P(x) = 16x² − 25 + (4x − 5)(3x + 1) a été factorisé en (4x − 5)(7x + 6).

Les questions posées portent **exclusivement sur le dénominateur** :

- a) « Résous dans ℝ l'équation (4x − 5)(7x + 6) = 0 »
- b) « Déduis-en la condition d'existence d'une valeur numérique de Q »

Le numérateur (3x − 7)(2x + 1) n'est donc **jamais utilisé**, et ne
correspond pas aux facteurs de P(x).

**Lectures possibles, aucune confirmée.** Le numérateur peut être un
leurre volontaire (tester si l'élève distingue ce qui intervient dans la
condition d'existence), ou une coquille.

**Traitement.** Signalé, non corrigé. Les réponses retenues (x = 5/4 et
x = −6/7) ne dépendent que du dénominateur et sont donc robustes quelle que
soit l'explication.

---

## D-4 — Corrigé 2026 : arrondi de la moyenne 🟢

**Constat.** Le corrigé écrit « 1880/30 ≈ **62,66** ».

1880 ÷ 30 = 62,6666… L'arrondi à la deuxième décimale donnerait 62,67.

**Impact nul.** La question demande un arrondi à l'unité supérieure : 63 kg
dans les deux cas. Le barème (0,5 pt pour « 62,66 » et 0,5 pt pour « 63 »)
reproduit la valeur du corrigé.

**Traitement.** Écart signalé dans le champ `divergence_signalee` de la
question. La valeur « 62,66 » est celle du corrigé, reproduite telle quelle.

---

## D-5 — Le cylindre hors intitulé de la leçon 14 🟡

**Constat.** Le sujet 2026, tâche 2, porte sur un **cylindre** (aire latérale
et aire d'une base). La leçon correspondante du référentiel annuel s'intitule
« **Pyramides et cônes** » (L14) et ne mentionne pas le cylindre.

Le rattachement de cette question à L14 repose donc sur une proximité
thématique, non sur une correspondance d'intitulé.

**Traitement.** Association maintenue avec le marqueur
`confiance: "confirme"` pour le bloc solide, mais le caractère couvrant est
explicitement documenté dans `docs/couverture-programme-bepc.md` (L14).

**Décision attendue.** Faut-il étendre la leçon 14 au cylindre, ou rattacher
cette question à une leçon distincte ? Cela touche au référentiel annuel et
**n'a pas été fait**.

---

## D-6 — Associations de leçons incertaines 🟡

**Constat.** Sur 49 associations question ↔ leçon, **8 sont incertaines**.

| Question | Leçon | Motif de l'incertitude |
|---|---|---|
| `BEPC-2025-A-NUM-EX1-1` | L1 Calcul littéral | Question de calcul fractionnaire ; rattachement au littéral par extension |
| `BEPC-2026-A-NUM-EX1-1` | L1 Calcul littéral | idem |
| `BEPC-2025-A-NUM-EX1-2c` | L5 Calcul numérique | Rationalisation rattachée au calcul numérique par extension |
| `BEPC-2025-A-GEO-EX1-1` | L7 Vecteurs | Orthogonalité de droites rattachée aux vecteurs |
| `BEPC-2025-A-GEO-EX1-2` | L9 Coordonnées de vecteurs | Colinéarité rattachée aux coordonnées de vecteurs |
| `BEPC-2026-A-GEO-EX2-1` | L7 Vecteurs | Placement dans un repère rattaché aux vecteurs |
| `BEPC-2025-B-T3` | L13 Applications affines | Comparaison de forfaits modélisée par des fonctions affines |
| `BEPC-2026-B-T2` | L5 Calcul numérique | Conversion cm² → m² rattachée au calcul numérique |

**Point rassurant.** Dans les 8 cas, l'association **principale** est confirmée :
l'incertitude porte uniquement sur le rattachement secondaire.

**Traitement.** Chaque association porte un champ `confiance` explicite
(`confirme` ou `incertain`). Aucune n'a été présentée comme certaine.

---

## D-7 — Fiabilité de l'OCR sur les expressions mathématiques 🟡

**Constat.** Les deux corrigés sont des numérisations sans couche texte. L'OCR
(Tesseract 5.5.0, modèle français) s'est révélé **inexploitable seul** sur les
expressions mathématiques.

Erreurs relevées et corrigées par relecture visuelle :

| Document | Sortie OCR | Valeur vérifiée sur l'image |
|---|---|---|
| Sujet 2025, QCM développé | `c)` | **`d)`** : 2x² + x − 28 |
| Sujet 2025, QCM factorisé | `b)` | **`b)`** : (x+4)(2x−7) — confirmé |
| Corrigé 2025, réponses QCM | `CR ET` / `DR ET` | **`1. d)`** et **`2. b)`** |
| Sujet 2026, consigne numérique | « Prendre **1 l** = 3,14 » | « Prendre **π** = 3,14 » |
| Sujet 2026, tableau de poids | `5; l 68° 652 1 6: 79° 11 1 1` | 55/60/62/65/70 ; 6/8/5/2/9 |
| Corrigé 2026, exercice 1 | « Écrivons le nombre **4** » | « Écrivons le nombre **A** » |
| Corrigé 2025, page 3 | illisible | 2ᵉ option : 10 000 + 1 000x |

Le corrigé 2026 était en outre **pivoté à 90°** : sans rotation préalable,
l'OCR produisait un texte entièrement illisible.

**Traitement appliqué.** L'OCR a servi uniquement à **localiser** les contenus.
**Chaque valeur retenue dans l'inventaire a été vérifiée visuellement sur
l'image du document.** Les tableaux, expressions et barèmes ont été relus à
partir des pages rendues.

**Limite assumée.** Cette relecture a été exhaustive pour les données
numériques et les résultats, mais **pas pour chaque mot des énoncés**. Les
énoncés ont été retranscrits à partir des sujets — dont la couche texte est
fiable — et recoupés visuellement pour les passages contenant des expressions.

---

## D-8 — Intitulé d'exercice non unique 🟢

**Constat.** Dans une même session, le libellé « Exercice 1 » désigne à la fois
un exercice d'**activités numériques** et un exercice d'**activités
géométriques**. Le libellé seul n'identifie donc pas un exercice.

**Impact constaté pendant l'analyse.** Ce point a produit une **fausse
association** lors d'un premier traitement automatisé : la question
`BEPC-2025-A-NUM-EX1-2a` a été rattachée à une question mère « 2 » qui était en
réalité l'exercice de géométrie.

**Traitement.** Un identifiant non ambigu a été ajouté
(`exercice_id`, format `2025-NUM-EX01`) et le rattachement des sous-questions
utilise désormais le couple session + bloc + exercice. L'anomalie a été
détectée par le validateur puis corrigée.

---

## D-9 — Leçon 6 « Angles inscrits » non observée 🟢

**Constat.** Aucune des 35 questions des sessions 2025 et 2026 ne se rattache à
la leçon 6 « Angles inscrits » (5 h au programme).

**Analyse.** Les deux sujets font apparaître des configurations géométriques
mais **aucune configuration circulaire** : triangle rectangle (2025 et 2026),
pyramide à base carrée, Thalès dans un triangle. La notion d'angle inscrit dans
un cercle n'apparaît pas explicitement.

**Ce que cela ne dit pas.** Deux sessions ne permettent pas de conclure que la
leçon 6 n'est pas évaluée. Le jury national peut l'inclure dans une session
ultérieure, ou l'aborder par un énoncé que cette analyse n'a pas su identifier.

**Traitement.** Constat consigné, aucune conclusion tirée.

---

## Pages et figures — état de lisibilité

| Document | Pages attendues | Pages lues | Figures |
|---|---|---|---|
| Sujet 2025 | 2 | **2 / 2** | Triangle non figuré (décrit) ; pyramide non figurée |
| Corrigé 2025 | 3 | **3 / 3** | Figures non reproduites dans le corrigé |
| Sujet 2026 | 2 | **2 / 2** | Repère orthonormé figuré ; triangle ABC **figuré** (« 2 cm », 30°) |
| Corrigé 2026 | 4 | **4 / 4** | Repère orthonormé figuré (avec points placés) |

**Aucune page manquante.** Toutes les pages annoncées par les documents ont été
lues.

**Figures.** Une seule figure informative a été exploitée : le triangle ABC du
sujet 2026, qui porte les indications « 2 cm » et 30°. Le tableau de statistiques
de la session 2026 a été intégralement relu (poids et effectifs). Les autres
figures sont des repères ou des solides décrits en texte, sans apport de donnée
supplémentaire.

**Aucune figure n'a été extraite ni reproduite** dans les livrables, pour
raisons de droits (D-1).

---

## Récapitulatif des décisions en attente

| # | Décision | Responsable | Bloque |
|---|---|---|---|
| 1 | Droits de réutilisation des sujets et corrigés | Juridique / Ministère | Publication de tout contenu |
| 2 | Traitement de la tâche 2 de 2025 sans solution de référence | Pédagogique | Génération de corrigé |
| 3 | Rattachement du cylindre 2026 à la leçon 14 | Pédagogique | Complétude du référentiel |
| 4 | Renforcement de la leçon 6 malgré son absence observée | Pédagogique | Planification des révisions |
| 5 | Validation humaine de l'inventaire avant publication | Pédagogique | Mise en production |
