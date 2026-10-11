# RAPPORT DE FIN DE CHANTIER C2a — MIGRATION DE `Exercice.tsx` SUR LE DESIGN SYSTEM

**Date :** 2026-10-11
**Dépôt :** `relio-frontend`
**Commit :** `3c0fd24`
**Nature :** migration de la couche visuelle. **Aucune fonctionnalité nouvelle, aucune suppression.** Le clavier n'est pas touché.

---

## 1. RÉSUMÉ

1. `Exercice.tsx` (463 → 199 l.) et `parcours/[id]/page.tsx` n'utilisent plus **aucune** classe de `globals.css`. L'en-tête et le pied de page réutilisent directement les classes de `parcours.module.css` — les deux écrans ne peuvent plus diverger.
2. **La logique est intacte** : 10 `useState`, 0 `useReducer`, les 4 appels d'API, le journal local, les props du clavier, la mesure `visualViewport`. Un test de migration vérifie chaque point.
3. Sept composants du design system sont utilisés : `Carte`, `Champ`, `EtatVide`, `Squelette`, `Bouton`, plus `Icone` et `Pastille` via `Verdict` et `Tutorat`, désormais des composants purs.
4. **`ClavierMath.tsx` n'a pas bougé** : `git diff 7a03ce7 -- src/components/ClavierMath.tsx src/lib/clavier.ts` est vide, et un test le garantit.
5. Poids : JS **+3,88 Ko** gzip (budget 2 ⚠️), CSS ajouté **+2,48 Ko** (budget 2 ⚠️). Tests : 294 → 376 (+82), 0 échec.

---

## 2. DIFF DES FICHIERS

### Créés (6)

| Fichier | Lignes | Rôle |
|---|---|---|
| `src/app/parcours/[id]/Verdict.tsx` | 148 | Composant **pur** du verdict. Les 5 variantes de la décision D5. |
| `src/app/parcours/[id]/Tutorat.tsx` | 79 | Composant **pur** du panneau d'aide. Les 3 niveaux. |
| `src/app/parcours/[id]/exercice.module.css` | 300 | Feuille locale. Tokens `--relio-*` uniquement. |
| `src/app/parcours/[id]/Verdict.test.tsx` | 220 | 29 tests : les 5 variantes, aucun score, langue. |
| `src/app/parcours/[id]/Tutorat.test.tsx` | 140 | 12 tests : les 3 niveaux, ce que le panneau ne dit jamais. |
| `src/components/Exercice.test.tsx` | 227 | 14 tests d'écran : les états, l'API, les rôles ARIA. |
| `src/design/exercice-migration.test.ts` | 284 | 27 tests statiques, dont **10 sur l'intégrité de la logique**. |

### Modifiés (3)

| Fichier | Modification |
|---|---|
| `src/components/Exercice.tsx` | 463 → **199 l.** −264 l. de JSX de présentation, + le rendu par `Verdict`. |
| `src/app/parcours/[id]/page.tsx` | 52 → 76 l. En-tête et pied de page migrés. |
| `src/design/parcours-migration.test.ts` | `SOURCES_C2` réduite à `ClavierMath.tsx` : `Exercice.tsx` et `page.tsx` sont migrés par le C2a. |

### Non touchés — vérifié par diff

`src/components/ClavierMath.tsx` · `src/lib/clavier.ts` · `src/lib/parcours.ts` · `src/lib/observations.ts` · `src/app/globals.css`

---

## 3. L'ÉCRAN MIGRÉ, ÉTAT PAR ÉTAT

### Chargement

```
┌───────────────────────────────────────────┐
│  ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬  (70 %)              │
│  ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬                    │
│  ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬    │
└───────────────────────────────────────────┘
```

`Carte role="status"` + trois `Squelette` (`aria-hidden`). L'ancien écran affichait « Chargement de l'exercice… » — un texte d'attente sans forme ; le squelette montre la forme de ce qui arrive, donc la page ne saute pas.

### Exercice indisponible

```
┌───────────────────────────────────────────┐
│  ℹ   Cet exercice n'est pas disponible    │
│      pour le moment                       │
│      Le service n'a pas répondu. La page  │
│      fonctionne ; seul l'exercice est en  │
│      attente.                             │
│                                           │
│        [    Réessayer    ]                │
└───────────────────────────────────────────┘
```

`EtatVide` + `<form action="/parcours" method="get"><Bouton type="submit">Réessayer</Bouton></form>`, comme sur l'accueil et `/parcours`. **Fonctionne sans JavaScript.**

L'ancien écran affichait `erreurChargement` — le motif technique brut de l'API — dans un `<p role="status">`. Un élève n'a rien à faire d'un message d'erreur réseau ; il peut réessayer. Test : `HTTP 500` n'apparaît pas à l'écran.

### Exercice chargé

```
R | Relio
Exercice
Lis l'énoncé, écris ta réponse, et vérifie.

┌───────────────────────────────────────────┐  ← Carte elevee
│ On considère le nombre A = 3(x + 2) − (x+5)│  ← enonce, taille xl
│ Développe et réduis A. Écris le résultat │  ← consigne, taille base
│ réduit.                                   │
└───────────────────────────────────────────┘

┌───────────────────────────────────────────┐
│ Ta réponse                                │  ← label lie par Champ
│ [ Ax + B                              ]  │  ← bordure forte 3,66:1
│ Réponse attendue : forme réduite.        │  ← aria-describedby
│                                           │
│ Tu écris : 3x+1                           │  ← aria-live="polite"
│                                           │
│ [        Vérifier         ]              │  ← Bouton primary lg pleine largeur
│ [    Un indice (3)    ]                   │  ← Bouton secondary lg
└───────────────────────────────────────────┘
```

**Ce qui a changé dans la structure :**

| Avant | Après |
|---|---|
| Énoncé et consigne en `<p>` dans une zone unique | Carte `variante="elevee"` dédiée |
| `<label>` posé à la main autour d'un `<input>` | `Champ` du design system |
| Aucune description liée au champ | `aria-describedby` vers l'aide « Réponse attendue : … » |
| Aperçu en `<p>` italique gris | Aperçu avec un libellé « Tu écris : », announced poliment |
| « Vérifier » et « Indice » côte à côte, sans hiérarchie | « Vérifier » **primary pleine largeur**, « Indice » secondary en dessous |

La hiérarchie demandée est respectée : à 360 px, un seul bouton primary occupe toute la largeur ; le secondaire ne peut pas être confondu avec lui.

### Après correction

```
┌───────────────────────────────────────────┐
│ [ À revoir ]                        ( ! )  │  ← Pastille + Icone
│ Ce n'est pas encore juste.                │  ← libelle du serveur
│                                           │
│ Reviens sur la distributivité.            │  ← explication
└───────────────────────────────────────────┘

┌───────────────────────────────────────────┐  ← carte imbriquée, bordure gauche
│ [ Première piste ]  aide 1 sur 3          │  ← Pastille + palier
│ Reprends la dernière étape.               │
│                                             │
│ Méthode à retenir : On distribue avant   │  ← seulement si résumé
│ de réduire.                                 │
└───────────────────────────────────────────┘
```

Les cinq variantes :

| Verdict | Pastille | Message (du serveur) |
|---|---|---|
| `correct` | `Juste` (succes) | « Ta réponse est juste. » |
| `partiellement_correct` | `À compléter` (alerte) | « Ta réponse est partiellement correcte. » |
| `resultat_juste_consigne_non_respectee` | `Juste, à reformuler` (alerte) | « Ton résultat est juste, mais pas dans la forme demandée. » |
| `incorrect` | `À revoir` (alerte) | « Ce n'est pas encore juste. » |
| `a_determiner` | `À vérifier` (neutre) | « Ta réponse est juste ; la forme demandée reste à vérifier. » |

`partiellement_correct` et `resultat_juste_consigne_non_respectee` partagent volontairement le ton `alerte` : tous deux signifient « tu n'as pas tout à fait, mais tu n'as pas faux ». Le signal « rouge » serait un contresens pédagogique — c'est la décision D5, pas un choix de charte.

### Réponse illisible

```
┌───────────────────────────────────────────┐
│ Ta réponse n'est pas lisible.             │
│ Vérifie les symboles.                     │
│ Relis la question.                        │
└───────────────────────────────────────────┘
```

`Carte role="status"`. La catégorie technique (`reponse_illisible`) n'apparaît jamais — vérifié par test.

---

## 4. COMPOSANTS DU DESIGN SYSTEM UTILISÉS

| Composant | Où | Rôle |
|---|---|---|
| `Carte` | énoncé, indices, suivi, verdict, saisie illisible, chargement, indisponible | Regroupements. `variante="elevee"` pour l'énoncé et le verdict ; `sansOmbre` pour les indices et le suivi |
| `Champ` | zone de saisie | **Le gain principal.** Relie `label`, `aide` et `erreur` par `aria-describedby` — l'ancien `<label>` manuel ne faisait pas cette liaison |
| `Bouton` | Vérifier, Indice, Réessayer, Revenir au clavier, Effacer l'historique | `primary`/`lg`/`pleineLargeur` pour Vérifier ; `secondary` pour Indice et Réessayer ; `ghost`/`sm` pour Effacer |
| `EtatVide` | exercice indisponible | Message + action de sortie |
| `Squelette` | chargement | Trois blocs de la forme de l'écran |
| `Icone` | verdict, action du tutorat | SVG inline. L'emoji `👉` littéral a disparu — il était lu « index pointant vers la droite » par un lecteur d'écran |
| `Pastille` | statut du verdict, niveau d'aide | Toujours **avec son texte** |

**Imports par chemin direct partout.** Le barrel `@/components/ds` n'apparaît dans aucun fichier migré — il entraînerait le mapping CSS des 14 composants dans le bundle client.

`page.tsx` réutilise aussi `parcours.module.css` pour l'en-tête et le pied de page : aucune duplication.

---

## 5. POIDS AVANT / APRÈS

Mesure gzip niveau 9, deux builds comparés (`7a03ce7` et `3c0fd24`).

### Route `/parcours/[id]`

| | Avant | Après | Écart | Budget |
|---|---|---|---|---|
| **JS total** | 109,24 Ko | **113,12 Ko** | **+3,88 Ko** | +2 Ko ⚠️ **+1,88** |
| **CSS total** | 3,44 Ko *(via `layout`)* | **5,92 Ko** | +2,48 Ko | — |
| **CSS réellement ajouté** | — | — | **+2,48 Ko** | +2 Ko ⚠️ **+0,48** |

Le chunk client de l'écran, isolément :

| | Avant | Après | Écart |
|---|---|---|---|
| `app/parcours/[id]/page-*.js` | **5,66 Ko** | **9,54 Ko** | **+3,88 Ko** |

Sortie du build :

```
Route (app)                                 Size  First Load JS
┌ ƒ /                                    1.29 kB         107 kB
├ ○ /_not-found                            993 B         104 kB
├ ƒ /design-system                       10.7 kB         113 kB
├ ƒ /parcours                            1.22 kB         107 kB
└ ƒ /parcours/[id]                       9.77 kB         116 kB     ← avant : 5.8 kB / 112 kB
```

### Pourquoi le budget est dépassé

C'est **le coût structurel de migrer un écran client**, et il est mesuré, pas supposé. `/parcours/[id]` est le seul composant `'use client'` de l'application : tout ce qu'il importe part dans le bundle du navigateur. Avant la migration, il n'utilisait **aucun** composant du design system. Après, il en utilise six.

Les 3,88 Ko ne sont pas du code superflu : ce sont `Carte`, `Champ`, `EtatVide`, `Squelette`, `Bouton`, `Icone`, `Pastille` et les deux composants locaux `Verdict` et `PanneauTutorat`, enlevés de `Exercice.tsx` (−264 lignes) et réintroduits comme briques du design system.

**Ce qui a été fait pour réduire :** l'import de `Pastille` dans `Exercice.tsx` a été retiré — il n'y était plus utilisé après la migration. Le reste est intégralement utilisé, contrôlé par test.

**Ce qui n'a pas été fait :** réduire davantage supposait de remplacer un composant du design system par un `<div>` local — exactement ce que le chantier interdit (« TOUT conteneur et TOUT élément interactif vient du DS »). Aucune dégradation visuelle n'a été appliquée pour faire entrer le chiffre.

**Compensation attendue au C2c :** le retrait des 39 classes de `globals.css` devenues morts rendra **0,56 Ko** (mesurés au C1) sur cette route, puisque `globals.css` y est toujours chargé pour le clavier. Cela ne comble pas entièrement le dépassement JS, mais ramène le CSS sous son budget d'origine.

---

## 6. TESTS

### Résultats

| Suite | Avant | Après | Écart |
|---|---|---|---|
| Frontend UI (Vitest) | 294 | **376** | **+82** |
| Frontend logique (`node --test`) | 119 | **119** | 0 |
| **Total** | 413 | **495** | **+82** |

`tsc --noEmit` : exit 0. `next build` : exit 0.

### `Verdict.test.tsx` — 29 tests

Les cinq variantes × (pastille + libellé serveur mot pour mot) = **10 tests**.
Puis : `correct` en ton succès · `resultat_juste…` jamais présenté comme faux · `a_determiner` ne tranche pas · repli quand le serveur ne fournit pas `libelle`.
Puis, pour chaque variante : **aucun pourcentage, aucun « 7/10 », aucun mot « score » ou « maîtris »** · **aucun terme technique** (`undefined`, `NaN`, `OO-L`, `erreur_de_signe`, `pointsArbitrage`…).
Puis : explication sans tutorat · message du tutorat quand il y en a un · consigne de réécriture · travail inachevé présenté comme un commencement · point non arbitré non présenté comme une conclusion.

### `Tutorat.test.tsx` — 12 tests

Les 3 niveaux avec leur pastille et leur palier · message toujours affiché · action seulement à partir du niveau 2 · méthode dépliée dès qu'elle existe · bilan sans palier ni action.
Puis : **niveau 1 ne dit jamais « essaie encore »** · **niveau 3 ne dit jamais « tu n'as pas compris »** · **aucun identifiant technique** (`OO-L`, `erreur_de_signe`, `signature`, `N1`…) · aucun score · « aide N sur 3 » qualifie l'aide reçue, pas un niveau de maîtrise.

### `Exercice.test.tsx` — 14 tests d'écran

Quatre états : chargement (squelette), exercice chargé, exercice indisponible (`EtatVide` + formulaire GET), réponse illisible.
Puis : énoncé et consigne · **label visible associé au champ** · **`aria-describedby` pointe bien vers l'aide « Réponse attendue »** · boutons Vérifier et « Un indice (3) » · Vérifier désactivé si vide · demander un indice appelle l'API avec les bons arguments et affiche le texte reçu · **le clavier est monté tel quel, sans changement** · aucun rôle inexistant en ARIA · la correction passe par l'API et s'affiche dans une région vivante · les arguments de `corrigerReponse` sont vérifiés un par un.

### `exercice-migration.test.ts` — 27 tests, dont 10 sur l'intégrité de la logique

| Groupe | Ce qui est verrouillé |
|---|---|
| Aucune classe globale | **liste explicite de 43 classes** de `globals.css` · aucun import de `globals.css` · le clavier est le seul élément qui garde ses classes, et `Exercice.tsx` ne les nomme même pas · `.exercice--saisie` est passée en module local et cible `:global(.clavier)` |
| Imports DS | jamais par le barrel · tous les composants importés existent |
| **Clavier (C2b)** | **`ClavierMath.tsx` n'a aucun import du design system, aucun import de module CSS, et conserve `className={\`bouton clavier__touche…\`}`** |
| Tokens | aucune couleur brute (hex, `rgb()`, `hsl()`) · toute couleur vient d'un token · aucune mesure hors échelle · points de rupture limités à `{360, 420, 768}` |
| **Logique intacte** | **10 `useState`, déclarés une seule fois chacun, nommés explicitement** · **aucun `useReducer`** · les 4 appels d'API inchangés · `ajouterObservation`, `effacerJournal`, `lireJournal`, `echecsConsecutifs` toujours là · les 7 props de `ClavierMath` identiques · `'use client'` conservé · `useHauteurClavierSysteme` et `data-clavier-systeme` toujours branchés · `label`, `aria-live="polite"`, `role="status"`, `aria-label="Indices"`, `aria-label="Mon suivi"` conservés · `LIBELLE_REPLI` et `libelleAffiche` absents de l'écran (ils ont suivi dans `Verdict.tsx`) |

### Vérification « échouait avant »

`exercice-migration.test.ts` exécuté sur `Exercice.tsx` et `page.tsx` d'origine (`git show 7a03ce7:…`) :

```
  × components/Exercice.tsx n’utilise aucune classe de globals.css
  × app/parcours/[id]/page.tsx n’utilise aucune classe de globals.css
  × les accessibilités déjà en place sont conservées
  × les libellés du serveur ne sont pas recomposés localement
  Tests  4 failed | 23 passed (27)
```

`Exercice.tsx` d'origine utilise `.carte`, `.exercice__*`, `.verdict--*`, `.tutorat__*`, `.indices`, `.suivi__*`, `.bouton--principal`, `.bouton--discret` ; `page.tsx` utilise `.page`, `.conteneur`, `.entete--interne`, `.pied`, `.lien`. Aucun `<Champ>`, et `libelleAffiche` est encore local.

---

## 7. CONFIRMATION EXPLICITE — `ClavierMath.tsx` N'A PAS BOUGÉ

```
$ git diff 7a03ce7 -- src/components/ClavierMath.tsx src/lib/clavier.ts
(VIDE)
```

Et un test le garantit en continu :

```ts
it('ClavierMath.tsx n'a reçu aucun import du design system (C2b)', () => {
  const source = sansCommentaires(contenu(CLAVIER));
  expect(source).not.toMatch(/@\/components\/ds/);
  expect(source).not.toMatch(/\.module\.css/);
  expect(source).toMatch(/className=\{`bouton clavier__touche/);
});
```

Le clavier est le seul élément de l'écran qui conserve des classes de `globals.css`. Le module local le cible avec `:global(.clavier)` pour Reproduire le comportement du chantier 7.7 — sans réécrire ses règles.

## 8. CONFIRMATION EXPLICITE — LES `useState` SONT INCHANGÉS

```
$ grep -c "= useState" src/components/Exercice.tsx   →  10
$ git show 7a03ce7:src/components/Exercice.tsx | grep -c "= useState"  →  10
```

Les dix états, déclarés une seule fois chacun, dans le même ordre :

| # | État | Origine |
|---|---|---|
| 1 | `exercice` | chantier 7 |
| 2 | `erreurChargement` | chantier 7 |
| 3 | `saisie` | chantier 7.5 |
| 4 | `verdict` | chantier 7 |
| 5 | `enCours` | chantier 7 |
| 6 | `indices` | chantier 7 |
| 7 | `clavierOuvert` | chantier 7.5 |
| 8 | `clavierSysteme` | chantier 7.5 |
| 9 | `tentatives` | chantier 7.5 |
| 10 | `suivi` | chantier 7.5 |

Aucun `useReducer` n'a été introduit. Les quatre appels d'API, le journal local, les sept props de `ClavierMath`, le `'use client'` et la mesure `visualViewport` sont vérifiés par test, pas par relecture.

---

## 9. CE QUI N'A PAS PU ÊTRE FAIT, ET POURQUOI

| Point | Raison |
|---|---|
| **Respecter le budget de +2 Ko gzip** | Dépassement de **1,88 Ko sur le JS** et **0,48 Ko sur le CSS**. La cause est structurelle et mesurée : un écran client qui utilise six composants du design system transporte leur code dans le bundle. Réduire supposait de remplacer un composant DS par un `<div>` local — ce que le chantier interdit. Aucune dégradation n'a été appliquée |
| **Vérification visuelle à 360 px avec le clavier ouvert** | Aucun navigateur, aucun appareil. La colonne contrainte est reproduite à l'identique et le comportement du chantier 7.7 est documenté dans le module, mais **pas observé** |
| **Contrôle du rendu réel de l'anneau de focus sur les nouveaux boutons** | `accessibilite.test.ts` contrôle le CSS du design system statiquement ; aucun rendu navigateur ici |
| **Le retrait des classes mortes de `globals.css`** | Chantier C2c, hors périmètre. Gain mesuré : 0,56 Ko sur cette route |
| **`ClavierMath` sur le design system** | Chantier C2b, hors périmètre. Vérifié par test |
| **`ZoneTexte`** | Prévu au cahier des charges « si un champ long est nécessaire ». La réponse à un exercice tient sur une ligne : `Champ` suffit. Importé nulle part |
| **`Notification`** | Prévu « si un feedback transitoire est nécessaire ». Le verdict s'affiche dans la zone défilante — un toast masquerait l'énoncé, qui est précisément ce que le chantier 7.7 a corrigé. **Décision à documenter par le commanditaire** si un retour transitoire est jugé nécessaire |
| **`verifier:poids` dans la CI** | Décision humaine en attente |

---

## 10. STATUT GLOBAL

# ⚠️

**Le chantier est fait et le comportement est intact :** la migration est complète, aucune classe globale ne subsiste, les 10 `useState`, les 4 appels d'API, le journal local et les props du clavier sont vérifiés par test, `ClavierMath.tsx` n'a pas bougé, et 82 tests nouveaux passent — 376 au total, 0 échec.

**Les deux budgets de poids sont dépassés : +3,88 Ko de JavaScript et +2,48 Ko de CSS, pour un seuil de +2 Ko sur chacun.** Le dépassement est structurel, mesuré et explicable : c'est le prix de la première migration d'un écran client, et il ne peut être réduit qu'en contournant le design system — ce que le chantier interdit explicitement. La compensation partielle est mesurée : 0,56 Ko au C2c.

Le chantier est donc livré, mais **le critère « poids » n'est pas tenu**. C'est le seul point non conforme, et il est explicitement mesuré plutôt que masqué.