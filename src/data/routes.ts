// Service pages: keys, URL slugs and contact-form topics. Kept in code, not in the CMS,
// because changing a slug changes a public URL (and needs a redirect).
// The page copy for each key lives in content/services/<key>.json.
export const serviceRoutes = [
  { key: 'audit', slug: { pl: 'audyt-technical-seo', en: 'technical-seo-audit' }, topic: { pl: 'Audyt techniczny', en: 'Technical audit' } },
  { key: 'ai', slug: { pl: 'widocznosc-w-ai-search', en: 'ai-search-visibility' }, topic: { pl: 'AI search', en: 'AI search' } },
  { key: 'large', slug: { pl: 'seo-duzych-serwisow', en: 'large-website-seo' }, topic: { pl: 'Duży serwis', en: 'Large website' } },
  { key: 'intl', slug: { pl: 'seo-enterprise-miedzynarodowe', en: 'enterprise-international-seo' }, topic: { pl: 'Enterprise / AEM', en: 'Enterprise / AEM' } },
  { key: 'migration', slug: { pl: 'migracja-strony-seo', en: 'website-migration-seo' }, topic: { pl: 'Migracja', en: 'Migration' } },
  { key: 'ecom', slug: { pl: 'seo-ecommerce', en: 'ecommerce-seo' }, topic: { pl: 'E-commerce', en: 'E-commerce' } },
] as const;

export const serviceBase = { pl: '/uslugi/', en: '/en/services/' } as const;
