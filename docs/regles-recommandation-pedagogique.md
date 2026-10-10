# Règles de recommandation pédagogique et parcours post-diagnostic

**Mission** : 3 — Spécification pédagogique du diagnostic initial
**Version** : 1.0 — `en_attente_de_validation`
**Date** : 2026-10-10
**Statut** : ⚠️ spécification, **aucun développement avant validation**

Documents liés : `docs/matrice-couverture-competences.md`,
`docs/specification-diagnostic-initial.md`

---

## PARTIE A — RÈGLES D'INTERPRÉTATION

### A.1 Principe directeur

> **Le système produit des hypothèses, jamais des verdicts.**

Toute sortie du diagnostic est une **hypothèse de niveau**, assortie d'un niveau
de confiance explicite. Le mot « diagnostic » désigne le processus, pas un
état de l'élève.

---

### A.2 Enregistrement des réponses

**Principe : minimisation des données.** Le référentiel n'exige aucune donnée
personnelle, et rien dans le fonctionnement du diagnostic ne les rend nécessaires.

| ❌ Ne pas collecter | ✅ Collecter |
|---|---|
| Nom, prénom | Identifiant technique anonyme (généré localement) |
| Numéro de téléphone, e-mail | Statut par question (`correcte` / `partielle` / `fausse`) |
| Adresse, localisation | Objectif opérationnel concerné |
| Date de naissance, classe exacte | Horodatage de la session |
| Photo, profil social | Statut de chaque sonde déclenchée |

**Enregistrement minimal par question :**

```json
{
  "question_id": "ORIG-M3-Q02",
  "objectif_id": "OO-L1-1",
  "statut": "fausse",
  "signature_erreur": "signe_non_distribue",
  "tentatives": 1,
  "duree_ms": 42000
}
```

- `signature_erreur` : valeur d'un catalogue fermé (§ A.4), **jamais du texte libre**.
- `duree_ms` : indicative seulement, jamais utilisée seule pour conclure.
- **Aucune donnée nominative n'est transmise à un serveur tiers.**
- Purge automatique de l'historique brut au-delà de N mois (N à fixer — décision produit).

---

### A.3 Trois statuts, pas deux

| Statut | Définition | Exemple |
|---|---|---|
| `correcte` | Égale à une forme acceptée | `7/6` |
| `partielle` | Juste mais pas dans la forme demandée, ou étape intermédiaire correcte non achevée | `14/12`, `(2x+1−3)(2x+1+3)` |
| `fausse` | Autre chose | `11/6` |

**Pourquoi le statut `partielle` est indispensable.** Sans lui, une difficulté
mineure de forme est traitée comme une lacune de concept, et l'exercice
recommandé est le mauvais. `14/12` ne signifie pas « l'élève ne sait pas
 additionner des fractions » : il sait, il ne sait pas réduire.

**Traitement** : `partielle` **ne compte jamais comme `fausse`** pour déclencher
une alerte, et **ne compte pas comme `correcte`** pour certifier un acquis.

---

### A.4 Catalogue fermé des erreurs observées

Chaque réponse fausse est rattachée à une **signature** définie à l'avance. Cette
rigueur est ce qui permet de recommander la bonne activité au lieu d'en proposer
une au hasard.

| Signature | Détection | Leçon(s) candidates |
|---|---|---|
| `signe_non_reparti` | Q1 → `11/6`, `5/3` | L5 |
| `denominateur_non_reduit` | Q1 → `14/12` | L5 |
| `signe_non_distribue` | Q2 → `5x + 7` | L1 |
| `termes_non_collectes` | Q2 → `7x + 11 + x²` | L1 |
| `non_factorise` | Q3 → `4x² + 4x − 8` | L1 |
| `signe_inverse_dans_difference_carre` | Q3 → `(2x − 4)(2x + 2)` | L1, L3 |
| `signe_perdu_en_resolution` | Q4 → `5` | L8 |
| `resolution_incompletee` | Q4 → `10`, `−17` | L8 |
| `carre_parfait_non_extrait` | Q5 → `50√2` | L3 |
| `coefficient_multiplicatif_oublie` | Q5 → `6√2` | L3 |
| `base_racine_erronee` | Q5 → `11√3` | L3 |
| `hors_perimetre` | Toute autre réponse | — → **activité générique de reprise** |

**Signature inconnue → ne rien conclure de spécifique.** On ne devine pas.

---

### A.5 Erreur ponctuelle ou difficulté probable ?

**C'est la règle centrale de la mission.** Elle est purement statistique, et
l'honnêteté impose de reconnaître qu'**une question ne prouve rien**.

#### La règle des trois

Si un élève réussit `n` trials sans erreur, la borne supérieure à 95 % du taux
d'erreur réel est d'environ **3/n**.

| Items sur un objectif | Erreurs observées | Borne sup. taux d'erreur | Ce qu'on peut dire |
|---|---|---|---|
| 1 | 0 | **300 %** | **Rien.** Complètement indécisif |
| 1 | 1 | — | Une erreur isolée : rien de concluant |
| 2 | 0 | 150 % | Toujours indécisif |
| 3 | 0 | 100 % | Encore indécisif |
| **4** | **0** | **75 %** | On commence à avoir une information |
| 5 | 0 | 60 % | Information réelle |

> **Conséquence directe et non négociable :**
> **la mini-évaluation (1 item par objectif) ne peut mathématiquement produire
> aucune conclusion d'acquisition.** Elle peut seulement signaler des *difficultés
> ponctuelles* et déclencher des *sondes*.

#### Niveaux de conclusion autorisés

| Niveau | Condition | Libellé autorisé |
|---|---|---|
| **Signal** | 1 erreur sur 1 item | « Difficulté ponctuelle possible » |
| **Hypothèse** | 2+ erreurs sur le même objectif (mini-eval + sonde, ou 2 items du diagnostic complet) | « Difficulté probable » |
| **Constat** | 3+ items sur l'objectif, pattern cohérent | « Difficulté confirmée » |
| **Acquis** | ≥ 3 items corrects sur l'objectif **dans le diagnostic complet** | « Acquis confirmé » |

**« Maîtrise » est interdite en sortie de mini-évaluation**, quel que soit le
nombre de réponses justes : un élève peut enchaîner 4 bonnes réponses par
contexte favorable sans maîtriser la compétence.

#### Règle de cohérence inter-questions

Les questions Q2 et Q3 portent sur la **même identité remarquable** (le carré).
C'est une **contre-épreuve** :

| Q2 (développer) | Q3 (factoriser) | Lecture |
|---|---|---|
| ✅ | ✅ | Signal cohérent — confirmer au diagnostic complet |
| ✅ | ❌ | **Profil typique** : développement acquis, passage à la factorisation fragile → activité ciblée `OO-L1-2` |
| ❌ | ✅ | Profil atypique : vérifier la saisie avant de conclure |
| ❌ | ❌ | Difficulté sur l'identité remarquable elle-même → `OO-L1-1` **et** `OO-L1-2` |

Ce croisement est **la principale valeur ajoutée** de la mini-évaluation : il
n'était pas visible question par question.

---

### A.6 Questions complémentaires (sondes)

**Déclenchement** : uniquement sur signal (`fausse` ou `partielle`) sur un item
unique. **Jamais** déclenchées sur une réussite.

| Sonde | Déclencheur | Contenu | Correction attendue |
|---|---|---|---|
| `SONDE-M3-S1` | Q1 = `14/12` | Réduire 24/36 puis 15/25 | `2/3`, `3/5` |
| `SONDE-M3-S2` | Q2 signature `signe_non_distribue` | Développer `3(2x − 4)` | `6x − 12` |
| `SONDE-M3-S3` | Q3 signature `non_factorise` | Factoriser `x² − 5x` | `x(x − 5)` |
| `SONDE-M3-S4` | Q4 signature `signe_perdu` | Résoudre `−3x = 12` | `x = −4` |
| `SONDE-M3-S5` | Q5 signature `carre_parfait_non_extrait` | Simplifier `√72` | `6√2` |
| `SONDE-M3-S6` | Q1 ❌ **et** Q5 ❌ | Fraction simple : `2/3 + 1/4` | `11/12` |

> `SONDE-M3-S6` est le **seul cas de conclusion transversale** autorisé :
> deux erreurs sur deux objectifs distincts suggèrent une faiblesse possible du
> « sens du nombre », hypothèse de travail large et prudente, jamais une
> conclusion.

**Règles des sondes :**
- **Maximum 2 sondes par session.** Au-delà, l'élève fatigue et le signal se dégrade.
- Une sonde **n'aggrave jamais** le bilan : une réponse fausse à la sonde ne crée
  pas de nouvelle alerte si l'objectif est déjà signalé.
- Chaque sonde a **sa propre correction**, vérifiée par calcul.
- Une sonde est présentée comme une aide (« on vérifie ensemble »), jamais comme
  un test supplémentaire.

---

### A.7 Garde-fous contre la surinterprétation

**Inférences explicitement interdites** : 

| Interdit | Raison |
|---|---|
| ❌ « Vous ne comprenez pas le calcul littéral » (d'après 1 item) | 1 item ≠ concept manquant |
| ❌ « Vous êtes niveau 2 » | Aucun référentiel de niveaux n'existe |
| ❌ Comparer l'élève à la moyenne de la classe | **Aucune donnée de classe n'est collectée** |
| ❌ Afficher un pourcentage de réussite | 5 items ne mesurent pas un niveau |
| ❌ Conclure sur une leçon **non testée** (10 leçons sur 14) | Absence de test ≠ absence d'acquis |
| ❌ Déduire une conclusion d'un temps de réponse seul | Trop bruitant |
| ❌ Présenter l'hypothèse comme un diagnostic confirmé | Contrainte de mission |
| ❌ Utiliser `competence_officielle` | Aucune compétence officielle n'existe |

**Phrase de cadrage obligatoire à l'écran** (jamais optionnelle) :
> « Ces 5 questions donnent une **première idée** de tes acquis sur quelques
> points du programme. Ils ne couvrent pas tout le programme. »

---

### A.8 Recommandation de la première activité

**Principe : viser la difficulté la plus *spécifique* identifiée, pas la plus grave.**

| Hypothèse active | Activité recommandée | Type |
|---|---|---|
| `OO-L1-2` fragile (Q2 ✅ / Q3 ❌) | Exercice de factorisation guidé, sur une différence de deux carrés | Ciblée |
| `OO-L1-1` et `OO-L1-2` fragiles | Reprise du développement d'abord, factorisation ensuite | Séquencée |
| `OO-L5-1` (signe) | Exercices de fractions avec changement de signe, décimales puis entières | Ciblée |
| `OO-L8-1` (signe perdu) | Exercices de résolution avec membre de gauche négatif | Ciblée |
| `OO-L3-1` (carrés parfaits) | Exercices d'extraction de √2, √3, √5 progressivement | Ciblée |
| Aucune difficulté signalée | Exercice de maintien / approfondissement sur `OO-L1-1` (le plus observé) | Entretien |
| ≥ 3 objectifs signalés | **Diagnostic complémentaire proposé avant toute activité** | — |

**Interdits de recommandation :**
- ❌ Proposer une activité sur une leçon **non observée** (L6, L11 en particulier).
- ❌ Proposer une activité exigeant une figure sur téléphone sans alternative.
- ❌ Enchaîner plus de **3 exercices d'affilée** sans nouvelle vérification.

---

## PARTIE B — PARCOURS APRÈS LE DIAGNOSTIC

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. MINI-ÉVALUATION                                               │
│    5 questions · 3 à 5 min · aucune donnée personnelle          │
└──────────────────────────┬──────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. RETOUR IMMÉDIAT                                              │
│    «Ta 1re idée» + 1 point fort + 1 point à consolider          │
│    + cadrage explicite (A.7)                                    │
└──────────────────────────┬──────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. PREMIER EXERCICE ADAPTÉ                                      │
│    Selon A.8 · 1 exercice · niveau ajusté à l'hypothèse        │
└──────────────────────────┬──────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. EXPLICATION / INDICE                                         │
│    Indice gradué : rappel → méthode → première étape      │
│    (3 paliers, jamais la réponse complète d'emblée)            │
└──────────────────────────┬──────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. RÉCOMPENSE LÉGÈRE                                           │
│   fondée sur l'effort, jamais sur la justesse seule             │
└──────────────────────────┬──────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 6. DIAGNOSTIC COMPLÉMENTAIRE PROPOSÉ                            │
│    «On va vérifier plus finement ?» → +15 à +20 questions       │
│    covering les 10 leçons non testées                            │
└──────────────────────────┬──────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 7. PROFIL DE COMPÉTENCES MIS À JOUR PROGRESSIVEMENT             │
│    Statut par objectif : non évalué / signal / hypothèse /     │
│    constat / acquis confirmé                                     │
└─────────────────────────────────────────────────────────────────┘
```

### B.2 Étape 2 — Retour immédiat

**Structure imposée, 4 éléments, dans cet ordre :**

1. **Le cadrage** (A.7) — d'abord, pour ne pas surinterpréter.
2. **Un point fort** — toujours présent, même si tout est faible. Cherché dans
   les réussites *et* les réponses partielles.
3. **Un seul point à consolider** — le plus spécifique, pas le plus grave.
4. **Une question d'engagement** — « On essaie une question ensemble ? »

**Interdit :** afficher 3 points faibles simultanés. L'élève décroche, et
l'application perd sa fonction.

### B.3 Étape 4 — Explication et indice

**Trois paliers, débit progressif :**

| Palier | Contenu | Déclencheur |
|---|---|---|
| 1 — Rappel | La règle utile (« une différence de deux carrés ») | Après 1 erreur |
| 2 — Méthode | Les étapes, avec la première appliquée | Après 2 erreurs |
| 3 — Départ | La première ligne de la résolution | Après 3 erreurs |

**Palier 3 ≠ solution affichée.** L'élève termine seul — c'est ce qui ancre
l'apprentissage. La solution complète n'est proposée qu'après une nouvelle
erreur, et **explicitement signalée comme telle**.

### B.4 Étape 5 — Récompense légère

**Règle : récompenser l'effort et la persévérance, pas la justesse.**

| Situation | Récompense |
|---|---|
| Réussite du premier coup | Badge de réussite, sobre |
| Réussite après un indice | **Même reconnaissance** — l'indice fait partie de l'apprentissage |
| Échec puis reprise réussie | **Récompense encouragée explicitement** — c'est le moment le plus utile |
| Abandon | **Aucune pénalité, aucun message négatif** |

> **Interdit** : un message du type « Réessaie, tu as eu 40 % ». La seule
> information utilisée est *réussi / pas encore réussi*.

### B.5 Étape 6 — Diagnostic complémentaire

**Déclenchement** : proposé systématiquement après le premier exercice
(étape 3), et **prioritairement** si ≥ 3 objectifs sont signalés (A.8).

**Contenu** : 15 à 20 questions couvrant **les 10 leçons non testées** par la
mini-évaluation, avec **au moins 2 items par objectif** — condition pour que la
règle des trois (§ A.5) commence à fonctionner.

⚠️ **Deux leçons ne peuvent pas être couvertes en l'état** :
- **L6 Angles inscrits** — 🔴 bloqué, aucun objectif dérivable (décision n° 2).
- **L11 Statistique** — 🟡 support de données original à concevoir (décision n° 3).

### B.6 Étape 7 — Profil de compétences

**Un profil n'est mis à jour que sur preuve, jamais par défaut.**

| Règle | Effet |
|---|---|
| Un objectif non testé reste `non_evalue` | **Jamais** `non_acquis` |
| Persistance entre 2 sessions | Passage `signal` → `hypothese` |
| 3+ items cohérents | Passage → `constat` |
| ≥ 3 items corrects au diagnostic complet | Passage → `acquis_confirme` |
| Absence de données | **Aucune dégradation du profil** |

> **Interdit : dégrader le profil parce qu'un élève n'a pas répondu.** L'absence
> de réponse est un manque de données, pas une difficulté.

---

## PARTIE C — POINTS OUVERTS

| # | Question | Impact si non tranchée |
|---|---|---|
| C1 | Durée de conservation de l'historique brut | Obligation RGPD / CNIL sur données de mineurs |
| C2 | Les réponses de l'élève sont-elles partagées avec un enseignant ? | Change entièrement le modèle de consentement |
| C3 | Évaluateur algébrique vs formes acceptées en dur | Détermine l'implémentation de la correction |
| C4 | Motivation à l'usage (compte, sans données personnelles) | conditionne l'anti-triche et la persistance |
| C5 | Langue : l'interface reste-t-elle uniquement en français ? | Le sujet source est francophone ; l'appareil de saisie (√, ²) n'a pas d'équivalent dans d'autres écritures |

---

*Fin du document.*