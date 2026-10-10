# Rapport final — Chantier 6 : validation pédagogique et cadrage du MVP

**Date** : 2026-10-10
**Objet** : préparer une décision de MVP pédagogique **fondée sur les documents existants**
**Périmètre** : aucun développement, aucune dépendance ajoutée, aucune architecture modifiée,
aucune fonctionnalité exposée aux élèves, aucun test manuel de l'application.
**Statut** : 🔴 **AUCUNE VALIDATION PÉDAGOGIQUE N'EST ACQUISE À CE JOUR.**
Ce rapport ne vaut pas validation : il établit ce qui est vérifiable, ce qui ne l'est pas,
et ce qui doit être tranché par un humain avant tout implémentation.

---

## 1. Résumé exécutif

**Ce que le chantier établit.** Le socle documentaire est **incomplet sur le plan
pédagogique et complet sur le plan arithmétique**. Les 11 réponses de la spécification
de la mission 3 (5 questions + 6 sondes) ont été **recalculées indépendamment dans ce
chantier** : **24 contrôles, 24 succès**. Ce n'est pas une validation pédagogique — c'est
la preuve que les corrections sont mathématiquement justes. Les deux plans sont
compatibles : *juste* et *validé*.

**Ce qui manque et qui ne peut pas être rattrapé par l'analyse.** Le référentiel annuel
ne contient **aucune compétence, aucun objectif, aucun prérequis** pour aucune des 14
leçons : ce n'est pas un défaut du fichier, c'est l'absence de document pédagogique de
référence. Les **26 objectifs opérationnels**, les **5 questions** et les **6 sondes** ont
donc été **déduits par un analyste** et **n'ont jamais été validés par un enseignant**.
Or le rapport de la mission 3 désigne précisément ce point comme son risque principal (H3).
Rien dans ce chantier ne peut lever ce risque : il ne peut que le documenter et le
transmettre.

**Trois faits nouveaux, établis par ce chantier, absents des rapports précédents :**

| # | Fait établi | Conséquence |
|---|---|---|
| **F1** | Les réponses `14/12` (Q1) et `4x² + 4x − 8` (Q3) sont **algebraiquement égales** aux réponses attendues. Une correction par égalité algébrique les validerait — ce qui **contredit** les signatures d'erreur prévues (`denominateur_non_reduit`, `non_factorise`) | La spécification de correction est **incomplète** : il manque une contrainte de forme canonique. Décision D5 à reformuler |
| **F2** | Le référentiel place **L8 « Équations » en S16–S17 (janvier)**. Or Q4 du diagnostic porte sur L8 | Un diagnostic déployé à la rentrée teste du contenu **non encore enseigné**. La question n'est pas « bonne ou mauvaise » mais « à quelle date » |
| **F3** | Les 4 PDF officiels du BEPC et l'inventaire contenant **35 énoncés transcrits verbatim** sont **versionnés dans ce dépôt Git** | L'exposition des documents est déjà possible. La visibilité du dépôt doit être vérifiée **avant** toute autre décision |

**Décision demandée.** Un seul arbitrage conditionne le calendrier : **faire relire les
26 objectifs déduits et les 5 questions par un enseignant de mathématiques**. Tant que ce
n'est pas fait, toute implémentation risque de coder un contenu mathématiquement juste et
pédagogiquement faux — le pire des deux mondes, car les erreurs seront invisibles : le
système fonctionnera, les élèves progresseront, et l'écart avec le programme réel ne se
révélera qu'à l'examen.

**Recommandation finale : 🔴 BLOQUÉ — en attente d'informations manquantes** (§ 10).
Le dossier est **prêt pour la revue du responsable du projet** et **n'est pas** prêt pour
le chantier d'implémentation.

---

## 2. Documents examinés

### 2.1 Présents dans le dépôt

| # | Document | Nature | Ce qu'il apporte | Ce qu'il n'apporte pas |
|---|---|---|---|---|
| D1 | `data/referentiel-maths-3e-cm-2025-2026.json` | Donnée | 14 leçons, 98 h, 3 trimestres, 30 semaines, position calendaire | Aucune compétence, aucun objectif, aucun prérequis |
| D2 | `data/inventaire-questions-bepc-2025-2026.json` | Donnée | 35 questions BEPC 2025/2026, corrigés, barèmes, associations aux leçons | Aucun droit de réutilisation ; aucune compétence officielle |
| D3 | `docs/matrice-couverture-competences.md` | Analyse | Couverture 14 leçons, objectifs **déduits**, lacunes, priorités | Aucune validation humaine |
| D4 | `docs/specification-diagnostic-initial.md` | Spécification | 5 questions originales, corrections, distracteurs, saisie mobile | Aucune validation humaine ; règle de correction incomplète (F1) |
| D5 | `docs/regles-recommandation-pedagogique.md` | Spécification | Règle des trois, 12 signatures d'erreur, 6 sondes, garde-fous, parcours | Aucune validation humaine |
| D6 | `docs/rapport-audit-fiabilite-chantier-4.md` | Rapport | Audit du socle déployé, réserves R1–R3 | — |
| D7 | `docs/rapport-final-chantier-5.md` | Rapport | 40 tests, corrections R1/R3/R5, état CI | — |
| D8 | `docs/ci-workflows-chantier-5.md` | Rapport | Contenu CI prêt à créer | — |
| D9 | `README.md` | Référentiel | État du dépôt, empreintes SHA-256, points en attente | — |
| D10 | `source-progression-maths-3e.jpg` | Source primaire | Tableau de progression 2025-2026 transcrit | Compétences (le document source n'en comporte pas davantage) |

### 2.2 Consulté hors du dossier de travail

| # | Document | Statut | Comment |
|---|---|---|---|
| D11 | `docs/rapport-final-mission-3.md` | 🔴 **Retiré du dossier de travail** | Récupéré depuis l'historique Git (`fb7fbeb^`) |

> 🔴 **Constat de fragilité documentaire.** Le rapport de la mission 3 a été supprimé de
> `docs/` le 2026-10-10 (commit `fb7fbeb`, « ne conserver que les documents courants »).
> Il est le document qui porte les **décisions bloquantes D1–D4** et l'**hypothèse H3**.
> Il n'existe plus que dans l'historique Git, comme les 12 autres rapports retirés. **La
> chaîne de décision d'un chantier critique n'est pas dans l'état courant du dépôt.**
> Ce rapport (chantier 6) en reprend les conclusions, ce qui limite la perte — mais la
> pratique de retrait mérite d'être revue par le responsable du projet.

### 2.3 Contrôles automatiques exécutés dans ce chantier

| Contrôle | Commande | Résultat | Attendu |
|---|---|---|---|
| Cohérence du référentiel | `node outils/valider-referentiel.mjs` | **0 erreur, 3 réserves** — code **2** | code 2 ✅ |
| Qualité de l'inventaire | `node outils/valider-inventaire-bepc.mjs` | **0 erreur, 0 réserve** — code **0** | code 0 ✅ |
| Recalcul indépendant des 11 réponses | Arithmétique rationnelle et polynomiale, Python 3 stdlib | **24 / 24 succès** | — |

> Le script de recalcul a été écrit **hors du dépôt** (`/tmp`), conformément au périmètre :
> ce chantier n'ajoute aucun fichier de production. Il peut être versé dans `outils/`
> comme `verifier-diagnostic-m3.py` sur décision du responsable du projet (§ 9, CP12).

---

## 3. Faits établis

### 3.1 Faits vérifiés dans ce chantier

| # | Fait | Preuve |
|---|---|---|
| V1 | Le référentiel contient **14 leçons, 0 compétence, 0 objectif, 0 prérequis** | Contrôle automatisé + lecture des 14 enregistrements |
| V2 | Total horaire cohérent : 98 h leçons + 14 h régulation + 8 h révision = **120 h** | Validateur, section 5 |
| V3 | **3 réserves** subsistantes : L5 (9 h pour 8 h disponibles), excédents L6/L8/L13, révision de 8 h sur une semaine de 4 h | Validateur, code 2 |
| V4 | L'inventaire recense **35 questions**, 32 avec étapes de corrigé, 9 requiring des figures, 3 divergences signalées, 1 résultat non publié | `controles` + lecture |
| V5 | **Les réponses attendues des 5 questions sont justes** | Recalcul indépendant, 24/24 |
| V6 | **Les réponses attendues des 6 sondes sont justes** | Recalcul indépendant (S1 ×2, S2, S3, S4, S5, S6) |
| V7 | **Les distracteurs analysables sont exacts** : `5x + 7` (signe non distribué), `(2x−4)(2x+2)` (inversion des signes), `4x² + 4x − 8` (forme développée), `5/3` (signe sur le dernier terme), `6√2` (coefficient oublié), `9√2` (carré parfait erroné) | Recalcul indépendant |
| V8 | `Q4` est **auto-vérifiable** : les deux membres valent −17 en x = −5 | Substitution vérifiée |
| V9 | **Position calendaire** : L1 = S1–S2, L3 = S5–S6, L5 = S10–S11, L8 = **S16–S17** | `sequence` du référentiel |
| V10 | `BEPC-2025-B-T2` est **annulée par le jury** (coquille « carton de savon/huile », barème accordé à tous) et n'a **aucune solution de référence** | `divergence_signalee` |
| V11 | Les droits d'utilisation sont **explicitement déclarés non vérifiés** dans les métadonnées de l'inventaire | `metadonnees.droits_utilisation` |
| V12 | `competence_officielle` est **vide sur les 35 questions**, avec motif renseigné | Validateur, section 5 |
| V13 | L'état des données est **inchangé** : les deux validateurs retournent les mêmes codes qu'à la mission 2/3 | Exécution directe |

### 3.2 Faits établis, mais **qualifiés**

| # | Fait | Qualification |
|---|---|---|
| V14 | La « règle des trois » (borne à 95 % ≈ 3/n) | **Exacte** pour un taux d'erreur nul observé sur *n* trials indépendants. Elle suppose l'indépendance des trials, **non garantie** ici (même élève, même séance, questions liées). L'hypothèse H2 rend l'indépendance encore plus doubtful. **Conclusion : la règle est un garde-fou prudent, pas un théorème applicable tel quel.** |
| V15 | Q2/Q3 forment une « contre-épreuve » | Le croisement est **logiquement cohérent** ; sa **valeur empirique** (le profil ✅/❌ se reconnaît-il réellement ?) n'est **pas** mesurée. Aucune donnée élève n'existe. |

### 3.3 Incertitudes

| # | Incertitude | Effet |
|---|---|---|
| I1 | **Aucun enseignant n'a jamais relu** les 26 objectifs déduits, les 5 questions et les 6 sondes | Le contenu pédagogique est **non qualifié** |
| I2 | **La leçon 1 « Calculations littéral » peut ne pas tourner autour du développement/factorisation** | Les questions cibleraient le mauvais contenu — avec des réponses mathématiquement irréprochables |
| I3 | **Le contenu attendu de L6 « Angles inscrits » n'est pas déterminable** (5 h, 0 question BEPC) | Blocage maintained pour toute question L6 |
| I4 | **Le support de L11 « Statistique » n'existe pas** (la seule observation dépend d'un tableau du sujet) | Blocage maintained pour L11 |
| I5 | **`11/6` (distracteur de Q1) n'a pas pu être reconstitué** comme erreur systématique simple à partir de l'énoncé. `5/3` se reconstitue (signe sur le dernier terme) ; `11/6` reste d'origine **inconnue** | Le couple `11/6`/`5/3` est rattaché à une **seule** signature `signe_non_reparti`, alors que les mécanismes peuvent différer. Discrimination à confirmer par l'enseignant |
| I6 | **La valeur diagnostique réelle des 5 questions n'est pas mesurée** et ne peut pas l'être sans données | H1, H2 (saisie mobile, suffisance de 5 questions) restent des hypothèses |
| I7 | **La visibilité du dépôt Git n'a pas été vérifiée** dans ce chantier (aucun accès réseau utilisé) | F3 : exposition possible des documents officiels |

### 3.4 Lacunes documentaires

| # | Lacune | Gravité | Qui peut la combler |
|---|---|---|---|
| L1 | **Aucun document pédagogique de référence** (programme officiel détaillé, compétences, prérequis) | 🔴 Majeure | Responsable pédagogique |
| L2 | **Aucun objectif pour L6 Angles inscrits** | 🔴 Majeure | Responsable pédagogique |
| L3 | **Aucun support de données original pour L11** | 🟡 Moyenne | Responsable pédagogique |
| L4 | **Aucune méthode détaillée publiée pour L12/L13/L14** dans les corrigés | 🟡 Moyenne | Responsable pédagogique |
| L5 | **Aucune preuve d'observation réelle de L6 dans l'examen** — 2 sessions ne sont pas le programme | 🟡 Moyenne | Responsable pédagogique |
| L6 | **Aucune donnée sur la saisie algébrique sur smartphone par des élèves de 3e** (H1) | 🟠 Moyenne | Test utilisateur avant conception de l'interface |
| L7 | **Aucun référentiel de niveaux** — interdit d'afficher un niveau, mais aucun système de remplacement n'est défini | 🟠 Moyenne | Responsable pédagogique |

### 3.5 Incohérences et contradictions internes identifiées

| # | Incohérence | Détail | Traitement proposé |
|---|---|---|---|
| **F1** | 🔴 **Correction algébrique vs forme attendue** | La spécification du diagnostic (`specification-diagnostic-initial.md` § 6) impose l'**égalité algébrique** pour Q2 et Q3. Mais `14/12` (Q1) et `4x² + 4x − 8` (Q3) sont **algebraiquement égales** aux réponses attendues (vérifié). Un correcteur par égalité algébrique les accepte → les signatures `denominateur_non_reduit` et `non_factorise` **ne se déclenchent jamais**, et l'exercice recommandé devient faux | Décision D5 reformulée : comparaison par égalité algébrique **ET** contrainte de forme canonique. Deux niveaux : *valeur juste* / *forme attendue*. Ne pas trancher sans l'enseignant : `4x²+4x−8` est-il une réponse acceptable ? |
| **F2** | 🟠 **Diagnostic contre calendrier scolaire** | Q4 porte sur L8, programmée **S16–S17 (janvier)**. Déployé à la rentrée (S1), l'élève n'a jamais vu les équations. Le rapport de la mission 3 n'aborde pas ce point ; H4 ne fait qu'évoquer « densité du programme » | **Garder Q4 mais conditionner son affichage à l'avancement réel dans l'année** (après S16), ou l'assumer comme une révision anticipée. Décision requise |
| **F3** | 🔴 **Documents officiels versionnés dans le dépôt** | `git ls-files` confirme : les 4 PDF officiels **et** l'inventaire (35 énoncés transcrits verbatim) sont suivis. Le README affirme « les droits ne sont pas établis » — mais les documents sont **dans le dépôt** | Vérifier la visibilité (public/privé) **avant toute autre action**. Voir § 8 |
| F4 | 🟡 **Deux conclusions de mission 3 non reproductibles** | Le rapport de la mission 3 affirme « 11 réponses recalculées indépendamment ». Confirmé ici (V5–V7). En revanche, il ne fournit **aucun script** : le contrôle n'était pas reproductible. Le contrôle de ce chantier l'est | Verser le script dans `outils/` |
| F5 | 🟡 **Champ `volume_horaire_heures` non lisible au niveau attendu** | Le référentiel utilise `volume_horaire_h` ; une lecture naïve donne `undefined` | Documenter le nom réel du champ dans le README (piège de lecture, pas défaut de données) |
| F6 | 🟡 **Cadre juridique cité probablement hors périmètre** | Le rapport de la mission 3 (C1) mentionne « RGPD / CNIL ». Le service vise des **mineurs résidant au Cameroun**. Le régime applicable est **à faire confirmer par un conseil juridique** — il ne peut pas être présumé | Ne pas figer le cadre juridique dans un document technique sans confirmation |
| F7 | 🟡 **Divergence 2026-A-NUM-EX2 non arbitrée** | Le corrigé écrit « 62,66 » pour 1880/30 = 62,666… — écart mineur signalé sans être corrigé. Sans impact sur le diagnostic (L11 bloquée) | Conserver le signalement ; ne pas trancher |

---

## 4. Décisions à prendre

### 4.1 Les cinq questions du diagnostic : correspondance au programme

**Avertissement :** la colonne « objectif opérationnel » est **déduite**, jamais validée.
La colonne « enchaînement des leçons » est **documentée** (référentiel transcrit du
document officiel) et **fiable**.

| Q | Identifiant | Leçon **documentée** | OO **déduit** | Position dans l'année | Base de calibrage BEPC | Fiabilité de la base | Statut |
|---|---|---|---|---|---|---|---|
| Q1 | `ORIG-M3-Q01` | **L5 — Calcul numérique** (9 h) | `OO-L5-1`, `OO-L5-2` | S10–S11 (novembre) | 5 questions, 3 confirmées | 🟢 Correct | ⚠️ Non validé |
| Q2 | `ORIG-M3-Q02` | **L1 — Calcul littéral** (7 h) | `OO-L1-1` | **S1–S2 (septembre)** | 11 questions, 9 confirmées | 🟢 Solide | ⚠️ Non validé |
| Q3 | `ORIG-M3-Q03` | **L1 — Calcul littéral** (7 h) | `OO-L1-2` | **S1–S2 (septembre)** | ↑ | 🟢 Solide | ⚠️ Non validé |
| Q4 | `ORIG-M3-Q04` | **L8 — Équations dans ℝ** (5 h) | `OO-L8-1` | **S16–S17 (janvier)** 🔴 | 4 questions, 4 confirmées | 🟢 Correct | ⚠️ Non validé + **F2** |
| Q5 | `ORIG-M3-Q05` | **L3 — Racines carrées** (7 h) | `OO-L3-1` | S5–S6 (octobre) | 4 questions, 4 confirmées | 🟢 Correct | ⚠️ Non validé |

**Couverture obtenue : 4 leçons sur 14, soit 28 h sur 98 h (29 %).**

**Ce que cette table permet de décider :**

1. **Q2 et Q3 sont le cœur justifié du dispositif** — L1 porte 11 des 49 associations
   observées, la leçon la mieux documentée du programme, et la seule située **dès S1–S2**.
   Elles sont cohérentes avec un lancement en début d'année.
2. **Q1 et Q5 sont justifiées mais tardives** (S5–S11) : elles ne sont cohérentes qu'avec
   un déploiement en octobre–novembre.
3. **Q4 est la plus discriminante mais la plus risquée** (F2). Elle ne peut pas(figurer
   dans un diagnostic de rentrée sans décision explicite.

**Conclusions que le système est autorisé à produire (règle des trois) :**

> 🔴 **Aucune conclusion d'acquisition.** 1 item par objectif ⇒ avec 0 erreur, la borne
> supérieure du taux d'erreur est **300 %**. La mini-évaluation ne peut **que** signaler
> des difficultés ponctuelles. Le mot « acquis », « maîtrisé », « niveau » et tout
> pourcentage sont **interdits** en sortie.

### 4.2 Décisions de validation humaine — **bloquantes**

| # | Décision | Responsable | Pourquoi elle bloque | Ce qu'il faut pour la trancher |
|---|---|---|---|---|
| **D1** | 🔴 **Droits d'utilisation des documents BEPC** | Propriétaire | Détermine si le contenu du jury peut un jour être utilisé. **Non levée depuis la mission 2.** En attendant : contenu élève **100 % original**, `source_bepc: null`, contrôle automatisé | Confirmation écrite, ou refus explicite acté |
| **D2** | 🔴 **Contenu attendu de la leçon 6 « Angles inscrits »** | Responsable pédagogique | Sans objectifs, toute question L6 serait **inventée**. 5 h de programme non couvertes | Contenu fourni, ou **acte formel que L6 est hors MVP** |
| **D3** | 🟡 **Support de données original pour L11 Statistique** | Responsable pédagogique | La seule source observée est non reproductible. 7 h non couvertes | Tableau original validé |
| **D4** | 🔴 **Validation des 5 questions et des 26 OO par un enseignant** | Responsable pédagogique | Les corrections sont justes **par calcul**, pas **par une autorité disciplinaire**. Risque H3 : un contenu juste et hors programme | Relecture signée (§ 6) |
| **D5** | 🟠 **Règle de correction : égalité algébrique + contrainte de forme** (F1) | Responsable pédagogique + technique | Détermine si `4x²+4x−8` et `14/12` sont acceptés, refusés ou « partiels ». Sans cela, les signatures d'erreur ne se déclenchent pas | Règle écrite et testée sur les 11 réponses |

### 4.3 Décisions de conception encore ouvertes

| # | Question ouverte | Options | Impact | Recommandation de ce chantier |
|---|---|---|---|---|
| **D6** | **Saisie des expressions algébriques sur smartphone** (Q2, Q3, Q5) | (a) clavier dédié `x ² √` + comparaison algébrique ; (b) formes acceptées en dur + expansion sur `x` ; (c) réponse structurée (choix de méthode + cases) | Hypothèse **H1** : si l'élève ne saisit pas, le périmètre dégrade vers le QCM, ce qui **détruit la valeur diagnostique** (réponse juste par hasard) | Trancher (b) pour le MVP : moins de dépendance, correction contrôlée. **Tester H1 sur 5 élèves réels avant** (L6) |
| **D7** | **Conservation des réponses brutes** | (a) ne conserver que le statut + la signature ; (b) conserver la saisie brute pour ré-analyse ; (c) ne rien conserver | (b) est nécessaire pour calibrer le moteur, mais crée une donnée liée à un élève. **Obligation de purge** (N mois) non fixée | **Décision obligatoire avant implémentation.** Phase de test : conservation courte et documentée, purge automatique, anonymisation |
| **D8** | **Accès des enseignants** | (a) aucun accès ; (b) export pseudonymisé pour l'enseignant ; (c) tableau de bord par classe | (b)/(c) changent **entièrement** le modèle de consentement et la base légale. Un élève mineur ne peut pas consentir seul à un traitement que son école surveille | **Hors MVP.** Décider après cadrage juridique |
| **D9** | **Comptes élèves** | (a) aucun compte, identifiant local anonyme ; (b) compte pseudonyme ; (c) compte lié à l'établissement | (b)/(c) créent une base de données d'élèves mineurs persistante. (a) est le seul choix cohérent avec la règle de minimisation déjà posée | **(a) pour le MVP.** Refuser (b)/(c) tant que le cadre juridique n'est pas posé |
| **D10** | **Protection des données des mineurs** | (a) minimisation stricte, purge, hébergement local ; (b) identification du responsable de traitement ; (c) politique de conservation écrite | F6 : le cadre juridique cité (RGPD/CNIL) est **probablement hors périmètre** pour un service visant des mineurs au Cameroun. **À faire confirmer par un conseil juridique** — ce chantier ne tranche pas | **Bloquant pour tout ce qui persiste.** D7/D9 en dépendent |
| **D11** | **Langue de l'interface** | (a) français uniquement ; (b) multilingue | L'appareil de saisie `√` et `²` n'a pas d'équivalent dans d'autres écritures | **Français uniquement** pour le MVP |
| **D12** | **Moment de déclenchement du diagnostic** (F2) | (a) rentrée ; (b) après S5 ; (c) au fil de l'année | Détermine si Q1, Q4, Q5 sont recevables | **Au fil de l'année**, avec affichage conditionné à l'avancement réel |

### 4.4 Décisions relatives aux réserves du référentiel

| # | Réserve (validateur, code 2) | Effet sur le MVP | Recommandation |
|---|---|---|---|
| R1 | L5 « Calcul numérique » : 9 h pour 8 h disponibles | Le séquençage réel de L5 déborde d'une heure | **Arbitrer** — impacte la date de disponibilité de Q1 |
| R2 | Excédents de capacité L6 (+1 h), L8 (+2 h), L13 (+2 h) | Le document source ne ventile pas les heures par semaine | **Acter comme non bloquant** pour le MVP : le moteur n'a pas besoin de la ventilation hebdomadaire exacte |
| R3 | Révision de 8 h sur une semaine de 4 h | Sans effet sur le contenu élève | **Acter comme non bloquant** — corriger lors de la prochaine version du référentiel |

> Aucune de ces trois réserves n'a été arbitrée. Elles sont **documentées, pas corrigées**
> (principe de non-correction silencieuse, respecté).

---

## 5. Proposition de MVP

### 5.1 Périmètre proposé — 3 leçons, 1 tranche

Le MVP est **volontairement plus étroit** que la spécification de la mission 3, parce que
la couverture de 4 leçons ne tient pas debout au regard du calendrier (F2).

| | Périmètre mission 3 | **MVP proposé** |
|---|---|---|
| Leçons | 4 (L1, L3, L5, L8) — 28 h | **3 (L1, L3, L5) — 23 h** |
| Questions diagnostiques | 5 | **4** (Q1, Q2, Q3, Q5) — Q4 différée à S16 |
| Leçons couvertes | 4 / 14 (29 %) | **3 / 14 (21 %)** |
| Géométrie, L6, L11, L12–L14 | exclues | **exclues — inchangé** |

**Pourquoi L6 et L11 restent exclus** : L6 n'a **aucun objectif dérivable** (D2, bloqué) ;
L11 n'a **aucun support de données** réutilisable (D3). Les inclure reviendrait à inventer
du contenu pédagogique. **Ce n'est pas un défaut du MVP, c'est une limite assumée et
documentée.**

### 5.2 Contenu proposé

| Bloc | Contenu | Objectifs | Exercices originaux | Explications |
|---|---|---|---|---|
| **B1 — Calcul littéral** (L1, 7 h, S1–S2) | Développer, factoriser | `OO-L1-1`, `OO-L1-2` | **6** (≥ 3 par objectif) | 3 paliers |
| **B2 — Racines carrées** (L3, 7 h, S5–S6) | Extraire les carrés parfaits, simplifier | `OO-L3-1` | **3** (≥ 3) | 3 paliers |
| **B3 — Calcul numérique** (L5, 9 h, S10–S11) | Fractions, forme irréductible | `OO-L5-1`, `OO-L5-2` | **3** (≥ 3) | 3 paliers |
| **Total** | | **5 objectifs** | **12 exercices** | |

**Règle dimensionnante : ≥ 3 items par objectif.** C'est la condition pour que la règle
des trois produise autre chose qu'une indécision (4 items, 0 erreur → 75 % ; 3 items →
encore 100 %). Sans elle, le MVP ne pourrait jamais afficher « acquis confirmé » ni
« constat », et **tout le dispositif d'interprétation resterait inerte**. C'est la
différence principale avec la mini-évaluation de la mission 3.

> ⚠️ **Ces exercices ne sont pas rédigés dans ce rapport.** Les produire suppose que les
> `OO` soient **validés** (D4). Rédiger 12 exercices sur des objectifs non validés
> produirait un contenu faux avec une apparence de qualité — exactement le scénario que
> ce chantier cherche à éviter.

### 5.3 Progression pédagogique — vérifiable

La progression **n'est pas une notion décorative** : elle doit pouvoir se contrôler
automatiquement. Quatre propriétés vérifiables :

| # | Propriété | Critère de vérification |
|---|---|---|
| P1 | **Ordre des prérequis** | `OO-L5-1` avant `OO-L5-2` ; `OO-L1-1` avant `OO-L1-2`. Vérifiable par la table de dépendances validée par l'enseignant |
| P2 | **Ancrage calendaire** | Un bloc n'est proposé que si la semaine du référentiel est atteinte : B1 dès S1, B2 dès S5, B3 dès S10. Vérifiable par comparaison avec `sequence` |
| P3 | **Progression de difficulté interne** | Chaque exercice d'un bloc porte un rang déclaré 1→n. Vérifiable par le rang, contrôlé par l'enseignant |
| P4 | **Pas de dégression du profil** | Un objectif non testé reste `non_evalue`, **jamais** `non_acquis`. Absence de réponse ≠ difficulté. Vérifiable par test automatisé |

> P2 est la traduction directe de F2 : **la progression suit le calendrier scolaire réel**,
> pas un ordre arbitraire. C'est le moyen le plus simple d'éviter qu'un élève de septembre
> soit évalué sur le programme de janvier.

### 5.4 Hors périmètre explicite du MVP

Tuteur IA · comptes élèves · notation / score · tableau de bord enseignant · diagnostic
complémentaire (10 leçons) · géométrie · L6 · L11 · L12–L14 · toute publication de contenu
BEPC · toute fonctionnalité non terminée exposée à un élève.

---

## 6. Plan de validation par un enseignant

### 6.1 Profil recherché

Un enseignant de mathématiques **exerçant en 3e au Cameroun**, ou ayant exercé
récemment. **Une seule personne suffit** pour lever D4. Un binôme (un enseignant de
mathématiques + un enseignant d'informatique pédagogique) est préférable pour D5 et D6.

### 6.2 Déroulé — 3 séances

**Séance 1 — Les objectifs (2 h) — la séance la plus importante**

| Étape | Durée | Contenu | Sortie |
|---|---|---|---|
| 1.1 | 30 min | Présentation du référentiel : les 14 leçons, leurs volumes, leur position calendaire | L'enseignant valide ou corrige la transcription |
| 1.2 | 45 min | Les **6 objectifs** du périmètre MVP (`OO-L1-1`, `OO-L1-2`, `OO-L3-1`, `OO-L5-1`, `OO-L5-2`) : est-ce bien le contenu attendu de ces leçons ? | **Feu vert / correction / rejet** par objectif |
| 1.3 | 30 min | Les 20 autres `OO` : information, sans arbitrage | Liste d'objectifs à retenir pour le MVP ultérieur |
| 1.4 | 15 min | **Les 3 réserves du référentiel** (§ 4.4, R1–R3) | Arbitrage ou actation |

> ⚠️ **Point de vigilance à porter à l'enseignant.** La question n'est pas « ces calculs
> sont-ils justes ? » — ils le sont, vérifié. La question est : **« un élève de 3e, à cet
> instant de l'année, travaille-t-il réellement là-dessus, et l exercise-t-il ainsi ? »**
> Une réponse « non » invalide la question, même si elle est mathématiquement parfaite.

**Séance 2 — Les questions et les corrections (2 h)**

| Étape | Durée | Contenu | Sortie |
|---|---|---|---|
| 2.1 | 45 min | Les **5 questions**, énoncé + réponse attendue + distracteurs, **une par une** | Validée / reformulée / rejetée |
| 2.2 | 30 min | Les **6 sondes** : pertinence, niveau, formulations | Validées / reformulées |
| 2.3 | 30 min | **Les 12 signatures d'erreur** : sont-elles les erreurs réellement commises par des élèves ? La granularité est-elle la bonne ? (`11/6` et `5/3` partagent `signe_non_reparti` — I5) | Catalogue ajusté |
| 2.4 | 15 min | **F1** : `4x²+4x−8` et `14/12` — acceptés, refusés ou « partiels » ? | **Règle de correction écrite** (D5) |

**Séance 3 — Le parcours et le test de saisie (1 h 30)**

| Étape | Durée | Contenu | Sortie |
|---|---|---|---|
| 3.1 | 30 min | Le parcours de 7 étapes et le cadrage à l'écran : le libellé « première idée » est-il le bon ton ? | Validation ou reformulation |
| 3.2 | 45 min | **Test de saisie (H1)** : demander à l'enseignant de saisir les réponses de Q2, Q3, Q5 **sur son téléphone, en 3 minutes**, sans aide | **Preuve ou réfutation de H1** |
| 3.3 | 15 min | Cadre juridique et Mineurs : ce que l'enseignant accepterait de voir sur ses élèves | Entrée de D7–D10 |

### 6.3 Restitution attendue

Un document de validation signé, contenant :

- la liste des `OO` **approuvés**, **modifiés** ou **rejetés** ;
- la liste des questions et sondes **approuvées** ;
- la règle de correction (D5) en une phrase opposable ;
- l'avis sur L6 (contenu fourni ou exclusion actée) ;
- l'avis sur H1 (test de saisie).

---

## 7. Critères d'acceptation

Le MVP ne pourra être considéré validé que si **les 12 critères** suivants sont
satisfaits. Ils sont volontairement **binaires et vérifiables**.

### 7.1 Critères pédagogiques

| # | Critère | Vérification | Bloquant |
|---|---|---|---|
| **A1** | ≥ 3 items par objectif du MVP | Comptage sur le contenu produit | ✅ |
| **A2** | Aucune conclusion d'acquisition issue d'un seul item | Revue de la règle d'interprétation + test automatisé sur le moteur | ✅ |
| **A3** | Le statut `partielle` existe et n'est jamais compté comme `fausse` **ni** comme `correcte` | Test automatisé | ✅ |
| **A4** | Le cadrage à l'écran est présent, non optionnel, et affiche « première idée » | Revue de l'interface | ✅ |
| **A5** | 100 % des exercices sont originaux, `source_bepc: null`, contrôle automatisé en place | Contrôle automatisé sur le contenu livré | ✅ |
| **A6** | Aucune leçon hors périmètre MVP n'est exposée à un élève | Contrôle automatisé (listes blanches) | ✅ |
| **A7** | Aucune fonctionnalité inachevée n'est accessible | Revue de la liste des points d'entrée | ✅ |

### 7.2 Critères de correction

| # | Critère | Vérification | Bloquant |
|---|---|---|---|
| **B1** | Les 5 réponses attendues et les 6 réponses de sondes sont recalculées par un script versionné dans le dépôt | `python3 outils/verifier-diagnostic-m3.py` → 24/24 | ✅ |
| **B2** | La règle D5 (égalité algébrique + forme canonique) est écrite et **testée sur les 2 cas de F1** | Test automatisé : `4x²+4x−8` et `14/12` produisent le statut attendu | ✅ |
| **B3** | Chaque distracteur documenté déclenche **la** signature prévue, et une seule | Test automatisé sur les 12 distracteurs | ✅ |
| **B4** | Aucun exercise n'accepte une réponse par simple longueur ou motif | Revue de la règle de comparaison | ✅ |

### 7.3 Critères de conformité et de sécurité

| # | Critère | Vérification | Bloquant |
|---|---|---|---|
| **C1** | Aucun contenu BEPC ne transite vers le client | Contrôle automatisé sur le bundle construit | ✅ |
| **C2** | La visibilité du dépôt Git est vérifiée et actée (§ 8, F3) | Vérification + note écrite | ✅ |
| **C3** | Aucune donnée nominative collectée ; identifiant local anonyme | Revue du modèle de données | ✅ |
| **C4** | Durée de conservation et purge automatique définies **par écrit** avant activation (D7/D10) | Document écrit | ✅ |
| **C5** | La CI des deux dépôts applicatifs est active et verte | `docs/rapport-final-chantier-5.md` le laissait bloquée (scope `workflow` du jeton) | ✅ |
| **C6** | Contrôles statiques (typecheck, lint, build) verts dans les deux dépôts | Exécution | ✅ |

---

## 8. Risques

### 8.1 Droits de réutilisation des sujets d'examen — **risque majeur**

**Sources concernées** : les sujets et corrigés harmonisés du BEPC, publiés par la
Direction des Examens, des Concours et de la Certification du Cameroun.

| # | Risque | État | Gravité | Traitement |
|---|---|---|---|---|
| **R-1** | **Droits non établis** | Confirmé : `droits_utilisation = "NON VÉRIFIÉS"` dans les métadonnées | 🔴 Critique | Aucune reproduction, republication ou exploitation. Statut inchangé depuis la mission 2 |
| **R-2** | **Exposition déjà possible via le dépôt** (F3) | Les 4 PDF officiels **et** 35 énoncés transcrits verbatim sont versionnés dans Git | 🔴 Critique | **Vérifier la visibilité du dépôt en priorité absolue.** Si public : le document est déjà exposé, indépendamment de toute décision produit |
| **R-3** | **Fuite vers le client** | Le frontend est public par défaut sur Vercel | 🔴 Critique | Aucun contenu BEPC dans le bundle. Contrôle automatisé obligatoire (C1). Le statut `source_bepc: null` doit être **contrôlé automatiquement**, pas seulement par convention |
| **R-4** | **Dérive par copie** | 35 énoncés sont présents dans le dépôt ; l'inventaire est à proximité immédiate du contenu produit | 🟠 Élevée | Règle d'or documentée : `source_bepc` ne jamais être renseigné. Contrôle automatisé |
| **R-5** | **Usage de « calibrage » mal compris** | Le calibrage est présenté comme autorisé | 🟠 Élevée | Le calibrage reste un usage **interne**. Il ne justifie aucune publication |
| **R-6** | **Recopie non intentionnelle par l'enseignant validateur** | Les documents officiels circulent pour la validation | 🟡 Moyenne | Ne pas fournir les PDF à un tiers sans mention explicite de la restriction |
| **R-7** | **Confusion sur l'autorité** | Les corrigés sont « la meilleure base disponible » | 🟡 Moyenne | L'antériorité et la fiabilité de la source **ne confèrent aucun droit**. Le document le dit déjà ; il faut le maintenir |

**Ce que ce chantier ne fait pas et ne peut pas faire** : il ne vérifie pas la
visibilité du dépôt (aucun accès réseau), et ne se prononce pas sur le fond juridique.

**Position recommandée :** le contenu élève reste **exclusivement original**. La levée de
D1 est un **bonus**, jamais un préalable à la construction du MVP. Il est donc possible de
avancer sur le contenu original sans attendre les droits — mais **pas** de publier quoi que
ce soit qui en dérive.

### 8.2 Risques pédagogiques

| # | Risque | Probabilité | Impact | Parade |
|---|---|---|---|---|
| **P-1** | **Objectifs déduits faux (H3)** | 🟠 Moyenne | 🔴 Élevé — tout le contenu est mal ciblé, avec des réponses justes | D4, séance 1. **Risque principal du projet** |
| **P-2** | **Saisie algébrique impossible sur téléphone (H1)** | 🟠 Moyenne | 🔴 Élevé — dégradation vers le QCM, perte de la valeur diagnostique | Test de saisie en séance 3.2 **avant** conception de l'interface |
| **P-3** | **5 questions ne suffisent pas (H2)** | 🟡 Faible | 🟠 Modéré | Le MVP passe à ≥ 3 items par objectif (§ 5.2) |
| **P-4** | **Élève testé avant l'enseignement (F2)** | 🔴 **Quasi certaine** sans parade | 🟠 Modéré | Affichage conditionné à la semaine du référentiel (P2) |
| **P-5** | **Surinterprétation par l'élève** (« j'ai 3/5, je suis nul ») | 🟡 Faible | 🟠 Modéré | Cadrage obligatoire (A4) + 3 paliers d'indice |
| **P-6** | **Dépendance à la stance du tuteur IA** | — | — | **Hors MVP.** Ne pas promettre de tuteur avant de l'avoir construit |

### 8.3 Risques techniques et de projet

| # | Risque | État | Parade |
|---|---|---|---|
| **T-1** | **CI non activée** | Le rapport du chantier 5 indique que le jeton n'a pas le scope `workflow` | Condition **C5**. À traiter avant le chantier d'implémentation |
| **T-2** | `API_BASE_URL` figée au build (R2, chantier 4) | Non corrigé | À traiter avant toute bascule |
| **T-3** | **Fragilité documentaire** : le rapport de la mission 3 n'est plus dans `docs/` | Constaté | Conserver les rapports **de décision** dans l'état courant |
| **T-4** | Cadre juridique des données des mineurs non posé (D10, F6) | Constaté | Consultation juridique avant toute persistance |

---

## 9. Conditions préalables au chantier d'implémentation

**Aucune de ces conditions ne peut être levée par l'analyse.** Elles exigent une
décision humaine ou une pièce externe.

| # | Condition | Responsable | Bloque |
|---|---|---|---|
| **CP1** | 🔴 **Relecture signée des objectifs** `OO` du périmètre MVP | Enseignant | Tout |
| **CP2** | 🔴 **Relecture signée des 5 questions et 6 sondes** | Enseignant | Tout |
| **CP3** | 🔴 **Règle de correction D5 écrite** (forme canonique, cas F1) | Enseignant + technique | Correction automatique |
| **CP4** | 🔴 **Visibilité du dépôt Git vérifiée et actée** | Responsable du projet | Conformité (R-2) |
| **CP5** | 🟠 **Position sur L6** : contenu fourni ou exclusion actée | Responsable pédagogique | Couverture, pas le MVP |
| **CP6** | 🟠 **Test de saisie H1 réalisé** sur 5 élèves | Responsable produit | Interface de saisie |
| **CP7** | 🟠 **Support original L11** fourni et validé | Responsable pédagogique | MVP ultérieur |
| **CP8** | 🟠 **D7–D10 tranchées** : conservation, accès enseignant, comptes, protection des mineurs | Responsable de projet + juridique | Persistance de données |
| **CP9** | 🟡 **Réserves du référentiel arbitrées** (R1–R3) | Responsable pédagogique | Séquencement calendaire |
| **CP10** | 🟡 **Décision D12** : moment de déclenchement du diagnostic | Responsable produit | Affichage conditionné |
| **CP11** | 🟡 **CI activée** dans les deux dépôts (T-1) | Responsable technique | Non-régression |
| **CP12** | 🟡 **Script de recalcul versé dans `outils/`** (F4) | Responsable technique | Reproductibilité |

> **CP1, CP2 et CP3 sont les trois verrous.** Les autres peuvent être traités en parallèle
> ou après. Sans les trois premiers, le chantier d'implémentation produirait du code
> correct sur un modèle faux — **le mode de défaillance le plus coûteux du projet**,
> parce qu'il ne se voit pas.

---

## 10. Recommandation finale

### 🔴 BLOQUÉ — en attente d'informations manquantes

**Le dossier est prêt pour la revue du responsable du projet. Il n'est pas prêt pour
l'implémentation.**

**Pourquoi « prêt pour la revue »** : le périmètre est documenté, les faits sont vérifiés,
les 11 réponses sont recalculées (24/24), les lacunes sont identifiées, les risques sont
cartographiés, le MVP est proposé avec des critères d'acceptation binaires, et les
conditions préalables sont listées. Le responsable dispose de tout ce qu'il faut pour
décider.

**Pourquoi « bloqué »** : trois informations manquent, et aucune ne peut être produite
par l'analyse :

1. **Aucune validation pédagogique n'existe.** Les 26 objectifs, 5 questions et 6 sondes
   ont été déduits par un analyste. Aucun enseignant ne les a vus. Le rapport de la
   mission 3 le disait déjà ; ce chantier le confirme sans pouvoir le lever.
2. **La règle de correction est incomplète** (F1). Deux réponses documentées comme
   « fausses » ou « partielles » sont mathématiquement égales aux réponses attendues. En
   l'état, une part du dispositif d'interprétation **ne se déclencherait pas**.
3. **Les droits sur les documents officiels ne sont pas établis** (D1), et les documents
   sont versionnés dans un dépôt dont la visibilité n'a pas été vérifiée (F3, R-2).

**Ce que le blocage ne signifie pas.** Le socle documentaire est bon : il est exact,
honnête sur ses limites, et il énonce ses propres interdits avant qu'on les découvre. Le
chantier 6 n'a trouvé **aucune erreur mathématique**. Le blocage est un blocage
d'**autorité** et de **connaissance**, pas de qualité.

**Séquence proposée :**

```
CP1 + CP2 + CP3   Relecture enseignant (séances 1 et 2, ~4 h)
        ↓
   D5 + L6         Décisions de fond
        ↓
   CP4             Vérification de visibilité du dépôt   ← peut démarrer IMMÉDIATEMENT
        ↓
   CP6             Test de saisie sur 5 élèves            ← peut démarrer en parallèle
        ↓
  CHANTIER 7       Implémentation du MVP (3 leçons, 12 exercices)
```

> CP4 et CP6 ne dépendent d'aucune validation pédagogique et peuvent être engagés
> **dès maintenant**. C'est le seul élément du chantier 6 qui ne demande pas d'attendre.

**Aucun développement ne doit commencer avant la revue de ce rapport par le responsable
du projet.**

---

## 11. Éléments à approuvés avant toute implémentation — liste récapitulative

À signer ou à acter formellement :

| # | Élément | Nature de l'approbation |
|---|---|---|
| 1 | Les 5 objectifs du périmètre MVP (`OO-L1-1`, `OO-L1-2`, `OO-L3-1`, `OO-L5-1`, `OO-L5-2`) | **Validation pédagogique** — enseignant |
| 2 | Les 5 questions originales et leurs distracteurs | **Validation pédagogique** — enseignant |
| 3 | Les 6 sondes et leurs déclencheurs | **Validation pédagogique** — enseignant |
| 4 | Le catalogue des 12 signatures d'erreur | **Validation pédagogique** — enseignant |
| 5 | La règle de correction (égalité algébrique + forme canonique) — **F1** | **Décision** — enseignant + technique |
| 6 | Le périmètre du MVP (3 leçons, 12 exercices) | **Décision produit** — responsable de projet |
| 7 | Le déclenchement conditionné au calendrier (P2 / F2) | **Décision produit** — responsable de projet |
| 8 | La position sur L6 (contenu ou exclusion) | **Décision pédagogique** — responsable pédagogique |
| 9 | Le support de données original pour L11 | **Décision pédagogique** — responsable pédagogique |
| 10 | La règle de conservation des réponses (D7) | **Décision + juridique** |
| 11 | Le statut des comptes élèves (D9) | **Décision + juridique** |
| 12 | Le statut de l'accès enseignant (D8) | **Décision + juridique** |
| 13 | Le cadre juridique applicable aux données des mineurs (D10, F6) | **Consultation juridique** |
| 14 | La visibilité du dépôt Git (F3) | **Décision du propriétaire** |
| 15 | Les 3 réserves du référentiel (R1–R3) | **Décision pédagogique** |
| 16 | L'activation de la CI (CP11) | **Décision technique** |
| 17 | Le libellé élève « première idée » | **Validation pédagogique** — enseignant |

---

*Documents liés : `docs/matrice-couverture-competences.md`,
`docs/specification-diagnostic-initial.md`, `docs/regles-recommandation-pedagogique.md`,
`data/referentiel-maths-3e-cm-2025-2026.json`,
`data/inventaire-questions-bepc-2025-2026.json`,
`docs/rapport-audit-fiabilite-chantier-4.md`, `docs/rapport-final-chantier-5.md`,
`docs/rapport-final-mission-3.md` (historique Git, commit `fb7fbeb^`).*