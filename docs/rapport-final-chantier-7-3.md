# Rapport final — Chantier 7.3 : arbitrage pédagogique D5 et fiabilisation de la correction

**Date** : 2026-10-10
**Objet** : appliquer la décision pédagogique D5, confirmée par l'enseignant, dans le moteur de correction
**Statut** : 🟢 **TERMINÉ** — décision implémentée, testée et **vérifiée en production**

> **Convention de lecture**
>
> - ✅ **Vérifié** — contrôlé dans ce chantier, avec une sortie observable.
> - 📋 **Déclaré** — transmis par le responsable de projet, non observé indépendamment.
> - ⏳ **À vérifier** — non testé ici, ou dépendant d'une action du propriétaire.
>
> Contrairement aux chantiers 7, 7.1 et 7.2, celui-ci a fait l'objet d'une
> **vérification en production** : les appels HTTP ci-dessous ont été faits
> contre `relio-backend-production-a2c3.up.railway.app` et
> `relio-frontend-one.vercel.app`, après le push.

---

## 1. État initial de la règle D5

### 1.1 Ce que le moteur faisait avant

Le moteur de correction (`src/contenu/correction.ts`) evaluait **deux axes
seulement** :

| Axe | Champ | État initial |
|---|---|---|
| Exactitude mathématique | `mathemathiquementJuste` | ✅ présent, égalité algébrique exacte |
| Respect de la consigne | `formeRespectee` | ✅ présent, `null` si non arbitrable |
| **Achèvement** | — | ❌ **inexistant** |

Un statut unique (`correcte` / `partielle` / `fausse` / `indeterminee`)
résumait l'ensemble, et le frontend reconstruisait son libellé à partir de ce
statut technique.

### 1.2 Les deux écarts avec la décision D5

✅ **Vérifié par exécution, avant toute modification.**

**Écart 1 — le cas B était impossible à traiter.** L'exemple donné par
l'enseignant, `√(25×2)`, était **refusé par la grammaire** des racines : le
motif n'acceptait qu'un radicand entier simple (`√50`), et supprimait
bêtement les `×`. La réponse était classée « illisible » (422) au lieu d'être
reconnue comme une étape correcte. Le troisième axe demandé n'existait pas, et
le cas B ne pouvait pas exister.

**Écart 2 — le libellé ne distinguait pas les cas A et B.** Une réponse exacte
hors forme demandée et une étape inachevée partageaient le même statut
`partielle` et le même libellé « Ta réponse est juste, mais pas dans la forme
demandée ».

### 1.3 D5 ne contredit pas les règles déjà validées

Point d'audit important, avant d'écrire la moindre ligne : A.3
(`regles-recommandation-pedagogique.md`) définit `partielle` comme « juste mais
pas dans la forme demandée, **ou** étape intermédiaire correcte non achevée ».
La décision D5 **sépare** ces deux cas que A.3 regroupait, mais **conserve
exactement sa garantie** : `partielle` ne compte ni comme juste ni comme fausse.

> La règle A.3 reste donc vérifiée par test (§ 4). D5 **précise** A.3, il ne
> l'annule pas. C'est pourquoi le statut technique est conservé tel quel et que
> `verdict` vient s'y **ajouter** sans le remplacer.

---

## 2. Fichiers modifiés et justification

### 2.1 Backend — `relio-backend`

| Fichier | Modification | Raison |
|---|---|---|
| `src/contenu/correction.ts` | Ajout des axes `achevement` et `verdict`, de `libelle`, de la dérivation du verdict et des messages validés | Cœur de la décision D5 |
| `src/lib/analyseur-reponse.ts` | Racine : radicand décomposable en produit + champ `radicandDecompose` | Rendre le cas B détectable |
| `src/routes/parcours.ts` | `/api/v1/corrections` renvoie `verdict`, `libelle`, `achevement` | Exposer la décision au client |
| `test/decision-d5.test.ts` | **Nouveau** — 17 contrôles | Les 8 cas exigés + invariants |
| `test/correction.test.ts` | 2 assertions obsolètes actualisées | Le marqueur d'arbitrage a disparu |
| `test/parcours.test.ts` | 4 contrôles D5 ajoutés, 1 assertion actualisée | Cohérence API |
| `openapi.yaml`, `docs/CONTRAT-API.md` | Contrat mis à jour (§ 13 créé) | Le changement de contrat doit être écrit |

### 2.2 Frontend — `relio-frontend`

| Fichier | Modification | Raison |
|---|---|---|
| `src/components/Exercice.tsx` | Affiche `libelle` du serveur ; classe CSS pilotée par `verdict` | Les 4 verdicts distincts à l'écran |
| `src/lib/parcours.ts` | Type `Verdict`, champs `libelle` et `achevement` | Contrat client |
| `src/app/globals.css` | Classes de verdict alignées sur D5 | Distinction visuelle |

### 2.3 Le point de conception qui a nécessité un arbitrage

Les structures existantes ne permettaient de représenter que **deux** axes. La
troisième dimension demandée — l'achèvement — n'avait aucun équivalent. La
modification minimale retenue est la suivante :

- un champ `achevement` (`acheve` / `inacheve` / `null`) sur la correction ;
- la seule trace observable d'un travail inachevé, dans le MVP, est le
  **radicand décomposé en produit** : `radicandDecompose` dans
  `ValeurRacine`.

**`achevement` vaut `null` partout ailleurs.** Le moteur ne prétend jamais
savoir qu'un développement est « fini » : il ne le sait pas, et le dit. C'est
ce `null` qui produit le verdict `a_determiner` quand une forme était exigée
mais non arbitrable.

### 2.4 Ce qui n'a **pas** été modifié

| Élément | État |
|---|---|
| Exercices, énoncés, réponses attendues | ✅ **Intacts** — aucun fichier de `contenu/exercices.ts` touché |
| Bloc, semaines d'ouverture, calendrier | ✅ Intacts |
| `progression.ts`, vocabulaire `STATUTS_REPONSE` | ✅ Intacts |
| Clavier mathématique | ✅ **Non développé**, hors périmètre |
| Frontend côté navigation, `API_BASE_URL`, CORS | ✅ Intacts |

---

## 3. Verdicts et messages appliqués

### 3.1 Les quatre verdicts

✅ **Vérifié en production**, sur les deux services.

| Cas | Verdict | Condition | Statut technique |
|---|---|---|---|
| **D** | `correct` | juste, achevé, conforme | `correcte` |
| **B** | `partiellement_correct` | juste **et** inachevé | `partielle` |
| **A** | `resultat_juste_consigne_non_respectee` | juste **et** forme non respectée | `partielle` |
| **C** | `incorrect` | mathématiquement faux | `fausse` |
| — | `a_determiner` | le moteur ne peut pas conclure | `indeterminee` |

**Règle cardinale** : une réponse mathématiquement juste n'est **jamais**
`incorrect`, quelle que soit son écriture.

### 3.2 Les messages, relevés sur la production

| Cas | Exercice | Réponse | Libellé retourné par l'API |
|---|---|---|---|
| D | `MVP-B1-E4` | `(2x-3)(2x+3)` | « Ta réponse est juste. » |
| A | `MVP-B1-E4` | `4x^2 - 9` | « Ton résultat est mathématiquement juste, mais tu n'as pas respecté la forme demandée. Écris ta réponse sous la forme d'un produit de facteurs du premier degré. » |
| B | `MVP-B2-E1` | `√(25×2)` | « Ta réponse est partiellement correcte : tu as bien commencé le travail, mais il reste une étape pour le terminer. Continue jusqu'à obtenir une réponse qui ne peut plus être simplifiée. » |
| C | `MVP-B2-E1` | `7√2` | « Ce n'est pas encore juste. » |

Le libellé **vient du serveur** et n'est pas reformulé par le frontend : il ne
peut donc pas diverger de la règle appliquée. Les textes sont ceux validés par
l'enseignant, avec le nom de la forme attendue inséré (« produit de facteurs du
premier degré », « fraction irréductible », « a√b… ») pour que l'élève sache
précisément quoi écrire.

### 3.3 Un choix de couleur qui est un choix pédagogique

`partiellement_correct` et `resultat_juste_consigne_non_respectee` partagent
**volontairement** la même couleur (ambre). Tous deux signifient « tu n'as pas
faux, mais ce n'est pas fini ». Les traiter en rouge reviendrait à dire à
l'élève qu'il s'est trompé — ce qui est faux dans les deux cas.

Ce qui les distingue à l'écran est le **libellé**, pas la couleur.

---

## 4. Tests ajoutés et résultats

### 4.1 Résultats réels

| Dépôt | Tests | Suites | Échecs |
|---|---|---|---|
| `relio-backend` | ✅ **182 / 182** | 38 | 0 |
| `relio-frontend` | ✅ **42 / 42** | 8 | 0 |

Progression : **197 → 224 tests** (+27, dont 21 backend et 6 contrôles D5 dans
les suites existantes).

| Vérification | Résultat |
|---|---|
| `npm run typecheck` (backend, frontend) | ✅ aucune erreur |
| `npm run build` (backend, frontend) | ✅ |
| `openapi.yaml` | ✅ YAML valide, 7 chemins, enums vérifiés |

### 4.2 Les 8 cas exigés

| # | Cas exigé | Test | Résultat |
|---|---|---|---|
| 1 | Correcte et conforme | `cas D : réponse entièrement correcte` | ✅ 3 exercices |
| 2 | Juste mais forme non respectée | `cas A : résultat juste, consigne non respectée` | ✅ factorisation, fraction, racine |
| 3 | Intermédiaire correcte mais incomplète | `cas B : réponse partiellement correcte` | ✅ 3 écritures équivalentes |
| 4 | Mathématiquement incorrecte | `cas C : réponse incorrecte` | ✅ 4 exercices |
| 5 | Équivalente sous une autre écriture | `équivalences algébriques` | ✅ + **anti-faux-positif** sur la forme |
| 6 | Forme / achèvement indéterminable | `prudence : ce que le moteur ne peut pas déterminer` | ✅ 3 tests |
| 7 | Cohérence backend / API / frontend | `décision D5 — cohérence du verdict renvoyé par l'API` | ✅ 4 contrôles |
| 8 | Non-régression corrections et indices | `préserve les indices` + suite existante | ✅ |

Les exercices réels du MVP sont utilisés partout : `4x² − 9` (factorisation),
`√50` (racines), `24/36` (fractions), `2x + 1` (développement).

### 4.3 L'anti-faux-positif exigé

> « Ne crée pas de faux positifs en acceptant systématiquement toute réponse
> équivalente : la forme demandée doit toujours être évaluée séparément. »

Le test `évalue toujours la forme séparément de la valeur` le vérifie
explicitement sur le **même exercice** :

| Réponse | Valeur exacte | Forme | Verdict |
|---|---|---|---|
| `(2x+3)(2x-3)` | ✅ | ✅ | `correct` |
| `4x^2 - 9` | ✅ | ❌ | `resultat_juste_consigne_non_respectee` |

Deux écritures de la même valeur, deux verdicts. C'est exactement ce que la
consigne demande.

### 4.4 Les tests peuvent-ils échouer ?

✅ **Vérifié** — chaque contrôle a été déclenché volontairement.

| Mutation | Tests en échec |
|---|---|
| Cas B traité comme un simple cas de forme | **6** |
| Réponse exacte déclarée `incorrect` | **15** |
| Libellé du cas A amputé de « mathématiquement juste » | **4** |

Le troisième cas est particulièrement important : il prouve que le **texte vu
par l'élève** est bien vérifié, et pas seulement le mot-clé du statut.

### 4.5 Non-régression complète

✅ **Vérifié**, sur le serveur compilé :

| Contrôle | Résultat |
|---|---|
| Les 12 exercices sur leur réponse attendue | **12 / 12** restent `correct` |
| Indices servis (12 exercices × 3 paliers) | **36 / 36** |
| Bloc fermé : correction d'un exercice de B3 en semaine 1 | **403** |
| Calendrier | `2026-09-07`, semaine 1 → seul B1 ouvert |
| Aucune réponse attendue dans le libellé | ✅ contrôlé sur les 4 verdicts |

### 4.6 Trois erreurs de mes propres tests, corrigées

Elles sont ici parce qu'elles sont instructives, et parce qu'un rapport qui
les cacherait donnerait une assurance fausse :

1. **`2x` ≠ `2x + 1`.** J'avais écrit que `2x` était la bonne réponse de
   `MVP-B1-E1`, dont l'attendu est `2x + 1`. Le test échouait à juste titre.
2. **`10√2` n'est pas équivalent à `5√2`.** `10√2 = 2 × 5√2`. Je l'avais
   listé comme équivalence ; c'est une réponse fausse, et le moteur le dit
   correctement. Le test le vérifie désormais comme cas C.
3. **Une attente de semaine fausse** sur la date de septembre.

Aucune n'a été « corrigée » en affaiblissant une assertion.

---

## 5. Commits et état du push

| Dépôt | SHA | Objet |
|---|---|---|
| `relio-backend` | **`728a5fd`** | `feat(correction): arbitrage pédagogique D5 par l'enseignant` |
| `relio-frontend` | **`bfaef2b`** | `feat(exercice): afficher les quatre verdicts de la décision D5` |

✅ **Vérifié** — SHA distants relus après envoi, identiques aux SHA locaux.
Branche `main`, deux dépôts.

---

## 6. Déploiement — ce qui a réellement été vérifié

✅ **Vérifié en production**, après le push.

### 6.1 Backend — Railway

```
GET  /health       → 200, {"status":"ok","environment":"production"}
GET  /api/v1       → status: mvp-pedagogique, 7 routes
GET  /api/v1/parcours → anneeScolaire.debut = "2026-09-07"
POST /api/v1/corrections → verdict + libelle présents
```

| Contrôle | Résultat observé |
|---|---|
| `/health` répond `ok`, `environment: production` | ✅ |
| Le champ `verdict` existe (absent avant ce chantier) | ✅ `resultat_juste_consigne_non_respectee` |
| Le champ `libelle` existe | ✅ présent sur les 4 cas |
| Le champ `achevement` existe | ✅ `inacheve` sur `√(25×2)` |
| Cas B détecté en production | ✅ `partiellement_correct` |
| `anneeScolaire.debut` = `2026-09-07` (chantier 7.2) | ✅ |
| Bloc B3 fermé hors semaine 10 | ✅ 0 exercice transmis |

**La décision D5 est donc déployée et fonctionnelle.** Railway a redéployé
automatiquement après le push.

### 6.2 Frontend — Vercel

```
GET /                     → 200, bouton « Voir le parcours », href="/parcours"
GET /parcours              → 200, 9 liens d'exercices (B1, B2), 0 pour B3
GET /parcours/MVP-B1-E4    → 200
```

| Contrôle | Résultat observé |
|---|---|
| Page d'accueil 200 + bouton présent | ✅ |
| `/parcours` 200 **avec** liens d'exercices | ✅ 9 liens |
| Page ne affiche pas « Exercices indisponibles » | ✅ absent |
| Bloc fermé signalé et sans exercice | ✅ « Disponible à partir de la semaine 10. » |
| CORS autorise `relio-frontend-one.vercel.app` | ✅ préflight 204 + `access-control-allow-origin` sur l'appel réel |

### 6.3 Ce qui n'a **pas** été vérifié

⏳ **Non testé :**

- **le rendu visuel des quatre verdicts à l'écran.** Les réponses de l'API sont
  confirmées, et le frontend affiche `libelle` tel quel — mais je n'ai pas
  observé le verdict peint dans un navigateur en production, la règle globale
  interdisant désormais tout navigateur local ;
- **la saisie au doigt sur un téléphone réel** (hypothèse H1) ;
- **l'état de la CI** sur GitHub — `gh` est absent de l'environnement.

Ces trois points restent ouverts et sont listés au § 8.

---

## 7. Décisions supplémentaires nécessaires

Aucune pour ce chantier : D5 était la décision attendue, et elle est
appliquée. Deux points neighbour restent ouverts, sans être bloquants.

| # | Point | Effet |
|---|---|---|
| 1 | **Détection de l'achèvement hors racines.** Seul un radicand décomposé est reconnu comme inachevé. Un développement inachevé (`2(x + 1/2)`) serait classé `correct` si la valeur est juste. | Le moteur ne prétend pas savoir : c'est un choix de prudence assumé. L'enseignant peut décider d'élargir. |
| 2 | **Message du cas B légèrement générique** — il ne nomme pas l'étape exacte pour chaque exercice. | Acceptable pour le MVP ; personnalisable plus tard si l'enseignant le souhaite. |

---

## 8. Réserves restantes

| # | Réserve | État |
|---|---|---|
| R1 | **Rendu visuel des verdicts non observé en production.** | Le plus important. Les textes API sont confirmés ; leur affichage ne l'est pas. |
| R2 | **Hypothèse H1** — saisie algébrique au doigt sur téléphone réel, jamais testée. | Inchangée depuis le chantier 6. |
| R3 | **Visibilité du dépôt GitHub** — contenus officiels du BEPC versionnés. | Inchangée. Juridique. |
| R4 | **État de la CI** — non observable sans `gh`. | Inchangée. |
| R5 | **Cases A/B au-delà du MVP** — le cas A n'est détecté que sur les 12 exercices existants. | Normal : le contenu est borné au MVP. |

**R1 et R2 sont les deux seules qui concernent l'expérience élève**, et R1
tient en une vérification manuelle : ouvrir un exercice sur le site, saisir
`4x^2 − 9` puis `√(25×2)`, et regarder le libellé s'afficher.

---

## 9. Statut du chantier

# 🟢 TERMINÉ

**La décision pédagogique D5 est implémentée par le moteur, pas seulement
documentée.**

Le chantier est terminé parce que les quatre conditions sont réunies :

1. **La règle est appliquée par le moteur.** Un quatrième axe (`achevement`) a
   été ajouté, l'exemple du cas B (`√(25×2)`) que la grammaire refusait
   auparavant est désormais reconnu, et les quatre verdicts sont dérivés des
   axes — jamais d'une comparaison de chaînes.
2. **Les tests pertinents passent.** 224 tests au total, 182 backend et 42
   frontend, zéro échec. Les 8 cas exigés sont couverts sur les exercices réels
   du MVP, avec l'anti-faux-positif sur la forme demandé, et chaque contrôle a
   été déclenché volontairement pour prouver qu'il mord.
3. **Les limites sont documentées.** Le cas B n'est détectable que sur un
   radicand décomposé ; ailleurs `achevement` vaut `null` et le moteur ne
   prétend pas savoir. Aucune notation ni barème n'a été inventé.
4. **C'est vérifié en production.** Les quatre verdicts, leurs libellés et le
   champ `achevement` sont constatés par appels HTTP sur Railway ; le
   frontend et le CORS sont constatés sur Vercel.

**Une réserve subsiste, qui n'empêche pas de conclure** : le rendu visuel des
verdicts n'a pas été observé à l'écran, et l'hypothèse H1 reste non testée.
Aucune des deux ne porte sur la correction elle-même — l'une relève de
l'affichage d'une donnée déjà vérifiée, l'autre d'un chantier à part.

---

*Documents liés : `docs/regles-recommandation-pedagogique.md` (A.3),
`docs/specification-diagnostic-initial.md`, `docs/rapport-final-chantier-7.md`,
`docs/rapport-final-chantier-7-2.md`.
Contrats : `relio-backend/openapi.yaml`, `relio-backend/docs/CONTRAT-API.md` § 13.*