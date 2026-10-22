// MCP server for maciejzieciak.com (Cloudflare Pages Function at /mcp).
// Streamable HTTP transport, stateless: every POST carries one JSON-RPC message (or a batch)
// and gets a JSON reply. Tools reuse the same code as the site's free tools, and the content
// comes from /mcp-data.json, generated at build time from the published pages.
import { parseRobots, check } from '../src/lib/robots';
import { generateRobots } from '../src/lib/robots-gen';
import { parseInput, checkHreflang } from '../src/lib/hreflang';
import { bots } from '../src/data/ai-bots';

type Lang = 'pl' | 'en';
type Rpc = { jsonrpc: '2.0'; id?: string | number | null; method: string; params?: any };
type Data = {
  site: { name: string; url: string; email: string; linkedin: string | null; booking: string | null };
  contact: Record<Lang, string>;
  about: Record<Lang, string>;
  tools: Record<Lang, { robots: string; generator: string; hreflang: string }>;
  services: ({ key: string } & Record<Lang, { name: string; description: string; url: string }>)[];
  guides: ({ key: string; service: string; updated: string } & Record<Lang, { title: string; slug: string; url: string; description: string; text: string }>)[];
};

const VERSIONS = ['2025-06-18', '2025-03-26', '2024-11-05'];
const MAX_INPUT = 200_000; // characters per text argument
const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Accept, Mcp-Session-Id, Mcp-Protocol-Version',
  'Access-Control-Expose-Headers': 'Mcp-Session-Id',
};

let cache: Data | null = null;
async function load(request: Request, env: any): Promise<Data> {
  if (cache) return cache;
  const url = new URL('/mcp-data.json', request.url);
  const res = env?.ASSETS ? await env.ASSETS.fetch(url) : await fetch(url);
  cache = (await res.json()) as Data;
  return cache;
}

const lang = (v: unknown): Lang => (v === 'en' ? 'en' : 'pl');
const text = (t: string, structured?: unknown) => ({ content: [{ type: 'text', text: t }], ...(structured ? { structuredContent: structured } : {}) });
const fail = (t: string) => ({ content: [{ type: 'text', text: t }], isError: true });
const str = (v: unknown, name: string) => {
  if (typeof v !== 'string') throw new Error(`"${name}" must be a string`);
  if (v.length > MAX_INPUT) throw new Error(`"${name}" is too long`);
  return v;
};

const LANG_PROP = { type: 'string', enum: ['pl', 'en'], description: 'Language of the answer: pl (Polish, default) or en (English).' };
const tools = [
  {
    name: 'check_robots_txt',
    title: 'Check robots.txt for AI bots',
    description: 'Checks a robots.txt file and reports which search engines, AI search bots, AI training bots and user-initiated fetchers may access a path (RFC 9309 matching). Use when someone asks whether GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot, Google-Extended or Googlebot can crawl their site.',
    inputSchema: {
      type: 'object',
      properties: {
        robots_txt: { type: 'string', description: 'Full contents of the robots.txt file.' },
        path: { type: 'string', description: 'Path to check, e.g. / or /products/. Default: /.' },
      },
      required: ['robots_txt'],
    },
    annotations: { readOnlyHint: true, openWorldHint: false },
  },
  {
    name: 'generate_robots_txt',
    title: 'Generate robots.txt for AI bots',
    description: 'Generates a robots.txt that allows or blocks specific AI and search bots, with paths closed to everyone repeated in each group. Presets: search_only (allow search and AI search, block training), allow_all, block_ai (only classic search engines).',
    inputSchema: {
      type: 'object',
      properties: {
        preset: { type: 'string', enum: ['search_only', 'allow_all', 'block_ai'], description: 'Starting policy. Default: search_only.' },
        allow: { type: 'array', items: { type: 'string' }, description: 'Extra bot tokens to allow, e.g. ["GPTBot"].' },
        block: { type: 'array', items: { type: 'string' }, description: 'Extra bot tokens to block, e.g. ["CCBot"].' },
        disallow_paths: { type: 'array', items: { type: 'string' }, description: 'Paths closed to every bot, e.g. ["/cart/"].' },
        sitemap: { type: 'string', description: 'Absolute sitemap URL.' },
      },
    },
    annotations: { readOnlyHint: true, openWorldHint: false },
  },
  {
    name: 'check_hreflang',
    title: 'Check hreflang',
    description: 'Validates hreflang annotations pasted as <link rel="alternate" hreflang> tags from one page or as an XML sitemap with xhtml:link entries: language and country codes (e.g. en-UK, en_GB), absolute URLs, duplicates, self-reference, x-default and return links.',
    inputSchema: {
      type: 'object',
      properties: {
        input: { type: 'string', description: 'Link tags or XML sitemap content.' },
        page_url: { type: 'string', description: 'URL of the page the tags come from (optional, for the self-reference check).' },
      },
      required: ['input'],
    },
    annotations: { readOnlyHint: true, openWorldHint: false },
  },
  {
    name: 'search_guides',
    title: 'Search SEO guides',
    description: 'Searches Maciej Zięciak’s technical SEO and AI search guides (AI bots in robots.txt, AI Overviews, ChatGPT apps and MCP, SEO audits and their cost, migrations, pre-release checks, hreflang, faceted navigation). Returns titles, short descriptions and URLs.',
    inputSchema: { type: 'object', properties: { query: { type: 'string', description: 'Topic or keywords. Empty returns all guides.' }, lang: LANG_PROP } },
    annotations: { readOnlyHint: true, openWorldHint: false },
  },
  {
    name: 'get_guide',
    title: 'Read a guide',
    description: 'Returns the full text of one guide, identified by the slug or URL returned by search_guides.',
    inputSchema: { type: 'object', properties: { slug: { type: 'string', description: 'Guide slug, key or URL.' }, lang: LANG_PROP }, required: ['slug'] },
    annotations: { readOnlyHint: true, openWorldHint: false },
  },
  {
    name: 'list_services',
    title: 'List consulting services',
    description: 'Lists the technical SEO and AI search consulting services Maciej Zięciak offers, with descriptions and page URLs.',
    inputSchema: { type: 'object', properties: { lang: LANG_PROP } },
    annotations: { readOnlyHint: true, openWorldHint: false },
  },
  {
    name: 'contact_info',
    title: 'How to get in touch',
    description: 'Returns how to contact Maciej Zięciak or book a free 30-minute consultation.',
    inputSchema: { type: 'object', properties: { lang: LANG_PROP } },
    annotations: { readOnlyHint: true, openWorldHint: false },
  },
];

const PRESETS: Record<string, (g: string) => boolean> = {
  search_only: (g) => g !== 'training',
  allow_all: () => true,
  block_ai: (g) => g === 'search',
};

async function callTool(name: string, args: any, data: () => Promise<Data>) {
  args = args ?? {};
  switch (name) {
    case 'check_robots_txt': {
      const groups = parseRobots(str(args.robots_txt, 'robots_txt'));
      let path = typeof args.path === 'string' && args.path.trim() ? args.path.trim() : '/';
      if (!path.startsWith('/')) path = '/' + path;
      const results = bots.map((b) => {
        const v = check(groups, b.token, path);
        return { bot: b.token, company: b.company, group: b.group, allowed: v.allowed, rule: v.rule ? `${v.rule.allow ? 'Allow' : 'Disallow'}: ${v.rule.path}` : null, from_group: v.group };
      });
      const blocked = results.filter((r) => !r.allowed);
      const lines = results.map((r) => `- ${r.bot} (${r.company}, ${r.group}): ${r.allowed ? 'allowed' : 'BLOCKED'}${r.rule ? ` by "${r.rule}" in group ${r.from_group}` : ''}`);
      return text(`Path ${path}: ${blocked.length} of ${results.length} bots blocked.\n${lines.join('\n')}\n\nNote: user-initiated fetchers (ChatGPT-User, Claude-User, Perplexity-User) may not follow robots.txt. A firewall or CDN can still block bots that robots.txt allows.`, { path, blocked: blocked.length, total: results.length, results });
    }
    case 'generate_robots_txt': {
      const rule = PRESETS[args.preset] ?? PRESETS.search_only;
      const allow = new Set(bots.filter((b) => rule(b.group)).map((b) => b.token));
      const extra = (v: unknown) => (Array.isArray(v) ? v.filter((x) => typeof x === 'string' && /^[\w.-]{1,60}$/.test(x)) : []);
      extra(args.allow).forEach((t: string) => allow.add(t));
      const block = new Set(bots.map((b) => b.token).filter((t) => !allow.has(t)));
      extra(args.block).forEach((t: string) => (allow.delete(t), block.add(t)));
      const out = generateRobots({
        allow: [...allow],
        block: [...block],
        disallow: Array.isArray(args.disallow_paths) ? args.disallow_paths.filter((x: unknown) => typeof x === 'string' && x.length < 300 && !/[\r\n]/.test(x)).slice(0, 50) : [],
        sitemap: typeof args.sitemap === 'string' ? args.sitemap.replace(/[\r\n].*$/s, '').slice(0, 500) : '',
      });
      return text(out, { robots_txt: out });
    }
    case 'check_hreflang': {
      const parsed = parseInput(str(args.input, 'input'), typeof args.page_url === 'string' ? args.page_url : '');
      const issues = checkHreflang(parsed.pages);
      const lines = issues.map((i) => `- [${i.level}] ${i.code}${i.detail ? `: ${i.detail}` : ''}${i.page ? ` (page ${i.page})` : ''}`);
      return text(`Mode: ${parsed.mode}, pages: ${parsed.pages.length}, issues: ${issues.length}.\n${lines.join('\n') || 'No problems found.'}`, { mode: parsed.mode, pages: parsed.pages.length, issues });
    }
    case 'search_guides': {
      const d = await data();
      const l = lang(args.lang);
      const words = (typeof args.query === 'string' ? args.query : '').toLowerCase().split(/\s+/).filter((w) => w.length > 2);
      const scored = d.guides
        .map((g) => {
          const hay = `${g[l].title} ${g[l].description} ${g[l].text}`.toLowerCase();
          return { g, score: words.length ? words.reduce((s, w) => s + (hay.includes(w) ? 1 : 0), 0) : 1 };
        })
        .filter((x) => x.score > 0)
        .sort((a, b) => b.score - a.score);
      const list = scored.map(({ g }) => ({ slug: g[l].slug, title: g[l].title, description: g[l].description, url: g[l].url }));
      return text(list.length ? list.map((x) => `- ${x.title}\n  ${x.description}\n  ${x.url} (slug: ${x.slug})`).join('\n') : 'No matching guides.', { guides: list });
    }
    case 'get_guide': {
      const d = await data();
      const l = lang(args.lang);
      const q = str(args.slug, 'slug').trim().replace(/\/+$/, '').split('/').pop() ?? '';
      const g = d.guides.find((x) => x.key === q || x.pl.slug === q || x.en.slug === q);
      if (!g) return fail(`Guide "${q}" not found. Use search_guides to list available guides.`);
      return text(`# ${g[l].title}\nSource: ${g[l].url} (updated ${g.updated})\n\n${g[l].text}`, { title: g[l].title, url: g[l].url, updated: g.updated });
    }
    case 'list_services': {
      const d = await data();
      const l = lang(args.lang);
      const list = d.services.map((s) => ({ name: s[l].name, description: s[l].description, url: s[l].url }));
      return text(list.map((s) => `- ${s.name}: ${s.description}\n  ${s.url}`).join('\n'), { services: list });
    }
    case 'contact_info': {
      const d = await data();
      const l = lang(args.lang);
      const info = { name: d.site.name, email: d.site.email, contact_form: d.contact[l], booking: d.site.booking, linkedin: d.site.linkedin, about: d.about[l] };
      const t = l === 'pl'
        ? `${info.name}, konsultant Technical SEO i AI search. Bezpłatna, 30-minutowa konsultacja: ${info.contact_form}. E-mail: ${info.email}.${info.booking ? ` Kalendarz: ${info.booking}.` : ''} Więcej: ${info.about}`
        : `${info.name}, technical SEO and AI search consultant. Free 30-minute consultation: ${info.contact_form}. Email: ${info.email}.${info.booking ? ` Calendar: ${info.booking}.` : ''} More: ${info.about}`;
      return text(t, info);
    }
  }
  throw Object.assign(new Error(`Unknown tool: ${name}`), { rpc: -32602 });
}

async function handle(msg: Rpc, ctx: { request: Request; env: any }) {
  const data = () => load(ctx.request, ctx.env);
  switch (msg.method) {
    case 'initialize': {
      const asked = msg.params?.protocolVersion;
      return {
        protocolVersion: VERSIONS.includes(asked) ? asked : VERSIONS[0],
        capabilities: { tools: { listChanged: false } },
        serverInfo: { name: 'maciejzieciak-seo', title: 'Maciej Zięciak: Technical SEO & AI search', version: '1.0.0' },
        instructions: 'Tools for technical SEO and AI search: check or generate robots.txt rules for AI bots, validate hreflang, search and read Maciej Zięciak’s guides, list his consulting services and get contact details. Answer in the user’s language and link to the source URLs returned by the tools.',
      };
    }
    case 'ping':
      return {};
    case 'tools/list':
      return { tools };
    case 'tools/call':
      try {
        return await callTool(msg.params?.name, msg.params?.arguments, data);
      } catch (e: any) {
        if (e?.rpc) throw e;
        return fail(String(e?.message ?? e));
      }
  }
  throw Object.assign(new Error(`Method not found: ${msg.method}`), { rpc: -32601 });
}

const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json', ...CORS } });

export const onRequest = async (context: { request: Request; env: any }) => {
  const { request } = context;
  if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: CORS });
  if (request.method !== 'POST') {
    return new Response('MCP endpoint. Send JSON-RPC requests with POST (Streamable HTTP).', { status: 405, headers: { Allow: 'POST, OPTIONS', ...CORS } });
  }
  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return json({ jsonrpc: '2.0', id: null, error: { code: -32700, message: 'Parse error' } }, 400);
  }
  const batch = Array.isArray(body);
  const msgs = (batch ? body : [body]) as Rpc[];
  const replies = [];
  for (const m of msgs) {
    if (!m || typeof m !== 'object' || typeof m.method !== 'string') {
      if (m && (m as any).id !== undefined) replies.push({ jsonrpc: '2.0', id: (m as any).id ?? null, error: { code: -32600, message: 'Invalid request' } });
      continue;
    }
    if (m.id === undefined || m.id === null) continue; // notification: no reply
    try {
      replies.push({ jsonrpc: '2.0', id: m.id, result: await handle(m, context) });
    } catch (e: any) {
      replies.push({ jsonrpc: '2.0', id: m.id, error: { code: e?.rpc ?? -32603, message: String(e?.message ?? e) } });
    }
  }
  if (!replies.length) return new Response(null, { status: 202, headers: CORS });
  return json(batch ? replies : replies[0]);
};
