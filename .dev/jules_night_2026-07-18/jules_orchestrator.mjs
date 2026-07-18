#!/usr/bin/env node
/**
 * Orchestrateur de nuit Jules — accident-main (18 juillet 2026).
 * Concatène PROMPT_COMMUN.md + Mxx_*.md, puis crée une session Jules
 * (repo criloOcom/accident-main, branch main, autoPr) par mission.
 *
 * PILLERS :
 *   🔴 Piller 1 — Intégrer HB BARBER (M01-M04)
 *   🟡 Piller 2 — Préparer déplacement semaine prochaine (M05-M09)
 *   🟢 Piller 3 — Nettoyage / Anti-hallucination (M10-M15)
 *
 * Usage :
 *   node jules_orchestrator.mjs --test M04        # test sur 1 mission
 *   node jules_orchestrator.mjs --all             # les 15 missions
 *   node jules_orchestrator.mjs --missions M01,M04,M07
 */
import fs from 'fs';
import path from 'path';
import { spawn } from 'child_process';
import readline from 'readline';

const DIR = path.dirname(new URL(import.meta.url).pathname);
const WRAPPER = process.env.JULES_WRAPPER || '/home/crilocom/.opencode/mcp-wrappers/mcp-jules.sh';
const MAP_PATH = path.join(DIR, 'SESSION_MAP.json');
const LOG_PATH = path.join(DIR, 'STATE_LOG.json');

function buildPrompt(mfile) {
  const commun = fs.readFileSync(path.join(DIR, 'PROMPT_COMMUN.md'), 'utf-8');
  const spec = fs.readFileSync(path.join(DIR, mfile), 'utf-8');
  return commun + '\n' + spec;
}

function listMissions() {
  return fs.readdirSync(DIR)
    .filter(f => /^M\d{2}_.*\.md$/.test(f))
    .sort();
}

function updateMap(mission, sessionId) {
  const map = JSON.parse(fs.readFileSync(MAP_PATH, 'utf-8'));
  map.missions[mission] = { sessionId, status: 'launched', launchedAt: new Date().toISOString() };
  fs.writeFileSync(MAP_PATH, JSON.stringify(map, null, 2));
  return true;
}

function updateLog(stats) {
  const log = JSON.parse(fs.readFileSync(LOG_PATH, 'utf-8'));
  log.stats = { ...log.stats, ...stats };
  log.lastUpdated = new Date().toISOString();
  fs.writeFileSync(LOG_PATH, JSON.stringify(log, null, 2));
}

function spawnServer() {
  const p = spawn(WRAPPER, [], { shell: true });
  const rl = readline.createInterface({ input: p.stdout });
  return { p, rl };
}

function createSession({ title, prompt, repo, branch, autoPr }) {
  return new Promise((resolve) => {
    const { p, rl } = spawnServer();
    let done = false;
    const callbacks = new Map();
    let callId = 1;

    function callTool(name, params) {
      return new Promise((res) => {
        const id = 'call-' + (callId++);
        callbacks.set(id, res);
        p.stdin.write(JSON.stringify({ jsonrpc: '2.0', id, method: 'tools/call', params: { name, arguments: params } }) + '\n');
      });
    }

    p.stderr.on('data', (d) => { process.stderr.write('[jules-server] ' + d.toString()); });

    rl.on('line', (line) => {
      if (!line) return;
      let msg; try { msg = JSON.parse(line); } catch { return; }
      try {
        if (msg.id === 'init') {
          p.stdin.write(JSON.stringify({ jsonrpc: '2.0', method: 'notifications/initialized' }) + '\n');
          (async () => {
            const r = await callTool('create_session', { repo, branch, title, prompt, autoPr });
            done = true;
            let text = '';
            try { text = r.content.map(c => c.text).join('\n'); } catch { text = JSON.stringify(r); }
            console.log(`\n=== ${title} ===\n${text}\n`);
            p.kill();
            resolve(text);
          })();
        } else if (msg.id && callbacks.has(msg.id)) {
          const cb = callbacks.get(msg.id);
          callbacks.delete(msg.id);
          cb(msg.error ? { __error__: msg.error } : msg.result);
        }
      } catch (e) { console.error('handler', e); }
    });

    p.stdin.write(JSON.stringify({ jsonrpc: '2.0', id: 'init', method: 'initialize', params: { protocolVersion: '2024-11-05', capabilities: {}, clientInfo: { name: 'hermes-orch', version: '1.0.0' } } }) + '\n');
  });
}

async function main() {
  const args = process.argv.slice(2);
  let missions;

  if (args.includes('--all')) {
    missions = listMissions();
  } else if (args.includes('--test')) {
    const idx = args.indexOf('--test');
    const m = args[idx + 1];
    if (!m) { console.error('Usage: --test M04'); process.exit(1); }
    if (!fs.existsSync(path.join(DIR, m))) { console.error(`Fichier ${m} introuvable`); process.exit(1); }
    missions = [m];
  } else if (args.includes('--missions')) {
    const idx = args.indexOf('--missions');
    const raw = args[idx + 1];
    if (!raw) { console.error('Usage: --missions M01,M04,M07'); process.exit(1); }
    missions = raw.split(',').map(m => m.trim()).filter(m => fs.existsSync(path.join(DIR, m)));
  } else {
    console.log('Usage :');
    console.log('  --all              Lancer les 15 missions');
    console.log('  --test M04         Tester 1 mission');
    console.log('  --missions M01,M04 Lancer un sous-ensemble');
    process.exit(0);
  }

  console.log(`\n🚀 Lancement de ${missions.length} mission(s) Jules...\n`);

  let launched = 0, failed = 0;

  for (const mfile of missions) {
    const title = mfile.replace(/\.md$/, '').replace(/^M\d{2}_/, '');
    const prompt = buildPrompt(mfile);
    console.log(`📤 ${mfile} — ${title}`);

    try {
      const result = await createSession({
        title: `[Nuit 18/07] ${title}`,
        prompt,
        repo: 'criloOcom/accident-main',
        branch: 'main',
        autoPr: true,
      });

      // Try to extract session ID from result
      let sessionId = null;
      try {
        const parsed = JSON.parse(result);
        sessionId = parsed.sessionId || null;
      } catch {}

      if (sessionId) {
        updateMap(mfile, sessionId);
        console.log(`✅ ${mfile} → session ${sessionId}`);
        launched++;
      } else {
        // Still save the raw result for debugging
        console.log(`⚠️  ${mfile} → lancé, session ID non extrait`);
        launched++;
      }
    } catch (e) {
      console.error(`❌ ${mfile} — ${e.message || e}`);
      failed++;
    }
  }

  updateLog({ launched, completed: 0, failed });
  console.log(`\n📊 Résultat : ${launched} lancées, ${failed} échecs\n`);
  console.log('Sessions enregistrées dans SESSION_MAP.json');
  console.log('Pour clôturer : node close_sessions.mjs');
}

main().catch(console.error);
