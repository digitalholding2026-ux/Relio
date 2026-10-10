# Rapport final — Chantier 7.4 : audit et correction des messages d'aide

**Date** : 2026-10-10
**Objet** : rendre tous les messages affichés aux élèves compréhensibles et concrets
**Statut** : 🟢 **TERMINÉ** — corrigé, testé et **vérifié en production**

> - ✅ **Vérifié** — contrôlé dans ce chantier, sortie observable.
> - ⏳ **À vérifier** — non testé ici, ou dépendant d'une action du propriétaire.
>
> Le défaut signalé — « Reprends la méthode de `OO-L1-2`… » — a été reproduit,
> corrigé, et **constaté corrigé en production** par appels HTTP après
> redéploiement.

---

## 1. Audit : ce qui a été trouvé

### 1.1 Périmètre audité

Les **deux** dépôts ont été inspectés, et le moteur a été exécuté sur **les
45 pièges documentés** des 12 exercices, en mesurant mécaniquement la présence
d'identifiants techniques dans chaque texte produit.

| Source auditée | Résultat |
|---|---|
| `explication` après réponse fausse | 🔴 **16 messages sur 45** avec identifiant |
| `libelle` (verdict D5) | ✅ aucun — corrigé au chantier 7.3 |
| **36 indices** (12 × 3 paliers) | ✅ **aucun** — déjà conformes |
| Messages du frontend | ✅ aucun — déjà conformes |
| Messages d'erreur de saisie | ✅ aucun — déjà conformes |

**Le défaut était circonscrit à un seul endroit** : le filet de sécurité de
`explicationFausse`.

### 1.2 La cause exacte

Une seule ligne produisait 16 des messages fautifs :

```ts
default:
  return `Reprends la méthode de ${exercice.objectifs.join(', ')} sur un exemple plus simple.`;
```

Deux défauts dans cette ligne :

1. elle **interpole un identifiant technique** destiné à l'élève ;
2. elle est atteinte dans **16 cas sur 45**, car 10 des 12 signatures
   d'erreur n'ont pas d'explication dédiée et retombent toutes dessus
   (`hors_perimetre` est volontairement vide : c'est le cas « cause inconnue »,
   et les deux signatures de la leçon 8 sont hors MVP).

Le second point est le plus important : le message fautif n'était pas une
exception, c'était le **message par défaut** — celui que recevaient les élèves
dans plus d'un tiers des erreurs.

### 1.3 Les identifiants légitimes, distingués

L'audit sépare ce qui doit rester des messages :

| Emplacement | Verdict | Raison |
|---|---|---|
| `blocs.ts`, `exercices.ts` (champs `id`, `objectifs`) | ✅ **Légitime** | Clés de correspondance application ↔ données pédagogiques |
| Tests, logs, documentation, `openapi.yaml` | ✅ **Légitime** | Usage technique, jamais affiché |
| **`explication` renvoyée à l'élève** | 🔴 **Corrigé** | Le client l'affiche tel quel |

---

## 2. La correspondance objectif → aide

Cinq objectifs, cinq méthodes réellement enseignées. Aucun exemple n'est
partagé entre objectifs.

| Objectif | Leçon du référentiel | Action nommée | Exemple résolu |
|---|---|---|---|
| `OO-L1-1` | Calcul littéral | Développer puis regrouper | `2(x + 3) = 2x + 6` · `3(x − 4) = 3x − 12` |
| `OO-L1-2` | Calcul littéral | Factoriser | `3x + 6 = 3(x + 2)` · `4x² − 9 = (2x − 3)(2x + 3)` |
| `OO-L3-1` | Racines carrées | Extraire un carré parfait | `√63 = 3√7` · `√147 = 7√3` |
| `OO-L5-1` | Calcul numérique | Dénominateur commun | `1/2 + 1/3 = 3/6 + 2/6 = 5/6` |
| `OO-L5-2` | Calcul numérique | Réduire une fraction | `6/8 = 3/4` |

Chaque message suit trois temps : **l'action** (« Pour factoriser, il faut… »),
**un exemple résolu**, **puis une invitation** (« Cherche d'abord un nombre ou
une lettre qui divise tous les termes… »).

### 2.1 Deux niveaux de message, du plus précis au plus prudent

| Situation | Message |
|---|---|
| Cause **reconnue** (signature identifiée) | Message de l'erreur : « Quand tu distribues une parenthèse précédée du signe −, ce signe change devant chaque terme. » |
| Cause **inconnue** (`hors_perimetre`) | Méthode de la leçon, **sans** prétendre savoir ce qui a échoué |

Aucune cause n'est inventée. Le message d'erreur inconnue ne dit jamais
« tu as oublié… » ou « tu as confondu… » : le moteur ne le sait pas.

### 2.2 Pourquoi des messages par signature

9 signatures sur 12 nommaient précisément l'erreur ; leur message était
efficace. Il aurait été une **régression pédagogique** de les remplacer par un
texte générique. Les 3 restantes — `hors_perimetre` (délibérément vide : c'est
le cas « cause inconnue ») et `signe_perdu_en_resolution` /
`resolution_incompletee` (leçon 8, hors MVP) — utilisent l'aide d'objectif.

---

## 3. Avant / après

### 3.1 Le message signalé

| | |
|---|---|
| **Avant** | « Reprends la méthode de `OO-L1-2` sur un exemple plus simple. » |
| **Après** | « Pour factoriser, il faut chercher un facteur commun aux deux termes, ou reconnaître une différence de deux carrés. Par exemple : dans 3x + 6, le nombre 3 divise les deux termes, donc 3x + 6 = 3(x + 2). Et 4x² − 9 s'écrit (2x)² − 3², donc 4x² − 9 = (2x − 3)(2x + 3). Cherche d'abord un nombre ou une lettre qui divise tous les termes de ton expression. » |

### 3.2 Exemples réels, avant → après

| Exercice | Piège | Avant | Après (début) |
|---|---|---|---|
| `MVP-B1-E2` | `2x^2 - 2x + 1` | « …méthode de OO-L1-1… » | « Pour développer, il faut distribuer chaque terme dans les parenthèses… » |
| `MVP-B1-E4` | `(2x-3)^2` | « …méthode de OO-L1-2… » | « Pour factoriser, il faut chercher un facteur commun… » |
| `MVP-B2-E3` | `9√2` | « …méthode de OO-L3-1… » | « Pour simplifier une racine, il faut trouver le plus grand carré parfait… » |
| `MVP-B3-E3` | `3/4` | « …méthode de OO-L5-1, OO-L5-2… » | « Pour additionner ou soustraire des fractions, il faut d'abord les écrire avec le même dénominateur… » |

Le dernier cas est particulier : l'ancien message affichait **deux**
identifiants à la fois.

---

## 4. Trois fuites de réponse détectées et corrigées

Un test a révélé un problème **plus grave** que l'identifiant : les aides
donnaient parfois la réponse de l'exercice en cours.

| Fuite | Exercice | Contenu | Correction |
|---|---|---|---|
| 1 | `MVP-B2-E1` (attendu `5√2`) | l'exemple des racines contenait `√50 = 5√2` | remplacé par `√63 = 3√7` |
| 2 | `MVP-B2-E3` (attendu `√2`) | l'exemple contenait `√8 = 2√2` | remplacé par `√147 = 7√3` |
| 3 | `MVP-B2-E3` (attendu `√2`) | le message de signature contenait `√72 = 6√2` | remplacé par `√175 = 5√7` |

> Une aide qui résout l'exercice à la place de l'élève n'est pas une aide.
> C'est précisément pour cela que la règle **« l'aide ne contient jamais la
> réponse attendue d'un exercice du même objectif »** est désormais testée
> sur les 12 exercices.

Les trois exemples de remplacement ont été **recalculés** avec le moteur de
production avant d'être écrits dans les messages.

---

## 5. Fichiers modifiés

### 5.1 Backend — `relio-backend`

| Fichier | Modification |
|---|---|
| `src/contenu/aides.ts` | **Nouveau** — correspondance objectif → aide, et signature → message |
| `src/contenu/correction.ts` | `explicationFausse` délègue aux aides ; suppression de l'interpolation d'identifiant |
| `test/aides.test.ts` | **Nouveau** — 24 contrôles |
| `test/correction.test.ts` | 1 assertion réécrite : elle visait l'ancien texte |

### 5.2 Frontend — `relio-frontend`

**Aucun fichier modifié.** L'audit a établi que les messages du frontend
étaient déjà propres, et qu'ils affichent `libelle` et `explication` tels quels
reçus du serveur. Rien à corriger, donc rien touché.

### 5.3 Éléments explicitement préservés

| Élément | État |
|---|---|
| Réponses attendues, énoncés, règles mathématiques | ✅ **Intacts** — aucun fichier de `exercices.ts` modifié |
| Les 36 indices | ✅ Intacts — déjà conformes |
| Les 4 verdicts D5 et leurs libellés | ✅ Intacts |
| Calendrier et disponibilité des blocs | ✅ Intacts |
| Progression, signatures, catalogue fermé | ✅ Intacts |

---

## 6. Tests, typecheck, builds

### 6.1 Résultats réels

| Dépôt | Tests | Suites | Échecs |
|---|---|---|---|
| `relio-backend` | ✅ **206 / 206** | 44 | 0 |
| `relio-frontend` | ✅ **42 / 42** | 8 | 0 |

| Vérification | Backend | Frontend |
|---|---|---|
| `npm run typecheck` | ✅ | ✅ |
| `npm run build` | ✅ | ✅ |

Progression : **224 → 248 tests** (+24).

### 6.2 Les 8 exigences du chantier

| # | Exigence | Test |
|---|---|---|
| 1 | Aucun identifiant dans un message élève | ✅ tous messages × 45 pièges + 36 indices |
| 2 | Messages associés au bon objectif | ✅ pas de confusion factorisation / racines / développement |
| 3 | Exemples mathématiquement corrects | ✅ recalculés par le moteur de production |
| 4 | Indices conservent leur progression | ✅ 3 paliers, aucun ne donne la réponse avant le 3 |
| 5 | Cohérence avec D5 | ✅ 5 cas, libellés distincts par verdict |
| 6 | 12 exercices et 36 indices accessibles | ✅ non-régression constatée |
| 7 | Blocs fermés protégés | ✅ inchangé, 403 vérifié |
| 8 | Réponses attendues toujours acceptées | ✅ 12/12 restent `correct` |

### 6.3 Les tests peuvent-ils échouer ?

✅ **Vérifié** — trois mutations volontaires.

| Mutation | Tests en échec |
|---|---|
| Filet de sécurité réintroduisant `OO-L1-2` | **1** |
| Aide des racines donnant la réponse de `MVP-B2-E1` | **4** |
| Aide des racines remplacée par un exemple de factorisation | **5** |

### 6.4 Deux erreurs de mes propres tests

Tracées parce qu'elles sont instructives :

1. **La longueur des paliers n'est pas un critère de progression.** J'avais
   écrit que le palier 3 devait être plus long que le palier 1 : c'est faux,
   `MVP-B3-E1` a un palier 1 de 64 caractères et un palier 3 de 14 — et c'est
   correct, car le palier 3 est une dernière ligne très directive. Le critère
   retenu est désormais « **aucun palier 1 ni 2 ne donne la réponse** ».
2. **`0` n'est pas une réponse analysable pour un exercice de racines.** Le
   test envoyait une saisie que la grammaire refuse légitimement. Les
   réponses de test sont désormais choisies par type d'exercice.

Aucune assertion n'a été affaiblie pour obtenir le vert.

---

## 7. Commits et push

| Dépôt | SHA | Objet |
|---|---|---|
| `relio-backend` | **`dd17de0`** | `fix(messages): remplacer les identifiants techniques par des aides concrètes` |
| `relio-frontend` | *(aucun)* | Aucun changement nécessaire |
| `Relio` | *(voir § 7)* | Ce rapport |

✅ SHA distant relu après envoi, identique au SHA local. Branche `main`.

---

## 8. Déploiement — vérifié en production

✅ **Vérifié**, après le push et le redéploiement automatique de Railway.

Le premier contrôle, effectué 15 s après le push, a montré l'**ancien**
message — le redéploiement était en cours (`uptimeSeconds: 1`). Un second
contrôle à ~60 s a confirmé la correction.

### 8.1 Backend — Railway

| Contrôle | Résultat observé |
|---|---|
| `/health` | ✅ `ok`, `environment: production` |
| `MVP-B1-E5` « 7x(x-1) » | ✅ message de factorisation, **contains `OO-L1-2` = false** |
| `MVP-B1-E2` « 4x²+4x+1 » | ✅ message de distribution du signe |
| `MVP-B2-E3` « 9√2 » | ✅ message des racines carrées |
| Identifiant dans un message de production | ✅ **aucun** |
| Bloc B3 en semaine 5 | ✅ fermé, correction refusée en **403** |
| Calendrier | ✅ `2026-09-07`, semaine 5 |

**Le message signalé est corrigé en production.**

### 8.2 Frontend — Vercel

Non redéployé : **aucun fichier modifié**. Le frontend consomme
`explication` sans la retraiter.

### 8.3 Ce qui n'a pas été vérifié

⏳ **Non testé :**

- **le rendu visuel des messages à l'écran** — la règle globale interdit
  désormais tout navigateur local. Les textes API sont constatés en
  production ; leur affichage ne l'est pas ;
- **la saisie au doigt sur un téléphone réel** (hypothèse H1), non traitée
  dans ce chantier ;
- **l'état de la CI** — `gh` est absent de l'environnement.

---

## 9. Limites restant à traiter

| # | Limite | Effet |
|---|---|---|
| L1 | **Le rendu visuel n'est pas observé.** Les messages sont vérifiés côté API, pas à l'écran. | Contrôle manuel : ouvrir un exercice, échouer, lire le message. |
| L2 | **Les aides ne sont pas personnalisées par exercice.** Elles le sont par **objectif**. | Deux exercices d'un même objectif partagent le même message. Choix assumé : l'objectif est le bon niveau de grain, et le moteur ne connaît pas la cause exacte. |
| L3 | **Le message d'erreur inconnue reste général.** | Volontaire : inventer un diagnostic serait faux. |
| L4 | **3 signatures sur 12 n'ont pas de message dédié** (`hors_perimetre`, et les 2 de la leçon 8 hors MVP). | Retombe sur l'aide d'objectif. |
| L5 | **Hypothèse H1, visibilité du dépôt, état de la CI.** | Inchangés depuis le chantier 6. |

---

## 10. Statut du chantier

# 🟢 TERMINÉ

**Les messages affichés aux élèves sont maintenant compréhensibles, concrets et
mathématiquement exacts.**

Le chantier est terminé parce que les quatre conditions sont réunies :

1. **L'audit a porté sur tout le périmètre**, pas sur le seul message
   signalé : 45 réponses, 36 indices, tous les messages du frontend. Il a
   établi que **16 messages sur 45** étaient fautifs — plus d'un tiers des
   erreurs d'un élève aboutissaient à un identifiant technique.
2. **Le problème est corrigé à la racine.** Le filet de sécurité interpolait
   un identifiant ; il délègue maintenant vers une correspondance
   objectif → aide, avec une action nommée, un exemple résolu et une
   invitation à réessayer. Aucun exemple n'est partagé entre objectifs.
3. **Un problème plus grave a été trouvé et corrigé** : les aides donnaient,
   dans trois cas, la réponse de l'exercice en cours. Une aide qui résout
   l'exercice à la place de l'élève n'est pas une aide.
4. **C'est vérifié en production.** Le message exact du défaut signalé a été
   constaté corrigé par appel HTTP sur Railway, après avoir observé qu'il était
   encore présent 15 s après le push — donc avant que le redéploiement n'ait
   eu lieu.

**Une limite subsiste, qui n'empêche pas de conclure** : le rendu visuel des
messages n'a pas été observé à l'écran, la règle globale interdisant tout
navigateur local. Elle se vérifie en une minute, sur un exercice.

---

*Documents liés : `docs/regles-recommandation-pedagogique.md` (A.3, A.4),
`docs/rapport-final-chantier-7-3.md`, `docs/rapport-final-chantier-7-2.md`.
Fichiers techniques : `relio-backend/src/contenu/aides.ts`,
`relio-backend/test/aides.test.ts`.*