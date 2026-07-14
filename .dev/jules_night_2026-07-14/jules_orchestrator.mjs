#!/usr/bin/env node
/**
 * Orchestrateur de nuit Jules — accident-main.
 * Concatène PROMPT_COMMUN.md + Mxx_*.md, puis crée une session Jules
 * (repo criloOcom/accident-main, branch main, autoPr) par mission.
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

function extractSessionId(text) {
  // Cherche un ID numérique ou une URL jules.google.com
  const m = text.match(/jules\.google\.com\/session\/([0-9]+)/) || text.match(/session[_\s-]?id["'\s:]+([0-9]+)/i) || text.match(/([0-9]{10,})/);
  return m ? m[1] : null;
}

async function main() {
  const args = process.argv.slice(2);
  let missions = [];
  if (args.includes('--all')) missions = listMissions();
  else if (args.includes('--test')) {
    const m = args[args.indexOf('--test') + 1];
    missions = [m.endsWith('.md') ? m : m + '.md'];
    if (!fs.existsSync(path.join(DIR, missions[0]))) missions = listMissions().filter(f => f.startsWith(m));
  } else if (args.includes('--missions')) {
    const list = args[args.indexOf('--missions') + 1].split(',');
    missions = listMissions().filter(f => list.some(x => f.startsWith(x)));
  } else {
    console.error('Usage: --all | --test Mxx | --missions M01,M04');
    process.exit(1);
  }

  const repo = 'criloOcom/accident-main';
  const branch = 'main';
  const autoPr = true;

  const results = [];
  for (const m of missions) {
    const title = 'Nuit Jules 14/07 — ' + m.replace('.md', '');
    const prompt = buildPrompt(m);
    console.log(`\n>>> Lancement ${title} (prompt ${prompt.length} chars) ...`);
    const out = await createSession({ title, prompt, repo, branch, autoPr });
    const sid = extractSessionId(out);
    results.push({ mission: m, sessionId: sid, raw: out });
    // Pause courte pour ne pas surcharger l'API
    await new Promise(r => setTimeout(r, 3000));
  }

  // Sauvegarde du mapping
  const mapPath = path.join(DIR, 'SESSION_MAP.json');
  const prev = fs.existsSync(mapPath) ? JSON.parse(fs.readFileSync(mapPath, 'utf-8')) : {};
  const merged = { ...prev };
  for (const r of results) merged[r.mission] = { sessionId: r.sessionId, launchedAt: new Date().toISOString() };
  fs.writeFileSync(mapPath, JSON.stringify(merged, null, 2));
  console.log('\n=== MAPPING SAUVEGARDÉ ===');
  console.log(JSON.stringify(merged, null, 2));
}

main();
