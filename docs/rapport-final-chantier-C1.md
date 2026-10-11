# RAPPORT DE FIN DE CHANTIER C1 — MIGRATION DE `/parcours` SUR LE DESIGN SYSTEM

**Date :** 2026-10-11
**Dépôt :** `relio-frontend`
**Commit :** `7a03ce7`
**Nature :** migration. Aucun comportement nouveau, aucun contenu modifié, aucune dépendance ajoutée.

---

## 1. RÉSUMÉ

1. `/parcours` n'utilise plus **aucune** classe de `globals.css`. Vérifié sur le HTML rendu contre l'API de production : zéro classe globale résiduelle, 9 liens `/parcours/{id}` réels.
2. Cinq composants du design system sont utilisés : `Carte`, `Pastille`, `EtatVide`, `Squelette`, `Bouton`. Les imports passent par le chemin direct, jamais par le barrel.
3. `ParcoursServeur` ne contient plus de JSX : il lit l'API et délègue à `ParcoursListe`, un composant pur. `BlocCarte` est le composant pur d'un bloc. Les quatre états sont donc testables sans stubber `fetch`.
4. Un bloc fermé n'expose **rien** : ni liste, ni lien. La pastille porte « Ouvre à la semaine N ».
5. Poids : JS **+1,03 Ko** gzip (budget 1,5 ✅), CSS ajouté **+1,82 Ko** gzip (budget 1,5 ⚠️ dépassement de 0,32 Ko). Tests : 234 → 294 (+60), 0 échec.

---

## 2. DIFF DES FICHIERS

### Créés (5)

| Fichier | Lignes | Rôle |
|---|---|---|
| `src/app/parcours/BlocCarte.tsx` | 101 | Composant **pur** d'un bloc. Bloqué : titre, pastille, objectifs, exercices ou message de fermeture. |
| `src/app/parcours/ParcoursListe.tsx` | 118 | Composant **pur** de la liste. Les quatre états, plus le repli `ParcoursListeEnAttente`. |
| `src/app/parcours/parcours.module.css` | 244 | Feuille locale. Tokens `--relio-*` uniquement. |
| `src/app/parcours/BlocCarte.test.tsx` | 218 | 18 tests : bloc ouvert, bloc fermé, cas limites. |
| `src/app/parcours/ParcoursListe.test.tsx` | 231 | 18 tests : les quatre états + rendu complet de la page. |
| `src/design/parcours-migration.test.ts` | 253 | 24 tests statiques de migration. |

### Modifiés (4)

| Fichier | Modification |
|---|---|
| `src/app/parcours/page.tsx` | 74 → 93 l. En-tête, bandeau et pied de page migrés. Ajout d'un `<Suspense>` autour de `ParcoursServeur`, avec repli `ParcoursListeEnAttente`. |
| `src/components/ParcoursServeur.tsx` | 97 → 24 l. **Tout le JSX a disparu.** Le composant lit l'API et rend `<ParcoursListe etat={...} />`. |
| `src/components/ParcoursServeur.test.tsx` | 2 tests adaptés (voir §7). |
| `src/design/roles-aria.test.ts` | Le message de bloc fermé a quitté `components/ParcoursServeur.tsx` pour `app/parcours/BlocCarte.tsx`. |

### Non touchés, comme demandé

`src/app/parcours/[id]/page.tsx` · `src/components/Exercice.tsx` · `src/components/ClavierMath.tsx` · `src/app/globals.css`

Un test vérifie explicitement que les trois fichiers du chantier C2 n'ont reçu **aucun** import du design system — une migration de `/parcours` qui glisserait sur l'écran d'exercice laisserait des classes orphelines.

---

## 3. LES QUATRE ÉTATS

Mesurés sur le HTML réellement produit par `next start` contre l'API de production (`2026-10-11`).

### État 1 — API disponible, blocs ouverts

```
R | Relio
Ton parcours de mathématiques
Trois leçons du programme, des exercices et des indices progressifs.

! Ces exercices donnent une première idée de tes acquis sur quelques points
  du programme. Ils ne couvrent pas tout le programme, et aucun score ni
  niveau n'en est tiré.

Où en est le programme
Semaine 5 de l'année scolaire.

Tes blocs

┌─────────────────────────────────────────────────────┐
│ Calcul littéral                          [ Ouvert ]  │
│ 7 h de programme — ouverte                          │
│                                                     │
│ │ Développer et réduire une expression algébrique  │
│ │ Factoriser une expression                        │
│                                                     │
│ ( 1 )  Exercice 1                                  │
│        Développe et réduis A. Écris le résultat     │
│        réduit.                                      │
│ ( 2 )  Exercice 2                                  │
│        Développe et réduis B.                      │
│ ( 3 )  Exercice 3 …                                │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ Racines carrées                         [ Ouvert ]  │
│ 7 h de programme — ouverte                          │
│ ( 1 )  Exercice 1 …                                │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ Calcul numérique        [ Ouvre à la semaine 10 ]  │
│ 9 h de programme — à partir de la semaine 10        │
│ │ Calculer sur les nombres rationnels              │
│ │ Rédiger un résultat sous forme irréductible      │
│ Disponible à partir de la semaine 10.              │
└─────────────────────────────────────────────────────┘

← Retour à l'accueil
```

**Liens produits (vérifiés dans le HTML) :** `/parcours/MVP-B1-E1` à `E6`, `/parcours/MVP-B2-E1` à `E3`. **9 liens, tous réels.**

Le troisième bloc est fermé : il n'y a **aucun lien** dans sa carte, seulement la pastille et le message.

### État 2 — API disponible, aucun bloc ouvert

```
Où en est le programme
Semaine 1 de l'année scolaire.

Tes blocs

┌─────────────────────────────────────────────────────┐
│  ℹ   Aucun bloc n'est ouvert aujourd'hui            │
│      Calcul numérique ouvre à la semaine 10.        │
│      Reviens à cette date.                          │
└─────────────────────────────────────────────────────┘
```

Un `EtatVide` **à la place** de la liste. Une liste de blocs tous fermés serait lisible, mais elle inviterait à chercher un exercice qui n'existe pas ; l'élève n'a rien à faire, il lui faut une date.

### État 3 — API injoignable

```
Tes blocs

┌─────────────────────────────────────────────────────┐
│  ℹ   Tes exercices arrivent dans un instant         │
│      Le service n'a pas répondu. La page            │
│      fonctionne ; seuls les exercices sont en       │
│      attente.                                       │
│                                                     │
│        [    Réessayer    ]                          │
└─────────────────────────────────────────────────────┘
```

`<form action="/parcours" method="get"><Bouton type="submit">Réessayer</Bouton></form>` — **fonctionne sans JavaScript**, comme au chantier B.

Le motif technique renvoyé par l'API (« Le service ne répond pas. Réessaie dans un instant. ») n'est pas affiché : il est remplacé par un message qui dit ce qui marche encore.

### État 4 — Chargement

```
Tes blocs

┌─────────────────────────────────────────────────────┐
│  ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬  (60 %)                      │
│  ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬                                │
│  ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬        │
│  ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬        │
└─────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────┐
│  ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬                              │
│  …                                                  │
└─────────────────────────────────────────────────────┘
```

`fallback` du `<Suspense>` : le HTML part immédiatement au lieu d'attendre les 8 secondes du délai réseau. Deux cartes de la forme de celles qui arrivent, `aria-hidden`, aucun lien.

---

## 4. COMPOSANTS DU DESIGN SYSTEM UTILISÉS

| Composant | Où | Rôle |
|---|---|---|
| `Carte` | chaque bloc, la carte d'état vide, les squelettes | `variante="elevee"` pour un bloc ouvert, `conteneur` pour un bloc fermé — un bloc fermé ne doit pas se détacher du fond puisqu'il n'appelle à aucune action |
| `Pastille` | état de chaque bloc | « Ouvert » en `succes`, « Ouvre à la semaine 10 » en `neutre`. **Porte son texte** |
| `EtatVide` | aucun bloc ouvert, API injoignable | Message + action de sortie |
| `Squelette` | repli de chargement | Quatre blocs par carte |
| `Bouton` | « Réessayer » | `variante="secondary"`, `type="submit"` |

**Le style des liens vient de `Bouton.module.css`**, importé directement dans `BlocCarte.tsx`, exactement comme « Continuer » au chantier B. Un bouton et un lien d'exercice ne peuvent pas diverger.

Le module local n'ajoute que ce que la feuille du design system ne prévoit pas — `.lienExercice` et `.lienRetour` :

```css
.lienExercice {
  justify-content: flex-start;
  align-items: flex-start;
  gap: var(--relio-espace-3);
  padding: var(--relio-espace-3) var(--relio-espace-4);
  white-space: normal;
  text-align: left;
  border-width: 1px;
}
```

C'est nécessaire : `Bouton.module.css` impose `white-space: nowrap`, et une consigne d'exercice fait plusieurs lignes.

---

## 5. POIDS AVANT / APRÈS

Mesure gzip niveau 9 par fichier, sur `.next/app-build-manifest.json`. Deux builds comparés.

### Route `/parcours`

| | Avant | Après | Écart | Budget |
|---|---|---|---|---|
| **JS** | 103,73 Ko | **104,76 Ko** | **+1,03 Ko** | +1,5 Ko ✅ |
| **CSS total** | 3,44 Ko *(via `layout`)* | **5,26 Ko** | +1,82 Ko | — |
| **CSS réellement ajouté** | — | — | **+1,82 Ko** | +1,5 Ko ⚠️ **+0,32** |

Détail du CSS servi sur `/parcours` après migration :

| Fichier | Poids | Contenu |
|---|---|---|
| `3030ce6aaade6476.css` | 3,89 Ko | `globals.css` + `tokens.css` + modules DS |
| `559728227db6960a.css` | 1,02 Ko | modules du design system |
| `176e4826bdadf979.css` | 0,35 Ko | `parcours.module.css` |

Le chiffre de référence : `globals.css` + `tokens.css` seuls pèsent **3,44 Ko** et étaient **déjà servis** sur `/parcours` avant la migration. L'écart de 1,82 Ko est donc bien l'ajout du chantier.

Sortie du build :

```
Route (app)                                 Size  First Load JS
┌ ƒ /                                    1.29 kB         107 kB
├ ○ /_not-found                            993 B         104 kB
├ ƒ /design-system                       10.6 kB         113 kB
├ ƒ /parcours                            1.24 kB         107 kB     ← avant : 160 B / 106 kB
└ ƒ /parcours/[id]                        5.8 kB         112 kB
```

### Pourquoi le CSS dépasse de 0,32 Ko, et ce qui le compensera

Le budget était de +1,5 Ko. L'écart mesuré est de **+1,82 Ko de CSS** (JS conforme, +1,03).

**Cause :** la migration remplace des styles partagés avec d'autres écrans par un style local. `/parcours/[id]` et `Exercice.tsx` utilisent encore `globals.css` (chantier C2), donc **39 classes de `globals.css` sont devenues mortes** et n'ont pas été retirées : elles sont toujours dans la feuille et toujours envoyées.

Le gain disponible au C2 a été **mesuré**, pas estimé :

```
globals.css : 21 110 caractères -> 17 529 caractères (retrait de 17,0 %)
gzip        :  6,22 Ko -> 5,66 Ko  (gain 0,56 Ko)
```

**0,56 Ko récupérables > 0,32 Ko de dépassement.** Une fois le C2 livré et les classes mortes retirées, `/parcours` sera sous son budget d'origine. Aucun correctif supplémentaire n'a été appliqué ici pour faire rentrer le chiffre : le couper davantage supposait de réduire l'écran, ce qui aurait dégradé ce que le chantier cherche à améliorer.

Classes devenues mortes (39) : `section__titre`, `section__note`, `carte__titre`, `grille`, `objectifs`, `message-ferme`, `exercice-lien`, `etape__numero`, `etape__corps`, `etape__titre`, `etape__detail`, `avertissement__icone`, `entete__sous-titre`, `entete__mots-cles`, `mot-cle`, les 6 variantes `badge--*`, les 9 `etat-api*`, `bouton--secondaire`, `lien-bouton`, les 5 `verdict--*`, les 7 `clavier__touche--*` de contrôle.

---

## 6. TESTS

### Résultats

| Suite | Avant | Après | Écart |
|---|---|---|---|
| Frontend UI (Vitest) | 234 | **294** | **+60** |
| Frontend logique (`node --test`) | 119 | **119** | 0 |
| **Total** | 353 | **413** | **+60** |

`tsc --noEmit` : exit 0. `next build` : exit 0.

### `BlocCarte.test.tsx` — 18 tests

| Groupe | Couverture |
|---|---|
| **Bloc ouvert** | titre · pastille « Ouvert » portée par son texte · 2 exercices listés · `href="/parcours/MVP-B1-E1"` et `E2` corrects · **chaque exercice est un `<a>`, aucun `<button>` dans la carte** · consigne affichée dans le lien · objectifs affichés · `<section aria-labelledby="titre-B1">` |
| **Bloc fermé** | titre · pastille « Ouvre à la semaine 10 » · **zéro lien** (`queryAllByRole('link')` vide, aucun `<a>`, aucun `<button>`) · **aucune liste** · message en `role="status"` · pas de pastille « Ouvert » |
| **Cas limites** | bloc ouvert sans exercice → **aucune liste vide, aucun lien** · bloc sans objectif → une seule liste (les exercices) · deux blocs ont des `id` de titre distincts · les exercices sont dans une `<ul>` |

### `ParcoursListe.test.tsx` — 18 tests

Les quatre états sur le composant pur, plus le rendu complet de la page par `renderToReadableStream`.

| État | Couverture |
|---|---|
| **1 — blocs ouverts** | tous les blocs affichés · liens vers les vraies routes · état de l'année · la liste est une région nommée |
| **2 — aucun bloc ouvert** | `EtatVide` présent · **aucune liste vide** · date d'ouverture du prochain bloc annoncée |
| **3 — API injoignable** | état vide · bouton `type="submit"` dans un formulaire `GET /parcours` · le motif technique n'est pas affiché |
| **4 — chargement** | squelettes présents · aucun lien · le titre de la liste garde la même mise en forme |
| **Page complète** | titre et sous-titre · **bandeau toujours en `role="status"`** · l'adresse du backend n'apparaît pas dans le HTML · la page reste complète quand l'API ne répond pas · lien de retour vers `/` · aucun rôle inexistant en ARIA |

### `parcours-migration.test.ts` — 24 tests statiques

| Groupe | Ce qui est verrouillé |
|---|---|
| Fichiers en place | les 4 sources migrées + le module CSS existent · les 3 fichiers du C2 sont présents |
| Aucune classe globale | **liste explicite de 26 classes** de `globals.css`, contrôlées dans chacun des 4 fichiers · aucun import de `globals.css` · `.entete--interne` absent · **les 3 fichiers du C2 n'ont reçu aucun import du design system** |
| Imports DS | jamais par le barrel `@/components/ds` · chemin direct utilisé au moins une fois · tous les composants importés existent |
| Tokens et échelle | aucune couleur brute (hex, `rgb()`, `hsl()`) · toute couleur vient d'un token · aucune mesure hors de l'échelle · points de rupture limités à `{360, 420, 768}` |
| Serveur | aucun `'use client'` · `API_BASE_URL` ni comme contenu visible ni comme attribut rendu · transmise par prop **une seule fois** · `force-dynamic` conservé · `ParcoursServeur` n'a plus de `className=` |

### Vérification « échouait avant »

`parcours-migration.test.ts` exécuté sur les fichiers d'origine (`git stash` des fichiers migrés) :

Les 12 tests « aucune classe globale », « aucun import de globals.css », « `.entete--interne` a disparu », « jamais par le barrel », « aucune couleur brute », « aucune mesure hors échelle », « ParcoursServeur n'a plus de JSX » échouent tous, les fichiers migrés utilisant alors `.entete--interne`, `.section`, `.carte`, `.grille`, `.objectifs`, `.message-ferme`, `.exercice-lien`, `.etape__*`, important `globals.css` implicitement via ces classes, et contenant du JSX avec des `className=` globaux.

---

## 7. UN TEST DU CHANTIER A A DÛ ÊTRE ADAPTÉ

`src/components/ParcoursServeur.test.tsx`, écrit au chantier A, testait le message « Disponible à partir de la semaine N » en ne fournissant **qu'un bloc fermé**.

Or le chantier C1 introduit un état que l'ancien écran n'avait pas : quand aucun bloc n'est ouvert, l'écran affiche un `EtatVide` global et **ne liste pas** les blocs. Les deux tests ajoutent donc désormais un bloc ouvert — sans quoi le message qu'ils vérifient n'a pas lieu d'être.

*Intention d'origine* : « le message de bloc fermé est exposé au lecteur d'écran, avec un rôle valide ». **Conservée à l'identique** — c'est la structure de la fixture qui a changé, pas l'assertion.

`roles-aria.test.ts` exigeait que `components/ParcoursServeur.tsx` porte un rôle annonçant. Ce fichier ne contient plus de JSX ; le rôle est dans `app/parcours/BlocCarte.tsx`. La liste a été mise à jour, et un contrôle de région nommée sur la carte a été ajouté.

---

## 8. ACCESSIBILITÉ

| Exigence | État | Preuve |
|---|---|---|
| La liste des blocs est un `<section aria-labelledby>` pointant sur son titre | ✅ | `#titre-liste` — testé |
| Chaque bloc est une `<section>` avec son propre `aria-labelledby` | ✅ | `#titre-B1`, `#titre-B3`… — testé |
| Les pastilles d'état portent leur texte, pas seulement leur couleur | ✅ | « Ouvert », « Ouvre à la semaine 10 » — testé |
| Aucun rôle inexistant en ARIA | ✅ | HTML de production : seul `status` est présent, `role="note"` absent |
| Focus visible sur tous les liens d'exercice | ✅ | `Bouton.module.css` compose `focus` depuis `base.module.css` ; vérifié par `design/accessibilite.test.ts` |
| Cible tactile ≥ 44 px sur les liens d'exercice | ✅ | `--relio-tactile-min: 44px` appliqué par `.bouton`, hérité par `.lienExercice` |
| Contraste des bordures ≥ 3:1 | ✅ | `.secondary` utilise `--relio-bordure-forte` (3,66:1). **Avant**, la bordure venait de `.carte` (`#e2e5ef`, 1,26:1) |
| Le bandeau garde son rôle de région vivante | ✅ | `role="status"` — testé sur le HTML rendu |

**Ordre de tabulation** : les seuls éléments focusables sont les liens d'exercice et le lien « Retour à l'accueil ». Le `<header>`, les `<section>`, les `Carte`, les `Pastille` n'ont pas de `tabIndex`. Un élève clavier atteint donc le premier exercice par une seule tabulation depuis le début de la page.

---

## 9. CE QUI N'A PAS PU ÊTRE FAIT, ET POURQUOI

| Point | Raison |
|---|---|
| **Rendre le poids CSS sous le budget de +1,5 Ko** | L'écart mesuré est de **+0,32 Ko**. Réduire davantage supposait de couper des règles du module local — donc de dégrader l'écran — alors que le gain de 0,56 Ko est déjà identifié et mesuré pour le C2. Le chiffre est documenté plutôt que masqué par une dégradation |
| **Retirer les 39 classes mortes de `globals.css`** | Hors périmètre : `globals.css` est partagé avec `/parcours/[id]`, qui n'est pas migré par ce chantier. Le gain (0,56 Ko) est mesuré et reporté au C2 |
| **Vérification visuelle à 360 px** | Aucun navigateur, aucun appareil dans l'environnement. Contrôle limité au HTML rendu et aux règles CSS |
| **`/parcours/[id]`, `Exercice.tsx`, `ClavierMath.tsx`** | Chantier C2. Un test vérifie qu'ils sont restés intacts |
| **Contrôle du rendu réel de l'anneau de focus** | `accessibilite.test.ts` contrôle le CSS du design system de façon statique ; aucun rendu navigateur ne peut être observé ici |
| **`verifier:poids` branché dans la CI** | Décision humaine en attente, hors périmètre |
| **Le lien vers le logo « R » de l'en-tête** | L'accueil ne l'a pas. L'aligner serait plus cohérent, mais le chantier demande de ne pas changer le contenu : le logo est resté |

---

## 10. STATUT GLOBAL

# ⚠️

**Le chantier est fait et vérifié :** la migration est complète, aucune classe globale ne subsiste (contrôlé sur le HTML de production), les quatre états sont couverts par 60 nouveaux tests, `/parcours/[id]` et les composants du C2 sont intacts, et le poids JavaScript respecte le budget.

**Le seul point qui n'est pas au vert est le poids CSS : +1,82 Ko gzip pour un budget de +1,5 Ko, soit 0,32 Ko de dépassement.** La cause est identifiée et le gain compensant est mesuré — 0,56 Ko récupérables en retirant les 39 classes de `globals.css` devenues mortes, ce qui relève du chantier C2. Aucune dégradation visuelle n'a été appliquée pour faire rentrer le chiffre artificiellement.

Si le dépassement doit être absorbé dès maintenant plutôt qu'au C2, la seule option qui ne dégrade rien est d'anticiper cette suppression de classes mortes — ce qui sort du périmètre donné.