#!/usr/bin/env node
/** Monitor l'état des sessions Jules listées dans SESSION_MAP.json. */
import fs from 'fs';
import path from 'path';
import { spawn } from 'child_process';
import readline from 'readline';

const DIR = path.dirname(new URL(import.meta.url).pathname);
const WRAPPER = process.env.JULES_WRAPPER || '/home/crilocom/.opencode/mcp-wrappers/mcp-jules.sh';
const mapPath = path.join(DIR, 'SESSION_MAP.json');
const map = JSON.parse(fs.readFileSync(mapPath, 'utf-8'));

function spawnServer() {
  const p = spawn(WRAPPER, [], { shell: true });
  const rl = readline.createInterface({ input: p.stdout });
  return { p, rl };
}

function getState(sid) {
  return new Promise((resolve) => {
    const { p, rl } = spawnServer();
    let done = false;
    const cb = new Map();
    let id = 1;
    function call(name, args) {
      return new Promise(r => { const i = 'c' + (id++); cb.set(i, r); p.stdin.write(JSON.stringify({ jsonrpc: '2.0', id: i, method: 'tools/call', params: { name, arguments: args } }) + '\n'); });
    }
    p.stderr.on('data', () => {});
    rl.on('line', (line) => {
      if (!line) return; let msg; try { msg = JSON.parse(line); } catch { return; }
      try {
        if (msg.id === 'init') {
          p.stdin.write(JSON.stringify({ jsonrpc: '2.0', method: 'notifications/initialized' }) + '\n');
          (async () => {
            const r = await call('get_session_state', { sessionId: sid });
            let txt = ''; try { txt = r.content.map(c => c.text).join('\n'); } catch { txt = JSON.stringify(r); }
            p.kill(); resolve(txt);
          })();
        } else if (msg.id && cb.has(msg.id)) {
          const c = cb.get(msg.id); cb.delete(msg.id); c(msg.error ? { __e: msg.error } : msg.result);
        }
      } catch {}
    });
    p.stdin.write(JSON.stringify({ jsonrpc: '2.0', id: 'init', method: 'initialize', params: { protocolVersion: '2024-11-05', capabilities: {}, clientInfo: { name: 'mon', version: '1' } } }) + '\n');
  });
}

async function main() {
  for (const [m, info] of Object.entries(map)) {
    if (!info.sessionId) { console.log(`${m}: NON LANCÉE`); continue; }
    const out = await getState(info.sessionId);
    // Extraire status + url
    let status = '?', url = '', title = '';
    try {
      const o = JSON.parse(out);
      status = o.status || '?';
      url = o.url || ''; title = o.title || '';
    } catch {
      const sm = out.match(/status["']?\s*[:]\s*["']?(\w+)/);
      if (sm) status = sm[1];
    }
    console.log(`${m.padEnd(32)} | ${status.padEnd(10)} | ${url}`);
  }
}
main();
