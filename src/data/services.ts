import { polishTypo } from '../i18n/typo';
import { getDict } from '../i18n';
import { serviceRoutes, serviceBase } from './routes';

// Service landing pages (PL + EN). Each entry is one sales page per language.
// The copy lives in content/services/<key>.json (edited in the CMS); slugs and topics in ./routes.ts.
// Copy is built only on facts from the profile; no invented client results or prices.

export type ServiceCopy = {
  slug: string;
  name: string;            // short name (nav, cards, breadcrumbs)
  card: { desc: string; tags: string[] }; // homepage gallery card
  metaTitle: string;
  metaDescription: string;
  eyebrow: string;
  title: string;           // benefit headline (H1)
  lead: string;
  painTitle: string;
  pains: string[];
  getTitle: string;
  gets: { t: string; d: string }[];
  stepsTitle: string;
  steps: { t: string; when: string; d: string }[];
  forTitle: string;
  forYes: string[];
  forNo: string[];
  proof: string;           // one experience line specific to this service
  faq: { q: string; a: string }[];
};

type Pair = { key: string; topic: { pl: string; en: string }; pl: ServiceCopy; en: ServiceCopy };

type Content = { pl: Omit<ServiceCopy, 'slug'>; en: Omit<ServiceCopy, 'slug'> };
const files = import.meta.glob<Content>('../../content/services/*.json', { eager: true, import: 'default' });

export const services: Pair[] = serviceRoutes
  .filter((r) => files[`../../content/services/${r.key}.json`])
  .map((r) => {
    const c = files[`../../content/services/${r.key}.json`];
    return {
      key: r.key,
      topic: r.topic,
      // Polish copy gets Polish typography (no one-letter words at line ends)
      pl: polishTypo({ ...c.pl, slug: r.slug.pl }),
      en: { ...c.en, slug: r.slug.en },
    };
  });

// Labels used on service pages ("Book a free consultation", "Other services" …) come from the
// language files; the base path is part of the URL and stays in code.
export const ui = {
  pl: { base: serviceBase.pl, ...getDict('pl').serviceUi },
  en: { base: serviceBase.en, ...getDict('en').serviceUi },
};
