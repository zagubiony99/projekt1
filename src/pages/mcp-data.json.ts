import type { APIRoute } from 'astro';
import { site } from '../config';
import { getDict } from '../i18n';
import { services, ui } from '../data/services';
import { guides } from '../data/pages';
import { pageRoutes } from '../data/routes';

// Content for the MCP server (functions/mcp.ts), generated from the same data as the pages,
// so the server always answers with what is currently published.
const plain = (s: string) =>
  s.replace(/<\/(p|li|h\d|tr|pre)>/gi, '\n').replace(/<br\s*\/?>/gi, '\n').replace(/<[^>]+>/g, '')
    .replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&amp;/g, '&')
    .replace(/ /g, ' ').replace(/[ \t]+\n/g, '\n').replace(/\n{3,}/g, '\n\n').trim();
const abs = (p: string) => new URL(p, site.url).href;

export const GET: APIRoute = () => {
  const langs = ['pl', 'en'] as const;
  const data = {
    site: { name: site.name, url: site.url, email: site.email, linkedin: site.linkedin || null, booking: site.bookingUrl || null },
    contact: Object.fromEntries(langs.map((l) => [l, abs(`${getDict(l).path}#${getDict(l).ids.contact}`)])),
    about: Object.fromEntries(langs.map((l) => [l, abs(pageRoutes.about[l])])),
    tools: Object.fromEntries(langs.map((l) => [l, { robots: abs(pageRoutes.robotsTool[l]), generator: abs(pageRoutes.robotsGen[l]), hreflang: abs(pageRoutes.hreflangTool[l]) }])),
    services: services.map((s) => ({
      key: s.key,
      ...Object.fromEntries(langs.map((l) => [l, { name: plain(s[l].name), description: plain(s[l].card.desc), url: abs(`${ui[l].base}${s[l].slug}/`) }])),
    })),
    guides: guides.map((g) => ({
      key: g.key,
      service: g.service,
      updated: g.updated,
      ...Object.fromEntries(
        langs.map((l) => [
          l,
          {
            title: plain(g[l].title),
            slug: g[l].slug,
            url: abs(g[l].path),
            description: plain(g[l].metaDescription),
            text: [plain(g[l].lead), ...g[l].sections.map((x) => `## ${plain(x.h)}\n${plain(x.body)}`), ...g[l].faq.map((f) => `Q: ${plain(f.q)}\nA: ${plain(f.a)}`)].join('\n\n'),
          },
        ]),
      ),
    })),
  };
  return new Response(JSON.stringify(data), { headers: { 'Content-Type': 'application/json; charset=utf-8' } });
};
