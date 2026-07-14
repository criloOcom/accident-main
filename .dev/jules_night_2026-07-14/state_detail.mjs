#!/usr/bin/env node
/** Affiche l'état détaillé (status, lastAgentMessage, pendingPlan, pr) de sessions données. */
import { spawn } from 'child_process';
import readline from 'readline';
const WRAPPER = process.env.JULES_WRAPPER || '/home/crilocom/.opencode/mcp-wrappers/mcp-jules.sh';
const sids = process.argv.slice(2);
if (!sids.length) { console.error('usage: node state_detail.mjs SID1 SID2 ...'); process.exit(1); }

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
    p.stdin.write(JSON.stringify({ jsonrpc: '2.0', id: 'init', method: 'initialize', params: { protocolVersion: '2024-11-05', capabilities: {}, clientInfo: { name: 'sd', version: '1' } } }) + '\n');
  });
}

function extract(out) {
  if (!out) return {};
  try { const o = JSON.parse(out); return o; } catch { return {}; }
}

async function main() {
  for (const sid of sids) {
    const out = await withSession(async ({ call }) => {
      const r = await call('get_session_state', { sessionId: sid });
      let txt = ''; try { txt = r.content.map(c => c.text).join('\n'); } catch { txt = JSON.stringify(r); }
      return txt;
    });
    const o = extract(out);
    console.log('\n========== SESSION', sid, '==========');
    console.log('status:', o.status);
    console.log('title :', o.title);
    console.log('url   :', o.url);
    if (o.pr) console.log('PR    :', JSON.stringify(o.pr));
    if (o.lastAgentMessage) console.log('agent :', String(o.lastAgentMessage.content || o.lastAgentMessage).slice(0, 600));
    if (o.pendingPlan) console.log('plan  :', JSON.stringify(o.pendingPlan).slice(0, 400));
  }
}
main();
