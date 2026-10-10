# Rapport final — Chantier 7.7 : clavier mobile, verdicts simples et écritures flexibles

Date : 11 octobre 2026
Dépôts : `relio-backend` (`dd2cad8`, `e425722`) · `relio-frontend` (`0b36123`)

> **Avertissement de lecture.** Aucune partie de ce rapport ne repose sur un
> test sur téléphone Android. L'environnement n'en dispose pas, et le règlement
> du projet interdit de lancer un navigateur local pour reproduire le parcours
> élève. Ce qui suit est soit **vérifié** (test automatisé ou appel HTTP sur la
> production), soit **à valider sur téléphone**, et la distinction est
> maintenue partout.

---

## 1. Les causes précises du clavier qui recouvre le contenu

### 1.1 Cause principale : le clavier est trop grand pour l'écran cible

Le clavier d'expression compte **9 rangées**. Chaque touche fait 44 px de haut —
minimum non négociable — et les espacements ajoutent 5 px entre rangées.

```
9 × 44 px + 8 × 5 px + 16 px de marge intérieure + 1 px de bordure = 453 px
```

| Écran | Part occupée | Hauteur restante |
|---|---|---|
| **360 × 640** (cible du produit) | **71 %** | **187 px** |
| 360 × 780 | 58 % | 327 px |
| 390 × 844 | 54 % | 391 px |

Sur l'écran de référence, il ne restait que **187 px** pour l'en-tête, l'énoncé,
la consigne, le champ de réponse et le bouton « Vérifier ». L'énoncé était donc
nécessairement hors de l'écran. **Ce n'est pas un réglage mal ajusté : c'est une
incompatibilité géométrique.**

### 1.2 Cause structurelle : `position: sticky` ne redistribue rien

Le clavier était positionné en `position: sticky; bottom: 0`.

Une position `sticky` **garde l'élément dans le flux** — mais la colonne qui le
contient continuait de grandir avec le contenu. Rien ne réservait de place au
clavier, donc rien ne rétrécissait. Un élément collé en bas d'une page qui
dépasse de l'écran **recouvre le contenu** au lieu de le pousser.

C'est le mécanisme exact du défaut observé : le clavier n'était pas « trop
bas », il n'avait simplement **rien à côté de quoi se réorganiser**.

### 1.3 Cause aggravante : la hauteur du clavier système n'était jamais mesurée

Sur Android, l'ouverture du clavier système **ne réduit pas la fenêtre de mise
en page** : seule la fenêtre visuelle change. Une page en `100dvh` continue
donc de croire que l'écran fait 640 px de haut, alors qu'il n'en reste que 400
à disposition. Tout ce qui est positionné en `bottom` se retrouve **derrière**
le clavier du téléphone.

Le projet n'utilisait nulle part `window.visualViewport`, l'API qui expose la
fenêtre réellement visible.

### 1.4 Cause secondaire : rien ne ramenait le champ dans la zone visible

À l'ouverture du clavier, le champ et le bouton restaient où ils étaient. Sur
un écran court, l'élève devait défiler **à l'aveugle** pour retrouver ce qu'il
venait de toucher.

---

## 2. Modifications apportées

### 2.1 Page en colonne contrainte à trois zones

En mode saisie, l'article n'est plus une boîte qui grandit mais une colonne de
hauteur contrainte :

```
┌─────────────────────────────────┐
│ zone défilante                  │  flex: 1, overflow-y: auto
│ énoncé, consigne, indices,     │
│ suivi                           │
├─────────────────────────────────┤
│ composeur                       │  hauteur propre
│ retour de correction,           │
│ champ, aperçu, bouton Vérifier │
├─────────────────────────────────┤
│ clavier                         │  hauteur propre
└─────────────────────────────────┘
```

Le clavier **prend de la place au lieu de recouvrir**. C'est la différence
entre un élément dans le flux et un élément positionné.

Le verdict et l'aide progressive sont dans le **composeur**, pas dans la zone
défilante : l'élève lit son retour sans avoir à défiler.

### 2.2 Mesure du clavier système

`src/hooks/useHauteurClavierSysteme.ts` mesure `innerHeight −
visualViewport.height − visualViewport.offsetTop` et publie le résultat dans
`--relio-clavier-systeme`. La feuille de style soustrait cette variable de la
hauteur disponible.

**C'est un mécanisme de sécurité, pas un doublon.** `inputMode="none"` *devrait*
empêcher le clavier système de s'ouvrir sur un champ mathématique, mais ce
n'est pas garanti sur tous les navigateurs Android. Si l'un des deux claviers
apparaît, l'autre ne peut plus masquer le contenu.

### 2.3 Ramener le composeur dans la zone visible

Au toucher du champ, `scrollIntoView({ block: 'end' })` amène le composeur dans
la zone visible. L'élève ne cherche plus où sont le champ et le bouton.

### 2.4 Écrans bas

Sur `max-height: 700px`, les espacements internes du clavier sont resserrés
(gaps 6 → 4 px, marges 8 → 4 px). **Les 44 px ne sont jamais réduits** : la
cible tactile ne se négocie pas.

### Éléments préservés

Saisie au curseur, toutes les touches existantes, fermeture et réouverture au
toucher du champ, bascule vers le clavier du téléphone : **tout est inchangé**.

### Limites restantes sur Android — **à valider sur téléphone**

| Point | État |
|---|---|
| Le clavier ne recouvre plus le texte | **Vérifié** statiquement (structure) — **non vérifié** sur appareil |
| Un seul clavier à la fois | Non vérifiable sans appareil ; le mécanisme de double protection est en place |
| `inputMode="none"` respecté par le navigateur | Non vérifiable ici — risque connu, identifié au chantier 7.6 |
| Défilement fluide dans la zone restreinte | Non vérifiable ici |
| Comportement sur Safari iOS | Non vérifié. `dvh` et `visualViewport` existent, mais le comportement diffère |

**Ce que je peux affirmer :** la cause est identifiée et chiffrée, la
correction est structurelle (le clavier est dans le flux, pas au-dessus), et la
dégradation est couverte par la mesure du clavier système.
**Ce que je ne peux pas affirmer :** que le défaut est éteint sur un téléphone.

---

## 3. Verdicts — avant et après

Mesurés sur la production, après redéploiement.

| Cas | Avant | Après |
|---|---|---|
| Réponse juste | « Ta réponse est juste. » | **« Bravo ! Ta réponse est juste. »** |
| Réponse fausse | « Ce n'est pas encore juste. » | **« Ce n'est pas encore ça. Essaie encore. »** |
| Juste mais incomplète | « Ta réponse est partiellement correcte : tu as bien commencé le travail, mais il reste une étape pour le terminer. Continue jusqu'à obtenir une réponse qui ne peut plus être simplifiée. » (169 car.) | **« Tu as bien commencé. Il reste une étape. Continue. »** (49 car.) |
| Juste, forme non respectée | « Ton résultat est mathématiquement juste, mais tu n'as pas respecté la forme demandée. Écris ta réponse sous la forme d'un produit de facteurs du premier degré. » | **« Ton calcul est juste, mais tu dois écrire la réponse sous la forme d'un produit entre parenthèses. »** |
| Saisie illisible | « Caractère non reconnu : « $ ». » | **« Je n'arrive pas à lire ta réponse. Le symbole « $ » ne sert pas ici. Vérifie les signes et essaie encore. »** |

### Formes demandées — vocabulaire simplifié

| Avant | Après |
|---|---|
| « une fraction irréductible » | « une fraction qu'on ne peut plus simplifier » |
| « un produit de facteurs du premier degré » | « un produit entre parenthèses » |
| « la forme a√b, avec a entier et b sans facteur carré » | « un nombre, puis le symbole racine, puis un nombre sans carré » |

### Longueur

Les libellés tiennent désormais en **moins de 130 caractères** (contre 169 pour
le plus long). Un test verrouille ce plafond : sur 360 px, un retour de
correction doit tenir en deux ou trois lignes.

### Garantie de non-régression

- **Aucun terme technique** dans un texte élève — 11 mots bannis, vérifiés sur
  les 12 exercices, toutes leurs réponses et tous les niveaux d'aide.
- **Jamais « faux » quand le calcul est juste** — vérifié sur les 5 verdicts :
  aucun mot de reproche ne peut apparaître sur un résultat juste.
- Les **5 verdicts** restent produits et distincts.
- Les **3 niveaux d'aide** progressifs sont conservés, y compris le bilan de
  méthode.

### Modification de contenu annoncée

**3 consignes d'exercice** contenant « produit de facteurs du premier degré »
sont devenues « produit entre parenthèses ». C'est la **seule** modification de
contenu du chantier, demandée explicitement par la Partie B, qui nommait cette
formule. La règle de forme (`regleForme: 'produit_de_facteurs'`) et la réponse
attendue sont **inchangées** — seul le texte change.

---

## 4. Formes désormais acceptées

Vérifié sur la production après redéploiement.

### Acceptées

| Saisie | Exercice | Verdict |
|---|---|---|
| `2x + 1` | MVP-B1-E1 | `correct` |
| **`A = 2x + 1`** | MVP-B1-E1 | **`correct`** |
| `A=2x+1` (sans espaces) | MVP-B1-E1 | `correct` |
| `A   =   2x + 1` | MVP-B1-E1 | `correct` |
| `D = (2x-3)(2x+3)` | MVP-B1-E4 | `correct` |
| `D = (2x−3)(2x+3)` (moins U+2212) | MVP-B1-E4 | `correct` |
| `G = 5√2` | MVP-B2-E1 | `correct` |
| `4x^2 - 9 = (2x-3)(2x+3)` | MVP-B1-E4 | `correct` |

### La règle appliquée

| Membre gauche | Membre droit | Décision |
|---|---|---|
| illisible seul, ressemble à un nom (`A`, `B`, `G`, `J`) | analysable | le nom est l'inconnue de l'énoncé : on analyse le droit |
| analysable | analysable | **les deux doivent être égaux**, sinon refus |
| analysable | nom | refus — l'élève a mis la réponse à gauche, on ne devine pas |
| ni l'un ni l'autre analysable | | refus |

### Toujours refusées

| Saisie | Raison |
|---|---|
| `x = 2x + 1` | « Les deux côtés de ton signe " = " ne valent pas la même chose. » |
| `0x = 2x + 1` | idem — contient la bonne réponse, mais l'égalité est fausse |
| `2x + 1 = A` | « Mets la réponse après le signe " = ". » |
| `A = B = 2x + 1` | « Écris une seule égalité. » |
| `5√2 = 5√3` | les deux membres s'analysent, l'égalité est fausse |
| `= 2x + 1`, `A = ` | membre vide |
| `A = B = C = ...`, `2x + 1 + = ...` | ambigu |

### Un cas contre-intuitif, énoncé explicitement

**`x = 5√2` est accepté** sur un exercice de racines ; **`x = 2x + 1` est
refusé** sur un exercice d'expressions.

Ce n'est pas une liste de lettres interdites. L'analyseur de racines ne
connaît que la forme `a√b` : `x` n'y est pas analysable, donc il est traité
comme le nom de l'inconnue. L'analyseur d'expressions, lui, **connaît** `x` :
les deux membres sont comparés, et `x = 2x + 1` est refusé parce que
l'égalité est fausse. **Le refus dépend de ce que le moteur sait lire.**

### Aucune confusion introduite

| Garantie | Vérifié |
|---|---|
| Une réponse fausse reste fausse avec ou sans `=` | même verdict, même statut, même catégorie |
| `A = 4x^2 - 9` sur MVP-B1-E4 garde le verdict « résultat juste, consigne non respectée » | oui |
| `G = √(25×2)` garde le verdict « partiellement correct » | oui |
| Les 12 réponses attendues sont acceptées avec et sans `=` | oui |

**Aucune règle mathématique n'a été modifiée.** Seule la façon de *lire* la
réponse a changé, jamais le jugement porté dessus.

**Aucune dépendance ajoutée.** Le module fait 130 lignes et s'appuie sur les
analyseurs existants.

---

## 5. Tests, commits et déploiement

### Tests

| Dépôt | Avant | Après | Commande |
|---|---|---|---|
| backend | 267 | **307** (+40) | `npm test` |
| frontend — logique | 119 | **119** | `npm run test:logique` |
| frontend — rendu, tokens, clavier | 136 | **136** (+12) | `npm run test:ui` |
| **Total** | 522 | **562** | `npm test` |

Couverture du clavier : 6 tests sur la mesure du clavier système — clavier
ouvert, fermé, `offsetTop` non répercuté, API absente, hauteur négative,
fermeture de la variable CSS.

### Commits

| Dépôt | Commit | Push |
|---|---|---|
| `relio-backend` | `dd2cad8` — `feat(ecriture): accepter les égalités écrites comme au cahier` | `e2c2e0e..dd2cad8` |
| `relio-backend` | `e425722` — `fix(tutorat): deux messages restaient dans l'ancien registre` | `dd2cad8..e425722` |
| `relio-frontend` | `0b36123` — `fix(clavier): le clavier ne recouvre plus le texte de l'application` | `2ff2744..0b36123` |

### Déploiement — vérifié séparément du push

| Constat | Moyen | Résultat |
|---|---|---|
| Backend redéployé | uptime Railway passé à 22 s, **et** nouveau libellé observé en réponse | **confirmé** |
| Frontend redéployé | CSS contenant `exercice__composeur` servi par Vercel | **confirmé** |
| `A = 2x + 1` accepté en production | appel HTTP | **confirmé** |
| `x = 2x + 1` refusé en production | appel HTTP | **confirmé** |
| Bloc B3 toujours fermé | `MVP-B3-E1` → **HTTP 403** | **confirmé** |
| Non-régression du parcours | `/`, `/parcours`, `/parcours/MVP-B1-E1` en 200 ; 9 liens d'exercices ; aucune page « Exercices indisponibles » | **confirmé** |
| `/design-system` toujours fermé | HTTP 404 | **confirmé** |
| CI backend | `e425722` → **success** | **confirmé** |
| CI frontend | `0b36123` → **success** | **confirmé** |
| Aucune réponse attendue dans le client | seules occurrences dans des fichiers `*.test.ts`, jamais dans le bundle | **confirmé** |

### Erreur de calcul corrigée au passage

L'aide sur les racines affirmait que « √8 et √18 donnent toutes deux 2√2 et
√3 ». C'est **faux** : √18 = 3√2. Une aide qui se trompe apprend à l'élève à se
tromper. Corrigé, avec un test qui verrouille l'exemple.

---

## 6. Points exigeant encore une validation humaine sur téléphone

**Aucun de ces points n'a été testé. Aucun n'est présenté comme acquis.**

1. **Ouverture du champ** — le clavier mathématique s'affiche-t-il seul, sans
   le clavier du téléphone ? C'est le test le plus important.
2. **Champ et bouton « Vérifier » visibles** pendant la saisie, sans défiler.
3. **Énoncé et verdict** lisibles : la zone défilante fait-elle défiler
   correctement quand elle est réduite à ~190 px ?
4. **Saisie au milieu** — les parenthèses s'insèrent-elles toujours au bon
   endroit ? Le comportement est inchangé côté logique, mais la position du
   curseur à l'écran peut différer.
5. **Fermeture / réouverture** — masquer puis retoucher le champ doit
   rouvrir le clavier, sans blocage après trois cycles.
6. **Bascule clavier système** — pas de double clavier, saisie conservée.
7. **Écrans 360 × 640, 360 × 780, 390 × 844** — comportement du défilement et
   qualité des gestes.
8. **Safarí iOS** — le chantier ne visait qu'Android, mais le code est partagé.

---

## 7. Ce qui n'est pas fait

- **Aucun test tactile.** Pas d'appareil, et le règlement interdit le navigateur
  local.
- **Aucun compte, aucun stockage serveur, aucun suivi de classe** — décisions
  non arbitrées, non touchées.
- **Aucune nouvelle fonctionnalité.** Le chantier est clos : pas de tableau de
  bord, pas de tuteur conversationnel, pas de nouveaux exercices.

---

## 8. Statut

**✅ Code livré, testé, poussé et déployé vérifié.**

**⚠️ La Partie A n'est pas validée sur téléphone.** La cause est identifiée et
chiffrée, la correction est structurelle, la dégradation est couverte — mais
le résultat réel sur un appareil Android reste à constater. C'est le seul point
qui empêche de déclarer ce chantier entièrement validé.