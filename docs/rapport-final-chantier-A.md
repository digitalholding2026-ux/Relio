# RAPPORT DE FIN DE CHANTIER A — CORRECTIFS CRITIQUES

**Date :** 2026-10-11
**Périmètre :** `relio-frontend` (9 fichiers modifiés, 7 créés) et `relio-backend` (1 fichier modifié, 1 créé)
**Source :** `AUDIT_RELIO.md`, rendu et poussé en `73337d3`
**Nature :** correctifs uniquement. Aucune fonctionnalité nouvelle, aucune migration vers le design system, aucun refactor hors correctif.

---

## 1. RÉSUMÉ EXÉCUTIF

Les **8 correctifs** demandés sont appliqués et vérifiés. Chacun porte un test qui échouait sur le code d'origine et passe maintenant — état vérifié par exécution réelle du `git stash` sur le fichier corrigé, pas par relecture.

**Résultats de mesure :**

| Indicateur | Avant | Après |
|---|---|---|
| Tests backend | 307 | **317** (+10) |
| Tests frontend logique (`node --test`) | 119 | **119** (inchangé) |
| Tests frontend UI (Vitest) | 136 | **193** (+57) |
| Total tests | 562 | **629** (+67) |
| Échecs | 0 | **0** |
| Typecheck backend / frontend | ✅ | ✅ |
| Build backend / frontend | ✅ | ✅ |
| `npm audit` | 0 vulnérabilité | 0 vulnérabilité |
| Budget CSS (30 Ko gzip) | 6,98 Ko | **7,00 Ko** |

**Correctif 1** — les 25 touches du clavier mathématique sont désormais actionnables au clavier physique, au commutateur et à toute technologie d'assistance. Le tactile ne double plus l'action : un `click` porteur d'un point d'appui est identifié par `detail > 0` et ignoré, sans minuteur ni état.
**Correctif 2** — `.bouton` n'est plus déclaré qu'une fois. Le bouton « Voir le parcours » s'affiche bleu au repos et bleu foncé au survol, au lieu de blanc au repos et bleu au survol.
**Correctif 3** — `--bordure-forte: #7c85a3` (3,66:1 sur blanc) appliqué au champ de saisie et aux touches du clavier. Le champ était à 1,26:1.
**Correctif 4** — les trois `role="note"` deviennent `role="status"`. Ces bandeaux sont enfin annoncés.
**Correctif 5** — le pied de page n'affirme plus que les réponses ne sont pas conservées.
**Correctif 6** — `/design-system` passe de `○` (prérendu en erreur) à `ƒ` (dynamique). La variable `DESIGN_SYSTEM_ENABLED` redevient pilotante.
**Correctif 7** — deux fautes corrigées : « Le service de exercices » et « APIRelio ». 132 chaînes affichées relues.
**Correctif 8** — `ANNEE_SCOLAIRE_DEBUT` et `DATE_NAVIGATION_TEST` documentées, avec l'avertissement sur le risque de figeage en production.

---

## 2. TABLEAU « CORRECTIF | FICHIER | LIGNE | TEST AJOUTÉ | STATUT »

| # | Correctif | Fichier | Ligne | Test ajouté | Échouait avant | Statut |
|---|---|---|---|---|---|---|
| 1 | Clavier mathématique actionnable au clavier | `src/components/ClavierMath.tsx` | 167-176 (`surPointerDown`), 178-186 (`surClick`), 191-192 (câblage) | `src/components/ClavierMath.test.tsx` — 14 tests | **9 échouaient** | ✅ |
| 2 | `.bouton` déclaré une seule fois | `src/app/globals.css` | 303-353 (fusion ; ancienne l.477 supprimée) | `src/design/globals-applicatif.test.ts` — 3 tests dédiés | **3 échouaient** | ✅ |
| 3 | `--bordure-forte` sur champ et clavier | `src/app/globals.css` | 16 (définition), 503-513 (`.exercice__saisie`), 641 (`.clavier__touche`) | `src/design/globals-applicatif.test.ts` — 5 tests dédiés | **5 échouaient** | ✅ |
| 4 | `role="note"` → `role="status"` | `src/app/page.tsx:97` · `src/app/parcours/page.tsx:50` · `src/components/ParcoursServeur.tsx:68` | idem | `src/design/roles-aria.test.ts` (5, statique) · `src/components/ParcoursServeur.test.tsx` (4, rendu) · `src/app/page.test.tsx` (3, rendu) | **10 échouaient** | ✅ |
| 5 | Texte exact sur la conservation des réponses | `src/app/page.tsx` | 177-182 | `src/app/page.test.tsx` — 5 tests | **5 échouaient** | ✅ |
| 6 | `/design-system` en rendu dynamique | `src/app/design-system/page.tsx` | 51 (`export const dynamic = 'force-dynamic'`) | `src/design/design-system-garde.test.ts` — 5 tests | **3 échouaient** | ✅ |
| 7 | Faute d'accord et mot collé | `src/lib/parcours.ts:139` · `src/components/ApiStatus.tsx:49` | idem | `src/design/textes-affiches.test.ts` — 10 tests | **3 échouaient** | ✅ |
| 8 | Variables calendrier documentées | `backend/.env.example` | 23-47 | `backend/test/env-example.test.ts` — 10 tests | **7 échouaient** | ✅ |
| — | Élargissement du périmètre Vitest (indispensable au correctif 5) | `vitest.config.mts` | 42-47 | — | — | ✅ |

**Bilan : 45 tests échouaient avant correction sur le périmètre des 8 correctifs ; les 629 tests passent après.**

---

## 3. DÉTAIL PAR CORRECTIF

### CORRECTIF 1 — Clavier mathématique inutilisable au clavier physique

**Diagnostic.** Les touches sont des `<button type="button">`. Le navigateur déclenche un `click` sur `Entrée` et sur `Espace` ; seul `onPointerDown` était écouté. Aucune des 25 touches n'était donc actionnable au clavier physique, au commutateur d'accès ou à une technologie d'assistance.

**Choix retenu.** Deux gestionnaires distincts, une seule action :

```ts
// tactile et souris — doit précéder le click pour ne pas perdre le curseur
const surPointerDown = useCallback((evenement, action) => {
  evenement.preventDefault();
  appuyer(action);
}, [appuyer]);

// clavier, commutateur, technologies d'assistance
const surClick = useCallback((evenement, action) => {
  if (evenement.detail > 0) return;
  appuyer(action);
}, [appuyer]);
```

**Pourquoi `detail > 0` et non un drapeau à minuteur.** Un `click` produit depuis le clavier porte toujours `detail === 0` : le navigateur ne compte aucun point d'appui. Un `click` issu d'un doigt, d'une souris ou d'un stylet porte `detail >= 1`. Cette propriété permet d'ignorer le doublon `pointerdown` + `click` sans aucun état à raisonner, **et sans minuteur** — donc sans le risque qu'un minuteur reste armé et avale la frappe clavier suivante si un `click` n'arrive jamais.

**Ce qui est conservé.** `preventDefault()` sur `pointerdown` est maintenu : c'est lui qui empêche le champ de perdre le focus — et le curseur avec — sur Android. Le comportement tactile est donc inchangé.

**Ce qui ne l'est pas, et pourquoi c'est mieux.** La saisie au curseur reste pilotée par l'`<input>` natif ; l'insertion au milieu n'a pas bougé (3 tests le vérifient).

**Tests ajoutés** — `src/components/ClavierMath.test.tsx`, 14 tests :

| Test | Ce qu'il prouve |
|---|---|
| « une touche déclenche l'action au clic clavier (Entrée) » | `Vérifier ma réponse` actionnable |
| « une touche déclenche l'action au clic clavier (Espace) » | une frappe numérique modifie la saisie |
| « la touche Masquer est actionnable au clavier » | `Masquer` actionnable |
| « la touche Clavier système est actionnable au clavier » | `Clavier système` actionnable |
| « chaque touche du service est actionnable au clavier » | les 3 touches de service, sur le clavier |
| « le pointerdown exécute l'action » | réactivité tactile conservée |
| « le pointerdown empêche le comportement natif » | `defaultPrevented === true` |
| « pointerdown suivi de click n'exécute l'action qu'une seule fois » | pas de doublon, valeur `7` et curseur `1` |
| « pointerdown puis deux clicks n'exécute toujours l'action qu'une fois » | pas d'accumulation |
| « un click porteur d'un point d'appui est ignoré » | le contrat anti-doublon est explicite |
| « après un pointerdown, un clic clavier ultérieur fonctionne normalement » | le clic clavier n'est pas confondu avec un doublon |
| « insère au milieu de la saisie, pas seulement à la fin » | non-régression : `12` + `7` au curseur 1 → `172` |
| « la touche effacer vide la saisie » | non-régression |
| « la touche fraction insère la barre au curseur » | non-régression |

**Vérification « échouait avant » :**

```
$ git stash push -- src/components/ClavierMath.tsx && npx vitest run …
  × déclenche l'action au clic clavier (Entrée)
  × déclenche l'action au clic clavier (Espace)
  × la touche Masquer est actionnable au clavier
  × la touche Clavier système est actionnable au clavier
  × chaque touche du service est actionnable au clavier
  × après un pointerdown, un clic clavier ultérieur fonctionne normalement
  × insère au milieu de la saisie, pas seulement à la fin
  × la touche « effacer » vide la saisie
  × la touche « fraction » insère la barre au curseur
  Tests  9 failed | 5 passed (14)
```

---

### CORRECTIF 2 — Bouton principal cassé sur l'accueil

**Diagnostic.** `.bouton` était déclaré à la l.303 (fond bleu, texte blanc) puis à la l.477 (fond blanc, texte noir). Spécificité égale (0,1,0) : la seconde écrasait la première. `.bouton--principal` (offset 8275) était sandwichné entre les deux, donc également écrasé.

**Correction.** Les deux déclarations sont fusionnées en une seule à la l.325. La base est **neutre** (`--surface`, `--texte`) : c'est le bouton le plus fréquent dans l'application (les actions de l'exercice, « Revérifier »). La couleur d'accent est le rôle explicite de `.bouton--principal`, qui n'a de sens que sur un bouton qu'on veut pousser à cliquer. Le survol de `.bouton--principal` assombrit le fond au lieu de l'éclaircir : passer du bleu au bleu pâle se lirait comme une désactivation.

**Éléments dépendant de la première déclaration :** vérifié. Les six usages de `.bouton` sont `bouton--principal` (×2), `bouton--secondaire`, `bouton--discret`, et `bouton` seul (×2, actions secondaires de l'exercice). Aucun ne depended de `border-radius: 10px` ni de `font-size: 0.9rem`. Les valeurs retenues (`min-height: 48px`, `1rem`, `var(--rayon)`) viennent du second bloc et sont conservées. `font-weight: 650` est conservé du premier : il n'était repris nulle part.

### PREUVE — extrait du CSS compilé

```
$ node -e "…recherche des règles .bouton dans .next/static/css/*.css…"

cb3ebbbccb56dffb.css -> .bouton de base : 1
  offset 7380 :: .bouton{-webkit-appearance:none;-moz-appearance:none;appearance:none;
                   min-height:48px;padding:0 1.1rem;
                   border:1px solid var(--bordure-forte);
                   border-radius:var(--rayon);
                   background:var(--surface);color:var(--texte);…}

   toutes règles .bouton* : 8
     - .bouton{-webkit-appearance:none;…}
     - .bouton:hover:not(:disabled){border-color:var(--primaire-sombre);back…
     - .bouton:disabled{opacity:.55;cursor:not-allowed}.bouton--secondaire{b…
     - .bouton--secondaire{background:var(--surface);color:var(--primaire-so…
     - .bouton--secondaire:hover:not(:disabled){background:var(--primaire-do…
     - .bouton--principal{background:var(--primaire);color:#fff;border-color…
     - .bouton--principal:hover:not(:disabled){background:var(--primaire-som…
     - .bouton--discret{padding:.35rem .7rem;font-size:.85rem;color:var(--te…
```

**Une seule règle `.bouton` de base**, contre 2 auparavant. Ordre des règles vérifié : `.bouton` (7380) puis `.bouton--principal` (8364) — le modificateur est bien appliqué après la base. Le hash du fichier CSS change (`c5b3424d1cf8f1d7` → `cb3ebbbccb56dffb`), cohérent avec la modification du contenu.

---

### CORRECTIF 3 — Contraste des bordures de champ et de clavier

**Diagnostic.** `--bordure: #e2e5ef` valait **1,26:1** sur `#ffffff`. Elle servait aussi bien aux séparateurs décoratifs qu'au champ de saisie et aux touches du clavier — c'est-à-dire à des éléments qui doivent être repérables avant d'être focalisés.

**Correction.** Deux tokens, comme dans le design system qui avait déjà résolu le problème :

| Token | Valeur | Usage |
|---|---|---|
| `--bordure` | `#e2e5ef` (inchangée) | séparateurs décoratifs : `.pied`, `.carte`, `.verdict` |
| `--bordure-forte` | `#7c85a3` (nouveau) | `.exercice__saisie`, `.clavier__touche`, `.bouton` |

### RATIO DE CONTRASTE MESURÉ

Calculé avec `rapportContraste()` de `src/design/contraste.ts` (formule WCAG 2.1 exacte), exécuté dans cette session :

```
--bordure-forte #7c85a3 sur #ffffff : 3.66:1   ✅ ≥ 3:1, et ≥ 3,5:1
--bordure-forte #7c85a3 sur #f7f8fc : 3.45:1   ✅ ≥ 3:1
ancienne --bordure  #e2e5ef sur #ffffff : 1.26:1   ❌
```

Le seuil visé (3,5:1) est atteint sur fond blanc, et le seuil WCAG 2.1 SC 1.4.11 (3:1) est atteint sur les deux fonds réellement utilisés par l'application. `#7c85a3` reste dans la famille bleutée du thème : la bordure ne devient pas un trait gris détaché de la palette.

La bordure des touches de service (`.clavier__touche--fermer`, `--systeme`, `--retour`, `--effacer`) hérite du nouveau token par cascade. La touche `--valider` conserve `border-color: var(--primaire)`, inchangé : son fond est déjà bleu.

---

### CORRECTIF 4 — `role="note"` n'existe pas en ARIA

**Diagnostic.** `role="note"` a été employé trois fois. Ce rôle **n'existe pas** dans la spécification ARIA : un lecteur d'écran ignore l'attribut, et les trois bandeaux n'étaient jamais annoncés.

**Correction.** `role="status"` dans les trois cas. Ce sont des messages d'information sur le périmètre du produit, pas des erreurs bloquantes : `status` implique `aria-live="polite"` et `aria-atomic="true"`, donc le message est lu sans interrompre la navigation en cours. `role="alert"` aurait été le mauvais choix — il interrompt.

| Emplacement | Contenu | Rôle retenu |
|---|---|---|
| `app/page.tsx:97` | « Première version. Le parcours couvre trois leçons… » | `status` |
| `app/parcours/page.tsx:50` | « Ces exercices donnent une première idée de tes acquis… » | `status` |
| `components/ParcoursServeur.tsx:68` | « Disponible à partir de la semaine N. » / « Ce bloc n'est pas encore ouvert. » | `status` |

**Tests ajoutés** — deux niveaux complémentaires :

*`src/design/roles-aria.test.ts` (5 tests, contrôle statique)* — porte sur le code source, seule façon d'atteindre les pages serveur et les composants serveur asynchrones :
- aucun `role="note"` ne subsiste dans `src/`
- tous les rôles utilisés appartiennent à la spécification ARIA 1.2
- aucun rôle **abstrait** n'est porté par un élément
- les trois fichiers portent bien un rôle annonçant

*`src/components/ParcoursServeur.test.tsx` (4 tests, rendu)* — vérifie que le rôle **existe dans le DOM**, ce qu'un attribut invalide ne fait pas : c'est la différence entre « l'attribut est valide » et « le lecteur d'écran voit une région ».

*`src/app/page.test.tsx` (3 tests, rendu)* — même vérification pour la page d'accueil.

---

### CORRECTIF 5 — Message affiché factuellement faux

**Diagnostic.** Le pied de page affirmait « Aucune donnée personnelle n'est collectée, et tes réponses ne sont pas conservées. » La seconde phrase est fausse côté client : les réponses sont conservées dans `localStorage` (jusqu'à 500 entrées, `relio.observations.v1`) et le journal complet est transmis au serveur à chaque tentative via `POST /api/v1/suivi`.

**Correction** — 3 phrases, français simple, aucun terme technique :

> Aucun contenu d'épreuve officielle n'est reproduit, et aucune donnée personnelle n'est collectée. Tes réponses sont enregistrées sur ton appareil pour te permettre de suivre ta progression ; tu peux les effacer à tout moment, et rien n'est conservé de ton parcours sur nos serveurs.

**Choix de formulation, justifiés :**

| Formulation | Raison |
|---|---|
| « sur ton appareil » | dit la vérité sans employer `localStorage`, `navigateur` ou `serveur` dans la première phrase |
| « pour te permettre de suivre ta progression » | donne la raison ; la suppression pure et simple serait une perte |
| « tu peux les effacer à tout moment » | reprend le bouton « Effacer mon historique » qui existe déjà dans l'écran d'exercice |
| « rien n'est conservé de ton parcours sur nos serveurs » | reste vrai : le backend ne persiste rien (0 dépendance base de données) et renvoie explicitement `avertissement` / `conservation` |

**Tests ajoutés** — `src/app/page.test.tsx`, 5 tests :
- ne dit pas que les réponses ne sont pas conservées
- dit où elles sont enregistrées, et qu'elles sont effaçables
- reste vrai sur le serveur, sans inventer de promesse
- n'introduit aucun terme technique dans le paragraphe de confidentialité
- conserve la promesse sur l'absence de collecte de données personnelles

---

### CORRECTIF 6 — `/design-system` renvoie 404 en production

**Diagnostic.** La page était **prérendue** au build. La garde lit `NODE_ENV` et `DESIGN_SYSTEM_ENABLED` ; or `next build` s'exécute avec `NODE_ENV=production` sans la seconde variable : la page était donc prérendue **en 404** (`.next/server/app/design-system.html` commençait par `<html id="__next_error__">`). Poser `DESIGN_SYSTEM_ENABLED=on` sur le déploiement ne changeait plus rien.

**Correction.** `export const dynamic = 'force-dynamic'` (l.51). L'évaluation de la garde se déplace au moment de la requête : la page redevient pilotable par la variable, et conserve le 404 propre lorsqu'elle est absente — les deux comportements demandés.

### SORTIE DU BUILD POUR `/design-system`

**Avant :**

```
Route (app)                                 Size  First Load JS
┌ ƒ /                                    1.41 kB         107 kB
├ ○ /_not-found                            993 B         104 kB
├ ○ /design-system                       10.6 kB         113 kB     ← prérendue, en erreur
├ ƒ /parcours                              160 B         106 kB
└ ƒ /parcours/[id]                        5.8 kB         112 kB
```

**Après :**

```
Route (app)                                 Size  First Load JS
┌ ƒ /                                    1.41 kB         107 kB
├ ○ /_not-found                            993 B         104 kB
├ ƒ /design-system                       10.6 kB         113 kB     ← dynamique
├ ƒ /parcours                              160 B         106 kB
└ ƒ /parcours/[id]                        5.8 kB         112 kB

○  (Static)   prerendered as static content
ƒ  (Dynamic)  server-rendered on demand
```

Le passage de `○` à `ƒ` est la preuve. Le nombre de pages statiques générées passe de 4 à 3 (`Generating static pages (3/3)`) : la route ne figure plus dans `prerender-manifest.json`, ce que vérifie également un test.

**Tests ajoutés** — `src/design/design-system-garde.test.ts`, 5 tests, dont :
- la page exporte bien `dynamic = 'force-dynamic'` (valeur réellement consommée par le routeur, importée dans le test)
- la garde `notFound()` est **conservée** — `force-dynamic` ne doit pas avoir supprimé la fermeture
- `prerender-manifest.json` ne contient plus `/design-system`

---

### CORRECTIF 7 — Faute d'accord livrée à l'élève

**Diagnostic.** `lib/parcours.ts:139` renvoyait « Le service **de** exercices n'est pas configuré sur ce déploiement. » — faute visible par l'élève en cas de mauvaise configuration. `ApiStatus.tsx:49` composait `APIRelio` sans espace.

**Corrections :**

| Fichier | Avant | Après |
|---|---|---|
| `src/lib/parcours.ts:139` | `Le service de exercices n'est pas configuré sur ce déploiement.` | `Le service d'exercices n'est pas configuré sur ce déploiement.` |
| `src/components/ApiStatus.tsx:49` | `` `APIRelio ${etat.version} — statut…` `` | `` `API Relio ${etat.version} — statut…` `` |

---

### LISTE DES TEXTES UTILISATEUR RELUS

Périmètre : `lib/parcours.ts`, `lib/api.ts`, `lib/tutorat.ts`, `components/Exercice.tsx`, `components/ApiStatus.tsx`, `components/ParcoursServeur.tsx`, `components/parcours.ts`, `app/page.tsx`, `app/parcours/page.tsx`, `app/parcours/[id]/page.tsx`.

**132 chaînes littérales** extraites et relues, commentaires retirés.

**Textes trouvés fautifs : 2** (les deux corrigés ci-dessus).

**Textes relus et conformes — aucun changement :**

| Emplacement | Texte | Verdict |
|---|---|---|
| `lib/parcours.ts:143` | « La réponse du service ne respecte pas le contrat attendu. » | ✅ |
| `lib/parcours.ts:150` | « Le service ne répond pas. Réessaie dans un instant. » | ✅ |
| `lib/parcours.ts:152` | « Impossible de joindre le service d'exercices. » | ✅ — déjà bien accordé |
| `lib/api.ts:84` | « Aucune réponse de l'API après N secondes. » | ✅ |
| `lib/api.ts:92` | « Impossible de joindre l'API. Vérifiez API_BASE_URL et la configuration CORS du backend. » | ✅ **conservé volontairement** — diagnostic d'opérateur, pas message élève. Un déploiement mal configuré n'offre aucune autre piste. Un test verrouille cette présence |
| `lib/tutorat.ts:73-76` | « Tu n'as pas encore assez travaillé pour que je puisse dire. » / « Tu as réussi du premier coup plusieurs exercices. » / « Tu as réussi avec de l'aide. » / « C'est difficile pour toi en ce moment. Demande un indice. » | ✅ |
| `lib/tutorat.ts:87-94` | 8 libellés de catégorie (« un facteur oublié dans la multiplication », « réduction incomplète », « fraction pas simplifiée », « difficulté que je n'ai pas su nommer »…) | ✅ — pas de terme technique |
| `Exercice.tsx:77-82` | 5 libellés de verdict (« Ta réponse est juste. », « Ce n'est pas encore juste. »…) | ✅ |
| `Exercice.tsx:151` | « Le service ne répond pas. Réessaie dans un instant. » | ✅ |
| `Exercice.tsx:230` | « Cet exercice n'est pas disponible pour le moment. » | ✅ |
| `ApiStatus.tsx:33-70` | 5 états : « Connexion à l'API en cours… », « API non configurée », « Contrat désynchronisé », « API indisponible », « Revérifier » | ✅ (le seul défaut, `APIRelio`, corrigé) |
| `ParcoursServeur.tsx:22` | « Exercices indisponibles » | ✅ |
| `ParcoursServeur.tsx:70-71` | « Disponible à partir de la semaine N. » / « Ce bloc n'est pas encore ouvert. » | ✅ |
| `parcours.ts:21-46` | 5 étapes marketing | ✅ |
| `page.tsx` §« Commencer » | « Les exercices s'ouvrent à la semaine où la leçon est enseignée… » | ✅ |
| `page.tsx` bandeau | « Première version. Le parcours couvre trois leçons du programme… » | ✅ |
| `parcours/page.tsx:45` | « Trois leçons du programme, des exercices et des indices progressifs. » | ✅ |
| `page.tsx` pied de page | paragraphe de confidentialité | ✅ — **corrigé** (correctif 5) |

**Message `throw new Error(\`HTTP ${reponse.status}\`)` (`lib/parcours.ts:128`)** : conservé tel quel. Il est intercepté par le `try/catch` et remplacé par un message élève ; il ne atteint jamais l'écran.

**Tests ajoutés** — `src/design/textes-affiches.test.ts`, 10 tests : 5 sur les fautes d'accord constatées, 5 sur les invariants de langue (aucune promesse de non-conservation, aucun terme d'implémentation dans un message d'erreur, le diagnostic CORS reste présent).

---

### CORRECTIF 8 — Variable d'environnement piège non documentée

**Diagnostic.** `ANNEE_SCOLAIRE_DEBUT` et `DATE_NAVIGATION_TEST` sont lues par `src/routes/parcours.ts` mais absentes de `.env.example`. La seconde est dangereuse : `dateDuJour()` la préfère à `new Date()` sans validation de contexte.

**Correction** — bloc ajouté à `.env.example` (l.23-47), les deux variables **commentées** :

- `ANNEE_SCOLAIRE_DEBUT` : format, défaut appliqué par le code (`2026-09-07`, repris de `DEBUT_ANNEE_DEFAUT`), et avertissement que la correction en production passe par la variable Railway **et** un redéploiement.
- `DATE_NAVIGATION_TEST` : avertissement explicite — *« À NE DÉFINIR QU'EN ENVIRONNEMENT DE TEST. En production, cette variable fige la date de l'application : les blocs resteraient bloqués sur la semaine simulée, indéfiniment, sans qu'aucune erreur ne soit visible. »*

**Tests ajoutés** — `backend/test/env-example.test.ts`, 10 tests. Le plus important compare `.env.example` aux **lectures réelles de `process.env`** dans `src/config.ts`, `src/routes/v1.ts` et `src/routes/parcours.ts` : toute variable lue mais non documentée fait échouer le test. Le balayage couvre les deux formes utilisées (`process.env.X` et `env.X`, cette dernière étant la forme de `loadConfig(env = process.env)`).

**Vérification « échouait avant » :**

```
$ git stash push -- .env.example && npx tsx --test test/env-example.test.ts
  not ok 3 - `ANNEE_SCOLAIRE_DEBUT` est décrite dans `.env.example`
  not ok 4 - `DATE_NAVIGATION_TEST` est décrite dans `.env.example`
  not ok 5 - `DATE_NAVIGATION_TEST` porte un avertissement explicite sur le risque en production
  not ok 6 - `DATE_NAVIGATION_TEST` reste commentée dans l'exemple
  not ok 7 - `ANNEE_SCOLAIRE_DEBUT` reste commentée dans l'exemple
  not ok 8 - l'exemple annonce la valeur par défaut réellement appliquée par le code
  not ok 9 - aucune variable lue par le code n'est absente de `.env.example`
  # tests 10 / # pass 3 / # fail 7
```

---

## 4. CE QUI N'A PAS PU ÊTRE FAIT, ET POURQUOI

| Point | Raison |
|---|---|
| **Vérification du clavier mathématique sur un téléphone réel (360×640 px, Android)** | Aucun appareil, aucun émulateur, aucun `/dev/kvm` dans cet environnement. Les 14 testsendents sur le comportement DOM et la cascade d'événements, pas sur le tactile réel. Le contrat « pas de double exécution » repose sur `MouseEvent.detail`, dont le comportement est normé et vérifié en jsdom mais **n'a pas été observé sur un navigateur** |
| **Vérification visuelle du bouton bleu sur l'accueil** | Le CSS compilé est vérifié par extraction (`offset 7380`), et l'ordre de cascade est vérifié par script. Le rendu pixel n'a pas été observé : aucun navigateur dans l'environnement |
| **Mesure du contraste `--bordure-forte` sur écran réel** | Le ratio 3,66:1 est calculé par la formule WCAG 2.1 du projet (`src/design/contraste.ts`). Il ne rend pas compte du contraste lumineux en plein soleil, ni du mode sombre — **que l'application applicative n'a toujours pas** (`globals.css` ne consomme aucune variable de `tokens.css`) |
| **Contrôle de la page `/design-system` en production** | Le correctif porte sur le comportement de build, vérifié par la sortie de `next build` et le manifeste. **La production Vercel n'est pas redéployée dans le cadre de ce chantier** : `https://relio-frontend-one.vercel.app/design-system` répond toujours 404, et le restera jusqu'au push suivi du redéploiement automatique |
| **Bascule effective de `DESIGN_SYSTEM_ENABLED` sur un déploiement** | Hors périmètre : c'est une action d'opérateur dans le tableau de bord Vercel. Le code est désormais correct pour la recevoir |
| **Validation linguistique native** | Aucuncorrecteur orthographique automatique n'est disponible dans l'environnement. La relecture des 132 chaînes est humaine et assistée par motif ; elle ne garantit pas l'absence de toute impropriété |
| **Non-régression de mise en page à 768 px** | Le chantier ne corrige pas la hauteur imposée par `.exercice--saisie`. Les tests ne couvrent pas la mise en page : `jsdom` n'applique pas les CSS — limite déjà documentée dans `accessibilite.test.ts` |
| **Branchement de `verifier:poids` dans la CI** | Signalé dans l'audit comme défaut de documentation, **hors des 8 correctifs demandés**. Le budget CSS passe de 6,98 à 7,00 Ko gzip, pour un seuil de 30 Ko : marge de 23 Ko |

---

## 5. ÉTAT FINAL MESURÉ

### Backend

```
$ npm run typecheck    → exit 0
$ npm test             → # tests 317 / # pass 317 / # fail 0   (67 suites, 14,3 s)
$ npm run build        → exit 0
```

### Frontend

```
$ npm run typecheck        → exit 0
$ npm run test:logique     → # tests 119 / # pass 119 / # fail 0   (22 suites, 6,2 s)
$ npm run test:ui          → Test Files 11 passed (11)
                            Tests 193 passed (193)                (26,6 s)
$ npm run build            → exit 0, 4 routes
$ npm run verifier:poids   → Total CSS : 30.7 Ko bruts -> 7.0 Ko gzip
                            Budget : 30 Ko gzip — marge 23.0 Ko — OK
```

**Avant : 562 tests. Après : 629 tests. Échecs : 0 dans les deux cas.**

Aucune régression : les 562 tests d'origine passent toujours.

---

## 6. STATUT GLOBAL

# ✅

**Les 8 correctifs sont appliqués, testés et vérifiés.** Chacun porte un test qui échouait sur le code d'origine — état établi par exécution réelle, pas par relecture. Les 629 tests passent, les typechecks et les builds sont propres sur les deux dépôts, le budget CSS reste à un quart de son seuil.

**Réserve unique, hors périmètre du chantier :** les correctifs ne sont pas encore en production. Le push déclenchera un redéploiement automatique chez Vercel et Railway ; `/design-system` restera en 404 jusque-là, et le bouton principal restera blanc jusque-là. Le chantier est terminé **dans le code**, pas encore **en production**.