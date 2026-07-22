#!/usr/bin/env node
/**
 * Client MCP Jules (transport JSON sur lignes, éprouvé sur www-v3).
 * Permet depuis Hermes de : discover, list, create, state, reply.
 *
 * Usage :
 *   node jules_client.mjs discover
 *   node jules_client.mjs list [--limit N]
 *   node jules_client.mjs create --title T --prompt-file P --branch B [--repo R] [--auto-pr true|false]
 *   node jules_client.mjs state --session S
 *   node jules_client.mjs reply --session S --message M
 */
import { spawn } from 'child_process';
import readline from 'readline';
import fs from 'fs';

const WRAPPER = process.env.JULES_WRAPPER || '/home/crilocom/.opencode/mcp-wrappers/mcp-jules.sh';
const args = process.argv.slice(2);
const command = args[0];

function parseFlags(argv) {
  const flags = {};
  for (let i = 1; i < argv.length; i++) {
    if (argv[i].startsWith('--')) {
      const key = argv[i].slice(2);
      const next = argv[i + 1];
      if (next && !next.startsWith('--')) { flags[key] = next; i++; }
      else flags[key] = true;
    }
  }
  return flags;
}
const flags = parseFlags(args);

function spawnServer() {
  const p = spawn(WRAPPER, [], { shell: true });
  const rl = readline.createInterface({ input: p.stdout });
  return { p, rl };
}

function run(operations) {
  return new Promise((resolve, reject) => {
    const { p, rl } = spawnServer();
    let initialized = false;
    const callbacks = new Map();
    let callId = 1;

    function callTool(name, params) {
      return new Promise((res) => {
        const id = 'call-' + (callId++);
        callbacks.set(id, res);
        p.stdin.write(JSON.stringify({ jsonrpc: '2.0', id, method: 'tools/call', params: { name, arguments: params } }) + '\n');
      });
    }
    function listTools() {
      return new Promise((res) => {
        const id = 'lt-' + (callId++);
        callbacks.set(id, res);
        p.stdin.write(JSON.stringify({ jsonrpc: '2.0', id, method: 'tools/list', params: {} }) + '\n');
      });
    }

    p.stderr.on('data', (d) => { process.stderr.write('[jules-server] ' + d.toString()); });

    rl.on('line', (line) => {
      if (!line) return;
      let msg;
      try { msg = JSON.parse(line); } catch { return; }
      try {
        if (msg.id === 'init') {
          p.stdin.write(JSON.stringify({ jsonrpc: '2.0', method: 'notifications/initialized' }) + '\n');
          initialized = true;
          operations({ callTool, listTools, p }).then(() => { p.kill(); resolve(); }).catch((e) => { console.error(e); p.kill(); resolve(); });
        } else if (msg.id && callbacks.has(msg.id)) {
          const cb = callbacks.get(msg.id);
          callbacks.delete(msg.id);
          if (msg.error) cb({ __error__: msg.error });
          else cb(msg.result);
        }
      } catch (e) { console.error('line handler error', e); }
    });

    p.stdin.write(JSON.stringify({ jsonrpc: '2.0', id: 'init', method: 'initialize', params: { protocolVersion: '2024-11-05', capabilities: {}, clientInfo: { name: 'hermes', version: '1.0.0' } } }) + '\n');
  });
}

function extractText(result) {
  if (!result) return result;
  if (Array.isArray(result.content)) {
    return result.content.map(c => c.text ?? c).join('\n');
  }
  return result;
}

async function main() {
  if (command === 'discover') {
    await run(async ({ listTools }) => {
      const r = await listTools();
      console.log(JSON.stringify(extractText(r) || r, null, 2));
    });
    return;
  }
  if (command === 'list') {
    await run(async ({ callTool }) => {
      const limit = parseInt(flags.limit || '50', 10);
      const r = await callTool('list_sessions', { pageSize: limit });
      const txt = extractText(r);
      try { console.log(JSON.stringify(JSON.parse(txt), null, 2)); }
      catch { console.log(txt); }
    });
    return;
  }
  if (command === 'create') {
    const title = flags.title || 'Mission Jules';
    const repo = flags.repo || 'criloOcom/accident-main';
    const branch = flags.branch || 'main';
    const autoPr = flags['auto-pr'] !== 'false';
    let prompt = flags.prompt || '';
    if (flags['prompt-file']) prompt = fs.readFileSync(flags['prompt-file'], 'utf-8');
    await run(async ({ callTool }) => {
      const r = await callTool('create_session', {
        repo, branch, title, prompt,
        autoPr,
      });
      const txt = extractText(r);
      try { console.log(JSON.stringify(JSON.parse(txt), null, 2)); }
      catch { console.log(txt); }
    });
    return;
  }
  if (command === 'state') {
    const sid = flags.session;
    await run(async ({ callTool }) => {
      const r = await callTool('get_session_state', { sessionId: sid });
      const txt = extractText(r);
      try { console.log(JSON.stringify(JSON.parse(txt), null, 2)); }
      catch { console.log(txt); }
    });
    return;
  }
  if (command === 'reply') {
    const sid = flags.session;
    let message = flags.message || '';
    if (flags['message-file']) message = fs.readFileSync(flags['message-file'], 'utf-8');
    await run(async ({ callTool }) => {
      const r = await callTool('send_reply_to_session', { sessionId: sid, action: 'send', message });
      const txt = extractText(r);
      try { console.log(JSON.stringify(JSON.parse(txt), null, 2)); }
      catch { console.log(txt); }
    });
    return;
  }
  console.error('Commande inconnue:', command);
  process.exit(1);
}

main();
