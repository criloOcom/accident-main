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

  p.stderr.on('data', (d) => { process.stderr.write('[jules] ' + d.toString()); });

  rl.on('line', (line) => {
    if (!line) return;
    let msg; try { msg = JSON.parse(line); } catch { return; }
    try {
      if (msg.id && cbs.has(msg.id)) {
        const cb = cbs.get(msg.id); cbs.delete(msg.id);
        cb(msg.error ? { __error__: msg.error } : msg.result);
      } else if (msg.id === 'init') {
        p.stdin.write(JSON.stringify({ jsonrpc: '2.0', method: 'notifications/initialized' }) + '\n');
        fn(p, cbs, idRef).then((r) => { if (!resolved) { resolved = true; p.kill(); process.exit(0); } })
          .catch((e) => { if (!resolved) { resolved = true; console.error('err', e); p.kill(); process.exit(1); } });
      }
    } catch (e) { console.error('handler', e); }
  });

  function callTool(name, args) { return new Promise((res) => { const id = 'c' + (idRef.n++); cbs.set(id, res); p.stdin.write(JSON.stringify({ jsonrpc: '2.0', id, method: 'tools/call', params: { name, arguments: args } }) + '\n'); }); }

  p.stdin.write(JSON.stringify({ jsonrpc: '2.0', id: 'init', method: 'initialize', params: { protocolVersion: '2024-11-05', capabilities: {}, clientInfo: { name: 'close-sessions', version: '1.0' } } }) + '\n');
}

async function main() {
  const missions = map.missions || {};
  const entries = Object.entries(missions);

  for (const [mission, data] of entries) {
    if (!data.sessionId) continue;
    if (data.status === 'pending' && !all) { console.log(`⏭️  ${mission} — pending, skip`); continue; }

    console.log(`🔌 Closing ${mission} (${data.sessionId})...`);
    try {
      await withSession(async (p, cbs, idRef) => {
        function callTool(name, args) { return new Promise((res) => { const id = 'c' + (idRef.n++); cbs.set(id, res); p.stdin.write(JSON.stringify({ jsonrpc: '2.0', id, method: 'tools/call', params: { name, arguments: args } }) + '\n'); }); }
        const r = await callTool('send_reply_to_session', { sessionId: data.sessionId, action: 'send', message: CLOSURE_MSG });
        console.log(`✅ ${mission} closed`);
      });
    } catch (e) {
      console.error(`❌ ${mission} — ${e.message || e}`);
    }
  }

  console.log('All closures attempted.');
}

main().catch(console.error);
