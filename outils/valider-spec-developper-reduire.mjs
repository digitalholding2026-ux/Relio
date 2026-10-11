#!/usr/bin/env node
/**
 * Contrôle de cohérence documentaire — spécification « développer et réduire » (OO-L1-1).
 *
 * Vérifie que chaque affirmation marquée [VÉRIFIÉ] dans
 * `docs/specification-pedagogique-developper-reduire-v1.md` correspond bien au
 * code réel de `backend/`, et que le document ne se déclare pas validé.
 *
 * Ce contrôle est DOCUMENTAIRE : il n'exécute pas le moteur pédagogique et ne
 * modifie aucun fichier applicatif. Il compare du texte à du texte.
 *
 * Sortie : rapport texte sur stdout. Code de retour 0 = OK, 1 = anomalie bloquante,
 *          2 = réserves (non bloquant, Mostly des points [À VALIDER]).
 *
 * Exécution :  node outils/valider-spec-developper-reduire.mjs
 */

import { readFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const ICI = dirname(fileURLToPath(import.meta.url));
const RACINE = resolve(ICI, '..');
const SPEC = resolve(RACINE, 'docs', 'specification-pedagogique-developper-reduire-v1.md');
const SRC = resolve(RACINE, 'backend', 'src');

const lit = (p) => readFileSync(p, 'utf8');

const erreurs = [];
const reserves = [];

const ok = (m) => console.log(`  [OK]      ${m}`);
const ko = (m) => { erreurs.push(m); console.log(`  [ERREUR]  ${m}`); };
const rs = (m) => { reserves.push(m); console.log(`  [RESERVE] ${m}`); };

// --- Chargement --------------------------------------------------------------

if (!existsSync(SPEC)) {
  console.error(`Document introuvable : ${SPEC}`);
  process.exit(1);
}
const spec = lit(SPEC);
const src = {
  signatures: lit(resolve(SRC, 'contenu', 'signatures.ts')),
  tutorat: lit(resolve(SRC, 'contenu', 'tutorat.ts')),
  exercices: lit(resolve(SRC, 'contenu', 'exercices.ts')),
  correction: lit(resolve(SRC, 'contenu', 'correction.ts')),
  progression: lit(resolve(SRC, 'lib', 'progression.ts')),
};

console.log('=== Contrôle de cohérence documentaire — OO-L1-1 ===\n');

// --- 1. Le document ne doit pas se déclarer validé --------------------------

/Maestro|valide par un enseignant/i.test(spec)
  ? ko('le document affirme être validé alors qu\'il est en attente de validation')
  : ok('le document est explicitement « en attente de validation pédagogique »');

spec.includes('Ne mets pas') || /en attente de validation/i.test(spec)
  ? ok('le statut de non-validation est présent')
  : ko('le statut de non-validation est absent');

// --- 2. Nombre de signatures : le doc doit dire 12 ---------------------------

const blocSignatures = src.signatures.match(/export const SIGNATURES = \[([\s\S]*?)\] as const;/);
if (!blocSignatures) {
  ko('impossible de lire SIGNATURES dans signatures.ts');
} else {
  const liste = [...blocSignatures[1].matchAll(/'([^']+)'/g)].map((m) => m[1]);
  const n = liste.length;
  n === 12
    ? ok(`le catalogue contient bien ${n} signatures`)
    : ko(`le catalogue contient ${n} signatures, la spécification en annonce 12`);
  n !== 11
    ? ok('la spécification annonce 12 signatures, ce qui correspond au code')
    : rs('vérifier le compte de signatures annoncé dans la spécification');
  /12\s*—\s*`signatures\.ts/.test(spec)
    ? ok('la contradiction C-2 (11 vs 12) est tranchée en faveur du code')
    : rs('la contradiction C-2 (11 vs 12) n\'est pas explicitement tranchée dans la spécification');
}

// --- 3. Catégories : 8, et toutes nommées dans le document ------------------

const blocCat = src.tutorat.match(/CATEGORIES_DIFICULTE = \[([\s\S]*?)\] as const;/);
if (!blocCat) {
  ko('impossible de lire CATEGORIES_DIFICULTE dans tutorat.ts');
} else {
  const cats = [...blocCat[1].matchAll(/'([^']+)'/g)].map((m) => m[1]);
  cats.length === 8
    ? ok(`le vocabulaire de catégories contient bien ${cats.length} catégories`)
    : ko(`le vocabulaire contient ${cats.length} catégories, la spécification en annonce 8`);

  const absentes = cats.filter((c) => !spec.includes(`\`${c}\``));
  absentes.length === 0
    ? ok('toutes les catégories du code sont nommées dans la spécification')
    : ko(`catégories du code absentes de la spécification : ${absentes.join(', ')}`);
}

// --- 4. Correspondance totale signature -> catégorie ------------------------

const blocMap = src.tutorat.match(/CATEGORIE_PAR_SIGNATURE[^=]*= \{([\s\S]*?)\n\};/);
if (!blocMap) {
  ko('impossible de lire CATEGORIE_PAR_SIGNATURE dans tutorat.ts');
} else {
  const paires = [...blocMap[1].matchAll(/(\w+):\s*'(\w+)'/g)].map((m) => [m[1], m[2]]);
  const toutes = [...src.signatures.matchAll(/^  '(\w+)',$/gm)].map((m) => m[1]);
  const sansCat = paires.filter(([s]) => !toutes.includes(s)).map(([s]) => s);
  sansCat.length === 0
    ? ok(`chaque signature a une catégorie (${paires.length} paires, correspondance totale)`)
    : ko(`signatures sans catégorie : ${sansCat.join(', ')}`);
}

// --- 5. Les 3 exercices OO-L1-1 ont regleForme: null -----------------------

const blocsEx = [...src.exercices.matchAll(
  /\{\s*id:\s*'(MVP-B1-E[123])'[\s\S]*?objectifs:\s*\['OO-L1-1'\][\s\S]*?regleForme:\s*(\w+)/g,
)];
if (blocsEx.length !== 3) {
  ko(`${blocsEx.length} exercice(s) OO-L1-1 avec regleForme trouvés, 3 attendus`);
} else {
  const avecForme = blocsEx.filter((m) => m[2] !== 'null').map((m) => `${m[1]}=${m[2]}`);
  avecForme.length === 0
    ? ok('les 3 exercices OO-L1-1 ont regleForme: null — « a_determiner » est bien inatteignable')
    : ko(`exercices OO-L1-1 exigeant une forme (donc atteignables) : ${avecForme.join(', ')}`);
}

// --- 6. Réponses attendues citées dans la spécification ---------------------

const attendus = [
  ['MVP-B1-E1', '2x + 1'],
  ['MVP-B1-E2', '4x^2 - 4x + 1'],
  ['MVP-B1-E3', 'x^2 - x - 4'],
];
for (const [id, attendu] of attendus) {
  const bloc = src.exercices.match(new RegExp(`id: '${id}'[\\s\\S]*?\\n  \\},`));
  const trouve = bloc && bloc[0].includes(`reponseAttendue: '${attendu}'`);
  trouve
    ? ok(`${id} : reponseAttendue « ${attendu} » confirmé`)
    : ko(`${id} : la spécification annonce « ${attendu} », le code ne correspond pas`);
}

// --- 7. Pièges cités dans les cas de test ----------------------------------

const pieges = [...src.exercices.matchAll(
  /id:\s*'MVP-B1-E[123]'[\s\S]*?pieges:\s*\[([\s\S]*?)\n    \],/g,
)].flatMap((m) => [...m[1].matchAll(/reponse:\s*'([^']+)',\s*signature:\s*'(\w+)'/g)]
  .map((p) => [p[1], p[2]]));

const citesTest = [
  ['4x + 1', 'signe_non_distribue'],
  ['2x + 11', 'signe_non_distribue'],
  ['2x + 1 + x', 'termes_non_collectes'],
  ['2x', 'termes_non_collectes'],
  ['4x^2 + 4x + 1', 'signe_non_distribue'],
  ['2x^2 - 2x + 1', 'hors_perimetre'],
  ['4x^2 - 4x', 'termes_non_collectes'],
  ['x^2 + 3x - 4', 'signe_non_distribue'],
  ['x^2 + x - 4', 'hors_perimetre'],
  ['x^2 - x - 8', 'signe_non_distribue'],
];
let citesOK = 0;
for (const [rep, sig] of citesTest) {
  const reel = pieges.find((p) => p[0] === rep);
  if (!reel) { ko(`piège cité « ${rep} » absent du code`); continue; }
  if (reel[1] !== sig) { ko(`piège « ${rep} » : spec dit ${sig}, code dit ${reel[1]}`); continue; }
  citesOK++;
}
citesOK === citesTest.length
  ? ok(`les ${citesTest.length} pièges cités dans les cas de test correspondent au code`)
  : rs(`${citesOK}/${citesTest.length} pièges cités correspondent`);

// --- 8. Ordre D5 inchangé ----------------------------------------------------

const dv = src.correction.match(/function deriverVerdict\([\s\S]*?\n\}/);
if (!dv) {
  ko('impossible de lire deriverVerdict dans correction.ts');
} else {
  const corps = dv[0];
  const iIncorrect = corps.indexOf("if (!juste) return 'incorrect'");
  const iAcheve = corps.indexOf("achevement === 'inacheve'");
  const iForme = corps.indexOf('formeRespectee === false');
  const iDet = corps.indexOf('return \'a_determiner\'');
  const ordreOK =
    iIncorrect >= 0 && iAcheve > iIncorrect && iForme > iAcheve && iDet > iForme;
  ordreOK
    ? ok('l\'ordre D5 (incorrect → inacheve → forme → a_determiner → correct) est bien celui documenté')
    : ko('l\'ordre de deriverVerdict ne correspond pas à l\'ordre D5 documenté');
}

// --- 9. Le niveau d'aide ne dépend QUE du nombre d'échecs (état actuel) -----

const npe = src.tutorat.match(/export function niveauPourNbEchecs\([\s\S]*?\n\}/);
npe && !/categorie|signature/.test(npe[0])
  ? ok('niveauPourNbEchecs ne dépend que du nombre d\'échecs — l\'écart décrit au § L4.1 est exact')
  : rs('niveauPourNbEchecs semble désormais dépendre d\'autre chose que nbEchecs : revoir § L4.1');

// --- 10. Le moteur n'atteint pas de statut de maîtrise --------------------

// --- 10. Le moteur n'atteint pas de statut de maîtrise --------------------
// On lit le TABLEAU des statuts, pas le texte du fichier : `progression.ts`
// *mentionne* `acquis_confirme` dans un commentaire pour dire qu'il est hors
// périmètre. Chercher la chaîne n'aurait aucun sens.

const blocStatuts = src.progression.match(/STATUTS_OBJECTIF = \[([\s\S]*?)\] as const;/);
if (!blocStatuts) {
  ko('impossible de lire STATUTS_OBJECTIF dans progression.ts');
} else {
  const statuts = [...blocStatuts[1].matchAll(/'([^']+)'/g)].map((m) => m[1]);
  const liste = statuts.join(', ');
  statuts.length === 4 && liste === 'non_evalue, signal, hypothese, constat'
    ? ok(`progression.ts expose exactement 4 statuts (${liste}) — aucun statut de maîtrise`)
    : ko(`statuts de progression inattendus : ${liste}`);
  !statuts.some((s) => /maitr|acquis|confirme/.test(s))
    ? ok('aucun statut de maîtrise parmi les statuts — cohérent avec le § L5')
    : ko(`un statut de maîtrise existe dans le code : ${statuts.join(', ')}`);
}

// --- 11. Référence de fichiers vérifiables ---------------------------------

const refs = [...spec.matchAll(/`((?:backend|frontend|docs)\/[\w\-./]+?)(?::\d+(?:,\s*\d+)*)?`/g)]
  .map((m) => m[1]);
const fichiers = [...new Set(refs)];
const absents = fichiers.filter((f) => !existsSync(resolve(RACINE, f)));
absents.length === 0
  ? ok(`les ${fichiers.length} fichiers cités par la spécification existent tous`)
  : ko(`fichiers cités mais introuvables : ${absents.join(', ')}`);

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
console.log('\nContrôle conforme.');
process.exit(0);