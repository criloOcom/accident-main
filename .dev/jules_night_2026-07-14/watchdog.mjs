#!/usr/bin/env node
/**
 * Watchdog de nuit Jules — accident-main.
 * - Monitor l'état des sessions du SESSION_MAP.json
 * - Relance M15_synthese_operationnalite dès qu'une place est libre
 * - Loggue l'état dans STATE_LOG.json
 * - À la fin, tente une clôture polie de chaque session terminée
 *
 * Usage : node watchdog.mjs
 */
import fs from 'fs';
import path from 'path';
import { spawn } from 'child_process';
import readline from 'readline';

const DIR = path.dirname(new URL(import.meta.url).pathname);
const WRAPPER = process.env.JULES_WRAPPER || '/home/crilocom/.opencode/mcp-wrappers/mcp-jules.sh';
const mapPath = path.join(DIR, 'SESSION_MAP.json');
const logPath = path.join(DIR, 'STATE_LOG.json');
const COMMUN = fs.readFileSync(path.join(DIR, 'PROMPT_COMMUN.md'), 'utf-8');
const M15 = fs.readFileSync(path.join(DIR, 'M15_synthese_operationnalite.md'), 'utf-8');

let map = JSON.parse(fs.readFileSync(mapPath, 'utf-8'));
let log = fs.existsSync(logPath) ? JSON.parse(fs.readFileSync(logPath, 'utf-8')) : [];

function spawnServer() {
  const p = spawn(WRAPPER, [], { shell: true });
  const rl = readline.createInterface({ input: p.stdout });
  return { p, rl };
}

function mcpCall(p, rl, cbs, idRef, name, args) {
  return new Promise((resolve) => {
    const id = 'c' + (idRef.n++);
    cbs.set(id, resolve);
    p.stdin.write(JSON.stringify({ jsonrpc: '2.0', id, method: 'tools/call', params: { name, arguments: args } }) + '\n');
  });
}

async function withSession(fn) {
  const { p, rl } = spawnServer();
  const cbs = new Map();
  const idRef = { n: 1 };
  let resolved = false;
  const promise = new Promise((resolve) => {
    p.stderr.on('data', () => {});
    rl.on('line', (line) => {
      if (!line) return; let msg; try { msg = JSON.parse(line); } catch { return; }
      try {
        if (msg.id === 'init') {
          p.stdin.write(JSON.stringify({ jsonrpc: '2.0', method: 'notifications/initialized' }) + '\n');
          (async () => { const res = await fn({ call: (n, a) => mcpCall(p, rl, cbs, idRef, n, a) }); if (!resolved) { resolved = true; p.kill(); resolve(res); } })();
        } else if (msg.id && cbs.has(msg.id)) {
          const c = cbs.get(msg.id); cbs.delete(msg.id); c(msg.error ? { __e: msg.error } : msg.result);
        }
      } catch {}
    });
    p.stdin.write(JSON.stringify({ jsonrpc: '2.0', id: 'init', method: 'initialize', params: { protocolVersion: '2024-11-05', capabilities: {}, clientInfo: { name: 'watch', version: '1' } } }) + '\n');
  });
  return promise;
}

function parseState(out) {
  if (!out) return { status: 'NO_OUTPUT' };
  if (out.__e) return { status: 'ERROR', err: JSON.stringify(out.__e).slice(0, 120) };
  try { const o = JSON.parse(out); return { status: o.status, url: o.url, title: o.title, lastAgent: o.lastAgentMessage?.content || '' }; }
  catch { const sm = out.match(/status["']?\s*[:]\s*["']?(\w+)/); return { status: sm ? sm[1] : '?' }; }
}

async function main() {
  const now = new Date().toISOString();
  const states = {};

  // 1. État de toutes les sessions existantes
  for (const [m, info] of Object.entries(map)) {
    if (!info.sessionId) { states[m] = { status: 'NOT_LAUNCHED' }; continue; }
    const out = await withSession(async ({ call }) => {
      const r = await call('get_session_state', { sessionId: info.sessionId });
      let txt = ''; try { txt = r.content.map(c => c.text).join('\n'); } catch { txt = JSON.stringify(r); }
      return txt;
    });
    states[m] = parseState(out);
  }

  // 2. Si M15 non lancée, tenter de la créer
  if (!map['M15_synthese_operationnalite.md']?.sessionId) {
    const active = Object.values(states).filter(s => s.status === 'busy' || s.status === 'stable').length;
    if (active < 14) {
      const raw = await withSession(async ({ call }) => {
        const r = await call('create_session', {
          repo: 'criloOcom/accident-main', branch: 'main', autoPr: true,
          title: 'Nuit Jules 14/07 — M15_synthese_operationnalite',
          prompt: COMMUN + '\n' + M15,
        });
        let txt = ''; try { txt = r.content.map(c => c.text).join('\n'); } catch { txt = JSON.stringify(r); }
        return txt;
      });
      const out = raw || '';
      const sm = out.match(/ID:\s*([0-9]+)/) || out.match(/([0-9]{10,})/);
      if (sm && !out.includes('Error')) {
        map['M15_synthese_operationnalite.md'] = { sessionId: sm[1], launchedAt: now };
        states['M15_synthese_operationnalite.md'] = { status: 'busy (just launched)' };
        console.log('M15 LANCÉE:', sm[1]);
      } else {
        states['M15_synthese_operationnalite.md'] = { status: 'FAILED_PRECONDITION (retry later)', raw: out.slice(0, 120) };
        console.log('M15 refusée, retry plus tard.');
      }
      fs.writeFileSync(mapPath, JSON.stringify(map, null, 2));
    } else {
      states['M15_synthese_operationnalite.md'] = { status: 'WAITING (14 sessions actives)' };
    }
  }

  // 3. Log
  log.push({ ts: now, states });
  fs.writeFileSync(logPath, JSON.stringify(log, null, 2));

  // 4. Résumé
  console.log('=== ÉTAT', now, '===');
  for (const [m, s] of Object.entries(states)) console.log(m.padEnd(32), '|', s.status);
}

main();
