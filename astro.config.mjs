import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import { serviceRoutes, serviceBase, pageRoutes, guideRoutes } from './src/data/routes.ts';

const SITE = 'https://maciejzieciak.com';

// PL/EN page pairs. Service, guide and other pages have different slugs per language,
// so the sitemap's hreflang links are built from the same data as the pages.
const pairs = [
  ['/', '/en/'],
  ['/polityka-prywatnosci/', '/en/privacy-policy/'],
  ...serviceRoutes.map((s) => [`${serviceBase.pl}${s.slug.pl}/`, `${serviceBase.en}${s.slug.en}/`]),
  ...Object.values(pageRoutes).map((r) => [r.pl, r.en]),
  ...guideRoutes.map((g) => [`${pageRoutes.guides.pl}${g.slug.pl}/`, `${pageRoutes.guides.en}${g.slug.en}/`]),
];
const alternates = new Map();
for (const [pl, en] of pairs) {
  const links = [
    { lang: 'pl', url: SITE + pl },
    { lang: 'en', url: SITE + en },
    { lang: 'x-default', url: SITE + pl },
  ];
  alternates.set(SITE + pl, links);
  alternates.set(SITE + en, links);
}

export default defineConfig({
  site: SITE,
  trailingSlash: 'always',
  i18n: {
    defaultLocale: 'pl',
    locales: ['pl', 'en'],
    routing: { prefixDefaultLocale: false },
  },
  integrations: [
    sitemap({
      filter: (page) => !page.includes('/404'),
      serialize(item) {
        const links = alternates.get(item.url);
        return links ? { ...item, links } : item;
      },
    }),
  ],
});
