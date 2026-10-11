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

// --- 1. Statut des decisions (Q1 a Q11 arbitrees) --------------------------
// Depuis le chantier 8.2, les ONZE decisions sont arbitrees par le responsable
// produit. Aucun controle ne doit accepter un sous-ensemble, ni inventer une
// validation enseignante.

// Encadre des decisions validees (SS L0.5) : plusieurs controles exigent que les
// termes cles y figurent, et pas seulement "quelque part dans le document".
const D0 = spec.indexOf('## 0.5 D');
const D1 = spec.indexOf('### 0.2 P');
const ENCADRE = D0 >= 0 && D1 > D0 ? spec.slice(D0, D1) : '';

// 1a. Aucune validation enseignante, meme en formulation affirmative.
const claims = [...spec.matchAll(/.{0,60}valid\u00e9e? par un enseignant/gi)]
  .map((m) => m[0])
  .filter((ctx) => !/n'a\s*PAS\s*été\s*valid/i.test(ctx) && !/aucune/i.test(ctx));
claims.length === 0
  ? ok("le document ne revendique aucune validation enseignante")
  : ko(`affirmation positive de validation enseignante detectee : \u00ab ${claims[0].trim()} \u00bb`);

// 1b. Le document doit annoncer que Q1 a Q11 sont arbitrees.
/Q1 . Q11 sont arbitr/i.test(spec)
  ? ok('le statut « Q1 a Q11 arbitrees » est explicite dans le document')
  : ko('le statut « Q1 a Q11 arbitrees » est absent ou formule autrement');

// 1c. Les 11 decisions doivent etre citees dans l encadre L0.5.
const attendues = ['Q1','Q2','Q3','Q4','Q5','Q6','Q7','Q8','Q9','Q10','Q11'];
const absentesEnc = attendues.filter((q) => !ENCADRE.includes(`**${q} \u2014`));
absentesEnc.length === 0
  ? ok(`les ${attendues.length} decisions sont citees dans l encadre L0.5`)
  : ko(`decisions absentes de l encadre L0.5 : ${absentesEnc.join(', ')}`);

// 1d. Aucun marqueur [VALIDE] ne doit citer une question hors Q1-Q11.
const VALIDE_MARK_RE = /\*\*\[VALID\u00c9[^\]]*\]\*\*/g;
const markersValide = [...spec.matchAll(VALIDE_MARK_RE)].map((m) => m[0]);
const qsValide = new Set([...spec.matchAll(VALIDE_MARK_RE)]
  .flatMap((m) => [...m[0].matchAll(/Q(\d+)/g)].map((n) => 'Q' + n[1])));
const horsQ = [...qsValide].filter((q) => !attendues.includes(q));
markersValide.length === 0
  ? ko('aucun marqueur [VALIDE] alors que Q1-Q11 sont validees')
  : horsQ.length === 0
    ? ok(`les ${markersValide.length} marqueurs [VALIDÉ] ne citent que Q1 a Q11`)
    : ko(`le marqueur [VALIDE] cite des questions non validees : ${horsQ.join(', ')}`);

// 1e. Aucune question de DECISION ne doit rester presentee comme ouverte dans
// L8.0 (les questions techniques I-1..I-7 sont legitimes et hors perimetre).
const L80 = spec.slice(spec.indexOf('## L8.0'), spec.indexOf('## L8.1'));
/\bQ(1[01]|[1-9])\b[^.]{0,80}\b(reste|restent|demande|encore)\b[^.]{0,30}ouverte|questions? de d[ée]cision[^.]{0,60}(restent ouvertes|encore ouvertes)/i.test(L80)
  ? ko('la section L8.0 presente encore des questions de decision comme ouvertes')
  : ok('la section L8.0 ne presente aucune question de decision comme ouverte');

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

// --- 12. Decisions 8.2 : Q6 (24 h), Q9 (nom), Q11, Q7 vs plafond --------------
// Ces controles exigent que le terme cle figure DANS la section concernee et
// DANS l encadre de decision, et pas seulement "quelque part" : plusieurs
// termes apparaissent a plusieurs endroits du document, et un simple includes
// passerait meme si la regle avait disparu de la section visee.

// 12a. Q6 : le delai de 24 h doit figurer dans l encadre de decision ET dans L5.4.
const L54 = spec.slice(spec.indexOf('## L5.4'), spec.indexOf('## L5.5'));
ENCADRE.includes('24 heures') && L54.includes('24 heures')
  ? ok('Q6 : le delai de 24 h figure dans l encadre et dans la section L5.4')
  : ko('Q6 : le delai de 24 h ne figure pas dans l encadre ET/OU dans L5.4');

// 12b. Q6 : la verification doit etre une seance distincte.
ENCADRE.includes('ance distincte') && /s[ée]ance distincte/i.test(L54)
  ? ok('Q6 : la condition de seance distincte est presente')
  : ko('Q6 : la condition de seance distincte est absente de l encadre ou de L5.4');

// 12c. Q9 : le nom canonique exact, dans l encadre ET dans L1.0.
const CANON = 'Développer et réduire une expression littérale';
const L10 = spec.slice(spec.indexOf('## L1.0'), spec.indexOf('# LIVRABLE 1'));
ENCADRE.includes(CANON) && L10.includes(CANON)
  ? ok('Q9 : le nom canonique figure dans l encadre et dans la section L1.0')
  : ko(`Q9 : le nom canonique « ${CANON} » est absent de l encadre ou de L1.0`);

// 12d. Q9 : la distinction litterale / algébrique doit etre explicitée.
L10.includes('littérale') && L10.includes('algébrique')
  ? ok('Q9 : la distinction litterale / algébrique est explicitée dans L1.0')
  : rs('Q9 : la distinction litterale / algébrique n est pas explicitée dans L1.0');

// 12e. Q11 : la distinction indice disponible / consulte doit etre ecrite dans L5.6.
const L56 = spec.slice(spec.indexOf('## L5.6'), spec.indexOf('## L5.7'));
/disponible/i.test(L56) && /non consult|pas consulté|aucun ouvert/i.test(L56)
  ? ok('Q11 : la distinction indice disponible / consulte est ecrite dans L5.6')
  : ko('Q11 : la distinction indice disponible / consulte est absente de L5.6');

// 12f. Q11 : le cas de l aide anterieure doit etre traite dans L5.6.
L56.includes('antérieure')
  ? ok('Q11 : le cas de l aide consultee lors d une tentative anterieure est traite')
  : ko('Q11 : le cas de l aide anterieure est absent de L5.6');

// 12g. Q7 : la contradiction avec TENTATIVES_MAX doit etre signalee dans L6.3,
// avec le VRAI chiffre lu dans le code applicatif (pas une constante en dur).
const observations = lit(resolve(RACINE, 'frontend', 'src', 'lib', 'observations.ts'));
const cap = observations.match(/TENTATIVES_MAX\s*=\s*(\d+)/);
const L63 = spec.slice(spec.indexOf('## L6.3'), spec.indexOf('## L6.4'));
cap && L63.includes('TENTATIVES_MAX') && L63.includes(cap[1])
  ? ok(`Q7 : la contradiction avec le plafond reel (${cap[1]}) est signalee dans L6.3`)
  : ko(`Q7 : la contradiction avec le plafond reel (${cap ? cap[1] : '?'}) n est pas signalee dans L6.3`);

// 12h. Q7 : l effacement par l eleve doit etre reconnu, et la fonction existe.
const EFFACER = /export function effacerJournal/.test(observations);
L63.includes('effacerJournal') && EFFACER
  ? ok('Q7 : l effacement par l eleve est reconnu dans L6.3 (fonction verifiee dans le code)')
  : ko('Q7 : l effacement par l eleve n est pas reconnu dans L6.3, ou la fonction est absente du code');

// 12i. Q7 : le document doit preciser que la decision n'est PAS une politique
// de protection des donnees des mineurs finalisee. On verifie la NEGATION
// explicite ; detecter une simple mention du sujet serait un faux positif.
const L63final = spec.slice(spec.indexOf('## L6.3'), spec.indexOf('## L6.4'));
/ne pr[ée]tend pas|n'est pas|pas une/i.test(L63final) && /mineurs|protection/i.test(L63final)
  ? ok('Q7 : le document precise que la decision nest pas une politique de mineurs finalisee')
  : ko('Q7 : le document ne precise PAS que la decision nest pas une politique de mineurs finalisee');

// --- 13. Les citations fichier:ligne de la spec doivent exister ---------------
// Une citation fausse (ligne decalee) passerait silencieusement : on verifie
// donc que chaque couple fichier:ligne designe un fichier reellement present.
const CIT_RE = /`([\w.\-/]+\.(?:ts|tsx|mjs|md))(?::(\d+)(?:\s*,\s*:?(\d+))*)`/g;
const cites = [...spec.matchAll(CIT_RE)];
const fichiersRel = [...new Set(cites.map((m) => m[1]))];
const racineFichiers = ['observations.ts', 'correction.ts', 'progression.ts', 'aides.ts',
  'exercices.ts', 'blocs.ts', 'tutorat.ts', 'signatures.ts', 'egalite.ts',
  'analyseur-expression.ts', 'parcours.ts', 'suivi.ts'];

const introuvables = [];
for (const rel of fichiersRel) {
  //On ne controle que les noms de fichiers courts references avec une ligne.
  if (!racineFichiers.includes(rel)) continue;
  const candidats = [
    resolve(RACINE, 'backend', 'src', 'contenu', rel),
    resolve(RACINE, 'backend', 'src', 'lib', rel),
    resolve(RACINE, 'frontend', 'src', 'lib', rel),
    resolve(RACINE, 'docs', rel),
  ].filter((x) => existsSync(x));
  if (candidats.length === 0) introuvables.push(`${rel} (fichier introuvable)`);
}
const citesAvecNomCourt = [...new Set(cites
  .filter((m) => racineFichiers.includes(m[1]))
  .map((m) => m[1]))];
introuvables.length === 0
  ? ok(`les ${citesAvecNomCourt.length} fichiers cites avec numero de ligne existent tous`)
  : ko(`fichiers cites introuvables : ${introuvables.join(', ')}`);

// Les nombres de ligne cites doivent rester dans la plage du fichier.
const horsPlage = [];
for (const [, rel, l1, l2] of cites) {
  if (!racineFichiers.includes(rel)) continue;
  const chemin = [
    resolve(RACINE, 'backend', 'src', 'contenu', rel),
    resolve(RACINE, 'backend', 'src', 'lib', rel),
    resolve(RACINE, 'frontend', 'src', 'lib', rel),
    resolve(RACINE, 'docs', rel),
  ].find((x) => existsSync(x));
  if (!chemin) continue;
  const nb = lit(chemin).split('\n').length;
  for (const l of [l1, l2].filter(Boolean).map(Number)) {
    if (l > nb) horsPlage.push(`${rel}:${l} (fichier de ${nb} lignes)`);
  }
}
horsPlage.length === 0
  ? ok('tous les numeros de ligne cites existent dans leurs fichiers')
  : ko(`numeros de ligne hors plage : ${horsPlage.join(', ')}`);

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