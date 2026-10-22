// Hreflang checks for pasted <link> tags (one page) or an XML sitemap with xhtml:link (many pages).
// Language and region codes are validated with the runtime's Intl data instead of bundled code lists.

export type Alt = { code: string; href: string };
export type Page = { url: string; alts: Alt[] };
export type Issue = { level: 'error' | 'warning' | 'info'; code: string; page?: string; detail: string };

const attrs = (tag: string) => {
  const out: Record<string, string> = {};
  for (const m of tag.matchAll(/([\w:-]+)\s*=\s*(?:"([^"]*)"|'([^']*)')/g)) out[m[1].toLowerCase()] = m[2] ?? m[3] ?? '';
  return out;
};

export function parseInput(input: string, pageUrl = ''): { mode: 'sitemap' | 'html'; pages: Page[] } {
  if (/<url[\s>]/i.test(input)) {
    const pages: Page[] = [];
    for (const block of input.match(/<url[\s>][\s\S]*?<\/url>/gi) ?? []) {
      const loc = block.match(/<loc>\s*([^<]+?)\s*<\/loc>/i)?.[1] ?? '';
      const alts = (block.match(/<xhtml:link\b[^>]*>/gi) ?? [])
        .map(attrs)
        .filter((a) => (a.rel ?? '').toLowerCase() === 'alternate' && a.hreflang !== undefined)
        .map((a) => ({ code: a.hreflang.trim(), href: (a.href ?? '').trim() }));
      pages.push({ url: loc, alts });
    }
    return { mode: 'sitemap', pages };
  }
  const alts = (input.match(/<link\b[^>]*>/gi) ?? [])
    .map(attrs)
    .filter((a) => (a.rel ?? '').toLowerCase().split(/\s+/).includes('alternate') && a.hreflang !== undefined)
    .map((a) => ({ code: a.hreflang.trim(), href: (a.href ?? '').trim() }));
  return { mode: 'html', pages: [{ url: pageUrl.trim(), alts }] };
}

let L: Intl.DisplayNames | null = null;
let R: Intl.DisplayNames | null = null;
const lang = (c: string) => (L ??= new Intl.DisplayNames(['en'], { type: 'language', fallback: 'none' })).of(c);
const region = (c: string) => (R ??= new Intl.DisplayNames(['en'], { type: 'region', fallback: 'none' })).of(c);
// two-letter codes Intl knows that are not countries in ISO 3166-1
const NOT_COUNTRY = new Set(['EU', 'EZ', 'UN', 'ZZ', 'QO']);

// Returns a problem description, or null when the code is fine.
export function codeProblem(code: string): { level: 'error' | 'warning'; key: string } | null {
  if (code.toLowerCase() === 'x-default') return null;
  if (code.includes('_')) return { level: 'error', key: 'underscore' };
  const parts = code.split('-');
  const [l, ...rest] = parts;
  if (!/^[a-z]{2,3}$/i.test(l)) return { level: 'error', key: 'format' };
  if (/^[a-z]{2}$/i.test(l) && region(l.toUpperCase()) && !lang(l.toLowerCase())) return { level: 'error', key: 'regionOnly' };
  if (!lang(l.toLowerCase())) return { level: 'error', key: 'language' };
  if (l.length === 3) return { level: 'warning', key: 'threeLetter' };
  let r = rest;
  if (r[0] && /^[a-z]{4}$/i.test(r[0])) r = r.slice(1); // script, e.g. zh-Hant
  if (r.length > 1) return { level: 'error', key: 'format' };
  if (r.length === 1) {
    const reg = r[0].toUpperCase();
    if (reg === 'UK') return { level: 'error', key: 'uk' };
    if (!/^[A-Z]{2}$/.test(reg)) return { level: 'warning', key: 'regionFormat' };
    if (NOT_COUNTRY.has(reg) || !region(reg)) return { level: 'error', key: 'region' };
  }
  return null;
}

const norm = (u: string) => u.trim().replace(/#.*$/, '');
const absolute = (u: string) => /^https?:\/\//i.test(u);

export function checkHreflang(pages: Page[]): Issue[] {
  const issues: Issue[] = [];
  const byUrl = new Map(pages.filter((p) => p.url).map((p) => [norm(p.url), p]));
  for (const p of pages) {
    const page = p.url || undefined;
    if (!p.alts.length) {
      issues.push({ level: 'error', code: 'none', page, detail: '' });
      continue;
    }
    const seen = new Map<string, string>();
    for (const a of p.alts) {
      const prob = codeProblem(a.code);
      if (prob) issues.push({ level: prob.level, code: `code.${prob.key}`, page, detail: a.code });
      if (!absolute(a.href)) issues.push({ level: 'error', code: 'relative', page, detail: `${a.code} → ${a.href || '""'}` });
      const k = a.code.toLowerCase();
      if (seen.has(k) && seen.get(k) !== norm(a.href)) issues.push({ level: 'error', code: 'duplicate', page, detail: a.code });
      seen.set(k, norm(a.href));
    }
    if (!p.alts.some((a) => a.code.toLowerCase() === 'x-default')) issues.push({ level: 'info', code: 'noXDefault', page, detail: '' });
    if (p.url && !p.alts.some((a) => norm(a.href) === norm(p.url))) issues.push({ level: 'warning', code: 'noSelf', page, detail: '' });
    // return links: every page this one points to must point back (checked only for pages in the input)
    if (p.url) {
      for (const a of p.alts) {
        const target = byUrl.get(norm(a.href));
        if (!target || norm(a.href) === norm(p.url) || a.code.toLowerCase() === 'x-default') continue;
        if (!target.alts.some((b) => norm(b.href) === norm(p.url))) issues.push({ level: 'error', code: 'noReturn', page, detail: a.href });
      }
    }
  }
  return issues;
}
