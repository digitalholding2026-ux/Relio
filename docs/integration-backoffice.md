# Proposition d'intégration dans le back-office

Document de travail — à valider avec l'équipe technique et le responsable pédagogique.

---

## 1. Principe directeur

Le référentiel est un **artefact de données versionné**, independent du code et
de tout modèle d'IA. Il est consommé par le back-office et, plus tard, par le
moteur pédagogique.

```
source-progression-maths-3e.jpg        (document d'origine, figé)
        │
        ▼
outils/generer-referentiel.py           (transcription, versionnée)
        │
        ▼
data/referentiel-*.json                (artefact : vérité unique)
        │
        ├──▶ outils/valider-referentiel.mjs   (contrôle, exécuté en CI)
        │
        ├──▶ back-office pédagogique          (consultation / édition)
        │
        └──▶ moteur pédagogique              (planification, parcours)
```

**Règle :** le JSON est généré, pas écrit à la main. Toute modification passe
par le générateur, puis par le validateur. Cela évite que la version affichée
dans le back-office et celle utilisée par le moteur divergent.

---

## 2. Persistance

Le backend du projet est **NestJS + Prisma + PostgreSQL**. Proposition de modèle,
directement dérivable du JSON :

```prisma
model Referentiel {
  id                        String   @id          // "REF-CM-FR-MATH-3E-2025-2026"
  pays                      String
  systemeEducatif          String
  classe                    String
  matiere                   String
  anneeScolaire            String
  volumeHoraireAnnuelH     Int
  volumeHoraireHebdoH      Int
  statutValidation         String   // "valide_avec_reserves"
  documentSourceRef        Json
  version                  Int      @default(1)
  dateGeneration           DateTime

  trimestres Trimestre[]
  mois       Mois[]
  semaines   Semaine[]
  lecons     Lecon[]
  periodes   Periode[]
}

model Lecon {
  id              String  @id        // "LEC-CM-MATH-3E-2025-2026-07"
  referentielId   String
  rang            Int
  intitule        String
  intituleNorm    String
  volumeHoraireH  Int
  trimestreId     String
  semaineDebutId  String
  semaineFinId    String

  // Pré-chargés, vides à ce stade
  competences CompetenceLecon[]
  prerequis   Prerequis[]
  exercices   Exercice[]
  corriges    Corrige[]
  refsBepc    ReferenceBepc[]
}

model Periode {
  id             String  @id       // régulation ou révision
  referentielId  String
  type           String  // "regulation" | "revision"
  libelle        String
  volumeHoraireH Int
  semaineId      String
}
```

**Apports du modèle relationnel par rapport au JSON :**

- les compétences, prérequis, exercices et références BEPC deviennent des
  entités à part entière, ajoutables **sans migration du référentiel** ;
- le suivi de l'élève (progression, maîtrise) se greffe naturellement sur `Lecon`
  via `CompetenceLecon` ;
- le JSON reste le format d'échange et de réimport.

**Contrainte à respecter :** `id` est la clé technique. **Ne jamais utiliser
`intitule` comme identifiant** — les intitulés évoluent, les identifiants non.
Un intitulé peut être corrigé sans casser les données élèves.

---

## 3. Identifiants

| Entité | Format | Exemple |
|---|---|---|
| Référentiel | `REF-<pays>-<sys>-<matiere>-<classe>-<annee>` | `REF-CM-FR-MATH-3E-2025-2026` |
| Trimestre | `TRIM-<prefixe>-<annee>-<n>` | `TRIM-CM-MATH-3E-2025-2026-01` |
| Mois | `MOIS-<prefixe>-<annee>-<mm>` | `MOIS-CM-MATH-3E-2025-2026-09` |
| Semaine | `SEM-<prefixe>-<annee>-<n>` | `SEM-CM-MATH-3E-2025-2026-01` |
| Leçon | `LEC-<prefixe>-<annee>-<rang>` | `LEC-CM-MATH-3E-2025-2026-07` |
| Régulation | `REG-<prefixe>-<annee>-S<sem>` | `REG-CM-MATH-3E-2025-2026-S15` |
| Révision | `REV-<prefixe>-<annee>-S<sem>` | `REV-CM-MATH-3E-2025-2026-S30` |

Propriétés : **stables** (ne changent jamais), **lisibles**, **dérivés du
positionnement** plutôt que du contenu. Le rang de la leçon est utilisé pour
l'identifiant : un réordonnancement crée de nouveaux identifiants, ce qui est le
comportement souhaité — l'historique de progression de l'élève reste rattaché
à la leçon d'origine.

---

## 4. Champs d'extension

Déjà présents et **vides** dans le JSON, pour ne pas avoir à reconstruire le
référentiel lors des phases suivantes :

| Champ | Type | Phase |
|---|---|---|
| `competences` | tableau | Analyse des écarts (gap analysis) vis-à-vis des programmes |
| `prerequis` | tableau | Construction du graphe de dépendances |
| `objectifs` | tableau | Rédaction pédagogique |
| `exercices_ids` | tableau | Constitution de la banque d'exercices |
| `corriges_ids` | tableau | Idem |
| `references_bepc` | tableau | Alignement sur les épreuves du BEPC |

Ces champs sont **volontairement vides** : aucun document de référence
pédagogique n'a été fourni. Les remplir sans source reviendrait à inventer un
programme, ce qu'interdit la mission.

---

## 5. Écarts à arbitrer avant mise en production

| # | Question | Enjeu | Qui arbitre |
|---|---|---|---|
| A-1 | Faut-il conserver la colonne « Taux d'exécution » (dénominateur 112 h) ? | Cohérence avec l'en-tête (120 h) ; aujourd'hui **exclue** | Responsable pédagogique |
| A-2 | Les révisions couvrent-elles S29–S30 ou S30 seule ? | Planification hebdomadaire ; dépassement de 4 h | Responsable pédagogique |
| A-4 | Comment ventiler les heures de chaque leçon entre ses semaines ? | Suivi horaire élève | Responsable pédagogique |
| — | Statut : `valide_avec_reserves` → `valide` ? | Passage en production | Responsable pédagogique |

Tant que ces points ne sont pas tranchés, le référentiel reste consultable mais
**ne doit pas piloter la planification automatique**.

---

## 6. Neutralité vis-à-vis de l'IA

La mission impose de ne pas créer de dépendance technique empêchant de changer
de modèle d'IA. Le référentiel y contribue par construction :

- il ne contient **aucun** contenu généré, aucun embedding, aucune référence à
  un modèle ;
- les champs pédagogiques sont des **structures vides**, à remplir par des
  sources humaines ;
- le format est **agnostique** : JSON pur, aucun SDK, aucun appel réseau ;
- le validateur est en Node.js **sans dépendance** (`node:fs`, `node:path`
  uniquement), exécutable en CI.

Conséquence pratique : le choix du modèle d'IA, le prompting et la stratégie de
récupération restent entièrement réversibles.

---

## 7. Séquencement suggéré

1. **Arbitrage** des points A-1, A-2, A-4 par le responsable pédagogique.
2. **Import** du JSON via une commande NestJS (`npx tsx tools/import-referentiel.ts`),
   idempotente, activable par Dry Run.
3. **Écran back-office** de consultation : liste des leçons, volumes, semaines,
   périodes de régulation ; export PDF pour les enseignants.
4. **Graph des compétences** : ajout du contenu via les champs d'extension,
   sans migration du référentiel.
5. **Moteur pédagogique** : planification à partir de `sequence`, en traitant
   explicitement le dépassement A-2.
