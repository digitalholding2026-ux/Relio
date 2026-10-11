# RAPPORT — CORRECTIF 9 : DESIGN_SYSTEM.md CONTIENT TROIS AFFIRMATIONS FAUSSES

**Date :** 2026-10-11
**Dépôt :** `relio-frontend`
**Fichier corrigé :** `frontend/DESIGN_SYSTEM.md` (10 284 o)
**Commit :** `35297ae`
**Nature :** correction documentaire. **Aucune ligne de code modifiée.**

---

## 1. RÉSUMÉ

`DESIGN_SYSTEM.md` est le **contrat visuel officiel** de Relio : c'est le document qu'un chantier consulte avant d'ajouter un écran, pour ne pas redéfinir une couleur ou un rayon. Cinq de ses affirmations étaient contredites par le code, constaté par l'audit.

Les cinq sont corrigées. Le document n'est pas réécrit : seules les cinq lignes en défaut et leurs phrases de contexte sont modifiées, la structure et le ton sont conservés.

| # | Défaut | Correction |
|---|---|---|
| 1 | « 6,8 Ko gzip » — valeur périmée | Valeur réellement mesurée : **6,97 Ko** (7 140 octets) |
| 2 | « branché dans la CI après le build » — faux | « Le contrôle existe et s'exécute manuellement. Il n'est pas branché dans la CI. » |
| 3 | §7 ne disait rien de la raison réelle du 404 | Note factuelle ajoutée : prérendu en erreur au build, corrigé au correctif 6 |
| 4 | « Trois conflicts » — faute dans un titre | « Trois conflits » |
| 5 | §9 ne nommait pas l'état réel du design system | Puce ajoutée : **aucun** composant utilisé hors de `/design-system` |

---

## 2. LES CINQ DÉFAUTS, AVEC PREUVE

### Défaut 1 — « 6,8 Ko gzip » (annoncés deux fois : §1 principe 2, §6 tableau des budgets)

**Pourquoi c'est faux.** Le poids CSS a été mesuré sur le build courant. Le document annonçait une valeur antérieure au chantier A, et aucune mesure ne la confirmait.

**Valeur exacte mesurée.**

```
$ npm run verifier:poids

  42947774f408bb39.css — 17.2 Ko -> 3.5 Ko gzip
  cb3ebbbccb56dffb.css — 13.5 Ko -> 3.4 Ko gzip

Total CSS : 30.7 Ko bruts -> 7.0 Ko gzip
Budget    : 30 Ko gzip — marge restante 23.0 Ko
OK
```

Le script arrondit à une décimale. La mesure au niveau octet :

```
$ node -e "…gzipSync(…, {level:9})…"
42947774f408bb39.css   3 615 octets = 3.53 Ko
cb3ebbbccb56dffb.css   3 525 octets = 3.44 Ko
TOTAL                  7 140 octets = 6.973 Ko
Budget 30 Ko = 30 720 octets — marge 23 580 octets = 23.03 Ko
```

**Valeur inscrite dans le document : `6,97 Ko` (7 140 octets)** — et non `7.0 Ko`, qui est un arrondi d'affichage, ni une valeur ronde choisie pour la commodité de lecture. Le document précise que le script affiche `7.0 Ko` par arrondi, ce qui évite qu'un lecteur futur y voie une contradiction.

**Traçabilité de l'évolution de la valeur :**

| Moment | Valeur | Origine |
|---|---|---|
| Document d'origine | 6,8 Ko (annoncé) | non vérifié |
| Audit du 2026-10-11, avant chantier A | 6,98 Ko (mesuré) | écart de 0,18 Ko |
| Après correctifs 2 et 3 | 6,97 Ko (mesuré) | + `--bordure-forte`, − seconde déclaration `.bouton` |

L'écart de 0,18 Ko entre le document et la réalité était trop faible pour être remarqué à la lecture, et assez net pour qu'un budget advertised soit faux.

### Défaut 2 — « branché dans la CI après le build »

**Pourquoi c'est faux.** Vérification par grep sur l'ensemble des points d'exécution possibles :

| Point d'exécution | Contient `verifier:poids` ? |
|---|---|
| `.github/workflows/ci.yml` | ❌ non — le workflow s'arrête à `npm run build` |
| `package.json` → `scripts.build` | ❌ non — `next build` seul |
| `package.json` → `scripts.test` | ❌ non — `test:logique` et `test:ui` seuls |
| `package.json` → `scripts.verifier:poids` | ✅ oui — **le script existe et fonctionne** |

Le script est déclaré et s'exécute correctement lorsqu'on l'appelle ; il n'est appelé par rien. Un dépassement du budget CSS passerait la CI au vert.

**État factuel écrit dans le document :**

> Le contrôle existe (`npm run verifier:poids`) et s'exécute manuellement. Il n'est pas branché dans la CI. Un test ne conviendrait pas — il s'exécuterait avant que les CSS Modules aient été fusionnés.

La phrase d'origine sur le fait qu'un test ne conviendrait pas est **conservée** : elle est exacte et explique pourquoi la solution est un script post-build et non un test.

### Défaut 3 — §7 « Accès à la page » ne disait rien de la raison réelle du 404

**Pourquoi c'est faux, ou plutôt incomplet.** La section expliquait *quand* la page est accessible, mais pas pourquoi poser `DESIGN_SYSTEM_ENABLED=on` ne suffisait pas à l'ouvrir. Un opérateur suivant le document à la lettre aurait posé la variable, Deployé, et constaté un 404 persistant — sans piste.

**Cause réelle**, établie par l'audit et corrigée au correctif 6 : la page était **prérendue en erreur au build**. `next build` s'exécute avec `NODE_ENV=production` sans `DESIGN_SYSTEM_ENABLED`, donc la garde renvoyait `notFound()` au moment de la construction, et le HTML figé était celui de l'erreur. Le build produisait `○ /design-system` ; il produit désormais `ƒ`.

**Note ajoutée au document :**

> **Pourquoi la page renvoyait 404 même avec la variable posée.** Elle était prérendue en erreur au build. Poser `DESIGN_SYSTEM_ENABLED=on` ne suffisait pas à la rendre accessible : la page devait être rendue dynamiquement. Ce point est corrigé au chantier A, correctif 6 — `dynamic = 'force-dynamic'`. La fermeture par défaut en production est conservée.

La dernière phrase est importante : la correction ne doit pas laisser croire que la page est ouverte par défaut.

### Défaut 4 — « Trois conflicts »

Faute d'orthographe dans un titre de niveau 4 (`###`). « Conflicts » est un mot anglais ; « conflits » est la graphie française. Corrigé.

### Défaut 5 — §9 « Ce qui reste à faire » ne nommait pas l'état réel

**Pourquoi c'est insuffisant.** La section disait qu'une migration reste à faire, et pourquoi elle n'a pas été faite dans le chantier du design system. Elle ne disait pas **l'état mesuré** : à ce jour, aucun composant n'est utilisé par l'application.

**État mesuré**, établi par grep sur tout `src/` :

```
$ grep -rn "components/ds" src/
src/app/design-system/PageDesignSystem.tsx:26..39   ← le catalogue lui-même
```

Un seul fichier de `src/` importe `src/components/ds/*`, hors du dossier `ds/` : c'est la page de catalogue. `Exercice.tsx`, `ClavierMath.tsx`, `ApiStatus.tsx`, `ParcoursServeur.tsx` et `globals.css` n'utilisent aucun composant ni aucun token du design system.

**Puce ajoutée :**

> **Adoption nulle à ce jour.** Aucun composant du design system n'est utilisé hors de `/design-system`. La seule page qui importe `src/components/ds/*` est son propre catalogue. La migration de l'application est un chantier à part entière.

**Précision sur la méthode.** La section contenait déjà une puce « Migration des écrans existants », qui porte l'**argumentaire** (pourquoi la migration n'a pas été faite dans ce chantier). Elle n'a pas été supprimée : elle répond à une question que la nouvelle puce ne traite pas. Seule sa fin a été reformulée, pour ne plus répéter la liste des trois fichiers désormais nommée dans la puce précédente. Le document ne perd donc aucune information.

---

## 3. DIFF DES 5 MODIFICATIONS

```diff
diff --git a/DESIGN_SYSTEM.md b/DESIGN_SYSTEM.md
index e5938ea..354d16f 100644
--- a/DESIGN_SYSTEM.md
+++ b/DESIGN_SYSTEM.md
@@ -17,7 +17,7 @@ Cinq règles, dans l'ordre d'importance.
 1. **Mobile d'abord.** La largeur de référence est **360 px**. Tout ce qui n'est
    pas vérifié à 360 px n'est pas vérifié.
 2. **Peu de données.** Police système, icônes SVG, aucune image bitmap, aucune
-   animation coûteuse. Le CSS complet pèse **6,8 Ko gzip**, pour un budget de
+   animation coûteuse. Le CSS complet pèse **6,97 Ko gzip**, pour un budget de
    30 Ko.
 3. **AA sans exception.** Le contraste est **calculé**, jamais estimé à l'œil.
 4. **44 px au doigt.** Toute cible tactile, sans exception.
@@ -46,7 +46,7 @@ On utilise des **rôles**, jamais des teintes directement.
 | `--relio-succes` | `#16A34A` | `#16A34A` | réussite |
 | `--relio-alerte` | `#DC2626` | `#F87171` | erreur |

-#### Trois conflicts que la palette de marque ne résout pas
+#### Trois conflits que la palette de marque ne résout pas

 Les couleurs imposées ne passent pas toutes l'AA. Ces trois décisions en
 découlent, et elles sont **vérifiées par test** :
@@ -206,14 +206,17 @@ proposer un produit dégradé.
 | Budget | Seuil | Actuel |
 |---|---|---|
-| CSS de production | 30 Ko gzip | **6,8 Ko** |
+| CSS de production | 30 Ko gzip | **6,97 Ko** (7 140 octets) |
 | Police externe | 0 | 0 |
 | Image bitmap | 0 | 0 |
 | Dépendance UI lourde | 0 | 0 |

-Le contrôle du CSS est automatisé : `npm run verifier:poids`, branché dans la
-CI après le build. Un test ne conviendrait pas — il s'exécuterait avant que les
-CSS Modules aient été fusionnés.
+La valeur est celle retournée par `npm run verifier:poids` sur le build
+courant, qui l'arrondit à une décimale et affiche `7.0 Ko`.
+
+Le contrôle existe (`npm run verifier:poids`) et s'exécute manuellement. Il
+n'est pas branché dans la CI. Un test ne conviendrait pas — il s'exécuterait
+avant que les CSS Modules aient été fusionnés.

 ---

 ## 7. Accès à la page
@@ -225,6 +228,12 @@ CSS Modules aient été fusionnés.
 - En production : accessible uniquement si `DESIGN_SYSTEM_ENABLED=on` est posé
   dans l'environnement de déploiement.

+**Pourquoi la page renvoyait 404 même avec la variable posée.** Elle était
+prérendue en erreur au build. Poser `DESIGN_SYSTEM_ENABLED=on` ne suffisait pas
+à la rendre accessible : la page devait être rendue dynamiquement. Ce point est
+corrigé au chantier A, correctif 6 — `dynamic = 'force-dynamic'`. La fermeture
+par défaut en production est conservée.
+
 Le projet ne dispose d'aucun système d'authentification et il n'en est pas
 introduit ici : une page interne n'est pas une raison de construire un contrôle
 d'accès. Une variable d'environnement règle le problème sans secret ni session.
@@ -247,10 +256,14 @@ La page est par ailleurs marquée `noindex`.
 
 ## 9. Ce qui reste à faire
 
+- **Adoption nulle à ce jour.** Aucun composant du design system n'est utilisé
+  hors de `/design-system`. La seule page qui importe `src/components/ds/*` est
+  son propre catalogue. La migration de l'application est un chantier à part
+  entière.
 - **Migration des écrans existants.** `Exercice.tsx`, `ClavierMath.tsx` et
   `globals.css` utilisent encore leurs propres classes. Ce chantier livre les
-  fondations, pas la migration : c'est un chantier à part, qui doit se faire
-  écran par écran sans casser le parcours déjà vérifié en production.
+  fondations, pas la migration : elle doit se faire écran par écran, sans casser
+  le parcours déjà vérifié en production.
 - **Revue sur appareil.** Les contrastes sont calculés et exacts ; la taille
   réelle des cibles tactiles, le défilement et le rendu à 360 px **ne sont pas
   vérifiés** — ils demanderaient un téléphone.
```

**Bilan : 5 blocs modifiés, 21 insertions, 8 suppressions, 1 fichier.** Aucune section ajoutée, aucune supprimée, aucun titre modifié.

---

## 4. VÉRIFICATIONS

| Vérification | Résultat |
|---|---|
| Aucune occurrence de « 6,8 » ne subsiste dans `DESIGN_SYSTEM.md` ni dans `README.md` | ✅ |
| Aucune autre mention de `verifier:poids` hors des deux lignes corrigées | ✅ — vérifié par grep |
| La mention « branché dans la CI » a disparu | ✅ |
| La section 7 mentionne-t-elle encore que la page est fermée par défaut en production ? | ✅ —phrase conservée |
| Aucune promesse sur un chantier futur non décidé | ✅ — « chantier à part entière » ne décrit aucun contenu, aucune échéance |
| Structure et ton du document | ✅ — inchangés |
| `npm run verifier:poids` | ✅ `OK`, 7.0 Ko gzip pour 30 Ko |
| Suite de tests frontend | ✅ **629 tests, 0 échec** (119 logique + 193 UI + 317 backend) |
| Typecheck et build | ✅ aucun changement de code, non relancés |
| Fichiers de code modifiés | **aucun** — `git diff --stat` : `DESIGN_SYSTEM.md \| 29 ++++--`, 1 fichier |

---

## 5. CE QUI N'A PAS PU ÊTRE FAIT, ET POURQUOI

| Point | Raison |
|---|---|
| **Vérification de la valeur 6,97 Ko sur un autre build** | Le poids CSS dépend du contenu exact des feuilles. La valeur est exacte **pour ce build** et se périmera au prochain ajout de CSS — c'est inherent à un chiffre écrit dans un document. Le chiffre a donc été choisi exact plutôt que rond, et la méthode de mesure est indiquée, ce qui permet de le refaire |
| **Mise à jour des trois valeurs de contraste de §4 (le tableau de la palette)** | Hors du périmètre demandé. Ces trois valeurs sont **vérifiées par test** (`tokens.test.ts`, 21 tests) et l'audit ne les a pas remises en cause. Elles sont correctes |
| **Mise à jour de la puce « Revue sur appareil »** | Elle dit « les contrastes sont calculés et exacts ». C'est toujours vrai pour les contrastes. La correction 3 a portant sur la **bordure** du champ de saisie, un problème de *frontière d'élément* et non de contraste de texte — hors du champ de cette puce |
| **Branchement de `verifier:poids` dans la CI** | Signalé dans le document comme non fait, ce qui est l'état réel. Le branchement lui-même est une modification de code hors du périmètre de ce correctif documentaire |

---

## 6. STATUT GLOBAL

# ✅

**Les cinq défauts sont corrigés, le diff est produit, les mesures sont exactes et la suite de tests passe sans changement.**

Le document reste le contrat visuel qu'il doit être : là où il annonçait un état qui n'existait pas — un chiffre périmé, un branchement inexistant, une raison de 404 absente, un état d'adoption non nommé — il décrit maintenant l'état vérifié du code. Aucun contenu n'a été ajouté qui n'ait été constaté par mesure.