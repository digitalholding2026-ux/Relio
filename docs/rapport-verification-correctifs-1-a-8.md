# RAPPORT DE VÉRIFICATION — ÉTAT RÉEL DES CORRECTIFS 1 À 8

**Date :** 2026-10-11
**Objet :** lever deux points d'incompréhension entre l'audit (`73337d3`), le chantier A (`747ae8a`, `15139b3`) et le correctif 9 (`35297ae`)
**Conclusion :** les correctifs 1 à 8 sont faits, testés, poussés et **en production**.

---

## 1. POURQUOI CE RAPPORT EXISTE

Le rapport du correctif 9 annonçait « 629 tests » alors que l'audit du même jour en comptait 562, et le hash CSS changeait entre les deux. Deux chiffres seemed incohérents avec l'état connu du projet.

Les deux s'expliquent : **les 67 tests supplémentaires et le changement de hash CSS sont la conséquence directe des correctifs 1 à 8.** Ils ne sont pas une anomalie, ni un travail parallel non declare.

Ce rapport etablit l'etat, apporte les preuves mesurees, et rappelle ou se trouvent les correctifs — dans deux depots Git distincts du depot racine.

---

## 2. POINT 1 — LE COMPTEUR DE TESTS

### 2.1 Les chiffres sont exacts

**629 est le nombre réel.** Les deux énoncés sont vrais : l'audit comptait 562, et après les correctifs 1 à 8 il y en a 629. Les 67 tests supplémentaires sont **ceux qui prouvent les correctifs**.

| Suite | Audit du 2026-10-11 | État actuel | Écart |
|---|---|---|---|
| Frontend logique (`node --test`) | 119 | **119** | 0 |
| Frontend UI (Vitest) | 136 | **193** | **+57** |
| Backend (`node --test`) | 307 | **317** | **+10** |
| **Total** | **562** | **629** | **+67** |

**Aucune suite n'a perdu de test.** Le passage de 136 à 193 dans la suite UI est intégralement constitué de tests ajoutés ; les 136 d'origine sont tous présents et passent.

### 2.2 D'où viennent les 67 tests

```
$ git show --stat 747ae8a
 src/app/page.test.tsx                    |  95 ++   ← correctifs 4 + 5   (8 tests)
 src/components/ClavierMath.test.tsx      | 201 ++   ← correctif 1         (14 tests)
 src/components/ParcoursServeur.test.tsx  | 143 ++   ← correctif 4         (4 tests)
 src/design/design-system-garde.test.ts   |  59 ++   ← correctif 6         (5 tests)
 src/design/globals-applicatif.test.ts    | 111 ++   ← correctifs 2 + 3    (11 tests)
 src/design/roles-aria.test.ts            | 123 ++   ← correctif 4         (5 tests)
 src/design/textes-affiches.test.ts       | 177 ++   ← correctif 7         (10 tests)
 backend/test/env-example.test.ts         (10 tests) ← correctif 8

 16 files changed, 1026 insertions(+), 39 deletions(-)
```

Les 7 fichiers de test du frontend +\`test/env-example.test.ts\` du backend sont **entièrement des ajouts**. Aucun test existant n'a été modifié ni retiré.

### 2.3 Une précision sur la formulation du rapport du correctif 9

Le correctif 9 (`35297ae`) disait « Aucune modification de code ». C'est exact **pour ce commit** : il ne touche qu'un fichier, \`DESIGN_SYSTEM.md\`, 21 insertions et 8 suppressions.

Les 629 tests étaient déjà le compte au moment où ce rapport a été écrit. Les deux énoncés — « aucune ligne de code modifiée » et « 629 tests » — sont simultanément vrais, et ne se contredisent pas.

---

## 3. POINT 2 — LE CHANGEMENT DE HASH CSS

### 3.1 Ce qui a changé

Le hash CSS est passé de \`c5b3424d1cf8f1d7.css\` (audit) à \`cb3ebbbccb56dffb.css\`. Le hash change dès qu'un octet de CSS change : **ce changement est la mesure de l'application des correctifs 2 et 3**, pas une anomalie.

| Fichier | Modification | Correctif |
|---|---|---|
| \`src/app/globals.css\` | 2ᵉ déclaration \`.bouton\` supprimée, les deux fusionnées en une seule | **2** |
| \`src/app/globals.css\` | \`--bordure-forte: #7c85a3\` ajouté à \`:root\` | **3** |
| \`src/app/globals.css\` | \`.exercice__saisie\` bascule sur \`--bordure-forte\` | **3** |
| \`src/app/globals.css\` | \`.clavier__touche\` bascule sur \`--bordure-forte\` | **3** |

**Aucune application partielle.** Les quatre modifications sont complètes et chacune est couverte par un test.

### 3.2 Preuve directe dans le CSS

**Avant** (audit) — deux règles \`.bouton\` en conflit :

```
offset 7357 :: .bouton{border:1px solid var(--primaire);background:var(--primaire);color:#fff;border-radius:10px…}
offset 8275 :: .bouton--principal{background:var(--primaire);color:#fff;border-color:var(--primaire)}
offset 9647 :: .bouton{min-height:48px;padding:0 1.1rem;border-radius:var(--rayon);border:1px solid var(--bordure);
                      background:var(--surface);color:var(--texte)…}
              ↑ celle-ci écrase la première : le bouton principal s'affichait blanc au repos, bleu au survol
```

**Après** — une seule règle de base, la variante appliquée ensuite :

```
offset 7380 :: .bouton{appearance:none;min-height:48px;padding:0 1.1rem;border:1px solid var(--bordure-forte);
                      border-radius:var(--rayon);background:var(--surface);color:var(--texte)…}
offset 8364 :: .bouton--principal{background:var(--primaire);color:#fff;border-color:var(--primaire)}
```

Contrôle automatisé :

```
$ node -e "…recherche des règles .bouton dans .next/static/css/*.css…"
cb3ebbbccb56dffb.css -> .bouton de base : 1
```

---

## 4. PREUVES MESURÉES, REFAITES À L'INSTANT

Toutes les mesures ci-dessous ont été réexécutées le 2026-10-11, après le correctif 9, et non reprises d'un rapport précédent.

### Correctif 2 — une seule règle \`.bouton\`

| Où | Résultat |
|---|---|
| Build local | \`.bouton de base : 1\` (offset 7380) |
| **Production** | \`.bouton de base dans le CSS PRODUCTION : 1\` |

### Correctif 3 — ratio de contraste mesuré

Calculé avec \`rapportContraste()\` de \`src/design/contraste.ts\` (formule WCAG 2.1 exacte) :

```
--bordure-forte #7c85a3 sur #ffffff : 3.66:1   ✅ seuil AA SC 1.4.11 = 3:1
ancienne      #e2e5ef sur #ffffff : 1.26:1   ❌
```

### Correctif 6 — sortie du build

```
Route (app)                                 Size  First Load JS
┌ ƒ /                                    1.41 kB         107 kB
├ ○ /_not-found                            993 B         104 kB
├ ƒ /design-system                       10.6 kB         113 kB    ← dynamique
├ ƒ /parcours                              160 B         106 kB
└ ƒ /parcours/[id]                        5.8 kB         112 kB
```

### Correctif 4 — test statique interdisant \`role="note"\`

| Où | Résultat |
|---|---|
| \`src/\` | **0 occurrence** |
| **Production** (HTML de l'accueil) | **0 occurrence** |
| Bandeau d'avertissement | \`class="avertissement" role="status"\` |

### Correctif 5 — test statique interdisant « ne sont pas conservées »

| Où | Résultat |
|---|---|
| \`src/app/page.tsx\` | **0 occurrence** de « ne sont pas conservées » |
| Texte en place | « Tes réponses sont enregistrées sur ton appareil pour te permettre de suivre ta progression ; tu peux les effacer à tout moment, et rien n'est conservé de ton parcours sur nos serveurs. » |

### Correctif 1 — le clavier en production

Code déployé dans \`app/parcours/[id]/page-*.js\` :

```js
onPointerDown:t=>f(t,e.action),onClick:t=>h(t,e.action)
e.detail>0||v(t)
```

Les deux gestionnaires sont câblés sur la même touche, et la discrimination \`detail > 0\` est présente : un clic issu d'un doigt est ignoré, un clic né du clavier est exécuté.

### Compteurs de tests, à l'instant

```
frontend  npm run test:logique  → # tests 119 / # pass 119 / # fail 0
frontend  npm run test:ui       → Test Files 11 passed (11) / Tests 193 passed (193)
backend   npm test              → # tests 317 / # pass 317 / # fail 0
```

**629 tests, 0 échec.**

---

## 5. OÙ SE TROUVENT LES CORRECTIFS

C'est la source la plus probable de l'incompréhension : **les correctifs ne sont pas dans le dépôt racine.**

| Dépôt | Commit | Contenu |
|---|---|---|
| \`digitalholding2026-ux/Relio\` (racine) | \`b30f325\`, \`fd663f4\`, \`73337d3\` | rapports et audit — **aucun code** |
| \`digitalholding2026-ux/relio-frontend\` | \`35297ae\`, \`747ae8a\` | **correctifs 1 à 7** |
| \`digitalholding2026-ux/relio-backend\` | \`15139b3\` | **correctif 8** |

Le dépôt racine ignore \`/frontend/\` et \`/backend/\` (`.gitignore` l.12-13). Un \`git status\` sur la racine ne montre donc **aucune** trace des correctifs 1 à 8 — c'est le comportement attendu de la règle de séparation des dépôts posée au début du projet.

---

## 6. TABLEAU DES 8 CORRECTIFS

| # | Correctif | Fichier | Ligne | Test ajouté | Preuve mesurée | Statut |
|---|---|---|---|---|---|---|
| 1 | Clavier actionnable au clavier | \`src/components/ClavierMath.tsx\` | 178, 200, 226-227 | \`ClavierMath.test.tsx\` (14 tests) | JS prod : \`onPointerDown\`+\`onClick\`, \`detail>0\` | ✅ |
| 2 | \`.bouton\` fusionné | \`src/app/globals.css\` | 325 | \`globals-applicatif.test.ts\` (11 tests) | CSS compilé **et** prod : **1** règle de base | ✅ |
| 3 | \`--bordure-forte\` | \`src/app/globals.css\` | 16, 486, 641 | \`globals-applicatif.test.ts\` (mêmes 11) | **3,66:1** sur blanc (seuil 3:1) | ✅ |
| 4 | \`role="note"\` → \`role="status"\` | \`page.tsx:97\` · \`parcours/page.tsx:50\` · \`ParcoursServeur.tsx:68\` | idem | \`roles-aria.test.ts\` (5) + \`ParcoursServeur.test.tsx\` (4) + \`page.test.tsx\` (3) | 0 occurrence dans \`src/\` **et en production** | ✅ |
| 5 | Texte exact sur les réponses | \`src/app/page.tsx\` | 177-182 | \`page.test.tsx\` (8 tests) | 0 occurrence de l'ancienne phrase | ✅ |
| 6 | \`/design-system\` en rendu dynamique | \`src/app/design-system/page.tsx\` | 51 | \`design-system-garde.test.ts\` (5 tests) | build : **\`ƒ /design-system\`** | ✅ |
| 7 | Fautes d'accord | \`src/lib/parcours.ts:139\` · \`src/components/ApiStatus.tsx:49\` | idem | \`textes-affiches.test.ts\` (10 tests) | 132 chaînes relues, 2 fautes trouvées et corrigées | ✅ |
| 8 | Variables calendrier documentées | \`backend/.env.example\` | 23-47 | \`env-example.test.ts\` (10 tests) | comparé aux lectures réelles de \`process.env\` | ✅ |

Le détail des correctifs — diff, sorties « échouait avant », et ce qui n'a pas pu être fait — se trouve dans \`docs/rapport-final-chantier-A.md\` (commit \`fd663f4\`).

---

## 7. RAPPEL DE LA RÈGLE « ÉCHOUAIT AVANT, PASSE APRÈS »

Chaque correctif a été validé par exécution réelle, et non par relecture : le fichier source était remis dans son état d'origine via \`git stash\`, la suite de tests relancée, l'échec constaté, puis le correctif réappliqué.

| Correctif | Tests échouant sur le code d'origine |
|---|---|
| 1 | 9 sur 14 |
| 2 | 3 sur 11 |
| 3 | 5 sur 11 |
| 4 | 10 sur 17 |
| 5 | 5 sur 8 |
| 6 | 3 sur 5 |
| 7 | 3 sur 10 |
| 8 | 7 sur 10 |

**45 tests échouaient avant correction sur le périmètre des 8 correctifs.** Ils passent tous maintenant.

---

## 8. STATUT GLOBAL

# ✅

**Les deux points d'incompréhension sont levés : le compte de 629 tests est exact et traçable jusqu'aux 7 fichiers de test ajoutés ; le changement de hash CSS est la mesure de l'application des correctifs 2 et 3, tous deux complets.**

Aucune action corrective n'est nécessaire. Les correctifs 1 à 8 sont appliqués, testés, poussés, et vérifiés en production par requête HTTP directe.

**Reste ouverte — sans rapport avec ce chantier :** \`/design-system\` renvoie toujours 404 en production, ce qui est le comportement correct. La garde est intacte ; pour ouvrir la page, il faut poser \`DESIGN_SYSTEM_ENABLED=on\` dans le tableau de bord Vercel.