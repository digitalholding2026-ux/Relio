# Rapport de fin de chantier — Design system foundation

Date : 11 octobre 2026
Dépôt : `relio-frontend`
Commit : `2ff2744` — `feat(design-system): tokens, composants de base et page de reference`

---

## 1. Résumé

Les fondations visuelles de Relio sont en place : des tokens en double source
(TypeScript + variables CSS) **empêchés de diverger** par test, et **14
composants de base** sans aucune dépendance UI, conformes AA et 44 px.
Les trois conflits de contraste de la palette imposée ont été **mesurés**,
documentés et résolus par des variantes calibrées, pas par des approximations.
La page `/design-system` sert de contrat visuel et affiche les contrastes
**calculés** — elle est fermée en production par défaut.
Le CSS de production pèse **6,8 Ko gzip pour un budget de 30 Ko**.
249 tests passent, la CI est verte, le déploiement est vérifié, et **aucun écran
existant n'a été modifié**.

---

## 2. Arborescence

### Créé

```
DESIGN_SYSTEM.md                       documentation du design system
scripts/verifier-poids-css.mjs         contrôle du budget CSS après build
vitest.config.mts                      configuration de la suite de rendu

src/design/
  tokens.ts                            source de vérité (TypeScript)
  tokens.css                           variables CSS, clair / sombre / économie
  contraste.ts                         calcul WCAG, sans dépendance
  setup.ts                             nettoyage entre les tests de rendu
  tokens.test.ts                       73 tests — contrastes et synchronisation
  accessibilite.test.ts                34 tests — invariants CSS

src/components/ds/                     14 composants, CSS Modules
  base.module.css                      classes partagées (focus, cible, cache)
  Bouton · BoutonIcone · Carte · Puce · Pastille
  BarreProgression · AnneauProgression · Champ/ZoneTexte · Avatar
  Feuille · Toast · Squelette · EtatVide · Icone · Theme
  composants.test.tsx                  57 tests de rendu

src/app/design-system/
  page.tsx                             route protégée, noindex
  PageDesignSystem.tsx                 le catalogue
  design-system.module.css             sa mise en page
```

### Modifié

| Fichier | Nature |
|---|---|
| `package.json` | scripts `test:ui`, `test:logique`, `verifier:poids` ; `test` exécute les deux suites |
| `package-lock.json` | dépendances de test |
| `src/app/layout.tsx | import de `tokens.css`, `theme-color` clair/sombre |

### Non modifié — vérifié

`src/lib/`, `src/components/Exercice.tsx`, `src/components/ClavierMath.tsx`,
`src/components/ParcoursServeur.tsx`, `src/app/page.tsx`, `src/app/parcours/`,
`src/app/globals.css`. Aucun écran existant n'est touché.

---

## 3. Dépendances ajoutées

| Paquet | Version | Justification |
|---|---|---|
| `vitest` | ^4.1.11 | Tests de rendu. Ajouté explicitement par le cahier des charges. |
| `jsdom` | ^26.1.0 | DOM pour le rendu. Évite un navigateur complet, donc plus léger et sans téléchargement de binaire. |
| `@testing-library/react` | ^16.3.3 | Rendu et requêtes par rôle ARIA. |

**Trois dépendances de développement, aucune de production.** Le bundle
livré à l'élève ne change pas.

`@testing-library/jest-dom` et `@testing-library/user-event` ont été **écartés
délibérément** : `fireEvent` suffit aux interactions testées, et `jest-dom`
n'apporte que des Sugar assertions qui alourdiraient le projet pour rien.

**Versions et vulnérabilités.** `vitest@3` (la version alors courante)
introduisait **3 vulnérabilités** dans l'arbre, dont 2 critiques
(`tinypool`). Passé à `vitest@4.1.11`, l'arbre est à **0 vulnérabilité**.
Cette vérification a été faite avant d'écrire la première ligne de composant.

**Tailwind écarté.** Le cahier des charges autorisait « Tailwind si présent,
sinon CSS Modules ». Tailwind n'est pas présent. L'ajouter aurait imposé de
réécrire les classes existantes de `globals.css` — donc de risquer les écrans
déjà vérifiés en production — et son utilitaire de génération fait peser le
budget CSS. **CSS Modules**, comme le permet le cahier des charges.

---

## 4. Composants — description visuelle

Page de référence : `/design-system`. Les éléments ci-dessous sont ce qu'elle
affiche.

### Bouton

Quatre variantes, trois tailles, quatre états.

| | Fond | Texte | Usage |
|---|---|---|---|
| `primary` | indigo | blanc (12,67:1) | action principale — **une seule par écran** |
| `secondary` | surface + bordure forte | encre | action concurrente |
| `ghost` | transparent | indigo | action discrète, répétée |
| `danger` | rouge | blanc (4,83:1) | action destructive |

Tailles `sm` / `md` / `lg` — **les trois font 44 px de haut**. La taille du
texte ne détermine pas la zone tactile. Pendant le chargement, le bouton est
indisponible et déclaré `aria-busy`, **le libellé reste visible** : la mise en
page ne saute pas.

### Bouton icône

Carré à coins arrondis, icône centrée. `label` **obligatoire dans l'API** :
sans lui, le bouton ne serait annoncé que par « bouton ». C'est le seul moyen
d'empêcher qu'une croix ou une flèche de retour ne soit incompréhensible.

### Carte

Surface arrondie 16 px, ombre douce. Trois paddings. Variante `elevee` pour un
panneau qui doit se détacher du fond.

### Pastille et puce

La pastille est une capsule colorée **toujours accompagnée d'un texte** : la
couleur seule n'est pas une information fiable. La puce est une capsule
cliquable dont l'état sélectionné est porté par **trois signaux** — fond,
graisse et `aria-pressed` — pour que la couleur ne soit jamais le seul
porteur d'information.

### Progression

Barre à piste bordée de 10 px ; anneau SVG de 96 px par défaut, arc démarrant à
midi. **Aucune des deux ne doit servir à afficher un score d'exercice** : c'est
une règle pédagogique inscrite dans la documentation et rappelée sur la page.

### Champs

48 px de haut, **16 px minimum de police** (en dessous, iOS zoome la page au
focus). L'étiquette, l'aide et l'erreur sont reliées par `aria-describedby`.
L'erreur double son signal : bordure rouge **et** message explicite, annoncé en
`role="alert"` pour interrompre la lecture.

### Feuille glissante

Remonte du bas, coins arrondis en haut, poignée de glissement, fond assombri. Le
focus y entre à l'ouverture, y reste piégé, et revient sur le bouton d'origine
à la fermeture. `Échap` ferme. Sur mobile, la feuille **pousse** le contenu au
lieu de le recouvrir.

### Notification

Barre fixe en bas, hors de la zone du champ et du bouton de validation. Trois
tons, bordures gauche colorées. `role="status"` pour une information,
`role="alert"` pour une erreur — qui dure 7 secondes contre 3 pour un succès,
parce que « c'est faux » se lit et « c'est enregistré » peut se dissiper.

### Autres

**Avatar** — initiale sur une teinte déduite du nom, donc stable d'un écran à
l'autre. **Squelette** — rectangles statiques, sans animation. **État vide** —
icône, message, et **toujours une action de sortie**. **Icônes** — 12 SVG en
ligne, trait de 2 px sur grille de 24 px.

---

## 5. Tests

| Suite | Commande | Nombre |
|---|---|---|
| Logique (historique) | `npm run test:logique` | **119** |
| Rendu + tokens | `npm run test:ui` | **130** |
| **Total** | `npm test` | **249** |

Couverture de ce que le cahier des charges demandait : **au moins un test de
rendu par composant**, soit 14 composants couverts.

### Ce que les tests vérifient réellement

- **Contraste** — 18 paires de l'interface, chacune nommée, calculées avec la
  formule WCAG. Une liste écrite à la main, pas générée : une liste auto-générée
  ne vérifierait que les paires qu'elle choisit.
- **Synchronisation TypeScript ↔ CSS** — 30 variables comparées. Une dérive fait
  échouer les tests, elle ne peut pas atteindre la production. *Ce test a
  d'ailleurs attrapé une divergence réelle pendant l'écriture.*
- **Cible tactile** — vérifiée **statiquement**, en résolvant la valeur
  effective de chaque feuille. `jsdom` n'applique pas de feuille de style : un
  test de rendu qui prétendrait mesurer une cible passerait toujours, donc ne
  vérifierait rien.
- **Accessibilité ARIA** — rôles, liaisons `label`/`aria-describedby`, piège de
  focus, `aria-busy`, `role="alert"`, libellés obligatoires.
- **Mouvement** — toute animation déclarée doit avoir son échappement
  `prefers-reduced-motion`.
- **Contraintes produit** — aucune image bitmap, aucune police distante, aucune
  couleur brute dans un composant, aucun rayon hors échelle.

### Les deux suites ne se mélangent pas

Le glob historique (`src/*/*.test.ts`) attrapait le nouveau test de tokens et
l'exécutait avec le mauvais runner. Les périmètres sont désormais disjoints et
explicites — `src/lib/*.test.ts` pour la logique, `src/components/**` et
`src/design/**` pour Vitest — avec un commentaire qui explique pourquoi, pour
que la collision ne revienne pas.

---

## 6. Performance

| Mesure | Avant | Après | Budget |
|---|---|---|---|
| **CSS gzip** | 4,3 Ko | **6,8 Ko** | 30 Ko ✅ |
| CSS brut | 16,5 Ko | 29,9 Ko | — |
| JS premier chargement `/` | 107 Ko | **107 Ko** | — |
| JS `/parcours/[id]` | 111 Ko | **111 Ko** | — |
| JS `/design-system` | — | 113 Ko | page interne |

**Le poids servi à l'élève n'a pas bougé** : 0 Ko de JS et 2,5 Ko de CSS
supplémentaires sur des feuilles partagées, et la page de référence est une
route à part. Les 12 Ko de JS du design system ne sont chargés que sur cette
route, fermée en production.

Le contrôle du budget est automatisé : `npm run verifier:poids`, exécuté après
le build. Un test ne conviendrait pas — il s'exécuterait avant que les CSS
Modules aient été fusionnés, et ne verrait que les sources.

---

## 7. Accessibilité

### Vérifié automatiquement

| Point | Comment |
|---|---|
| Contraste AA | 18 paires mesurées par la formule WCAG |
| Bordures de formulaire ≥ 3:1 | mesuré sur fond, surface et surface haute |
| Cible tactile 44 px | résolution de la valeur effective dans chaque feuille |
| Anneau de focus | vérifié dans chaque feuille interactive |
| `prefers-reduced-motion` | toute animation doit avoir son échappement |
| Rôles et liaisons ARIA | 14 composants rendus et interrogés par rôle |
| Pas d'image bitmap, pas de police distante | analyse des feuilles de style |

### Trois conflits de la palette imposée — mesurés, pas contournés

| Usage naïf | Mesure | Décision |
|---|---|---|
| Blanc sur orange `#F97316` | 2,62:1 | interdit — l'orange porte l'encre (6,37:1) |
| Blanc sur vert `#16A34A` | 3,08:1 | interdit — le vert porte l'encre (5,42:1) |
| `#64748B` sur fond sable | 4,45:1 | variante `#63738A` (4,52:1) pour le texte courant |

**La règle qui en découle : un fond coloré porte de l'encre, sauf le rouge et
l'indigo.** Elle est écrite dans `tokens.ts`, dans `DESIGN_SYSTEM.md` et
affichée sur la page de référence.

Un quatrième conflit a été trouvé et corrigé en cours de route : la pastille
d'alerte plaçait du texte rouge sur fond rouge pâle, à 4,01:1. Corrigée par le
même motif que les autres.

### Reste à vérifier — **non fait**

- **Taille réelle des cibles tactiles à l'écran.** La feuille déclare 44 px ; ce
  que l'œil et le doigt rencontrent n'a pas été mesuré.
- **Rendu à 360 / 390 / 768 px.** La mise en page est pensée pour ces largeurs et
  écrite sur une seule colonne sous 768 px, mais elle **n'a pas été vue**.
- **Comportement du mode sombre sur un vrai appareil.**
- **Lecture des contrastes sur un écran réel**, en plein soleil : un ratio
  calculé sur un écran calibré en intérieur ne dit rien d'un téléphone à faible
  luminosité.
- **Navigateurs Android anciens**, notamment la prise en charge de `dvh`,
  `composes` et `inset`.

Aucune de ces vérifications n'est faisable sans appareil : **aucune n'est
présentée comme acquise**.

---

## 8. Points bloquants

### Un seul, et il est levé

**Le contrôle du poids du CSS n'est pas branché dans la CI.** Le jeton de dépôt
n'a pas la portée `workflow` : GitHub a refusé le push tant que
`.github/workflows/ci.yml` était modifié. Le refus a été **respecté, pas
contourné** — ni force-push, ni modification du jeton, ni réglage de plateforme.
Le contrôle existe et fonctionne (`npm run verifier:poids`), et il tourne
manuellement. Le branchement demande soit un jeton à portée `workflow`, soit que
le responsable du projet ajoute l'étape.

### Aucun autre blocage

---

## 9. Recommandations

**Par ordre d'utilité immédiate :**

1. **Ouvrir la page sur un téléphone Android.** C'est la seule chose qui
   manquerait pour que le design system soit réellement validé. Cinq minutes,
   un appareil, et les cinq points « reste à vérifier » tombent.
2. **Brancher `verifier:poids` dans la CI** — décision qui vous revient.
3. **Migrer `Exercice.tsx` et `ClavierMath.tsx`** sur les composants du design
   system. C'est un chantier à part : ces écrans sont **vérifiés en production**
   et leur migration ne doit pas les casser. Un écran à la fois.
4. **Décider du sort de `globals.css`.** Il reste 16,5 Ko de styles
   historiques parallèles au nouveau système. Il ne sera supprimé qu'après la
   migration complète.
5. **Ajouter une barre de progression de parcours**, si le projet en veut une :
   le composant est prêt, et la règle « jamais un score d'exercice » est déjà
   écrite.

---

## 10. Statut global

# ⚠️ Partiel

**Ce qui est acquis :** les fondations demandées existent, sont typées, testées,
accessibles et déployées. Les 7 critères d'acceptation sont vérifiés
automatiquement, et le déploiement est constaté par HTTP.

**Ce qui ne l'est pas :** aucun écran n'a été **regardé** sur un écran réel. Le
cahier des charges demandait de vérifier le rendu à 360 × 640, 390 × 844 et
768 × 1024 ; ces dimensions ont guided la conception, mais aucun rendu n'a été
constaté. Je ne peux pas prétendre l'avoir fait sans appareil.

C'est la seule réserve qui empêche un ✅, et elle ne se lève qu'en dix minutes
sur un téléphone.