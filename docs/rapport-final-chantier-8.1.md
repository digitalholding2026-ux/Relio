# RAPPORT FINAL — CHANTIER 8.1

## Intégration des décisions validées Q1 à Q4 dans la spécification `OO-L1-1`

**Date :** 2026-10-11
**Nature du chantier :** documentaire — mise à jour de spécification
**Statut :** Q1 à Q4 **intégrées** · Q5 à Q9 **ouvertes** · 2 ambiguïtés **nouvelles**

---

## 1. Ce qui a été fait

Quatre décisions de contrat pédagogique, arbitrées par le responsable produit, ont
été intégrées dans la spécification existante. **Aucun code applicatif n'a été
modifié, aucun exercice touché, aucune règle de correction changée, aucun
déploiement effectué.**

| Livrable | Fichier | Action |
|---|---|---|
| Spécification | `docs/specification-pedagogique-developper-reduire-v1.md` | **modifiée** (v1.0 → v1.1) |
| Contrôle de cohérence | `outils/valider-spec-developer-reduire.mjs` | **modifié** (3 contrôles ajoutés, 2 corrigés) |
| Le présent rapport | `docs/rapport-final-chantier-8.1.md` | **créé** |

---

## 2. Les décisions validées, et où elles sont intégrées

Les quatre décisions sont reprises **mot pour mot** au § L0.5, dans un encadré
qui leur donne le statut de contrat. Elles ne sont pas reformulées.

| Décision | Texte validé (abrégé) | Sections intégrées |
|---|---|---|
| **Q1 — Prérequis** | Vérifier selon les besoins de l'élève, remédiation ciblée, **sans blocage systématique** | **L1.2** (réécrite), L7.5 (T-34) |
| **Q2 — Diagnostic** | Cause étayée → aide ciblée · plusieurs causes → question · inconnue → rester neutre | **L2.5** (nouvelle), **L3.3**, **L4.1**, **L4.3**, L7.5 (T-35→T-37) |
| **Q3 — Maîtrise** | 3 réussites probantes dont ≥1 en vérification ultérieure · aide = progrès · dédupliquer les tentatives identiques | **L5.2**, **L5.3**, **L5.5**, **L5.6** (nouvelle), **L6.2**, L7.4, L7.5 |
| **Q4 — Diversité** | ≥2 tâches distinctes · expression différente en vérification · pas de difficulté excessive | **L5.2**, **L5.4**, **L6.2**, L7.4 (T-29) |

### Ce qui a changé dans le fond

| Point | v1.0 (proposé) | v1.1 (validé) |
|---|---|---|
| Prérequis | « à déclarer » comme conditions d'accès | **catalogue de remédiation**, jamais un blocage |
| Diagnostic | question posée seulement si information *manquante* (illisible, forme indéterminée) | **trois branches**, dont « plusieurs causes possibles » |
| Seuil de maîtrise | « 3 réussites sans aide » (à valider) | **3 réussites probantes**, dont **1 en vérification ultérieure** |
| Réussite avec aide | non traitée | **progrès** : ne compte pour **zéro** réussite autonome |
| Tâches | « 2 exercices différents » | « **2 tâches distinctes** », expression différente en vérification |
| Champs manquants | **1** (`estVerificationUlterieure`) | **3** : `nbIndicesConsultes`, `estVerificationUlterieure`, `expressionTache` |

**Correction d'une erreur de la v1.0 :** le document affirmait qu'**un seul**
champ manquait. C'est faux : Q3 exige de distinguer une réussite autonome d'un
progrès, et le journal ne compte que les **échecs**, pas les **indices consultés**.
Il manque donc trois champs ([L6.2](#l62-les-données-minimales-pour-la-règle-du--l5)).

---

## 3. Cohérence entre réussite autonome, vérification ultérieure et maîtrise

C'était le point 5 du cahier des charges. La chaîne a été vérifiée de bout en
bout, et **se tient** :

```
1. Q3 : 3 réussites PROBANTES            → « acquis fragile » suffit
2. Q3 : déduplication par tâche          → E1 réussi 3 fois = 1 seule preuve
3. Q4 : ≥2 tâches distinctes             → impossible d'avoir 3 preuves sur 1 tâche
4. Q3 : ≥1 preuve en vérification ult.   → sans elle : toujours « acquis fragile »
5. Q4 : expression différente            → sinon la vérification est refusée (T-29)
```

**Les deux règles sont complémentaires, pas concurrentes.** Q3 déduplique, Q4
garantit qu'il reste assez de tâches distinctes pour atteindre le seuil : sans
Q4, la déduplication de Q3 rendrait la maîtrise **mathématiquement inatteignable**.
C'est écrit explicitement dans [L5.6](#l56-réussite-autonome--progrès--preuve).

**Deux écarts signalés dans les cas de test** ([L7.4](#l74-cas-de-progression--deux-colonnes--aujourdhui--cible-validée)) :

- **T-24** — 3 réussites **avec aide** sur 3 tâches : le moteur actuel conclurait,
  la cible Q3 **refuse** (3 progrès ≠ 3 réussites).
- **T-25** — 3 réussites **autonomes** sur **une seule** tâche : le moteur actuel
  conclurait, la cible Q3 **refuse** (déduplication).

Ces deux cas sont les plus dangereux du lot : ce sont ceux où le code **conclurait
trop vite**. Ils sont documentés comme écarts, pas comme corrections.

---

## 4. Tests documentaires effectués

Le validateur a été **étendu** (3 contrôles : statut Q1–Q4, statut Q5–Q9, marqueurs
`[VALIDÉ]`) et **corrigé sur deux bugs réels** découverts en le testant.

### 4.1 Résultat

```
=== Résultat : 0 erreur(s), 0 réserve(s) ===
21 contrôles au vert
```

### 4.2 Les tests qui ont échoué, et ce qu'ils ont révélé

C'est le point important. Un contrôle qui ne détecte pas sa régression ne prouve
rien. Trois régressions ont été injectées volontairement dans la spec :

| Régression injectée | Détectée ? | Ce que ça a révélé |
|---|---|---|
| Affirmation positive « a été validée par un enseignant » | ✅ **après correction** | Le motif `/validé par un enseignant/` ne reconnaissait pas la forme féminine **« validée »**. Corrigé en `validée?` |
| Un marqueur `**[VALIDÉ — Q10]**` | ✅ **après correction** | Le motif `/Q(\d)/` capturait **« Q10 » comme « Q1 »** — une décision non validée aurait passé le contrôle sans être vue. Corrigé en `/Q(\d+)/` |
| Retrait de « Q5 à Q9 restent ouvertes » | ✅ détecté du 1er coup | — |

**Les deux premiers contrôles étaient faux et l'un d'eux était dangereux** : avant
correction, `[VALIDÉ — Q10]` était lu comme `[VALIDÉ — Q1]` et **passait**. C'est
exactement le genre de défaut que le chantier 8 devait éviter.

### 4.3 Contrôles conservés du chantier 8

Les 18 contrôles initiaux sont inchangés et passent toujours : 12 signatures,
8 catégories, correspondance totale signature→catégorie, `regleForme: null` sur les
3 exercices, réponses attendues, 10 pièges, ordre D5, `niveauPourNbEchecs`,
absence de statut de maîtrise, existence des fichiers cités.

**Résultat : le code n'a pas bougé, et le validateur le confirme.**

---

## 5. Questions encore ouvertes

### 5.1 Q5 à Q9 — inchangées, non arbitrées

| # | Question | Effet si non tranchée |
|---|---|---|
| **Q5** | Enrichir les pièges hors périmètre ? | **Bloque la branche « plusieurs causes » de Q2** : sans elle, les branches B et C restent indiscernables |
| **Q6** | Délai avant vérification ultérieure ? | Sans délai, la vérification prouve peu de plus que l'exercice |
| **Q7** | Conservation des données locales ? | Perte du journal au vidage du navigateur |
| **Q8** | Champ `estVerificationUlterieure` ? | Rendue nécessaire par Q3, mais le champ lui-même reste à valider |
| **Q9** | Libellé de la compétence ? | Deux libellés affichés dans deux documents différents |

### 5.2 Deux ambiguïtés nouvelles, signalées et non tranchées

Elles ne figuraient pas en v1.0 : elles sont apparues en intégrant Q3 et Q4, parce
que les deux décisions nomment des notions que le produit n'a pas définies
opérationnellement.

| # | Ambiguïté | Origine | Conséquence si non tranchée |
|---|---|---|---|
| **Q10** | **Comment savoir qu'un prérequis manque ?** Q1 impose de « vérifier les prérequis selon les besoins », mais aucun signal du moteur ne distingue « prérequis manquant » d'« erreur occasionnelle ». Le code déclare `prerequis: []` et n'a aucun mécanisme de remédiation. | Q1 | **Q1 n'est pas applicable** en l'état |
| **Q11** | **Définition opérationnelle de la tentative autonome.** Q3 exclut les réponses « obtenues après une aide », mais le journal ne compte que les **échecs**. Restent flous : (a) un indice **affiché mais non ouvert** disqualifie-t-il ? (b) une aide reçue sur une **tentative antérieure** disqualifie-t-elle la suivante ? | Q3 | Les cas T-24 à T-29 reposent sur une définition **provisoire** |

**Le § L5.6 fournit une définition de travail** (« aucun indice consulté pendant
la tentative ») qui a servi à écrire les cas de test. Elle est explicitement
**provisoire** et disparaîtra si Q11 est arbitrée autrement. Aucune option n'est
retenue par ce document.

---

## 6. Contraintes — respect vérifié

| Contrainte | État |
|---|---|
| Aucun code applicatif modifié | ✅ `backend/` et `frontend/` intacts |
| Aucun exercice existant modifié | ✅ `exercices.ts` intact |
| Aucune règle de correction changée | ✅ D5 intact ; Q2 ne touche que le **choix de l'aide**, jamais le verdict |
| Aucun déploiement | ✅ aucun commit sur `backend/` ou `frontend/` |
| Aucune autre décision considérée comme validée | ✅ 26 marqueurs `[VALIDÉ]`, tous Q1–Q4 (contrôlé automatiquement) |
| Aucune validation enseignante revendiquée | ✅ contrôlé automatiquement, y compris la forme féminine « validée » |
| Décisions non réécrites au-delà du nécessaire | ✅ reprises mot pour mot au § L0.5 |

---

## 7. Réserves honnêtes

1. **Le document reste sans validation enseignante.** Q1 à Q4 sont un contrat
   produit, pas une validation pédagogique. La distinction est maintenue partout.
2. **Q2 est en partie inapplicable tant que Q5 n'est pas tranchée.** La branche
   « plusieurs causes possibles » exige une information qui n'existe pas dans le
   modèle actuel. Le contrat est validé ; la mécanique ne l'est pas. C'est
   écrit dans le document ([L2.5](#l25-le-tri-de-la-cause--décision-validée-q2)).
3. **Trois champs de données manquent** pour que Q3 et Q4 soient calculables.
   Aucun n'a été ajouté : ce chantier est documentaire.
4. **Le validateur compare du texte à du texte.** Il garantit que la spec décrit
   fidèlement le code et le statut des décisions ; il ne valide pas la pédagogie.

---

## 8. Étape suivante proposée

1. Arbitrer **Q5** en priorité : elle conditionne l'applicabilité de Q2.
2. Arbitrer **Q10** et **Q11**, sans lesquelles Q1 et Q3 restent partiellement
   inapplicables.
3. Trancher **Q6** et **Q8**, qui conditionnent la mise en œuvre du suivi.
4. **Ensuite seulement**, un chantier d'implémentation — qui pourra modifier le
   journal et les exercices, ce que le présent chantier ne pouvait pas faire.

Aucune de ces étapes n'est engagée par ce rapport.