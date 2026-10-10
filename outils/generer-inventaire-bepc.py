#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère l'inventaire des questions du BEPC mathématiques 2025 et 2026,
relié au référentiel annuel (data/referentiel-maths-3e-cm-2025-2026.json).

RÈGLES DE CONSTRUCTION
----------------------
* Aucune donnée n'est inventée. Énoncés, résultats et barèmes sont recopiés
  des documents sources (sujets + corrigés harmonisés nationaux).
* Les identifiants de leçons sont repris du référentiel annuel. Le référentiel
  n'est PAS modifié par ce script.
* Aucune compétence officielle n'est créée : le champ `competence_officielle`
  est null partout, faute de référentiel de compétences fourni.
* Chaque élément porte un niveau de confiance : "confirme", "incertain" ou
  "non_etabli", avec justification.
* Les résultats non publiés par le corrigé (ex. tâche 2 de 2025) sont null et
  signalés par `resultat_non_publie`.

Exécution :  python3 outils/generer-inventaire-bepc.py
Sortie   :  data/inventaire-questions-bepc-2025-2026.json
"""

import json
import os

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPERTOIREL = os.path.join(RACINE, "data", "referentiel-maths-3e-cm-2025-2026.json")
SORTIE = os.path.join(RACINE, "data", "inventaire-questions-bepc-2025-2026.json")

# --------------------------------------------------------------------------
# SOURCES
# --------------------------------------------------------------------------
SOURCES = {
    "2025": {
        "session": 2025,
        "sujet": {
            "fichier": "BEPC 04 juin 2025.pdf",
            "intitule": "BEPC Session 2025 — Épreuve de Mathématiques",
            "organisme": "Ministère des Enseignements Secondaires, Direction des Examens, des Concours et de la Certification",
            "format": "PDF 1.6, texte extractible",
            "pages": 2,
            "date_indiquee": "04 juin 2025",
        },
        "corrige": {
            "fichier": "BEPC-MATHS-CORRIGE-2025.pdf",
            "intitule": "Corrigé harmonisé national — Session 2025",
            "organisme": "Ministère des Enseignements Secondaires, Direction des Examens, des Concours et de la Certification",
            "format": "PDF 1.3, NUMÉRISÉ (scan sans couche texte) — rendu lisible par OCR (tesseract 5.5.0, modèle fra, 300 dpi)",
            "pages": 3,
            "pages_annoncees": 3,
            "pages_lues": "3/3 — document complet",
            "signataire": "Rose Eliane Lucien Douala — Président du Jury d'harmonisation (PLEG HE-IPN/MATHS)",
            "date_signature": "04/06/2025",
        },
        "duree_h": 2,
        "coefficient": 4,
        "series": "TOUTES",
    },
    "2026": {
        "session": 2026,
        "sujet": {
            "fichier": "BEPC 2026.pdf",
            "intitule": "BEPC Session 2026 — Épreuve de Mathématiques",
            "organisme": "Ministère des Enseignements Secondaires, Direction des Examens, des Concours et de la Certification",
            "format": "PDF 1.6, texte extractible",
            "pages": 2,
        },
        "corrige": {
            "fichier": "bepc 2026 corriger.pdf",
            "intitule": "Corrigé harmonisé national — Session 2026",
            "organisme": "Ministère des Enseignements Secondaires, Direction des Examens, des Concours et de la Certification",
            "format": "PDF 1.5, NUMÉRISÉ (scan sans couche texte) — pages pivotées à 90°, rendues lisibles par OCR (tesseract 5.5.0, modèle fra, 300 dpi)",
            "pages": 4,
            "pages_annoncees": 4,
            "pages_lues": "4/4 — document complet",
            "signataire": "Rose Eliane Lucien Douala — Président du Jury d'harmonisation (PLEG HE-IPN/MATHS)",
            "date_signature": "03/06/2026",
        },
        "duree_h": 2,
        "coefficient": 4,
        "series": "TOUTES",
    },
}

# --------------------------------------------------------------------------
# INVENTAIRE DES QUESTIONS
# --------------------------------------------------------------------------
# (id, session, partie, activite, exo_label, exo_num, q_num, bareme,
#  enonce, donnees, figure, notions, lecons[(rang, confiance)], methode,
#  resultat, etapes, bareme_corrige, divergence)
Q = []


def q(**kw):
    Q.append(kw)


# ---------------------------------------------------------------- SESSION 2025
q(id="BEPC-2025-A-NUM-EX1-1", session=2025, partie="A", activite="Activités numériques",
  bloc="Numerique", exo="Exercice 1", exo_num=1, question=1, bareme=1.0,
  enonce="Écrire le nombre A = (3/2 + 5/4) × (3/2 − 5/4) sous la forme d'une fraction irréductible.",
  donnees=["3/2", "5/4"], figure=False,
  notions=["Fractions", "Calcul littéral", "Opérations sur les nombres rationnels"],
  lecons=[(5, "confirme"), (1, "incertain")],
  methode="Réduction des fractions au même dénominateur puis produit, réduction du résultat.",
  resultat="A = 11/16",
  etapes=["A = (6/4 + 5/4) × (6/4 − 5/4)", "= 11/4 × 1/4", "= 11/16"],
  bareme_corrige="1 pt (0,25 somme + 0,25 différence + 0,25 produit + 0,25 résultat)",
  divergence=None)

q(id="BEPC-2025-A-NUM-EX1-2a", session=2025, partie="A", activite="Activités numériques",
  bloc="Numerique", exo="Exercice 1", exo_num=1, question="2.a", bareme=0.75,
  enonce="Écrire le nombre B = (3√2 − 4)² sous la forme a + b√2 où a et b sont des entiers.",
  donnees=["3√2 − 4"], figure=False,
  notions=["Racines carrées", "Calcul littéral", "Développement d'un carré"],
  lecons=[(1, "confirme"), (3, "confirme")],
  methode="Développement de (a − b)² puis reduction.",
  resultat="B = 34 − 24√2",
  etapes=["B = (3√2)² − 2(3√2)(4) + 4²", "= 18 − 24√2 + 16", "= 34 − 24√2"],
  bareme_corrige="0,75 pt (0,25 démarche + 0,25 par entier juste)",
  divergence=None)

q(id="BEPC-2025-A-NUM-EX1-2b", session=2025, partie="A", activite="Activités numériques",
  bloc="Numerique", exo="Exercice 1", exo_num=1, question="2.b", bareme=0.75,
  enonce="Montrer que le nombre C = (3√2 − 4)(3√2 + 4) est un entier.",
  donnees=["3√2 − 4", "3√2 + 4"], figure=False,
  notions=["Identité remarquable (a − b)(a + b) = a² − b²", "Racines carrées"],
  lecons=[(3, "confirme"), (1, "confirme")],
  methode="Utilisation de l'identité remarquable pour Recognaitre une différence de deux carrés.",
  resultat="C = 2, donc C est un entier.",
  etapes=["C = (3√2)² − 4²", "= 18 − 16", "= 2"],
  bareme_corrige="0,75 pt (0,5 démarche + 0,25 pour C = 2)",
  divergence=None)

q(id="BEPC-2025-A-NUM-EX1-2c", session=2025, partie="A", activite="Activités numériques",
  bloc="Numerique", exo="Exercice 1", exo_num=1, question="2.c", bareme=0.75,
  enonce="Écrire le nombre D = (3√2 − 4)/(3√2 + 4) sans radical au dénominateur.",
  donnees=["3√2 − 4", "3√2 + 4"], figure=False,
  notions=["Rationalisation d'un dénominateur", "Racines carrées", "Identité remarquable"],
  lecons=[(3, "confirme"), (5, "incertain")],
  methode="Multiplication par l'expression conjuguée, puis réduction.",
  resultat="D = 17 − 12√2",
  etapes=["D = (3√2 − 4)(3√2 − 4) / ((3√2 + 4)(3√2 − 4))",
          "= (3√2 − 4)² / ((3√2)² − 4²)",
          "= (34 − 24√2) / 2", "= 17 − 12√2"],
  bareme_corrige="0,75 pt (0,25 expression conjuguée + 0,25 calculs + 0,25 résultat)",
  divergence=None)

q(id="BEPC-2025-A-NUM-EX2-1", session=2025, partie="A", activite="Activités numériques",
  bloc="Numerique", exo="Exercice 2", exo_num=2, question=1, bareme=1.0,
  enonce="On considère E = (x − 3)(x + 4) + x² − 16. Choisir la forme développée de E parmi : "
          "a) 2x² − x − 28 ; b) 2x² − x + 28 ; c) 2x² + x + 28 ; d) 2x² + x − 28.",
  donnees=["E = (x − 3)(x + 4) + x² − 16"], figure=False,
  notions=["Calcul littéral", "Développement", "QCM"],
  lecons=[(1, "confirme")],
  methode="QCM — développement de (x − 3)(x + 4) puis addition.",
  resultat="Réponse d) : E = 2x² + x − 28",
  etapes=["(x − 3)(x + 4) = x² + 4x − 3x − 12 = x² + x − 12",
          "E = x² + x − 12 + x² − 16", "E = 2x² + x − 28"],
  bareme_corrige="1 pt — totalité du point pour la réponse d)",
  divergence=None)

q(id="BEPC-2025-A-NUM-EX2-2", session=2025, partie="A", activite="Activités numériques",
  bloc="Numerique", exo="Exercice 2", exo_num=2, question=2, bareme=1.0,
  enonce="Choisir la forme factorisée de E parmi : a) (x − 4)(2x − 7) ; b) (x + 4)(2x − 7) ; "
          "c) (x − 4)(2x + 7) ; d) (x + 4)(2x + 7).",
  donnees=["E = (x − 3)(x + 4) + x² − 16"], figure=False,
  notions=["Calcul littéral", "Factorisation", "QCM"],
  lecons=[(1, "confirme")],
  methode="QCM — reconnaissance de la factorisation.",
  resultat="Réponse b) : E = (x + 4)(2x − 7)",
  etapes=["Vérification : (x + 4)(2x − 7) = 2x² − 7x + 8x − 28 = 2x² + x − 28"],
  bareme_corrige="1 pt — totalité du point pour la réponse b)",
  divergence=None)

q(id="BEPC-2025-A-NUM-EX2-3a", session=2025, partie="A", activite="Activités numériques",
  bloc="Numerique", exo="Exercice 2", exo_num=2, question="3.a", bareme=0.5,
  enonce="On considère la fraction rationnelle Q = ((x + 4)(2x − 7)) / ((x + 4)(2x + 7)). "
          "a) Écrire la condition d'existence d'une valeur numérique de Q.",
  donnees=["Q = ((x + 4)(2x − 7)) / ((x + 4)(2x + 7))"], figure=False,
  notions=["Condition d'existence d'une fraction rationnelle", "Calcul littéral"],
  lecons=[(1, "confirme")],
  methode="Un quotient n'est défini que si son dénominateur est non nul.",
  resultat="Q existe si et seulement si (x + 4)(2x + 7) ≠ 0, c'est-à-dire x ≠ −4 et x ≠ −7/2",
  etapes=["(x + 4)(2x + 7) = 0", "x + 4 = 0 ou 2x + 7 = 0", "x = −4 ou x = −7/2"],
  bareme_corrige="0,5 pt (0,25 pour (x + 4)(2x + 7) ≠ 0 ; 0,25 pour x ≠ −4 ou x ≠ −7/2)",
  divergence=None)

q(id="BEPC-2025-A-NUM-EX2-3b", session=2025, partie="A", activite="Activités numériques",
  bloc="Numerique", exo="Exercice 2", exo_num=2, question="3.b", bareme=0.5,
  enonce="b) Simplifier Q.",
  donnees=["Q = ((x + 4)(2x − 7)) / ((x + 4)(2x + 7))"], figure=False,
  notions=["Simplification d'une fraction rationnelle", "Calcul littéral"],
  lecons=[(1, "confirme")],
  methode="Simplification par le facteur commun (x + 4), pour x ≠ −4 et x ≠ −7/2.",
  resultat="Q = (2x − 7)/(2x + 7), pour x ≠ −4 et x ≠ −7/2",
  etapes=["(x + 4) est un facteur commun au numérateur et au dénominateur",
          "Q = (2x − 7)/(2x + 7)"],
  bareme_corrige="0,5 pt pour Q = (2x − 7)/(2x + 7)",
  divergence=None)

q(id="BEPC-2025-A-GEO-EX1-1", session=2025, partie="A", activite="Activités géométriques",
  bloc="Geometrique", exo="Exercice 1", exo_num=1, question=1, bareme=1.0,
  enonce="Répondre par vrai ou faux. Dans un repère orthonormé du plan, les droites (D) et (L) "
          "d'équations respectives y = 2x − 1 et y = (1/2)x + 3 sont perpendiculaires.",
  donnees=["(D) : y = 2x − 1", "(L) : y = (1/2)x + 3"], figure=False,
  notions=["Droites perpendiculaires", "Coefficients directeurs", "Équations de droites"],
  lecons=[(10, "confirme"), (7, "incertain")],
  methode="Vrai/Faux — produit des coefficients directeurs.",
  resultat="Faux",
  etapes=["Produit des coefficients directeurs : 2 × (1/2) = 1 ≠ −1",
          "Les droites ne sont donc pas perpendiculaires."],
  bareme_corrige="1 pt (1 pt × 2 pour les deux questions de l'exercice)",
  divergence=None)

q(id="BEPC-2025-A-GEO-EX1-2", session=2025, partie="A", activite="Activités géométriques",
  bloc="Geometrique", exo="Exercice 1", exo_num=1, question=2, bareme=1.0,
  enonce="Répondre par vrai ou faux. Les vecteurs u(−2 ; 5) et v(5 ; 2) sont colinéaires.",
  donnees=["u(−2 ; 5)", "v(5 ; 2)"], figure=False,
  notions=["Vecteurs colinéaires", "Déterminant de deux vecteurs", "Coordonnées de vecteurs"],
  lecons=[(7, "confirme"), (9, "incertain")],
  methode="Vrai/Faux — deux vecteurs sont colinéaires si leurs coordonnées sont proportionnelles.",
  resultat="Faux",
  etapes=["(−2) × 2 − 5 × 5 = −4 − 25 = −29 ≠ 0",
          "Les vecteurs ne sont pas colinéaires."],
  bareme_corrige="1 pt (1 pt × 2)",
  divergence=None)

q(id="BEPC-2025-A-GEO-EX2-1", session=2025, partie="A", activite="Activités géométriques",
  bloc="Geometrique", exo="Exercice 2", exo_num=2, question=1, bareme=1.25,
  enonce="ABC est un triangle rectangle en B tel que AB = 6 cm et BC = 8 cm. Calculer AC.",
  donnees=["AB = 6 cm", "BC = 8 cm", "angle droit en B"], figure=True,
  figure_desc="Triangle ABC rectangle en B (non figuré dans le sujet)",
  notions=["Théorème de Pythagore", "Triangle rectangle"],
  lecons=[(4, "confirme")],
  methode="Application du théorème de Pythagore.",
  resultat="AC = 10 cm",
  etapes=["AC² = AB² + BC²", "= 6² + 8² = 36 + 64 = 100", "AC = 10 cm"],
  bareme_corrige="1,25 pt (0,5 pour AC² = AB² + BC² ; 0,5 calculs ; 0,25 résultat)",
  divergence=None)

q(id="BEPC-2025-A-GEO-EX2-2", session=2025, partie="A", activite="Activités géométriques",
  bloc="Geometrique", exo="Exercice 2", exo_num=2, question=2, bareme=1.0,
  enonce="Calculer la tangente de l'angle BAC et en déduire la mesure de l'angle BAC arrondie "
          "à l'entier le plus proche.",
  donnees=["AB = 6 cm", "BC = 8 cm", "AC = 10 cm"], figure=True,
  figure_desc="Même triangle ABC rectangle en B",
  notions=["Tangente d'un angle dans un triangle rectangle", "Calculatrice"],
  lecons=[(4, "confirme")],
  methode="tan(BAC) = côté opposé / côté adjacent, puis calcul inverse de l'angle.",
  resultat="tan(BAC) = BC/BA = 8/6 = 4/3 ; mes BAC ≈ 53,13° ≈ 53°",
  etapes=["tan BAC = BC/BA = 8/6 = 4/3", "mes BAC ≈ 53,13°", "arrondi : 53°"],
  bareme_corrige="1 pt (0,25 formule ; 0,25 valeur ; 0,25 valeur approchée ; 0,25 arrondi)",
  divergence=None)

q(id="BEPC-2025-A-GEO-EX3", session=2025, partie="A", activite="Activités géométriques",
  bloc="Geometrique", exo="Exercice 3", exo_num=3, question=1, bareme=2.0,
  enonce="SABCD est une pyramide régulière de hauteur 9 cm, dont la base est un carré de côté 8 cm. "
          "Calculer le volume de cette pyramide.",
  donnees=["Hauteur = 9 cm", "Base : carré de côté 8 cm"], figure=True,
  figure_desc="Pyramide à base carrée (non figurée dans le sujet)",
  notions=["Volume d'une pyramide", "Aire d'un carré"],
  lecons=[(14, "confirme")],
  methode="V = (aire de la base × hauteur)/3.",
  resultat="V = 192 cm³",
  etapes=["Aire de la base = 8 × 8 = 64", "V = (64 × 9)/3", "V = 192 cm³"],
  bareme_corrige="2 pts (0,5 formule ; 0,5 calculs ; 0,5 résultat ; 0,5 unité)",
  divergence=None)

q(id="BEPC-2025-B-T1", session=2025, partie="B", activite="Évaluation des compétences",
  bloc="Competences", exo="Tâche 1", exo_num=1, question=1, bareme=2.25,
  enonce="Une association vient en aide à un orphelinat qui a présenté un budget. En début d'année, "
          "la caisse disposait de 500 000 FCFA. Les membres ont cotisé en plus une somme "
          "représentant 4/5 du budget. Ils constatent qu'il leur manque 100 000 FCFA pour boucler "
          "le budget. Quel est le montant du budget présenté par l'orphelinat ?",
  donnees=["Caisse : 500 000 FCFA", "Cotisation : 4/5 du budget", "Manque : 100 000 FCFA"],
  figure=False,
  notions=["Équation du premier degré", "Mise en équation", "Résolution"],
  lecons=[(8, "confirme")],
  methode="Mise en équation puis résolution (critères C1, C2, C3 du corrigé).",
  resultat="Budget = 3 000 000 FCFA",
  etapes=["x = montant du budget", "(4/5)x + 500 000 = x − 100 000",
          "x − (4/5)x = 500 000 + 100 000", "(1/5)x = 600 000", "x = 3 000 000"],
  bareme_corrige="2,25 pts (C1 : 0,25 inconnue + 0,25 pour 4/5 x + 0,25 équation juste ; "
                 "C2 : 0,5 transformation en ax = b + 0,25 résultat ; C3 : 0,75 enchaînement)",
  divergence=None)

q(id="BEPC-2025-B-T2", session=2025, partie="B", activite="Évaluation des compétences",
  bloc="Competences", exo="Tâche 2", exo_num=2, question=1, bareme=2.25,
  enonce="Les dons en nature (sacs de riz et cartons d'huile) ont été achetés en deux temps chez "
          "le même vendeur : 1er temps, 3 sacs de riz et 2 cartons d'huile pour 146 000 FCFA ; "
          "2ème temps, 2 sacs de riz et 2 cartons d'huile pour 111 000 FCFA. "
          "Combien ont coûté un sac de riz et un carton d'huile ?",
  donnees=["3 sacs de riz + 2 cartons d'huile = 146 000 FCFA",
           "2 sacs de riz + 2 cartons d'huile = 111 000 FCFA"],
  figure=False,
  notions=["Système de deux équations à deux inconnues", "Résolution"],
  lecons=[(12, "confirme")],
  methode="NON PUBLIÉE — le corrigé n'apporte aucune solution pour cette tâche.",
  resultat=None,
  resultat_non_publie=True,
  etapes=[],
  bareme_corrige="2,25 pts attribués en bloc à tout candidat présent (N.B. du corrigé sur une coquille)",
  divergence="Le corrigé indique qu'une coquille dans le libellé de la tâche 2 fait allusion à un "
             "'carton de savon' au lieu d'un 'carton d'huile', et accorde les 2,25 pts à tout "
             "candidat présent. Or le sujet numérisé utilise 'carton d'huile' partout. Le corrigé "
             "ne fournit AUCUNE solution de référence pour cette tâche : aucun résultat ne peut "
             "donc être retranscrit.")

q(id="BEPC-2025-B-T3", session=2025, partie="B", activite="Évaluation des compétences",
  bloc="Competences", exo="Tâche 3", exo_num=3, question=1, bareme=2.25,
  enonce="Le chauffeur du véhicule chargé du transport des achats a proposé deux options : "
          "1ère option, payer 5 000 FCFA pour le carburant et 2 000 FCFA par heure ; "
          "2ème option, payer 10 000 FCFA pour le carburant et 1 000 FCFA par heure. "
          "À partir de quelle durée en heures l'option 2 est-elle plus avantageuse ?",
  donnees=["Option 1 : 5 000 + 2 000x", "Option 2 : 10 000 + 1 000x"],
  figure=False,
  notions=["Inéquation du premier degré", "Comparaison de deux fonctions affines"],
  lecons=[(8, "confirme"), (13, "incertain")],
  methode="Mise en inéquation puis résolution (critères C1, C2, C3 du corrigé).",
  resultat="x > 5, donc l'option 2 est plus avantageuse à partir de 6 heures.",
  etapes=["10 000 + 1 000x < 5 000 + 2 000x", "1 000x > 5 000", "x > 5",
          "Durée retenue (entier) : 6 heures"],
  bareme_corrige="2,25 pts (C1 : 0,25 inconnue + 0,25 expression + 0,25 inéquation ; "
                 "C2 : 0,25 transformation + 0,25 x > 5 + 0,25 durée 6 h ; C3 : 0,75 enchaînement)",
  divergence=None)

q(id="BEPC-2025-B-PRES", session=2025, partie="B", activite="Présentation",
  bloc="Presentation", exo="Présentation", exo_num=0, question=1, bareme=0.75,
  enonce="L'évaluation de la qualité de la présentation porte sur l'ensemble de toute la copie "
          "du candidat.",
  donnees=[], figure=False,
  notions=["Rédaction mathématique", "Orthographe et grammaire"],
  lecons=[],
  methode="Évaluation globale de la copie.",
  resultat="0,5 pt pour la lisibilité ; 0,25 pt pour la connaissance de l'orthographe et de la grammaire.",
  etapes=[], bareme_corrige="0,75 pt (0,5 lisibilité + 0,25 orthographe/grammaire)",
  divergence=None)

# ---------------------------------------------------------------- SESSION 2026
q(id="BEPC-2026-A-NUM-EX1-1", session=2026, partie="A", activite="Activités numériques",
  bloc="Numerique", exo="Exercice 1", exo_num=1, question=1, bareme=1.0,
  enonce="Écris le nombre A = 7/5 − (3/8) × (16/7) + 2/35 sous la forme d'une fraction irréductible.",
  donnees=["7/5", "3/8", "16/7", "2/35"], figure=False,
  notions=["Fractions", "Priorités opératoires", "Calcul littéral"],
  lecons=[(5, "confirme"), (1, "incertain")],
  methode="Priorité à la multiplication, puis réduction au même dénominateur.",
  resultat="A = 3/5",
  etapes=["A = 7/5 − (3 × 16)/(8 × 7) + 2/35", "= 7/5 − 6/7 + 2/35",
          "= 49/35 − 30/35 + 2/35", "= 21/35 = 3/5"],
  bareme_corrige="1 pt (0,25 calcul de 3/8 × 16/7 ; 0,25 réduction ; 0,25 résultat non simplifié ; "
                 "0,25 résultat irréductible)",
  divergence=None)

q(id="BEPC-2026-A-NUM-EX1-2", session=2026, partie="A", activite="Activités numériques",
  bloc="Numerique", exo="Exercice 1", exo_num=1, question=2, bareme=1.0,
  enonce="Écris le nombre B = −5√128 + 3√72 − 7√32 sous la forme de a√2, où a est un entier.",
  donnees=["−5√128", "3√72", "7√32"], figure=False,
  notions=["Racines carrées", "Réduction d'un radical", "Calcul littéral"],
  lecons=[(3, "confirme"), (5, "confirme")],
  methode="Réduction de chaque radical à la forme k√2 puis sommation.",
  resultat="B = −50√2",
  etapes=["√128 = √(64 × 2) = 8√2", "√72 = √(36 × 2) = 6√2", "√32 = √(16 × 2) = 4√2",
          "B = −5(8√2) + 3(6√2) − 7(4√2) = −40√2 + 18√2 − 28√2 = −50√2"],
  bareme_corrige="1 pt (0,75 démarche ; 0,25 résultat)",
  divergence=None)

q(id="BEPC-2026-A-NUM-EX2", session=2026, partie="A", activite="Activités numériques",
  bloc="Numerique", exo="Exercice 2", exo_num=2, question=1, bareme=2.0,
  enonce="Les poids de 30 passagers d'un bus de transport ont été relevés dans le tableau suivant : "
          "poids 55 / 60 / 62 / 65 / 70 kg ; effectifs 6 / 8 / 5 / 2 / 9. "
          "Calcule le poids moyen des passagers de ce bus et donne le résultat arrondi à "
          "l'unité supérieure.",
  donnees=["55→6", "60→8", "62→5", "65→2", "70→9", "30 passagers"],
  figure=True,
  figure_desc="Tableau de double entrée (poids / effectifs) — lisible, valeurs relevées sur l'image",
  notions=["Statistique", "Moyenne pondérée", "Lecture d'un tableau de données"],
  lecons=[(11, "confirme")],
  methode="Moyenne pondérée par les effectifs, puis arrondi.",
  resultat="Moyenne = 1880/30 ≈ 62,66 → 63 kg",
  etapes=["Somme des poids × effectifs : 6×55 + 8×60 + 5×62 + 2×65 + 9×70 = 1880",
          "Effectif total : 6 + 8 + 5 + 2 + 9 = 30", "Moyenne = 1880/30 ≈ 62,66",
          "Arrondi à l'unité supérieure : 63 kg"],
  bareme_corrige="2 pts (1 pt démarche ; 0,5 pt pour 62,66 ; 0,5 pt pour 63)",
  divergence="Le corrigé écrit « 62,66 » alors que 1880/30 = 62,666… (valeur tronquée, sans "
             "incidence sur l'arrondi). Écart mineur, signalé sans être corrigé.")

q(id="BEPC-2026-A-NUM-EX3-1", session=2026, partie="A", activite="Activités numériques",
  bloc="Numerique", exo="Exercice 3", exo_num=3, question=1, bareme=1.0,
  enonce="On considère P(x) = 16x² − 25 + (4x − 5)(3x + 1). Développe, réduis et ordonne P(x) "
          "suivant les puissances croissantes de x.",
  donnees=["P(x) = 16x² − 25 + (4x − 5)(3x + 1)"], figure=False,
  notions=["Calcul littéral", "Développement", "Réduction et ordonnancement"],
  lecons=[(1, "confirme")],
  methode="Développement puis réduction.",
  resultat="P(x) = 28x² − 11x − 30",
  etapes=["P(x) = 16x² − 25 + 12x² + 4x − 15x − 5", "P(x) = 28x² − 11x − 30"],
  bareme_corrige="1 pt (0,5 développement de (4x − 5)(3x + 1) ; 0,25 réduction ; 0,25 forme attendue)",
  divergence=None)

q(id="BEPC-2026-A-NUM-EX3-2", session=2026, partie="A", activite="Activités numériques",
  bloc="Numerique", exo="Exercice 3", exo_num=3, question=2, bareme=1.0,
  enonce="Écris P(x) sous la forme d'un produit de facteurs du premier degré.",
  donnees=["P(x) = 16x² − 25 + (4x − 5)(3x + 1)"], figure=False,
  notions=["Calcul littéral", "Factorisation", "Identité remarquable a² − b²"],
  lecons=[(1, "confirme")],
  methode="Factorisation de 16x² − 25 par a² − b², puis mise en évidence du facteur commun.",
  resultat="P(x) = (4x − 5)(7x + 6)",
  etapes=["16x² − 25 = (4x)² − 5² = (4x − 5)(4x + 5)",
          "P(x) = (4x − 5)(4x + 5) + (4x − 5)(3x + 1)",
          "= (4x − 5)(4x + 5 + 3x + 1)", "= (4x − 5)(7x + 6)"],
  bareme_corrige="1 pt (0,25 mise en évidence du facteur commun ; 0,25 résultat)",
  divergence=None)

q(id="BEPC-2026-A-NUM-EX3-3a", session=2026, partie="A", activite="Activités numériques",
  bloc="Numerique", exo="Exercice 3", exo_num=3, question="3.a", bareme=0.75,
  enonce="On pose Q(x) = ((3x − 7)(2x + 1)) / ((4x − 5)(7x + 6)). "
          "a) Résous dans ℝ l'équation (4x − 5)(7x + 6) = 0.",
  donnees=["Q(x) = ((3x − 7)(2x + 1)) / ((4x − 5)(7x + 6))"], figure=False,
  notions=["Équation produit", "Résolution d'une équation dans ℝ"],
  lecons=[(8, "confirme")],
  methode="Mise en équation produit : un produit de facteurs est nul si l'un des facteurs est nul.",
  resultat="S = {5/4 ; −6/7}",
  etapes=["(4x − 5)(7x + 6) = 0", "4x − 5 = 0 ou 7x + 6 = 0", "x = 5/4 ou x = −6/7"],
  bareme_corrige="0,75 pt (0,25 démarche ; 0,25 par solution)",
  divergence="Observation : le numérateur de Q(x), (3x − 7)(2x + 1), ne correspond pas aux "
             "facteurs de P(x), (4x − 5)(7x + 6). Les questions a) et b) portent uniquement sur le "
             "dénominateur ; le numérateur n'est donc jamais utilisé. Signalé sans être corrigé.")

q(id="BEPC-2026-A-NUM-EX3-3b", session=2026, partie="A", activite="Activités numériques",
  bloc="Numerique", exo="Exercice 3", exo_num=3, question="3.b", bareme=0.75,
  enonce="b) Déduis-en la condition d'existence d'une valeur numérique de Q.",
  donnees=["Q(x) = ((3x − 7)(2x + 1)) / ((4x − 5)(7x + 6))"], figure=False,
  notions=["Condition d'existence d'une fraction rationnelle", "Lecture d'un ensemble solution"],
  lecons=[(1, "confirme"), (8, "confirme")],
  methode="Application de la condition d'existence à partir de l'ensemble solution de a).",
  resultat="Q existe pour x ≠ 5/4 et x ≠ −6/7",
  etapes=["Q existe si et seulement si (4x − 5)(7x + 6) ≠ 0", "ce qui équivaut à x ≠ 5/4 et x ≠ −6/7"],
  bareme_corrige="0,75 pt (0,25 démarche ; 0,5 pour chaque valeur interdite)",
  divergence=None)

q(id="BEPC-2026-A-GEO-EX1-1", session=2026, partie="A", activite="Activités géométriques",
  bloc="Geometrique", exo="Exercice 1", exo_num=1, question=1, bareme=2.0,
  enonce="L'unité de longueur est le centimètre. ABC est un triangle rectangle en B. "
          "E ∈ [AB] et F ∈ [AC]. On donne AE = 2 ; AC = 8 et mes BAC = 30°. "
          "Détermine les distances AB et BC.",
  donnees=["AE = 2 cm", "AC = 8 cm", "mes BAC = 30°", "cos30° = √3/2", "sin30° = 1/2"],
  figure=True,
  figure_desc="Triangle ABC rectangle en B avec E sur [AB] et F sur [AC], indication « 2 cm » et angle 30°",
  notions=["Triangle rectangle", "Cosinus et sinus d'un angle aigu", "Longueur d'un côté"],
  lecons=[(4, "confirme")],
  methode="cos BAC = AB/AC et sin BAC = BC/AC.",
  resultat="AB = 4√3 cm ; BC = 4 cm",
  etapes=["AB = AC × cos BAC = 8 × (√3/2) = 4√3", "BC = AC × sin BAC = 8 × (1/2) = 4"],
  bareme_corrige="2 pts (0,5 pt par distance : 0,5 démarche + 0,5 résultat)",
  divergence=None)

q(id="BEPC-2026-A-GEO-EX1-2", session=2026, partie="A", activite="Activités géométriques",
  bloc="Geometrique", exo="Exercice 1", exo_num=1, question=2, bareme=1.25,
  enonce="Les droites (EF) et (BC) sont parallèles. Calcule la distance AF.",
  donnees=["AE = 2 cm", "AB = 4√3", "AC = 8 cm"], figure=True,
  figure_desc="Même figure que la question précédente",
  notions=["Théorème de Thalès", "Segments proportionnels"],
  lecons=[(2, "confirme")],
  methode="Thalès : AE/AB = AF/AC.",
  resultat="AF = (AE × AC)/AB = (2 × 8)/(4√3) = 4√3/3 cm",
  etapes=["AE/AB = AF/AC", "AF = (AE × AC)/AB = (2 × 8)/(4√3) = 16/(4√3) = 4/√3 = 4√3/3"],
  bareme_corrige="1,25 pt (0,25 égalité des quotients ; 0,5 calculs ; 0,5 résultat)",
  divergence=None)

q(id="BEPC-2026-A-GEO-EX2-1", session=2026, partie="A", activite="Activités géométriques",
  bloc="Geometrique", exo="Exercice 2", exo_num=2, question=1, bareme=1.0,
  enonce="Dans le plan muni d'un repère orthonormé (O ; I, J), on considère les points A, B et C "
          "de coordonnées respectives (5 ; 1), (2 ; −4) et (−3 ; 3). "
          "Place les points A, B et C dans le repère.",
  donnees=["A(5 ; 1)", "B(2 ; −4)", "C(−3 ; 3)"], figure=True,
  figure_desc="Repère orthonormé gradué (figure fournie dans le sujet et dans le corrigé)",
  notions=["Repère orthonormé", "Abscisse et ordonnée", "Placement de points"],
  lecons=[(9, "confirme"), (7, "incertain")],
  methode="Repérage à partir de l'abscisse puis de l'ordonnée.",
  resultat="Les trois points sont placés sur le repère.",
  etapes=["A à 5 en abscisse et 1 en ordonnée", "B à 2 et −4", "C à −3 et 3"],
  bareme_corrige="1 pt (0,25 pt pour le repère ; 0,25 pt par point bien placé)",
  divergence=None)

q(id="BEPC-2026-A-GEO-EX2-2", session=2026, partie="A", activite="Activités géométriques",
  bloc="Geometrique", exo="Exercice 2", exo_num=2, question=2, bareme=1.0,
  enonce="Détermine les coordonnées des vecteurs BA et BC.",
  donnees=["A(5 ; 1)", "B(2 ; −4)", "C(−3 ; 3)"], figure=False,
  notions=["Coordonnées d'un vecteur", "Différence de coordonnées"],
  lecons=[(9, "confirme")],
  methode="Pour deux points M(x1 ; y1) et N(x2 ; y2), le vecteur MN a pour coordonnées "
          "(x2 − x1 ; y2 − y1).",
  resultat="BA(3 ; 5) et BC(−5 ; 7)",
  etapes=["BA = (5 − 2 ; 1 − (−4)) = (3 ; 5)", "BC = (−3 − 2 ; 3 − (−4)) = (−5 ; 7)"],
  bareme_corrige="1 pt (0,25 abscisse + 0,25 ordonnée, par vecteur)",
  divergence=None)

q(id="BEPC-2026-A-GEO-EX2-3", session=2026, partie="A", activite="Activités géométriques",
  bloc="Geometrique", exo="Exercice 2", exo_num=2, question=3, bareme=1.0,
  enonce="Montre que la droite (L) passant par le point A et perpendiculaire à la droite (BC) "
          "a pour équation −5x + 7y + 18 = 0.",
  donnees=["A(5 ; 1)", "BC(−5 ; 7)"], figure=False,
  notions=["Équation cartésienne d'une droite", "Orthogonalité de deux vecteurs", "Produit scalaire"],
  lecons=[(10, "confirme"), (9, "confirme")],
  methode="Un point M de (L) tel que AM ⟂ BC, donc produit scalaire nul.",
  resultat="L : −5x + 7y + 18 = 0",
  etapes=["AM(x − 5 ; y − 1)", "AM ⟂ BC ⟺ −5(x − 5) + 7(y − 1) = 0",
          "−5x + 25 + 7y − 7 = 0", "−5x + 7y + 18 = 0"],
  bareme_corrige="1 pt (0,25 coordonnées de AM ; 0,25 orthogonalité ; 0,25 développement ; "
                 "0,25 réduction)",
  divergence=None)

q(id="BEPC-2026-A-GEO-EX2-4", session=2026, partie="A", activite="Activités géométriques",
  bloc="Geometrique", exo="Exercice 2", exo_num=2, question=4, bareme=0.75,
  enonce="Montre que le point D(0 ; 8) est l'image du point C par la translation de vecteur BA.",
  donnees=["C(−3 ; 3)", "D(0 ; 8)", "BA(3 ; 5)"], figure=False,
  notions=["Translation de vecteur", "Image d'un point"],
  lecons=[(9, "confirme"), (13, "confirme")],
  methode="Calcul du vecteur CD puis identification avec BA.",
  resultat="CD(0 + 3 ; 8 − 3) = (3 ; 5) = BA, donc D est l'image de C par la translation de vecteur BA.",
  etapes=["CD = (0 − (−3) ; 8 − 3) = (3 ; 5)", "Or BA = (3 ; 5)", "Donc CD = BA"],
  bareme_corrige="0,75 pt (0,5 coordonnées de CD ; 0,25 pour CD = BA)",
  divergence=None)

q(id="BEPC-2026-A-GEO-EX2-5", session=2026, partie="A", activite="Activités géométriques",
  bloc="Geometrique", exo="Exercice 2", exo_num=2, question=5, bareme=0.5,
  enonce="Déduis-en la nature du quadrilatère ABCD.",
  donnees=["ABCD quadrilatère", "CD = BA"], figure=False,
  notions=["Critères de parallélisme", "Parallélogramme", "Translation"],
  lecons=[(13, "confirme"), (9, "confirme")],
  methode="Un quadrilatère dont deux côtés opposés sont translates l'un de l'autre est "
          "un parallélogramme.",
  resultat="Le quadrilatère ABCD est un parallélogramme.",
  etapes=["CD = BA", "Un côté est l'image de l'autre par une translation",
          "Donc ABCD est un parallélogramme"],
  bareme_corrige="0,5 pt pour la réponse",
  divergence=None)

q(id="BEPC-2026-B-T1", session=2026, partie="B", activite="Évaluation des compétences",
  bloc="Competences", exo="Tâche 1", exo_num=1, question=1, bareme=1.5,
  enonce="Mme Adamou achète en deux phases dans une boutique où les mêmes prix sont appliqués : "
          "phase 1, 2 sacs de riz et un carton de savon pour 61 000 FCFA ; "
          "phase 2, un sac de riz et 3 cartons de savon pour 75 500 FCFA. "
          "Quel est le prix d'un sac de riz et celui d'un carton de savon ?",
  donnees=["2x + y = 61 000", "x + 3y = 75 500"], figure=False,
  notions=["Système de deux équations à deux inconnues", "Résolution"],
  lecons=[(12, "confirme")],
  methode="Mise en système puis résolution (critères C1, C2, C3 du corrigé).",
  resultat="Sac de riz : 21 500 FCFA ; carton de savon : 18 000 FCFA",
  etapes=["x = prix du sac de riz, y = prix du carton de savon",
          "2x + y = 61 000 et x + 3y = 75 500", "Résolution : x = 21 500, y = 18 000"],
  bareme_corrige="1,5 pt (C1 : 0,25 choix des inconnues + 0,25 l'une des deux équations attendues ; "
                 "C2 : 0,25 pour 21 500 + 0,25 pour 18 000 ; C3 : 0,5 enchaînement)",
  divergence=None)

q(id="BEPC-2026-B-T2", session=2026, partie="B", activite="Évaluation des compétences",
  bloc="Competences", exo="Tâche 2", exo_num=2, question=1, bareme=1.5,
  enonce="Mme Adamou utilise un fût cylindrique sans couvercle. Elle choisit de revêtir entièrement "
          "l'extérieur du fût (y compris le bas) pour limiter l'envahissement de la rouille avec "
          "une peinture dont 1 l couvre 10 m² de surface. Ce fût a 120 cm de hauteur et a un rayon "
          "de disque de base 30 cm. Prendre π = 3,14. "
          "Quelle quantité de peinture pourra aider le technicien à revêtir entièrement "
          "l'extérieur du fût ?",
  donnees=["Hauteur = 120 cm", "Rayon = 30 cm", "π = 3,14", "1 l couvre 10 m²"],
  figure=True,
  figure_desc="Fût cylindrique (décrit en texte, non figuré)",
  notions=["Aire latérale d'un cylindre", "Aire d'un disque", "Conversion d'unités", "Volumes et contenance"],
  lecons=[(14, "confirme"), (5, "incertain")],
  methode="Aire latérale + aire d'une base, puis division par la couverture par litre.",
  resultat="Aire = 25 434 cm² = 2,5434 m² ; quantité = 0,25434 litre",
  etapes=["Aire = aire latérale + aire d'une base",
          "= 2 × 3,14 × 30 × 120 + 3,14 × 30²", "= 22 608 + 2 826 = 25 434 cm² = 2,5434 m²",
          "Quantité = 2,5434 / 10 = 0,25434 litre"],
  bareme_corrige="1,5 pt (C1 : 0,25 idée du calcul d'aire + 0,25 idée de la division par 10 ; "
                 "C2 : 0,25 pour 25 434 ou 2,5434 + 0,25 pour 0,25434 ; C3 : 0,5 enchaînement)",
  divergence=None)

q(id="BEPC-2026-B-T3", session=2026, partie="B", activite="Évaluation des compétences",
  bloc="Competences", exo="Tâche 3", exo_num=3, question=1, bareme=1.5,
  enonce="Mme Adamou passe la commande dans une boulangerie pour la fabrication de 50 cornets de "
          "glace. Elle choisit des cornets ayant la forme d'un cône de révolution de génératrice "
          "de longueur 13 cm et de rayon du disque de base 5 cm. Le boulanger fait savoir à "
          "Mme Adamou que le prix de revient de 100 cm³ de cornet est de 50 FCFA. "
          "Prendre π = 3,14. Quel est le prix de revient de 50 cornets de glace ?",
  donnees=["Génératrice g = 13 cm", "Rayon r = 5 cm", "50 cornets",
           "100 cm³ = 50 FCFA", "π = 3,14"],
  figure=True,
  figure_desc="Cornets en forme de cône de révolution (décrits en texte, non figurés)",
  notions=["Volume d'un cône de révolution", "Théorème de Pythagore", "Proportionnalité"],
  lecons=[(14, "confirme"), (4, "confirme")],
  methode="Hauteur du cône par Pythagore, volume, puis prix de revient par proportionnalité.",
  resultat="h = 12 cm ; V = 314 cm³ ; 50 cornets = 15 700 cm³ ; prix = 7 850 FCFA",
  etapes=["g² = h² + r² → h = √(13² − 5²) = √144 = 12 cm",
          "V = (3,14 × 5² × 12)/3 = 314 cm³",
          "50 cornets : 50 × 314 = 15 700 cm³",
          "Prix = (15 700 × 50)/100 = 7 850 FCFA"],
  bareme_corrige="1,5 pt (C1 : 0,25 idée hauteur du cornet + 0,25 idée du prix de revient ; "
                 "C2 : 0,25 pour 12 + 0,25 pour 7 850 ; C3 : 0,5 enchaînement)",
  divergence=None)

q(id="BEPC-2026-B-PRES", session=2026, partie="B", activite="Présentation",
  bloc="Presentation", exo="Présentation", exo_num=0, question=1, bareme=0.5,
  enonce="L'évaluation de la qualité de la présentation porte sur l'ensemble de toute la copie "
          "du candidat.",
  donnees=[], figure=False,
  notions=["Lisibilité", "Rédiger"],
  lecons=[],
  methode="Évaluation globale de la copie.",
  resultat="0,5 pt pour la lisibilité.",
  etapes=[], bareme_corrige="0,5 pt pour la lisibilité",
  divergence=None)


def construire(referentiel):
    """Assemble l'inventaire en enrichissant chaque question des identifiants du référentiel."""
    par_rang = {l["rang"]: l for l in referentiel["lecons"]}

    questions = []
    for item in Q:
        # Rattachement explicite d'une sous-question (« 3.a ») à sa question mère (« 3 »).
        # Lorsque le sujet ne comporte pas de question Autonomous 3 (l'énoncé introductif est
        # fusionné avec la sous-question), le rattachement est déclaré « intégré ».
        question_mere = None
        nq = item["question"]
        if isinstance(nq, str) and "." in nq:
            mere = nq.split(".")[0]
            standalone = any(
                isinstance(o["question"], int) and str(o["question"]) == mere
                for o in Q if o["session"] == item["session"]
                and o["exo"] == item["exo"] and o["bloc"] == item["bloc"])
            question_mere = {
                "libelle": mere,
                "statut": "question distincte" if standalone else "introduction integrée à l'énoncé",
            }

        # L'intitulé « Exercice 1 » désigne un exercice de numération ET un de géométrie :
        # il n'est donc pas unique. On ajoute un identifiant d'exercice non ambigu.
        exercice_id = f"{item['session']}-{item['bloc'][:3].upper()}-EX{item['exo_num']:02d}"

        lecons = []
        for rang, confiance in item["lecons"]:
            l = par_rang[rang]
            lecons.append({
                "lecon_id": l["lecon_id"],
                "rang": l["rang"],
                "intitule": l["intitule"],
                "volume_horaire_h": l["volume_horaire_h"],
                "confiance": confiance,
            })
        src = SOURCES[str(item["session"])]
        questions.append({
            "question_id": item["id"],
            "session": item["session"],
            "source_sujet": src["sujet"]["fichier"],
            "source_corrige": src["corrige"]["fichier"],
            "partie": item["partie"],
            "activite": item["activite"],
            "bloc": item["bloc"],
            "exercice": item["exo"],
            "exercice_id": exercice_id,
            "numero_exercice": item["exo_num"],
            "numero_question": item["question"],
            "question_mere": question_mere,
            "bareme_pt": item["bareme"],
            "enonce_transcrit": item["enonce"],
            "donnees_numeriques": item["donnees"],
            "figure_requise": item["figure"],
            "figure_description": item.get("figure_desc"),
            "notions_mathematiques": item["notions"],
            "competence_officielle": None,
            "competence_officielle_statut": "non_etabli — aucun référentiel de compétences officiel "
                                            "n'a été fourni ; aucune compétence n'a été inventée",
            "lecons_referentiel": lecons,
            "corrige": {
                "methode": item["methode"],
                "resultat_attendu": item["resultat"],
                "resultat_non_publie": item.get("resultat_non_publie", False),
                "etapes": item["etapes"],
                "bareme": item["bareme_corrige"],
                "provenance": f"{src['corrige']['fichier']} — corrigé harmonisé national, "
                              f"lu après OCR et vérification visuelle",
            },
            "divergence_signalee": item["divergence"],
            "provenance": {
                "enonce": "transcrit du sujet officiel, vérifié visuellement sur l'image",
                "bareme_sujet": "transcrit du sujet officiel",
                "resultat": "transcrit du corrigé harmonisé national",
                "etapes": "transcrit du corrigé harmonisé national",
            },
        })

    couverture = {}
    for l in referentiel["lecons"]:
        obs = [q["question_id"] for q in questions
               if any(x["lecon_id"] == l["lecon_id"] for x in q["lecons_referentiel"])]
        couverture[l["lecon_id"]] = {
            "lecon_id": l["lecon_id"],
            "rang": l["rang"],
            "intitule": l["intitule"],
            "volume_horaire_h": l["volume_horaire_h"],
            "nombre_questions_observees": len(obs),
            "questions_ids": obs,
            "statut": "observee" if obs else "non_observee",
        }

    return {
        "$schema_version": "1.0.0",
        "metadonnees": {
            "titre": "Inventaire des questions — Épreuves harmonisées BEPC Mathématiques 2025 et 2026",
            "pays": "Cameroun",
            "classe": "3e",
            "matiere": "Mathématiques",
            "referentiel_annual_id": referentiel["metadonnees"]["referentiel_id"],
            "referentiel_annual_fichier": "data/referentiel-maths-3e-cm-2025-2026.json",
            "referentiel_annual_modifie": False,
            "sessions_analysees": [2025, 2026],
            "statut_validation": "analyse_provisoire_en_attente_de_validation_humaine",
            "avertissement_portee": "Ces deux sessions ne constituent PAS une représentation de "
                                    "la totalité du programme annuel. Elles ne couvrent que 2 des 14 "
                                    "leçons de façon complète ou partielle ; l'absence d'une leçon "
                                    "dans ces sujets ne signifie pas qu'elle est absente du "
                                    "programme ni qu'elle n'est pas évaluée.",
            "droits_utilisation": "NON VÉRIFIÉS. Les sujets, figures et corrigés harmonisés sont "
                                  "des documents publiés par la Direction des Examens, des Concours "
                                  "et de la Certification du Cameroun. Leur reproduction, "
                                  "republication ou exploitation commerciale dans l'application "
                                  "n'est pas autorisée en l'état. Une vérification des droits est "
                                  "un préalable obligatoire.",
            "competences_officielles": "Aucune. Le champ reste vide par construction.",
        },
        "sources": SOURCES,
        "questions": questions,
        "couverture_par_lecon": couverture,
        "controles": {},
    }


def controles(ref, inv):
    qs = inv["questions"]
    par_session = {}
    for s in (2025, 2026):
        sq = [q for q in qs if q["session"] == s]
        par_session[str(s)] = {
            "nombre_questions": len(sq),
            "nombre_exercices": len({(q["bloc"], q["numero_exercice"]) for q in sq}),
            "bareme_total_pt": round(sum(q["bareme_pt"] for q in sq), 2),
        }
    couverture = inv["couverture_par_lecon"]
    return {
        "questions_inventoriees": len(qs),
        "par_session": par_session,
        "lecons_referencees_au_referentiel": len(couverture),
        "lecons_observees": sum(1 for v in couverture.values() if v["statut"] == "observee"),
        "lecons_non_observees": sum(1 for v in couverture.values() if v["statut"] == "non_observee"),
        "questions_sans_source": sum(1 for q in qs if not q["source_sujet"] or not q["source_corrige"]),
        "questions_avec_divergence_signalee": sum(1 for q in qs if q["divergence_signalee"]),
        "questions_avec_resultat_non_publie": sum(1 for q in qs if q["corrige"]["resultat_non_publie"]),
        "competences_officielles_inventories": sum(1 for q in qs if q["competence_officielle"]),
        "bareme_partie_a_2025_pt": 12.5,
        "bareme_partie_b_2025_pt": 7.5,
        "bareme_total_2025_pt": 20,
        "bareme_partie_a_2026_pt": 15,
        "bareme_partie_b_2026_pt": 5,
        "bareme_total_2026_pt": 20,
    }


def main():
    with open(REPERTOIREL, encoding="utf-8") as fh:
        referentiel = json.load(fh)

    inv = construire(referentiel)
    inv["controles"] = controles(referentiel, inv)

    os.makedirs(os.path.dirname(SORTIE), exist_ok=True)
    with open(SORTIE, "w", encoding="utf-8") as fh:
        json.dump(inv, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    c = inv["controles"]
    print(f"OK -> {SORTIE}")
    print(f"  questions inventoriées : {c['questions_inventoriees']}")
    for s, v in c["par_session"].items():
        print(f"    session {s} : {v['nombre_questions']} questions, "
              f"{v['nombre_exercices']} exercices, barème {v['bareme_total_pt']} pt")
    print(f"  leçons observées      : {c['lecons_observees']}/{c['lecons_referencees_au_referentiel']}")
    print(f"  leçons non observées  : {c['lecons_non_observees']}")
    print(f"  divergences signalées  : {c['questions_avec_divergence_signalee']}")
    print(f"  résultats non publiés  : {c['questions_avec_resultat_non_publie']}")
    print(f"  compétences inventées  : {c['competences_officielles_inventories']} (doit être 0)")


if __name__ == "__main__":
    main()
