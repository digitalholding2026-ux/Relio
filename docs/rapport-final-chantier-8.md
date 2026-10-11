# RAPPORT FINAL — CHANTIER 8

## Spécification pédagogique « développer et réduire » (`OO-L1-1`)

**Date :** 2026-10-11
**Nature du chantier :** documentaire — conception et validation
**Statut :** spécification **rédigée**, **non validée** par un enseignant

---

## 1. Ce qui a été fait

Le chantier demandé consistait à **ne pas implémenter** mais à **spécifier** la
pédagogie de la compétence `OO-L1-1`, et à auditer si les rapports des chantiers
précédents tenaient encore. Trois livrables sont produits :

| Livrable | Fichier |
|---|---|
| Spécification pédagogique (9 sections) | `docs/specification-pedagogique-developper-reduire-v1.md` |
| Contrôle automatique de cohérence | `outils/valider-spec-developper-reduire.mjs` |
| Le présent rapport | `docs/rapport-final-chantier-8.md` |

**Aucun fichier applicatif n'a été modifié.** `backend/` et `frontend/` sont
intacts — seuls deux fichiers nouveaux, non exécutés en production, ont été
ajoutés à la racine.

---

## 2. Les trois réponses aux trois questions posées

### 2.1 « Les rapports 7.4–7.7 tenaient-ils ? »

**Globalement oui sur le fond, mais avec une fragilité commune :** ces rapports
décrivent des **intentions** ou des **états intermédiaires**, et plusieurs de
leurs affirmations chiffrées ne sont plus exactes. La règle appliquée dans ce
chantier : **le code prime sur le rapport**. Un rapport qui se contredit avec le
code est un rapport à corriger, pas une fonctionnalité acquise.

Concrètement, ce qui **résiste** à la vérification :
- l'échelle de tutorat à 3 niveaux et sa règle d'escalade existent bien ;
- le suivi de progression et la règle des trois sont réellement implémentés ;
- le journal local élève existe, plafonné à 500 observations.

Ce qui **ne résiste pas** : le compte de signatures (voir § 3, C-2), et surtout la
promesse de « maîtrise » qui n'existe nulle part dans le moteur (voir § 2.3).

### 2.2 « Les spécifications pédagogiques tenaient-elles ? »

**Non, pas entièrement.** `docs/regles-recommandation-pedagogique.md` est encore
explicitement marquée « en attente de validation » **et** porte l'interdiction
suivante : *« ne pas développer avant validation »*. Or le MVP a été développé.
Il y a donc un décalage de séquence entre ce que la mission 3 demandait et ce que
les chantiers suivants ont livré. La présente spécification **reprend cet
interdit à son compte** : elle est rédigée pour être validée, et rien ne doit être
codé avant arbitrage.

### 2.3 « Les 5 étapes par niveau étaient-elles conformes ? »

**Oui sur l'existence des 5 niveaux, non sur l'idée qu'ils mesurent un niveau.**

Le moteur a bien les 5 niveaux (orienter / expliquer / accompagner). Mais ces
niveaux répondent à la question **« combien de fois l'élève a échoué ? »**, pas à
**« que sait l'élève ? »**. C'est toute la différence entre « connaître la règle »
et « savoir l'utiliser seul ». Le § L5 de la spécification écrit cette distinction
noir sur blanc, parce que c'est le cœur du problème du chantier.

---

## 3. Contradictions relevées (3)

| # | Contradiction | Comment elle a été traitée |
|---|---|---|
| **C-1** | Libellé de `OO-L1-1` : « développer une expression » (matrice) vs « développer **et réduire** » (code) | La spec retient le libellé du code (affiché à l'élève) et renvoie l'arbitrage à **Q9** |
| **C-2** | **11 signatures** annoncées dans la spec et dans deux rapports vs **12** dans le code | La spec retient **12** et signale que les trois comptes « 11 » sont faux. Le validateur vérifie ce point automatiquement |
| **C-3** | Le mot « maîtrise » est **interdit** par la spec de mission 3 mais **employé** dans la spec du diagnostic initial | La spec OO-L1-1 **n'emploie plus** ce mot pour un état calculé ; elle réserve « maîtrisé » à la vérification ultérieure postérieure |

---

## 4. Contrôle automatique — `valider-spec-developper-reduire.mjs`

Un validateur compare **le texte de la spécification au code réel**, de façon
indépendante. Il suit le style des validateurs existants (`valider-referentiel.mjs`),
retourne 0/1/2, et n'exécute **aucun** code applicatif.

**Résultat : 18 contrôles, 0 erreur, 0 réserve.**

```
  [OK]  le document est explicitement « en attente de validation pédagogique »
  [OK]  le statut de non-validation est présent
  [OK]  le catalogue contient bien 12 signatures
  [OK]  la spécification annonce 12 signatures, ce qui correspond au code
  [OK]  la contradiction C-2 (11 vs 12) est tranchée en faveur du code
  [OK]  le vocabulaire de catégories contient bien 8 catégories
  [OK]  toutes les catégories du code sont nommées dans la spécification
  [OK]  chaque signature a une catégorie (12 paires, correspondance totale)
  [OK]  les 3 exercices OO-L1-1 ont regleForme: null — « a_determiner » est inatteignable
  [OK]  MVP-B1-E1 : reponseAttendue « 2x + 1 » confirmé
  [OK]  MVP-B1-E2 : reponseAttendue « 4x^2 - 4x + 1 » confirmé
  [OK]  MVP-B1-E3 : reponseAttendue « x^2 - x - 4 » confirmé
  [OK]  les 10 pièges cités dans les cas de test correspondent au code
  [OK]  l'ordre D5 (incorrect → inacheve → forme → a_determiner → correct) est bien celui documenté
  [OK]  niveauPourNbEchecs ne dépend que du nombre d'échecs — l'écart décrit au § L4.1 est exact
  [OK]  progression.ts expose exactement 4 statuts — aucun statut de maîtrise
  [OK]  aucun statut de maîtrise parmi les statuts — cohérent avec le § L5
  [OK]  les 5 fichiers cités par la spécification existent tous

=== Résultat : 0 erreur(s), 0 réserve(s) ===
```

**Ce que ce contrôle prouve :** que la spécification **ne ment pas** sur le code.
Il ne dit pas que la pédagogie est bonne — il dit que chaque affirmation marquée
« vérifié » est exacte, et il échouera le jour où le code changera sans que la
spécification soit mise à jour.

---

## 5. Ce que ce chantier a décidé / laissé en l'air

**Décidé (sans arbitrage) :**
- Le contenu des 9 sections et 27 cas de test ;
- Le fait que D5 n'est **pas** remis en cause ;
- Que sur `OO-L1-1`, seuls `correct` et `incorrect` sont **atteignables** comme verdicts, parce que les 3 exercices n'exigent aucune forme ;
- Le constat qu'il manque **un seul champ** (`estVerificationUlterieure`) pour rendre la règle de maîtrise calculable.

**Laissé volontairement ouvert — 9 questions de validation (§ L8) :**
- **4 conditionnent la mise en œuvre** du suivi : le seuil (Q3), l'exigence de 2 exercices différents (Q4), le délai de vérification (Q6), le champ à ajouter (Q8) ;
- les autres (Q1, Q2, Q5, Q7, Q9) portent sur des arbitrages de fond : prérequis, granularité des catégories, conservation des données, libellé de la compétence.

**Un défaut code signalé, non corrigé (hors périmètre) :**
`backend/src/contenu/aides.ts:131` contient le mot anglais « could-tu » dans un
message destiné à l'élève (« par quel nombre **could-tu** les diviser… »). C'est un
défaut réel, hors compétence `OO-L1-1` ; il est signalé pour un chantier de
correction, **pas corrigé ici** pour ne pas sortir du périmètre documentaire.

---

## 6. Réserves honnêtes

1. **La spécification n'est pas validée.** C'est le statut normal d'un document
   qui attend un enseignant. Tant que § L8 n'est pas arbitré, les propositions
   [PROPOSÉ] ne doivent pas être codées.
2. **Le validateur compare du texte à du texte.** Il vérifie que la spec décrit
   fidèlement le code ; il ne valide pas la pédagogie elle-même. Seule une lecture
   enseignante peut le faire.
3. **Les seuils proposés (3 réussites, 2 exercices, vérification ultérieure) sont
   des recommandations**, alignées sur la règle des trois déjà présente dans le
   code, mais ce ne sont pas des constantes historiques — elles doivent être
   assumées ou ajustées par un enseignant, pas héritées de ce document.

---

## 7. Prochaine étape proposée

1. Un enseignant relit la spec et **arbitre les 9 questions du § L8**.
2. Le statut passe à « validée » ; le validateur est mis à jour en conséquence.
3. **Ensuite seulement**, un chantier d'implémentation peut reprendre les
   [PROPOSÉ] retenus — en commençant par le plus structurant : la règle
   d'escalade par cause (§ L4.1) et le champ `estVerificationUlterieure` (§ L6.2).

Aucune de ces trois étapes n'est engagée par le présent rapport.