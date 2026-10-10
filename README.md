# Référentiel numérique — Progression annuelle de mathématiques 3e

**Cameroun · 2025-2026 · Préparation BEPC**

Transcription structurée et contrôlée du document de progression annuelle fourni.
Ce dépôt ne contient **que des données** : aucune fonctionnalité, aucun moteur,
aucune intégration IA.

---

## Contenu du dépôt

| Fichier | Rôle |
|---|---|
| `source-progression-maths-3e.jpg` | Document source d'origine, conservé tel quel |
| `data/referentiel-maths-3e-cm-2025-2026.json` | **Livrable 1** — données structurées |
| `docs/progression-maths-3e-2025-2026.md` | **Livrable 2** — représentation lisible administrateurs |
| `docs/rapport-controle-donnees.md` | **Livrable 3** — rapport de contrôle |
| `docs/incoherences.md` | **Livrable 4** — liste des incohérences détectées |
| `docs/integration-backoffice.md` | **Livrable 5** — proposition d'intégration |
| `outils/generer-referentiel.py` | Génération du JSON à partir de la transcription |
| `outils/valider-referentiel.mjs` | Contrôle de cohérence (sans dépendance) |

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
