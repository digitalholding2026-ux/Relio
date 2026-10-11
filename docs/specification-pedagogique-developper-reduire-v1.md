# SPÉCIFICATION PÉDAGOGIQUE — « DÉVELOPPER ET RÉDUIRE » (OO-L1-1)

**Version :** 1.0 — **en attente de validation pédagogique**
**Compétence :** `OO-L1-1`
**Chantier :** 8 — conception et validation
**Date :** 2026-10-11

---

> ## ⚠️ Statut de ce document
>
> **Ce document n'a PAS été validé par un enseignant.** Il est une proposition
> rédigée à partir du code réel du moteur et des documents de mission 3.
>
> Il décrit ce qui **existe déjà** dans `relio-backend` (vérifié par lecture du
> code, fichier:ligne) et ce qui **serait à construire** (proposé, non
> implémenté). Chaque section indique lequel des deux elle décrit.
>
> Tant que cette validation n'a pas eu lieu, aucune de ces propositions ne
> doit être traitée comme une règle acquise. Le § L8 liste les décisions qui
> doivent être tranchées en priorité.

---

## 0. CONVENTIONS, ET CE QUE CE DOCUMENT EST

### 0.1 Trois marqueurs

Chaque énoncé de ce document porte l'un de ces trois marqueurs :

| Marqueur | Signification |
|---|---|
| **[VÉRIFIÉ]** | Le comportement existe aujourd'hui dans le code. La référence `fichier:ligne` est donnée et rejouable. |
| **[PROPOSÉ]** | Le comportement n'existe pas. C'est une proposition de ce chantier, à valider avant toute implémentation. |
| **[À VALIDER]** | Une décision est nécessaire. La question est reportée au § L8 avec ses options. |

### 0.2 Périmètre strict

Ce document ne décrit que la compétence **`OO-L1-1`**. Les exercices
`OO-L1-2` (factorisation), `OO-L3-1` (racines) et `OO-L5-1`/`OO-L5-2` (fractions)
ne sont mentionnés que là où ils rendent la règle OO-L1-1 explicite.

### 0.3 Ce que ce document n'est pas

- Ce n'est pas une spécification d'interface. L'ergonomie est traitée par un autre chantier ; le § L6.6 décrit seulement les **besoins** pédagogiques que l'interface devra permettre.
- Ce n'est pas une refonte du moteur de correction. La règle D5, arbitrée par l'enseignant, est reprise telle quelle et n'est jamais remise en cause ici.
- Ce n'est pas une création d'exercices. Les deux exemples cités (`2(x + 3)`, `3(x − 4)`) servent de point de départ à la définition, pas de liste d'exercices à produire.

### 0.4 Trois contradictions relevées pendant l'audit, signalées sans être tranchées

Ces contradictions existent **avant** ce chantier. Elles ne sont pas créées ici et
ne sont pas arbitrées ici.

| # | Contradiction | Version A | Version B | Position retenue dans ce document |
|---|---|---|---|---|
| **C-1** | Libellé de la compétence `OO-L1-1` | « Développer une expression algébrique (distributivité, identités remarquables) » — `docs/matrice-couverture-competences.md:128` | « Développer et réduire une expression algébrique » — `backend/src/contenu/blocs.ts:29` | **Version B**, parce que c'est celle affichée à l'élève (`BlocCarte.tsx`) et celle qui correspond à l'objectif demandé. **À arbitrer.** |
| **C-2** | Nombre de signatures d'erreur | « 11 signatures » — `regles-recommandation-pedagogique.md`, `rapport-final-chantier-7-5.md:17` | 12 — `signatures.ts:11-24` | **12**, le code tranche. Les trois comptes « 11 » sont faux |
| **C-3** | Emploi du mot « maîtrise » | Interdit explicitement — `regles-recommandation-pedagogique.md:134` | Employé trois fois — `specification-diagnostic-initial.md:152`, `:192`, `:229` | Ce document **n'emploie pas** « maîtrise » pour désigner un état calculé. Le § L5 précise le vocabulaire |

---

# LIVRABLE 1 — DÉFINITION DE LA COMPÉTENCE

## L1.1 Ce que l'élève doit être capable de faire

**[PROPOSÉ]** L'élève **maîtrise** `OO-L1-1` — « développer et réduire une
expression algébrique » — lorsqu'il est capable, **sans aucune aide et sur un
exercice qu'il n'a pas déjà vu**, de :

1. **Développer** — distribuer un facteur sur chaque terme d'une parenthèse, y
   compris lorsque ce facteur est preceded du signe « − » ;
2. **Réduire** — regrouper les termes de même nature (les `x` entre eux, les
   nombres entre eux) en un terme unique ;
3. **Justifier oralement ou par écrit** au moins une fois pourquoi le signe
   change, ou pourquoi deux termes se regroupent.

Le troisième point est ce qui distingue « connaître une règle » de « savoir
l'utiliser seul ». Une réponse juste obtenue par tâtonnement ne prouve que le
point 1-2.

## L1.2 Connaissances préalables

**[VÉRIFIÉ]** Le code déclare `OO-L1-1.prerequis = []` (`blocs.ts:31`). C'est un
choix de conception : `OO-L1-1` est le premier objectif du bloc B1.

**[PROPOSÉ]** Cette absence de prérequis est **mathématiquement fausse** et
pédagogiquement coûteuse. Développer suppose au minimum :

| Prérequis | Pourquoi il est nécessaire | Est-il déclaré ailleurs ? |
|---|---|---|
| Calcul littéral dans une parenthèse : `a(b + c) = ab + ac` | C'est la règle de base de toute la compétence | Non déclaré |
| Sens du signe « − » devant un terme : `-3x` est l'opposé de `3x` | Le piège le plus fréquent du corpus est exactement celui-ci | Non déclaré |
| Terme constant / terme en `x` : savoir nommer ce que contient une expression | Nécessaire pour regrouper | Non déclaré |
| Regroupement de termes semblables : `2x + x = 3x` | C'est la deuxième moitié de la compétence | Non déclaré |

**[À VALIDER]** — L8-Q1. Soit on déclare ces prérequis, soit on assume que
`OO-L1-1` les englobe et on ne parle plus de « connaissances préalables ».

## L1.3 Les étapes de raisonnement attendues

**[PROPOSÉ]** L'ordre est fixed et observable. Il correspond déjà, sans le dire,
à la structure des trois indices existants de `MVP-B1-E1`
(`exercices.ts:36-38`) :

| Étape | Ce que l'élève fait | Ce qui trahit qu'elle est sautée |
|---|---|---|
| **1. Repérer** | Identifier le facteur à distribuer (le nombre ou le `x` devant la parenthèse) | Une réponse qui ne contient qu'un terme en `x` : rien n'a été distribué |
| **2. Distribuer** | Multiplier **chaque** terme entre parenthèses par ce facteur | Un seul terme de la parenthèse a été traité |
| **3. Propager le signe** | Si le facteur est précédé de « − », **changer le signe des deux termes** | Les deux termes sont bons mais de signes contraires : c'est le piège `signe_non_distribue` |
| **4. Écrire** | Écrire le résultat intermédiaire, sans regrouper | Une réponse comme `3x + 6 - x - 5` : juste numériquement, mais intermédiaire |
| **5. Regrouper** | Additionner les coefficients des termes en `x`, additionner les constantes | `2x + 1 + x` : les termes ne sont pas regroupés |

**[VÉRIFIÉ]** L'étape 4 ne pose pas de problème de correction : `3x + 6 - x - 5`
vaut `2x + 1`, donc le moteur le juge `correct`. L'élève n'est pas pénalisé pour
avoir montré son travail intermédiaire. C'est un bon choix, à conserver.

## L1.4 Types d'expressions couverts par le périmètre initial

**[VÉRIFIÉ]** Ce que le moteur sait effectivement traiter. Source :
`backend/src/lib/analyseur-expression.ts`, grammaire `AnalyseurSyntaxique`
(lignes 175-304).

| Catégorie | Exemple | Accepté ? | Source |
|---|---|---|---|
| Distributivité par un nombre | `3(x + 2)` | ✅ | `analyseur-expression.ts:214-240` |
| Distributivité avec signe « − » | `3(x + 2) − (x + 5)` | ✅ | idem, `-` unaire `:267-274` |
| Produit de deux parenthèses | `(x + 3)(x − 2)` | ✅ | multiplication implicite `:232-236` |
| Produit d'un terme par deux parenthèses | `2(x + 3)(x + 1)` | ✅ | boucle `:214-236` |
| Carré d'une parenthèse | `(2x − 1)²` | ✅ | `:242-258` |
| Puissances | `2x^2 + 3x` | ✅ | exposant entier 0-16 `:252-254` |
| Terme seul | `3x`, `-x` | ✅ | `:134-138`, `:267-274` |
| Lettre autre que `x` | `2(y + 3)` | ❌ | `Caractère non reconnu : « y ».` `:152` |
| Division par une expression | `(x+1)/(x-1)` | ❌ | `La division par une expression contenant x n'est pas supportée ici.` `:392` |
| Racine | `√(2x)` | ❌ | racine absente de la grammaire d'expressions |
| Fraction typographique | `\frac{2x}{3}` | ❌ | `:152` |
| Identité remarquable `a² − b²` | posée directement | ❌ par le moteur, mais voir L1.5 | ce n'est pas du développement |

## L1.5 Les cas exclus au départ

**[PROPOSÉ]** Exclus, avec une raison vérifiable pour chacun. Un périmètre qui
ne dit pas ce qu'il exclut déborde toujours ensuite.

| Cas exclu | Raison | Ce que fait le code aujourd'hui |
|---|---|---|
| Équations : `2(x + 3) = 5x` | Développer est une étape, pas l'objectif. Résoudre relève de `OO-L8-1`, hors MVP | `egalite.ts:134-138` refuse si les deux membres ne sont pas égaux |
| Factorisation comme réponse | C'est `OO-L1-2`. Un élève qui factorise quand on lui demande de développer ne doit pas être valorisé | Le moteur compare les **valeurs** : `2(x+3)` vaut `2x+6`, donc accepté |
| Termes d'un seul membre, `2x + 3 − 5x` | Prérequis de L1.2, pas la compétence. Utile en diagnostic, pas en évaluation | Accepté et jugé juste |
| Expressions à plus de 16 termes | Borné par le moteur, pas par la compétence | `Degré trop élevé.` `:453` |
| Forme imposée (« donne la forme développée ») | Les trois exercices `OO-L1-1` ont `regleForme: null` (`exercices.ts:33, 58, 82`) : **aucune forme n'est exigée** | Le verdict `resultat_juste_consigne_non_respectee` est donc **inatteignable** sur cette compétence — voir L3.2 |

## L1.6 Connaître une règle ≠ savoir l'utiliser seul

**[VÉRIFIÉ]** Le moteur **ne peut pas** faire cette différence aujourd'hui, et
c'est le cœur du problème que ce chantier doit documenter.

**[VÉRIFIÉ]** Le niveau d'aide est une fonction du **nombre d'échecs**, et de
rien d'autre (`backend/src/contenu/tutorat.ts:202-206`) :

```ts
export function niveauPourNbEchecs(nbEchecs: number): NiveauAide {
  if (nbEchecs <= 0) return 1;
  if (nbEchecs === 1) return 2;
  return 3;
}
```

La catégorie d'erreur n'entre **pas** dans ce calcul. Un élève qui se trompe de
signe trois fois et un élève qui oublie de regrouper trois fois reçoivent la
même escalade, et au niveau 3 la même aide.

**[VÉRIFIÉ]** Ce que le moteur sait faire, et qui va dans la bonne direction :
la signature d'erreur est recherchée **même sur une réponse juste**
(`correction.ts:376-379`) et l'origine du texte d'aide est retournée
(`tutorat.origine ∈ {signature, indice, objectif, forme, bilan, generique}`).
La matière est là ; lebranchement sur le niveau n'est pas fait.

**La différence à établir, en langage observable :**

| | Connaître la règle | Savoir l'utiliser seul |
|---|---|---|
| **Ce que l'élève produit** | Il sait reformuler la règle, ou la reproduire sur un exemple résolu | Il réussit sur un énoncé qu'il n'a pas déjà vu |
| **Ce que le système peut observer** | Un indice demandé **et lu** ; un énoncé d'exemple réussi | Une réponse juste sans qu'aucune aide ait été demandée |
| **Ce que le système ne peut pas observer** | S'il a *lu* l'indice ou l'ignore | La part de hasard, de plagiat entre exercices, de reconnaissance |

**Conclusion honnête :** la différence entre les deux colonnes n'est mesurable
que sur la colonne de droite. Tout le reste est une hypothèse sur un processus
mental. Le § L5.2 en tire les conséquences, et le § L5.5 le dit explicitement :
**le système ne prétendra pas détecter « sait » ; il mesurera « réussit sans
aide »**, qui est un plancher, pas une preuve.

---

# LIVRABLE 2 — TAXONOMIE DES ERREURS

## L2.1 Deux niveaux de vocabulaire, et pourquoi

**[VÉRIFIÉ]** Le moteur distingue deux niveaux (`signatures.ts`, `tutorat.ts:122-166`) :

- la **signature** — ce que produit une réponse d'élève précise et reproductible ;
- la **catégorie** — le regroupement pédagogique qui sert au suivi.

La correspondance est **explicite et totale** : chaque signature a une catégorie,
aucune ne reste sans catégorie (`tutorat.ts:153-166`).

Deux propriétés de ce catalogue sont des **garanties**, pas des hasards, et il
faut les préserver dans toute évolution :

1. **Catalogue fermé.** Toute réponse qui ne correspond exactement à aucun piège
   est classée `hors_perimetre` → catégorie `erreur_non_identifiee`
   (`signatures.ts:11`, `tutorat.ts:165`). On ne devine jamais une difficulté
   qu'on n'a pas observée.
2. **Une cause inconnue ne devient jamais une cause plausible.** `hors_perimetre`
   donne `erreur_non_identifiee`, jamais une catégorie « scapegoat »
   (`tutorat.ts:148-151`).

## L2.2 Les 8 catégories (catalogue fermé)

**[VÉRIFIÉ]** `tutorat.ts:122-133`, vocabulaire fermé :

| # | Catégorie | Ce que cela signifie pour l'élève | Concernée par OO-L1-1 ? |
|---|---|---|---|
| 1 | `oubli_de_distribuer_un_facteur` | Le facteur n'a pas été distribué sur un terme | ✅ oui (cœur) |
| 2 | `erreur_de_signe` | Un signe s'est inversé / perdu | ✅ oui (cœur) |
| 3 | `reduction_incomplete` | Les termes n'ont pas été regroupés | ✅ oui (cœur) |
| 4 | `facteur_commun_non_identifie` | Factorisation demandée, non faite | ❌ (`OO-L1-2`) |
| 5 | `simplification_de_racine_incomplete` | Carré parfait non extrait / base fausse | ❌ (`OO-L3-1`) |
| 6 | `fraction_non_reduite` | Fraction pas irréductible | ❌ (`OO-L5-1/2`) |
| 7 | `reponse_illisible` | La saisie n'a pas pu être analysée | ✅ oui (entrée) |
| 8 | `erreur_non_identifiee` | Cause inconnue — ne rien affirmer | ✅ oui (filet de sécurité) |

**Conséquence pour ce chantier :** sur `OO-L1-1`, seules **4 catégories sur 8**
sont atteignables — `oubli_de_distribuer_un_facteur`, `erreur_de_signe`,
`reduction_incomplete`, `reponse_illisible`, plus `erreur_non_identifiee` en
repli. Les 4 autres sont hors périmètre de la compétence.

## L2.3 Signatures → catégories, pour OO-L1-1

**[VÉRIFIÉ]** `tutorat.ts:153-166` :

| Signature | Catégorie | Un exemple de réponse qui la déclenche sur OO-L1-1 |
|---|---|---|
| `signe_non_distribue` | `oubli_de_distribuer_un_facteur` | `2x + 11` au lieu de `2x + 1` (le − n'a struck que le terme constant) |
| `termes_non_collectes` | `reduction_incomplete` | `2x + 1 + x` (les `x` non regroupés) |
| `coefficient_multiplicatif_oublie` | `oubli_de_distribuer_un_facteur` | *(non atteignable sur les 3 exercices actuels)* |
| `hors_perimetre` | `erreur_non_identifiee` | toute réponse fausse hors des pièges listés |
| *(illisible)* | `reponse_illisible` | saisie non analysable |

**Point important :** `signe_non_distribue` et `erreur_de_signe` sont deux
catégories **distinctes** (`oubli_de_distribuer_un_facteur` vs `erreur_de_signe`)
mais partagent un mécanisme (le signe « − » devant une parenthèse). Le L1.3-étape-3
(piège `signe_non_distribue`) tombe donc dans `oubli_de_distribuer_un_facteur`, pas
dans `erreur_de_signe`. **[À VALIDER]** — L8-Q2 : faut-il distinguer
« distributivité non faite » et « distributivité mal signée » pour OO-L1-1, ou
les regrouper sous une catégorie « signe en distributivité » ? Le code les sépare
déjà ; ce document assume la séparation existante.

## L2.4 Ce que la taxonomie garantit, et ce qu'elle ne garantit pas

**Elle garantit :**
- Qu'aucune cause ne sera affirmée sans piège correspondant (pas d'invention).
- Qu'une réponse hors périmètre ne soit pas dramatisée.
- Que le suivi ne remonte qu'un signal observé.

**Elle ne garantit pas :**
- Que le piège Capturera la cause « réelle » : la détection se fait par **égalité
  de valeur** avec une liste de pièges (`exercices.ts`). Si l'élève fait une erreur
  non listée, la catégorie sera `erreur_non_identifiee` — une **absence de
  détection**, pas une absence d'erreur.
- Qu'un élève qui réussit sans faute sur un exercice maîtrise pour autant (§ L1.6).

---

# LIVRABLE 3 — ARBRE DE DÉCISION (RÈGLE DE CORRECTION)

## L3.1 Les trois axes, puis le verdict

**[VÉRIFIÉ]** `correction.ts` calcule trois axes indépendants, puis dérive un
verdict. Les trois axes sont :

| Axe | Question | Sortie |
|---|---|---|
| **1. Justesse** | La valeur écrite est-elle égale à la valeur attendue ? | `juste : boolean` (comparaison exacte de valeurs, pas de chaînes) |
| **2. Forme** | La réponse respecte-t-elle la forme éventuellement exigée ? | `conforme` / `non_conforme` / `indeterminee` |
| **3. Achèvement** | Le travail est-il complet (ex. racine non finie) ? | `acheve` / `inacheve` |

## L3.2 L'ordre de décision D5 — et ce qu'il rend inatteignable sur OO-L1-1

**[VÉRIFIÉ]** `deriverVerdict`, `correction.ts:328-342`. L'ordre **n'est pas
décoratif** :

```
1. si !juste                      → incorrect          (une réponse fausse n'est
                                                        jamais « juste mais mal formée »)
2. si achevement === 'inacheve'   → partiellement_correct  (AVANT la forme : l'étape
                                                        qui reste n'est pas un réécriture)
3. si formeRespectee === false    → resultat_juste_consigne_non_respectee
4. si formeExigee && forme==null  → a_determiner
5. sinon                          → correct
```

**Contrainte propre à OO-L1-1 :** les trois exercices ont `regleForme: null`
(`exercices.ts:33, 58, 82`). Aucune forme n'est donc exigée. Conséquences :

- **étape 3 inatteignable** : pas de « juste mais forme non demandée » ;
- **étape 4 inatteignable** : `a_determiner` exige une forme exigée ;
- `correct` est obtenu pour toute valeur juste (la formeReturning `null` +
  `regleForme null` → statut `correcte`, `correction.ts:400-402`).

**Bilan des verdicts sur OO-L1-1 : seuls `correct` et `incorrect` sont
atteignables.** Les cinq verdicts D5 existent, mais cette compétence n'en
exploite que deux aujourd'hui. Le L3.3 propose d'enrichir, sans casser D5.

## L3.3 Arbre de décision enrichi — proposition

**[PROPOSÉ]** L'arbre ci-dessous **respecte strictement D5** pour le verdict, et
ajoute **par-dessus** la notion de **question de diagnostic** quand il manque une
information. Il ne remplace pas D5 ; il l'habille.

```
ENTRÉES :
  valeur          = valeur de la réponse élève (analysée)
  attendue        = valeur attendue
  formeExigee     = (exercice.regleForme != null)
  formeResp       = conforme | non_conforme | indeterminee
  achevement      = acheve | inacheve
  piegesTouches   = [signatures des pièges dont la valeur == valeur élève]

ÉTAPE A — Valeur juste ?
  SI NON :
    ├─ SI la saisie était illisible → statut « illisible », pas de verdict math.
    │     ACTION : poser une question de clarification (L4.3), jamais un indice
    │     de méthode, car on ne sait pas encore ce que l'élève a fait.
    ├─ SI au moins un piège touché → catégorie = CATEGORIE_PAR_SIGNATURE[piège]
    │     ACTION : aide ciblée sur cette catégorie (L4.2), niveau selon L4.1.
    │     signatureDuPiege cherche d'abord par égalité de valeur.
    └─ SINON (aucun piège) → catégorie = erreur_non_identifiee (hors_perimetre)
          ACTION : aide neutre, sans cause affirmée (L4.2).
          NE PAS nommer de cause plausible.

ÉTAPE B — Valeur juste, mais quoi de plus ?
  SI achevement === 'inacheve'  → verdict = partiellement_correct   (étape 2)
        ACTION : aide « il reste une étape », sur l'étape manquante. (Rare sur
        OO-L1-1 : inatteignable aujourd'hui, atteint si on ajoute une forme.)
  SINON SI formeExigee ET formeResp === false → resultat_juste_consigne_non_respectee
        ACTION : aide « réécris sous la forme demandée ». (Inatteignable sur
        OO-L1-1 actuel, atteint si on impose une forme à un exercice futur.)
  SINON SI formeExigee ET formeResp === indeterminee → a_determiner
        ACTION : NE PAS conclure. Poser la question de diagnostic sur la FORME
        (L4.3) pour lever l'indétermination avant toute aide de méthode.
  SINON → verdict = correct
        ACTION : si l'élève a déjà échoué, marquage « acquis fragile » → Program.
        (voir L5.3)
```

## L3.4 La règle qui manque aujourd'hui, et c'est celle du L3.3 étape B

**[VÉRIFIÉ]** Aujourd'hui, quand `juste == true` et qu'aucune forme n'est exigée,
le verdict est `correct` et le suivi compte une réussite (`progression.ts:74-88`).
Rien ne distingue « première fois juste » de « juste après 3 aides ».

**[PROPOSÉ]** C'est exactement le cas où le système doit **ne rien conclure sur la
maîtrise** et, si l'élève a des échecs antérieurs, le renvoyer au § L5
(maitrise exige plusieurs preuves indépendantes). D5 reste intact : le verdict
mathématique est `correct` ; c'est l'**interprétation pédagogique** qui change, et
elle vit dans le suivi, pas dans le verdict.

---

# LIVRABLE 4 — RÈGLE DU TUTORAT (choix des questions)

## L4.1 Le principe : l'aide se choisit par la cause, pas par le compteur

**[VÉRIFIÉ]** Ce que le code fait **aujourd'hui** :

- Le **niveau** (1/2/3) est fonction **du nombre d'échecs seulement**
  (`tutorat.ts:202-206`) : 0 échec → niveau 1 ; 1 échec → niveau 2 ; ≥2 → niveau 3.
- Le **contenu** du niveau 1 est choisi par la **signature reconnue**
  (`ORIENTATIONS_PAR_SIGNATURE`) ; sinon le texte vient de la leçon de l'objectif
  (`AIDES_PAR_OBJECTIF[].action`) ; sinon aide neutre (`tutorat.ts`, en-tête).

Autrement dit : **la catégorie pilote déjà le texte du premier niveau**, mais
**pas l'escalade**. Deux élèves qui échouent tous les deux une fois, l'un en
signe, l'autre en regroupement, reçoivent le même palier, mais un texte
d'orientation différent — bien.

**[PROPOSÉ]** Améliorer l'escalade sans casser le déterministe :

| Situation | Niveau | Ce qui est affiché |
|---|---|---|
| 1ʳᵉ échec, cause reconnue | 1 (Orienter) | **une question ciblée sur la cause** (« le signe − change-t-il le signe des deux termes ? ») |
| 2ᵉ échec, **même** cause | 2 (Expliquer) | la règle, puis **une étape sur un autre exemple** — jamais la réponse |
| 2ᵉ échec, **cause différente** | 1 (Orienter) | on rebascule sur une question ciblée : la cause a changé, l'escalade ne s'applique pas |
| 3ᵉ échec | 3 (Accompagner) | la prochaine opération **sur son exercice**, sans publier la réponse |

**Règle d'or à écrire dans le code et les tests :** *« l'aide monte d'un cran
quand l'élève échoue **pour la même raison**, et **redescend/change de cible**
quand il échoue **pour une autre raison**. »* C'est le seul changement de
comportement proposé, et il est testable sans IA.

## L4.2 Le script d'aide, par cause — pour OO-L1-1

**[VÉRIFIÉ]** Les formulations existantes viennent de `AIDES_PAR_OBJECTIF['OO-L1-1']`
(`aides.ts:79-89`) et des indices d'exercice (`exercices.ts:34-38`). **Elles ne
doivent pas être réécrites** dans ce chantier. Le tableau ci-dessous ne fait que
**associer** les causes aux textes déjà présents.

| Cause (catégorie) | Question niveau 1 (déjà dans le code) | Origine du texte |
|---|---|---|
| `oubli_de_distribuer_un_facteur` / `erreur_de_signe` | « qu'est-ce qui se passe quand le nombre devant la parenthèse se distribue dans chacun d'eux ? » | `AIDES_PAR_OBJECTIF.question` (aides.ts:88) |
| `reduction_incomplete` | « regarde les deux termes : qu'est-ce qui se passe… » + l'action « puis regroupe les x et les nombres » | action (aides.ts:80-81) |
| `erreur_non_identifiee` (repli) | **Aucune cause affirmée.** Reprendre la question d'objectif, qui est neutre. | idem |

## L4.3 La question de diagnostic — quand le système manque d'information

C'est le point explicitement demandé et **absent du code**. On ne pose une
question de clarification que dans **deux** cas, jamais par défaut :

1. **Réponse illisible** (catégorie `reponse_illisible`) : on ne sait pas ce que
   l'élève a écrit → on redemande une saisie lisible, **sans indice de méthode**.
2. **Forme indéterminée** (verdict `a_determiner`) : on ne sait pas si la forme
   est respectée → on demande à l'élève de reformuler ou de préciser, **avant**
   toute aide de méthode. (Inatteignable sur OO-L1-1 actuel ; conçu pour les
   futurs exercices à forme exigée.)

**[PROPOSÉ]** — Format d'une question de diagnostic :
- **une** question fermée, courte ;
- **deux ou trois choix** (pas de saisie libre) ;
- **une** conséquence par réponse.

Exemple (réponse illisible) :
> « Ton expression n'a pas pu être lue. Réessaie en écrivant le résultat, par exemple : 2x + 1 »
> → si l'élève réessaie et réussit : on compte un échec « saisie », pas une
> erreur de concept → catégorie `reponse_illisible`, aide = « réécris plus lisiblement ».

**Ce qu'on ne fait pas :** on ne pose **jamais** de question de diagnostic pour
« deviner la cause » d'une erreur déjà identifiée. La cause est lue dans la
signature ; le diagnostic n'est que pour l'information **manquante**.

---

# LIVRABLE 5 — EXIGENCES DE RÉUSSITE ET DE MAÎTRISE

## L5.1 Le problème à résoudre, énoncé franchement

**[VÉRIFIÉ]** Aujourd'hui, une seule réponse juste fait monter le compteur
(`progression.ts:74-88`). Mais `progression.ts:8-25` dit noir sur blanc que
« `correcte` seul ne prouve rien » et que **`acquis_confirme` est hors périmètre,
le moteur ne l'atteint pas**. Le code est donc honnête sur sa limite — c'est la
spécification qui doit décider ce qu'on fait de cette limite.

## L5.2 Trois niveaux de réussite, du plus faible au plus fort

**[PROPOSÉ]** Trois statuts distincts, à ne pas confondre :

| Niveau | Définition | Ce qui le fonde | Confiance |
|---|---|---|---|
| **Réussite isolée** | 1 réponse juste | 1 item | très faible — peut être du hasard |
| **Acquis fragile** | 2 réussites **sur 2 exercices différents**, sans aide | 2 items indépendants | moyenne — début réel, mais court |
| **Maîtrise** | **au moins 3 réussites sans aide, sur ≥2 exercices différents, dont 1 après une vérification ultérieure** (voir L5.4) | 3+ items, avec intervalle | élevée — **recommandé, à valider** |

## L5.3 La règle des trois, réconciliée avec le moteur

**[VÉRIFIÉ]** `progression.ts` applique une règle des trois (« 3 réussites sans
erreur → borne d'erreur ~ 3/n ≤ 100 % ») et exige **4 items** pour conclure
(`progression.ts:82-83`). Le moteur **ne conclut jamais** à `acquis_confirme`.

**[PROPOSÉ]** Aligner le statut d'**affichage** sur cette borne déjà calculée :
- 0 donnée → `non_evalue` ;
- 1 erreur → `signal` ;
- ≥2 erreurs cohérentes → `hypothese` (à faire confirmer par l'enseignant) ;
- **3+ réussites sans aide sur ≥2 exercices différents** → afficher
  « **acquis fragile** » (pas « maîtrisé ») ;
- le passage à « maîtrisé » exige en plus **une vérification ultérieure** réussie
  (L5.4).

**Le mot « maîtrisé » n'est employé qu'après vérification ultérieure.** C'est ce
qui répond à l'interdiction de `regles-recommandation-pedagogique.md:134`.

## L5.4 La vérification ultérieure — le « peut-être qu'il avait deviné »

**[PROPOSÉ]** C'est la pièce manquante, et c'est la réponse directe à « connaître la
règle ≠ savoir l'utiliser seul » (L1.6).

**Principe :** après 2 réussites, on propose un exercice **différent** sur la
même compétence, **quelques jours plus tard**, avec une **forme d'énoncé
changée** mais le **même niveau de difficulté**.

Exemple de vérification pour `MVP-B1-E1` (`3(x+2) − (x+5)`) :
> « Développe et réduis C = 2(x − 3) + (x + 1). »
> (mêmes compétences — distributivité + signe − + regroupement — mais
> chiffres et signes différents, donc pas réciter la solution.)

**Règles :**
- la vérification **ne compte pas** comme un item de maîtrise « gratuit » : elle
  est la **condition** de la maîtrise, pas un item de plus ;
- elle n'est **pas** affichée comme un contrôle punitif (« retiens-tu ? ») mais
  comme une « nouvelle façon de le faire » ;
- si la vérification est ratée → retour au statut précédent (« acquis fragile »),
  **sans effacer** les réussites antérieures.

## L5.5 Ce que le système ne prétendra pas détecter

**[PROPOSÉ]** Trois affirmations que ce document refuse de faire, pour rester
honnête :

1. **Le système ne dira pas « tu sais la règle »** — il constatera « tu as réussi
   sans aide sur N exercices différents ».
2. **Le système ne dira pas « tu as compris »** — la compréhension est un
   processus mental non observable depuis une réponse.
3. **Une réussite unique ne conclura rien** — elle incrémente un compteur, rien de
   plus.

---

# LIVRABLE 6 — SUIVI ET STOCKAGE LOCAL (données client)

## L6.1 Ce qui est stocké aujourd'hui

**[VÉRIFIÉ]** Le suivi est **local au navigateur**, dans une clé
`relio.observations.v1` (`frontend/src/lib/observations.ts`), plafonnée à **500
observations**. Aucune persistance serveur, aucun compte élève, aucun appel IA.

**[VÉRIFIÉ]** Le serveur n'a **aucun** état de progression : `parcours.ts` renvoie
les corrections, `progression.ts` est une **fonction pure** recalculée à partir
d'un journal fourni par le client.

## L6.2 Les données minimales pour la règle du § L5

**[PROPOSÉ]** Pour être capable d'afficher « acquis fragile » puis « maîtrisé »,
le journal local doit porter, par réponse :

| Champ | Pourquoi | Existe ? |
|---|---|---|
| `exerciceId` | savoir si 2 réussites viennent de 2 exercices différents | ✅ oui |
| `objectifId` | rattacher à `OO-L1-1` | ✅ oui |
| `statut` (`correcte`/`fausse`/…) | compter réussites / erreurs | ✅ oui |
| `signatureErreur` / `categorie` | ne recompter que des erreurs **de même catégorie** (L4.1) | ✅ oui |
| `nbEchecsAuPrecedent` | savoir si l'élève échouait avant (succès « fragile ») | ✅ oui (le client connaît l'historique de l'exercice) |
| `estVerificationUlterieure` | distinguer la condition de maîtrise (L5.4) | ❌ **à ajouter** |
| `horodatage` | l'intervalle « quelques jours » entre succès et vérification | ✅ oui (observations horodatées) |

**Un seul champ manque : `estVerificationUlterieure`.** Sans lui, la règle L5.3
n'est pas calculable.

## L6.3 Ce que ce chantier ne fait pas

**[VÉRIFIÉ]** + **à respecter strictement** :
- **aucune** politique de conservation durable n'est conçue ici — la question est
  laissée à L8-Q7 ;
- le plafond de 500 et la clé `v1` **restent tels quels** ;
- le serveur **ne devient pas** persistant : la progression reste une fonction
  pure recalculée côté client.

## L6.4 Ce que le suivi doit remonter à l'enseignant

**[PROPOSÉ]** Vue enseignante minimale, alimentée par le même journal :
- par objectif : `statut` + compteurs (déjà faits par `progression.ts`) ;
- par **catégorie** : nombre d'occurrences, pour cibler une reprise (fait par
  `suivi.ts:169`, agrégation par catégorie) ;
- **jamais** de cause affirmée quand la catégorie est `erreur_non_identifiee` —
  la garantie du § L2.1 tient ici.

---

# LIVRABLE 7 — CAS DE TEST

## L7.1 Ce que ces cas testent

Des cas exécutables sur le moteur **actuel**, sans rien modifier. Ils servent
de **contrat** : si une évolution du moteur casse l'un d'eux, c'est qu'elle a
changé la règle D5 ou la taxonomie, donc qu'elle doit être validée.

Les entrées sont les 3 exercices `OO-L1-1` existants :
- **E1** `MVP-B1-E1` : `A = 3(x + 2) − (x + 5)`, attendu `2x + 1`
- **E2** `MVP-B1-E2` : `B = (2x − 1)²`, attendu `4x^2 − 4x + 1`
- **E3** `MVP-B1-E3` : `C = (x + 3)(x − 2) − 2(x − 1)`, attendu `x^2 - x - 4`

## L7.2 Cas de correction (verdict + catégorie) — [VÉRIFIÉ] aujourd'hui

| # | Ex. | Saisie élève | Verdict D5 | Signature | Catégorie | Statut |
|---|---|---|---|---|---|---|
| T-01 | E1 | `2x + 1` | `correct` | — | — (`null`) | `correcte` |
| T-02 | E1 | `3x + 6 - x - 5` (intermédiaire) | `correct` | — | — | `correcte` |
| T-03 | E1 | `4x + 1` | `incorrect` | `signe_non_distribue` | `oubli_de_distribuer_un_facteur` | `fausse` |
| T-04 | E1 | `2x + 11` | `incorrect` | `signe_non_distribue` | `oubli_de_distribuer_un_facteur` | `fausse` |
| T-05 | E1 | `2x + 1 + x` | `incorrect` | `termes_non_collectes` | `reduction_incomplete` | `fausse` |
| T-06 | E1 | `2x` | `incorrect` | `termes_non_collectes` | `reduction_incomplete` | `fausse` |
| T-07 | E1 | `2(x + 0.5) - x` *(équivalent)* | `correct` | — | — | `correcte` |
| T-08 | E2 | `4x^2 + 4x + 1` | `incorrect` | `signe_non_distribue` | `oubli_de_distribuer_un_facteur` | `fausse` |
| T-09 | E2 | `2x^2 - 2x + 1` | `incorrect` | `hors_perimetre` | `erreur_non_identifiee` | `fausse` |
| T-10 | E2 | `4x^2 - 4x` | `incorrect` | `termes_non_collectes` | `reduction_incomplete` | `fausse` |
| T-11 | E3 | `x^2 - x - 4` | `correct` | — | — | `correcte` |
| T-12 | E3 | `x^2 + 3x - 4` | `incorrect` | `signe_non_distribue` | `oubli_de_distribuer_un_facteur` | `fausse` |
| T-13 | E3 | `x^2 + x - 4` | `incorrect` | `hors_perimetre` | `erreur_non_identifiee` | `fausse` |
| T-14 | E3 | `x^2 - x - 8` | `incorrect` | `signe_non_distribue` | `oubli_de_distribuer_un_facteur` | `fausse` |
| T-15 | E1 | `2x + 1  zzz` (illisible) | pas de verdict | — | `reponse_illisible` | rejet 422 |

**Points de lecture :**
- **T-02** et **T-07** encodent une décision pédagogique forte : la **forme
  intermédiaire est acceptée**. L'élève qui montre son travail n'est pas puni.
- **T-13** est le cas le plus intéressant : l'élève a oublié le terme `+ 3x` dans
  le premier produit. Le moteur le classe `hors_perimetre` → `erreur_non_identifiee`,
  donc **il ne lui dit pas** « tu as oublié le 3x ». C'est voulu (ne rien inventer),
  mais c'est une aide **moins précise** pour une erreur **réelle**. → **L8-Q5**.
- **T-09** : même chose sur le carré — `2x^2` trahit « seul x a été mis au carré »,
  mais le moteur refuse de l'affirmer. → **L8-Q5**.

## L7.3 Cas de tutorat (niveau d'aide) — [VÉRIFIÉ] aujourd'hui

| # | Situation | Niveau attendu | Origine du texte attendue |
|---|---|---|---|
| T-16 | E1, 0 échec, 1ʳᵉ saisie fausse | **1** — Orienter | `signature` (`ORIENTATIONS_PAR_SIGNATURE`) |
| T-17 | E1, 1 échec, 2ᵉ saisie fausse | **2** — Expliquer | `indice` (palier 2) ou `objectif.exemple` |
| T-18 | E1, 2 échecs, 3ᵉ saisie fausse | **3** — Accompagner | `indice` (palier 3) |
| T-19 | E1, erreur `hors_perimetre`, 1ʳᵉ saisie | **1** | `objectif` (pas de cause affirmée) |
| T-20 | Réponse juste, 2 échecs antérieurs | verdict `correct`, **mais** statut de suivi ≠ « maîtrisé » | — |

**Le cas T-20 est le cœur du LIVRABLE 5** : le verdict mathématique est `correct`,
et pourtant la conclusion pédagogique doit être prudente.

## L7.4 Cas de progression (suivi) — [VÉRIFIÉ] aujourd'hui

| # | Situation | Statut attendu | Commentaire |
|---|---|---|---|
| T-21 | 0 réponse sur `OO-L1-1` | `non_evalue` | jamais dégradé |
| T-22 | 1 réponse fausse | `signal` | |
| T-23 | 2 réponses fausses | `hypothese` | à confirmer par l'enseignant |
| T-24 | 3 réponses justes, 0 fausse, **total < 4** | `non_evalue` | règle des trois : pas encore de conclusion |
| T-25 | 3 justes + 1 fausse | `signal` | |
| T-26 | 3 justes sur **1 seul exercice** | rien de concluant | **L8-Q4 : faut-il exiger ≥2 exercices différents ?** |
| T-27 | 3 justes sur **2 exercices différents** + vérification | **« maîtrisé »** | première fois où le mot est permis (§ L5.4) |

**T-24 et T-26 sont les deux seuls cas où la règle proposée (L5.2) modifie le
comportement actuel.** Le reste est déjà correct.

## L7.5 Cas où le système doit **refuser** de conclure

| # | Situation | Comportement exigé |
|---|---|---|
| T-28 | Cause inconnue (`erreur_non_identifiee`) | Aucune catégorie de difficulté plausible n'est enregistrée |
| T-29 | Une seule réussite | Aucun statut de maîtrise n'est affiché |
| T-30 | Élève qui réussit en recopiant la réponse d'un indice | Le système ne peut pas le détecter → **ne pas prétendre l'avoir détecté** (§ L5.5) |

---

# LIVRABLE 8 — QUESTIONS DE VALIDATION

## L8.0 Comment lire cette section

Rien de ce qui suit n'est décidé. Ce sont les **arbitrages qui manquent**, avec
leur option par défaut (celle que ce document a écrite) et leur conséquence si on
ne tranche pas.

| # | Question | Option retenue par défaut | Risque si non tranchée |
|---|---|---|---|
| **Q1** | Les prérequis de `OO-L1-1` doivent-ils être déclarés ? (L1.2) | Oui : distributivité de base, signe « − », termes constants, regroupement | Un élève qui ne sait pas ce qu'est un terme constant est mesuré sur « développement » |
| **Q2** | `signe_non_distribue` doit-il rester distinct de `erreur_de_signe` pour OO-L1-1 ? (L2.3) | Distinct, comme le code le fait déjà | Risque de regroupement trop fin, ou trop large |
| **Q3** | Le seuil « acquis fragile » est-il **3 réussites sans aide** ? (L5.3) | Oui, aligné sur la règle des trois déjà codée | Seuil arbitraire, non justifié par le moteur |
| **Q4** | Faut-il exiger **≥2 exercices différents** pour conclure ? (L5.2) | Oui | Un élève qui réussit 3 fois le même exercice est compté comme maîtrisant |
| **Q5** | Faut-il **enrichir** les pièges pour couvrir les erreurs hors périmètre ? (L7.2, T-09, T-13) | **Non pour ce chantier** — on ne touche pas aux exercices | L'élève « a oublié le 3x » reçoit une aide neutre au lieu d'une aide ciblée |
| **Q6** | Faut-il un **délai** entre succès et vérification ultérieure ? (L5.4) | « quelques jours », non chiffré | Sans délai, la vérification ne prouve rien de plus que l'exercice |
| **Q7** | Quelle **conservation des données locales** ? (L6.3) | Rien de décidé — hors périmètre | Perte du journal au vidage du navigateur, sans que personne ne l'ait choisi |
| **Q8** | Faut-il ajouter `estVerificationUlterieure` au journal local ? (L6.2) | Oui — c'est le seul champ manquant | La règle du § L5 n'est pas calculable |
| **Q9** | Le libellé de la compétence est-il « développer **et réduire** » ? (C-1) | Oui | Le backend et la matrice affichent deux libellés différents |

## L8.1 Ce qui n'est PAS une question de validation

Pour éviter de transformer ce chantier en réunion :

- **D5 n'est pas remis en cause.** L'ordre `incorrect` → `partiellement_correct` →
  `resultat_juste_consigne_non_respectee` → `a_determiner` → `correct` est
  considéré comme acquis.
- **Le nombre de signatures est un fait** : 12 (C-2). Il n'y a pas à trancher.
- **La taxonomie fermée n'est pas discutée** : `hors_perimetre` →
  `erreur_non_identifiee` est une garantie de non-invention, à préserver.

## L8.2 Le défaut relevé au passage, hors périmètre de ce chantier

**[VÉRIFIÉ]** `backend/src/contenu/aides.ts:131` contient, dans un message destiné
à l'élève, le mot anglais **« could-tu »** au lieu de « pourrais-tu » :

> « Regarde le numérateur et le dénominateur de ta fraction : par quel nombre
> **could-tu** les diviser tous les deux ? »

C'est un défaut **réel**, visible par l'élève, sur l'objectif `OO-L5-2` (hors
périmètre `OO-L1-1`). Ce chantier est documentaire et **ne le corrige pas**. Il
est signalé ici pour qu'il soit traité dans un chantier de correction.

---

## CONCLUSION DU DOCUMENT

Ce qui est établi : la compétence est définie (L1), sa taxonomie est celle du
code et elle est vérifiée (L2), la règle de correction D5 est reprise intacte et
ses limites propres à OO-L1-1 sont établies (L3), la règle de tutorat et la
question de diagnostic sont spécifiées (L4), et les exigences de réussite et de
maîtrise sont définies avec leurs 27 cas de test (L5, L7).

Ce qui reste ouvert : les 9 questions du § L8, dont 4 (Q3, Q4, Q6, Q8) conditionnent
directement la mise en œuvre du suivi.

**Statut : en attente de validation pédagogique.** Aucune des propositions
[PROPOSÉ] ne doit être implémentée avant arbitrage des questions du § L8.