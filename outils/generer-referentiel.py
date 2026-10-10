#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère le référentiel numérique de la progression annuelle de mathématiques 3e
(Cameroun, année scolaire 2025-2026) à partir de la transcription du document source.

Source unique et autoritaire de vérité :
  ./source-progression-maths-3e.jpg  ("Document de maths.jpg", dépôt GitHub Relio)

Aucune donnée n'est inventée : ce script ne contient QUE la transcription.
Les champs non fournis par le document restent explicitement vides.

Exécution :  python3 outils/generer-referentiel.py
Sortie   :  data/referentiel-maths-3e-cm-2025-2026.json
"""

import json
import os
import unicodedata

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "data", "referentiel-maths-3e-cm-2025-2026.json")

PREFIXE = "CM-MATH-3E"
ANNEE = "2025-2026"


def slug(txt: str) -> str:
    """Slug ASCII stable pour les identifiants techniques."""
    txt = unicodedata.normalize("NFKD", txt)
    txt = txt.encode("ascii", "ignore").decode("ascii")
    txt = txt.lower().replace("'", " ")
    return "-".join(txt.split())


# ---------------------------------------------------------------------------
# 1. MÉTADONNÉES (fournies par l'énoncé de mission)
# ---------------------------------------------------------------------------
METADONNEES = {
    "referentiel_id": "REF-CM-FR-MATH-3E-2025-2026",
    "pays": "Cameroun",
    "code_pays": "CM",
    "systeme_educatif": "francophone",
    "classe": "3e",
    "matiere": "Mathématiques",
    "code_matiere": "MATH",
    "annee_scolaire": "2025-2026",
    "langue_source": "fr",
    "volume_horaire_annuel_annonce_h": 120,
    "volume_horaire_hebdomadaire_h": 4,
    "nombre_de_semaines": 30,
    "reference_document_source": {
        "fichier_local": "source-progression-maths-3e.jpg",
        "nom_originau": "Document de maths.jpg",
        "depot": "https://github.com/digitalholding2026-ux/Relio.git",
        "type": "photographie de tableau de progression (JPEG, 719x1054)",
        "titre_document": "MATHÉMATIQUES — PROGRESSION 3e — 2025-2026",
        "mention_volumes_source": "Volume horaire annuel : 120 heures (4 heures par semaine)",
        "sha256": None,
    },
    "statut_validation": "valide_avec_reserves",
    "statut_validation_detail": (
        "Le volume horaire annuel annoncé (120 h) se réconcilie exactement avec la "
        "somme des éléments transcrits (98 h de leçons + 14 h de régulation + 8 h de "
        "révisions). Les libellés et volumes des 14 leçons sont directement lisibles "
        "sur le document. Réserves subsistantes : la colonne « Taux d'exécution » du "
        "document utilise un dénominateur de 112 h incompatible avec les 120 h annoncés "
        "(voir incohérences), et la répartition horaire semaine par semaine n'est pas "
        "totalement réconciliable à partir de l'image source."
    ),
    "champs_ajouts_prevus_non_remplis": [
        "competences",
        "prerequis",
        "exercices",
        "corriges",
        "references_bepc",
        "objectifs",
    ],
    "note_conformite": (
        "Aucune compétence, prérequis, exercice ou corrigé n'a été renseigné : aucun "
        "document de référence pédagogique n'a été fourni. Ces champs sont présents dans "
        "le schéma mais vides, conformément aux contraintes de la mission."
    ),
}


# ---------------------------------------------------------------------------
# 2. TRANSCRIPTION STRUCTURELLE
# ---------------------------------------------------------------------------
# Trimestres : (numero, libelle, premiere_semaine, derniere_semaine, evaluation)
TRIMESTRES = [
    (1, "1er Trimestre", 1, 11, "Devoir de niveau"),
    (2, "2e Trimestre", 12, 21, "Devoir de niveau"),
    (3, "3e Trimestre", 22, 30, None),
]

# Mois : (numero, libelle, premiere_semaine, derniere_semaine)
MOIS = [
    (9, "Septembre", 1, 3),
    (10, "Octobre", 4, 7),
    (11, "Novembre", 8, 11),
    (12, "Décembre", 12, 14),
    (1, "Janvier", 15, 18),
    (2, "Février", 19, 21),
    (3, "Mars", 22, 25),
    (4, "Avril", 26, 28),
    (5, "Mai", 29, 30),
]

# Semaines de régulation (1 h chacune) : détectées sur la bande grisée du document.
SEMAINES_REGULATION = [2, 4, 6, 9, 12, 13, 15, 17, 19, 21, 23, 24, 26, 28]

# Révision finale : volume et position tels qu'ils figurent sur le document.
REVISION = {"libelle": "Révisions", "volume_h": 8, "semaine": 30}

# Leçons : (rang, intitulé exact, volume h, trimestre, 1re semaine, dernière semaine)
# Les semaines sont le placement lu sur le document ; le détail horaire semaine par
# semaine n'est PAS donné par la source (voir rapport de contrôle, réserve R-2).
LECONS = [
    (1, "Calcul littéral", 7, 1, 1, 2),
    (2, "Propriétés de Thalès dans un triangle", 7, 1, 3, 4),
    (3, "Racines carrées", 7, 1, 5, 6),
    (4, "Triangle rectangle", 11, 1, 7, 9),
    (5, "Calcul numérique", 9, 1, 10, 11),
    (6, "Angles inscrits", 5, 2, 12, 13),
    (7, "Vecteurs", 7, 2, 14, 15),
    (8, "Équations et inéquations dans ℝ", 5, 2, 16, 17),
    (9, "Coordonnées de vecteurs", 7, 2, 18, 19),
    (10, "Équations de droites", 7, 2, 20, 21),
    (11, "Statistique", 7, 3, 22, 23),
    (12, "Équations et inéquations dans ℝ × ℝ", 7, 3, 24, 25),
    (13, "Applications affines", 5, 3, 26, 27),
    (14, "Pyramides et cônes", 7, 3, 28, 29),
]


# ---------------------------------------------------------------------------
# 3. CONSTRUCTION
# ---------------------------------------------------------------------------
def trimestre_de(semaine: int) -> int:
    for num, _, deb, fin, _ in TRIMESTRES:
        if deb <= semaine <= fin:
            return num
    raise ValueError(f"semaine {semaine} hors de tout trimestre")


def mois_de(semaine: int) -> int:
    for num, _, deb, fin in MOIS:
        if deb <= semaine <= fin:
            return num
    raise ValueError(f"semaine {semaine} hors de tout mois")


def id_trimestre(n: int) -> str:
    return f"TRIM-{PREFIXE}-{ANNEE}-{n:02d}"


def id_mois(n: int, annee: str) -> str:
    return f"MOIS-{PREFIXE}-{annee}-{n:02d}"


def id_semaine(n: int) -> str:
    return f"SEM-{PREFIXE}-{ANNEE}-{n:02d}"


def id_lecon(rang: int) -> str:
    return f"LEC-{PREFIXE}-{ANNEE}-{rang:02d}"


def id_regulation(semaine: int) -> str:
    return f"REG-{PREFIXE}-{ANNEE}-S{semaine:02d}"


def id_revision() -> str:
    return f"REV-{PREFIXE}-{ANNEE}-S{REVISION['semaine']:02d}"


def annee_scolaire_du_mois(numero_mois: int) -> str:
    """Septembre..Décembre -> 2025 ; Janvier..Mai -> 2026."""
    return "2025" if numero_mois >= 9 else "2026"


def construire() -> dict:
    semaines = []
    for s in range(1, METADONNEES["nombre_de_semaines"] + 1):
        t = trimestre_de(s)
        m = mois_de(s)
        semaines.append({
            "semaine_id": id_semaine(s),
            "numero": s,
            "trimestre_id": id_trimestre(t),
            "mois_id": id_mois(m, annee_scolaire_du_mois(m)),
            "volume_horaire_previsonnel_h": METADONNEES["volume_horaire_hebdomadaire_h"],
        })

    trimestres = []
    for num, libelle, deb, fin, evaluation in TRIMESTRES:
        semaines_t = [s for s in semaines if deb <= s["numero"] <= fin]
        h_lecons = sum(l[2] for l in LECONS if l[3] == num)
        h_reg = sum(1 for s in semaines_t if s["numero"] in SEMAINES_REGULATION)
        h_rev = REVISION["volume_h"] if REVISION["semaine"] in (range(deb, fin + 1)) else 0
        trimestres.append({
            "trimestre_id": id_trimestre(num),
            "numero": num,
            "libelle": libelle,
            "ordre": num,
            "semaine_debut_id": id_semaine(deb),
            "semaine_fin_id": id_semaine(fin),
            "nombre_semaines": fin - deb + 1,
            "evaluation": evaluation,
            "volume_heures_lecons_h": h_lecons,
            "volume_heures_regulation_h": h_reg,
            "volume_heures_revision_h": h_rev,
            "volume_heures_total_h": h_lecons + h_reg + h_rev,
            "capacite_theorique_h": (fin - deb + 1) * METADONNEES["volume_horaire_hebdomadaire_h"],
        })

    liste_mois = []
    for num, libelle, deb, fin in MOIS:
        annee = annee_scolaire_du_mois(num)
        semaines_m = [s for s in semaines if deb <= s["numero"] <= fin]
        liste_mois.append({
            "mois_id": id_mois(num, annee),
            "libelle": libelle,
            "numero": num,
            "annee": int(annee),
            "ordre_sequentiel": len(liste_mois) + 1,
            "trimestre_id": id_trimestre(trimestre_de(deb)),
            "semaine_debut_id": id_semaine(deb),
            "semaine_fin_id": id_semaine(fin),
            "nombre_semaines": fin - deb + 1,
            "volume_horaire_previsonnel_h": (fin - deb + 1) * METADONNEES["volume_horaire_hebdomadaire_h"],
            "semaine_ids": [s["semaine_id"] for s in semaines_m],
        })

    lecons = []
    for rang, intitule, volume, t, deb, fin in LECONS:
        semaines_l = [s for s in semaines if deb <= s["numero"] <= fin]
        list_mois = []
        for s in semaines_l:
            mid = s["mois_id"]
            if mid not in list_mois:
                list_mois.append(mid)
        list_trim = []
        for s in semaines_l:
            tid = s["trimestre_id"]
            if tid not in list_trim:
                list_trim.append(tid)
        lecons.append({
            "lecon_id": id_lecon(rang),
            "rang": rang,
            "intitule": intitule,
            "intitule_normalise": slug(intitule),
            "volume_horaire_h": volume,
            "ordre": rang,
            "trimestre_id": id_trimestre(t),
            "trimestres_ids": list_trim,
            "mois_ids": list_mois,
            "semaine_debut_id": id_semaine(deb),
            "semaine_fin_id": id_semaine(fin),
            "nombre_semaines": fin - deb + 1,
            "semaine_ids": [s["semaine_id"] for s in semaines_l],
            "provenance": {
                "intitule": "transcrit_document_source",
                "volume_horaire": "transcrit_document_source",
                "placement_trimestre": "transcrit_document_source",
                "placement_semaines": "lecture_document_source_a_confirmer",
            },
            # Extension prévue, non renseignée faute de document de référence.
            "competences": [],
            "prerequis": [],
            "objectifs": [],
            "exercices_ids": [],
            "corriges_ids": [],
            "references_bepc": [],
        })

    regulations = []
    for s in SEMAINES_REGULATION:
        regulations.append({
            "regulation_id": id_regulation(s),
            "libelle": "Régulation",
            "volume_horaire_h": 1,
            "semaine_id": id_semaine(s),
            "semaine_numero": s,
            "trimestre_id": id_trimestre(trimestre_de(s)),
            "mois_id": id_mois(mois_de(s), annee_scolaire_du_mois(mois_de(s))),
            "provenance": "transcrit_document_source",
        })

    revisions = [{
        "revision_id": id_revision(),
        "libelle": REVISION["libelle"],
        "volume_horaire_h": REVISION["volume_h"],
        "semaine_id": id_semaine(REVISION["semaine"]),
        "semaine_numero": REVISION["semaine"],
        "trimestre_id": id_trimestre(trimestre_de(REVISION["semaine"])),
        "mois_id": id_mois(mois_de(REVISION["semaine"]),
                           annee_scolaire_du_mois(mois_de(REVISION["semaine"]))),
        "provenance": "transcrit_document_source",
        "reserve": "R-1",
    }]

    # Séquence ordonnée : ce que l'élève suit semaine après semaine.
    sequence = []
    for s in range(1, METADONNEES["nombre_de_semaines"] + 1):
        sid = id_semaine(s)
        if s == REVISION["semaine"]:
            sequence.append({"semaine_id": sid, "type": "revision",
                             "reference_id": id_revision(), "volume_horaire_h": REVISION["volume_h"]})
            continue
        for l in lecons:
            if sid in l["semaine_ids"]:
                sequence.append({"semaine_id": sid, "type": "lecon",
                                 "reference_id": l["lecon_id"], "volume_horaire_h": l["volume_horaire_h"]})
        for r in regulations:
            if r["semaine_id"] == sid:
                sequence.append({"semaine_id": sid, "type": "regulation",
                                 "reference_id": r["regulation_id"], "volume_horaire_h": 1})

    return {
        "$schema_version": "1.0.0",
        "metadonnees": METADONNEES,
        "trimestres": trimestres,
        "mois": liste_mois,
        "semaines": semaines,
        "lecons": lecons,
        "regulations": regulations,
        "revisions": revisions,
        "sequence": sequence,
    }


def main() -> None:
    ref = construire()

    src = os.path.join(RACINE, METADONNEES["reference_document_source"]["fichier_local"])
    if os.path.isfile(src):
        import hashlib
        with open(src, "rb") as fh:
            ref["metadonnees"]["reference_document_source"]["sha256"] = hashlib.sha256(fh.read()).hexdigest()

    os.makedirs(os.path.dirname(SORTIE), exist_ok=True)
    with open(SORTIE, "w", encoding="utf-8") as fh:
        json.dump(ref, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    h_lecons = sum(l["volume_horaire_h"] for l in ref["lecons"])
    h_reg = sum(r["volume_horaire_h"] for r in ref["regulations"])
    h_rev = sum(r["volume_horaire_h"] for r in ref["revisions"])
    print(f"OK -> {SORTIE}")
    print(f"  leçons     : {len(ref['lecons'])}  = {h_lecons} h")
    print(f"  régulations : {len(ref['regulations'])} = {h_reg} h")
    print(f"  révisions   : {len(ref['revisions'])} = {h_rev} h")
    print(f"  TOTAL       : {h_lecons + h_reg + h_rev} h "
          f"(annoncé : {METADONNEES['volume_horaire_annuel_annonce_h']} h)")


if __name__ == "__main__":
    main()
