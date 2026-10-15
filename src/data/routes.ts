// Service pages: keys, URL slugs and contact-form topics. Kept in code, not in the CMS,
// because changing a slug changes a public URL (and needs a redirect).
// The page copy for each key lives in content/services/<key>.json.
export const serviceRoutes = [
  { key: 'audit', slug: { pl: 'audyt-technical-seo', en: 'technical-seo-audit' }, topic: { pl: 'Audyt techniczny', en: 'Technical audit' } },
  { key: 'ai', slug: { pl: 'widocznosc-w-ai-search', en: 'ai-search-visibility' }, topic: { pl: 'AI search', en: 'AI search' } },
  { key: 'schema', slug: { pl: 'dane-strukturalne-schema', en: 'structured-data-schema' }, topic: { pl: 'Dane strukturalne', en: 'Structured data' } },
  { key: 'webops', slug: { pl: 'webops-seo-operations', en: 'webops-seo-operations' }, topic: { pl: 'WebOps', en: 'WebOps' } },
  { key: 'content', slug: { pl: 'planowanie-tresci-seo', en: 'seo-content-planning' }, topic: { pl: 'Planowanie treści', en: 'Content planning' } },
  { key: 'large', slug: { pl: 'seo-duzych-serwisow', en: 'large-website-seo' }, topic: { pl: 'Duży serwis', en: 'Large website' } },
  { key: 'intl', slug: { pl: 'seo-enterprise-miedzynarodowe', en: 'enterprise-international-seo' }, topic: { pl: 'Enterprise / CMS', en: 'Enterprise / CMS' } },
  { key: 'migration', slug: { pl: 'migracja-strony-seo', en: 'website-migration-seo' }, topic: { pl: 'Migracja', en: 'Migration' } },
  { key: 'ecom', slug: { pl: 'seo-ecommerce', en: 'ecommerce-seo' }, topic: { pl: 'E-commerce', en: 'E-commerce' } },
] as const;

export const serviceBase = { pl: '/uslugi/', en: '/en/services/' } as const;
