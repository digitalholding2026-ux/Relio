# SPÉCIFICATION PÉDAGOGIQUE — « DÉVELOPPER ET RÉDUIRE » (OO-L1-1)

**Version :** 1.1 — **Q1 à Q4 validées** (chantier 8.1) · **Q5 à Q9 ouvertes**
**Compétence :** `OO-L1-1`
**Chantiers :** 8 (conception) → 8.1 (intégration des décisions validées)
**Date :** 2026-10-11

---

> ## ⚠️ Statut de ce document
>
> **Ce document n'a PAS été validé par un enseignant.** Aucune validation
> enseignante n'est revendiquée ici.
>
> En revanche, quatre décisions de contrat pédagogique ont été **arbitrées par le
> responsable produit** au chantier 8.1 (§ L0.5) : **Q1, Q2, Q3, Q4**. Elles sont
> reprises telles quelles, marquées **[VALIDÉ]**, et ne sont plus des propositions.
>
> **Q5 à Q9 restent ouvertes** et sont toujours listées au § L8.
>
> Chaque énoncé indique s'il décrit le code existant (**[VÉRIFIÉ]**), une décision
> approuvée (**[VALIDÉ]**), une proposition non arbitrée (**[PROPOSÉ]**) ou un
> arbitrage encore dû (**[À VALIDER]**).

---

## 0. CONVENTIONS, ET CE QUE CE DOCUMENT EST

### 0.1 Quatre marqueurs

Chaque énoncé de ce document porte l'un de ces quatre marqueurs :

| Marqueur | Signification |
|---|---|
| **[VÉRIFIÉ]** | Le comportement existe aujourd'hui dans le code. La référence `fichier:ligne` est donnée et rejouable. |
| **[VALIDÉ]** | Décision approuvée par le responsable produit au chantier 8.1. Ce n'est plus une proposition. |
| **[PROPOSÉ]** | Le comportement n'existe pas et n'a pas été arbitré. Proposition à valider avant toute implémentation. |
| **[À VALIDER]** | Une décision est nécessaire. La question est reportée au § L8 avec ses options. |

## 0.5 Décisions validées au chantier 8.1 (Q1 à Q4)

> Les quatre énoncés ci-dessous sont **repris mot pour mot** de l'arbitrage du
> responsable produit. Ils constituent le contrat pédagogique. Toute évolution
> ultérieure suppose un nouvel arbitrage explicite.

**Q1 — Prérequis.** « Vérifier les prérequis selon les besoins de l'élève et
proposer une remédiation ciblée. Ne pas imposer de blocage systématique ou
permanent du parcours. »

**Q2 — Diagnostic des erreurs.** « Lorsque la cause de l'erreur est suffisamment
étayée, proposer une aide ciblée. Lorsque plusieurs causes sont possibles, poser
une question de diagnostic. Lorsque la cause reste inconnue, ne pas inventer de
diagnostic et rester neutre. »

**Q3 — Critères de maîtrise.** « Exiger trois réussites probantes, dont au moins
une lors d'une vérification ultérieure. Une réponse obtenue après une aide
constitue un progrès, mais ne compte pas comme une réussite autonome. Ne pas
compter plusieurs tentatives identiques sur le même exercice comme des preuves
independantes. »

**Q4 — Diversité des tâches.** « Exiger au minimum deux tâches distinctes. La
vérification ultérieure doit utiliser une expression différente de celle ayant
servi à la première réussite. Les tâches doivent rester dans le périmètre réellement
enseigné et ne pas introduire de difficulté excessive uniquement pour satisfaire
le critère de diversité. »

**Portée de cet arbitrage :** ces quatre décisions portent sur le **contrat
pédagogique**, c'est-à-dire sur ce que le produit doit garantir. Elles ne
sont **pas** implémentées dans le moteur — ce chantier reste documentaire. Elles
portent aussi **pas** validation de la pédagogie des exercices existants.

**Ce que cet arbitrage ne décide pas :** ni le délai de la vérification
ultérieure (**Q6**, ouverte), ni l'enrichissement des pièges (**Q5**, ouverte),
ni la conservation des données (**Q7**), ni le libellé de la compétence
(**Q9**). Voir § L8.

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

## L1.2 Connaissances préalables et remédiation

**[VALIDÉ — Q1]** « Vérifier les prérequis selon les besoins de l'élève et proposer
une remédiation ciblée. Ne pas imposer de blocage systématique ou permanent du
parcours. »

**[VÉRIFIÉ]** Le code déclare `OO-L1-1.prerequis = []` (`blocs.ts:31`) : aucun
prérequis n'est déclaré pour l'exercice. `OO-L1-2` déclare en revanche
`prerequis: ['OO-L1-1']` (`blocs.ts:38-40`).

**[VÉRIFIÉ]** Une fonction `prerequisAtteints()` existe dans `progression.ts` et
teste si les prérequis atteignent au moins le niveau `signal`. **Elle n'est appelée
nulle part dans le code applicatif** — uniquement dans `test/progression.test.ts`.
Autrement dit : **rien ne bloque aujourd'hui**, et c'est exactement ce que Q1
demande de conserver.

**[VALIDÉ — Q1]** Les prérequis ci-dessous ne sont donc **pas des conditions
d'accès**. Ils sont un **catalogue de remédiation** : quand une difficulté
sur `OO-L1-1` s'explique par l'un d'eux, on cible cet item — et on ne bloque pas.

| Prérequis | Pourquoi il peut manquer | Remédiation ciblée |
|---|---|---|
| Calcul littéral dans une parenthèse : `a(b + c) = ab + ac` | C'est la règle de base de toute la compétence | Exercice de distribution seule, sans signe « − » |
| Sens du signe « − » devant un terme : `-3x` est l'opposé de `3x` | C'est le piège le plus fréquent du corpus | Exercice de changement de signe, sans distribution |
| Terme constant / terme en `x` : savoir nommer le contenu d'une expression | Nécessaire pour regrouper | Exercice de nommage des termes |
| Regroupement de termes semblables : `2x + x = 3x` | C'est la deuxième moitié de la compétence | Exercice de regroupement, sans distribution |

**[VALIDÉ — Q1]** Trois règles que cette décision impose :

1. **Pas de blocage systématique ni permanent.** L'élève peut toujours tenter
   l'exercice et avancer dans le parcours.
2. **Vérification *selon les besoins***, donc déclenchée par une difficulté
   observée, pas par un contrôle préalable systématique.
3. **Remédiation ciblée** : on travaille le prérequis manquant, pas la compétence
   entière, et on y revient.

**Conséquence non traitée ici :** ce document ne conçoit ni la mécanique de
remédiation, ni son déclenchement applicatif. C'est du ressort d'un chantier
d'implémentation, et cela suppose de savoir *quand* on sait qu'un prérequis
manque — ce que le code ne sait pas encore aujourd'hui. Voir **L8-Q10**.

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
| `signe_non_distribue` | `oubli_de_distribuer_un_facteur` | `2x + 11` au lieu de `2x + 1` (le − n'a agi que sur le terme constant) |
| `termes_non_collectes` | `reduction_incomplete` | `2x + 1 + x` (les `x` non regroupés) |
| `coefficient_multiplicatif_oublie` | `oubli_de_distribuer_un_facteur` | *(non atteignable sur les 3 exercices actuels)* |
| `hors_perimetre` | `erreur_non_identifiee` | toute réponse fausse hors des pièges listés |
| *(illisible)* | `reponse_illisible` | saisie non analysable |

**Point important :** `signe_non_distribue` et `erreur_de_signe` sont deux
catégories **distinctes** (`oubli_de_distribuer_un_facteur` vs `erreur_de_signe`)
mais partagent un mécanisme (le signe « − » devant une parenthèse). Le L1.3-étape-3
(piège `signe_non_distribue`) tombe donc dans `oubli_de_distribuer_un_facteur`, pas
dans `erreur_de_signe`. **La séparation existante est conservée** — Q2 (ci-dessous)
porte désormais sur le *traitement* de la cause, pas sur son *granularité*.

## L2.5 Le tri de la cause — décision validée Q2

**[VALIDÉ — Q2]** « Lorsque la cause de l'erreur est suffisamment étayée,
proposer une aide ciblée. Lorsque plusieurs causes sont possibles, poser une
question de diagnostic. Lorsque la cause reste inconnue, ne pas inventer de
diagnostic et rester neutre. »

**[VÉRIFIÉ]** Le code dispose déjà de la matière des deux premières branches :
`signatureDuPiege` reconnaît une cause exacte, et `categoriePourSignature` la
convertit en catégorie d'aide (`correction.ts`, `tutorat.ts:153-166`). Ce qui
manque est **l'arbitrage entre les trois branches** : aujourd'hui, tout ce qui
n'est pas reconnu devient `hors_perimetre` sans distinction.

### Les trois branches

| Branch | Condition | Ce que le système fait | Exemple vérifiable |
|---|---|---|---|
| **A — Cause étayée** | La réponse de l'élève **correspond exactement** à un piège listé de l'exercice | **Aide ciblée** sur la catégorie de ce piège. Le nom de la cause peut être utilisé. | E1 → `2x + 11` : le piège `signe_non_distribue` existe, donc aide ciblée sur `oubli_de_distribuer_un_facteur` |
| **B — Plusieurs causes possibles** | La réponse est fausse, mais **plusieurs lectures** en sont plausibles, ou la lecture est indéterminée | **Question de diagnostic**, avant toute aide de méthode | E2 → `2x^2 - 2x + 1` : on peut lire « seul x a été mis au carré », ou une confusion sur `(a − b)²`, ou une distributivité incomplète |
| **C — Cause inconnue** | La réponse est fausse et **aucune** lecture plausible ne peut être étayée | **Neutre.** Aucune cause affirmée, aucune aide spécifique. | E3 → `x^2 - x - 6` *(erreur réelle mais non listée)* : le moteur ne sait pas pourquoi |

### Ce qui change concrètement

- **[VÉRIFIÉ]** Aujourd'hui, les branches B et C sont **confondues** : tout ce qui
  n'est pas un piège exact tombe dans `hors_perimetre` → `erreur_non_identifiee`.
- **[VALIDÉ — Q2]** Elles doivent être **distinguées**. C'est le seul changement de
  comportement que cette décision impose sur le chemin de l'aide.
- **Ce que Q2 ne change pas** : la taxonomie fermée du § L2.2 et la garantie de
  non-invention sont **préservées**. La branche C reste la règle par défaut — on
  passe de `C` à `B` seulement quand une **indication concrète** justifie
  l'ambiguïté, pas par confort pédagogique.

### Le cas où Q2 bute sur l'état actuel du corpus

**[VÉRIFIÉ]** La branche B exige de savoir *quand* plusieurs causes sont
plausibles. Or aujourd'hui, la seule façon de le savoir est qu'un piège existe —
et le piège, par définition, désigne **une** cause. Les branches B et C sont donc
**actuellement indiscernables**.

**[À VALIDER — L8-Q5]** Rendre B réellement atteignable suppose de distinguer
« erreur reconnue » et « erreur dont on peut parler sans l'affirmer ». Les
moyens possibles sont listés en Q5 et **n'ont pas été arbitrés**. Tant que Q5
n'est pas tranchée, **Q2 est en partie inapplicable** : le contrat est validé,
la mécanique ne l'est pas. C'est le premier arbitrage à conduire.

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

## L3.3 Arbre de décision — D5 inchangé, tri de la cause selon Q2

**[VALIDÉ — Q2]** L'arbre ci-dessous applique la décision Q2. Il **respecte
strictement D5** pour le verdict : il ne le remplace pas, il l'habille. La seule
modification par rapport à la version 1.0 est le **tri explicite des trois
branches** de l'étape A (étayée / ambiguë / inconnue), conformément à
[L2.5](#l25-le-tri-de-la-cause--décision-validée-q2).

```
ENTRÉES :
  valeur          = valeur de la réponse élève (analysée)
  attendue        = valeur attendue
  formeExigee     = (exercice.regleForme != null)
  formeResp       = conforme | non_conforme | indeterminee
  achevement      = acheve | inacheve
  piegesTouches   = [signatures des pièges dont la valeur == valeur élève]
  aideDemandee    = nombre d'indices déjà consultés sur cet exercice

ÉTAPE A — Valeur juste ?
  SI NON :
    ├─ A0. SI la saisie était illisible → statut « illisible », pas de verdict math.
    │       ACTION : question de clarification (L4.3), JAMAIS un indice de méthode,
    │       car on ne sait pas encore ce que l'élève a fait.
    │       → c'est la branche « plusieurs causes possibles » : on ne peut pas
    │         savoir ce qu'il a écrit.
    │
    ├─ A1. BRANCHE « cause étayée » (Q2)
    │       SI au moins un piège touché :
    │         catégorie = CATEGORIE_PAR_SIGNATURE[piège]
    │         ACTION : aide ciblée sur cette catégorie, niveau selon L4.1.
    │
    ├─ A2. BRANCHE « plusieurs causes possibles » (Q2)
    │       SI aucune correspondance exacte MAIS plusieurs lectures plausibles :
    │         ACTION : question de diagnostic (L4.3) AVANT toute aide de méthode.
    │         ⚠ N'atteignable qu'après l'arbitrage L8-Q5 (voir L2.5).
    │
    └─ A3. BRANCHE « cause inconnue » (Q2)
            SINON → catégorie = erreur_non_identifiee (hors_perimetre)
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
        ACTION : NE PAS conclure. Question de diagnostic sur la FORME (L4.3)
        pour lever l'indétermination avant toute aide de méthode.
  SINON → verdict = correct
        ACTION : la tentative est AUTONOME si et seulement si aideDemandee === 0.
        SI aideDemandee > 0 → c'est un PROGRÈS (L5.6), pas une réussite autonome.
        Dans les deux cas, D5 reste `correct` : rien ne change au verdict.
```

**Point de cohérence :** Q2 ne modifie **aucun** verdict D5. Il ne change que le
**choix de l'aide affichée** quand la réponse est fausse. Un élève qui obtient
`correct` après une aide a bien `correct` au sens de D5 — c'est le **suivi**
qui refuse d'en faire une preuve (voir [L5.6](#l56-réussite-autonome--progrès--preuve)).

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
quand il échoue **pour une autre raison**. »*

**[PROPOSÉ — inchangé, toujours non validé]** Ce changement d'escalade **n'est pas
une décision validée** : il ne fait partie ni de Q1, ni de Q2, ni de Q3, ni de Q4.
Q2 valide le **tri de la cause** (quelle aide proposer), pas la **cadence**
d'escalade. La règle reste une proposition.

**[VALIDÉ — Q2]** Ce que Q2 impose en revanche, et qui est directement
applicable : si la cause est **étayée**, l'aide doit être **ciblée** sur cette
cause. C'est une exigence sur le **contenu** de l'aide, pas sur son niveau.

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

## L4.3 La question de diagnostic — décision validée Q2

**[VALIDÉ — Q2]** Q2 fait de la question de diagnostic la **branche centrale** du
tri de la cause : « lorsque **plusieurs causes sont possibles**, poser une question
de diagnostic ». Ce n'est plus seulement une réponse à une saisie illisible.

### Les trois déclencheurs

| # | Déclencheur | Ce que le système ne sait pas | Ce qu'il fait |
|---|---|---|---|
| 1 | **Plusieurs causes possibles** (Q2) | quelle cause est la bonne | **question de diagnostic**, avant toute aide de méthode |
| 2 | **Réponse illisible** (`reponse_illisible`) | ce que l'élève a écrit | question de clarification, **sans** indice de méthode |
| 3 | **Forme indéterminée** (`a_determiner`) | si la forme est respectée | question de diagnostic sur la **forme**. *Inatteignable sur `OO-L1-1` actuel* (aucune forme exigée) |

### Règle de non-diagnostic

**[VALIDÉ — Q2]** « Lorsque la cause reste inconnue, ne pas inventer de diagnostic
et rester neutre. »

Concrètement, on **ne pose pas** de question de diagnostic pour « deviner » la cause
d'une erreur dont on ignore tout. Poser une question de diagnostic quand
l'information manque est légitime ; poser une question **pour faire semblant
d'avoir une hypothèse** ne l'est pas. La v1.0 énonçait cette règle ; Q2 la confirme
et l'élève au rang de contrat.

**[VALIDÉ — Q2]** Corollaire : une question de diagnostic **précède** l'aide de
méthode. On ne montre jamais la règle avant d'avoir lever l'ambiguïté — sinon la
question de diagnostic devient décorative.

**[PROPOSÉ — non validé]** Format d'une question de diagnostic :
- **une** question fermée, courte ;
- **deux ou trois choix** (pas de saisie libre) ;
- **une** conséquence par réponse.

Exemple (réponse illisible) :
> « Ton expression n'a pas pu être lue. Réessaie en écrivant le résultat, par exemple : 2x + 1 »
> → si l'élève réessaie et réussit : on compte un échec « saisie », pas une
> erreur de concept → catégorie `reponse_illisible`, aide = « réécris plus lisiblement ».

**[À VALIDER — L8-Q5]** Les déclencheurs 1 et 2 sont atteignables. Le
déclencheur 1 (« plusieurs causes possibles ») suppose de savoir qu'une réponse
admet plusieurs lectures : aujourd'hui, cette information **n'existe pas** dans le
modèle. Voir [L2.5](#l25-le-tri-de-la-cause--décision-validée-q2).

---

# LIVRABLE 5 — EXIGENCES DE RÉUSSITE ET DE MAÎTRISE

## L5.1 Le problème à résoudre, énoncé franchement

**[VÉRIFIÉ]** Aujourd'hui, une seule réponse juste fait monter le compteur
(`progression.ts:74-88`). Mais `progression.ts:8-25` dit noir sur blanc que
« `correcte` seul ne prouve rien » et que **`acquis_confirme` est hors périmètre,
le moteur ne l'atteint pas**. Le code est donc honnête sur sa limite — c'est la
spécification qui doit décider ce qu'on fait de cette limite.

## L5.2 Trois niveaux de réussite, du plus faible au plus fort

**[VALIDÉ — Q3 et Q4]** Les définitions ci-dessous appliquent les décisions Q3
(« trois réussites probantes, dont au moins une lors d'une vérification
ultérieure ») et Q4 (« au minimum deux tâches distinctes »).

| Niveau | Définition | Ce qui le fonde | Confiance |
|---|---|---|---|
| **Réussite isolée** | 1 réponse juste | 1 item | très faible — peut être du hasard |
| **Acquis fragile** | 2 réussites **autonomes** sur **2 tâches distinctes** | 2 items indépendants | moyenne — début réel, mais court |
| **Maîtrise** | **3 réussites autonomes**, sur **≥2 tâches distinctes**, dont **au moins 1 pendant une vérification ultérieure** (L5.4) | 3 items, dont 1 différé | élevée |

**Deux précisions imposées par Q3 et Q4, qui changent la v1.0 :**

1. **[VALIDÉ — Q3]** Le seuil de maîtrise est **3**, pas « 2 puis 3 ». La v1.0
   disait « acquis fragile » dès 2 réussites : c'est **conservé**, mais 2
   réussites ne sont **jamais** la maîtrise.
2. **[VALIDÉ — Q3]** Une réponse juste **obtenue après une aide** est un **progrès**,
   et **compte pour zéro réussite autonome** (voir [L5.6](#l56-réussite-autonome--progrès--preuve)).
   Un élève qui réussit du premier coup 2 fois, puis réussit avec de l'aide une
   3ᵉ fois, n'a **pas** la maîtrise.
3. **[VALIDÉ — Q3]** Plusieurs tentatives **identiques sur le même exercice** ne
   comptent **qu'une seule fois** comme preuve. Réussir E1 trois fois d'affilée
   vaut **une** preuve, pas trois.

## L5.3 La règle des trois, réconciliée avec le moteur

**[VÉRIFIÉ]** `progression.ts` applique une règle des trois (« 3 réussites sans
erreur → borne d'erreur ~ 3/n ≤ 100 % ») et exige **4 items** pour conclure
(`progression.ts:94`, `:101`). Le moteur **ne conclut jamais** à `acquis_confirme`.

**[VALIDÉ — Q3]** Le seuil des **3 réussites probantes** est donc cohérent avec la
règle des trois déjà codée — cette décision **confirme** le seuil que la v1.0
proposait, au lieu de le changer.

**[VALIDÉ — Q3 + Q4]** Statuts d'affichage, en tenant compte de la déduplication
par tâche et de l'exclusion des réponses obtenues avec aide :

| Situation | Statut affiché |
|---|---|
| 0 donnée | `non_evalue` |
| 1 erreur isolée | `signal` |
| ≥2 erreurs cohérentes | `hypothese` (à confirmer par l'enseignant) |
| 2 réussites autonomes sur 2 tâches distinctes | **acquis fragile** |
| 3 réussites autonomes sur ≥2 tâches distinctes, **sans** vérification ultérieure réussie | **acquis fragile** — les 3 preuves sont là, il manque le différé |
| idem **+** 1 réussite pendant une vérification ultérieure | **maîtrisé** |

**Le mot « maîtrisé » n'est employé qu'après vérification ultérieure réussie.**
C'est ce qui répond à l'interdiction de `regles-recommandation-pedagogique.md:134`.

## L5.4 La vérification ultérieure — le « peut-être qu'il avait deviné »

**[VALIDÉ — Q4]** « La vérification ultérieure doit utiliser une expression
différente de celle ayant servi à la première réussite. Les tâches doivent rester
dans le périmètre réellement enseigné et ne pas introduire de difficulté excessive
uniquement pour satisfaire le critère de diversité. »

**[PROPOSÉ — non validé]** Le déclencheur (*« après combien de réussites ? »*,
*« après combien de temps ? »*) reste **ouvert** : c'est l'objet de **Q6** et de
**L8-Q11**.

### Ce que Q4 fixe

| Règle | Contenu |
|---|---|
| **Expression différente** | La vérification ne peut pas réutiliser l'expression de la première réussite. « Different » porte sur **l'expression**, pas seulement sur l'identifiant de l'exercice. |
| **Périmètre enseigné** | Même vocabulaire que les exercices déjà rencontrés — pas d'identité remarquable nouvelle, pas de lettre autre que `x`. |
| **Pas de difficulté excessive** | La difficulté ne doit pas être augmentée **pour satisfaire le critère de diversité**. Un critère de comptage ne justifie pas un saut de niveau. |

**[VÉRIFIÉ]** Cette contrainte est cohérente avec le périmètre réel du moteur :
l'analyseur ne connaît que `x` et les puissances entières 0-16
(`analyseur-expression.ts:152`, `:252-254`). Une vérification qui sortait de ce
périmètre serait à la fois hors programme et non analysable.

### Exemple conforme à Q4

Pour `MVP-B1-E1` (`3(x + 2) − (x + 5)`, réponse `2x + 1`) :
> « Développe et réduis C = 2(x − 3) + (x + 1). »
> réponse : `2x - 6 + x + 1` → `3x - 5`
>
> **Pourquoi c'est conforme :** expression **différente** de `3(x + 2) − (x + 5)` ;
> mêmes compétences (distributivité + signe + regroupement) ; **pas plus difficile**
> (un facteur au lieu de deux) ; dans le périmètre exact du moteur.

### Règles de fonctionnement

- **[PROPOSÉ — non validé]** La vérification **compte comme l'une des 3 réussites
  autonomes** si elle est réussie sans aide (c'est la lecture de Q3 : « dont au
  moins une lors d'une vérification ultérieure »). Elle n'est donc **pas** un
  item « gratuit » en plus — c'est l'une des trois.
- **[PROPOSÉ — non validé]** Si la vérification est ratée → retour à « acquis
  fragile », **sans effacer** les réussites antérieures.
- **[PROPOSÉ — non validé]** Elle n'est **pas** affichée comme un contrôle punitif
  (« retiens-tu ? ») mais comme une « nouvelle façon de le faire ».

**[VÉRIFIÉ]** Deux limites réelles, à connaître avant tout chantier d'implémentation :
- il n'existe **aucun** exercice de vérification dans le corpus : les 3 exercices
  `OO-L1-1` servent tous à l'apprentissage initial ;
- les expressions de vérification de ce type sont **analysables** par le moteur
  actuel, mais **aucun exercice** ne les porte. Les créer est hors de ce chantier
  documentaire (contrainte : ne modifier aucun exercice existant).

## L5.5 Ce que le système ne prétendra pas détecter

**[VALIDÉ — Q3]** Trois affirmations que ce document refuse de faire :

1. **Le système ne dira pas « tu sais la règle »** — il constatera « tu as réussi
   **autonome** sur **N tâches distinctes**, dont une en vérification ultérieure ».
2. **Le système ne dira pas « tu as compris »** — la compréhension est un
   processus mental non observable depuis une réponse.
3. **Une réussite unique ne conclura rien** — elle incrémente un compteur, rien de
   plus. Et **une réussite avec aide n'est pas une réussite** (§ L5.6).

## L5.6 Réussite autonome / progrès / preuve

**[VALIDÉ — Q3]** « Une réponse obtenue après une aide constitue un progrès, mais
ne compte pas comme une réussite autonome. Ne pas compter plusieurs tentatives
identiques sur le même exercice comme des preuves indépendantes. »

Cette section **précise** la décision : elle en donne la définition opérationnelle.
C'est le seul endroit du document où une décision validée est complétée, et le
complément est signalé comme tel.

### Les trois notions

| Notion | Définition opérationnelle | Compte pour la maîtrise ? |
|---|---|---|
| **Réussite autonome** | réponse juste sur une tâche donnée, **sans qu'aucune aide ait été demandée ni affichée pendant cette tentative** | ✅ oui |
| **Progrès** | réponse juste, mais obtenue **après au moins une aide** | ❌ non — mais c'est un progrès réel, à afficher |
| **Preuve** | une **tâche distincte** ayant donné une réussite autonome | c'est l'unité de compte de la maîtrise |

**[VALIDÉ — Q3]** « Sans aide » = **aucun indice consulté**. Un élève qui
n'ayant jamais demandé d'indice mais qui en a vu un passivement affiché n'est
pas dans ce cas — c'est une ambiguïté, voir **L8-Q11**.

### Pourquoi dédupliquer par tâche

**[VALIDÉ — Q3]** « Ne pas compter plusieurs tentatives identiques sur le même
exercice comme des preuves indépendantes. » Concrètement :

- réussir E1 une fois → **1 preuve** ;
- réussir E1 trois fois → **toujours 1 preuve** (la deuxième et la troisième
  répétitions ne sont pas des preuves) ;
- réussir E1 puis E3 → **2 preuves** (tâches distinctes).

**[VALIDÉ — Q4]** C'est pourquoi Q4 exige **au minimum deux tâches distinctes** :
sans cette exigence, la règle Q3 réduirait mécaniquement le décompte à 1 seule
preuve possible, et la maîtrise serait inatteignable.

### Cohérence des trois notions

| Règle | Effet |
|---|---|
| Réussite autonome | un élève qui réussit systématiquement **avec** aide ne progresse vers la maîtrise que s'il réussit **ensuite sans** aide |
| Progrès | ne fait jamais régresser l'élève, et ne bloque rien (cohérent avec Q1) |
| Preuve dédupliquée | cohérent avec Q4 : au moins 2 tâches, donc au moins 2 preuves |

**Point de vigilance pour l'implémentation :** le journal actuel ne distingue pas
une réussite autonome d'une réussite avec aide. Le champ `nbEchecsAuPrecedent`
existe, mais il compte les **échecs**, pas les **indices consultés**. → voir
[L6.2](#l62-les-données-minimales-pour-la-règle-du--l5).

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

**[VALIDÉ — Q3, Q4]** Pour appliquer « 3 réussites autonomes sur ≥2 tâches
distinctes, dont 1 en vérification ultérieure », le journal local doit porter,
par réponse :

| Champ | Pourquoi | Existe ? |
|---|---|---|
| `exerciceId` | identifier la **tâche**, pour dédupliquer (Q3) et exiger 2 tâches distinctes (Q4) | ✅ oui |
| `objectifId` | rattacher à `OO-L1-1` | ✅ oui |
| `statut` (`correcte`/`fausse`/…) | compter réussites / erreurs | ✅ oui |
| `signatureErreur` / `categorie` | ne recompter que des erreurs **de même catégorie** (L4.1) | ✅ oui |
| `nbEchecsAuPrecedent` | distinguer une réussite « fragile » d'une première réussite | ✅ oui (le client connaît l'historique de l'exercice) |
| `nbIndicesConsultes` | **Q3** — distinguer une réussite autonome d'un progrès | ❌ **à ajouter** |
| `estVerificationUlterieure` | **Q3** : compter celle des 3 réussites qui est différée | ❌ **à ajouter** |
| `expressionTache` | **Q4** : vérifier que la vérification utilise une **expression différente** de la première réussite | ❌ **à ajouter** |
| `horodatage` | **Q6 (ouverte)** : intervalle entre succès et vérification | ✅ oui (observations horodatées) |

### Les trois champs manquants, et ce qu'ils rendent chacun impossible

| Champ manquant | Règle qu'il rend calculable | Sans lui |
|---|---|---|
| `nbIndicesConsultes` | **Q3** — le progrès vs la réussite autonome | impossible de distinguer une réussite autonome d'un progrès |
| `estVerificationUlterieure` | **Q3** — « dont au moins une en vérification » | impossible de savoir si la condition est remplie |
| `expressionTache` | **Q4** — expression différente de la première réussite | impossible de vérifier la contrainte de diversité |

**[VÉRIFIÉ]** Ces trois champs sont **absents** du journal actuel. Le champ
`nbEchecsAuPrecedent` existe mais compte les **échecs**, pas les **indices
consultés** : la v1.0 le prenait pour un équivalent, ce qui était une erreur.

**[PROPOSÉ]** Aucun de ces trois champs n'est ajouté par ce chantier — la
modification du journal est hors périmètre documentaire. Ils sont décrits ici
comme **prérequis d'implémentation** de Q3 et Q4.

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

## L7.4 Cas de progression — deux colonnes : aujourd'hui / cible validée

**Lecture :** la colonne « aujourd'hui » est le comportement **vérifié** du moteur.
La colonne « cible Q3/Q4 » est le comportement **validé par le responsable
produit** mais **pas encore implémenté**. L'écart entre les deux est le travail
d'un futur chantier d'implémentation, pas de ce chantier documentaire.

| # | Situation | Aujourd'hui [VÉRIFIÉ] | Cible Q3+Q4 [VALIDÉ] |
|---|---|---|---|
| T-21 | 0 réponse sur `OO-L1-1` | `non_evalue` | `non_evalue` — inchangé |
| T-22 | 1 réponse fausse | `signal` | `signal` — inchangé |
| T-23 | 2 réponses fausses | `hypothese` | `hypothese` — inchangé |
| T-24 | 3 réussites **avec aide**, 3 tâches distinctes | compte **3** `correcte` | **0 réussite autonome** — 3 progrès, pas de maîtrise |
| T-25 | 3 réussites **autonomes**, **1 seule** tâche (E1 ratée 3 fois) | compte **3** | **1 preuve** — dédupliqué, pas de maîtrise |
| T-26 | 2 réussites autonomes, 2 tâches distinctes | rien de concluant | **acquis fragile** |
| T-27 | 3 réussites autonomes, 2 tâches distinctes, **sans** vérification | rien de concluant | **acquis fragile** — il manque la condition différée |
| T-28 | 3 réussites autonomes, ≥2 tâches, **1** pendant une vérification ultérieure, **expression différente** | rien de concluant | **maîtrisé** — premier cas où le mot est permis |
| T-29 | idem T-28 mais la vérification réutilise **la même expression** | rien de concluant | **maîtrisé refusé** — Q4 violée, à traiter en échec de la vérification |

### Points de lecture

- **T-24 et T-25 sont les deux écarts les plus dangereux** : ce sont des cas où le
  moteur actuel **conclurait trop vite**, parce qu'il ne connaît ni l'aide ni la
  déduplication par tâche. Les deux sont des cas où la maîtrise doit être
  **refusée**, et où le moteur actuel risquerait de l'accorder.
- **T-27** rappelle que Q3 a deux conditions : le **nombre** (3) et le **caractère**
  de l'une d'elles (vérification ultérieure). Satisfaire la première ne suffit pas.
- **T-29** est la traduction testable de Q4 : la contrainte porte sur
  **l'expression**, pas sur l'identifiant de l'exercice. Sans le champ
  `expressionTache` ([L6.2](#l62-les-données-minimales-pour-la-règle-du--l5)), cette
  contrainte **n'est pas vérifiable**.
- **Le déclencheur temporel reste ouvert (Q6)** : aucun de ces cas ne suppose de
  délai. Si Q6 fixe un délai, T-28 devient conditionné au franchissement de ce délai.

## L7.5 Cas où le système doit **refuser** de conclure

| # | Situation | Comportement exigé | Origine |
|---|---|---|---|
| T-30 | Cause inconnue (`erreur_non_identifiee`) | Aucune catégorie de difficulté plausible n'est enregistrée | [VÉRIFIÉ] |
| T-31 | Une seule réussite | Aucun statut de maîtrise n'est affiché | [VÉRIFIÉ] |
| T-32 | Réussite obtenue après une aide | Afficher un **progrès**, ne jamais compter comme réussite autonome | **Q3** |
| T-33 | Élève qui réussit en recopiant la réponse d'un indice | Le système ne peut pas le détecter → **ne pas prétendre l'avoir détecté** | [VÉRIFIÉ] (§ L5.5) |
| T-34 | Prérequis manquant (au sens Q1) | Proposer une remédiation ciblée, **sans bloquer** le parcours | **Q1** |
| T-35 | Cause étayée sur E1 (`2x + 11` → `signe_non_distribue`) | Aide ciblée sur `oubli_de_distribuer_un_facteur`, nom de la cause utilisable | **Q2**, branche A |
| T-36 | Cause non étayée sur E3 (`x^2 - x - 6`, hors pièges) | Reste **neutre**, aucune cause affirmée | **Q2**, branche C |
| T-37 | Réponse illisible (`2x + 1 zzz`) | Question de clarification, **jamais** un indice de méthode | [VÉRIFIÉ] + **Q2** |

---

# LIVRABLE 8 — QUESTIONS DE VALIDATION

## L8.0 Comment lire cette section

**Q1 à Q4 sont arbitrées** par le responsable produit (chantier 8.1) et sont
reprises mot pour mot au [§ L0.5](#l05-décisions-validées-au-chantier-81-q1-à-q4).
Elles ne figurent plus dans la liste des questions ouvertes.

**Q5 à Q9 restent ouvertes.** Rien n'a été décidé à leur sujet, et ce document
ne les arbitre pas.

### Questions arbitrées (rappel)

| # | Question | Décision retenue |
|---|---|---|
| **Q1** | Prérequis | Vérification selon les besoins + remédiation ciblée, **sans blocage** ([L1.2](#l12-connaissances-préalables-et-remédiation)) |
| **Q2** | Diagnostic des erreurs | 3 branches : étayée → aide ciblée ; ambiguë → question ; inconnue → neutre ([L2.5](#l25-le-tri-de-la-cause--décision-validée-q2)) |
| **Q3** | Critères de maîtrise | 3 réussites probantes, ≥1 en vérification ultérieure ; aide = progrès ; déduplication par tâche ([L5.2](#l52-trois-niveaux-de-réussite-du-plus-faible-au-plus-fort)) |
| **Q4** | Diversité des tâches | ≥2 tâches distinctes ; expression différente en vérification ; pas de difficulté excessive ([L5.4](#l54-la-vérification-ultérieure--le--peut-être-quil-avait-deviné)) |

### Questions encore ouvertes

| # | Question | Option par défaut (non arbitrée) | Risque si non tranchée |
|---|---|---|---|
| **Q5** | Faut-il **enrichir** les pièges pour couvrir les erreurs hors périmètre ? (L7.2, T-09, T-13) | **Non pour ce chantier** — on ne touche pas aux exercices | L'élève « a oublié le 3x » reçoit une aide neutre. **Bloque la branche « plusieurs causes » de Q2** ([L2.5](#l25-le-tri-de-la-cause--décision-validée-q2)) |
| **Q6** | Faut-il un **délai** entre succès et vérification ultérieure ? (L5.4) | « quelques jours », non chiffré | Sans délai, la vérification prouve peu de plus que l'exercice |
| **Q7** | Quelle **conservation des données locales** ? (L6.3) | Rien de décidé — hors périmètre | Perte du journal au vidage du navigateur, sans que personne ne l'ait choisi |
| **Q8** | Faut-il ajouter `estVerificationUlterieure` au journal local ? (L6.2) | Oui | La règle de maîtrise n'est pas calculable. **Rendue nécessaire par Q3**, mais le champ lui-même reste à valider |
| **Q9** | Le libellé de la compétence est-il « développer **et réduire** » ? (C-1) | Oui | Le backend et la matrice affichent deux libellés différents |

### Ambiguïtés à arbitrer avant toute implémentation

Ces deux points ne figuraient **pas** dans la v1.0. Ils sont apparus en
intégrant Q3 et Q4, parce que les deux décisions nomment des notions que le
produit n'a pas définies opératoirement.

| # | Ambiguïté | Origine | Options |
|---|---|---|---|
| **Q10** | **Comment savoir qu'un prérequis manque ?** Q1 impose de « vérifier les prérequis selon les besoins de l'élève », mais aucun signal du moteur ne distingue « prérequis manquant » d« erreur occasionnelle ». Le code déclare `prerequis: []` et n'a aucun mécanisme de remédiation. | **Q1** | (a) se fonder sur la répétition d'une même catégorie d'erreur ; (b) sur une erreur isolée ; (c) mécanisme dédié, hors périmètre. Sans cet arbitrage, Q1 n'est pas applicable |
| **Q11** | **Définition opérationnelle de la tentative autonome.** Q3 exclut les réponses « obtenues après une aide ». Or le journal ne compte que les **échecs** (`nbEchecsAuPrecedent`), pas les **indices consultés**. Deux points restent flous : (a) un indice **affiché mais non ouvert** disqualifie-t-il la réussite ? (b) une aide reçue **sur une tentative antérieure du même exercice** disqualifie-t-elle la tentative suivante ? | **Q3** | (a) seul l'indice **demandé** disqualifie ; (b) tout indice affiché disqualifie ; (c) l'aide antérieure est purgée après un certain délai. **Aucune option n'est retenue par ce document** |

**Les deux ambiguïtés sont signalées, pas tranchées.** Le § L5.6 donne une
définition de travail explicite (« aucun indice consulté pendant la tentative »)
qui a servi à écrire les cas de test T-24 à T-29 ; cette définition est
**provisoire** et disparaîtra si Q11 est arbitrée autrement.

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
ses limites propres à OO-L1-1 sont établies (L3), la règle de tutorat et le tri
de la cause sont spécifiés (L4), et les exigences de réussite et de maîtrise sont
définies avec leurs cas de test (L5, L7).

**Ce qui est validé** : quatre décisions de contrat pédagogique (Q1 à Q4,
[L0.5](#l05-décisions-validées-au-chantier-81-q1-à-q4)) — prérequis sans blocage,
tri de la cause en trois branches, 3 réussites probantes dont une en vérification
ultérieure, et diversité des tâches. Elles sont intégrées aux sections L1.2, L2.5,
L3.3, L4.1, L4.3, L5.2 à L5.6, L6.2 et L7.4/L7.5.

**Ce qui reste ouvert** : les questions **Q5 à Q9** et deux ambiguïtés
**Q10 et Q11**, listées au [§ L8](#l80-comment-lire-cette-section).

**Statut :** Q1 à Q4 **validées** par le responsable produit ; Q5 à Q9 et Q10-Q11
**ouvertes**. Le document reste sans validation enseignante. Aucune des
propositions [PROPOSÉ] ne doit être implémentée avant arbitrage.