# Rapport de contrôle des données

**Référentiel** : `REF-CM-FR-MATH-3E-2025-2026`
**Document source** : `source-progression-maths-3e.jpg` — « Document de maths.jpg »
**Date du contrôle** : 2026-10-10
**Outil** : `outils/valider-referentiel.mjs` (Node.js, sans dépendance)
**Résultat** : **0 erreur bloquante · 3 réserves documentées**

---

## 1. Faits retranscrits

Éléments lus directement sur le document source. Aucune interprétation.

| # | Fait | Valeur |
|---|---|---|
| F-1 | Titre | MATHÉMATIQUES — PROGRESSION 3e — 2025-2026 |
| F-2 | Volume horaire annuel annoncé | 120 heures |
| F-3 | Rythme hebdomadaire annoncé | 4 heures par semaine |
| F-4 | Nombre de leçons | 14 |
| F-5 | Nombre de trimestres | 3 |
| F-6 | Dernière semaine numérotée | 30 |
| F-7 | Intitulés des 14 leçons | voir § 2 |
| F-8 | Volumes horaires des 14 leçons | voir § 2 |
| F-9 | Position des leçons (trimestre, mois, semaines) | voir § 2 |
| F-10 | Périodes de régulation | 14 périodes de 1 h |
| F-11 | Période de révision | « Révisions », 8 h |
| F-12 | Mention d'évaluation | « Devoir de niveau » (1er et 2e trimestre) |

### Méthode de transcription

Le document étant une photographie, la lecture a été croisée :

1. lecture visuelle des colonnes (recadrages haute résolution) ;
2. détection programmatique de la géométrie du tableau (lignes de séparation,
   bandeaux gris des cellules « Régulation », valeur de remplissage 217) ;
3. recoupement des deux méthodes.

Le volume horaire de chaque leçon, les intitulés et le nombre de périodes de
régulation sont **non ambigus**. Le placement semaine par semaine l'est moins :
la grille de lignes du tableau diffère selon les colonnes (voir réserve R-3).

---

## 2. Les 14 leçons

| # | Intitulé | Volume | Trim. | Semaines |
|---|---|---|---|---|
| 1 | Calcul littéral | 7 h | 1er | S1–S2 |
| 2 | Propriétés de Thalès dans un triangle | 7 h | 1er | S3–S4 |
| 3 | Racines carrées | 7 h | 1er | S5–S6 |
| 4 | Triangle rectangle | 11 h | 1er | S7–S9 |
| 5 | Calcul numérique | 9 h | 1er | S10–S11 |
| 6 | Angles inscrits | 5 h | 2e | S12–S13 |
| 7 | Vecteurs | 7 h | 2e | S14–S15 |
| 8 | Équations et inéquations dans ℝ | 5 h | 2e | S16–S17 |
| 9 | Coordonnées de vecteurs | 7 h | 2e | S18–S19 |
| 10 | Équations de droites | 7 h | 2e | S20–S21 |
| 11 | Statistique | 7 h | 3e | S22–S23 |
| 12 | Équations et inéquations dans ℝ × ℝ | 7 h | 3e | S24–S25 |
| 13 | Applications affines | 5 h | 3e | S26–S27 |
| 14 | Pyramides et cônes | 7 h | 3e | S28–S29 |
| | **Total** | **98 h** | | |

Aucun intitulé ni volume n'a été modifié, corrigé ou reformulé.
L'intitulé 12 conserve l'espacement `ℝ × ℝ` du document.

---

## 3. Calculs de contrôle

### 3.1 Somme des volumes horaires

| Poste | Détail | Total |
|---|---|---|
| Leçons | 7+7+7+11+9+5+7+5+7+7+7+7+5+7 | **98 h** |
| Régulation | 14 × 1 h | **14 h** |
| Révision | 8 h | **8 h** |
| **Somme** | | **120 h** |

**→ Conforme aux 120 h annoncés (F-2).**

### 3.2 Cohérence avec le rythme hebdomadaire

30 semaines × 4 h = **120 h** — cohérent avec l'annonce.

### 3.3 Volume par trimestre

| Trimestre | Leçons | Régul. | Révision | Total | Capacité (sem. × 4 h) | Écart |
|---|---|---|---|---|---|---|
| 1er | 41 h | 4 h | — | 45 h | 44 h | **+1 h** |
| 2e | 31 h | 6 h | — | 37 h | 40 h | **−3 h** |
| 3e | 26 h | 4 h | 8 h | 38 h | 36 h | **+2 h** |
| **Total** | 98 h | 14 h | 8 h | **120 h** | 120 h | **0** |

**→ Le total annuel est exact ; les écarts par trimestre se compensent.**
Voir réserve R-2.

### 3.4 Contrôles structurels

| Contrôle | Résultat |
|---|---|
| 14 leçons présentes | conforme |
| Ordre des rangs 1→14, sans trou ni doublon | conforme |
| Intitulé non vide pour chaque leçon | conforme |
| Volume horaire strictement positif | conforme |
| Identifiants uniques sur toutes les entités | conforme |
| Aucun identifiant dérivé d'un intitulé | conforme |
| Aucune référence orpheline (semaines ↔ mois ↔ trimestres ↔ leçons ↔ périodes) | conforme |
| 30 semaines numérotées 1→30 sans trou | conforme |
| Mois couvrant les 30 semaines sans recouvrement | conforme |
| Trimestres couvrant les 30 semaines sans recouvrement | conforme |
| Rattachement semaine → mois et → trimestre correct | conforme |
| Somme des volumes par trimestre = total annuel | conforme |
| Total = 120 h annoncés | conforme |
| 14 périodes de régulation présentes, toutes > 0 | conforme |
| 1 période de révision présente, > 0 | conforme |
| Toutes les leçons et régulations présentes dans la séquence | conforme |
| Révision positionnée sur la dernière semaine | conforme |
| Champs d'extension présents et vides | conforme |
| **Aucune compétence / prérequis / exercice / corrigé inventé** | conforme |

---

## 4. Réserves

| Réf. | Réserve | Impact | Traitement |
|---|---|---|---|
| **R-1** | La révision porte 8 h alors qu'une semaine n'en compte que 4 h. Dépassement de 4 h. | Bloquant pour un moteur qui.planifie semaine par semaine | **Non corrigé.** Documenté. |
| **R-2** | Le placement semaine par semaine n'est pas entièrement réconciliable : L5 « Calcul numérique » (9 h) sur S10–S11 qui n'offrent que 8 h ; excédent de 1 h sur L6, 2 h sur L8, 2 h sur L13. | Faible — les volumes annuels et par trimestre sont exacts | **Non corrigé.** Documenté. |
| **R-3** | La grille de lignes du tableau source diffère d'une colonne à l'autre (les cellules « Sem » et les cellules « Vol. hor. » ne s'alignent pas). Le placement des leçons sur les semaines est donc une lecture, pas une donnée explicite. | Moyen — à confirmer par le responsable pédagogique | **Non corrigé.** Documenté. |

---

## 5. Points restant à confirmer

Ces points ne peuvent pas être tranchés à partir du document seul. Ils sont
laissés en l'état, sans correction silencieuse.

1. **La révision couvre-t-elle S29–S30 ou S30 seule ?** Les 8 h
   s'étaleraient sur les deux dernières semaines, ce qui rendrait la grille
   parfaitement régulière (S29 : 4 h + S30 : 4 h). C'est l'hypothèse la plus
   économique, mais elle **n'a pas été appliquée**.
2. **La colonne « Taux d'exécution » du document** utilise un dénominateur de
   **112 h** et atteint 100 % à `(112/112)`, alors que l'en-tête annonce 120 h.
   Cette colonne est **exclue du référentiel** : elle ne se réconcilie ni avec
   les 120 h annoncés, ni avec la somme des éléments transcrits. Voir
   [incohérences](incoherences.md).
3. **Le « Devoir de niveau »** est mentionné pour les 1er et 2e trimestres
   uniquement. Rien n'est indiqué pour le 3e. Ne rien supposer.
4. **Le découpage horaire intra-semaine** (quelles heures pour quelles leçons
   dans une même semaine) n'est pas fourni par la source.

---

## 6. Conformité aux critères d'acceptation

| Critère | État |
|---|---|
| Les 14 leçons sont présentes et correctement ordonnées | **Conforme** |
| Aucun intitulé ni volume modifié silencieusement | **Conforme** — intitulés recopiés à l'identique |
| Les périodes de régulation et de révision sont représentées | **Conforme** — 14 régulations + 1 révision |
| Les contrôles de cohérence sont documentés | **Conforme** — § 3, reproductible via le validateur |
| Les données sont réutilisables par le futur moteur pédagogique | **Conforme** — identifiants stables, séquence ordonnée, champs d'extension en place |
| Le rapport distingue faits / calculs / points à confirmer | **Conforme** — § 1, § 3, § 5 |

## 7. Conclusion

Le référentiel est **exploitable en l'état** pour un back-office de consultation
et pour la préparation du moteur pédagogique, sous réserve de traiter R-1 et R-2
lors de la planification.

Il **n'est pas déclaré « validé »** : le statut retenu est `valide_avec_reserves`,
conformément à la contrainte de ne pas considérer les données comme officiellement
validées tant que leur conformité n'a pas été vérifiée — ici elle l'est sur les
volumes, mais pas sur le placement horaire intra-semaine.

**Décision attendue du responsable pédagogique** sur les points du § 5.
