# RAPPORT FINAL — CHANTIER 8.2

## Consolidation du contrat pédagogique « Développer et réduire une expression littérale » (`OO-L1-1`)

**Date :** 2026-10-11
**Nature :** documentaire uniquement
**Statut :** Q1 à Q11 intégrées · 32 contrôles au vert · **non implémenté**

---

## 1. Fichiers lus et modifiés

### 1.1 Lus

| Fichier | Usage |
|---|---|
| `docs/specification-pedagogique-developper-reduire-v1.md` | document modifié (v1.1 → **v1.2**) |
| `docs/rapport-final-chantier-8.md` | contexte, décisions antérieures |
| `docs/rapport-final-chantier-8.1.md` | intégrations Q1–Q4, cas limites |
| `outils/valider-spec-developer-reduire.mjs` | validateur modifié (271 → **393** lignes) |
| `backend/src/contenu/blocs.ts` | libellé de `OO-L1-1` (Q9) |
| `backend/src/contenu/exercices.ts` | 3 exercices, pièges, `regleForme` |
| `backend/src/contenu/tutorat.ts`, `signatures.ts`, `correction.ts` | taxonomie, D5 |
| `backend/src/lib/progression.ts` | statuts, absence de maîtrise |
| `frontend/src/lib/observations.ts` | **journal local, plateau de 500, effacement** |
| `docs/matrice-couverture-competences.md` | second libellé erroné |

### 1.2 Modifiés

| Fichier | Nature |
|---|---|
| `docs/specification-pedagogique-developper-reduire-v1.md` | v1.1 → v1.2 |
| `outils/valider-spec-developer-reduire.mjs` | contrôles Q1–Q4 → Q1–Q11, + 13 contrôles |
| `docs/rapport-final-chantier-8.2.md` | **créé** (ce document) |

**Aucun autre fichier modifié.**

---

## 2. Décisions Q1 à Q11 et sections d'intégration

| Décision | Intégrée dans | Effet concret |
|---|---|---|
| **Q1** Prérequis sans blocage | **L1.2** | catalogue de remédiation, pas condition d'accès |
| **Q2** Tri de la cause | **L2.5**, **L3.3**, **L4.1**, **L4.3** | 3 branches + **interdiction de transformer** une erreur nouvelle en catégorie connue |
| **Q3** 3 réussites probantes | **L5.2**, **L5.3**, **L5.6** | déduplication par tâche |
| **Q4** ≥2 tâches distinctes | **L5.4**, **L6.2** | expression différente exigée |
| **Q5** Enrichissement progressif | **L2.5** | Q2 devient **applicable** : la branche « neutre » est la règle |
| **Q6** Vérification ≥24 h | **L5.4** | 4 conditions cumulatives ; **le délai se recalcule à chaque réussite** |
| **Q7** Conservation locale | **L6.3** | contradiction avec le plafond de 500 **constatée** |
| **Q8** `estVerificationUlterieure` | **L6.2** | calculé par Relio, **nécessaire mais non suffisant** |
| **Q9** Nom canonique | **L1.0**, en-tête | « Développer et réduire une expression **littérale** » |
| **Q10** Détection prudente | **L1.2** | circuit erreur → vérification → remédiation **ou** retour |
| **Q11** Tentative autonome | **L5.6** | disponible ≠ consulté ; aide antérieure ne disqualifie pas |

---

## 3. Les trois champs de données

### 3.1 `nbIndicesConsultes`

| | |
|---|---|
| **Objectif** | Permettre à Q11 de distinguer réussite autonome et progrès |
| **Définition** | Nombre d'indices **réellement ouverts** pendant la tentative. Un indice **disponible mais non ouvert** ne compte pas |
| **Qui / quand** | Le client, **à l'ouverture** de l'indice — pas l'élève, pas a posteriori |
| **Calcul** | Incrémenté par ouverture ; remis à zéro à chaque tentative ; **jamais reporté** d'une tentative à l'autre |
| **Limite actuelle** | Aucun champ équivalent. `niveauAide` ne le porte pas |

**Distinction disponible/consulté vérifiée** : c'est bien la raison d'être du champ. Un compteur d'« indices affichés » ne satisferait pas Q11.

### 3.2 `estVerificationUlterieure`

| | |
|---|---|
| **Objectif** | Marquer la tentative conforme à Q6 |
| **Définition** | Vrai si les **4 conditions** de Q6 sont réunies |
| **Qui / quand** | **La logique de Relio**, jamais l'élève (Q8 explicite) |
| **Validation** | `true` uniquement si les 4 conditions sont vraies ; **opaque pour l'élève** |
| **Limite actuelle** | **Aucun horodatage n'est stocké** → le calcul des 24 h est matériellement impossible |

### 3.3 `expressionTache`

| | |
|---|---|
| **Objectif** | Vérifier Q4 (expression différente) et dédupliquer Q3 |
| **Définition** | Représentation **normalisée** de l'expression proposée |
| **Qui / quand** | Relio, à la construction de l'observation |
| **Validation** | Comparaison par **normalisation**, **jamais** par chaînes brutes |
| **Limite actuelle** | Aucun champ ; `exerciceId` ne dit rien de l'expression |

**Une chaîne de texte ne suffit pas** — trois raisons documentées : non-normalisation (`3x+6-x-5` ≠ `3x + 6 - x - 5` en chaîne), équivalence mathématique (`2(x+3)` = `2x+6`), faux positifs (deux exercices, même expression).

### 3.4 Correction d'une erreur de la v1.1

**La v1.1 déclarait `objectifId`, `signatureErreur` et `nbEchecsAuPrecedent` comme existants (« ✅ oui »). C'est faux pour le journal local.** L'interface `Observation` ne contient que 7 champs (`observations.ts:41-51`). Par ailleurs `reussiteApresAides` est **collant** (`.some(...)`, `observations.ts:159`) et **ne peut pas** servir au décompte des preuves.

---

## 4. Cas limites vérifiés

| Cas | Attendu | Où |
|---|---|---|
| 3 réponses justes **avec aide** | 0 réussite autonome — 3 progrès | T-24 |
| 3 réussites autonomes sur **une seule** tâche | 1 seule preuve | T-25 |
| Indice **affiché mais non consulté** | réussite autonome | T-41 |
| Aide consultée sur une **tentative précédente** | réussite autonome | T-43 |
| Erreur pouvant correspondre à **plusieurs causes** | question diagnostique courte | L4.3 |
| Vérification **trop tôt** (12 h, ou même séance à 30 h) | refusée | T-38, T-40 |
| Vérification sur la **même expression** | refusée | T-29, T-48 |
| `estVerificationUlterieure` seul | **insuffisant** | T-47 |

**Distinction demandée par le cahier des charges :**

| Nature | Cas | Exécutable aujourd'hui ? |
|---|---|---|
| **Documentaire** | T-34 à T-37, T-38 à T-43, T-45 à T-49 | **Oui** — règles écrites |
| **Implémentation** | T-21 à T-33 | **Non** — le moteur n'a ni aide, ni tâche, ni délai |

**Le validateur ne contrôle que la première catégorie.** Il ne simule aucun cas de la seconde.

---

## 5. Contrôles : réussis, échoués, non applicables

### 5.1 Exécution réelle

```
$ node outils/valider-spec-developer-reduire.mjs
=== Résultat : 0 erreur(s), 0 réserve(s) ===
=== Contrôle conforme. ===   (code de sortie 0)
```

**32 contrôles réussis · 0 échoué · 0 réserve.**

### 5.2 Régressions injectées — 12 tests

| # | Régression injectée | Résultat |
|---|---|---|
| R1 | « 24 heures » retiré de l'encadré | **détectée** |
| R2 | « séance distincte » retirée de l'encadré | **détectée** |
| R3 | nom canonique faux dans l'encadré | **détectée** |
| R4 | Q11 retirée de l'encadré | **détectée** |
| R5 | Q10 réintroduite comme ouverte dans L8.0 | **détectée** |
| R6 | bloc L6.3 remplacé (plafond / effacement) | **détectée** |
| R7 | bloc L5.6 remplacé | **détectée** |
| R8 | marqueur `[VALIDÉ — Q12]` | **détectée** |
| R9 | citation de ligne hors plage | **détectée** |
| R10 | citation vers un fichier inexistant | **détectée** |
| R11 | validation enseignante affirmée | **détectée** |
| R12 | retour à « Q5 à Q9 restent ouvertes » | **détectée** |

**12/12 détectées.** L'exécution de ces 12 tests est réelle ; le tableau reprend la sortie du validateur.

### 5.3 Faiblesses du validateur trouvées et corrigées

**C'est le résultat le plus important du chantier.** En injectant des régressions, j'ai découvert que **5 des 7 premiers contrôles ne détectaient rien** :

| Faiblesse trouvée | Cause | Correction |
|---|---|---|
| Contrôles Q6/Q9/Q7 passaient malgré la régression | les termes apparaissent **plusieurs fois** : `.includes` passait pour la mauvaise raison | exigence dans **la section visée** et **l'encadré** |
| `[VALIDÉ — Q10]` passait | `/Q(\d)/` lisait « Q10 » comme « Q1 » | corrigé en `/Q(\d+)/` (déjà en 8.1) |
| « Q10 **reste** ouverte » passait | regex au pluriel uniquement (`restent ouvertes`) | motif élargi au singulier |
| Citation de ligne fausse passait | aucun contrôle des références | **13 contrôles ajoutés** (fichier existe + ligne dans la plage) |
| Q9 détectait une mention légitime | « …données des mineurs finalisée » matchait, alors que le document la **nie** | vérification de la **négation explicite** |

**Le contrôle R9 a d'ailleurs trouvé une vraie erreur de ma part** : la spec citait `observations.ts:164` pour le `slice(-TENTATIVES_MAX)`, qui est en réalité à la **ligne 167**. Corrigé.

---

## 6. Commandes exécutées et résultats réels

```bash
# Lecture des faits
sed -n '41,51p' frontend/src/lib/observations.ts   # 7 champs, pas 8
sed -n '159,167p' frontend/src/lib/observations.ts # dejaReussi collant + slice(-500)

# Validation
node outils/valider-spec-developer-reduire.mjs     # 0 erreur, 0 réserve, exit 0
python3 /tmp/opencode/regre.py                     # 12 régressions, 12 détectées

# Non-modification
cd backend  && git diff HEAD --stat src/           # vide
cd frontend && git diff HEAD --stat src/           # vide
```

---

## 7. Confirmation vérifiable de non-modification

| Élément | Preuve | Résultat |
|---|---|---|
| `backend/` | `git status --short` + `git diff HEAD --stat` | **vide** |
| `frontend/` | `git status --short` + `git diff HEAD --stat` | **vide** |
| `exercices.ts` | `git diff HEAD --stat src/contenu/exercices.ts` | **vide** |
| `correction.ts` (règles D5) | `git diff HEAD --stat src/contenu/correction.ts` | **vide** |
| `progression.ts` | `git diff HEAD --stat src/lib/progression.ts` | **vide** |
| Schémas applicatifs | aucun fichier `.ts` modifié | **intact** |
| Dépendances | aucun `package.json` modifié | **intact** |
| Déploiement | aucun commit sur `backend/` ni `frontend/` | **aucun** |

HEAD : `966367f` (chantier 8.1) — inchangé pendant le travail.

**Réserve d'honnêteté** : `git status` racine affiche ` D outils/valider-spec-developer-reduire.mjs`. Le fichier **existe**, son hash est **identique à celui de l'index**, et il s'exécute normalement. C'est un artefact du montage du conteneur, déjà observé au chantier 8.1, et non une suppression réelle.

---

## 8. Limites des vérifications documentaires

**Ce que le validateur prouve :** que la spécification décrit fidèlement le code, que les 11 décisions y figurent, et que les références `fichier:ligne` sont exactes.

**Ce qu'il ne prouve pas — et qu'aucun contrôle documentaire ne peut prouver :**

1. **Que la pédagogie est valide.** Le document ne l'est pas davantage en passant au vert. Le § L5.7 l'écrit explicitement.
2. **Que les cas de test T-21 à T-33 se comportent comme annoncé.** Ils exigent un moteur ; ils sont **écrits, non exécutés**.
3. **Que le corpus d'exercices est pertinent.** Le validateur vérifie les réponses attendues, pas leur valeur pédagogique.
4. **Que Q5 fonctionne.** L'enrichissement « après analyse et validation » n'a **aucun** mécanisme described.
5. **Que le circuit Q10 est réalisable.** Aucun contenu de vérification ciblée ni de remédiation n'existe.

**Sur les 32 contrôles :** 11 sont des vérifications de code (signatures, catégories, D5, exercices), 5 de statut des décisions, 13 de références documentaires, 3 de contenu 8.2.

---

## 9. Questions encore ouvertes avant implémentation

Aucune n'est un arbitrage produit. Ce sont des choix techniques (**I-1 à I-7** dans la spec) :

| # | Question | Pourquoi elle bloque |
|---|---|---|
| **I-1** | Forme de normalisation de `expressionTache` | sans elle, la déduplication Q3 et la diversité Q4 ne sont **pas calculables** |
| **I-2** | Définition d'une « séance distincte » (Q6) | Q6 l'exige sans le définir ; aucun moyen de le savoir |
| **I-3** | Que faire si la vérification est ratée | Q3 ne le dit pas |
| **I-4** | Politique de rétention conforme à Q7 | le plafond de 500 viole Q7 aujourd'hui |
| **I-5** | Où expliquer la perte possible des données | Q7 l'exige ; aucun écran ne le fait |
| **I-6** | Contenu de la vérification ciblée et de la remédiation Q10 | le circuit est décrit, pas alimenté |
| **I-7** | Correction des deux libellés erronés (Q9) | hors périmètre de ce chantier |

**Point le plus urgent : I-1.** Tant qu'il n'est pas résolu, `expressionTache` ne peut pas distinguer deux tâches, et **Q3 comme Q4 restent inapplicables** — exactement le problème que le chantier 8.1 avait identifié, et que Q9 aggravait sans le résoudre.

---

## 10. Prochaine étape recommandée

1. **Concevoir I-1** (normalisation des tâches) — préalable à Q3 et Q4.
2. **Concevoir I-2 et I-4** — sans eux, Q6 et Q7 ne sont pas applicables.
3. **Trancher I-3** — le seul point où une décision produit reste peut-être nécessaire.
4. Décider si les **deux libellés erronés** (I-7) et le **défaut « could-tu »** sont traités dans le chantier d'implémentation.
5. **Ensuite seulement**, implémentation.

**Aucun de ces travaux n'est engagé par ce rapport. Ce chantier ne contient aucun code applicatif.**

---

## 11. Déclaration finale

Le contrat pédagogique de `OO-L1-1` est **complet et cohérent** : onze décisions arbitrées, intégrées sans contradiction, et contrôlées automatiquement.

Il **n'est pas implémenté** : aucun des trois champs décrits n'existe, aucune des règles de L5 n'est calculable par le moteur actuel, et les deux libellés erronés sont toujours en place.

**Le succès du validateur documentaire atteste que la spécification est fidèle au code. Il n'atteste en rien de la qualité de la pédagogie de Relio, ni d'une validation enseignante, qui n'a toujours pas eu lieu.**