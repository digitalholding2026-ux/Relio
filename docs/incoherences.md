# Liste des incohérences détectées

**Référentiel** : `REF-CM-FR-MATH-3E-2025-2026`
**Source** : `source-progression-maths-3e.jpg`

> **Aucune correction n'a été appliquée.** Les données du document source sont
> reproduites telles quelles. Les anomalies sont signalées ici pour arbitrage
> par le responsable pédagogique.

---

## Synthèse

| Réf. | Gravité | Anomalie | État |
|---|---|---|---|
| A-1 | **Majeure** | Colonne « Taux d'exécution » sur un dénominateur de 112 h, incompatible avec les 120 h annoncés | Signalée, non corrigée |
| A-2 | **Majeure** | La révision (8 h) dépasse la capacité d'une semaine (4 h) | Signalée, non corrigée |
| A-3 | Mineure | Le total par trimestre ne correspond pas au rythme de 4 h/semaine (écarts +1 / −3 / +2 h) | Signalée, non corrigée |
| A-4 | Mineure | Leçon 5 : 9 h sur deux semaines n'offrant que 8 h ; excédents sur leçons 6, 8 et 13 | Signalée, non corrigée |
| A-5 | Mineure | La grille de lignes du tableau diffère d'une colonne à l'autre | Signalée, non corrigée |
| A-6 | **Absente** | Aucune incohérence sur les 14 leçons, leurs intitulés et leurs volumes | — |

---

## A-1 — Dénominateur 112 h dans la colonne « Taux d'exécution »

**Constat.** Le document comporte une colonne « Taux d'exécution » dont les
valeurs sont exprimées en pourcentage d'un total de **112 h**, et non de 120 h.
La dernière entrée vaut `100 % (112/112)`, atteinte avant la ligne « Révisions ».

Extrait de la colonne, dans l'ordre du document :

```
3,57 % (4/112)     6,25 % (7/112)     7,14 % (8/112)
10,71 % (12/112)   13,39 % (15/112)   14,28 % (16/112)
17,85 % (20/112)   20,53 % (23/112)   21,42 % (24/112)
25 % (28/112)      28,57 % (32/112)   31,25 % (35/112)
32,14 % (36/112)   35,71 % (40/112)   39,28 % (44/112)
40,17 % (45/112)   41,07 % (46/112)   42,85 % (48/112)
…                  …                   100 % (112/112)
```

**Analyse.**

- L'en-tête annonce 120 h ; le dénominateur est 112 h. Écart de 8 h.
- 112 h ne correspond ni aux 120 h annoncés, ni à la somme des éléments
  transcrits (98 h de leçons + 14 h de régulation + 8 h de révisions = 120 h),
  ni à 98 + 14 = 112… ce dernier point est à noter : **112 h = 98 h de leçons
  + 14 h de régulation, soit le total hors révisions**.
- La granularité de cette colonne ne correspond pas à la grille hebdomadaire :
  elle comporte environ 47 entrées pour 30 semaines, avec des pas de 1, 3 et 4 h.

**Hypothèses possibles (non retenues).**

1. La colonne aurait été produite sur une version antérieure du programme
   (28 semaines × 4 h = 112 h) et n'aurait pas été mise à jour.
2. La colonne exclurait volontairement les 8 h de révisions.

**Traitement.** La colonne « Taux d'exécution » est **exclue du référentiel**.
Elle n'est ni transcrite ni utilisée comme source de vérité, et ne doit pas être
propagée au back-office. **À arbitrer** par le responsable pédagogique.

---

## A-2 — La révision dépasse la capacité hebdomadaire

**Constat.** La période « Révisions » est libellée 8 h et placée sur la semaine
S30. Le rythme annoncé est de 4 h par semaine. Une seule semaine ne peut donc
pas accueillir 8 h : **dépassement de 4 h**.

**Hypothèse la plus économique (NON APPLIQUÉE).** Que les révisions s'étalent
sur S29 et S30 (4 h + 4 h). Cela rendrait la grille parfaitement régulière et
absorberait au passage l'excédent de capacité de la leçon 5 (A-4).

**Traitement.** La donnée est conservée telle quelle : 8 h, semaine S30.
Le moteur pédagogique devra traiter ce dépassement lors de la planification.

---

## A-3 — Écarts entre volume placé et capacité trimestrielle

**Constat.**

| Trimestre | Volume placé | Capacité (sem. × 4 h) | Écart |
|---|---|---|---|
| 1er | 45 h | 44 h | +1 h |
| 2e | 37 h | 40 h | −3 h |
| 3e | 38 h | 36 h | +2 h |
| **Total** | **120 h** | **120 h** | **0** |

Le total annuel est **exact**. Seule la répartition trimestrielle dévie.

**Traitement.** Signalé. Le total annuel, seul exigé par le document, est conforme.

---

## A-4 — Placement des leçons par rapport à la capacité hebdomadaire

**Constat.** Le document donne un volume par leçon mais **ne ventile pas** les
heures de chaque leçon entre les semaines qu'elle couvre. On ne peut donc pas
vérifier le placement semaine par semaine ; le contrôle de faisabilité révèle :

| Leçon | Volume | Semaines | Capacité dispo | Écart |
|---|---|---|---|---|
| L5 Calcul numérique | 9 h | S10–S11 | 8 h | **−1 h** |
| L6 Angles inscrits | 5 h | S12–S13 | 6 h | +1 h |
| L8 Équations et inéquations dans ℝ | 5 h | S16–S17 | 7 h | +2 h |
| L13 Applications affines | 5 h | S26–S27 | 7 h | +2 h |

Les excédents et le déficit se compensent (−1 + 1 + 2 + 2 = +4 h de capacité
non utilisée), ce qui est cohérent avec le placement des révisions (A-2).

**Traitement.** Signalé. Aucune ventilation horaire n'a été inventée : les seules
données relatives au placement sont les semaines de début et de fin.

---

## A-5 — Géométrie du tableau source non uniforme

**Constat.** Dans la photographie, les cellules de la colonne « Sem » et celles de
la colonne « Vol. hor. » ne reposent pas sur la même grille de lignes : une même
« ligne » visuelle peut correspondre à des cellules de hauteurs différentes selon
la colonne.

Conséquence : le rattachement d'une leçon à une semaine précise est une **lecture
croisée**, pas une donnée explicitement fournie par le document.

**Méthode retenue.** Recoupement de (a) la lecture visuelle haute résolution et
(b) la détection programmatique des lignes et des bandeaux gris de régulation
(valeur de remplissage 217, hauteur ~19 px), qui a permis de confirmer les
14 périodes de régulation aux semaines S2, S4, S6, S9, S12, S13, S15, S17, S19,
S21, S23, S24, S26 et S28.

**Traitement.** Le placement des leçons est marqué
`placement_semaines: "lecture_document_source_a_confirmer"` dans le JSON.

---

## A-6 — Contrôles sans anomalie

Les contrôles suivants ne révèlent **aucune** incohérence :

- les 14 leçons sont présentes, dans l'ordre 1→14, sans doublon ni trou ;
- les intitulés sont lisibles et ont été recopiés sans reformulation ;
- les volumes horaires sont tous strictement positifs ;
- la somme lessons + régulation + révision = **120 h**, exactement l'annoncé ;
- 30 semaines × 4 h = **120 h** ;
- les mois (9) et les trimestres (3) couvrent les 30 semaines sans recouvrement ;
- chaque semaine est rattachée au bon mois et au bon trimestre ;
- aucune référence orpheline entre entités ;
- aucune donnée pédagogique n'a été inventée.
