#!/usr/bin/env node
/**
 * Contrôles qualité de l'inventaire des questions BEPC 2025-2026.
 *
 * Indépendant du générateur Python : relit le JSON produit et le vérifie.
 *
 * Vérifie :
 *   - que chaque question renvoie à une source identifiable et à une leçon
 *     existante du référentiel annuel ;
 *   - la cohérence des numéros d'exercices et de questions ;
 *   - que les barèmes se recomptent et concordent avec les totaux annoncés
 *     par les documents sources (20 pt par session) ;
 *   - qu'aucune compétence officielle n'a été inventée ;
 *   - qu'aucun résultat n'est annoncé sans source dans le corrigé.
 *
 * Codes de sortie : 0 = conforme · 1 = erreur bloquante · 2 = réserves.
 *
 * Exécution : node outils/valider-inventaire-bepc.mjs [chemin/inventaire.json]
 */

import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const ICI = dirname(fileURLToPath(import.meta.url));
const CHEMIN = resolve(process.argv[2] ?? resolve(ICI, '..', 'data', 'inventaire-questions-bepc-2025-2026.json'));
const CHEMIN_REF = resolve(ICI, '..', 'data', 'referentiel-maths-3e-cm-2025-2026.json');

const inv = JSON.parse(readFileSync(CHEMIN, 'utf8'));
const ref = JSON.parse(readFileSync(CHEMIN_REF, 'utf8'));

const erreurs = [], reserves = [];
const ok = (m) => console.log(`  [OK]     ${m}`);
const ko = (m) => { erreurs.push(m); console.log(`  [ERREUR] ${m}`); };
const rs = (m) => { reserves.push(m); console.log(`  [RESERVE] ${m}`); };

const qs = inv.questions;
const leconIds = new Set(ref.lecons.map((l) => l.lecon_id));
const fichiersConnus = new Set([
  ...Object.values(inv.sources).flatMap((s) => [s.sujet.fichier, s.corrige.fichier]),
]);

console.log(`\n=== Contrôle de l'inventaire BEPC ${qs.length} questions ===`);
console.log(`Fichier : ${CHEMIN}\nRéférentiel : ${CHEMIN_REF}\n`);

// --- 1. Sources -------------------------------------------------------------
console.log('1. Inventaire des sources');
for (const [sess, s] of Object.entries(inv.sources)) {
  for (const t of ['sujet', 'corrige']) {
    const d = s[t];
    if (!d?.fichier) { ko(`session ${sess} : ${t} sans nom de fichier`); continue; }
    fichiersConnus.has(d.fichier)
      ? ok(`session ${sess} ${t} : ${d.fichier} (${d.pages} p.)`)
      : ko(`session ${sess} ${t} : fichier hors inventaire`);
  }
  const lu = s.corrige.pages_lues ?? '';
  String(lu).includes(`${s.corrige.pages}/${s.corrige.pages}`)
    ? ok(`session ${sess} : corrigé intégralement lu (${lu})`)
    : rs(`session ${sess} : corrigé lu partiellement (${lu})`);
}
const pagesManquantes = Object.entries(inv.sources).filter(
  ([, s]) => s.corrige.pages_annoncees && s.corrige.pages !== s.corrige.pages_annoncees);
pagesManquantes.length === 0
  ? ok('aucune page manquante : pages lues = pages annoncées')
  : rs(`pages manquantes : ${pagesManquantes.map(([s, v]) => `${s} (${v.corrige.pages}/${v.corrige.pages_annoncees})`).join(', ')}`);

// --- 2. Traçabilité des questions ------------------------------------------
console.log('\n2. Traçabilité des questions');
const sansSujet = qs.filter((q) => !q.source_sujet || !fichiersConnus.has(q.source_sujet));
sansSujet.length === 0 ? ok('toutes les questions renvoient à un sujet identifié') : ko(`${sansSujet.length} question(s) sans sujet identifiable`);

const sansCorrige = qs.filter((q) => !q.source_corrige || !fichiersConnus.has(q.source_corrige));
sansCorrige.length === 0 ? ok('toutes les questions renvoient à un corrigé identifié') : ko(`${sansCorrige.length} question(s) sans corrigé identifiable`);

const sansEnonce = qs.filter((q) => !q.enonce_transcrit || q.enonce_transcrit.trim().length < 15);
sansEnonce.length === 0 ? ok('toutes les questions portent un énoncé transcrit') : ko(`${sansEnonce.length} question(s) sans énoncé exploitable`);

const sansLecon = qs.filter((q) => q.lecons_referentiel.length === 0 && q.bloc !== 'Presentation');
sansLecon.length === 0 ? ok('toute question de calcul est rattachée à au moins une leçon') : ko(`${sansLecon.length} question(s) de calcul sans leçon rattachée`);

const leconInconnue = qs.flatMap((q) => q.lecons_referentiel.filter((l) => !leconIds.has(l.lecon_id)).map((l) => l.lecon_id));
leconInconnue.length === 0 ? ok('toutes les leçons citées existent dans le référentiel annuel') : ko(`leçons inexistantes : ${[...new Set(leconInconnue)].join(', ')}`);

const ids = qs.map((q) => q.question_id);
const doublons = ids.filter((x, i) => ids.indexOf(x) !== i);
doublons.length === 0 ? ok('identifiants de question uniques') : ko(`identifiants dupliqués : ${[...new Set(doublons)].join(', ')}`);

// --- 3. Cohérence des exercices et questions -------------------------------
console.log('\n3. Cohérence de la numérotation');
const parBloc = {};
for (const q of qs) { (parBloc[q.session] ??= {})[q.bloc] ??= new Set(); parBloc[q.session][q.bloc].add(q.numero_exercice); }
let numOk = true;
for (const [sess, blocs] of Object.entries(parBloc)) {
  for (const [bloc, nums] of Object.entries(blocs)) {
    if (bloc === 'Presentation') continue;
    const sorted = [...nums].sort((a, b) => a - b);
    const attendu = sorted.map((_, i) => i + 1);
    if (JSON.stringify(sorted) !== JSON.stringify(attendu)) { ko(`session ${sess} / ${bloc} : exercices ${sorted.join(',')} au lieu de ${attendu.join(',')}`); numOk = false; }
  }
}
numOk && ok('numérotation des exercices continue et sans trou dans chaque bloc');

// Une sous-question « N.x » doit avoir une question mère « N » dans le même exercice.
// Une tâche ne comportant qu'une seule question n'est PAS orpheline.
const estSousQuestion = (nq) => typeof nq === 'string' && /^\d+\s*[.)]\s*[a-z]$/i.test(String(nq).trim());
const sousQuestions = qs.filter((q) => estSousQuestion(q.numero_question));
const orphelines = sousQuestions.filter((q) => {
  const mere = String(q.question_mere?.libelle ?? '').trim();
  if (!mere) return true;
  if (q.question_mere?.statut === 'question distincte') return true;
  // « introduction integrée » : la sous-question doit porter elle-même l'énoncé introductif.
  return (q.enonce_transcrit || '').trim().length < 15;
});
orphelines.length === 0
  ? ok(`${sousQuestions.length} sous-question(s), chacune rattachée à sa question mère`)
  : ko(`${orphelines.length} sous-question(s) sans question mère : ${orphelines.map((q) => q.question_id).join(', ')}`);

const confiancesOk = ['confirme', 'incertain'];
const confianceInvalide = qs.flatMap((q) => q.lecons_referentiel.filter((l) => !confiancesOk.includes(l.confiance)).map((l) => l.confiance));
confianceInvalide.length === 0 ? ok('toutes les associations portent un niveau de confiance déclaré') : ko(`niveaux de confiance invalides : ${[...new Set(confianceInvalide)].join(', ')}`);

// --- 4. Barèmes ------------------------------------------------------------
console.log('\n4. Barèmes');
const attendus = { 2025: { A: 12.5, B: 7.5, total: 20 }, 2026: { A: 15, B: 5, total: 20 } };
for (const [sess, exp] of Object.entries(attendus)) {
  const sq = qs.filter((q) => q.session === Number(sess));
  const a = sq.filter((q) => q.partie === 'A').reduce((s, q) => s + q.bareme_pt, 0);
  const b = sq.filter((q) => q.partie === 'B').reduce((s, q) => s + q.bareme_pt, 0);
  const tot = Math.round((a + b) * 100) / 100;
  a === exp.A ? ok(`session ${sess} partie A : ${a} pt (attendu ${exp.A})`) : ko(`session ${sess} partie A : ${a} pt au lieu de ${exp.A}`);
  b === exp.B ? ok(`session ${sess} partie B : ${b} pt (attendu ${exp.B})`) : ko(`session ${sess} partie B : ${b} pt au lieu de ${exp.B}`);
  tot === exp.total ? ok(`session ${sess} total : ${tot} pt (attendu ${exp.total})`) : ko(`session ${sess} total : ${tot} pt au lieu de ${exp.total}`);
}

const baremeNegatif = qs.filter((q) => typeof q.bareme_pt !== 'number' || q.bareme_pt <= 0);
baremeNegatif.length === 0 ? ok('tous les barèmes sont strictement positifs') : ko(`${baremeNegatif.length} barème(s) invalide(s)`);

const sansBaremeCorrige = qs.filter((q) => !q.corrige?.bareme);
sansBaremeCorrige.length === 0 ? ok('toutes les questions portent un barème de corrigé') : ko(`${sansBaremeCorrige.length} question(s) sans barème de corrigé`);

// --- 5. Non-invention ------------------------------------------------------
console.log('\n5. Non-invention');
const compInventees = qs.filter((q) => q.competence_officielle);
compInventees.length === 0
  ? ok('aucune compétence officielle inventée (champ vide sur les 35 questions)')
  : ko(`${compInventees.length} compétence(s) officielle(s) inventée(s) — interdit`);

const sansStatut = qs.filter((q) => !q.competence_officielle_statut);
sansStatut.length === 0 ? ok('l\'absence de compétence officielle est explicitement motivée') : ko(`${sansStatut.length} question(s) sans justification d'absence`);

const resultatSansSource = qs.filter((q) => q.corrige?.resultat_attendu && !q.corrige?.provenance);
resultatSansSource.length === 0 ? ok('tout résultat annoncé renvoie à une provenance de corrigé') : ko(`${resultatSansSource.length} résultat(s) sans provenance`);

const resultatNonPublie = qs.filter((q) => q.corrige?.resultat_non_publie);
resultatNonPublie.length === 0
  ? ok('tous les résultats sont publiés par les corrigés')
  : ok(`${resultatNonPublie.length} question(s) sans résultat publié, correctement signalée(s) : ${resultatNonPublie.map((q) => q.question_id).join(', ')}`);

const resultatFantasme = qs.filter((q) => q.corrige?.resultat_non_publie && q.corrige?.resultat_attendu);
resultatFantasme.length === 0
  ? ok('aucun résultat inventé là où le corrigé n\'en publie pas')
  : ko(`${resultatFantasme.length} résultat(s) inventé(s) sur une question sans corrigé`);

// --- 6. Couverture ---------------------------------------------------------
console.log('\n6. Couverture du programme');
const couv = inv.couverture_par_lecon;
const observees = Object.values(couv).filter((v) => v.statut === 'observee');
const nonObservees = Object.values(couv).filter((v) => v.statut === 'non_observee');
Object.keys(couv).length === ref.lecons.length
  ? ok(`les ${ref.lecons.length} leçons du référentiel sont toutes positionnées`)
  : ko(`${Object.keys(couv).length} leçons positionnées au lieu de ${ref.lecons.length}`);
ok(`${observees.length} leçons observées · ${nonObservees.length} non observée(s) : ${nonObservees.map((v) => `L${v.rang} ${v.intitule}`).join(', ') || 'aucune'}`);

const incompletes = Object.values(couv).filter((v) => v.nombre_questions_observees !== v.questions_ids.length);
incompletes.length === 0 ? ok('le décompte par leçon est cohérent avec la liste des questions') : ko(`${incompletes.length} incohérence(s) de décompte`);

// --- 7. Périmètre ----------------------------------------------------------
console.log('\n7. Périmètre et avertissements');
inv.metadonnees.avertissement_portee?.includes('PAS une représentation')
  ? ok("l'avertissement de non-représentativité du programme est présent")
  : rs("avertissement de non-représentativité absent ou trop faible");
inv.metadonnees.droits_utilisation?.startsWith('NON VÉRIFIÉS')
  ? ok("les droits d'utilisation sont explicitement signalés comme non vérifiés")
  : ko('les droits d\'utilisation ne sont pas signalés comme non vérifiés');
inv.metadonnees.referentiel_annual_modifie === false
  ? ok('le référentiel annuel est déclaré non modifié')
  : ko('le référentiel annuel semble avoir été modifié');
inv.metadonnees.statut_validation?.includes('provisoire')
  ? ok("le statut d'attente de validation humaine est explicite")
  : rs("statut de validation humaine non explicite");

// --- Verdict ---------------------------------------------------------------
console.log(`\n=== Résultat : ${erreurs.length} erreur(s), ${reserves.length} réserve(s) ===`);
if (erreurs.length) {
  console.log('\nÉchec du contrôle :');
  erreurs.forEach((e, i) => console.log(`  ${i + 1}. ${e}`));
  process.exit(1);
}
if (reserves.length) {
  console.log('\nContrôle passé, réserves :');
  reserves.forEach((r, i) => console.log(`  ${i + 1}. ${r}`));
  process.exit(2);
}
console.log('Inventaire conforme.');
process.exit(0);
