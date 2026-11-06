// Bots checked by the robots.txt tool. Tokens and purposes follow the providers' own
// documentation; review this list when providers announce new or renamed bots.
export type BotGroup = 'search' | 'aiSearch' | 'training' | 'user';
export type Bot = { token: string; company: string; group: BotGroup; purpose: { pl: string; en: string } };

export const bots: Bot[] = [
  { token: 'Googlebot', company: 'Google', group: 'search', purpose: { pl: 'Wyszukiwarka Google, w tym AI Overviews i AI Mode', en: 'Google Search, including AI Overviews and AI Mode' } },
  { token: 'Bingbot', company: 'Microsoft', group: 'search', purpose: { pl: 'Wyszukiwarka Bing, z której korzysta też Copilot', en: 'Bing search, also used by Copilot' } },
  { token: 'OAI-SearchBot', company: 'OpenAI', group: 'aiSearch', purpose: { pl: 'Wyszukiwanie w ChatGPT', en: 'ChatGPT search' } },
  { token: 'Claude-SearchBot', company: 'Anthropic', group: 'aiSearch', purpose: { pl: 'Wyszukiwanie w Claude', en: 'Search in Claude' } },
  { token: 'PerplexityBot', company: 'Perplexity', group: 'aiSearch', purpose: { pl: 'Indeks wyszukiwarki Perplexity', en: 'Perplexity search index' } },
  { token: 'GPTBot', company: 'OpenAI', group: 'training', purpose: { pl: 'Trening modeli OpenAI', en: 'OpenAI model training' } },
  { token: 'ClaudeBot', company: 'Anthropic', group: 'training', purpose: { pl: 'Trening modeli Anthropic', en: 'Anthropic model training' } },
  { token: 'Google-Extended', company: 'Google', group: 'training', purpose: { pl: 'Użycie treści przez modele Gemini (nie wpływa na wyszukiwarkę)', en: 'Use of content by Gemini models (does not affect Search)' } },
  { token: 'Applebot-Extended', company: 'Apple', group: 'training', purpose: { pl: 'Użycie treści do trenowania modeli Apple', en: 'Use of content to train Apple models' } },
  { token: 'CCBot', company: 'Common Crawl', group: 'training', purpose: { pl: 'Otwarty zbiór danych używany do trenowania modeli', en: 'Open dataset used for model training' } },
  { token: 'meta-externalagent', company: 'Meta', group: 'training', purpose: { pl: 'Trening modeli i produkty AI Mety', en: 'Meta model training and AI products' } },
  { token: 'Bytespider', company: 'ByteDance', group: 'training', purpose: { pl: 'Crawler ByteDance zbierający dane dla modeli AI', en: 'ByteDance crawler collecting data for AI models' } },
  { token: 'ChatGPT-User', company: 'OpenAI', group: 'user', purpose: { pl: 'Otwarcie strony na prośbę użytkownika ChatGPT', en: 'Opening a page when a ChatGPT user asks' } },
  { token: 'Claude-User', company: 'Anthropic', group: 'user', purpose: { pl: 'Otwarcie strony na prośbę użytkownika Claude', en: 'Opening a page when a Claude user asks' } },
  { token: 'Perplexity-User', company: 'Perplexity', group: 'user', purpose: { pl: 'Otwarcie strony na prośbę użytkownika Perplexity', en: 'Opening a page when a Perplexity user asks' } },
];
