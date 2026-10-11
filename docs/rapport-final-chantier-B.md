# RAPPORT DE FIN DE CHANTIER B — REFONTE DE L'ACCUEIL SUR LE DESIGN SYSTEM

**Date :** 2026-10-11
**Dépôt :** `relio-frontend`
**Commit :** `92ddfb4`
**Nature :** première migration réelle sur le design system. Aucune fonctionnalité nouvelle, aucune dépendance ajoutée.

---

## 1. RÉSUMÉ

1. L'accueil affiche désormais l'**état réel** renvoyé par `GET /api/v1/parcours` : semaine en cours, bloc ouvert, titre du bloc, nombre d'exercices. Plus aucun état en dur.
2. Les cinq informations demandées sont présentes, dans l'ordre, au-dessus de la ligne de flottaison à 360 px : « Bonjour. », « Prépare ton BEPC de mathématiques », « Ta route cette semaine », « Ouvert », « Calcul littéral », « Semaine 5 sur 30 », « Continuer », « 10 min environ ».
3. Sept composants du design system sont utilisés : `Carte`, `Pastille`, `BarreProgression`, `EtatVide`, `Squelette`, `Icone`, `Bouton`. **Aucune classe globale** sur cet écran.
4. La section « État des fonctionnalités » et le fichier `components/parcours.ts` sont **supprimés**, pas déplacés. `ApiStatus` n'affiche plus l'adresse du backend.
5. Poids : **JS −0,10 Ko gzip**, **CSS +1,17 Ko gzip** sur la route `/`. Budget de +2 Ko respecté. Tests : 193 → 234 (+41), 0 échec.

---

## 2. DIFF DES FICHIERS

### Créés (5)

| Fichier | Lignes | Rôle |
|---|---|---|
| `src/app/CarteRoute.tsx` | 190 | La carte principale. **Composant pur** : reçoit l'état déjà résolu, ne fait aucun appel réseau. Contient aussi le repli de chargement. |
| `src/app/page.module.css` | 202 | Feuille locale de la page. Tokens `--relio-*` uniquement, aucune couleur brute, aucun px hors échelle. |
| `src/app/CarteRoute.test.tsx` | 253 | 18 tests : les quatre états de la carte. |
| `src/components/ApiStatus.module.css` | 20 | Ligne d'état du service. |
| `src/design/accueil-migration.test.ts` | 244 | 19 tests statiques : pas de classe globale, pas d'état en dur, pas d'URL backend, tokens respectés. |

### Modifiés (7)

| Fichier | Lignes | Modification |
|---|---|---|
| `src/app/page.tsx` | 126 | Refaite. `Bonjour.` + sous-titre + `<Suspense>` + carte + 3 étapes + pied de page. Suppression de `FONCTIONNALITES`, de `PARCOURS`, de `.entete`, des 4 sections. |
| `src/components/ApiStatus.tsx` | 78 | Passe de composant **client** à composant **serveur**. Devient une `Pastille` discrète. Plus d'URL, plus de carte à 5 états. |
| `src/app/page.test.tsx` | 129 | Réécrit : le bandeau d'avertissement n'existe plus, les contrôles portent sur le HTML rendu et sur le texte de confidentialité. |
| `src/design/roles-aria.test.ts` | 149 | La liste des fichiers portant un rôle annonçant passe de 3 à 2 (l'accueil n'a plus de bandeau). Ajout d'un contrôle de la région nommée. |
| `src/design/textes-affiches.test.ts` | 193 | `components/parcours.ts` remplacé par `app/CarteRoute.tsx` et `app/page.module.css`. |
| `src/lib/navigation.test.ts` | 240 | Deux tests réécrits (voir §7). |
| `vitest.config.mts` | 44 | Inchangé sur ce chantier (l'élargissement datait du chantier A). |

### Supprimé (1)

| Fichier | Lignes | Raison |
|---|---|---|
| `src/components/parcours.ts` | 49 | Les cinq étapes en dur. Elles annonçaient un état du service sans jamais le vérifier. |

**Total : 410 insertions, 378 suppressions, 5 fichiers créés, 1 supprimé.**

---

## 3. LES QUATRE ÉTATS DE LA CARTE PRINCIPALE

Mesurés sur le HTML réellement produit (`renderToReadableStream`, API réelle en production).

### État 1 — API disponible, bloc ouvert

```
Ta route cette semaine                        [Ouvert]

Calcul littéral

Semaine 5 sur 30
▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░

[          Continuer          ]
10 min environ · 6 exercices
```

- `Pastille ton="succes"` portant le texte « Ouvert »
- Titre du bloc **issu de l'API** (`bloc.titre`), jamais reconstruit localement
- `BarreProgression` : `role="progressbar"`, `aria-valuenow="17"` (5/30), `aria-valuemin="0"`, `aria-valuemax="100"`, `aria-label="Semaine 5 sur 30"`
- `<Link href="/parcours/MVP-B1-E1">` stylé avec `Bouton.module.css` — **un vrai lien**, pas un `button`
- Durée : `dureeEstimeeMinutes(6)` → `10 min environ`

**Texte rendu en production (serveur `next start` contre l'API réelle) :**
```
Relio — Préparation BEPC Mathématiques Bonjour. Prépare ton BEPC de
mathématiques. Ta route cette semaine Ouvert Calcul littéral Semaine 5
sur 30 Continuer 10 min environ · 6 exercices Comment ça marche Tu lis
la notion Une leçon courte, écrite simplement, avant de commencer. Tu
t'entraînes Des exercices qui correspondent à ce que tu viens de voir.
Tu comprends tes erreurs Chaque réponse est expliquée, pour que tu
progresses vraiment. Aucun contenu d'épreuve officielle n'est reproduit
… Service disponible
```

### État 2 — API disponible, aucun bloc ouvert

```
Ta route cette semaine

  ℹ   Aucun bloc n'est ouvert pour l'instant
      Calcul numérique ouvre à la semaine 10. Reviens à cette date.

      Semaine 5 sur 30
      ▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
```

`EtatVide` avec `icone="info"`, message bienveillant et date d'ouverture du **prochain** bloc (le plus petit `semaineDebut` parmi les blocs fermés). **Aucun bouton « Continuer »** : il n'y a rien à faire, et un bouton qui ne mène nulle part est un cul-de-sac.

### État 3 — API injoignable

```
Ta route cette semaine

  ℹ   Ton parcours arrive dans un instant
      Le service n'a pas répondu. La page fonctionne ;
      seul le parcours est en attente.

      [ Réessayer ]
```

`EtatVide` + `<form action="/" method="get"><Bouton type="submit">Réessayer</Bouton></form>`.

Le `raison` technique renvoyé par `chargerParcours` (« Le service ne répond pas. Réessaie dans un instant. ») **n'est pas affiché** : il est remplacé par un message qui dit ce qui marche encore. Un élève ne peut rien faire d'un message d'erreur réseau ; il peut réessayer.

Le bouton est un formulaire, pas un `onClick` : **il fonctionne sans JavaScript**.

### État 4 — Chargement

```
Ta route cette semaine

  ▬▬▬▬▬▬▬▬▬▬
  ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
  ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
```

Trois `Squelette` (`aria-hidden="true"`) dans une `Carte` de même hauteur que la carte réelle. Le titre est **identique** — vérifié par test — donc rien ne saute à l'arrivée des données.

C'est le `fallback` du `<Suspense>` : le HTML part immédiatement, sans attendre les 8 s du délai réseau.

---

## 4. POIDS JS ET CSS (mesuré)

Mesure par fichier, gzip niveau 9, sur `.next/app-build-manifest.json` — deux builds comparés, l'un à `92ddfb4^`, l'autre à `92ddfb4`.

| Route `/` | Avant | Après | Écart |
|---|---|---|---|
| **JS gzip** | 104,94 Ko | **104,84 Ko** | **−0,10 Ko** |
| **CSS gzip** | 0,00 Ko | **4,60 Ko** | **+4,60 Ko** |

Détail du CSS de l'accueil : `ac0b1b059acd05c7.css` = 3,30 Ko (tokens + globals, déjà là) · `f2c19aba335fa1d2.css` = **1,17 Ko** (module de page + modules des composants DS) · `3f32e8f669699ef2.css` = 0,14 Ko.

**Écart réel sur l'accueil : +1,17 Ko de CSS.** Le reste du CSS était déjà chargé par le layout.

Ce qui est demandé : « ne pas dépasser de plus de 2 Ko gzip le poids actuel (107 Ko JS, 6,97 Ko CSS) ».

| Contrainte | Mesure | Verdict |
|---|---|---|
| JS de `/` | −0,10 Ko | ✅ |
| CSS ajouté à `/` | +1,17 Ko | ✅ |
| Budget CSS global (30 Ko) | 6,97 → **8,00 Ko** | ✅ marge de 22 Ko |

Sortie de `next build` :

```
Route (app)                                 Size  First Load JS
┌ ƒ /                                    1.3 kB         107 kB     ← avant : 1.41 kB / 107 kB
├ ○ /_not-found                            993 B         104 kB
├ ƒ /design-system                       10.6 kB         113 kB
├ ƒ /parcours                              160 B         106 kB
└ ƒ /parcours/[id]                        5.8 kB         112 kB
+ First Load JS shared by all             103 kB
```

`$ npm run verifier:poids`
```
  42947774f408bb39.css — 17.2 Ko -> 3.5 Ko gzip
  f2c19aba335fa1d2.css — 4.0 Ko -> 1.2 Ko gzip
  cb3ebbbccb56dffb.css — 13.5 Ko -> 3.4 Ko gzip

Total CSS : 34.0 Ko bruts -> 8.0 Ko gzip
Budget    : 30 Ko gzip — marge restante 22.0 Ko
OK
```

### Ce qui a coûté du poids, et pourquoi c'est un gain

La première version mesurait **+3,67 Ko gzip de JavaScript**. La cause : `ApiStatus` était un composant client, il importait `Bouton`, qui importe `Icone` — et le barrel `@/components/ds` entraînait le mapping CSS de tout le catalogue (`Avatar`, `Puce`, `Toast`, `Feuille`…). Tout cela partait au navigateur pour un composant qui n'a **aucune interaction** : il affiche une pastille.

Deux décisions ont ramené le coût à zéro :

1. `ApiStatus` devient un composant **serveur**. L'accueil interroge déjà l'API côté serveur pour la carte ; la seconde vérification, faite depuis le navigateur, était redondante.
2. Les imports passent par le chemin direct (`@/components/ds/Bouton`) plutôt que par le barrel `@/components/ds`. Le barrel reste utile pour les tests, mais il ne doit pas entrer dans un graphe client.

---

## 5. COMPOSANTS DU DESIGN SYSTÈME UTILISÉS

Sept, tous importés par leur chemin direct.

| Composant | Où | Rôle sur l'accueil |
|---|---|---|
| `Carte` | carte principale, 3 cartes d'étape | Surface de regroupement. `variante="elevee"` sur la carte principale pour qu'elle se détache du fond |
| `Pastille` | état du bloc, état du service | « Ouvert » en `succes`, « Service disponible » / « Service injoignable », « Service non configuré ». **Porte son texte** — une couleur seule n'est pas une information |
| `BarreProgression` | position dans l'année | `role="progressbar"` + les trois attributs ARIA. Valeur = semaine / 30, **jamais un score** |
| `EtatVide` | aucun bloc ouvert, API injoignable | Message + action de sortie, comme le veut le contrat du composant |
| `Squelette` | repli de chargement | Trois blocs de la forme de la carte |
| `Icone` | trois étapes, `EtatVide` | SVG inline, aucune image bitmap |
| `Bouton` | « Réessayer » ×2 | `variante="secondary"` sur la carte, `variante="ghost"` sur l'état du service |

**`Bouton.module.css` est importé directement** dans `CarteRoute.tsx` pour styler le `<Link>` « Continuer » : même feuille, mêmes tokens, aucune seconde définition de bouton à maintenir. C'est la seule façon d'avoir à la fois un vrai lien et l'apparence du composant.

### Ce qui n'a pas été supprimé de `globals.css`

Les classes `.entete`, `.section`, `.grille`, `.carte`, `.bouton` **restent dans `globals.css`** : les écrans `/parcours` et `/parcours/[id]` s'en servent encore, et ce chantier ne les reprend pas. Elles ne sont simplement **plus utilisées par l'accueil**, ce qu'un test statique verrouille.

`layout.tsx` continue donc d'importer `globals.css` — il le faut pour les deux autres écrans. Conséquence mesurée : 3,30 Ko de CSS non migré sont encore servis sur l'accueil. **C'est le reliquat du chantier C**, et il est assumé.

---

## 6. TESTS AJOUTÉS ET RÉSULTAT

### `src/app/CarteRoute.test.tsx` — 18 tests

Quatre états, deux раза par état.

| État | Tests |
|---|---|
| **1 — bloc ouvert** | titre de carte · pastille « Ouvert » portée par son texte · « Semaine 5 sur 30 » · `role="progressbar"` avec `aria-valuenow=17` · le bouton est un `href="/parcours/MVP-B1-E1"` · durée affichée · `<section aria-labelledby>` · **aucun pourcentage de réussite dans le texte** |
| **2 — aucun bloc ouvert** | `EtatVide` présent · date d'ouverture annoncée · **pas de bouton « Continuer »** · position dans l'année conservée |
| **3 — API injoignable** | message bienveillant · **le motif technique n'est pas affiché** · bouton `type="submit"` dans un formulaire `GET /` · ni bloc, ni « Continuer », ni progression |
| **4 — chargement** | squelette présent · squelette `aria-hidden` · **aucun bouton actif, aucun faux bloc** · la mise en forme du titre est identique à la carte réelle |

### `src/design/accueil-migration.test.ts` — 19 tests

| Groupe | Ce qui est verrouillé |
|---|---|
| Aucune classe globale | Les 3 fichiers de l'accueil n'utilisent aucune des 13 classes de `globals.css` · `page.tsx` n'importe pas `globals.css` · l'accueil utilise bien un module local et le design system |
| Pas de retour du parcours en dur | « État des fonctionnalités » absente de **toute** `src/` · `components/parcours.ts` **n'existe plus** · plus de `FONCTIONNALITES` ni d'`etat: 'Disponible'` · `chargerParcours` est importé |
| L'adresse ne sort pas du serveur | Aucun rendu visible de `baseUrl` / `apiBaseUrl` dans le JSX · aucun `'use client'` dans les 3 fichiers · l'adresse n'est transmise **que** par prop (2 occurrences) |
| Tokens | Aucune couleur hexadécimale en dur · toute couleur vient de `var(--relio-…)` · aucune mesure hors échelle 4/8/12/16/24/32/48/64 · points de rupture limités à `{360, 420, 768}` |

### `src/app/page.test.tsx` — 11 tests

Contrôles sur le **HTML rendu** (`renderToReadableStream`, qui gère les composants serveur `async` — le runtime de rendu client des tests ne le fait pas).

- Le contenu est produit · aucun rôle qui n'existe pas en ARIA
- La carte principale est `<section aria-labelledby>` dont l'`id` pointe bien sur son `<h2>`
- **L'adresse du backend n'apparaît pas dans le HTML** (contrôlé avec une API fonctionnelle ET une URL witness)
- « Continuer » est un `<a href="/parcours/…">`, pas un `<button>`
- **La page reste utilisable quand l'API ne répond pas** : « Bonjour. », « Comment ça marche » et « Réessayer » sont tous présents
- Les 5 contrôles de texte du chantier A sont conservés tels quels

### Résultat

| Suite | Avant | Après | Écart |
|---|---|---|---|
| Frontend UI (Vitest) | 193 | **234** | **+41** |
| Frontend logique (`node --test`) | 119 | **119** | 0 |
| **Total frontend** | 312 | **353** | **+41** |

`tsc --noEmit` : exit 0. `next build` : exit 0. `npm run verifier:poids` : OK.

### Vérification « échouait avant »

`accueil-migration.test.ts` sur le code d'origine (`page.tsx` et `ApiStatus.tsx` restaurés, `parcours.ts` remis) :

```
  × app/page.tsx n’utilise aucune classe de globals.css
  × components/ApiStatus.tsx n’utilise aucune classe de globals.css
  × l’accueil utilise bien des modules CSS locaux ou du design system
  × « État des fonctionnalités » a disparu de toute la source
  × le fichier `components/parcours.ts` n’existe plus
  × la page ne déclare plus de liste de fonctionnalités en dur
  × la seule source de vérité du parcours est l’API
  × l’adresse n’est transmise que par prop, jamais rendue
  × l’API n’est jamais appelée depuis le navigateur pour cette page
  Tests  9 failed | 10 passed (19)
```

---

## 7. DEUX TESTS DU CHANTIER A ONT DÛ ÊTRE RÉÉCRITS

Ils verrouillaient la structure de l'ancien accueil. Ils sont signalés ici parce que modifier un test est toujours un risque — ce qu'ils contrôlaient est donc conservé, pas supprimé.

**`navigation.test.ts` — « la page d'accueil contient un lien vers le parcours »**

Il exigeait le libellé « Voir le parcours » et `href="/parcours"`. Le bouton s'appelle désormais « Continuer » et pointe vers `/parcours/MVP-B1-E1`.

*Intention d'origine* : l'accueil donne accès au parcours — c'était le défaut du chantier 7.1, où le bouton avait disparu. **Conservé** : le test vérifie qu'il existe un lien `href` vers `/parcours`, chaîne littérale ou gabarit. Seule la forme a changé.

**`navigation.test.ts` — « la page d'état des fonctionnalités reste accessible et séparée »**

Il exigeait que la section existe mais vienne **après** le parcours, pour ne pas donner l'impression que l'état technique est la destination.

*Intention d'origine* : « la destination principale est le parcours, pas un état technique ». **Conservée, et satisfaite plus fortement** : la section n'existe plus du tout. Le test vérifie désormais son absence, la présence de la carte principale, et l'absence des libellés « Disponible » / « Bientôt ».

**`roles-aria.test.ts`** exigeait que `app/page.tsx` porte un rôle annonçant. L'accueil n'a plus de bandeau. La liste est passée de 3 à 2 fichiers ; un contrôle a été ajouté sur la région nommée de la carte.

**`textes-affiches.test.ts`** listait `components/parcours.ts` dans ses modules contrôlés — le fichier n'existe plus. Remplacé par `app/CarteRoute.tsx` et `app/page.module.css`.

---

## 8. ACCESSIBILITÉ

| Exigence | État | Preuve |
|---|---|---|
| La carte principale est un `<section>` avec `aria-labelledby` pointant sur son titre | ✅ | `CarteRoute.tsx` — testé sur le HTML rendu |
| « Continuer » est un vrai lien, pas un `button` + `router.push` | ✅ | `<Link href>` — testé (`a[href^="/parcours/"]`) |
| La `Pastille` porte son texte, pas seulement sa couleur | ✅ | « Ouvert », « Service disponible » — testé |
| La `BarreProgression` a `role="progressbar"` + `aria-valuenow` | ✅ | `aria-valuenow="17"`, `valuemin=0`, `valuemax=100` — testé |
| Le bouton principal est atteignable en moins de 5 tabulations | ✅ | Voir ci-dessous |
| Aucun rôle inexistant en ARIA | ✅ | 0 occurrence de `role="note"` — testé sur `src/` et sur le HTML rendu |
| Contraste AA | ✅ | Contrôlé par `design/tokens.test.ts` (21 tests) — aucun couleur brute introduite |
| Cible tactile ≥ 44 px | ✅ | `--relio-tactile-min: 44px` appliqué par `Bouton.module.css` |
| Focus visible | ✅ | `Bouton.module.css` compose `focus` depuis `base.module.css` |

**Ordre de tabulation sur l'accueil.** Les seuls éléments focusables avant le bouton principal sont : le `<a>` « Continuer ». Le `<header>`, les `<section>`, les `Carte`, la `Pastille` et la `BarreProgression` sont des `div`/`section` sans `tabIndex` — ils ne prennent donc pas le focus. Le bouton principal est **le premier élément focusable de la page** : 1 tabulation. Exigence : moins de 5. ✅

**Le « Réessayer » de la carte est un formulaire `GET`** — il est au clavier et fonctionne sans JavaScript, ce qu'un `onClick` n'aurait pas garanti.

---

## 9. CE QUI N'A PAS PU ÊTRE FAIT, ET POURQUOI

| Point | Raison |
|---|---|
| **Vérifier l'affichage à 360 × 640 px sur un écran réel** | Aucun appareil, aucun émulateur, aucun navigateur dans l'environnement. L'estimation ci-dessous est **calculée**, pas mesurée. Aucun rendu par pixel n'a pu être fait |
| **Les cinq secondes de compréhension ne sont pas mesurables ici** | C'est une mesure de temps passé par un humain réel sur un écran réel. Ce que le chantier garantit, c'est que les cinq informations sont présentes, dans l'ordre, au-dessus de la ligne de flottaison — pas qu'elles sont comprises en cinq secondes |
| **L'état « Terminé » de la pastille n'existe pas** | Il est mentionné dans la demande, mais **aucune donnée ne permet de le déterminer** : le suivi de progression est local à l'appareil et n'est pas remonté au serveur. Afficher « Terminé » sans donnée serait inventer un état — ce que ce chantier refuse par principe. Les deux états réellement possibles sont « Ouvert » et l'« Ouvre dans X semaines » |
| **La durée « 10 min » est une estimation, pas une mesure** | L'API ne renvoie aucune durée et le temps passé par un élève n'est pas connu. La formule est `max(5, round(nbExercices × 2 / 5) × 5)`, documentée comme estimation dans le code. Le mot « environ » est affiché à l'élève |
| **`SEMAINES_PAR_ANNEE = 30` duplique une donnée du serveur** | L'API renvoie la semaine en cours mais pas la longueur de l'année. L'écran doit dire « Semaine 5 sur 30 » sans ajouter d'aller-retour. C'est **la seule donnée de la page qui ne vient pas de l'API**, et le commentaire signale où elle doit être changée si le serveur la modifie. Aucun contrôle automatisé ne lie les deux valeurs |
| **Les écrans `/parcours` et `/parcours/[id]` ne sont pas repris** | Hors périmètre : c'est le chantier C. Ils continuent d'utiliser `globals.css`, ce qui explique les 3,30 Ko de CSS non migrés encore servis sur l'accueil |
| **`lib/api.ts` est moins utilisé qu'avant** | `verifierApi` n'est plus appelé depuis le navigateur, mais il l'est désormais côté serveur par `ApiStatus`. Ses 13 tests restent valides. Aucun code n'est devenu orphelin |
| **`verifier:poids` n'est pas branché dans la CI** | Décision humaine en attente, hors périmètre |
| **Le mode sombre n'est pas vérifié sur cet écran** | `tokens.css` déclare un mode sombre complet, et l'accueil l'utilise désormais — c'est un gain. Mais aucun rendu n'a pu être contrôlé dans ce mode, faute de navigateur |

### Estimation de la hauteur à 360 px

Calculée à partir des tokens et de l'échelle, **pas mesurée sur un écran** :

| Élément | Estimation |
|---|---|
| Padding haut du conteneur | 24 px |
| Padding haut du bandeau | 24 px |
| « Bonjour. » (24 px × 1,2) | 29 px |
| Marge + « Prépare ton BEPC de mathématiques » | 28 px |
| Marge basse du bandeau | 24 px |
| **Sous-total avant la carte** | **≈ 136 px** |
| Carte : titre + titre du bloc + barre + bouton + durée + padding | ≈ 226 px |
| **Total avant le bas du bouton** | **≈ 362 px** |

Écran de référence : 640 px de haut. Le bouton « Continuer » se termine vers **362 px**, soit 278 px de marge restante. « Comment ça marche » et l'état du service sont bien en dessous de la ligne de flottaison, comme demandé.

---

## 10. STATUT GLOBAL

# ✅

**Le chantier est fait : l'accueil est bâti sur sept composants du design system, sans aucune classe globale, et il affiche l'état réel renvoyé par l'API au lieu d'un parcours marketing figé dans le code.**

Les deux budgets sont respectés sans dépassement — le JavaScript a même **diminué** de 0,10 Ko gzip, parce que la vérification du service a quitté le navigateur alors que la carte l'avait déjà fait côté serveur. Les 41 tests ajoutés couvrent les quatre états de la carte et les trois contraintes statiques demandées ; deux tests du chantier A ont dû être réécrits parce qu'ils verrouillaient une structure supprimée, et leur intention d'origine est conservée.

**Réserve principale :** le rendu à 360 × 640 px est une **estimation calculée**, pas une mesure sur appareil — aucun téléphone, aucun navigateur n'est disponible dans cet environnement. La prochaine vérification utile est un coup d'œil sur un vrai écran.

**Non traité, par conception :** l'état « Terminé » de la pastille, qui exigerait des données de progression que le serveur ne possède pas ; et la migration de `/parcours` et `/parcours/[id]`, qui est le chantier suivant.