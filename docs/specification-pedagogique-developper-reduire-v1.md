# SPÉCIFICATION PÉDAGOGIQUE — « DÉVELOPPER ET RÉDUIRE UNE EXPRESSION LITTÉRALE » (`OO-L1-1`)

**Version :** 1.2 — **Q1 à Q11 validées** (chantiers 8.1 et 8.2)
**Compétence :** `OO-L1-1` — **nom canonique : « Développer et réduire une expression littérale »** (Q9)
**Chantiers :** 8 (conception) → 8.1 (Q1–Q4) → **8.2 (Q1–Q11 consolidées)**
**Date :** 2026-10-11

---

> ## ⚠️ Statut de ce document
>
> **Ce document n'a PAS été validé par un enseignant.** Aucune validation
> enseignante n'est revendiquée ici.
>
> Les onze décisions de contrat pédagogique ont été **arbitrées par le
> responsable produit** — Q1 à Q4 au chantier 8.1, Q5 à Q11 au chantier 8.2
> (§ L0.5). Elles sont reprises mot pour mot, marquées **[VALIDÉ]**.
>
> **Le mot « maîtrise » désigne ici un seuil contractuel atteignable, jamais une
> validation pédagogique** (voir § L5.7). Un validateur documentaire qui passe ne
> signifie **pas** que la pédagogie est validée.
>
> Chaque énoncé indique s'il décrit le code existant (**[VÉRIFIÉ]**), une décision
> approuvée (**[VALIDÉ]**), une proposition non arbitrée (**[PROPOSÉ]**) ou un
> point non applicable ici (**[HORS-PÉRIMÈTRE]**).

---

## 0. CONVENTIONS, ET CE QUE CE DOCUMENT EST

### 0.1 Marqueurs

| Marqueur | Signification |
|---|---|
| **[VÉRIFIÉ]** | Le comportement existe aujourd'hui dans le code. La référence `fichier:ligne` est donnée et rejouable. |
| **[VALIDÉ]** | Décision approuvée par le responsable produit (chantiers 8.1 / 8.2). Ce n'est plus une proposition. |
| **[PROPOSÉ]** | Le comportement n'existe pas et n'a pas été arbitré. |
| **[À VALIDER]** | Une décision est nécessaire. La question est reportée au § L8 avec ses options. |
| **[HORS-PÉRIMÈTRE]** | Point identifié mais volontairement non traité dans ce chantier. |

## 0.5 Décisions validées (Q1 à Q11)

> Les onze énoncés ci-dessous sont **repris mot pour mot** de l'arbitrage du
> responsable produit. Ils constituent le contrat pédagogique. Toute évolution
> ultérieure suppose un nouvel arbitrage explicite.

### Décisions validées au chantier 8.1 (Q1 à Q4)

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

### Décisions validées au chantier 8.2 (Q5 à Q11)

**Q5 — Enrichissement des pièges.** « Enrichir progressivement le catalogue des
pièges après analyse et validation. Ne pas chercher à prévoir toutes les erreurs
possibles et ne pas forcer un diagnostic si les éléments sont insuffisants. »

**Q6 — Délai de vérification ultérieure.** « La vérification a lieu lors d'une
séance distincte, au moins 24 heures après la dernière réussite autonome
comptabilisée pour la compétence. Elle porte sur une expression différente et
s'effectue sans indice consulté pendant cette tentative. »

**Q7 — Conservation locale.** « Conserver localement le journal tant qu'il reste
utile à l'apprentissage, sans suppression automatique arbitraire. Prévoir la
possibilité pour l'élève d'effacer son historique. Expliquer que les données
peuvent être perdues si les données du navigateur sont supprimées ou si l'élève
change d'appareil. À ce stade, ne pas envoyer le journal au serveur. »

**Q8 — Champ `estVerificationUlterieure`.** « Prévoir ce champ, renseigné par la
logique de Relio et non choisi par l'élève. Il indique si une tentative satisfait
les critères de vérification ultérieure. Ce champ ne suffit pas, à lui seul, à
établir la maîtrise. »

**Q9 — Nom canonique de la compétence.** « Retenir exactement :
« Développer et réduire une expression littérale ».
Une forme courte peut être employée dans l'interface, mais le nom canonique
doit rester cohérent dans les données et la documentation. »

**Q10 — Détection d'un prérequis manquant.** « Une erreur peut déclencher une
vérification ciblée, mais ne suffit pas automatiquement à conclure qu'un prérequis
manque. Selon le résultat, proposer une remédiation courte ou revenir à l'exercice
initial, sans blocage systématique. »

**Q11 — Définition d'une tentative autonome.** « Un indice est disponible mais
n'est pas consulté : la tentative peut rester autonome. Un indice est consulté
pendant la tentative : une réponse correcte compte comme progrès, pas comme
réussite autonome. Une aide consultée lors d'une tentative antérieure ne
disqualifie pas une nouvelle tentative sans aide. »

**Portée de cet arbitrage :** ces décisions portent sur le **contrat pédagogique**,
c'est-à-dire sur ce que le produit doit garantir. Elles ne sont **pas**
implémentées dans le moteur. Elles ne valent **pas** validation de la pédagogie
des exercices existants, et le passage du validateur documentaire ne vaut **pas**
validation de la maîtrise pédagogique.

### 0.2 Périmètre strict

Ce document ne décrit que la compétence **`OO-L1-1`**. Les exercices
`OO-L1-2` (factorisation), `OO-L3-1` (racines) et `OO-L5-1`/`OO-L5-2` (fractions)
ne sont mentionnés que là où ils rendent la règle OO-L1-1 explicite.

### 0.3 Ce que ce document n'est pas

- Ce n'est pas une spécification d'interface. L'ergonomie est traitée par un autre chantier ; le § L6.6 décrit seulement les **besoins** pédagogiques que l'interface devra permettre.
- Ce n'est pas une refonte du moteur de correction. La règle D5, arbitrée par l'enseignant, est reprise telle quelle et n'est jamais remise en cause ici.
- Ce n'est pas une création d'exercices. Les deux exemples cités (`2(x + 3)`, `3(x − 4)`) servent de point de départ à la définition, pas de liste d'exercices à produire.

### 0.4 Trois contradictions relevées pendant l'audit

| # | Contradiction | Version A | Version B | Position retenue |
|---|---|---|---|---|
| **C-1** | Nom de la compétence `OO-L1-1` | « Développer une expression algébrique (distributivité, identités remarquables) » — `docs/matrice-couverture-competences.md:128` | « Développer et réduire une expression algébrique » — `backend/src/contenu/blocs.ts:29` | **[VALIDÉ — Q9]** Nom canonique : **« Développer et réduire une expression littérale »**. Ni A ni B : le nom retenu est un **troisième**, et les deux libellés existants sont **erronés**. Voir [L1.0](#l10-nom-canonique--q9) |
| **C-2** | Nombre de signatures d'erreur | « 11 signatures » — `regles-recommandation-pedagogique.md`, `rapport-final-chantier-7-5.md:17` | 12 — `signatures.ts:11-24` | **12**, le code tranche. Les trois comptes « 11 » sont faux |
| **C-3** | Emploi du mot « maîtrise » | Interdit explicitement — `regles-recommandation-pedagogique.md:134` | Employé trois fois — `specification-diagnostic-initial.md:152`, `:192`, `:229` | Ce document **emploie** « maîtrise » depuis Q3, mais **au sens d'un seuil contractuel** et non d'une validation pédagogique. Le glissement est explicité en [L5.7](#l57-quest-ce-que--maîtrise--ne-signifie-pas) |

## L1.0 Nom canonique — Q9

**[VALIDÉ — Q9]** « Retenir exactement : « Développer et réduire une expression
littérale ». Une forme courte peut être employée dans l'interface, mais le nom
canonique doit rester cohérent dans les données et la documentation. »

| Contexte | Valeur | Statut |
|---|---|---|
| Nom canonique (données + documentation) | `Développer et réduire une expression littérale` | **[VALIDÉ — Q9]** |
| Forme courte utilisable en interface | `Développer et réduire` | autorisé explicitement par Q9 |
| `blocs.ts:29` | `Développer et réduire une expression algébrique` | ❌ **à corriger** — hors périmètre de ce chantier |
| `matrice-couverture-competences.md:128` | `Développer une expression algébrique (distributivité, identités remarquables)` | ❌ **à corriger** — hors périmètre de ce chantier |

**[HORS-PÉRIMÈTRE]** La correction de `blocs.ts` modifierait le code applicatif,
ce que le chantier 8.2 interdit explicitement. Les deux libellés erronés sont donc
**construits et signalés, pas corrigés**. Le nom canonique s'applique dès que le
chantier d'implémentation les remplacera.

**[VÉRIFIÉ]** Q9 emploie le mot **« littérale »**, et non « algébrique ». C'est un
choix à comprendre : « algébrique » est plus familier au secondaire, mais le
moteur ne manipule que des littéraux sur `x` (`analyseur-expression.ts:152`).
« Littérale » décrit exactement le périmètre réellement implémenté.

---

# LIVRABLE 1 — DÉFINITION DE LA COMPÉTENCE

## L1.1 Ce que l'élève doit être capable de faire

**[PROPOSÉ]** L'élève atteint le seuil de **maîtrise** sur `OO-L1-1` — **« développer
et réduire une expression littérale »** (nom canonique, [Q9](#l10-nom-canonique--q9))
— lorsqu'il est capable, **sans aucune aide et sur un exercice qu'il n'a pas déjà
vu**, de :

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

**[VALIDÉ — Q10]** « Une erreur peut déclencher une vérification ciblée, mais ne
suffit pas automatiquement à conclure qu'un prérequis manque. Selon le résultat,
proposer une remédiation courte ou revenir à l'exercice initial, sans blocage
systématique. »

**Le circuit Q10 — une erreur n'est jamais un verdict sur un prérequis :**

```
UNE ERREUR OBSERVÉE
   └─ déclenche une VÉRIFICATION CIBLÉE
        (n'est pas une conclusion)
         ├─ le prérequis est confirmé manquant
         │     → REMÉDIATION COURTE, ciblée
         │     → puis retour à l'exercice initial
         ├─ le prérequis est confirmé présent
         │     → retour à l'exercice initial, sans remédiation
         │     → l'erreur relève de la compétence elle-même (Q2)
         └─ la vérification ne conclut rien
               → retour à l'exercice initial
               → AUCUNE remédiation, AUCUN blocage
               → le motif reste « non étayé » (Q2, branche C)
```

**[VALIDÉ — Q10]** Trois garde-fous que cette décision pose :

1. **Une erreur isolée ne conclut pas.** Elle ouvre une vérification, rien de plus.
2. **La remédiation est courte et ciblée**, puis on revient à l'exercice initial.
   On ne remplace pas l'exercice par un parcours de prérequis.
3. **Aucun blocage systématique**, dans tous les trois cas de sortie — y compris
   quand la vérification ne conclut rien.

**[VÉRIFIÉ]** Le moteur n'a aujourd'hui **aucun** mécanisme de vérification ni de
rémédiation : `prerequisAtteints()` existe mais n'est appelée que dans les tests
(voir ci-dessus). Q10 décrit un comportement à construire, pas à corriger.

**Conséquence non traitée ici :** ce document ne conçoit ni le contenu de la
vérification ciblée, ni son mécanisme. Voir [L8](#l80-comment-lire-cette-section).

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

### Le cas où Q2 bute sur l'état actuel du corpus — tranché par Q5

**[VALIDÉ — Q5]** « Enrichir progressivement le catalogue des pièges après analyse
et validation. Ne pas chercher à prévoir toutes les erreurs possibles et ne pas
forcer un diagnostic si les éléments sont insuffisants. »

**[VÉRIFIÉ]** La branche B exige de savoir *quand* plusieurs causes sont plausibles.
Or aujourd'hui, la seule façon de le savoir est qu'un piège existe — et le piège,
par définition, désigne **une** cause. Les branches B et C sont donc **actuellement
indiscernables**, et Q5 **confirme** cet état au lieu d'y remédier.

**Ce que Q5 tranche, précisément :**

| Point | Décision Q5 | Effet |
|---|---|---|
| Enrichissement des pièges | **progressif**, après analyse et validation | Le catalogue ne se remplit pas par anticipation |
| Recherche exhaustive | **exclue** | On ne cherche pas à couvrir toutes les erreurs possibles |
| Forçage d'un diagnostic | **exclu** si les éléments sont insuffisants | Une erreur nouvelle **reste** dans la branche C (neutre) |

**[VALIDÉ — Q5]** L'enrichissement est donc un **processus**, pas un correctif
ponctuel : on observe une erreur récurrente, on l'analyse, on la valide, puis on
la transforme en piège. **Aucune erreur n'est convertie en catégorie connue par
simple similarité de forme.**

**[VALIDÉ — Q2 + Q5]** Conséquence directe et non ambigu : tant qu'un piège
n'a pas été validé, l'erreur correspondante reste en **branche C** — neutre,
sans cause affirmée. C'est le comportement correct, pas une limite temporaire :
**Q5 refuse explicitement** de forcer le diagnostic.

**Résultat : Q2 est applicable en l'état**, parce que Q5 fournit la règle de
fun fallback qui manquait :

```
erreur fausse
  ├─ piège existant ET validé      → branche A (aide ciblée)
  ├─ plusieurs lectures plausibles ET étayées
  │                                 → branche B (question diagnostique)
  └─ sinon                          → branche C (neutre, réessai)
```

**Point d'attention assumé :** la branche B reste **difficile à atteindre** tant que
les pièges désignent une cause unique. Q5 ne demande pas de résoudre cela ; il
demande de **ne pas forcer** le diagnostic quand on ne sait pas. Le § L8 liste ce
qui reste à préciser à ce sujet.

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
| 1 | **Plusieurs causes possibles** (Q2) | quelle cause est la bonne | **question diagnostique courte**, avant de choisir l'aide |
| 2 | **Réponse illisible** (`reponse_illisible`) | ce que l'élève a écrit | **inviter à réessayer**, sans indice de méthode |
| 3 | **Forme indéterminée** (`a_determiner`) | si la forme est respectée | question de diagnostic sur la **forme**. *Inatteignable sur `OO-L1-1` actuel* (aucune forme exigée) |

### La règle de non-transformation — [VALIDÉ — Q2]

**[VALIDÉ — Q2]** « Cause inconnue ou réponse ambiguë : rester neutre et inviter à
réessayer. **Ne pas transformer automatiquement une erreur nouvelle en catégorie
connue.** »

C'est une **interdiction explicite**, et elle est plus forte que la formulation du
chantier 8.1. Elle écarte trois raccourcis que rien n'interdisait jusqu'ici :

| Raccourci interdit | Pourquoi il est interdit |
|---|---|
| Rapprocher la réponse de la réponse d'un piège existant | une proximité de forme n'est pas une identité de cause |
| Déduire la cause de la catégorie de l'erreur **précédente** | deux erreurs successives peuvent avoir des causes sans rapport |
| Transformer une erreur récurrente en catégorie dès son deuxième occurrence | Q5 exige **analyse et validation**, pas seulement une récurrence |

**[VALIDÉ — Q2]** Ce qui reste permis : créer un **nouveau** piège, mais seulement
après analyse et validation ([Q5](#le-cas-où-q2-bute-sur-létat-actuel-du-corpus--tranché-par-q5)).

### Règle de non-diagnostic

**[VALIDÉ — Q2]** « Lorsque la cause reste inconnue, ne pas inventer de diagnostic
et rester neutre. »

Concrètement, on **ne pose pas** de question de diagnostic pour « deviner » la cause
d'une erreur dont on ignore tout. Poser une question **pour faire semblant d'avoir
une hypothèse** n'est pas permis.

**[VALIDÉ — Q2]** Corollaire, à ne pas confondre : une question diagnostique n'est
**pas** une aide de méthode déguisée. Elle sert à **choisir** l'aide, donc elle
précède l'aide. Si l'élève répond, on utilise sa réponse pour choisir entre la
branche A et la branche C — pas pour lui souffler la réponse.

**[VALIDÉ — Q2]** Format d'une question diagnostique, cohérent avec le mot
**« courte »** de la décision :
- **une** question fermée, courte ;
- **deux ou trois choix** (pas de saisie libre) ;
- **une** conséquence par réponse ;
- **jamais** de nom de cause dans les choix eux-mêmes (sinon on affine le
  diagnostic au lieu de le laisser à l'élève).

Exemple (réponse illisible) :
> « Ton expression n'a pas pu être lue. Réessaie en écrivant le résultat, par exemple : 2x + 1 »
> → si l'élève réessaie et réussit : on compte un échec « saisie », pas une
> erreur de concept → catégorie `reponse_illisible`, aide = « réécris plus lisiblement ».

**[VALIDÉ — Q5]** Si la question diagnostique ne permet toujours pas de trancher
après une réponse, on **retombe en branche C** : neutre et réessai. On ne
transforme pas l'échec de diagnostic en catégorie connue.

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

## L5.4 La vérification ultérieure — [Q4 + Q6] — le « peut-être qu'il avait deviné »

**[VALIDÉ — Q6]** « La vérification a lieu lors d'une **séance distincte, au moins
24 heures après la dernière réussite autonome comptabilisée pour la compétence**.
Elle porte sur une expression différente et s'effectue **sans indice consulté
pendant cette tentative**. »

**[VALIDÉ — Q4]** « La vérification ultérieure doit utiliser une expression
différente de celle ayant servi à la première réussite. Les tâches doivent rester
dans le périmètre réellement enseigné et ne pas introduire de difficulté excessive
uniquement pour satisfaire le critère de diversité. »

### Les quatre conditions cumulatives

| # | Condition | Origine | Ce qu'elle exclut |
|---|---|---|---|
| 1 | **Séance distincte** | Q6 | une vérification faite dans la foulée, dans la même session |
| 2 | **≥ 24 h** après la **dernière réussite autonome** comptabilisée | Q6 | une vérification le soir même |
| 3 | **Expression différente** | Q4 + Q6 | reprendre l'expression de la première réussite |
| 4 | **Aucun indice consulté** pendant cette tentative | Q6 + Q11 | vérifier en regardant l'aide |

**Les quatre sont cumulatives.** Une seule qui manque ⇒ ce n'est pas une
vérification ultérieure. Le résultat est alors une tentative ordinaire, qui peut
rester une réussite autonome (Q3) mais **ne peut pas** être la preuve différée.

### Q6 tranche une difficulté que Q3 laissait ouverte

**[PROPOSÉ] → [VALIDÉ]** La v1.0 laissait le déclencheur « après combien de
réussites / après combien de temps » entièrement ouvert. Q6 fixe maintenant le
**point de départ** du délai, et c'est un choix qui mérite d'être explicité :

> « au moins 24 heures après **la dernière réussite autonome comptabilisée pour la
> compétence** »

**[VALIDÉ — Q6]** Deux conséquences directes, à ne pas rater :

1. **Le délai se recalcule à chaque réussite autonome.** Il ne se mesure pas
   depuis la première réussite de la série : c'est la **dernière** qui fait
   reference. Un élève qui réussit E1 lundi, E2 mardi et E3 mercredi ne pourra
   vérifier que **jeudi au plus tôt** — même s'il a déjà « ses » 3 preuves.
2. **C'est la compétence, pas l'exercice, qui est l'unité.** Le délai se mesure
   au niveau de `OO-L1-1`, pas exercice par exercice.

**[VALIDÉ — Q6 + Q3]** « sans indice consulté pendant cette tentative » : la
vérification est donc **toujours** une tentative autonome potentielle. Un élève qui
ouvre un indice pendant la vérification ne la **dégrade pas** en simple progrès —
il **la disqualifie** comme preuve différée.

**[VÉRIFIÉ] Le déclencheur temporel n'existe pas dans le code.** Le journal local
n'horodate pas ses observations (`Observation` ne contient aucun champ de date,
`frontend/src/lib/observations.ts:41-51`), et rien dans `progression.ts` ne
manipule de durée. La règle des 24 h est donc **entièrement à construire**.

### Ce que Q4 fixe sur le contenu

| Règle | Contenu |
|---|---|
| **Expression différente** | La vérification ne peut pas réutiliser l'expression de la première réussite. « Différent » porte sur **l'expression**, pas seulement sur l'identifiant de l'exercice. |
| **Périmètre enseigné** | Même vocabulaire que les exercices déjà rencontrés — pas d'identité remarquable nouvelle, pas de lettre autre que `x`. |
| **Pas de difficulté excessive** | La difficulté ne doit pas être augmentée **pour satisfaire le critère de diversité**. Un critère de comptage ne justifie pas un saut de niveau. |

**[VÉRIFIÉ]** Cette contrainte est cohérente avec le périmètre réel du moteur :
l'analyseur ne connaît que `x` et les puissances entières 0-16
(`analyseur-expression.ts:152`, `:252-254`). Une vérification qui sortait de ce
périmètre serait à la fois hors programme et non analysable.

### Exemple conforme à Q4 et Q6

Pour `MVP-B1-E1` (`3(x + 2) − (x + 5)`, réponse `2x + 1`), Plus tard dans une **séance distincte**, **plus de 24 h après** la dernière réussite autonome :
> « Développe et réduis C = 2(x − 3) + (x + 1). »
> réponse attendue : `2x - 6 + x + 1` → `3x - 5`
>
> **Pourquoi c'est conforme :** expression **différente** de `3(x + 2) − (x + 5)` ;
> mêmes compétences (distributivité + signe + regroupement) ; **pas plus difficile**
> (un facteur au lieu de deux) ; dans le périmètre exact du moteur ; séance et délai
> respectés ; aucun indice consulté.

### Règles de fonctionnement

- **[VALIDÉ — Q3]** La vérification **compte comme l'une des 3 réussites
  autonomes** si elle est réussie sans aide.
- **[PROPOSÉ — non validé]** Si la vérification est ratée → retour à « acquis
  fragile », **sans effacer** les réussites antérieures. *(Ce point précis reste
  une proposition : Q3 ne dit rien de ce qui se passe en cas d'échec, et aucune
  décision ne l'a tranché. Voir [L8](#l80-comment-lire-cette-section).)*
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

## L5.6 Réussite autonome / progrès / preuve — [VALIDÉ — Q11]

**[VALIDÉ — Q11]** « Un indice est disponible mais n'est pas consulté : la
tentative peut rester autonome. Un indice est consulté pendant la tentative : une
réponse correcte compte comme progrès, pas comme réussite autonome. Une aide
consultée lors d'une tentative antérieure ne disqualifie pas une nouvelle tentative
sans aide. »

**Cette décision lève l'ambiguïté Q11 du chantier 8.1.** Les trois cas qu'elle
distingue sont exactement les trois cas laissés ouverts.

### Les trois notions

| Notion | Définition opérationnelle | Compte pour la maîtrise ? |
|---|---|---|
| **Réussite autonome** | réponse juste sur une tâche donnée, **sans qu'aucun indice ait été consulté pendant cette tentative** | ✅ oui |
| **Progrès** | réponse juste, mais obtenue **après consultation d'au moins un indice pendant cette tentative** | ❌ non — mais c'est un progrès réel, à afficher |
| **Preuve** | une **tâche distincte** ayant donné une réussite autonome | c'est l'unité de compte de la maîtrise |

### La règle qui manquait — la disponibilité n'est pas la consultation

**[VALIDÉ — Q11]** C'est la distinction la plus importante du chantier 8.2 :

> **Un indice disponible n'est pas un indice consulté.**

L'élève qui a un indice **sous les yeux** mais ne l'ouvre pas est dans la même
situation que celui qui n'en a pas. La seule chose qui compte est **l'ouverture**.

| Situation | Réussite autonome ? | Fondement |
|---|---|---|
| Aucun indice proposé | ✅ oui | rien n'a été consulté |
| Indices **disponibles** mais **aucun ouvert** | ✅ **oui** | **Q11, premier cas** |
| Un indice **ouvert** pendant la tentative | ❌ non → **progrès** | **Q11, deuxième cas** |
| Indice ouvert lors d'une **tentative antérieure** du même exercice, tentative actuelle sans aide | ✅ **oui** | **Q11, troisième cas** |

**[VALIDÉ — Q11] Le troisième cas est une porte de sortie, pas une sanction.** Un
élève qui a consulté un indice, s'est trompé, puis recommence **sans aide** et réussit :
c'est une réussite autonome valide. Sans cette clause, un élève serait
définitivement condamné sur un exercice par une erreur qu'il a déjà corrigée.

**[VÉRIFIÉ] L'état actuel ne permet aucune de ces distinctions.** Le journal
local ne porte **aucun** compteur d'indices : il n'a qu'un booléen
`reussiteApresAides` (`frontend/src/lib/observations.ts:50`), et ce booléen est
**collant** — dès qu'une réussite est mémorisée sur un exercice, elle y reste
(`.some((o) => o.reussiteApresAides)`, `observations.ts:159`). Un tel champ ne
peut pas servir à compter les preuves : il ne distingue ni « aide de cette
tentative » de « aide d'avant », ni « indices ouverts » de « indices disponibles ».
Voir [L6.2](#l62-les-données-minimales-pour-la-règle-du--l5).

### Pourquoi dédupliquer par tâche

**[VALIDÉ — Q3]** « Ne pas compter plusieurs tentatives identiques sur le même
exercice comme des preuves indépendantes. » Concrètement :

- réussir E1 une fois → **1 preuve** ;
- réussir E1 trois fois → **toujours 1 preuve** (les deuxième et troisième
  répétitions ne sont pas des preuves) ;
- réussir E1 puis E3 → **2 preuves** (tâches distinctes).

**[VALIDÉ — Q4]** C'est pourquoi Q4 exige **au minimum deux tâches distinctes** :
sans cette exigence, la règle Q3 réduirait mécaniquement le décompte à 1 seule
preuve possible, et la maîtrise serait inatteignable.

### Cohérence des trois notions

| Règle | Effet |
|---|---|
| Réussite autonome (Q11) | un élève qui réussit systématiquement **avec** aide ne progresse vers la maîtrise que s'il réussit **ensuite sans** aide |
| Progrès | ne fait jamais régresser l'élève, et ne bloque rien (cohérent avec Q1) |
| Preuve dédupliquée (Q3) | cohérent avec Q4 : au moins 2 tâches, donc au moins 2 preuves |

## L5.7 Ce que « maîtrise » ne signifie pas

**[VALIDÉ — Q3]** Le mot « maîtrisé » est employé par ce document au sens d'un
**seuil contractuel** : les critères de Q3 sont remplis. C'est un terme de
produit, pas un jugement pédagogique.

| Ce que « maîtrise » **signifie** ici | Ce qu'elle **ne signifie pas** |
|---|---|
| 3 réussites autonomes, sur ≥2 tâches distinctes | que l'élève a compris la notion |
| dont au moins 1 en vérification ultérieure (≥24 h, [Q6](#l54-la-vérification-ultérieure--q6--le--peut-être-quil-avait-deviné)) | que l'élève saura le refaire dans un autre contexte |
| et que les critères de Q4 sont respectés | **que la pédagogie de Relio est validée** |
| | qu'un validateur documentaire passant atteste de la qualité de l'enseignement |

**[VÉRIFIÉ]** Le moteur n'a **aucun** statut de maîtrise aujourd'hui :
`STATUTS_OBJECTIF` ne contient que `non_evalue`, `signal`, `hypothese`, `constat`
(`progression.ts:29-32`). Le mot « maîtrisé » est donc, en l'état, une **cible de
contrat** et non un état produit.

---

# LIVRABLE 6 — SUIVI ET STOCKAGE LOCAL (données client)

## L6.1 Ce qui est stocké aujourd'hui

**[VÉRIFIÉ]** Le suivi est **local au navigateur**, dans une clé
`relio.observations.v1` (`frontend/src/lib/observations.ts`), plafonnée à **500
observations**. Aucune persistance serveur, aucun compte élève, aucun appel IA.

**[VÉRIFIÉ]** Le serveur n'a **aucun** état de progression : `parcours.ts` renvoie
les corrections, `progression.ts` est une **fonction pure** recalculée à partir
d'un journal fourni par le client.

## L6.2 Les données minimales — les trois champs à définir

**[VALIDÉ — Q3, Q4, Q6, Q8, Q11]** Pour appliquer « 3 réussites autonomes sur
≥2 tâches distinctes, dont 1 en vérification ultérieure », le journal local doit
porter, par tentative :

| Champ | Règle qu'il sert | Existe aujourd'hui ? |
|---|---|---|
| `exerciceId` | identifier la tâche, pour dédupliquer (Q3) | ✅ oui — `observations.ts:42` |
| `rang` | situer la tentative sur l'exercice | ✅ oui — `observations.ts:44` |
| `statut` | compter réussites / erreurs | ✅ oui — `observations.ts:46` |
| `categorie` | rejouer le tri de la cause (Q2) | ✅ oui — `observations.ts:48` |
| `niveauAide` | tracer l'aide reçue (Q11) | ✅ oui mais **insuffisant**, voir ci-dessous |
| `reussiteApresAides` | … | ⚠️ **collant**, ne peut pas servir au décompte |
| **`nbIndicesConsultes`** | **Q11** — distinguer indices disponibles / consultés | ❌ **à définir** |
| **`estVerificationUlterieure`** | **Q3, Q6, Q8** — la preuve différée | ❌ **à définir** |
| **`expressionTache`** | **Q4** — vérifier la diversité des expressions | ❌ **à définir** |
| **horodatage** | **Q6** — les 24 h | ❌ **à définir** |

### Correction importante par rapport à la v1.1

**[VÉRIFIÉ]** La v1.1 déclarait `objectifId`, `signatureErreur` et
`nbEchecsAuPrecedent` comme « ✅ oui ». **C'est faux pour le journal local.**
L'interface `Observation` de `frontend/src/lib/observations.ts:41-51` ne contient
**que** : `exerciceId`, `rang`, `reponse`, `statut`, `categorie`, `niveauAide`,
`reussiteApresAides`. Ni `objectifId`, ni `signatureErreur`, ni `nbEchecsAuPrecedent`,
ni aucun horodatage.

**[VÉRIFIÉ]** `niveauAide` existe mais **ne convient pas** à Q11 : c'est un niveau
(1/2/3) déjà atteint, pas un compte d'indices ouverts pendant la tentative.

**[VÉRIFIÉ]** `reussiteApresAides` est un booléen **collant** : dès qu'une
réussite est mémorisée sur un exercice, elle le reste définitivement
(`observations.ts:159`, `.some((o) => o.reussiteApresAides)`). Il ne distingue ni
l'aide de cette tentative de celle d'avant, ni un indice ouvert d'un indice
disponible. **Il ne peut pas servir à compter les preuves de Q3.**

---

### Champ 1 — `nbIndicesConsultes`

| | |
|---|---|
| **Objectif pédagogique** | Permettre à Q11 de distinguer une **réussite autonome** d'un **progrès**. Sans lui, on ne peut pas savoir si l'élève a réussi seul. |
| **Définition opérationnelle** | Nombre d'indices **réellement ouverts** par l'élève pendant cette tentative. Un indice **disponible mais non ouvert** ne compte pas. |
| **Qui le renseigne, et quand** | **Le client (Relio)**, au moment où l'élève ouvre un indice — pas l'élève lui-même, et pas a posteriori. |
| **Règles de calcul** | Incrémenté à chaque ouverture d'indice dans la fenêtre de la tentative ; remis à zéro à chaque nouvelle tentative ; jamais reporté d'une tentative à l'autre (Q11, troisième cas). |
| **Limites du modèle actuel** | Aucun champ équivalent. `niveauAide` ne porte pas cette information, et `reussiteApresAides` est collant. |

**[VALIDÉ — Q11]** C'est précisément ce champ qui rend la distinction
**disponible / consulté** mesurable. Un compteur d'« indices affichés » ne
donnerait pas ce que Q2 exige : un élève qui a trois indices sous les yeux mais
n'en ouvre aucun doit rester en réussite autonome.

---

### Champ 2 — `estVerificationUlterieure`

| | |
|---|---|
| **Objectif pédagogique** | Marquer la tentative qui satisfait les critères de Q6, afin qu'elle puisse servir de preuve différée pour Q3. |
| **Définition opérationnelle** | Booléen indiquant que **les quatre conditions de Q6 sont réunies** : séance distincte, ≥24 h depuis la dernière réussite autonome de la compétence, expression différente, aucun indice consulté pendant la tentative. |
| **Qui le renseigne, et quand** | **La logique de Relio**, et **pas l'élève** — décision explicite de Q8. Il est calculé, pas choisi. |
| **Règles de validation** | `true` **uniquement si** les quatre conditions sont vraies ; `false` sinon. Le champ est **opaque pour l'élève** et ne doit pas apparaître comme un interrupteur. |
| **Limites du modèle actuel** | Aucun horodatage n'est stocké : le calcul des 24 h est **matériellement impossible** aujourd'hui. |

**[VALIDÉ — Q8]** « Ce champ ne suffit pas, à lui seul, à établir la maîtrise. »
Autrement dit : `estVerificationUlterieure === true` est **nécessaire** mais
**non suffisant** — il faut aussi les 2 autres tâches distinctes, les 3 réussites
autonomes, et l'expression différente. Le champ ne porte **aucune** conclusion
pédagogique ; il ne porte qu'un **fait de session**.

---

### Champ 3 — `expressionTache`

| | |
|---|---|
| **Objectif pédagogique** | Permettre à Q4 de vérifier qu'une expression **différente** est bien proposée en vérification, et à Q3 de **dédupliquer** les preuves par tâche. |
| **Définition opérationnelle** | Représentation **normalisée** de l'expression proposée à l'élève (l'énoncé, pas la réponse attendue), afin de pouvoir comparer deux tâches. |
| **Qui le renseigne, et quand** | **Relio**, à la construction de l'observation — c'est une donnée du contenu pédagogique, pas une saisie de l'élève. |
| **Règles de validation** | Comparaison par **normalisation** (espaces, `^`/puissance, ordre des termes), jamais par comparaison de chaînes brutes. |
| **Limites du modèle actuel** | Aucun champ équivalent ; `exerciceId` ne dit rien de l'expression. |

**[HORS-PÉRIMÈTRE] Une chaîne de texte ne suffit pas, et ce document ne prétend pas
le contraire.** Une égalité de chaînes est **insuffisante** pour distinguer deux
tâches, pour trois raisons vérifiables :

1. **Non-normalisation.** `3x+6-x-5` et `3x + 6 - x - 5` sont **la même** tâche
   mais pas **la même** chaîne. Une comparaison brute conclurait à tort qu'il y a
   deux tâches distinctes.
2. **Équivalence mathématique.** Deux écritures de la même expression — `2(x+3)` et
   `2x + 6` — désignent la même tâche. Une égalité de chaînes les traiterait comme
   différentes.
3. **Faux positifs.** Deux exercices différents portant la même expression seraient
   refusés comme « non distincts » par un critère d'égalité stricte.

**La déduplication par tâche ne peut donc pas reposer sur une simple chaîne.**
Elle suppose une **normalisation syntaxique**, c'est-à-dire la réutilisation de
l'analyseur d'expressions déjà présent (`analyseur-expression.ts`), ou un
identifiant de tâche stable fourni par le contenu pédagogique. **Aucune de ces deux
voies n'est implémentée** — c'est un préalable à Q3 et Q4, et il est listé au
[§ L8](#l80-comment-lire-cette-section).

## L6.3 Conservation locale — [VALIDÉ — Q7]

**[VALIDÉ — Q7]** « Conserver localement le journal tant qu'il reste utile à
l'apprentissage, sans suppression automatique arbitraire. Prévoir la possibilité
pour l'élève d'effacer son historique. Expliquer que les données peuvent être
perdues si les données du navigateur sont supprimées ou si l'élève change
d'appareil. À ce stade, ne pas envoyer le journal au serveur. »

**[HORS-PÉRIMÈTRE]** Q7 est une décision **produit**, pas une politique de
protection des données des mineurs finalisée. Ce document ne prétend pas livrer une
telle politique et n'en réinvente aucune.

### Les cinq exigences, et leur état réel

| # | Exigence Q7 | État vérifié |
|---|---|---|
| 1 | Conserver **tant qu'il reste utile** | ⚠️ voir la contradiction ci-dessous |
| 2 | **Sans suppression automatique arbitraire** | ❌ **violé en l'état** |
| 3 | L'élève **peut effacer** son historique | ✅ **déjà implémenté** — `effacerJournal()`, `observations.ts:184` |
| 4 | **Expliquer** la perte possible de données | ❌ à faire côté interface — hors périmètre |
| 5 | **Ne pas envoyer** le journal au serveur | ✅ **déjà respecté** — aucune persistance serveur |

### ⚠️ Contradiction relevée : le plafond de 500 viole l'exigence 2

**[VÉRIFIÉ]** `TENTATIVES_MAX = 500` (`observations.ts:64`) et le journal est
**tronqué automatiquement** à l'écriture :

```ts
const journal = [...existantes, complete].slice(-TENTATIVES_MAX);
```
(`observations.ts:167`)

Les **500 tentatives les plus anciennes sont supprimées silencieusement**, sans
que l'élève soit informé et sans que ce soit lié à leur utilité.

**[VALIDÉ — Q7]** C'est exactement ce que Q7 interdit : une suppression
automatique, arbitraire (fondée sur un compte, pas sur l'utilité), et invisible.
Le plafond existait pour éviter qu'une session longue ne fasse grossir le stockage —
c'est une contrainte technique légitime, mais elle **ne peut pas rester un
arbitrage silencieux** face à une décision produit.

**Ce que Q7 impose donc à l'implémentation :**

| Point | Exigence |
|---|---|
| Base de la suppression | l'**utilité à l'apprentissage**, pas un compteur fixe |
| Information de l'élève | toute suppression doit être **explicite**, jamais silencieuse |
| Compatibilité | l'**effacement par l'élève reste prioritaire** et immédiat |

**[HORS-PÉRIMÈTRE]** Le chantier 8.2 **ne modifie pas** `TENTATIVES_MAX` : cela
reviendrait à changer le code applicatif, ce qui est interdit. La contradiction est
**constatée, documentée et transmise**, pas corrigée.

### Le lien avec la vérification différée — la contrainte oubliée

**[VALIDÉ — Q6 + Q7]** Les deux décisions se rejoignent sur un point qui mérite
d'être explicite, parce qu'il n'était visible dans aucune des deux :

> La vérification ultérieure exige **24 h** et une **séance distincte**.
> Le journal est **local au navigateur**.
> Donc les données de la dernière réussite autonome **doivent survivre au moins
> 24 h**.

**[VÉRIFIÉ]** Avec un plafond de 500, ce n'est pas garanti. Un élève très actif
peut faire tomber ses premières tentatives hors du journal en moins de 24 h, et la
vérification se retrouve **sans point de comparaison** : impossible de vérifier
l'expression différente, impossible de dater la dernière réussite.

**Conséquence : Q6 exige que le journal survive au moins 24 h.** C'est un
exigence chiffrée minimale que ce document tire des deux décisions combinées, et
qui devra être respecté par toute politique de rétention ultérieure.

### Limites assumées

**[VALIDÉ — Q7]** Le stockage local a des limites **réelles et à dire à l'élève** :
- les données disparaissent si l'élève **vide les données du navigateur** ;
- elles **ne suivent pas** l'élève s'il **change d'appareil** ;
- elles sont **liées à ce navigateur**, pas à un compte.

**[HORS-PÉRIMÈTRE]** La formulation de cette information à l'élève relève de
l'interface, hors de ce chantier. Q7 exige qu'elle existe ; elle n'existe pas
encore.

## L6.4 Ce que ce chantier ne fait pas

**[VÉRIFIÉ]** + **à respecter strictement** :
- **aucun** champ n'est ajouté au schéma applicatif : `Observation` reste
  inchangée (`observations.ts:41-51`) ;
- `TENTATIVES_MAX`, la clé `v1` et `effacerJournal()` **restent tels quels** ;
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

## L7.4 Cas de progression — trois colonnes

**Lecture des colonnes :**
- « Aujourd'hui » = comportement **vérifié** du moteur ;
- « Cible » = comportement **validé** par le responsable produit, **non implémenté** ;
- « Type » = **documentaire** (vérifiable sur le papier, sans code) ou
  **implémentation** (nécessitera un vrai moteur pour être exécuté).

| # | Situation | Aujourd'hui [VÉRIFIÉ] | Cible [VALIDÉ] | Type |
|---|---|---|---|---|
| T-21 | 0 réponse sur `OO-L1-1` | `non_evalue` | `non_evalue` | implémentation |
| T-22 | 1 réponse fausse | `signal` | `signal` | implémentation |
| T-23 | 2 réponses fausses | `hypothese` | `hypothese` | implémentation |
| T-24 | 3 réponses justes **avec indice consulté**, 3 tâches distinctes | compte **3** `correcte` | **0 réussite autonome** — 3 progrès | implémentation |
| T-25 | 3 réussites autonomes sur **une seule** tâche | compte **3** | **1 preuve** — dédupliqué | implémentation |
| T-26 | 2 réussites autonomes, 2 tâches distinctes | rien de concluant | **acquis fragile** | implémentation |
| T-27 | 3 réussites autonomes, 2 tâches, **sans** vérification | rien de concluant | **acquis fragile** | implémentation |
| T-28 | 3 réussites autonomes, ≥2 tâches, 1 en vérification différée conforme | rien de concluant | **maîtrisé** | implémentation |
| T-29 | idem T-28 mais **même expression** en vérification | rien de concluant | **refusé** — Q4 violée | implémentation |
| **T-38** | Vérification faite **12 h** après la dernière réussite autonome | — | **refusée** — moins de 24 h (Q6) | **documentaire** |
| **T-39** | Vérification faite **25 h** après, séance distincte | — | **acceptée** comme preuve différée | **documentaire** |
| **T-40** | Vérification faite dans la **même séance**, 30 h après | — | **refusée** — Q6 exige une séance distincte | **documentaire** |
| **T-41** | Réussite après **indice disponible mais non ouvert** | — | **réussite autonome** (Q11, cas 1) | **documentaire** |
| **T-42** | Réussite après **indice ouvert** pendant la tentative | — | **progrès**, pas preuve (Q11, cas 2) | **documentaire** |
| **T-43** | Indice ouvert lors d'une tentative **antérieure**, réussite **sans aide** ensuite | — | **réussite autonome** (Q11, cas 3) | **documentaire** |
| **T-44** | 3 réussites, 2 tâches, mais **aucune** en vérification différée | — | **jamais « maîtrisé »** — Q3 non satisfait | **documentaire** |
| **T-45** | Erreur nouvelle proche d'un piège existant, 2ᵉ occurrence | `hors_perimetre` | **reste neutre** — pas de conversion (Q2 + Q5) | **documentaire** |

### Points de lecture

- **T-24 et T-25 sont les écarts les plus dangereux** : ce sont des cas où le
  moteur actuel **conclurait trop vite**, parce qu'il ne connaît ni l'aide ni la
  déduplication par tâche. Les deux doivent être **refusés**.
- **T-27 et T-44 disent la même chose par les deux bouts** : T-27 montre que les
  3 preuves ne suffisent pas sans différé, T-44 montre qu'un différé sans les
  3 preuves ne suffit pas non plus. **Les deux conditions sont cumulatives.**
- **T-38 à T-40 impliquent une notion de séance** que le moteur n'a pas et que le
  journal local ne peut pas porter aujourd'hui (aucun horodatage). Ils sont
  **documentaires** : on peut décider qu'ils doivent être refusés, mais pas les
  exécuter.
- **T-41 à T-43 sont directement issus de Q11** et se lisent sans le moteur :
  c'est ce qui permet de les trancher dès ce chantier.
- **T-45** est le cas que Q5 refuse : une récurrence n'est ni une analyse ni une
  validation. Le résultat correct est **neutre**, pas « presque reconnu ».

## L7.5 Cas où le système doit **refuser** de conclure

| # | Situation | Comportement exigé | Origine |
|---|---|---|---|
| T-30 | Cause inconnue (`erreur_non_identifiee`) | Aucune catégorie de difficulté plausible n'est enregistrée | [VÉRIFIÉ] |
| T-31 | Une seule réussite | Aucun statut de maîtrise n'est affiché | [VÉRIFIÉ] |
| T-32 | Réussite après un indice consulté | **Progrès**, jamais réussite autonome | **Q3, Q11** |
| T-33 | Élève qui réussit en recopiant la réponse d'un indice | Le système ne peut pas le détecter → **ne pas prétendre l'avoir détecté** | [VÉRIFIÉ] (§ L5.5) |
| T-34 | Erreur observée sur `OO-L1-1` | Vérification ciblée, **puis** remédiation courte **ou** retour à l'exercice — **jamais** de blocage | **Q1, Q10** |
| T-35 | Cause étayée sur E1 (`2x + 11` → `signe_non_distribue`) | Aide ciblée sur `oubli_de_distribuer_un_facteur` | **Q2**, branche A |
| T-36 | Cause non étayée sur E3 (`x^2 - x - 6`, hors pièges) | Reste **neutre**, invite à réessayer | **Q2**, branche C |
| T-37 | Réponse illisible (`2x + 1 zzz`) | Inviter à réessayer, **jamais** un indice de méthode | [VÉRIFIÉ] + **Q2** |
| T-46 | Vérification **trop tôt** (< 24 h, ou même séance) | N'est pas une preuve différée ; reste une tentative ordinaire | **Q6** |
| T-47 | `estVerificationUlterieure === true` **seul** | **Ne suffit pas** à établir la maîtrise | **Q8** |
| T-48 | Expression de vérification **identique** à la première réussite | Vérification **invalidée** | **Q4** |
| T-49 | Données du navigateur effacées | Le suivi repart de zéro ; l'élève doit en être **informé** | **Q7** |

### Distinction contrôles documentaires / tests d'implémentation

**[VÉRIFIÉ]** Les cas ci-dessus se répartissent nettement :

| Nature | Cas | Peut être exécuté aujourd'hui ? |
|---|---|---|
| **Documentaire** (règle écrite, vérifiable par lecture) | T-34, T-35, T-36, T-37, T-41 à T-46, T-48, T-49 | **Oui** — ce sont des énoncés de comportement |
| **Implémentation** (nécessite un moteur les calculant) | T-21 à T-33 | **Non** — `progression.ts` n'a ni notion d'aide, ni de tâche, ni de délai |

**Le validateur de ce chantier ne contrôle que la première catégorie**, par
comparaison de texte. Il ne simule **aucun** des cas de la seconde. Le dire
autrement serait faux.

---

# LIVRABLE 8 — QUESTIONS DE VALIDATION

## L8.0 Comment lire cette section

**Q1 à Q11 sont arbitrées** par le responsable produit (chantiers 8.1 et 8.2) et
sont reprises mot pour mot au [§ L0.5](#05-décisions-validées-q1-à-q11).

**Aucune question de décision produit ne reste ouverte.** Les questions qui suivent
ne sont plus des arbitrages à rendre : ce sont des **choix techniques** à
concevoir lors du chantier d'implémentation.

### Récapitulatif des décisions

| # | Décision validée | Section |
|---|---|---|
| **Q1** | Prérequis sans blocage | [L1.2](#l12-connaissances-préalables-et-remédiation) |
| **Q2** | Tri de la cause en 3 branches | [L2.5](#l25-le-tri-de-la-cause--décision-validée-q2), [L4.3](#l43-la-question-de-diagnostic--décision-validée-q2) |
| **Q3** | 3 réussites probantes, déduplication | [L5.2](#l52-trois-niveaux-de-réussite-du-plus-faible-au-plus-fort), [L5.6](#l56-réussite-autonome--progrès--preuve--validé--q11) |
| **Q4** | ≥2 tâches distinctes, expression différente | [L5.4](#l54-la-vérification-ultérieure--q4--q6--le--peut-être-quil-avait-deviné) |
| **Q5** | Enrichissement progressif des pièges, pas de diagnostic forcé | [L2.5](#le-cas-où-q2-bute-sur-létat-actuel-du-corpus--tranché-par-q5) |
| **Q6** | Vérification : séance distincte, ≥24 h, sans indice | [L5.4](#l54-la-vérification-ultérieure--q4--q6--le--peut-être-quil-avait-deviné) |
| **Q7** | Conservation locale, effacement possible | [L6.3](#l63-conservation-locale--validé--q7) |
| **Q8** | `estVerificationUlterieure` calculé, non suffisant seul | [L6.2](#champ-2--estverificationulterieure) |
| **Q9** | Nom canonique « Développer et réduire une expression littérale » | [L1.0](#l10-nom-canonique--q9) |
| **Q10** | Une erreur ouvre une vérification, ne conclut pas | [L1.2](#l12-connaissances-préalables-et-remédiation) |
| **Q11** | Disponible ≠ consulté ; aide antérieure ne disqualifie pas | [L5.6](#l56-réussite-autonome--progrès--preuve--validé--q11) |

### Questions techniques restant à concevoir

**Aucune n'est un arbitrage produit.** Ce sont des choix d'implémentation que ce
chantier documentaire ne fait pas.

| # | Question | Pourquoi elle est ouverte |
|---|---|---|
| **I-1** | Quelle **forme de normalisation** pour `expressionTache` ? | Une chaîne brute ne distingue pas les tâches ([L6.2](#champ-3--expressiontache)). Réutiliser l'analyseur ou fournir un identifiant stable : les deux voies existent, aucune n'est choisie |
| **I-2** | Comment définir une **« séance distincte »** (Q6) ? | Q6 l'exige sans dire si c'est une journée, un créneau, ou 24 h glissantes. Aucun moyen de le savoir n'existe aujourd'hui |
| **I-3** | Que se passe-t-il si la **vérification est ratée** ? | Q3 ne le dit pas. « Acquis fragile » avec conservation des preuves est une proposition, pas une décision |
| **I-4** | Quelle **politique de rétention** conforme à Q7 ? | Q7 interdit la suppression automatique arbitraire ; `TENTATIVES_MAX = 500` la pratique. Le compromis n'est pas conçu |
| **I-5** | Où et comment **expliquer** la perte possible des données ? | Q7 l'exige ; aucun écran ne le fait aujourd'hui. Relève de l'interface |
| **I-6** | Quel **contenu** pour la vérification ciblée et la remédiation courte de Q10 ? | Q10 décrit le circuit, pas les exercices qui l'alimentent |
| **I-7** | Comment corriger les **deux libellés erronés** (C-1) ? | Q9 fixe le nom canonique ; `blocs.ts:29` et `matrice:128` sont hors périmètre de ce chantier |

## L8.1 Ce qui n'est PAS une question de validation

Pour éviter de transformer ce chantier en réunion :

- **D5 n'est pas remis en cause.** L'ordre `incorrect` → `partiellement_correct` →
  `resultat_juste_consigne_non_respectee` → `a_determiner` → `correct` est
  considéré comme acquis.
- **Le nombre de signatures est un fait** : 12 (C-2). Il n'y a pas à trancher.
- **La taxonomie fermée n'est pas discutée** : `hors_perimetre` →
  `erreur_non_identifiee` est une garantie de non-invention, à préserver.
- **Le passage du validateur documentaire n'est pas une validation pédagogique.**
  Il vérifie que la spécification dit la vérité sur le code et sur le statut des
  décisions. Il ne dit rien de la qualité de l'enseignement.

## L8.2 Défauts relevés au passage, hors périmètre de ce chantier

### Le défaut « could-tu »

**[VÉRIFIÉ]** `backend/src/contenu/aides.ts:131` contient, dans un message destiné
à l'élève, le mot anglais **« could-tu »** au lieu de « pourrais-tu » :

> « Regarde le numérateur et le dénominateur de ta fraction : par quel nombre
> **could-tu** les diviser tous les deux ? »

Défaut **réel**, visible par l'élève, sur l'objectif `OO-L5-2` (hors périmètre
`OO-L1-1`). Signalé, **non corrigé** ici.

### Les deux libellés erronés de la compétence

**[VÉRIFIÉ]** Q9 fixe le nom canonique **« Développer et réduire une expression
littérale »**. Ni `blocs.ts:29` (« …une expression algébrique ») ni
`matrice-couverture-competences.md:128` (« Développer une expression algébrique
(distributivité, identités remarquables) ») ne portent ce nom.

**[HORS-PÉRIMÈTRE]** Les corriger modifierait le code applicatif ou la matrice,
ce que le chantier 8.2 interdit. Voir [I-7](#l80-comment-lire-cette-section).

### Le plafond de 500 et l'exigence de Q7

**[VÉRIFIÉ]** `TENTATIVES_MAX` tronque silencieusement le journal
(`observations.ts:64`, `:167`), ce que Q7 interdit. Voir
[L6.3](#l63-conservation-locale--validé--q7) et [I-4](#l80-comment-lire-cette-section).

---

## CONCLUSION DU DOCUMENT

**Ce qui est établi.** La compétence est définie (L1), sa taxonomie est celle du
code et elle est vérifiée (L2), D5 est reprise intacte avec ses limites propres à
`OO-L1-1` établies (L3), le tri de la cause et la question diagnostique sont
spécifiés (L4), les exigences de réussite, de vérification différée et de maîtrise
sont définies avec leurs cas de test (L5, L7), et les trois champs de données
nécessaires sont spécifiés sans être ajoutés (L6).

**Ce qui est validé.** Les onze décisions de contrat **Q1 à Q11**
([§ L0.5](#05-décisions-validées-q1-à-q11)), reprises mot pour mot.

**Ce qui reste à concevoir.** Sept questions **techniques** (I-1 à I-7), qui ne
sont pas des arbitrages produit.

**Statut.** Le contrat pédagogique est **complet et cohérent**. Il **n'est pas
implémenté** : aucun des champs décrits n'existe, aucune des règles de L5 n'est
calculable par le moteur actuel. Ce document ne constitue pas une validation
pédagogique, et le succès du validateur documentaire ne vaut pas davantage.