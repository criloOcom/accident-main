#!/usr/bin/env node
/** Relance M03 (sécurisation probatoire) — session d'origine a dévié (notes à la racine, pas de rapport). */
import fs from 'fs';
import path from 'path';
import { spawn } from 'child_process';
import readline from 'readline';
const DIR = path.dirname(new URL(import.meta.url).pathname);
const WRAPPER = process.env.JULES_WRAPPER || '/home/crilocom/.opencode/mcp-wrappers/mcp-jules.sh';
const mapPath = path.join(DIR, 'SESSION_MAP.json');
const COMMUN = fs.readFileSync(path.join(DIR, 'PROMPT_COMMUN.md'), 'utf-8');
const map = JSON.parse(fs.readFileSync(mapPath, 'utf-8'));
const src = 'M03_securite_preuves.md';
const title = 'Nuit Jules 14/07 (RELANCE) — M03_securite_preuves';

function withSession(fn) {
  const p = spawn(WRAPPER, [], { shell: true });
  const rl = readline.createInterface({ input: p.stdout });
  const cbs = new Map(); const idRef = { n: 1 }; let resolved = false;
  return new Promise((resolve) => {
    p.stderr.on('data', () => {});
    rl.on('line', (line) => {
      if (!line) return; let msg; try { msg = JSON.parse(line); } catch { return; }
      try {
        if (msg.id === 'init') {
          p.stdin.write(JSON.stringify({ jsonrpc: '2.0', method: 'notifications/initialized' }) + '\n');
          (async () => { const res = await fn({ call: (n, a) => new Promise(r => { const i = 'c' + (idRef.n++); cbs.set(i, r); p.stdin.write(JSON.stringify({ jsonrpc: '2.0', id: i, method: 'tools/call', params: { name: n, arguments: a } }) + '\n'); }) }); if (!resolved) { resolved = true; p.kill(); resolve(res); } })();
        } else if (msg.id && cbs.has(msg.id)) { const c = cbs.get(msg.id); cbs.delete(msg.id); c(msg.error ? { __e: msg.error } : msg.result); }
      } catch {}
    });
    p.stdin.write(JSON.stringify({ jsonrpc: '2.0', id: 'init', method: 'initialize', params: { protocolVersion: '2024-11-05', capabilities: {}, clientInfo: { name: 'relaunchM03', version: '1' } } }) + '\n');
  });
}

async function main() {
  const spec = fs.readFileSync(path.join(DIR, src), 'utf-8');
  const out = await withSession(async ({ call }) => {
    const r = await call('create_session', { repo: 'criloOcom/accident-main', branch: 'main', autoPr: true, title, prompt: COMMUN + '\n' + spec });
    let txt = ''; try { txt = r.content.map(c => c.text).join('\n'); } catch { txt = JSON.stringify(r); }
    return txt;
  });
  const sm = out.match(/ID:\s*([0-9]+)/) || out.match(/([0-9]{10,})/);
  if (sm && !out.includes('Error')) {
    map['M03b_securite_preuves.md'] = { sessionId: sm[1], launchedAt: new Date().toISOString(), note: 'RELANCE (M03 d\'origine a dévié: notes à la racine, pas de rapport)' };
    fs.writeFileSync(mapPath, JSON.stringify(map, null, 2));
    console.log('M03b →', sm[1]);
  } else {
    console.log('M03b → ÉCHEC', out.slice(0, 150));
  }
}
main();
