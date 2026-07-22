#!/usr/bin/env node
/** Relance les missions M05 et M07 (clôturées trop tôt sans rapport). Stocke sous M05b/M07b. */
import fs from 'fs';
import path from 'path';
import { spawn } from 'child_process';
import readline from 'readline';
const DIR = path.dirname(new URL(import.meta.url).pathname);
const WRAPPER = process.env.JULES_WRAPPER || '/home/crilocom/.opencode/mcp-wrappers/mcp-jules.sh';
const mapPath = path.join(DIR, 'SESSION_MAP.json');
const COMMUN = fs.readFileSync(path.join(DIR, 'PROMPT_COMMUN.md'), 'utf-8');
const map = JSON.parse(fs.readFileSync(mapPath, 'utf-8'));

const targets = [
  { key: 'M05b_qualite_actes.md', src: 'M05_qualite_actes.md', title: 'Nuit Jules 14/07 (RELANCE) — M05_qualite_actes' },
  { key: 'M07b_dirigeants_societes.md', src: 'M07_dirigeants_societes.md', title: 'Nuit Jules 14/07 (RELANCE) — M07_dirigeants_societes' },
];

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
    p.stdin.write(JSON.stringify({ jsonrpc: '2.0', id: 'init', method: 'initialize', params: { protocolVersion: '2024-11-05', capabilities: {}, clientInfo: { name: 'relaunch', version: '1' } } }) + '\n');
  });
}

async function main() {
  const now = new Date().toISOString();
  for (const t of targets) {
    const spec = fs.readFileSync(path.join(DIR, t.src), 'utf-8');
    const out = await withSession(async ({ call }) => {
      const r = await call('create_session', { repo: 'criloOcom/accident-main', branch: 'main', autoPr: true, title: t.title, prompt: COMMUN + '\n' + spec });
      let txt = ''; try { txt = r.content.map(c => c.text).join('\n'); } catch { txt = JSON.stringify(r); }
      return txt;
    });
    const sm = out.match(/ID:\s*([0-9]+)/) || out.match(/([0-9]{10,})/);
    if (sm && !out.includes('Error')) {
      map[t.key] = { sessionId: sm[1], launchedAt: now, note: 'RELANCE (M05/M07 clôturées trop tôt sans rapport)' };
      console.log(t.key, '→', sm[1]);
    } else {
      console.log(t.key, '→ ÉCHEC', out.slice(0, 150));
    }
  }
  fs.writeFileSync(mapPath, JSON.stringify(map, null, 2));
  console.log('Mapping mis à jour.');
}
main();
