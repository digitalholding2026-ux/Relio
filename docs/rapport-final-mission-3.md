# Rapport de fin de mission 3 — Spécification du diagnostic initial

**Mission** : 3 — Spécification pédagogique du diagnostic initial du MVP
**Date** : 2026-10-10
**Statut** : 🔴 **EN ATTENTE DE VALIDATION — aucun développement ne doit commencer**
**Entrées** : `data/referentiel-maths-3e-cm-2025-2026.json`, `data/inventaire-questions-bepc-2025-2026.json`

---

## 1. Le résultat en une phrase

Une mini-évaluation de **5 questions originales** couvrant **4 leçons sur 14**,
dont toutes les réponses ont été **vérifiées par calcul indépendant**, accompagnée
d'un jeu de règles qui interdit explicitement au système de conclure quoi que ce
soit à partir d'un échantillon trop petit — parce que c'est mathématiquement
impossible, pas seulement par prudence décorative.

---

## 2. Les deux.constats qui structurent la mission

### 2.1 Le référentiel ne contient aucune compétence

Vérification sur les 14 leçons :

| Champ | Éléments |
|---|---|
| `competences` | **0** |
| `objectifs` | **0** |
| `prerequis` | **0** |
| `exercices_ids`, `corriges_ids`, `references_bepc` | **0** |

La note de conformité du fichier l'indique : *« aucun document de référence
pédagogique n'a été fourni »*.

**La demande portait sur « les compétences documentées, lorsqu'elles sont
disponibles ». Elles ne le sont pas, pour aucune leçon.** La matrice est donc
construite sur un socle documentaire mince — les leçons, leur volume horaire,
leur placement trimestriel — et sur des **objectifs opérationnels déduits**, dont
chacun est marqué ⚠️ *DÉDUIT* dans la matrice et qu'aucun ne doit être présenté
comme relevant d'un texte officiel.

### 2.2 Aucune question BEPC n'est publiable

Les droits restent non vérifiés (constat de mission 2, non levé). Cela place le
projet devant une tension qu'il faut assumer :

> **Le contenu le plus fiable du projet — 35 corrigés harmonisés nationaux dont
> chaque réponse a été revérifiée à la source — est précisément le contenu que
> l'application n'a pas le droit de montrer.**

Les questions BEPC servent donc de **calibrage** (savoir *ce qui* est évalué et à
quel niveau). Les questions **originales** constituent le contenu élève. Ce
n'est pas un pis-aller : c'est la seule voie conforme, et elle a l'avantage de
permettre de contrôler la correction exactement.

---

## 3. Couverture obtenue, et ses limites assumées

| Niveau | Couverture |
|---|---|
| Leçons du programme | **4 / 14** (L1, L3, L5, L8) |
| Volume horaire | **28 h / 98 h** (29 %) |
| Questions | 5 originales + 6 sondes |
| Objectifs opérationnels testés | 6 |

### Leçons exclues et motifs

| Exclue | Motif |
|---|---|
| **L6 Angles inscrits** (5 h) | 🔴 **Bloqué** — aucun objectif dérivable de l'intitulé seul. Produire une question serait inventer du contenu pédagogique |
| **L11 Statistique** (7 h) | 🟡 La seule question observée est **inexploitable** : elle se déduit d'un tableau figurant dans le sujet, non reproductible |
| L2, L4, L7, L9, L10 (géométrie) | Figures obligatoires — forte contrainte téléphone, figures BEPC non réutilisables |
| L12, L13, L14 | Non prioritaires ; le corrigé 2026 n'y publie pas de méthode détaillée, donc mauvaise base de calibrage |

**L6 et L11 représentent 12 h de programme sans aucune question mobilisable
dans le MVP.** C'est le principal deficit de couverture, et il n'est pas
technique : il est lié aux droits et à l'absence de source pédagogique.

---

## 4. La règle qui gouverne l'interprétation

La décision la plus importante de la mission est négative : **interdire au système
de conclure trop vite**, sur une base statistique et non par prudence décorative.

Application de la règle des trois (0 erreur sur *n* trials → borne supérieure à
95 % du taux d'erreur ≈ 3/n) :

| Items sur un objectif | Erreurs | Borne sup. | Conclusion possible |
|---|---|---|---|
| 1 | 0 | **300 %** | **Aucune** |
| 2 | 0 | 150 % | Aucune |
| 4 | 0 | 75 % | Information naissante |
| 5 | 0 | 60 % | Information réelle |

> **La mini-évaluation, qui ne teste qu'un item par objectif, ne peut
> mathématiquement produire aucune conclusion d'acquisition.** Elle signale des
> difficultés ponctuelles et déclenche des sondes. Point.

D'où quatre interdits structurants : pas de score en pourcentage, pas de niveau
`n/5`, pas de conclusion sur une leçon non testée, et pas d'exploitation du mot
« diagnostic » sans réserve.

### La valeur ajoutée réelle : le croisement Q2 / Q3

Q2 (développer) et Q3 (factoriser) portent sur **la même identité remarquable**.
Le croisement des deux réponses produit un profil que ni l'une ni l'autre ne
donne seule :

| Q2 | Q3 | Lecture |
|---|---|---|
| ✅ | ❌ | Développement acquis, passage à la factorisation fragile → activité ciblée sur `OO-L1-2` |
| ❌ | ✅ | Profil atypique → vérifier la saisie avant de conclure |
| ❌ | ❌ | Difficulté sur l'identité remarquable elle-même |

**C'est le meilleur discriminant du lot**, et il est gratuit.

---

## 5. Vérifications réalisées

| Contrôle | Résultat |
|---|---|
| Références `lecon_id` citées existantes dans le référentiel | ✅ 4/4 (L1, L3, L5, L8) |
| Objectifs opérationnels rattachés aux questions | ✅ 5/5 questions, 6 objectifs distincts |
| **Réponses des 5 questions recalculées indépendamment** | ✅ 5/5 (fractions exactes, développement formel) |
| **Réponses des 6 sondes recalculées indépendamment** | ✅ 6/6 |
| Cohérence arithmétique des distracteurs (Q5 : 11−2−3+2…) | ✅ cohérents |
| Aucune question BEPC reproduite dans le contenu élève | ✅ 0 question, `source_bepc: null` partout |
| Aucune compétence officielle inventée | ✅ `competence_officielle` reste vide |
| Référentiel annuel **non modifié** | ✅ `sha256 f766f412…`, `git diff` vide |
| Question annulée `BEPC-2025-B-T2` exclue du diagnostic | ✅ exclu |
| Vrai/faux sans raisonnement (L7) exclus | ✅ exclus, motif documenté |
| Statuts de réponse définis au nombre de 3 (`partielle` inclus) | ✅ |
| Garde-fous anti-surinterprétation documentés | ✅ 8 interdits |
| Données personnelles collectées | ✅ **aucune** |
| Développement ou intégration IA | ✅ aucun |

**Vérification de non-régression** : le validateur de la mission 2 reste à
0 erreur / 0 réserve, et le référentiel annuel est bit-pour-bit inchangé.

---

## 6. Hypothèses retenues

| # | Hypothèse | Conséquence si fausse |
|---|---|---|
| H1 | Un élève de 3e saisit une expression algébrique sur téléphone | Périmètre réduit au QCM — **dégradation majeure** de la valeur diagnostique |
| H2 | 5 questions suffisent à déclencher un exercice pertinent | Descendre à 3 questions, signal encore plus faible |
| H3 | Les objectifs déduits correspondent au contenu réel des leçons 1, 3, 5, 8 | Les questions ciblent le mauvais contenu — **validation pédagogique requise** |
| H4 | L'élève n'a pas encore fait la densité du programme | L'interprétation des acquis est faussée dans un sens ou dans l'autre |
| H5 | `origine: "originale"` sera garantie techniquement | Une question BEPC finit par fuiter dans l'app — **droit bloqué** |

**H3 est le risque principal** : toute la spécification repose sur des objectifs
déduits, jamais validés par un enseignant.

---

## 7. Décisions attendues du responsable produit

### Bloquantes — le développement ne doit pas démarrer sans elles

| # | Décision | Pourquoi c'est bloquant |
|---|---|---|
| **D1** | 🔴 **Droits d'utilisation des documents BEPC** | Détermine si le contenu du jury peut un jour être utilisé. Reporté de la mission 2 |
| **D2** | 🔴 **Contenu attendu de la leçon 6 « Angles inscrits »** | Sans objectives définis, toute question produite serait inventée. Fournir le contenu, ou acter que L6 est hors MVP |
| **D3** | 🟡 **Support de données original pour L11 Statistique** | La seule source existante est non reproductible. Un tableau original est nécessaire |
| **D4** | 🟡 **Validation des 5 questions originales par un enseignant** | Les corrections sont vérifiées par calcul, **pas** par un didacticien |

### Non bloquantes pour la spécification, bloquantes pour l'implémentation

| # | Décision |
|---|---|
| **D5** | Évaluateur algébrique, ou formes acceptées en dur par question ? |
| **D6** | Durée de conservation de l'historique brut (RGPD — données de mineurs) |
| **D7** | Les réponses sont-elles accessibles à un enseignant ? (change le consentement) |
| **D8** | Motivation à l'usage : compte obligatoire ou non ? (impacte l'anti-triche et la persistance) |
| **D9** | Langue : français uniquement, ou l'appareil de saisie √/² doit-il être porté à d'autres écritures ? |

---

## 8. Conformité aux contraintes

| Contrainte | État |
|---|---|
| Ne pas modifier le référentiel annuel | ✅ inchangé, `sha256` identique |
| Ne pas publier les sujets/corrigés sans droits | ✅ contenu élève 100 % original, `source_bepc: null` |
| Ne pas inventer de barème ou de compétence officielle | ✅ aucune compétence inventée ; aucun barème BEPC repris |
| Ne pas développer ni intégrer l'IA | ✅ aucun développement |
| Ne pas présenter une estimation provisoire comme un diagnostic certain | ✅ règle des trois + 8 interdits + cadrage obligatoire à l'écran |
| Ne pas commencer de développement avant validation | ✅ statut bloquant, 4 décisions bloquantes listées |

---

## 9. Livrables

| Fichier | Contenu |
|---|---|
| `docs/matrice-couverture-competences.md` | 14 leçons, objectifs documentés vs déduits, questions BEPC, fiabilité, lacunes, besoins en questions originales |
| `docs/specification-diagnostic-initial.md` | 5 questions originales, corrections vérifiées, distracteurs, ce que chaque réponse permet/ne permet pas de conclure, saisie mobile |
| `docs/regles-recommandation-pedagogique.md` | Règles d'interprétation, signatures d'erreurs, sondes, garde-fous, parcours en 7 étapes |
| `docs/rapport-final-mission-3.md` | Ce rapport |

---

## 10. Conclusion

La spécification est **complète et vérifiable sur le plan technique**, et
**explicitement incomplète sur le plan pédagogique**. Les 11 réponses (5
questions + 6 sondes) sont contrôlées par calcul. Les garde-fous statistiques
sont posés et non négociables.

Mais **tout repose sur des objectifs opérationnels déduits par un analyste, que
personne n'a validés**. Un enseignant peut parfaitement juger que la leçon 1 ne
tourne pas autour de « développer une expression algébrique », et alors les
questions ciblent le mauvais contenu — avec des réponses mathématiquement
irréprochables.

**La recommandation est donc de ne pas commencer à coder**, mais de faire relire
les 5 questions et les 6 objectifs déduits par un enseignant de mathématiques,
puis de trancher les quatre décisions bloquantes. Ce sont elles, et non la
conception, qui conditionnent le calendrier.

**Rien n'a été publié et rien ne doit l'être** tant que D1 n'est pas tranchée.

---

*Documents liés : `docs/matrice-couverture-competences.md`,
`docs/specification-diagnostic-initial.md`, `docs/regles-recommandation-pedagogique.md`.*