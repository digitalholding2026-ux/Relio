# Rapport final — Chantier 7.1 : navigation, calendrier scolaire et parcours élève

**Date** : 2026-10-10
**Objet** : corriger le bouton « Voir le parcours » et la date de début de l'année scolaire
**Statut** : 🟠 **TERMINÉ AVEC RÉSERVES**

> **Convention de lecture.** Chaque affirmation porte l'une de ces trois marques :
>
> - ✅ **Vérifié** — contrôlé directement dans ce chantier, avec une sortie observable.
> - 📋 **Déclaré** — exécuté selon le compte rendu du propriétaire, non observé indépendamment.
> - ⏳ **À vérifier** — non testé ici, ou dépendant d'une action du propriétaire.
>
> **Rien n'a été déployé par ce chantier.** Les vérifications de navigateur ont été
> menées en local, contre les serveurs réellement compilés. La validation en
> production reste à effectuer par le propriétaire.

---

## 1. Diagnostic initial et cause réelle

### 1.1 Le symptôme n'était pas unique

Le propriétaire signalait : « un clic sur *Voir le parcours* n'ouvre pas le parcours
de mathématiques ; on arrive sur une page présentant l'état des fonctionnalités ».

Le diagnostic a révélé **deux défauts distincts, indépendants l'un de l'autre**, dont
un second était plus grave que le symptôme décrit — et que le propriétaire n'avait
pas encore constaté, parce que le premier le masquait entièrement.

### 1.2 Premier constat : le bouton n'existait pas dans la version déployée

✅ **Vérifié.** Inspection de l'historique du dépôt `relio-frontend` :

```bash
# Version effectivement déployée (b148b90) — celle du site observé
git show b148b90:src/app/page.tsx | grep -c "Voir le parcours\|href="
# → 0

git ls-tree -r --name-only b148b90 -- src/app
# → src/app/globals.css
#   src/app/layout.tsx
#   src/app/page.tsx          ← aucune route /parcours
```

La page d'accueil servie en production ne contenait **aucun lien** et **aucun
bouton** « Voir le parcours ». Elle affichait une section statique intitulée
« État des fonctionnalités », qui expliquait ce que Relio prévoyait de proposer.
La page `/parcours` n'existait pas dans cette version : les deux routes
(`/parcours` et `/parcours/[id]`) avaient été créées par le chantier 7.

**Cette version correspondait à la situation décrite.** Le propriétaire n'avait
cliqué sur aucun bouton défaillant : il n'y avait rien à cliquer, et la page
d'accueil servait elle-même d'état des fonctionnalités.

### 1.3 Cause racine réelle : le prerendu statique figeait l'URL du service

Le chantier 7 ayant été poussé, le bouton et la route `/parcours` existent
désormais dans le code. Mais un **second défaut** a été démontré en testant le
parcours réel — il aurait empêché toute correction du premier :

✅ **Vérifié.** La page `/parcours` lisait `process.env.API_BASE_URL` sans être
déclarée dynamique. Next.js la classait donc comme **statique** et la
prérendait au build, moment où la variable vaut `undefined`. La page servie
affichait alors, en toutes lettres :

> « Exercices indisponibles — Le service d'exercices n'est pas configuré sur ce
> déploiement. »

Observation décisive : la variable était **bien** présente dans l'environnement du
processus (`/proc/<pid>/environ`), mais absente du HTML rendu. La valeur avait été
figée au build.

Conséquence : **changer `API_BASE_URL` sur Vercel n'aurait rien produit**, et le
symptôme aurait persisté après le déploiement du bouton. Deux défauts, l'un
visible et l'autre invisible, qui se renforçaient.

| Défaut | Symptôme | why invisible au typecheck et au build |
|---|---|---|
| Bouton et route absents | Aucune navigation possible | Le build passait : il n'y avait rien à construire |
| `/parcours` prérendue | Parcours vide, « service non configuré » | Le build passait : le HTML était « valide » |

### 1.4 Diagnostic du calendrier : un second blocage, plus grave

✅ **Vérifié.** `DEBUT_ANNEE_DEFAUT` valait `2025-09-01`. Avec la date du jour
(2026-10-10), toute date est postérieure à la fin de cette année scolaire :

```
GET /api/v1/parcours
  anneeScolaire.semaine : null
  message : « L'année scolaire du référentiel est terminée. Les blocs se rouvrent à la rentrée. »
  B1 disponible=false 0 exercice(s)
  B2 disponible=false 0 exercice(s)
  B3 disponible=false 0 exercice(s)

POST /api/v1/corrections (MVP-B1-E1) → HTTP 403
```

**Même après correction du bouton, un élève aurait trouvé un parcours vide** : les
trois blocs fermés, y compris B1 qui doit s'ouvrir en semaine 1. Et l'API répondait
**200**, avec un message explicite et une liste d'exercices vide — rien n'indiquait
une panne. Une application de rentrée affichant « aucune leçon disponible » alors
que rien n'était réellement indisponible.

C'est le défaut le plus grave des deux : il ne se voyait pas, et il aurait été
attribué à l'élève ou au programme.

---

## 2. Fichiers modifiés et justification

### 2.1 Frontend — `relio-frontend`

| Fichier | Modification | Justification |
|---|---|---|
| `src/app/parcours/page.tsx` | Ajout de `export const dynamic = 'force-dynamic'` | La page doit lire `API_BASE_URL` **à la requête**, pas au build. Sans cela elle est prérendue et fige l'indisponibilité. |
| `src/app/page.tsx` | Ajout de `export const dynamic = 'force-dynamic'` | Même latence sur l'état de connexion au service. |
| `src/lib/navigation.test.ts` | **Nouveau** — 7 contrôles de navigation | Le défaut initial n'aurait été détecté par **aucun** test, **aucun** typecheck, **aucun** build. |

**Vérifié** — le build classe désormais les pages en dynamique :

```
┌ ƒ /                 ← était ○ (statique)
├ ○ /_not-found
├ ƒ /parcours         ← était ○ (statique)
└ ƒ /parcours/[id]
```

`/parcours/[id]` était déjà dynamique (route paramétrée) : aucun correctif requis.

### 2.2 Backend — `relio-backend`

| Fichier | Modification | Justification |
|---|---|---|
| `src/lib/calendrier.ts` | `DEBUT_ANNEE_DEFAUT` : `2025-09-01` → `2026-09-05` | Date retenue par le propriétaire pour 2026-2027. |
| `test/calendrier.test.ts` | +9 contrôles sur 2026-2027 | Semaines, frontières, ouvertures, refus de date mal formée. |
| `test/parcours.test.ts` | +5 contrôles d'API | Variable d'environnement, ouverture des blocs, protection des blocs fermés. |
| `docs/CONTRAT-API.md` | § 11 créé, tableaux mis à jour | L'action Railway doit être écrite dans le contrat. |

**Le séquencement pédagogique n'a pas été touché** : B1 en S1, B2 en S5, B3 en S10.
Ces semaines viennent du référentiel annuel ; elles sont désormais **vérifiées par
test**, ce qui les protège d'une modification involontaire.

---

## 3. Solution retenue pour la date de début d'année

### 3.1 Ce qui a été choisi

`ANNEE_SCOLAIRE_DEBUT` **n'est pas codée en dur** : la route la lit à chaque appel
(`process.env.ANNEE_SCOLAIRE_DEBUT ?? DEBUT_ANNEE_DEFAUT`). Le changement porte
donc sur le **repli**, pas sur le mécanisme.

| Élément | Valeur |
|---|---|
| Repli dans le code | `2026-09-05` |
| Variable d'environnement | `ANNEE_SCOLAIRE_DEBUT`, prioritaire, à définir sur Railway |
| Séquencement | B1 · S1 · B2 · S5 · B3 · S10 — **inchangé** |

Le propriétaire peut ainsi changer d'année scolaire **sans redéploiement**.

### 3.2 Une conséquence à connaître : les semaines commencent le samedi

✅ **Vérifié.** Le 5 septembre 2026 est un **samedi**. Les semaines sont des blocs
de sept jours à partir de la date de rentrée :

| Jour | Semaine calculée |
|---|---|
| sam. 5 sept. 2026 | 1 |
| ven. 11 sept. 2026 | 1 |
| **sam. 12 sept. 2026** | **2** |

Les ouvertures de blocs tombent donc **un samedi**, deux jours avant un découpage
lundi-dimanche : B2 le samedi 3 octobre, B3 le samedi 7 novembre.

C'est un comportement **cohérent et volontaire** — la rentrée est fixée au
5 septembre — mais ce n'est pas ce qu'un enseignant camerounais attend
habituellement, où l'année scolaire démarre généralement un lundi. ⏳ **À arbitrer
par le propriétaire** : soit il conserve le 5 septembre comme date de rentrée et
accepte des ouvertures le samedi, soit il fixe la rentrée au lundi 7 septembre.
Aucun code n'a été modifié sur ce point : c'est une décision, pas un défaut.

### 3.3 Le frontend ne dépend pas du calendrier

✅ **Vérifié.** `grep` sur `src/` : aucune lecture de date dans le frontend. Il
reçoit `anneeScolaire` du backend et l'affiche tel quel. Le correctif était donc
**entièrement backend** — aucun changement côté client n'était justifié.

---

## 4. Tests et vérifications

### 4.1 Résultats consolidés — ✅ Vérifié

| | Backend | Frontend |
|---|---|---|
| `npm run typecheck` | ✅ aucune erreur | ✅ aucune erreur |
| `npm test` | ✅ **155 / 155**, 30 suites | ✅ **42 / 42**, 8 suites |
| `npm run build` | ✅ | ✅ |

Progression depuis le chantier 7 : **175 → 197 tests** (+22).

### 4.2 Le parcours élève complet, dans un vrai navigateur

✅ **Vérifié.** Serveurs réels compilés (`dist/server.js` et le build
`output: standalone`, c'est-à-dire exactement ce que Vercel déploie), puis pilotage
de **Chromium headless en 390 × 844** (taille d'un téléphone). Client CDP écrit
spécifiquement pour ce contrôle, sans dépendance ajoutée au projet.

| # | Étape | Résultat observé |
|---|---|---|
| 1 | Accueil | `Prépare ton BEPC de mathématiques` |
| 2 | Clic sur « Voir le parcours » | ✅ le bouton existe et répond |
| 3 | Page atteinte | `/parcours` — « Ton parcours de mathématiques » |
| 4 | Position dans l'année | « **Semaine 6** de l'année scolaire. » |
| 5 | Blocs accessibles | B1 : 6 exercices · B2 : 3 exercices · B3 : **0** |
| 6 | Bloc fermé expliqué | « Disponible à partir de la semaine 10. » |
| 7 | Ouverture d'un exercice | `/parcours/MVP-B2-E1` — énoncé et consigne affichés |
| 8 | Saisie d'une réponse | champ `#reponse` alimenté, bouton « Vérifier » actif |
| 9 | **Correction juste** | `5√2` → « Ta réponse est juste. » |
| 10 | **Correction fausse** | `7√2` → « Ce n'est pas encore juste. » |
| 11 | **Correction partielle** | `√50` → « Ta réponse est juste, mais pas dans la forme demandée. » |
| 12 | **Indices progressifs** | « Indice 1. On distribue le 3 dans (x + 2)… » |
| 13 | Bloc fermé, contournement | `MVP-B3-E1` → « Cet exercice n'est pas disponible pour le moment. » |
| 14 | Affichage mobile | `scrollWidth ≤ innerWidth` — **aucun débordement horizontal** |

Les trois statuts de correction ont donc été observés **rendus à l'écran**, pas
seulement dans la réponse API.

### 4.3 Protection des blocs fermés — ✅ Vérifié

Cinq routes contrôlées en semaine 1 (seul B1 ouvert), sur l'année 2026-2027 :

| Route | Résultat |
|---|---|
| `GET /api/v1/exercices/MVP-B3-E1` | **403** |
| `GET /api/v1/exercices/MVP-B3-E1/indice/1` | **403** |
| `GET /api/v1/exercices/MVP-B2-E1/indice/2` | **403** |
| `POST /api/v1/corrections` (B3) | **403** — « …s'ouvre en semaine 10 » |
| `POST /api/v1/progression` (B2) | **403** |

Et le même exercice B1, ouvert, répond **200**. Le garde-fou n'est pas un
blocage global : il discrimine correctement.

### 4.4 Les nouveaux tests peuvent-ils échouer ?

Un test qui passe toujours ne prouve rien. Les contrôles ont été **déclenchés
volontairement** :

| Défaut injecté | Contrôle qui a mordu |
|---|---|
| Bouton retiré ou pointant vers `/` | « Le bouton a disparu de la page d'accueil » ✅ |
| Lien vers `/tuteur` (fonctionnalité inexistante) | « Lien vers une fonctionnalité non implémentée » ✅ |
| Lien mort `/parcours-absent` | « pointe vers une route qui n'existe pas » ✅ |

Le troisième cas a d'abord **échappé** au contrôle : le motif de recherche ne
voyait pas les liens en gabarit `` href={`…`} ``. Le test a été corrigé pour couvrir
les deux écritures, puis re-vérifié — il détecte désormais le lien mort.

### 4.5 Absence de dépendance à l'horloge — ✅ Vérifié

La suite 2026-2027 écrit **toutes** ses dates explicitement (`2026-10-06`,
`2027-03-29`…). Aucun test ne lit `new Date()`. Conséquence : les résultats sont
identiques le 5 septembre, le 10 octobre ou dans trois ans.

Le chantier 7 avait déjà rendu les tests d'API indépendants de l'horloge ;
ce chantier l'a étendu au module de calcul lui-même.

---

## 5. Résultats du typecheck et des builds — ✅ Vérifié

| Commande | Backend | Frontend |
|---|---|---|
| `npm run typecheck` | Aucune erreur | Aucune erreur |
| `npm run build` | `tsc --project tsconfig.build.json` | `next build`, 4 routes |

Une erreur de type a été trouvée et corrigée pendant ce chantier : le nouveau
`navigation.test.ts` violait `noUncheckedIndexedAccess`. **Le contrôle de type
l'a détectée**, ce qui confirme sa valeur — le fichier n'aurait pas dû être
commité autrement.

Contrôle du bundle après build :

| Contrôle | Résultat |
|---|---|
| Contenu d'épreuve BEPC dans `.next/static` | ✅ absent |
| Secret dans `.next/static` | ✅ absent |
| Enoncé d'exercice embarqué | ✅ absent |

---

## 6. Vérifications de navigation et du calendrier — ✅ Vérifié

| Contrôle | Résultat |
|---|---|
| Bouton « Voir le parcours » présent sur l'accueil | ✅ |
| Clic → `/parcours` → parcours de mathématiques | ✅ observé dans Chromium |
| Bloc ouvert → exercice cliquable | ✅ 9 liens observés (6 B1 + 3 B2) |
| Bloc fermé → aucun exercice, message explicite | ✅ |
| Retour vers l'accueil depuis le parcours et un exercice | ✅ |
| Page d'état des fonctionnalités conservée et séparée | ✅ présente, après le parcours |
| Aucun lien vers tuteur / comptes / tableau de bord | ✅ |
| Semaines B1/B2/B3 = 1/5/10 en 2026-2027 | ✅ vérifié par test et en HTTP |
| `ANNEE_SCOLAIRE_DEBUT` prioritaire sur le repli | ✅ vérifié par test |
| Frontend indépendant du calendrier | ✅ |

---

## 7. Commits publiés — ✅ Vérifié

| Dépôt | Commit | Objet |
|---|---|---|
| `relio-backend` | `251f2a3` | `fix(calendrier): année scolaire 2026-2027 au 5 septembre 2026` |
| `relio-frontend` | `f6f85f2` | `fix(parcours): rendre /parcours dynamique pour lire la config à l'exécution` |

Poussés sur `main`. Les deux dépôts ont été rebasés au préalable sur les commits
CI reçus entre-temps ; les tests ont été rejoués après rebase.

---

## 8. Actions manuelles restantes

### 8.1 Railway — action requise

⏳ **À faire par le propriétaire.** Le backend a besoin de cette variable :

```
ANNEE_SCOLAIRE_DEBUT=2026-09-05
```

> **Pourquoi c'est obligatoire et pas seulement recommandé.** Le repli du code vaut
> déjà `2026-09-05`, donc l'application fonctionnerait sans la variable. Mais une
> variable **périmée** qui traîne dans l'environnement Railway aurait priorité sur
> le code et refermerait de nouveau tous les blocs. Il faut donc **vérifier la
> valeur réellement enregistrée**, et la remplacer si elle vaut encore 2025.

Emplacement : Railway → projet `relio-backend` → service → onglet **Variables** →
`ANNEE_SCOLAIRE_DEBUT`. Un redémarrage du service est nécessaire pour qu'elle
prenne effet.

### 8.2 Vercel — actions requises

| # | Action | Détail |
|---|---|---|
| 1 | **Redéployer le frontend** | Le correctif `force-dynamic` est dans le code. Un simple rechargement ne suffit pas : Vercel doit rebuild. |
| 2 | **Vérifier `API_BASE_URL`** | Elle doit pointer vers le domaine Railway (ex. `https://…up.railway.app`), sans slash final — la normalisation retire les slashs, mais mieux vaut une valeur propre. |
| 3 | **Vérifier `CORS_ORIGINS`** sur Railway | Doit contenir le domaine Vercel exact (ex. `https://…vercel.app`). Sans cela, le navigateur bloque la requête et l'élève voit « service indisponible » — le message que ce chantier vient de corriger. |

### 8.3 Après redéploiement — contrôle par le propriétaire

Le parcours à rejouer, dans l'ordre. C'est la validation en production qui n'a
**pas** été faite ici :

1. Ouvrir le site → cliquer « Voir le parcours » → **le parcours doit s'afficher**
2. Vérifier que les blocs ouverts **listent des exercices cliquables**
3. Ouvrir un exercice → saisir la réponse → **obtenir un verdict**
4. Demander un indice → **obtenir le palier suivant**
5. Ouvrir directement l'URL d'un exercice d'un bloc fermé → **« non disponible »**

Si le parcours reste vide, deux causes probables, dans cet ordre :
`API_BASE_URL` absente ou incorrecte sur Vercel, puis `CORS_ORIGINS` ne
contenant pas le domaine Vercel.

### 8.4 Décision pédagogique à trancher

⏳ **Le 5 septembre 2026 est un samedi** (§ 3.2). Confirmer si les ouvertures le
samedi sont acceptables, ou si la rentrée doit être fixée au lundi 7 septembre.
Aucun code n'a été modifié sur ce point.

---

## 9. Contrôles réellement effectués en production

**Aucun.** ⏳

Ce chantier n'a **pas** accès à Vercel ni à Railway. Aucune commande de
redéploiement n'a été passée. Tout ce qui a été vérifié l'a été **en local**,
contre des serveurs réellement compilés et un vrai navigateur — ce qui est plus
qu'un test unitaire, mais ce qui **n'est pas** de la production.

L'hypothèse que la production soit configurée avec les bonnes valeurs
(`API_BASE_URL`, `CORS_ORIGINS`, `ANNEE_SCOLAIRE_DEBUT`) **n'est pas vérifiée** et
relève du contrôle du propriétaire (§ 8).

---

## 10. Réserves et problèmes ouverts

### 10.1 Ce que ce chantier ne corrige pas

| # | Réserve | Effet |
|---|---|---|
| R1 | **La lecture « juste mais mal formé » (D5) reste non arbitrée.** Inchangé depuis le chantier 7. | `√50` reste `partielle` avec `lectureArbitree: false`. Un mot de l'enseignant suffit à trancher. |
| R2 | **Hypothèse H1 non testée** — rien n'établit qu'un élève saisisse une expression sur son téléphone. | Risque principal du projet, non levé. Le chantier 7 l'avait désigné. |
| R3 | **Visibilité du dépôt GitHub** (contenus officiels du BEPC versionnés) — non vérifiée. | Juridique. |
| R4 | **État de la CI non observé** — `gh` absent de l'environnement. | Les commandes passent localement ; l'exécution sur GitHub n'est pas prouvée. |

### 10.2 Une réserve sur la solution elle-même

Le correctif `force-dynamic` règle le problème, mais **mérite une surveillance** :
la page est désormais rendue à chaque requête, ce qui implique un appel réseau au
backend à chaque visite. Pour une page consultée par un élève sur un forfait
mobile, c'est un coût réel.

C'est le prix de la correction : sans elle, la configuration de production ne peut
jamais être lue. Alternatives écartées — un cache court (la page dépend de la
semaine, mais celle-ci ne change que chaque semaine), ou la lecture de la
configuration côté client (elle exposerait l'URL dans le bundle). **Si la
performance devient un problème, un cache de quelques minutes serait la première
piste à essayer** — pas avant d'avoir une mesure.

### 10.3 Ce que ce chantier a appris sur la méthode

Le défaut de navigation **était invisible à toute la chaîne de vérification** :
typecheck vert, build vert, tests API verts, 140 tests verts. Rien n'y renvoyait.

Il n'a été trouvé que parce que le parcours a été suivi **dans un navigateur, en
cliquant réellement**, après avoir lancé les serveurs **tels qu'ils seraient
déployés** (`output: standalone`, et non `next start`, qui ne reproduit pas la
configuration de Vercel).

Le test `navigation.test.ts` et la directive `force-dynamic` traitent le symptôme.
Ce qui reste à installer durablement, c'est l'habitude de **suivre le parcours
après build**, dans un navigateur, sur la configuration de production simulée.

---

## 11. Statut du chantier

# 🟠 TERMINÉ AVEC RÉSERVES

**Les deux problèmes signalés sont corrigés, démontrés et publiés.**

- Le bouton « Voir le parcours » mène bien au parcours de mathématiques, vérifié
  dans un vrai navigateur en taille mobile : énoncé, saisie, correction juste /
  fausse / partielle, et indices progressifs ont tous été observés rendus à
  l'écran.
- Le calendrier est réglé sur l'année 2026-2027 avec une rentrée au 5 septembre,
  et les trois blocs s'ouvrent bien aux semaines 1, 5 et 10.
- 197 tests passent, typecheck et builds sont verts dans les deux dépôts.

**Quatre réserves motivent de ne pas conclure en « TERMINÉ » :**

1. **Rien n'est vérifié en production.** Ni Vercel ni Railway ne sont accessibles
   depuis ce chantier. La correction est prouvée en local, sur des serveurs
   réellement compilés et dans un navigateur réel — ce qui est solide, mais ce
   n'est pas du même ordre qu'un contrôle sur le site déployé. C'est précisément
   pour cela que le contrôle post-déploiement du § 8.3 est écrit à l'avance.

2. **La configuration de production n'est pas contrôlée.** `API_BASE_URL` et
   `CORS_ORIGINS` peuvent être erronés sur Vercel et Railway. Dans ce cas, le
   parcours restera vide — et le message affiché laissera croire à une
   indisponibilité de service, pas à une configuration manquante.

3. **Une décision attend le propriétaire :** le 5 septembre 2026 est un samedi,
   donc les blocs s'ouvrent un samedi. C'est cohérent, mais inhabituel pour une
   rentrée scolaire.

4. **Les réserves du chantier 7 subsistent** — la lecture D5 non arbitrée et
   l'hypothèse H1 non testée. Elles ne bloquent pas la livraison, mais ce sont
   les deux points les plus susceptibles de ne pas être encore justes.

---

*Documents liés : `docs/rapport-final-chantier-7.md`,
`data/referentiel-maths-3e-cm-2025-2026.json`.
Contrats : `relio-backend/openapi.yaml`, `relio-backend/docs/CONTRAT-API.md`.*
