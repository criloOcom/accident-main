#!/usr/bin/env node
/** Récupère M03b : si PR présente et contient un rapport 📊 Rapports/, merge + clôture + sync + push. */
import { spawn } from 'child_process';
import readline from 'readline';
import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';

const DIR = path.dirname(new URL(import.meta.url).pathname);
const WRAPPER = process.env.JULES_WRAPPER || '/home/crilocom/.opencode/mcp-wrappers/mcp-jules.sh';
const map = JSON.parse(fs.readFileSync(path.join(DIR, 'SESSION_MAP.json'), 'utf-8'));
const SID = map['M03b_securite_preuves.md']?.sessionId;
const GH = process.env.GH_TOKEN || (() => { try { return execSync(`python3 -c "import sys; sys.path.insert(0,'$HOME/.opencode'); from souverain import get_secret; print(get_secret('GITHUB_TOKEN'))"`, { encoding: 'utf-8' }).trim(); } catch { return ''; } })();
process.env.GH_TOKEN = GH;

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
    p.stdin.write(JSON.stringify({ jsonrpc: '2.0', id: 'init', method: 'initialize', params: { protocolVersion: '2024-11-05', capabilities: {}, clientInfo: { name: 'm03b', version: '1' } } }) + '\n');
  });
}

function sh(cmd) { try { return execSync(cmd, { encoding: 'utf-8', stdio: ['pipe', 'pipe', 'pipe'] }); } catch (e) { return e.stdout || e.stderr || ''; } }

async function main() {
  if (!SID) { console.log('M03b introuvable dans le mapping.'); return; }
  const out = await withSession(async ({ call }) => {
    const r = await call('get_session_state', { sessionId: SID });
    let txt = ''; try { txt = r.content.map(c => c.text).join('\n'); } catch { txt = JSON.stringify(r); }
    return txt;
  });
  let st = '?', pr = null;
  try { const o = JSON.parse(out); st = o.status; pr = o.pr; } catch {}
  console.log('M03b status:', st, '| PR:', pr ? pr.url : 'aucune');
  if (st === 'stable' && pr) {
    const num = (pr.url.match(/pull\/(\d+)/) || [])[1];
    if (!num) { console.log('Numéro PR introuvable.'); return; }
    // Vérifie que la PR contient un rapport dans 📊 Rapports/
    const files = sh(`gh pr view ${num} --repo criloOcom/accident-main --json files`).trim();
    let hasReport = false;
    try { hasReport = JSON.parse(files).files.some(f => f.path.startsWith('📊 Rapports/') && f.path.endsWith('.md')); } catch {}
    if (!hasReport) { console.log('PR #' + num + ' ne contient PAS de rapport 📊 Rapports/ — déviation, on n merge pas. À investiguer.'); return; }
    console.log('Merge PR #' + num + ' (rapport détecté)...');
    sh(`gh pr merge ${num} --repo criloOcom/accident-main --rebase --delete-branch`);
    sh('git pull origin main --quiet');
    // Sync README
    sh('python3 .dev/app/sync_readme_listings.py --apply');
    sh('git add -A && git commit -q -m "chore: merge rapport M03b sécurisation preuves + sync README" && git push origin main');
    console.log('M03b mergée et poussée.');
    // Clôture session
    await withSession(async ({ call }) => { await call('send_reply_to_session', { sessionId: SID, action: 'send', message: 'Mission terminée, tu peux clôturer et archiver cette session. Merci.' }); });
    console.log('Session M03b clôturée.');
  } else {
    console.log('M03b pas encore prête (status=' + st + '). On réessaiera au prochain passage.');
  }
}
main();
