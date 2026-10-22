// Service pages: keys, URL slugs and contact-form topics. Kept in code, not in the CMS,
// because changing a slug changes a public URL (and needs a redirect).
// The page copy for each key lives in content/services/<key>.json.
export const serviceRoutes = [
  { key: 'audit', slug: { pl: 'audyt-technical-seo', en: 'technical-seo-audit' }, topic: { pl: 'Audyt techniczny', en: 'Technical audit' } },
  { key: 'ai', slug: { pl: 'widocznosc-w-ai-search', en: 'ai-search-visibility' }, topic: { pl: 'AI search', en: 'AI search' } },
  { key: 'mcp', slug: { pl: 'aplikacja-chatgpt-mcp', en: 'chatgpt-app-mcp' }, topic: { pl: 'Aplikacja w ChatGPT', en: 'ChatGPT app' } },
  { key: 'schema', slug: { pl: 'dane-strukturalne-schema', en: 'structured-data-schema' }, topic: { pl: 'Dane strukturalne', en: 'Structured data' } },
  { key: 'webops', slug: { pl: 'webops-seo-operations', en: 'webops-seo-operations' }, topic: { pl: 'WebOps', en: 'WebOps' } },
  { key: 'content', slug: { pl: 'planowanie-tresci-seo', en: 'seo-content-planning' }, topic: { pl: 'Planowanie treści', en: 'Content planning' } },
  { key: 'large', slug: { pl: 'seo-duzych-serwisow', en: 'large-website-seo' }, topic: { pl: 'Duży serwis', en: 'Large website' } },
  { key: 'intl', slug: { pl: 'seo-enterprise-miedzynarodowe', en: 'enterprise-international-seo' }, topic: { pl: 'Enterprise / CMS', en: 'Enterprise / CMS' } },
  { key: 'migration', slug: { pl: 'migracja-strony-seo', en: 'website-migration-seo' }, topic: { pl: 'Migracja', en: 'Migration' } },
  { key: 'ecom', slug: { pl: 'seo-ecommerce', en: 'ecommerce-seo' }, topic: { pl: 'E-commerce', en: 'E-commerce' } },
] as const;

export const serviceBase = { pl: '/uslugi/', en: '/en/services/' } as const;

// Standalone pages. Paths are public URLs, so they live in code (changing one needs a redirect).
export const pageRoutes = {
  about: { pl: '/o-mnie/', en: '/en/about/' },
  guides: { pl: '/poradniki/', en: '/en/guides/' },
  robotsTool: { pl: '/narzedzia/robots-txt-boty-ai/', en: '/en/tools/robots-txt-ai-bot-checker/' },
  robotsGen: { pl: '/narzedzia/generator-robots-txt/', en: '/en/tools/robots-txt-generator/' },
  hreflangTool: { pl: '/narzedzia/tester-hreflang/', en: '/en/tools/hreflang-checker/' },
  mcpServer: { pl: '/narzedzia/serwer-mcp/', en: '/en/tools/mcp-server/' },
} as const;

// Guides: key, URL slugs and the service each guide leads to.
// The article copy lives in content/guides/<key>.json.
export const guideRoutes = [
  { key: 'chatgpt-apps', service: 'mcp', slug: { pl: 'aplikacja-w-chatgpt-mcp', en: 'chatgpt-apps-mcp' } },
  { key: 'ai-overviews', service: 'ai', slug: { pl: 'ai-overviews-jak-przygotowac-strone', en: 'ai-overviews-how-to-prepare' } },
  { key: 'ai-bots', service: 'ai', slug: { pl: 'boty-ai-robots-txt', en: 'ai-bots-robots-txt' } },
  { key: 'audit-cost', service: 'audit', slug: { pl: 'audyt-seo-cena', en: 'seo-audit-cost' } },
  { key: 'audit', service: 'audit', slug: { pl: 'audyt-techniczny-seo-checklista', en: 'technical-seo-audit-checklist' } },
  { key: 'migration', service: 'migration', slug: { pl: 'migracja-strony-checklista-seo', en: 'website-migration-seo-checklist' } },
  { key: 'release', service: 'webops', slug: { pl: 'seo-przed-wdrozeniem-checklista', en: 'pre-release-seo-checklist' } },
  { key: 'hreflang', service: 'intl', slug: { pl: 'hreflang-najczestsze-bledy', en: 'hreflang-common-mistakes' } },
  { key: 'facets', service: 'ecom', slug: { pl: 'filtry-w-sklepie-seo', en: 'faceted-navigation-seo' } },
] as const;
