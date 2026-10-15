// English copy lives in content/en.json and is edited in the CMS (see .pages.yml).
// Only technical fields stay here: section anchors and paths are part of the URLs.
import type { Dict } from './pl';
import copy from '../../content/en.json';

export const en: Dict = {
  lang: 'en',
  locale: 'en_GB',
  path: '/en/',
  ids: { services: 'services', experience: 'experience', process: 'process', faq: 'faq', contact: 'contact', gets: 'what-you-get' },
  ...copy,
  privacy: { ...copy.privacy, path: '/en/privacy-policy/' },
};
