# Référentiel numérique — Progression annuelle de mathématiques 3e

**Cameroun · 2025-2026 · Préparation BEPC**

Transcription structurée et contrôlée du document de progression annuelle fourni.
Ce dépôt ne contient **que des données** : aucune fonctionnalité, aucun moteur,
aucune intégration IA.

---

## Contenu du dépôt

| Fichier | Rôle |
|---|---|
| `docs/rapport-final-mission.md` | **Livrable 0** — rapport de fin de mission 1 (référentiel annuel) |
| `docs/rapport-final-mission-2.md` | **Rapport final mission 2** — analyse BEPC 2025-2026 |
| `data/inventaire-questions-bepc-2025-2026.json` | Inventaire structuré des 35 questions BEPC 2025-2026 |
| `docs/analyse-bepc-2025-2026.md` | Synthèse pédagogique des deux sessions |
| `docs/couverture-programme-bepc.md` | Couverture des 14 leçons par les questions observées |
| `docs/anomalies-documents-bepc.md` | 10 anomalies, ambiguïtés et incertitudes |
| `source-progression-maths-3e.jpg` | Document source d'origine, conservé tel quel |
| `data/referentiel-maths-3e-cm-2025-2026.json` | **Livrable 1** — données structurées |
| `docs/progression-maths-3e-2025-2026.md` | **Livrable 2** — représentation lisible administrateurs |
| `docs/rapport-controle-donnees.md` | **Livrable 3** — rapport de contrôle |
| `docs/incoherences.md` | **Livrable 4** — liste des incohérences détectées |
| `docs/integration-backoffice.md` | **Livrable 5** — proposition d'intégration |
| `outils/generer-referentiel.py` | Génération du JSON à partir de la transcription |
| `outils/valider-referentiel.mjs` | Contrôle de cohérence du référentiel annuel (sans dépendance) |
| `outils/generer-inventaire-bepc.py` | Génération de l'inventaire des questions BEPC 2025-2026 |
| `outils/valider-inventaire-bepc.mjs` | Contrôles qualité de l'inventaire BEPC (sans dépendance) |

---

## Reproduire et vérifier

### 1. Régénérer le JSON

```bash
cd /config/Relio
python3 outils/generer-referentiel.py
```

Sortie attendue :

```
OK -> /config/Relio/data/referentiel-maths-3e-cm-2025-2026.json
  leçons     : 14  = 98 h
  régulations : 14 = 14 h
  révisions   : 1 = 8 h
  TOTAL       : 120 h (annoncé : 120 h)
```

### 2. Contrôler la cohérence

```bash
cd /config/Relio
node outils/valider-referentiel.mjs
```

Ou sur un autre fichier :

```bash
node outils/valider-referentiel.mjs chemin/vers/autre-referentiel.json
```

**Codes de sortie :**

| Code | Signification |
|---|---|
| `0` | Contrôle conforme, aucune réserve |
| `1` | Anomalie bloquante (données incohérentes) |
| `2` | Contrôle passé, réserves à documenter — **état actuel** |

L'état attendu est `2` : les trois réserves correspondent aux points A-2, A-3/A-4
de `docs/incoherences.md`, qui doivent être arbitrés par le responsable pédagogique.

### Prérequis

- Python 3 (standard, aucune bibliothèque tierce)
- Node.js 18+ (aucun `npm install` : le validateur n'utilise que `node:fs` et `node:path`)

### Exécution du validateur en CI

```bash
node outils/valider-referentiel.mjs && echo "OK" || echo "À examiner (code $?)"
```

---

## Chiffres clés

| Indicateur | Valeur |
|---|---|
| Leçons principales | **14** |
| Volume des leçons | **98 h** |
| Périodes de régulation | **14 × 1 h = 14 h** |
| Révision finale | **8 h** |
| **Total** | **120 h** — conforme aux 120 h annoncés |
| Trimestres | 3 (S1–S11, S12–S21, S22–S30) |
| Mois | 9 (Septembre → Mai) |
| Semaines | 30 × 4 h |

Statut de validation : **`valide_avec_reserves`**.

---

## Règles respectées

- **Aucune leçon inventée** — les 14 leçons et leurs volumes sont recopiés du document.
- **Aucune donnée pédagogique inventée** — `competences`, `prerequis`, `exercices`,
  `corriges`, `references_bepc` existent dans le modèle mais sont **vides**.
- **Aucune correction silencieuse** — les anomalies du document source sont
  signalées dans `docs/incoherences.md`, pas arbitrées.
- **Identifiants stables et techniques** — les intitulés ne servent jamais de clé.
- **Pas de dépendance IA** — format JSON standard, aucun SDK, aucun appel réseau.
- **Pas de fonctionnalité hors MVP** — uniquement des données et leur contrôle.

---

## Points en attente d'arbitrage

1. Colonne « Taux d'exécution » du document (dénominateur **112 h** vs 120 h annoncés) — aujourd'hui **exclue** du référentiel.
2. La révision de **8 h** sur une seule semaine de 4 h — hypothèse « S29–S30 » **non appliquée**.
3. Ventilation horaire des leçons entre leurs semaines — non fournie par la source, **non inventée**.

Voir `docs/incoherences.md` et `docs/rapport-controle-donnees.md` § 5.

---

## Mission 2 — Analyse BEPC 2025-2026

Les sujets et corrigés harmonisés du BEPC Mathématiques 2025 et 2026 ont été
analysés et reliés au référentiel annuel.

| Indicateur | Valeur |
|---|---|
| Documents analysés | 4 (2 sujets, 2 corrigés) — 11/11 pages lues |
| Questions inventoriées | 35 (17 en 2025, 18 en 2026) |
| Exercices et tâches | 18 |
| Barème recompté | **20 pt** par session — conforme aux documents |
| Leçons couvertes | **13 / 14** |
| Leçon non observée | **L6 — Angles inscrits** (5 h au programme) |
| Associations incertaines | 8 sur 49, toutes signalées |
| Anomalies documentées | 10 |
| Compétences officielles inventées | **0** |

**Reproduire :**

```bash
python3 outils/generer-inventaire-bepc.py
node     outils/valider-inventaire-bepc.mjs
```

> 🔒 **Droits d'utilisation NON VÉRIFIÉS.** Les sujets, figures et corrigés
> harmonisés sont publiés par la Direction des Examens, des Concours et de la
> Certification du Cameroun. Aucune republication dans l'application n'est
> autorisée avant vérification — voir `docs/anomalies-documents-bepc.md` (D-1).
>
> L'inventaire est un **outil d'analyse interne**. Son statut est
> `analyse_provisoire_en_attente_de_validation_humaine` : il n'est pas publié.

Le référentiel annuel **n'a pas été modifié** : ses identifiants sont
uniquement référencés depuis l'inventaire.

---

## Mission 3 — Spécification du diagnostic initial

| Fichier | Rôle |
|---|---|
| `docs/matrice-couverture-competences.md` | Couverture des 14 leçons, objectifs documentés vs déduits |
| `docs/specification-diagnostic-initial.md` | Mini-évaluation du MVP — 5 questions originales |
| `docs/regles-recommandation-pedagogique.md` | Règles d'interprétation et parcours post-diagnostic |
| `docs/rapport-final-mission-3.md` | Rapport de fin de mission 3 |

> ⚠️ **Ces 4 documents ne sont pas validés** par un enseignant. Ils constituent
> une spécification provisoire, pas une référence pédagogique opposable.

---

## Chantier 1 — Audit technique et préparation de la séparation

> 🔴 **Ce dépôt ne contient aucun code applicatif** — ni frontend, ni backend.

| Fichier | Rôle |
|---|---|
| `docs/audit-migration-architecture.md` | État réel du dépôt, inventaire A→J, stack détectée |
| `docs/architecture-cible.md` | Architecture cible des deux dépôts, contrat API, sécurité |
| `docs/plan-migration-depots.md` | Destination de chaque fichier, séquence réversible |
| `docs/plan-deploiement-vercel-railway.md` | Configuration prévue Vercel / Railway, actions manuelles |
| `docs/rapport-final-chantier-1.md` | Rapport de fin de chantier 1 |

**Constat principal :** le chantier 2 ne sera pas une séparation mais une
**création**, à laquelle ne sera transposé qu'**un seul fichier** —
`data/referentiel-maths-3e-cm-2025-2026.json`.

**Règle de sécurité :** aucun contenu BEPC ne doit transiter vers le frontend,
qui est public par défaut. Voir `docs/architecture-cible.md` § 7.
