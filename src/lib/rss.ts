import { site } from '../config';
import { getDict, type Lang } from '../i18n';
import { guides } from '../data/pages';
import { pageRoutes } from '../data/routes';

// RSS 2.0 feed of the guides, one per language (/poradniki/rss.xml, /en/guides/rss.xml).
const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/ /g, ' ');

export function guidesFeed(lang: Lang) {
  const t = getDict(lang);
  const index = new URL(pageRoutes.guides[lang], site.url).href;
  const items = [...guides]
    .sort((a, b) => b.updated.localeCompare(a.updated))
    .map((g) => {
      const url = new URL(g[lang].path, site.url).href;
      return `<item><title>${esc(g[lang].title)}</title><link>${url}</link><guid>${url}</guid><pubDate>${new Date(g.published).toUTCString()}</pubDate><description>${esc(g[lang].metaDescription)}</description></item>`;
    });
  const body = `<?xml version="1.0" encoding="UTF-8"?><rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel><title>${esc(t.guidesUi.metaTitle)}</title><link>${index}</link><description>${esc(t.guidesUi.metaDescription)}</description><language>${lang === 'pl' ? 'pl-PL' : 'en-GB'}</language><atom:link href="${index}rss.xml" rel="self" type="application/rss+xml"/>${items.join('')}</channel></rss>`;
  return new Response(body, { headers: { 'Content-Type': 'application/rss+xml; charset=utf-8' } });
}
