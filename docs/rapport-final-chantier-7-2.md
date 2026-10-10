# Rapport final — Chantier 7.2 : date de référence du calendrier scolaire

**Date** : 2026-10-10
**Objet** : fixer le début de l'année scolaire 2026-2027 au lundi 7 septembre 2026
**Périmètre** : une correction de date, et rien d'autre
**Statut** : 🟠 **TERMINÉ AVEC RÉSERVES**

> **Convention de lecture**
>
> - ✅ **Vérifié** — contrôlé dans ce chantier, avec une sortie observable.
> - 📋 **Déclaré** — transmis par le responsable du projet, non observé indépendamment.
> - ⏳ **À vérifier** — non testé ici, ou dépendant d'une action du propriétaire.

---

## 1. Modifications réalisées

### 1.1 Inventaire préalable des références à `2026-09-05`

Avant toute modification, la date a été recherchée dans les trois dépôts.
✅ **Vérifié** — le relevé est exhaustif :

| Emplacement | Nature | Traitement |
|---|---|---|
| `backend/src/lib/calendrier.ts` | **Défaut du code** | Corrigé |
| `backend/test/calendrier.test.ts` | 6 occurrences (dates + énoncés) | Adaptées |
| `backend/test/parcours.test.ts` | 4 occurrences | Adaptées |
| `backend/docs/CONTRAT-API.md` | 2 occurrences (tableau + § 11) | Mises à jour |
| `Relio/docs/rapport-final-chantier-7-1.md` | 5 occurrences | **Conservées** — rapport d'un chantier passé |
| `frontend` | **Aucune occurrence** | Non modifié |

Le rapport du chantier 7.1 décrit ce qui était vrai à ce jour-là. Le modifier
pourrait le rendre faux sur ce qu'il a constaté ; il est conservé tel quel, et
le présent rapport fait foi pour la date actuelle.

### 1.2 Fichiers modifiés — 4 fichiers, backend uniquement

| Fichier | Changement |
|---|---|
| `src/lib/calendrier.ts` | `DEBUT_ANNEE_DEFAUT` : `2026-09-05` → `2026-09-07`, commentaire de justification |
| `test/calendrier.test.ts` | Suite 2026-2027 réécrite sur le lundi 7 septembre, + 2 contrôles renforcés |
| `test/parcours.test.ts` | Assertions de date mises à jour, test de priorité renforcé |
| `docs/CONTRAT-API.md` | Valeurs, avertissement de migration, tableau des ouvertures |

**Le frontend n'a pas été modifié** : ✅ **Vérifié** — `grep` confirme qu'il ne
contient aucune référence à la date, aucun calcul de semaine, et qu'il reçoit
`anneeScolaire` du backend sans l'interpréter. Aucune raison technique de le
toucher.

### 1.3 Ce qui a été délibérément conservé

| Élément | État |
|---|---|
| `ANNEE_SCOLAIRE_DEBUT ?? DEBUT_ANNEE_DEFAUT` | ✅ Inchangé — le changement d'année reste possible sans redéploiement |
| B1 · S1, B2 · S5, B3 · S10 | ✅ Inchangé — séquencement pédagogique validé, vérifié par test |
| Contenu, corrections, indices, protections | ✅ Aucun fichier de contenu pédagogique touché |

### 1.4 Commit publié

| Dépôt | SHA | Objet |
|---|---|---|
| `relio-backend` | **`293d997`** | `fix(calendrier): rentrée scolaire au lundi 7 septembre 2026` |
| `relio-frontend` | *(aucun)* | Aucun changement nécessaire |
| `Relio` | `2df6620` + ce rapport | Documentation |

✅ **Vérifié** — SHA distant relu après envoi, identique au SHA local.

---

## 2. Tests exécutés

### 2.1 Commandes et résultats réels

| Dépôt | Commande | Résultat |
|---|---|---|
| backend | `npm run typecheck` | ✅ aucune erreur |
| backend | `npm test` | ✅ **155 / 155**, 30 suites, 0 échec |
| backend | `npm run build` | ✅ |
| frontend | `npm run typecheck` | ✅ aucune erreur |
| frontend | `npm test` | ✅ **42 / 42**, 8 suites |
| frontend | `npm run build` | ✅ |

Aucun test n'a été supprimé, affaibli ou contourné. Le total reste **155** côté
backend : des contrôles ont été **renforcés**, pas retirés.

### 2.2 Deux contrôles affaiblis puis renforcés

Deux erreurs sont apparues pendant l'adaptation. Les deux venaient de **mes
données de test**, pas du code — mais elles auraient pu être « corrigées » en
assouplissant les assertions. Elles ont été traitées dans l'autre sens :

**a) Une attente fausse.** J'avais écrit que le 6 octobre 2026 serait en
semaine 4. Le calcul correct est semaine 5 : le lundi 5 octobre ouvre la
semaine 5, et le mardi 6 est toujours dedans. L'assertion a été remplacée par
les trois dates qui prouvent le découpage (5 → S5, 6 → S5, 12 → S6).

**b) Un test qui ne prouvait rien.** Le test de priorité de la variable
d'environnement fixait `ANNEE_SCOLAIRE_DEBUT = '2026-09-05'`, **identique au
défaut du code**. Il aurait donc passé aussi bien si la variable était
totalement ignorée. Il utilise désormais une date différente et vérifie les
deux lectures : avec la variable à `2026-09-14`, le 7 septembre est hors année
scolaire ; sans elle, il est en semaine 1. C'est ce contrôle qui protège du
défaut du chantier 7.1 — une année périmée en production refermant tous les
blocs.

### 2.3 Les contrôles peuvent-ils échouer ?

✅ **Vérifié** — chaque contrôle a été déclenché volontairement en modifiant le
code, puis remis :

| Défaut injecté | Tests en échec |
|---|---|
| Retour au samedi 5 septembre | **3** |
| Rentrée non-lundi (samedi 12 septembre) | **4** |
| Variable d'environnement ignorée | **1** |
| État nominal | 0 |

Le second cas est nouveau et important : **aucun test ne détectait
précédemment une rentrée non-lundi.** C'est précisément la propriété que ce
chantier corrige.

### 2.4 Non-régression du parcours pédagogique

✅ **Vérifié** — sur le serveur **compilé**, année 2026-2027.

| Contrôle | Résultat |
|---|---|
| Parcours en semaine 6 | B1 ouvert (6 ex.), B2 ouvert (3 ex.), B3 fermé (0 ex.) |
| Corrections conformes (10 cas) | **10 / 10** |
| Indices servis (3 blocs × 3 paliers) | **9 / 9** |
| Bloc fermé : énoncé / indice / correction / progression | **403** sur les 4 |

Les corrections couvrent les trois statuts, y compris le cas dégénéré du
chantier 6 : `4x² − 9` et `√50` restent `partielle`, jamais `fausse`.

> Deux cas B3 avaient d'abord renvoyé un statut vide : B3 est fermé en semaine
> 6. Rejoués en semaine 10, ils passent. **C'est le comportement attendu du
> garde-fou, pas une régression** — il est signalé ici pour que la lecture des
> chiffres ne prête pas à confusion.

---

## 3. Calendrier obtenu

✅ **Vérifié** — par tests automatisés et par appel HTTP réel.

| Bloc | Leçon | Semaine | Ouverture | Jour de la semaine |
|---|---|---|---|---|
| **B1** | Calcul littéral | S1 | **lundi 7 septembre 2026** | lundi |
| **B2** | Racines carrées | S5 | **lundi 5 octobre 2026** | lundi |
| **B3** | Calcul numérique | S10 | **lundi 9 novembre 2026** | lundi |

| Propriété | Résultat |
|---|---|
| Semaine 1 commence le lundi 7 septembre 2026 | ✅ |
| Bloc fermé juste avant l'ouverture | ✅ inaccessible |
| Bloc ouvert à la semaine prévue | ✅ accessible |
| Bloc fermé : énoncé, indice, correction, progression | ✅ **403** sur les 4 |
| `ANNEE_SCOLAIRE_DEBUT` explicite remplace le défaut | ✅ vérifié dans les deux sens |
| Aucune dépendance à la date d'exécution des tests | ✅ dates toutes explicites |

### 3.1 Ce que la correction résout

Le rapport du chantier 7.1 signalait qu'une rentrée un samedi décalait les
ouvertures d'un samedi, et recommandait de fixer la rentrée au lundi. **C'est
fait, et c'est désormais vérifié par test** : une rentrée non-lundi fait
échouer la suite.

---

## 4. Configuration de production

### 4.1 Ce que j'ai réellement vérifié

✅ **Vérifié** — l'absence d'accès à Railway, établie factuellement :

| Vérification | Résultat |
|---|---|
| Binaire `railway` | **Absent** |
| Variables `RAILWAY_*` dans l'environnement | **Aucune** |
| Accès à l'API Railway | Non authentifié (HTTP 404) |

### 4.2 Ce qui reste à vérifier manuellement

⏳ **À vérifier par le propriétaire.** La valeur actuellement enregistrée dans
l'environnement Railway **n'est pas connue** et **ne peut pas l'être** depuis
ce dépôt.

**Le point critique :** `ANNEE_SCOLAIRE_DEBUT` a **priorité sur le défaut du
code**. Si elle vaut encore `2026-09-05` dans Railway, **la correction
déployée n'aura aucun effet visible** : les semaines resteront décalées d'un
samedi.

| Situation dans Railway | Action |
|---|---|
| Variable absente | Le défaut du code s'applique : `2026-09-07`. **Rien à faire.** |
| Variable = `2026-09-05` | **La remplacer par `2026-09-07`**, puis redémarrer le service. |
| Variable = autre valeur périmée | La remplacer par `2026-09-07`, puis redémarrer. |

Emplacement : Railway → projet `relio-backend` → service → onglet **Variables**.

> Aucun secret n'est demandé ni nécessaire : seule la valeur de cette variable
> est à contrôler, et elle est publique dans le dépôt.

---

## 5. Déploiement

### 5.1 Ce qui a été fait

| Action | État |
|---|---|
| Correction écrite et testée | ✅ |
| Commit backend `293d997` poussé sur `main` | ✅ SHA distant vérifié |
| Modification du frontend | ✅ **aucune, et non nécessaire** |
| Rapport poussé sur `Relio` | ✅ |

### 5.2 Ce qui n'a pas été fait — et ce que cela signifie

| Action | État |
|---|---|
| **Redéploiement du backend sur Railway** | ❌ **Non effectué** — aucun accès |
| Vérification de la configuration Railway | ❌ Non effectuée |
| Vérification du parcours en production | ❌ Non effectuée |

> **Le code est publié, la production n'est pas mise à jour.** Un push sur
> GitHub ne redéploie rien : tant que Railway n'a pas redéployé, la production
> tourne avec l'ancien code et l'ancienne date.

Le propriétaire ayant confirmé que le parcours fonctionne en production, un
redéploiement est nécessaire **uniquement** si Railway ne redéploie pas
automatiquement à chaque push sur `main`. À vérifier de ce côté également.

### 5.3 Contrôle à effectuer après redéploiement

Sur la page de parcours, en cours d'année :

1. Le message doit indiquer la bonne semaine.
2. `GET /api/v1/parcours` doit renvoyer `"debut": "2026-09-07"` — **le contrôle
   le plus direct et le plus fiable**.

Si `"debut"` renvoie `2026-09-05`, c'est que la variable d'environnement prime
encore sur le code, et c'est elle qu'il faut modifier.

---

## 6. Réserves restantes

### 6.1 Réserve principale — la production

⏳ **Tant que Railway n'est pas reconfiguré et redéployé, la correction n'est
pas visible.** Le dépôt et la production sont deux états distincts, et seul le
premier a été agi sur ce chantier.

C'est la seule réserve qui empêche de conclure en « TERMINÉ ».

### 6.2 Réserves du chantier 7, inchangées

| # | Réserve | État |
|---|---|---|
| R1 | **Règle D5** — lecture « juste mais mal formé » non arbitrée par l'enseignant | Inchangée. Hors périmètre de ce chantier, explicitement exclu. |
| R2 | **Hypothèse H1** — saisie algébrique sur téléphone non testée avec de vrais élèves | Inchangée. |
| R3 | **Visibilité du dépôt GitHub** — contenus officiels du BEPC versionnés | Inchangée. Juridique. |
| R4 | **État de la CI** — non observé (`gh` absent de l'environnement) | Inchangée. |

Aucune de ces réserves n'est liée à la date ; aucune n'a été traitée, et aucune
ne devait l'être.

### 6.3 Une observation sur la méthode

Ce chantier est resté dans un périmètre étroit et **aucun contenu pédagogique
n'a été touché** — conformément à la consigne.

Deux contrôles ont été renforcés plutôt que contournés, dont un qui manquait
auparavant (rentrée non-lundi). C'est le seul ajout de fond : il transforme une
correction ponctuelle en propriété vérifiée, ce qui empêche le problème de
revenir par une modification ultérieure.

---

## 7. Statut du chantier

# 🟠 TERMINÉ AVEC RÉSERVES

**La correction demandée est faite, vérifiée et publiée.** Le backend utilise
le lundi 7 septembre 2026 ; les trois blocs s'ouvrent les lundis 7 septembre,
5 octobre et 9 novembre 2026 ; le séquencement pédagogique, les corrections, les
indices et les protections de blocs fermés sont inchangés et vérifiés. 155 tests
backend et 42 frontend passent, typecheck et builds sont verts.

**Une réserve empêche de conclure en « TERMINÉ » :**

> **La production n'a pas été mise à jour et sa configuration n'a pas pu être
> vérifiée.** Aucun accès à Railway n'existe depuis ce chantier — établi
> factuellement, pas supposé. Et comme `ANNEE_SCOLAIRE_DEBUT` prime sur le
> défaut du code, **si cette variable vaut encore `2026-09-05` dans Railway,
> la correction déployée restera invisible**. Le contrôle tient en une ligne :
> après redéploiement, `GET /api/v1/parcours` doit renvoyer
> `"debut": "2026-09-07"`.

Ce n'est pas une réserve sur la qualité du code — le dépôt est correct et
testé. C'est une réserve sur le **déploiement**, qui ne peut être levée que par
le propriétaire.

Les réserves du chantier 7 (règle D5, hypothèse H1, visibilité du dépôt, état
de la CI) subsistent sans avoir été touched : hors périmètre de ce chantier.

---

*Documents liés : `docs/rapport-final-chantier-7-1.md`,
`docs/rapport-final-chantier-7.md`, `data/referentiel-maths-3e-cm-2025-2026.json`.
Contrat : `relio-backend/docs/CONTRAT-API.md` § 11.*
