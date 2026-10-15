// Polish copy lives in content/pl.json and is edited in the CMS (see .pages.yml).
// Only technical fields stay here: section anchors and paths are part of the URLs.
import copy from '../../content/pl.json';

export const pl = {
  lang: 'pl',
  locale: 'pl_PL',
  path: '/',
  ids: { services: 'uslugi', experience: 'doswiadczenie', process: 'proces', faq: 'faq', contact: 'kontakt', gets: 'co-dostajesz' },
  ...copy,
  privacy: { ...copy.privacy, path: '/polityka-prywatnosci/' },
};

export type Dict = typeof pl;
