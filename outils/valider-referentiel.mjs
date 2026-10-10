#!/usr/bin/env node
/**
 * Contrôle de cohérence du référentiel de progression — Maths 3e (Cameroun, 2025-2026).
 *
 * Vérifie, de manière INDEPENDANTE du générateur Python :
 *   - la présence et l'ordre des 14 leçons ;
 *   - la concordance des identifiants et des clés étrangères ;
 *   - la somme des volumes horaires ;
 *   - la cohérence avec les 120 heures annoncées ;
 *   - la présence et le placement des périodes de régulation et de révision ;
 *   - la cohérence du découpage trimestres / mois / semaines.
 *
 * Sortie : rapport texte sur stdout. Code de retour 0 = OK, 1 = anomalie bloquante,
 *          2 = réserves (non bloquant).
 *
 * Exécution :  node outils/valider-referentiel.mjs [chemin/vers/referentiel.json]
 */

import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const ICI = dirname(fileURLToPath(import.meta.url));
const CHEMIN = resolve(
  process.argv[2] ?? resolve(ICI, '..', 'data', 'referentiel-maths-3e-cm-2025-2026.json'),
);

const ref = JSON.parse(readFileSync(CHEMIN, 'utf8'));

const erreurs = [];   // bloquantes
const reserves = [];  // non bloquantes

const ok = (m) => console.log(`  [OK]    ${m}`);
const ko = (m) => { erreurs.push(m); console.log(`  [ERREUR] ${m}`); };
const rs = (m) => { reserves.push(m); console.log(`  [RESERVE] ${m}`); };

const M = ref.metadonnees;
const parId = (arr) => new Map(arr.map((x) => [Object.values(x)[0], x]));
const idDe = (o) => o[Object.keys(o)[0]];

const semaines = ref.semaines;
const lecons = ref.lecons;
const regs = ref.regulations;
const revs = ref.revisions;
const mois = ref.mois;
const trims = ref.trimestres;

const hLecons = lecons.reduce((s, l) => s + l.volume_horaire_h, 0);
const hRegs = regs.reduce((s, r) => s + r.volume_horaire_h, 0);
const hRevs = revs.reduce((s, r) => s + r.volume_horaire_h, 0);
const hTotal = hLecons + hRegs + hRevs;

console.log(`\n=== Contrôle du référentiel : ${M.referentiel_id} ===`);
console.log(`Fichier : ${CHEMIN}\n`);

// --- 1. Métadonnées ---------------------------------------------------------
console.log('1. Métadonnées');
const metaAttendus = {
  pays: 'Cameroun',
  systeme_educatif: 'francophone',
  classe: '3e',
  matiere: 'Mathématiques',
  annee_scolaire: '2025-2026',
};
for (const [cle, attendu] of Object.entries(metaAttendus)) {
  M[cle] === attendu ? ok(`${cle} = ${M[cle]}`) : ko(`${cle} attendu « ${attendu} », obtenu « ${M[cle]} »`);
}
M.reference_document_source?.fichier_local
  ? ok(`référence document source : ${M.reference_document_source.fichier_local}`)
  : ko('référence document source absente');
M.statut_validation
  ? ok(`statut de validation : ${M.statut_validation}`)
  : ko('statut de validation absent');

// --- 2. Leçons --------------------------------------------------------------
console.log('\n2. Leçons principales');
lecons.length === 14
  ? ok('14 leçons présentes')
  : ko(`${lecons.length} leçons au lieu de 14`);

const rangs = lecons.map((l) => l.rang);
const attendus = Array.from({ length: lecons.length }, (_, i) => i + 1);
JSON.stringify(rangs) === JSON.stringify(attendus)
  ? ok('ordre des leçons conforme (rangs 1..14 sans trou ni doublon)')
  : ko(`ordre des leçons non conforme : ${rangs.join(',')}`);

const sansIntitule = lecons.filter((l) => !l.intitule || !l.intitule.trim());
sansIntitule.length === 0
  ? ok('toutes les leçons ont un intitulé')
  : ko(`${sansIntitule.length} leçon(s) sans intitulé`);

const sansVolume = lecons.filter((l) => typeof l.volume_horaire_h !== 'number' || l.volume_horaire_h <= 0);
sansVolume.length === 0
  ? ok('toutes les leçons ont un volume horaire positif')
  : ko(`${sansVolume.length} leçon(s) avec volume horaire invalide`);

// Unicité et stabilité des identifiants (les intitulés ne servent pas d'id).
const ids = [...lecons, ...regs, ...revs, ...semaines, ...mois, ...trims].map(idDe);
const doublons = ids.filter((x, i) => ids.indexOf(x) !== i);
doublons.length === 0
  ? ok('tous les identifiants sont uniques')
  : ko(`identifiants dupliqués : ${[...new Set(doublons)].join(', ')}`);

const idSurIntitule = lecons.filter((l) => l.lecon_id === l.intitule || l.lecon_id === l.intitule_normalise);
idSurIntitule.length === 0
  ? ok('aucun identifiant de leçon n\'est construit à partir de l\'intitulé')
  : ko(`${idSurIntitule.length} identifiant(s) de leçon dérivés de l'intitulé`);

// --- 3. Intégrité référentielle --------------------------------------------
console.log('\n3. Intégrité référentielle');
const setSem = new Set(semaines.map((s) => s.semaine_id));
const setMois = new Set(mois.map((m) => m.mois_id));
const setTrim = new Set(trims.map((t) => t.trimestre_id));

const refsOrphelins = [];
const check = (v, set, quoi) => { if (v && !set.has(v)) refsOrphelins.push(`${quoi} -> ${v}`); };

for (const s of semaines) { check(s.trimestre_id, setTrim, 'semaine.trimestre_id'); check(s.mois_id, setMois, 'semaine.mois_id'); }
for (const l of lecons) {
  check(l.trimestre_id, setTrim, 'lecon.trimestre_id');
  l.mois_ids?.forEach((v) => check(v, setMois, 'lecon.mois_ids'));
  l.semaine_ids?.forEach((v) => check(v, setSem, 'lecon.semaine_ids'));
  check(l.semaine_debut_id, setSem, 'lecon.semaine_debut_id');
  check(l.semaine_fin_id, setSem, 'lecon.semaine_fin_id');
  l.trimestres_ids?.forEach((v) => check(v, setTrim, 'lecon.trimestres_ids'));
}
for (const r of [...regs, ...revs]) check(r.semaine_id, setSem, 'periode.semaine_id');
for (const s of [...mois, ...trims]) {
  check(s.trimestre_id, setTrim, 'periode.trimestre_id');
  check(s.semaine_debut_id, setSem, 'periode.semaine_debut_id');
  check(s.semaine_fin_id, setSem, 'periode.semaine_fin_id');
}
refsOrphelins.length === 0
  ? ok('aucune référence orpheline entre semaines, mois, trimestres, leçons et périodes')
  : ko(`références orphelines : ${refsOrphelins.join(' | ')}`);

// --- 4. Découpage calendaire ------------------------------------------------
console.log('\n4. Découpage calendaire');
const nums = semaines.map((s) => s.numero);
const suite = Array.from({ length: M.nombre_de_semaines }, (_, i) => i + 1);
JSON.stringify(nums) === JSON.stringify(suite)
  ? ok(`${semaines.length} semaines numérotées 1..${M.nombre_de_semaines} sans trou`)
  : ko(`numérotation des semaines incohérente : ${nums.join(',')}`);

const couverture = mois.reduce((s, m) => s + m.nombre_semaines, 0);
couverture === semaines.length
  ? ok(`les mois couvrent les ${semaines.length} semaines sans recouvrement`)
  : ko(`les mois couvrent ${couverture} semaines au lieu de ${semaines.length}`);

const couvertureT = trims.reduce((s, t) => s + t.nombre_semaines, 0);
couvertureT === semaines.length
  ? ok(`les trimestres couvrent les ${semaines.length} semaines sans recouvrement`)
  : ko(`les trimestres couvrent ${couvertureT} semaines au lieu de ${semaines.length}`);

// Chaque semaine tombe bien dans le mois et le trimestre déclarés.
const numSem = (id) => Number(String(id).match(/(\d{2})$/)?.[1]);
const bornes = (p) => [numSem(p.semaine_debut_id), numSem(p.semaine_fin_id)];
let incoherentes = 0;
const detail = [];
for (const s of semaines) {
  const m = mois.find((x) => x.mois_id === s.mois_id);
  const t = trims.find((x) => x.trimestre_id === s.trimestre_id);
  if (!m || !t) { incoherentes++; detail.push(`S${s.numero} : parent introuvable`); continue; }
  const [md, mf] = bornes(m);
  const [td, tf] = bornes(t);
  if (s.numero < md || s.numero > mf) { incoherentes++; detail.push(`S${s.numero} hors mois ${m.libelle}`); }
  if (s.numero < td || s.numero > tf) { incoherentes++; detail.push(`S${s.numero} hors ${t.libelle}`); }
}
incoherentes === 0
  ? ok('chaque semaine est rattachée au bon mois et au bon trimestre')
  : ko(`${incoherentes} rattachement(s) incorrect(s) : ${detail.join('; ')}`);

// --- 5. Volumes horaires ----------------------------------------------------
console.log('\n5. Volumes horaires');
console.log(`  leçons ${hLecons} h + régulations ${hRegs} h + révisions ${hRevs} h = ${hTotal} h`);
hTotal === M.volume_horaire_annuel_annonce_h
  ? ok(`total ${hTotal} h conforme aux ${M.volume_horaire_annuel_annonce_h} h annoncés`)
  : ko(`total ${hTotal} h ≠ ${M.volume_horaire_annuel_annonce_h} h annoncés`);

const theorique = M.nombre_de_semaines * M.volume_horaire_hebdomadaire_h;
theorique === M.volume_horaire_annuel_annonce_h
  ? ok(`${M.nombre_de_semaines} semaines × ${M.volume_horaire_hebdomadaire_h} h = ${theorique} h (cohérent avec l'annonce)`)
  : ko(`${M.nombre_de_semaines} × ${M.volume_horaire_hebdomadaire_h} = ${theorique} h ≠ ${M.volume_horaire_annuel_annonce_h} h annoncés`);

const sommeTrim = trims.reduce((s, t) => s + t.volume_heures_total_h, 0);
sommeTrim === hTotal
  ? ok('la somme des volumes par trimestre égale le total annuel')
  : ko(`somme par trimestre ${sommeTrim} h ≠ total ${hTotal} h`);

// Détail semaine par semaine : le document ne ventile PAS les heures de chaque
// leçon entre ses semaines. On contrôle donc la faisabilité : la capacité des
// semaines couvertes par une leçon (4 h/semaine, moins la régulation) doit
// être suffisante pour porter le volume de la leçon.
const semainesDe = (id) => numSem(id);
const capacite = (nums) => nums.reduce(
  (s, n) => s + M.volume_horaire_hebdomadaire_h - (regs.some((r) => r.semaine_numero === n) ? 1 : 0), 0,
);

const infaisables = [];
for (const l of lecons) {
  const nums = (l.semaine_ids ?? []).map(semainesDe);
  const dispo = capacite(nums);
  if (l.volume_horaire_h > dispo) {
    infaisables.push(`${l.lecon_id} « ${l.intitule} » : ${l.volume_horaire_h} h pour ${dispo} h disponibles (déficit ${l.volume_horaire_h - dispo} h)`);
  }
}
const exces = [];
for (const l of lecons) {
  const nums = (l.semaine_ids ?? []).map(semainesDe);
  const dispo = capacite(nums);
  if (dispo > l.volume_horaire_h) exces.push(`${l.lecon_id} (+${dispo - l.volume_horaire_h} h)`);
}
if (infaisables.length === 0) {
  ok('aucune leçon ne dépasse la capacité des semaines qu\'elle couvre');
} else {
  rs(`capacité insuffisante pour ${infaisables.length} leçon(s) — le document ne ventile pas les heures par semaine :\n         - ${infaisables.join('\n         - ')}`);
}
if (exces.length) {
  rs(`capacité en excédent pour ${exces.length} leçon(s) : ${exces.join(', ')}`);
}

// --- 6. Périodes de régulation et de révision ------------------------------
console.log('\n6. Périodes de régulation et de révision');
regs.length > 0 ? ok(`${regs.length} périodes de régulation présentes`) : ko('aucune période de régulation');
revs.length > 0 ? ok(`${revs.length} période de révision présente`) : ko('aucune période de révision');
regs.every((r) => r.volume_horaire_h > 0) ? ok('toutes les régulations ont un volume > 0') : ko('régulation à volume nul');
revs.every((r) => r.volume_horaire_h > 0) ? ok('la révision a un volume > 0') : ko('révision à volume nul');

const regHorsSequence = regs.filter((r) => !ref.sequence.some((s) => s.reference_id === r.regulation_id));
regHorsSequence.length === 0 ? ok('toutes les régulations figurent dans la séquence') : ko(`${regHorsSequence.length} régulation(s) absente(s) de la séquence`);

const leconsHorsSequence = lecons.filter((l) => !ref.sequence.some((s) => s.reference_id === l.lecon_id));
leconsHorsSequence.length === 0 ? ok('toutes les leçons figurent dans la séquence') : ko(`${leconsHorsSequence.length} leçon(s) absente(s) de la séquence`);

const semaineRev = revs[0]?.semaine_numero;
const semaineRevEstDerniere = semaineRev === M.nombre_de_semaines;
semaineRevEstDerniere
  ? ok(`la révision est positionnée sur la dernière semaine (S${semaineRev})`)
  : rs(`la révision est en S${semaineRev} alors que l'année compte ${M.nombre_de_semaines} semaines`);

if (revs[0] && revs[0].volume_horaire_h > M.volume_horaire_hebdomadaire_h) {
  rs(`la révision porte ${revs[0].volume_horaire_h} h sur une seule semaine de ${M.volume_horaire_hebdomadaire_h} h : dépassement de ${revs[0].volume_horaire_h - M.volume_horaire_hebdomadaire_h} h (hypothèse : la révision s'étend sur 2 semaines — NON appliqué)`);
}

// --- 7. Champs d'extension prévus mais vides --------------------------------
console.log('\n7. Extensions prévues (non renseignées)');
const champs = ['competences', 'prerequis', 'exercices_ids', 'corriges_ids', 'references_bepc'];
const manquants = [];
for (const l of lecons) for (const c of champs) if (!(c in l)) manquants.push(`${l.lecon_id}.${c}`);
manquants.length === 0
  ? ok('tous les champs d\'extension sont présents sur chaque leçon (vides, non inventés)')
  : ko(`champs d'extension manquants : ${manquants.join(', ')}`);

const nonVides = lecons.flatMap((l) => champs.filter((c) => Array.isArray(l[c]) && l[c].length > 0));
nonVides.length === 0
  ? ok('aucune compétence, prérequis, exercice, corrigé ou référence BEPC inventé')
  : ko('des données pédagogiques ont été renseignées sans document de référence');

// --- Verdict ----------------------------------------------------------------
console.log(`\n=== Résultat : ${erreurs.length} erreur(s), ${reserves.length} réserve(s) ===`);
if (erreurs.length) {
  console.log('\nÉchec du contrôle. Anomalies bloquantes :');
  erreurs.forEach((e, i) => console.log(`  ${i + 1}. ${e}`));
  process.exit(1);
}
if (reserves.length) {
  console.log('\nContrôle passé, réserves à documenter (non bloquantes) :');
  reserves.forEach((r, i) => console.log(`  ${i + 1}. ${r}`));
  process.exit(2);
}
console.log('Contrôle conforme.');
process.exit(0);
