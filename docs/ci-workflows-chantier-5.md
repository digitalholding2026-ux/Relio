# CI GitHub Actions — contenu prêt à créer (chantier 5)

**Date** : 2026-10-10
**Statut** : 🔴 **workflows NON activés** — fichiers non poussés, raison expliquée au § 3

> Ce document contient le contenu **intégral et prêt à copier** des deux
> workflows. Il est stocké dans `Relio` (et non dans les dépôts applicatifs)
> précisément parce qu'un fichier situé à `.github/workflows/` ne peut pas être
> poussé avec le jeton actuel.

---

## 1. Vérification préalable — les workflows correspondent aux scripts réels

Chaque étape du workflow a été confrontée aux scripts `package.json` réellement
présents dans chaque dépôt.

| Étape du workflow | `relio-backend` | `relio-frontend` |
|---|---|---|
| `npm ci` | lockfile `v3` ✅ | lockfile `v3` ✅ |
| `npm run typecheck` | `tsc --noEmit` ✅ | `tsc --noEmit` ✅ |
| `npm test` | `node --import tsx --test test/*.test.ts` ✅ | `node --import tsx --test src/*/*.test.ts` ✅ |
| `npm run build` | `tsc --project tsconfig.build.json` ✅ | `next build` ✅ |

### Les motifs de test correspondent-ils aux fichiers réels ?

| Dépôt | Motif du script | Fichiers trouvés | Concordance |
|---|---|---|---|
| `relio-backend` | `test/*.test.ts` | `test/api.test.ts` | ✅ 1 fichier, motif correct |
| `relio-frontend` | `src/*/*.test.ts` | `src/lib/api.test.ts` | ✅ 1 fichier, motif correct |

> **Pourquoi un `*` et pas `**`** : GitHub Actions exécute les étapes avec
> `bash`. Sans l'option `globstar`, bash ne développe pas `**` — un motif
> `test/**/*.test.ts` exigerait un sous-dossier et échouerait. Les motifs
> utilisés ici ne dépendent **que** de `*`, donc ils fonctionnent sur n'importe
> quelle machine.

### Vérification réellement exécutée sur Node 22

La séquence exacte du workflow a été rejouée localement avec **Node v22.23.3**,
la version déclarée dans le workflow :

| Dépôt | `npm ci` | `typecheck` | `test` | `build` | Alerte moteur |
|---|---|---|---|---|---|
| `relio-backend` | ✅ | ✅ | ✅ **27 / 27** | ✅ | **0** |
| `relio-frontend` | ✅ | ✅ | ✅ **13 / 13** | ✅ | **0** |

`npm audit --audit-level=high` → `found 0 vulnerabilities` sur les deux dépôts.

> L'avertissement `EBADENGINE` observé au chantier 2 (`cookie@2.0.31` exige
> `>= 22`) **disparaît sous Node 22** : c'est une confirmation supplémentaire du
> choix de version.

**⚠️ ceci ne prouve PAS que la CI fonctionne.** Cela prouve que les commandes
passent sur Node 22. Un workflow GitHub n'a encore jamais été exécuté.

---

## 2. Contenu des workflows

### 2.1 `relio-backend/.github/workflows/ci.yml`

```yaml
name: CI

# Verification statique et tests uniquement.
# Aucun deploiement automatique : Vercel et Railway gerent les leurs.
# Aucun secret n'est necessaire : toutes les etapes sont publiques.

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

env:
  NEXT_TELEMETRY_DISABLED: '1'

jobs:
  verify:
    name: Typecheck, tests et build
    runs-on: ubuntu-latest

    steps:
      - name: Recuperer le code
        uses: actions/checkout@v4

      # Node 22 : une dependance transitive (cookie@2.0.1) exige >= 22.
      - name: Installer Node.js 22
        uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: npm

      # Installation reproductible a partir du lockfile.
      - name: Installer les dependances
        run: npm ci

      - name: Verification des types
        run: npm run typecheck

      - name: Tests automatises
        run: npm test

      - name: Build de production
        run: npm run build

  audit:
    name: Audit de dependances (informatif)
    runs-on: ubuntu-latest
    # Ne bloque pas la fusion : le resultat est publie, la decision reste humaine.
    continue-on-error: true

    steps:
      - name: Recuperer le code
        uses: actions/checkout@v4

      - name: Installer Node.js 22
        uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: npm

      - name: Installer les dependances
        run: npm ci

      - name: Audit npm
        run: npm audit --audit-level=high
```

### 2.2 `relio-frontend/.github/workflows/ci.yml`

**Identique au précédent**, à une seule différence : le nom du job `verify`
précise la technologie.

```yaml
name: CI

# Verification statique et tests uniquement.
# Aucun deploiement automatique : Vercel et Railway gerent les leurs.
# Aucun secret n'est necessaire : toutes les etapes sont publiques.

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

env:
  NEXT_TELEMETRY_DISABLED: '1'

jobs:
  verify:
    name: Typecheck, tests et build (Next.js)
    runs-on: ubuntu-latest

    steps:
      - name: Recuperer le code
        uses: actions/checkout@v4

      # Node 22 : une dependance transitive (cookie@2.0.1) exige >= 22.
      - name: Installer Node.js 22
        uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: npm

      # Installation reproductible a partir du lockfile.
      - name: Installer les dependances
        run: npm ci

      - name: Verification des types
        run: npm run typecheck

      - name: Tests automatises
        run: npm test

      - name: Build de production
        run: npm run build

  audit:
    name: Audit de dependances (informatif)
    runs-on: ubuntu-latest
    # Ne bloque pas la fusion : le resultat est publie, la decision reste humaine.
    continue-on-error: true

    steps:
      - name: Recuperer le code
        uses: actions/checkout@v4

      - name: Installer Node.js 22
        uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: npm

      - name: Installer les dependances
        run: npm ci

      - name: Audit npm
        run: npm audit --audit-level=high
```

---

## 3. Pourquoi je ne les ai pas poussés

Le push a été **rejeté par GitHub** :

```
remote: Permission to digitalholding2026-ux/relio-backend.git denied…
refusing to allow a Personal Access Token to create or update workflow
`.github/workflows/ci.yml` without `workflow` scope
```

GitHub exige qu'un jeton possède le **scope `workflow`** pour créer ou modifier
un fichier situé sous `.github/workflows/`.

**Je ne peux pas m'accorder ce scope moi-même** : cela modifierait les paramètres
de votre compte, ce qui sort de mes capacités.

Le contournement par l'interface GitHub (§ 5) est la voie prévue.

---

## 4. Ancien identifiant GitHub

### 4.1 État constaté le 2026-10-10 — aucune valeur affichée

Le contrôle a été réalisé en lisant l'entrée via `git credential fill`, en
la passant dans une variable, et en n'affichant qu'un **verdict**.

| Élément | Constat |
|---|---|
| Entrée présente | ✅ Oui — `/config/.git-credentials`, 1 entrée |
| **Jeton encore valide ?** | 🔴 **OUI — actif (HTTP 200)** |
| Périmètre sur `Relio` | 🔴 `admin: true`, `push: true` |
| Périmètre sur `relio-frontend` | 🔴 `admin: true`, `push: true` |
| Périmètre sur `relio-backend` | 🔴 `admin: true`, `push: true` |
| Visibilité des trois dépôts | Public |
| Distinct du jeton de session | ✅ Confirmé par comparaison |

> 🔴 **Correction par rapport au rapport du chantier 4** : celui-ci indiquait que
> ce jeton n'avait d'accès qu'à `Relio`. C'est **faux aujourd'hui** : il a
> `admin` sur les **trois** dépôts. Le périmètre a évolué depuis.
> **Il est donc plus urgent que signalé.**

### 4.2 Vérifier vous-même, sans rien afficher

Copiez ce bloc dans un terminal. **Il n'affiche jamais le secret.**

```sh
cred=$(printf 'protocol=https\nhost=github.com\n\n' | git credential fill 2>/dev/null)
token=$(printf '%s\n' "$cred" | sed -n 's/^password=//p')
[ -z "$token" ] && { echo "aucune entree"; exit 0; }

code=$(curl -s -o /dev/null -w '%{http_code}' -H "Authorization: Bearer $token" \
       https://api.github.com/user)
[ "$code" = 200 ] && echo "Jeton actif : OUI" || echo "Jeton actif : NON (HTTP $code)"

unset token cred
```

| Résultat | Signification |
|---|---|
| `Jeton actif : OUI` | Le jeton fonctionne encore → **il faut le révoquer** |
| `Jeton actif : NON (HTTP 401)` | Déjà révoqué → vous pouvez nettoyer l'entrée locale directement |

### 4.3 ⚠️ Deux actions distinctes, à ne pas confondre

| Action | Effet | Endroit |
|---|---|---|
| **Révoquer le jeton** | Le rend inutilisable, **où qu'il soit** | GitHub → Settings → Developer settings |
| **Nettoyer l'entrée locale** | Efface la copie sur disque | Votre machine |

> **Nettoyer le fichier local ne révoque RIEN sur GitHub.** Un jeton révoqué
> reste valide dans le fichier jusqu'à ce que le fichier soit, lui, nettoyé.
> Dans votre cas, **la révocation est l'action prioritaire** : elle suffit à
> neutraliser le risque, même si la copie locale subsiste.

### 4.4 Ordre impératif — ne pas inverser

**Ne supprimez l'entrée locale qu'une fois l'authentification de remplacement
opérationnelle.** Aujourd'hui, cette entrée est **la seule manière de pousser
vers `Relio`** : la supprimer d'abord casserait vos pushes.

```
1. RÉVOQUER le jeton sur GitHub          ← étape prioritaire, suffit à sécuriser
2. CONFIGURER l'authentification de remplacement
3. TESTER un push sur Relio
4. SEULEMENT ALORS nettoyer l'entrée locale
```

### 4.5 Préparer l'authentification de remplacement

À faire **avant** l'étape 4, sinon `Relio` devient inaccessible en écriture.

**a. Générer un nouveau jeton**

GitHub → Settings → Developer settings → *Personal access tokens* →
*Fine-grained tokens* → *Generate new token*.

Portée recommandée — **au minimum** :

| Ressource | Permission | Pourquoi |
|---|---|---|
| `Relio` | Contents → **Read and write** | commits du dépôt documentaire |
| `relio-frontend` | Contents → **Read and write** | commits applicatifs |
| `relio-backend` | Contents → **Read and write** | commits applicatifs |

> Si vous souhaitez que **je** pousse les workflows moi-même, ajoutez :
> **Workflows → Read and write**. Ce scope est précisément celui qui manque.

**b. Ne jamais coller ce jeton dans une conversation.** Écrivez-le dans un
fichier sur votre machine.

**c. Script d'authentification** (le secret reste dans une variable
d'environnement, jamais dans l'URL du dépôt ni dans `.git/config`) :

```sh
#!/bin/sh
# ~/bin/gh-askpass.sh   — chmod 700
# Utilise la variable RELIO_GITHUB_TOKEN, définie hors de tout dépôt git.
case "$1" in
  *sername*) printf '%s\n' "x-access-token" ;;
  *assword*) printf '%s\n' "$RELIO_GITHUB_TOKEN" ;;
esac
```

```sh
# Dans ~/.bashrc — hors de tout dépôt
export RELIO_GITHUB_TOKEN='…'
export GIT_ASKPASS=~/bin/gh-askpass.sh
export GIT_TERMINAL_PROMPT=0
```

**d. Désactiver le helper global qui lit le fichier obsolète**

```sh
git config --global credential.helper ""
```

**e. Tester avant de nettoyer**

```sh
cd ~/Relio   # ou votre clone
git ls-remote origin >/dev/null && echo "OK : authentification de remplacement operationnelle"
```

Tant que cette commande n'affiche pas `OK`, **ne supprimez rien**.

**f. Nettoyer l'entrée obsolète — seulement ensuite**

```sh
git credential reject <<'EOF'
protocol=https
host=github.com
EOF
```

Ou, si aucune authentification ne repose encore dessus :

```sh
rm -f ~/.git-credentials
```

> Vérification finale : `git credential fill` ne doit plus rien renvoyer pour
> `github.com`.

---

## 5. Procédure manuelle ordonnée

### A. Sécurité du jeton

| # | Action | Où | Preuve |
|---|---|---|---|
| A1 | Lancer le bloc § 4.2 | Votre terminal | Verdict affiché |
| A2 | **Révoquer** le jeton actif | GitHub → Settings → Developer settings → *Personal access tokens* | Le jeton disparaît de la liste |
| A3 | Vérifier qu'il est bien révoqué | Relancer § 4.2 | `Jeton actif : NON` |
| A4 | Préparer le remplacement | Voir § 4.5 | — |
| A5 | **Nettoyer l'entrée locale** | Votre machine | § 4.5, étape 5 |

### B. Mise en place de la CI

| # | Action | Précision |
|---|---|---|
| B1 | Ouvrir le dépôt `relio-backend` sur GitHub | — |
| B2 | **Add file → Create new file** | Onglet en haut |
| B3 | Frapper `.github/workflows/ci.yml` | La création des dossiers est automatique |
| B4 | Coller le contenu § 2.1 | **Supprimer la ligne d'ouverture ```` ```yaml ```` et la ligne de fermeture ```` ``` ````** |
| B5 | Choisir un message de commit, ex. `ci: ajouter le workflow CI` | — |
| B6 | **Commit changes** directement sur `main` | Laisse `main` cochée |
| B7 | Répéter B1 → B6 pour `relio-frontend` avec le contenu § 2.2 | — |
| B8 | Ouvrir l'onglet **Actions** du dépôt | — |

> 💡 Si vous préférez ne rien coller dans le navigateur : régénérez un jeton
> GitHub **avec le scope `workflow`** et donnez-moi son **nom** uniquement —
> je n'ai pas besoin de sa valeur dans la conversation. (Le canal sûr reste
> votre machine.)

### C. Configuration plateforme recommended

| # | Action | Où |
|---|---|---|
| C1 | Vérifier la version Node **22** | Railway → service settings |
| C2 | Confirmer que Vercel a redéployé après `b148b90` | Vercel → deployments |

---

## 6. Preuves à contrôler pour déclarer la CI validée

⚠️ **Un workflow écrit n'est pas une CI fonctionnelle.** Un run vert n'est pas
non plus la preuve que tout fonctionne. Voici les preuves exactes.

### 6.1 Le workflow existe et a été reconnu

| Preuve | Où | Attendu |
|---|---|---|
| Workflow listé | `Actions` → onglet latéral | `CI` apparaît |
| Fichier présent dans l'arbre | `Code` → `.github/workflows/ci.yml` | Le fichier s'affiche |
| `total_count` = 1 | API GitHub | Un seul workflow enregistré |

### 6.2 Le run s'est exécuté avec succès

Pour **chaque** dépôt :

| Preuve | Attendu |
|---|---|
| Badge à côté du nom du dépôt | ✅ vert |
| Onglet **Actions** → ligne `CI` | conclusion **Success** |
| Job `verify` | ✅ vert |
| Job `audit` | ✅ ou ⚠️ *(non bloquant, `continue-on-error`)* |

### 6.3 Les quatre étapes ont bien tourné

Cliquer sur le run → job `verify` → développer les quatre étapes :

| Étape | Attendu |
|---|---|
| `Installation des dependances` | ✅ — et le log montre une installation **depuis le lockfile** |
| `Verification des types` | ✅ |
| `Tests automatises` | ✅ — **le log doit afficher `# pass 27` (backend) ou `# pass 13` (frontend)** |
| `Build de production` | ✅ |

### 6.4 La version Node est bien 22

Dans le log de l'étape `Installer Node.js 22` :

```
Setting up node version '22.x.x'
```

Si Node 20 apparaît, le workflow n'a pas été pris en compte tel quel.

### 6.5 Le job d'audit est cohérent

| Preuve | Attendu |
|---|---|
| `Audit npm` terminé | `found 0 vulnerabilities` |

### 6.6 La CI se déclenche bien sur Pull Request

| Preuve | Attendu |
|---|---|
| Ouvrir une PR de test sur `main` | Une exécution `CI` apparaît, liée à la PR |
| Commentaire sur la PR | Le statut de contrôle apparaît (optionnel) |

> Ce point est le seul qui prouve le **déclencheur `pull_request`**. Un run
> issu d'un `push` ne le démontre pas.

### 6.7 Récapitulatif — la CI est validée si

- [ ] Le workflow est listé dans `Actions`
- [ ] Un run `CI` est terminé en **Success** sur `main` (chaque dépôt)
- [ ] Le job `verify` est vert
- [ ] Les 4 étapes sont vertes
- [ ] Le log des tests affiche `pass 27` (backend) / `pass 13` (frontend)
- [ ] Le log indique Node **22**
- [ ] Le job `audit` rapporte `0 vulnerabilities`
- [ ] Une Pull Request a déclenché une exécution

**Tant que ces 8 points ne sont pas tous cochés, la CI est `NON VÉRIFIÉ`.**

---

## 7. Contraintes respectées

| Contrainte | État |
|---|---|
| Pas de modification d'architecture | ✅ workflows seulement |
| Pas de modification Vercel / Railway | ✅ aucune action plateforme |
| Aucune fonctionnalité élève | ✅ aucune |
| Aucun secret dans les workflows | ✅ aucun `secrets.*` requis |
| Aucun déploiement automatique ajouté | ✅ aucun `deploy` job |
| Scripts alignés sur les scripts réels | ✅ § 1, vérifié dépôt par dépôt |
| Node 22 | ✅ et séquence rejouée localement sur v22.23.3 |

---

*Rapport associé : `docs/rapport-final-chantier-5.md`.*