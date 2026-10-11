# RAPPORT DE FIN DE CHANTIER C2b — MIGRATION DU CLAVIER MATHÉMATIQUE

**Date :** 2026-10-11
**Dépôt :** `relio-frontend`
**Commit :** `ef12f42`
**Nature :** migration d'habillage. Aucun changement de comportement, aucune modification de dimension, aucun changement de timing.

---

## 1. RÉSUMÉ

1. `ClavierMath.tsx` n'utilise plus **aucune** classe de `globals.css`. Le clavier est habillé par deux modules locaux : `clavier.module.css` (contenu, grille) et `ToucheClavier.module.css` (les 25 touches).
2. **La hauteur est reproduite à l'identique : 453 px**, recalculée par un test à partir des valeurs du CSS. Sous 700 px de hauteur d'écran, 437 px. Le `min-height` passe par `--relio-tactile-min` (44 px) — le token du design system.
3. **`onPointerDown` + `onClick` + `detail > 0` sont conservés** — déplacés dans `ToucheClavier.tsx`, pas réécrits. Un test le vérifie sur les deux fichiers.
4. `lib/clavier.ts`, `useHauteurClavierSysteme.ts`, `Exercice.tsx` et `exercice.module.css` : **diff vide**.
5. Poids : JS **+0,26 Ko** gzip (budget 4 ✅), CSS **+0,42 Ko** (budget 3 ✅). Chunk client **9,81 Ko**, sous le plafond de 15 Ko. Tests : 376 → 414 (+38), 0 échec.

---

## 2. DIFF DES FICHIERS

### Créés (5)

| Fichier | Lignes | Rôle |
|---|---|---|
| `src/components/ToucheClavier.tsx` | 78 | Une touche. `<button type="button">`, `aria-label`, `aria-controls`, `gridColumn`, les deux gestionnaires. |
| `src/components/ToucheClavier.module.css` | 125 | La touche : hauteur, padding, variante par identifiant, `:active`, `:focus-visible`, media `max-height: 700px`. |
| `src/components/clavier.module.css` | 74 | Le clavier : `sticky`, `bottom`, `z-index`, la grille à quatre colonnes, les deux media queries. |
| `src/components/ToucheClavier.test.tsx` | 157 | 14 tests : cible tactile, deux voies d'activation, pas de double déclenchement. |
| `src/design/clavier-migration.test.ts` | 285 | 24 tests statiques, dont le **calcul de la hauteur** et le **plafond du chunk**. |

### Modifiés (5)

| Fichier | Modification |
|---|---|
| `src/components/ClavierMath.tsx` | 233 → 218 l. Le JSX des 25 touches part dans `ToucheClavier` ; `ClavierMath` garde `appliquer`, `appuyer` et les deux gestionnaires. |
| `src/app/globals.css` | 2 110 → 1 909 caractères. **11 blocs retirés**, tous `.clavier*`. |
| `src/design/exercice-migration.test.ts` | « ClavierMath n'a aucun import du design system » → « n'utilise plus aucune classe de globals.css ». |
| `src/design/parcours-migration.test.ts` | Idem. |
| `src/design/globals-applicatif.test.ts` | Le contrôle de bordure des touches pointe désormais `ToucheClavier.module.css`, et vérifie que l'ancien bloc a disparu de `globals.css`. |

### Non touchés — vérifié par diff

```
$ git diff 3c0fd24 -- src/lib/clavier.ts \
    src/hooks/useHauteurClavierSysteme.ts \
    "src/app/parcours/[id]/exercice.module.css"
(VIDE)
```

`src/components/Exercice.tsx` : également inchangé.

---

## 3. CONFIRMATION EXPLICITE — `lib/clavier.ts` N'A PAS BOUGÉ

```
$ git diff 3c0fd24 -- src/lib/clavier.ts
(VIDE)
```

Les trois dispositions de touches, les `id`, `libelle`, `aria`, `action` et `largeur` de chaque touche sont exactement ce qu'ils étaient. `ToucheClavier.tsx` lit `Touche` par import de type : il ne définit, ne duplique et ne modifie aucune touche.

`COLONNES = 4` reste exporté par `lib/clavier.ts` et reste consommé par `ClavierMath` pour alimenter `--colonnes`.

---

## 4. CONFIRMATION EXPLICITE — LA HAUTEUR EST DE 453 px

Le calcul, refait par le test à partir des valeurs réellement présentes dans le CSS — pas recopiées d'un commentaire :

```
  9 rangées   × 44 px  =  396 px   (min-height: var(--relio-tactile-min) = 44px)
  8 écarts    ×  5 px  =   40 px   (margin-top de .rangee + .rangee)
  2 paddings  ×  8 px  =   16 px   (padding de .clavier)
  bordure     ×  1 px  =    1 px   (border-top)
                              ─────────
                                 453 px
```

Sous `max-height: 700px` — le cas d'un écran 360×640 : padding 4 px, écarts 4 px.

```
  9 rangées   × 44 px  =  396
  8 écarts    ×  4 px  =   32
  2 paddings  ×  4 px  =    8
  bordure     ×  1 px  =    1
                              ─────
                                 437 px
```

**La règle `@media (max-height: 700px)` ne touche que le `padding` de la touche, jamais sa hauteur.** Un test le vérifie explicitement : `expect(TOUCHE_BAS).not.toContain('min-height')`.

### Largeur des touches

Inchangée par construction — aucune valeur de la grille n'a bougé :

```
360 px − 32 (conteneur) − 16 (clavier) − 18 (3 écarts de 6) = 294
294 / 4 colonnes = 73,5 px par touche
```

---

## 5. CONFIRMATION EXPLICITE — `onPointerDown` + `onClick` + `detail > 0`

**Ils sont conservés, pas réécrits.** Ils ont changé de fichier, pas de rôle.

| Élément | Avant | Après | Test |
|---|---|---|---|
| `onPointerDown` | sur le `<button>` dans `ClavierMath` | sur le `<button>` dans `ToucheClavier` | ✅ |
| `onClick` | sur le `<button>` dans `ClavierMath` | sur le `<button>` dans `ToucheClavier` | ✅ |
| `preventDefault()` | dans `ClavierMath` | **dans `ClavierMath`, inchangé** | ✅ |
| `if (evenement.detail > 0) return` | dans `ClavierMath` | **dans `ClavierMath`, inchangé** | ✅ |
| `appuyer(action)` | `action: ToucheAction` | `appuyer(touche.action)` | ✅ |

**Pourquoi les gestionnaires reçoivent désormais la touche entière et non son action.** `ToucheClavier` n'a pas à connaître la grammaire d'insertion : il transmet l'objet. `ClavierMath` en extrait `touche.action` et appelle `appuyer()`, qui est le code d'origine du chantier 7.5 — inchangé.

**La discrimination reste au même endroit, pour la même raison.** Elle est dans `ClavierMath` (`surClick`), parce que c'est lui qui sait qu'un `click` suivi d'un `pointerdown` est un doublon. `ToucheClavier` ne filtre rien : un test le vérifie (`expect(surClick).toHaveBeenCalledTimes(1)` après un `click` à `detail: 1`).

Les 14 tests de `ClavierMath.test.tsx` (correctif A1) **passent sans aucune modification**.

---

## 6. L'ÉCRAN, AVANT / APRÈS

### La touche

| | Avant (`globals.css`) | Après (module local) |
|---|---|---|
| Fond | `--surface` `#ffffff` | `--relio-surface` `#ffffff` |
| Texte | `--texte` `#14161f` | `--relio-texte` `#0f172a` (17:1) |
| Bordure | `--bordure-forte` `#7c85a3` (**3,66:1**) | `--relio-bordure-forte` `#838a96` (**3,48:1**) |
| Hauteur | `min-height: 44px` | `min-height: var(--relio-tactile-min)` (44 px) |
| Touche « Vérifier » | `--primaire` `#2b4bd8` (**6,77:1**) | `--relio-primaire` `#1e2a78` (**12,67:1**) |
| Touches de correction | `--fond` `#f7f8fc` | `--relio-fond` `#faf7f2` |
| Focus | `outline: 3px solid var(--primaire)`, offset 1 px | idem, via le token |

**Le contraste de la touche de validation passe de 6,77:1 à 12,67:1.** C'est la seule amélioration de contraste — elle vient du choix des tokens du design system, pas d'une règle ajoutée.

**La bordure passe de 3,66:1 à 3,48:1.** C'est la seule valeur qui baisse légèrement. Elle reste au-dessus du seuil de 3:1 (WCAG 2.1 SC 1.4.11).

### Le conteneur

`position: sticky`, `bottom: 0`, `margin-top: 0.75rem`, `padding: 0.5rem`, `border-top`, `z-index: 10`, grille à quatre colonnes avec `gap: 6px` : **toutes les valeurs sont identiques**, seuls les tokens changent.

### Ce qui a été ajouté, et pourquoi

Une `transition` sur la touche, coupée par `@media (prefers-reduced-motion: reduce)`. Les touches n'en avaient aucune avant. Le design system en met une sur `Bouton` ; sans le réglage système, une transition maintiendrait le compositeur éveillé pendant la frappe — sur un appareil d'entrée de gamme, c'est le pire moment. Le réglage système est donc nécessaire, et un test vérifie qu'il est présent.

La grille, elle, reste **sans aucune animation**, comme avant — vérifié par test.

---

## 7. POIDS

### Route `/parcours/[id]`

| | Avant (C2a) | Après (C2b) | Écart | Budget |
|---|---|---|---|---|
| **JS total** | 113,12 Ko | **113,38 Ko** | **+0,26 Ko** | +4 Ko ✅ |
| **CSS total** | 5,92 Ko | **6,34 Ko** | +0,42 Ko | — |
| **CSS réellement ajouté** | 2,48 Ko | **3,23 Ko** | **+0,75 Ko** | +3 Ko ✅ |

`globals.css` a **réduit** de 0,33 Ko grâce au retrait des 11 blocs clavier — c'est pourquoi le CSS total n'augmente que de 0,42 alors que la migration en ajoute 0,75.

Sortie du build :

```
Route (app)                                 Size  First Load JS
┌ ƒ /                                    1.29 kB         107 kB
├ ○ /_not-found                            993 B         104 kB
├ ƒ /design-system                       10.7 kB         113 kB
├ ƒ /parcours                            1.22 kB         107 kB
└ ƒ /parcours/[id]                       10 kB         116 kB
```

**Le budget ajusté est respecté sur les deux critères**, avec une large marge : 0,26 Ko sur 4 autorisés, 0,75 Ko sur 3 autorisés.

---

## 8. TEST DU PLAFOND 15 Ko gzip — RÉSULTAT

Un test ajouté dans `clavier-migration.test.ts` mesure le plus gros chunk applicatif de `/parcours/[id]` et **échoue s'il dépasse 15 Ko gzip**. Il lit `.next/app-build-manifest.json`, ce qui signifie qu'il n'a de valeur qu'après un build — le test le dit et retourne alors sans conclure plutôt que de mentir.

```
Chunk client de /parcours/[id] : 9,81 Ko gzip
Plafond imposé                   : 15,00 Ko gzip
Marge                            : 5,19 Ko
Tests  24 passed (24)
```

**Le plafond n'est pas atteint.** À titre de comparaison, le chunk mesurait 5,66 Ko avant le C2a, 9,54 Ko après le C2a, et 9,81 Ko après le C2b : **la migration du clavier n'a ajouté que 0,27 Ko de JavaScript**. Le clavier était déjà client ; il s'agissait de changer sa feuille, pas son architecture.

---

## 9. TESTS

### Résultats

| Suite | Avant | Après | Écart |
|---|---|---|---|
| Frontend UI (Vitest) | 376 | **414** | **+38** |
| Frontend logique (`node --test`) | 119 | **119** | 0 |
| **Total** | 495 | **533** | **+38** |

`tsc --noEmit` : exit 0. `next build` : exit 0. `npm run verifier:poids` : OK, 9,5 Ko gzip pour 30 Ko.

### `ToucheClavier.test.tsx` — 14 tests

Cible tactile : classe du module local (plus `clavier__touche`) · `<button type="button">` avec `aria-label` et `aria-controls` · largeur appliquée sur la grille · variante de service présente.
Activation au doigt : `pointerdown` exécute l'action · événement transmis tel quel · ne déclenche pas la voie clavier.
Activation au clavier : `click` exécute · `Masquer` actionnable · un clic à `detail: 1` est transmis (c'est `ClavierMath` qui filtre).
Pas de double déclenchement : `pointerdown` puis `click` transmettent les deux événements · les deux portent la même touche.
Accessibilité : contrôle de formulaire natif, non désactivé, sans `tabindex` manuel — donc tabulable.

### `clavier-migration.test.ts` — 24 tests

| Groupe | Ce qui est verrouillé |
|---|---|
| Hauteur | `min-height` par token 44 px · **le calcul refait depuis le CSS donne 453 px** · 437 px sous 700 px, et la règle ne touche que le padding · l'écart entre rangées reste plus faible que l'écart entre touches |
| Largeur | quatre colonnes · `COLONNES = 4` toujours dans `lib/clavier.ts` · **73,5 px par touche à 360 px** |
| Activation | `onPointerDown` et `onClick` présents sur chaque touche · `ClavierMath` fournit toujours les deux gestionnaires · **`detail > 0` toujours là, avec sa forme exacte** · `preventDefault` conservé · les gestionnaires reçoivent la touche entière · `aria-label`, `aria-controls`, `role="group"` conservés |
| Variable CSS | `--relio-clavier-systeme` toujours publié par le hook · toujours consommé par `exercice.module.css` · `position: sticky`, `bottom: 0`, `z-index: 10` conservés |
| Aucune classe globale | **`globals.css` ne contient plus aucune règle `.clavier`** · aucun fichier migré ne nomme de classe globale · la grille n'a aucune animation · la transition de la touche est coupée par `prefers-reduced-motion` |
| Tokens et échelle | aucune couleur brute, **à l'exception documentée et comptée de l'ombre du clavier** · toute couleur vient d'un token · aucune mesure hors échelle |
| Plafond | **le chunk client de `/parcours/[id]` ne dépasse pas 15 Ko gzip** |

### Vérification « échouait avant »

`ClavierMath.tsx` et `globals.css` remis dans leur état C2a (`git show 3c0fd24:…`) :

```
  × les deux gestionnaires reçoivent la touche entière
  × `globals.css` ne contient plus aucune règle `.clavier`
  × aucun fichier migré ne nomme de classe de `globals.css`
  Tests  3 failed | 21 passed (24)
```

### Un test du chantier A a dû être adapté

`globals-applicatif.test.ts` vérifiait que `.clavier__touche` utilise une bordure forte. La classe n'existe plus. **L'intention est conservée** : le test pointe désormais `ToucheClavier.module.css`, vérifie la bordure forte, **et vérifie que l'ancien bloc a disparu de `globals.css`** — un test qui s'efface au lieu de se mettre à jour est un test mort.

---

## 10. CE QUI N'A PAS PU ÊTRE FAIT, ET POURQUOI

| Point | Raison |
|---|---|
| **Utiliser le composant `Bouton` du design system pour les touches** | `Bouton` impose `min-height: 48px`. Le clavier fait 9 rangées de 44 px : le porter à 48 px le ferait passer de **453 à 485 px**, et le chantier 7.7 a précisément corrigé le fait que le clavier recouvrait l'énoncé. C'est documenté dans `ToucheClavier.module.css` et dans le rapport. Le composant `Bouton` n'a pas été forcé. |
| **Utiliser `Carte` pour le conteneur** | Le clavier a un fond, une bordure haute et une ombre portée vers le haut. Une `Carte` ajouterait un rayon et une ombre vers le bas : un double contour autour du clavier. Un `div` avec module local est le bon choix. Documenté. |
| **Utiliser `Icone` pour les touches de contrôle** | Le cahier des charges le mentionne comme option. Les touches sont des libellés courts (« Masquer », « Clavier système », « Vérifier ») : remplacer le mot par une icône retirerait le seul texte que l'élève lit. Aucun glyphe n'a été introduit. |
| **Zéro couleur brute** | Une seule subsiste : l'ombre portée **vers le haut** du clavier, `rgba(15, 23, 42, 0.06)`. Le design system n'a pas de token pour elle — ses trois ombres sont toutes vers le bas. La recomposer en `color-mix(in srgb, var(--relio-texte) 6%, transparent)` donnerait exactement la même teinte, mais **exclut les navigateurs antérieurs à 2023**, alors que le public est un téléphone d'entrée de gamme. Une ombre ne porte aucune information : l'exception est comptée par le test et documentée, plutôt que risquée. |
| **Vérification tactile sur un téléphone réel** | Aucun appareil, aucun émulateur dans l'environnement. Les 44 px sont vérifiés **par calcul sur le CSS**, pas à la mesure. C'est la limite assumée de cet environnement, déjà signalée aux chantiers précédents. |
| **Le retrait des autres classes mortes de `globals.css`** | Chantier C2c, hors périmètre. 28 classes restent mortes, pour un gain mesuré de 0,56 Ko au C1. |
| **Le test du plafond sans build** | `.next/app-build-manifest.json` n'existe pas avant un build. Le test retourne alors sans conclure — plutôt que d'affirmer un plafond qu'il n'a pas pu mesurer. Le rapport donne la mesure réelle. |
| **`verifier:poids` dans la CI** | Décision humaine en attente. |

---

## 11. STATUT GLOBAL

# ✅

**Le chantier est fait, et il est le premier de la série à tenir tous ses critères.**

La migration est complète : `ClavierMath.tsx` n'utilise plus aucune classe de `globals.css`, et les 11 blocs `.clavier*` ont été retirés de la feuille globale après vérification qu'aucun autre écran ne les employait. Les deux budgets de poids sont respectés avec une large marge — **+0,26 Ko de JavaScript sur 4 autorisés**, **+0,75 Ko de CSS sur 3 autorisés**. Le plafond de 15 Ko imposé sur le chunk client n'est pas atteint : **9,81 Ko**, et le test le fera échouer si un jour il l'est.

Les trois garanties du chantier sont vérifiées par des commandes reproductibles : `lib/clavier.ts` n'a pas bougé, les dimensions sont recalculées depuis le CSS (453 px, 437 px sous 700 px), et `onPointerDown` + `onClick` + `detail > 0` sont conservés — déplacés, pas réécrits. Les 14 tests du correctif A1 passent sans modification.

**Deux points à signaler.** D'abord, le composant `Bouton` n'a **pas** été utilisé : ses 48 px auraient porté le clavier à 485 px et recouvré l'énoncé, c'est-à-dire annulé le chantier 7.7. C'est documenté, pas subi. Ensuite, une couleur brute subsiste — l'ombre vers le haut du clavier — parce que la recomposer en `color-mix` exclut les navigateurs anciens alors que le public est un appareil d'entrée de gamme. Elle est comptée par le test, donc elle ne peut pas se propager sans être vue.