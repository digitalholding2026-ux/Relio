# Rapport final — Chantier 5 : corrections de fiabilité et tests automatisés

**Date** : 2026-10-10
**Révision auditée** : `5c517b5e856165463157a123ce90a9af1b9fb149`
**Statut global** : ⚠️ **Corrections principales appliquées et vérifiées en production**
🔴 **CI GitHub Actions NON activée** — blocage de droits, action manuelle requise

---

## 1. Résumé exécutif

**Corrections appliquées et poussées :**

| Correction | Dépôt | État |
|---|---|---|
| Vulnérabilité `postcss` (élevée) + `next` (modérée) | frontend | ✅ **VALIDÉ** — 0 vulnérabilité |
| Documentation du comportement au build de `API_BASE_URL` | frontend | ✅ **VALIDÉ** |
| 13 tests du contrôle de connexion API | frontend | ✅ **VALIDÉ** — 13/13 |
| 27 tests de l'API (routes, erreurs, CORS, configuration) | backend | ✅ **VALIDÉ** — 27/27 |
| Neutralisation des messages d'erreur 4xx (divulgation Fastify) | backend | ✅ **VALIDÉ** — vérifié **en production** |
| Journalisation silencieuse sous test | backend | ✅ **VALIDÉ** |

**Non réalisé :**

| Élément | Cause |
|---|---|
| CI GitHub Actions | 🔴 Le jeton n'a pas le scope `workflow`. **Aucune permission pour l'élargir.** |

**Décision proposée : acceptable sous réserves**, les trois réserves P1/P2 du
chantier 4 (R1, R3, R5) étant levées. La CI reste le point ouvert.

---

## 2. Fichiers modifiés par dépôt

### `relio-frontend` — commit `b148b90`

| Fichier | Action | Contenu |
|---|---|---|
| `package.json` | modifié | Ajout `overrides`, script `test`, dépendance dev `tsx` |
| `package-lock.json` | modifié | `postcss` 8.4.31 → 8.5.29, `tsx` ajouté |
| `README.md` | modifié | Documentation `API_BASE_URL` + section dépendances |
| `src/lib/api.test.ts` | **créé** | 13 tests |
| `.github/workflows/ci.yml` | **créé, non commité** | Workflow CI |

### `relio-backend` — commit `2d1c91a`

| Fichier | Action | Contenu |
|---|---|---|
| `package.json` | modifié | Script `test` |
| `src/plugins/error-handler.ts` | modifié | Messages 4xx neutralisés |
| `src/app.ts` | modifié | Journalisation silencieuse sous test |
| `tsconfig.json` | modifié | Inclut `test/**/*.ts` pour le typecheck |
| `test/api.test.ts` | **créé** | 27 tests |
| `.github/workflows/ci.yml` | **créé, non commité** | Workflow CI |

### `Relio` — dépôt documentaire

**Uniquement** ce rapport. Aucun document pédagogique modifié.
Empreintes SHA-256 des deux JSON **inchangées** (`f766f412…`, `d74a68fb…`).

---

## 3. Vulnérabilités : identification et état après correction

### Diagnostic

| Élément | Valeur |
|---|---|
| Paquet vulnérable | `postcss` |
| **Type** | **Transitif** — non déclaré dans `package.json` |
| Chemin | `relio-frontend` → `next@15.5.27` → `postcss@8.4.31` |
| Plage vulnérable | `<= 8.5.22` |
| Version corrigée | `> 8.5.22` → `8.5.29` (dernière publiée) |
| Avis associés | 4 (XSS CSS, lecture arbitraire, correction incomplète, traversée de chemin) |
| `next` | marqué modéré **uniquement** parce qu'il embarque `postcss` |

**Point important vérifié** : `next@15.5.27` est la **dernière version 15.x**
(81 versions stables au total). **Aucun patch correctif n'existe sur cette
branche.** La seule alternative aurait été `next@16`, une **rupture majeure**.

### Correctif appliqué

```json
"overrides": { "postcss": "^8.5.29" }
```

**Justification de la version imposée** : passage de `8.4.31` à `8.5.29`, soit la
**même major `8.x`** — compatible au sens de SemVer. `8.5.29` est la dernière
version publiée et corrige les quatre avis. Le paquet n'est pas mis à jour
« pour être mise à jour », mais pour franchir la frontière de sécurité.

**`npm audit fix --force` n'a PAS été lancé.** Il aurait installé `next@16.4.0`.

### Preuve de compatibilité

| Contrôle | Avant | Après |
|---|---|---|
| `npm audit` | 1 modérée + 1 élevée | ✅ **0 vulnérabilité** |
| `next` installé | 15.5.27 | **15.5.27 — inchangé** |
| `postcss` installé | 8.4.31 | **8.5.29 (overridden)** |
| `npm run typecheck` | OK | ✅ OK |
| `npm run build` | OK | ✅ OK |
| **CSS produit, comparaison byte-à-byte** | — | ✅ **IDENTIQUE** (sha `eb5dbe11…` avant et après) |
| `npm ci` (lockfile) | — | ✅ reproductible |
| Idempotence après `npm install` | — | ✅ `postcss` reste en 8.5.29 |

**La production du CSS étant byte-identique**, l'override ne modifie pas le
traitement CSS de ce projet. Risque de régression : nul.

**Aucune alerte restante n'a été masquée** : `npm audit` ne signale plus rien.

---

## 4. Tests réellement exécutés

### Frontend — `src/lib/api.test.ts`

**13 tests, 13 réussis, 0 échec.**
`fetch` est remplacé par un stub local : **aucune connexion sortante, aucun
contact avec la production**, exécution déterministe.

| Cas couvert |
|---|
| URL non configurée → `non-configure` |
| Contrat valide → `joignable` avec version et statut |
| URL, méthode, `cache: 'no-store'` effectivement utilisés |
| 404 → `desaccord` |
| 500 → `indisponible` |
| Réponse hors contrat → refusée |
| 4 réponses incomplètes → **aucune** considérée comme joignable |
| Panne réseau (`TypeError`) → `indisponible` |
| `AbortError` (délai dépassé) → `indisponible` |
| Délai borné (constante testée) |
| `AbortSignal` transmis à `fetch` |
| 5 pannes différentes → aucune exception propagée |

### Backend — `test/api.test.ts`

**27 tests, 27 réussis, 0 échec.**
`app.inject()` : dispatch **en mémoire**, **aucun port ouvert**, aucun trafic
sortant.

| Suite | Nombre | Contenu |
|---|---|---|
| `GET /health` | 6 | 200, structure JSON, horodatage ISO, **aucun secret dans la réponse**, **aucune version de dépendance**, refus des méthodes non-GET |
| `GET /api/v1` | 4 | 200, version `v1`, statut `socle`, **routes réellement exposées** |
| Routes inconnues | 2 | 404 au format commun, **aucune stack trace** |
| Erreurs contrôlées | 3 | 400 sur JSON invalide, **message neutralisé**, format homogène |
| CORS | 5 | origine configurée acceptée ; origine inconnue, **suffixe usurpé**, liste vide refusés ; requête sans `Origin` acceptée |
| `loadConfig` | 7 | defaults, `PORT` non entier et hors plage, `NODE_ENV` inconnu, **`*` refusé en production**, origines malformées refusées, déduplication |

### Vérifications statiques et builds

| Commande | Backend | Frontend |
|---|---|---|
| `npm ci` (lockfile) | ✅ | ✅ |
| `npx tsc --noEmit` | ✅ 0 erreur | ✅ 0 erreur |
| `npm test` | ✅ 27/27 | ✅ 13/13 |
| `npm run build` | ✅ | ✅ |
| `npm audit` | ✅ 0 | ✅ **0** (corrigé) |
| Séquence CI complète rejouée | ✅ 4/4 étapes | ✅ 4/4 étapes |

---

## 5. Commandes ayant échoué

| Commande | Échec | Cause | Traitement |
|---|---|---|---|
| `npm test` (backend, 1ᵉʳ essai) | `Could not find 'test/**/*.test.ts'` | `sh` ne développe pas `**` : le motif exigeait un sous-dossier | Motif corrigé en `test/*.test.ts` |
| `npm test` (frontend) | idem en puissance | Même cause, masqué car le fichier est à un niveau de profondeur | Motif aligné en `src/*/*.test.ts` |
| `npx tsc --noEmit` (backend) | 0 erreur, mais **angle mort** | `tsconfig.json` n'incluait que `src/**/*.ts` → les tests n'étaient **pas** typecheckés | `test/**/*.ts` ajouté ; vérifié présent via `--listFiles` |
| `git push` (backend) | `remote rejected — refusing to allow a Personal Access Token to create or update workflow .github/workflows/ci.yml without workflow scope` | 🔴 Le jeton n'a pas le scope `workflow` | Commit scindé ; le reste a été poussé. Voir § 8 |
| `git push` (frontend) | idem | idem | idem |

**Commande qui n'a pas été exécutée** : `npm audit fix --force` — interdite par
le cahier des charges, et évitée car elle aurait installé `next@16`.

---

## 6. Résultats de build, de CI et commits

| Dépôt | Commit poussé | Contenu distant vérifié |
|---|---|---|
| `relio-frontend` | **`b148b90`** | `.env.example`, `.gitignore`, `README.md`, `next-env.d.ts`, `next.config.ts`, `package-lock.json`, `package.json`, `src`, `tsconfig.json` |
| `relio-backend` | **`2d1c91a`** | + `docs`, `test` |
| `Relio` | `5c517b5` (inchangé pendant les travaux) | + ce rapport |

**Workflows GitHub enregistrés : `0` sur les deux dépôts** — vérifié par API.
`total_count: 0`.

| Élément de CI | État |
|---|---|
| Fichier `ci.yml` écrit | ✅ 67 lignes, **YAML validé syntaxiquement** (parse), 2 jobs, 2 déclencheurs |
| Workflow enregistré sur GitHub | 🔴 **NON** |
| Exécution de la CI | 🔴 **NON VÉRIFIÉ** — aucun workflow n'a tourné |

⚠️ **Aucune affirmation d'une CI fonctionnelle n'est faite.** Le fichier existe
et sa syntaxe est valide ; son exécution n'a jamais eu lieu.

### Contenu prévu du workflow

- Déclencheurs : `push` sur `main`, `pull_request` vers `main`
- Node.js **22** — cohérent avec `cookie@2.0.1` qui exige `>= 22`
- Étapes : `npm ci` → `typecheck` → `test` → `build`
- Job `audit` séparé, `continue-on-error` : **informatif, non bloquant**
- Aucun secret requis
- **Aucun déploiement automatique ajouté**

---

## 7. Vérification en production après correctifs

Le push a déclenché un redéploiement automatique des deux plateformes.

| Contrôle | Résultat |
|---|---|
| Frontend `GET /` | ✅ **HTTP 200**, 92 ms |
| Backend `GET /health` | ✅ **HTTP 200** |
| Backend `GET /api/v1` | ✅ JSON, `v1`, `socle` |
| **Message d'erreur Fastify divulgué** | ✅ **CORRIGÉ** — `{"code":"BAD_REQUEST","message":"Requête invalide."}` |
| Redémarrage effectif | ✅ `uptime` descendu à **13 s** — preuve du redéploiement |
| 404 route inconnue | ✅ Message conservé : `Route inconnue : GET /inconnue` |
| CORS origine frontend | ✅ En-tête correct |

**Le correctif R5 est vérifié actif en production**, avec preuve de redéploiement.

---

## 8. Ancien identifiant GitHub — contrôle d'état

⚠️ **Aucune valeur n'est affichée, copiée ou reproduite.**

| Élément | Constat |
|---|---|
| Fichier | `/config/.git-credentials` |
| Présence | ✅ **Toujours présent** |
| Taille / permissions | 135 octets, `600` |
| Entrées | **1** — `https://<IDENTIFIANT_MASQUE>@github.com` |
| `credential.helper` global | `store` |
| `Relio` | `store` → **utilise encore cette entrée** |
| `frontend`, `backend` | helper **désactivé localement** → n'utilisent pas l'entrée |
| Accès lecture `Relio` | ✅ Fonctionne via l'entrée stockée |

### Conclusion

🔴 **L'ancien identifiant n'est PAS éliminé.** Il est **présent et actively
utilisé** par le dépôt `Relio`.

### Pourquoi je ne l'ai pas supprimé

Le supprimer **casserait immédiatement les pushes vers `Relio`** : c'est
aujourd'hui le seul moyen d'authentification disponible pour ce dépôt (le helper
`store` est global, et j'ai au contraire **désactivé** le helper dans les deux
nouveaux dépôts lors du chantier 2 pour les forcer à utiliser `GIT_ASKPASS`).
Passer d'une authentification qui fonctionne à aucune serait une **régression**.

### ⚠️ Distinction essentielle

> **Supprimer l'entrée locale ne révoque PAS le jeton.**
> Nettoyer `~/.git-credentials` est une opération **locale**. Si le jeton a été
> exposé (historique de shell, sauvegarde, journal), il reste **valide sur
> GitHub** tant qu'il n'y est pas **révoqué explicitement** dans les paramètres
> du compte. Les deux actions sont **indépendantes**.

### Procédure manuelle recommandée — ordre impératif

1. **Vérifier le périmètre** du jeton stocké, sans jamais l'afficher ni le
   transmettre :
   ```
   GitHub → Settings → Developer settings → Personal access tokens
   ```
   Repérer le jeton correspondant, lire ses périmètres et sa date de création.

2. **Révoquer** ce jeton sur GitHub (bouton *Delete*). Cette étape suffit à
   neutraliser le risque : un jeton révoqué est inutilisable, même s'il figure
   encore dans le fichier local.

3. **Configurer** une authentification de remplacement **avant** de nettoyer :
   ```
   git config --global credential.helper ""
   ```
   puis fournir `GIT_ASKPASS` lisant une variable d'environnement, sur le même
   modèle que celui utilisé dans ce chantier.

4. **Nettoyer** l'entrée, seulement après l'étape 3 :
   ```
   git credential reject <<< "protocol=https
   host=github.com"
   ```

**Aucun jeton ne doit être collé dans une conversation** pour cette opération.

---

## 9. Tableau de statut

| Élément | Statut | Preuve |
|---|---|---|
| Vulnérabilité `postcss` corrigée | `VALIDÉ` | `npm audit` → 0 ; CSS byte-identique |
| `next` inchangé, pas de rupture | `VALIDÉ` | 15.5.27 avant/après |
| `npm audit fix --force` non lancé | `VALIDÉ` | Non exécuté |
| Lockfile cohérent et reproductible | `VALIDÉ` | `npm ci` OK ; idempotent |
| Tests frontend | `VALIDÉ` | 13/13 |
| Tests backend | `VALIDÉ` | 27/27 |
| Typecheck backend (tests inclus) | `VALIDÉ` | `tsconfig` étendu ; `--listFiles` confirme |
| Build backend | `VALIDÉ` | `dist/` sans test |
| Build frontend | `VALIDÉ` | 104 kB |
| Neutralisation 4xx **en production** | `VALIDÉ` | Message observé + `uptime` 13 s |
| `API_BASE_URL` documenté | `VALIDÉ` | README, § dédié |
| Secrets dans les commits | `VALIDÉ` | Scan sur contenu commité : 0 |
| Scripts Railway inchangés | `VALIDÉ` | `npm run build` / `npm start` / `PORT` |
| Commits poussés | `VALIDÉ` | `b148b90`, `2d1c91a` |
| **CI GitHub Actions activée** | `ÉCHEC` | Jeton sans scope `workflow` ; `total_count: 0` |
| **CI exécutée avec succès** | `NON VÉRIFIÉ` | Aucun workflow n'a tourné |
| Ancien identifiant GitHub éliminé | `ÉCHEC` | Entrée présente et utilisée par `Relio` |
| Affichage mobile | `NON VÉRIFIÉ` | Aucun navigateur |
| Tests React du composant `ApiStatus` | `NON VÉRIFIÉ` | Hors périmètre, nécessite jsdom |

---

## 10. Actions manuelles restantes

| # | Action | Où | Pourquoi |
|---|---|---|---|
| **M1** | **Créer `.github/workflows/ci.yml`** dans les deux dépôts | GitHub (interface web) | 🔴 Le jeton n'a pas le scope `workflow`. Le fichier est prêt, 67 lignes, validé syntaxiquement. **Collez son contenu via l'interface GitHub** ou regénérez un jeton avec le scope `workflow` |
| **M2** | **Révoquer l'ancien jeton GitHub** | GitHub → Developer settings | Neutralise le risque (§ 8, étape 2) |
| **M3** | Configurer `GIT_ASKPASS` puis nettoyer `~/.git-credentials` | Votre machine | Évite de casser les pushes `Relio` |
| **M4** | Vérifier la version Node sur Railway (**22**) | Railway | `cookie@2.0.1` exige `>= 22` |
| **M5** | Confirmer que Vercel a bien redéployé après `b148b90` | Vercel | Le site répond 200, mais le détail du déploiement n'est pas vérifié |

> ⚠️ **Si Vercel ne redéploie pas automatiquement** après un futur push,
> l'override `postcss` ne sera appliqué en production qu'au prochain déploiement.

---

## 11. Risques encore ouverts

| # | Risque | Gravité | État |
|---|---|---|---|
| 1 | **Aucune CI active** — pas de garde-fou automatique | 🔴 Élevée | Action M1 |
| 2 | Ancien jeton présent et utilisé | 🟡 Moyenne | Actions M2 + M3 |
| 3 | `API_BASE_URL` figée au build — basculement d'API silencieux | 🟡 Moyenne | Documenté ; corriger si basculement fréquent |
| 4 | `ApiError` reste du code mort (aucune route métier) | 🟢 Faible | Attendu, point d'extension |
| 5 | Aucun `requestTimeout` / `connectionTimeout` | 🟢 Faible | Risque *slowloris*, sans base de données |
| 6 | Cibles tactiles ≈ 42 px (< 44 px) | 🟢 Faible | Non mesuré sur appareil |
| 7 | `output: 'standalone'` inutile sur Vercel | 🟢 Faible | Non corrigé, hors périmètre |
| 8 | Aucune route racine sur le backend | 🟢 Faible | `GET /` → JSON 404 |

---

## 12. Confirmation — aucune fonctionnalité pédagogique

| Élément | État |
|---|---|
| Diagnostic, exercices, tuteur IA | ❌ **Aucun** |
| Compte élève, authentification, espace enseignant | ❌ **Aucun** |
| Base de données, persistance | ❌ **Aucune** |
| Collecte de données d'élève | ❌ **Aucune** |
| Import de document BEPC | ❌ **Aucun** |
| Modification d'architecture | ❌ **Aucune** |
| Modification de Vercel / Railway | ❌ **Aucune** |
| Test destructif ou de charge en production | ❌ **Aucun** |

**Les modifications sont limitées au chantier 5** : dépendances (`postcss`),
scripts de test, gestion d'erreurs, configuration de typecheck, documentation,
et fichiers de test.

**Données pédagogiques** — empreintes identiques au début du chantier :
```
f766f412…  data/referentiel-maths-3e-cm-2025-2026.json
d74a68fb…  data/inventaire-questions-bepc-2025-2026.json
```

---

## 13. Décision proposée

**Chantier 5 : acceptable sous réserves.**

Trois des quatre réserves prioritaires du chantier 4 sont levées et vérifiées,
dont une **confirmée en production**. La quatrième — la CI — est bloquée par une
limite de droits qui ne relève pas de moi.

**Avant de commencer tout développement pédagogique :**

1. Créer les deux workflows CI (action **M1**) — sans eux, le moteur de
   diagnostic s'écrirait sans filet.
2. Révoquer l'ancien jeton (**M2**, **M3**).

Le moteur de recommandation reste, comme au chantier 4, la partie qui sera
réécrite après arbitrage pédagogique. Il ne doit pas être codé avant la
validation des objectifs par un enseignant.

**Le chantier suivant ne commence pas avant validation explicite.**

---

*Rapport précédent conservé : `docs/rapport-audit-fiabilite-chantier-4.md`.*
*Rapports des chantiers 1 et 2 : supprimés de `docs/` le 2026-10-10 pour ne conserver
que l'état courant.archivés dans l'historique Git, consultables au commit `efa8d1b`.*