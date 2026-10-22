import { getDict, type Lang } from '../i18n';
import { services } from './services';
import { about, guides, robotsTool, robotsGen, hreflangTool, mcpServer } from './pages';

// One share card per page: /og/<lang>/<key>.png (rendered by src/pages/og/[lang]/[key].png.ts).
// The home page keeps its hand-made public/og-<lang>.png.
export type OgCard = { lang: Lang; key: string; eyebrow: string; title: string };

export const ogCards: OgCard[] = (['pl', 'en'] as const).flatMap((lang) => {
  const t = getDict(lang);
  return [
    ...services.map((s) => ({ lang, key: `service-${s.key}`, eyebrow: s[lang].eyebrow, title: s[lang].title })),
    ...guides.map((g) => ({ lang, key: `guide-${g.key}`, eyebrow: t.guidesUi.eyebrow, title: g[lang].title })),
    { lang, key: 'guides', eyebrow: t.guidesUi.eyebrow, title: t.guidesUi.title },
    { lang, key: 'about', eyebrow: about[lang].eyebrow, title: about[lang].title },
    { lang, key: 'tool-robots', eyebrow: robotsTool[lang].eyebrow, title: robotsTool[lang].title },
    { lang, key: 'tool-robots-gen', eyebrow: robotsGen[lang].eyebrow, title: robotsGen[lang].title },
    { lang, key: 'tool-hreflang', eyebrow: hreflangTool[lang].eyebrow, title: hreflangTool[lang].title },
    { lang, key: 'tool-mcp', eyebrow: mcpServer[lang].eyebrow, title: mcpServer[lang].title },
  ];
});

export const ogPath = (lang: Lang, key: string) => `/og/${lang}/${key}.png`;
