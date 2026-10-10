# Rapport final — Mission 2

**Mission** : analyse pédagogique des épreuves harmonisées BEPC 2025 et 2026 (Mathématiques, 3e, Cameroun)
**Date** : 2026-10-10
**Statut** : `analyse_provisoire_en_attente_de_validation_humaine`

---

## 1. Documents réellement trouvés et analysés

Les 4 documents ont été retrouvés dans le dépôt GitHub et sont **intégralement
lisibles**. Aucun document n'a été inventé ni supposé.

| Session | Document | Fichier | Pages | État |
|---|---|---|---|---|
| 2025 | Sujet | `BEPC 04 juin 2025.pdf` | 2 | Texte extractible |
| 2025 | Corrigé harmonisé national | `BEPC-MATHS-CORRIGE-2025.pdf` | 3 | Numérisé — OCR + relecture visuelle |
| 2026 | Sujet | `BEPC 2026.pdf` | 2 | Texte extractible |
| 2026 | Corrigé harmonisé national | `bepc 2026 corriger.pdf` | 4 | Numérisé, pivoté 90° — OCR + relecture visuelle |

**Complétude : 14 pages sur 14 lues** (7 de sujets, 7 de corrigés). Aucune page
manquante. Les deux corrigés sont signés et datés (Rose Eliane Lucien Douala,
Président du Jury d'harmonisation — PLEG HE-IPN/MATHS).

Les sujets portent la mention `sujetexa.com` en pied de page : ce sont des
documents tiers, dont la teneur éditoriale n'est pas garantie par l'administration.

---

## 2. Exercices et questions inventoriés

| | 2025 | 2026 | Total |
|---|---|---|---|
| Exercices et tâches | 9 | 9 | 18 |
| **Questions inventoriées** | **17** | **18** | **35** |

**Répartition par partie**

| | 2025 | 2026 |
|---|---|---|
| Partie A — évaluation des ressources | 12,5 pt (13 questions) | 15 pt (13 questions) |
| Partie B — évaluation des compétences | 7,5 pt (4 questions) | 5 pt (5 questions) |
| **Total** | **20 pt** | **20 pt** |

Le barème se **recompte exactement** à partir des 35 questions inventoriées et
concorde avec les totaux annoncés par les documents.

Pour chaque question ont été relevés : l'énoncé transcrit, les données
numériques, le caractère obligatoire ou non d'une figure, les notions
mobilisées, les leçons du référentiel, la méthode du corrigé, le résultat
attendu, les étapes de raisonnement, le barème du sujet et celui du corrigé,
et le degré de confiance de chaque association.

---

## 3. Leçons couvertes et non observées

**13 des 14 leçons** du référentiel annuel sont observées dans ces deux sessions.

| Leçon | Intitulé | Questions | Leçon | Intitulé | Questions |
|---|---|---|---|---|---|
| L1 | Calcul littéral | **11** | L8 | Équations et inéquations dans ℝ | 4 |
| L2 | Thalès dans un triangle | 1 | L9 | Coordonnées de vecteurs | 6 |
| L3 | Racines carrées | 4 | L10 | Équations de droites | 2 |
| L4 | Triangle rectangle | 4 | L11 | Statistique | 1 |
| L5 | Calcul numérique | 5 | L12 | Équations dans ℝ × ℝ | 2 |
| L7 | Vecteurs | 3 | L13 | Applications affines | 3 |
| | | | L14 | Pyramides et cônes | 3 |

**Leçon non observée : L6 « Angles inscrits » (5 h au programme).**
Aucune des 35 questions ne s'y rattache. Aucune des deux sessions ne présente
de configuration circulaire. Cela ne dit rien de sa place réelle dans
l'épreuve : deux sessions ne suffisent pas à conclure.

**Lecture d'ensemble.** Le calcul littéral domine très largement (11 questions
sur 35, dans les deux sessions). À l'inverse, deux leçons lourdes du programme
sont très peu présentes : la leçon 11 (Statistique, 7 h, **une seule** question)
et la leçon 6 (5 h, aucune).

Détail dans `docs/couverture-programme-bepc.md`.

---

## 4. Associations incertaines

**8 associations incertaines sur 49.**

| Question | Leçon | Motif |
|---|---|---|
| `BEPC-2025-A-NUM-EX1-1` | L1 | Calcul fractionnaire rattaché au littéral par extension |
| `BEPC-2026-A-NUM-EX1-1` | L1 | idem |
| `BEPC-2025-A-NUM-EX1-2c` | L5 | Rationalisation rattachée au calcul numérique par extension |
| `BEPC-2025-A-GEO-EX1-1` | L7 | Orthogonalité de droites rattachée aux vecteurs |
| `BEPC-2025-A-GEO-EX1-2` | L9 | Colinéarité rattachée aux coordonnées de vecteurs |
| `BEPC-2026-A-GEO-EX2-1` | L7 | Placement dans un repère rattaché aux vecteurs |
| `BEPC-2025-B-T3` | L13 | Comparaison de forfaits modélisée par des fonctions affines |
| `BEPC-2026-B-T2` | L5 | Conversion d'unités rattachée au calcul numérique |

**Dans les 8 cas, l'association principale est confirmée** : l'incertitude ne
porte que sur le rattachement secondaire. Aucune association incertaine n'est
présentée comme confirmée dans les livrables.

---

## 5. Erreurs et divergences détectées

| Réf. | Constat | Traitement |
|---|---|---|
| **D-1** 🔴 | **Droits d'utilisation des documents non vérifiés** | Bloquant pour toute republication |
| **D-2** 🟠 | **Sujet 2025 T2 / corrigé divergent** sur « savon / huile », et le corrigé ne publie **aucune solution** | Résultat laissé `null`, signalé |
| **D-3** 🟡 | Corrigé 2026 : Q(x) a un numérateur (3x−7)(2x+1) distinct de P(x), jamais utilisé | Signalé, non corrigé |
| **D-4** 🟢 | Corrigé 2026 écrit « 62,66 » pour 1880/30 = 62,666… | Sans incidence sur l'arrondi |
| **D-5** 🟡 | Le cylindre (sujet 2026) ne relève pas de l'intitulé « Pyramides et cônes » | Association signalée comme couvrant |
| **D-6** 🟡 | 8 associations incertaines sur 49 | Champ `confiance` explicite |
| **D-7** 🟡 | OCR peu fiable sur les expressions mathématiques | Toutes valeurs recontrôlées visuellement |
| **D-8** 🟢 | « Exercice 1 » non unique dans une session (numération **et** géométrie) | `exercice_id` non ambigu ajouté |
| **D-9** 🟢 | Leçon 6 non observée dans les deux sessions | Constat consigné |

### Trois points méritant attention particulière

**D-2 est le plus important.** Le corrigé harmonisé 2025 annule la tâche 2 et
attribue les 2,25 points à tout candidat présent, en invoquant une coquille qui
**n'existe pas** dans la version numérisée du sujet dont nous disposons. Conséquence
concrète : une correction automatique de cette question produirait un résultat
que le jury national n'a jamais validé. Le système admet bien une solution, mais
elle ne figure dans aucune source — **elle n'a donc pas été retenue**.

**D-7 a réellement failli produire des erreurs.** L'extraction automatique donnait
la réponse **c)** au QCM de 2025 alors que la bonne réponse est **d)**, et
interprétait « Prendre π = 3,14 » comme « Prendre 1 l = 3,14 ». Ces valeurs ont
été corrigées par relecture visuelle systématique. Le tableau de statistiques
2026, illisible en texte, a été relevé à l'image : poids 55/60/62/65/70,
effectifs 6/8/5/2/9, total 30 — ce qui **confirme** indépendamment le
1880/30 du corrigé.

**D-8 a été détecté par l'outillage, pas par la relecture.** Un premier
traitement rattachait à tort une question de numération à une question mère
appartenant à l'exercice de géométrie. Le validateur l'a signalé ; un
identifiant d'exercice non ambigu a été introduit.

---

## 6. Fichiers créés

| Fichier | Contenu |
|---|---|
| `data/inventaire-questions-bepc-2025-2026.json` | Inventaire structuré — 35 questions, sources, couverture par leçon |
| `docs/analyse-bepc-2025-2026.md` | Synthèse pédagogique |
| `docs/couverture-programme-bepc.md` | Tableau de couverture des 14 leçons |
| `docs/anomalies-documents-bepc.md` | 9 anomalies, ambiguïtés et incertitudes |
| `docs/rapport-final-mission-2.md` | Ce rapport |
| `outils/generer-inventaire-bepc.py` | Générateur de l'inventaire |
| `outils/valider-inventaire-bepc.mjs` | Contrôles qualité (sans dépendance) |

**Fichier non modifié** : `data/referentiel-maths-3e-cm-2025-2026.json`
(`sha256 f766f412…`) — ses identifiants sont uniquement *référencés*.

---

## 7. Vérifications réalisées

| Contrôle | Résultat |
|---|---|
| Complétude des documents | 14/14 pages lues, aucune manquante |
| Traçabilité : chaque question renvoie à un sujet identifié | ✅ 35/35 |
| Traçabilité : chaque question renvoie à un corrigé identifié | ✅ 35/35 |
| Énoncé transcrit pour chaque question | ✅ 35/35 |
| Toute question de calcul rattachée à au moins une leçon | ✅ |
| Toutes les leçons citées existent dans le référentiel annuel | ✅ |
| Identifiants de question uniques | ✅ |
| Numérotation des exercices continue, sans trou | ✅ dans chaque bloc |
| Sous-questions rattachées à leur question mère | ✅ 7 sous-questions |
| **Barème session 2025** | ✅ 12,5 + 7,5 = **20 pt** |
| **Barème session 2026** | ✅ 15 + 5 = **20 pt** |
| Tous les barèmes strictement positifs | ✅ |
| **Aucune compétence officielle inventée** | ✅ 0 sur 35 |
| Aucun résultat sans provenance de corrigé | ✅ |
| Aucun résultat inventé là où le corrigé n'en publie pas | ✅ |
| Les 14 leçons du référentiel positionnées | ✅ |
| Décompte par leçon cohérent | ✅ |
| Avertissement de non-représentativité présent | ✅ |
| Droits d'utilisation signalés comme non vérifiés | ✅ |
| Référentiel annuel déclaré non modifié | ✅ |
| Statut d'attente de validation humaine explicite | ✅ |

**Résultat du validateur : 0 erreur, 0 réserve.**

### Vérifications de méthode

**Le validateur n'est pas conforme par construction.** Cinq anomalies ont été
injectées dans une copie de l'inventaire — source fantôme, barème falsifié,
leçon inexistante, compétence officielle inventée, résultat fantôme sur une
question sans corrigé. **Les 5 ont été détectées.**

**Reproductibilité.** Le fichier a été supprimé puis régénéré : la sortie est
**strictement identique**.

**Non-régression du référentiel.** `git diff` sur le référentiel annuel est
vide ; son empreinte est inchangée ; son propre validateur retourne toujours
le code 2 (les 3 réserves connues de la mission 1).

---

## 8. Points nécessitant une décision du responsable pédagogique

| # | Décision | Enjeu | Bloque |
|---|---|---|---|
| 1 | **Droits de réutilisation des sujets et corrigés** | Toute reproduction dans l'application | Publication de contenu |
| 2 | Traitement de la tâche 2 de 2025, sans solution de référence | Correction automatique non légitime | Génération de corrigé |
| 3 | Rattachement du cylindre 2026 à la leçon 14 | Cohérence du référentiel annuel | Complétude |
| 4 | Renforcement de la leçon 6 malgré son absence observée | Planification des révisions | Pédagogie |
| 5 | Statistique (7 h) observée une seule fois | Écart volume / exposition | Pédagogie |
| 6 | Validation humaine de l'inventaire avant publication | Statut `provisoire` | Mise en production |

---

## 9. Conformité aux contraintes

| Contrainte | État |
|---|---|
| Aucun développement de fonctionnalité IA | ✅ |
| Aucune modification silencieuse du référentiel annuel | ✅ empreinte inchangée |
| Aucune compétence officielle inventée | ✅ 0 sur 35, absence motivée |
| Aucun contenu incertain présenté comme confirmé | ✅ champ `confiance` sur chaque association |
| Vérifier les droits avant republication | ✅ **droits signalés NON VÉRIFIÉS**, republication bloquée |
| Ne pas présenter les 2 sessions comme le programme | ✅ avertissement dans le JSON et les 3 documents |
| Ne pas publier automatiquement | ✅ statut provisoire, validation humaine requise |
| Ne jamais inventer un document absent | ✅ les 4 documents ont été physiquement retrouvés et lus |

---

## 10. Conclusion

Les deux sessions ont été localisées, rendues lisibles et analysées :
**35 questions inventoriées**, **18 exercices**, **13 des 14 leçons** du
référentiel annuel observées, **8 associations incertaines** explicitement
signalées, **9 anomalies** documentées.

Le travail le plus important de cette mission n'est pas l'inventaire, mais le
contrôle de fiabilité. Deux pièges ont été désamorcés :

- l'extraction automatique produisait une **mauvaise réponse** à un QCM et
  massacrait la consigne « π = 3,14 ». Toutes les valeurs ont été recontrôlées
  visuellement ;
- le corrigé 2025 **annule** une question et n'en publie pas la solution. Cette
  question a été laissée sans résultat, alors même qu'un calcul automatique
  aurait fourni une réponse. Fournir cette réponse aurait été inventer une
  solution du jury national.

**Aucun contenu n'est publié.** Le statut reste provisoire, et les droits
d'utilisation — reste le préalable bloquant à toute mise en production.

**Deux constats méritent une décision rapide** : la leçon 6 « Angles inscrits »
(5 h) n'apparaît dans aucune des deux sessions, et la leçon 11 « Statistique »
(7 h) n'y apparaît qu'une fois. Ce sont précisément les écarts qu'un examen
sur deux sessions peut révéler, et qu'aucune extrapolation ne permet de
trancher seule.

---

*Documents complémentaires : `docs/analyse-bepc-2025-2026.md`,
`docs/couverture-programme-bepc.md`, `docs/anomalies-documents-bepc.md`,
`data/inventaire-questions-bepc-2025-2026.json`.*
