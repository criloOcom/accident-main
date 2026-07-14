#!/usr/bin/env node
/**
 * Clôture propre des sessions Jules terminées (Règle #12 du projet).
 * Pour chaque session en statut 'stable' ou 'failed' dans SESSION_MAP.json,
 * envoie un message de clôture via send_reply_to_session (action: send).
 *
 * Usage : node close_sessions.mjs [--all]
 *   --all : clôture même si statut busy (à éviter sauf fin de nuit)
 */
import fs from 'fs';
import path from 'path';
import { spawn } from 'child_process';
import readline from 'readline';

const DIR = path.dirname(new URL(import.meta.url).pathname);
const WRAPPER = process.env.JULES_WRAPPER || '/home/crilocom/.opencode/mcp-wrappers/mcp-jules.sh';
const mapPath = path.join(DIR, 'SESSION_MAP.json');
const map = JSON.parse(fs.readFileSync(mapPath, 'utf-8'));
const all = process.argv.includes('--all');
const CLOSURE_MSG = "Mission terminée, tu peux clôturer et archiver cette session. Merci pour le rapport.";

function spawnServer() {
  const p = spawn(WRAPPER, [], { shell: true });
  const rl = readline.createInterface({ input: p.stdout });
  return { p, rl };
}

function withSession(fn) {
  const { p, rl } = spawnServer();
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
    p.stdin.write(JSON.stringify({ jsonrpc: '2.0', id: 'init', method: 'initialize', params: { protocolVersion: '2024-11-05', capabilities: {}, clientInfo: { name: 'close', version: '1' } } }) + '\n');
  });
}

async function getState(sid) {
  const out = await withSession(async ({ call }) => {
    const r = await call('get_session_state', { sessionId: sid });
    let txt = ''; try { txt = r.content.map(c => c.text).join('\n'); } catch { txt = JSON.stringify(r); }
    return txt;
  });
  if (!out) return 'NO_OUTPUT';
  try { const o = JSON.parse(out); return o.status; } catch { const sm = out.match(/status["']?\s*[:]\s*["']?(\w+)/); return sm ? sm[1] : '?'; }
}

async function sendClosure(sid) {
  const out = await withSession(async ({ call }) => {
    const r = await call('send_reply_to_session', { sessionId: sid, action: 'send', message: CLOSURE_MSG });
    let txt = ''; try { txt = r.content.map(c => c.text).join('\n'); } catch { txt = JSON.stringify(r); }
    return txt || 'OK';
  });
  return out;
}

async function main() {
  for (const [m, info] of Object.entries(map)) {
    if (!info.sessionId) { console.log(`${m}: non lancée, skip`); continue; }
    const st = await getState(info.sessionId);
    if (st === 'stable' || st === 'failed' || all) {
      console.log(`${m} (${st}) → clôture...`);
      const res = await sendClosure(info.sessionId);
      console.log(`   → ${String(res).slice(0, 100)}`);
    } else {
      console.log(`${m}: ${st} (encore en cours, pas de clôture)`);
    }
  }
}
main();
