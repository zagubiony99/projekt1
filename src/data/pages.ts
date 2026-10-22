import { polishTypo } from '../i18n/typo';
import type { Lang } from '../i18n';
import aboutCopy from '../../content/about.json';
import robotsCopy from '../../content/tools/robots-ai.json';
import robotsGenCopy from '../../content/tools/robots-gen.json';
import { guideRoutes, pageRoutes } from './routes';

// Copy for the standalone pages (About, guides, the robots.txt tool). It lives in content/
// and is edited in the CMS; paths stay in ./routes.ts. Polish copy gets Polish typography.
export const about = { pl: polishTypo(aboutCopy.pl), en: aboutCopy.en };
export const robotsTool = { pl: polishTypo(robotsCopy.pl), en: robotsCopy.en };
export const robotsGen = { pl: polishTypo(robotsGenCopy.pl), en: robotsGenCopy.en };

export type GuideCopy = {
  metaTitle: string;
  metaDescription: string;
  title: string;
  lead: string;
  sections: { h: string; body: string }[]; // body is HTML (rich text in the CMS)
  faq: { q: string; a: string }[];
};
type GuideFile = { published: string; updated: string; pl: GuideCopy; en: GuideCopy };
const files = import.meta.glob<GuideFile>('../../content/guides/*.json', { eager: true, import: 'default' });

// Heading → anchor id for the table of contents ("Błąd 1: brak linków" → "blad-1-brak-linkow")
const slugify = (s: string) =>
  s.toLowerCase().replace(/ł/g, 'l').normalize('NFD').replace(/[̀-ͯ]/g, '')
    .replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

const words = (c: GuideCopy) =>
  [c.title, c.lead, ...c.sections.flatMap((x) => [x.h, x.body]), ...c.faq.flatMap((f) => [f.q, f.a])]
    .join(' ').replace(/<[^>]+>/g, ' ').split(/\s+/).filter(Boolean).length;

const build = (c: GuideCopy, lang: Lang, slug: string) => ({
  ...c,
  slug,
  path: `${pageRoutes.guides[lang]}${slug}/`,
  sections: c.sections.map((x) => ({ ...x, id: slugify(x.h) })),
  minutes: Math.max(1, Math.round(words(c) / 200)),
});

export const guides = guideRoutes
  .filter((r) => files[`../../content/guides/${r.key}.json`])
  .map((r) => {
    const f = files[`../../content/guides/${r.key}.json`];
    return {
      key: r.key,
      service: r.service as string,
      published: f.published,
      updated: f.updated,
      pl: build(polishTypo(f.pl), 'pl', r.slug.pl),
      en: build(f.en, 'en', r.slug.en),
    };
  });

export type Guide = (typeof guides)[number];
