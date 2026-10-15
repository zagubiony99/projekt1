import type { APIRoute } from 'astro';
import { site } from '../config';
import { getDict } from '../i18n';
import { services } from '../data/services';

// /llms.txt: a plain-text map of the site for AI assistants (llmstxt.org format),
// generated from the same data as the pages so it never goes stale.
export const GET: APIRoute = () => {
  const pl = getDict('pl');
  const en = getDict('en');
  const plain = (s: string) => s.replace(/ /g, ' ');
  const url = (p: string) => new URL(p, site.url).href;

  const body = [
    `# ${site.name}`,
    '',
    `> ${en.meta.description}`,
    '',
    `${site.name} is an independent Technical SEO and AI search consultant with 9 years of experience, working in Polish and English. ` +
      `Experience includes Philip Morris International (Manager SEO & AI Search Operations), Accenture Song and IG. ` +
      `Industries: ${en.experience.industries.join(', ')}. Tools: ${en.tools.items.join(', ')}. Contact: ${site.email}.`,
    '',
    '## Services (English)',
    ...services.map((s) => `- [${s.en.name}](${url(`/en/services/${s.en.slug}/`)}): ${s.en.metaDescription}`),
    '',
    '## Usługi (polski)',
    ...services.map((s) => `- [${plain(s.pl.name)}](${url(`/uslugi/${s.pl.slug}/`)}): ${plain(s.pl.metaDescription)}`),
    '',
    '## Pages',
    `- [Home (English)](${url('/en/')}): ${en.meta.description}`,
    `- [Strona główna (polski)](${url('/')}): ${plain(pl.meta.description)}`,
    `- [Contact](${url(`/en/#${en.ids.contact}`)}): free 30-minute consultation`,
    '',
    '## Optional',
    `- [${en.privacy.label}](${url(en.privacy.path)})`,
    `- [${pl.privacy.label}](${url(pl.privacy.path)})`,
    '',
  ].join('\n');

  return new Response(body, { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
};
