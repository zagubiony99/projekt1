// Personal and contact settings live in content/site.json and are edited in the CMS.
// The CMS drops empty fields on save, so every optional setting has a default here.
// The domain stays in code: it is used for canonicals, hreflang and the sitemap.
import settings from '../content/site.json';

type Settings = {
  name: string;
  email: string;
  linkedin?: string;
  photo?: string;
  formEndpoint?: string;
  formAccessKey?: string;
  bookingUrl?: string;
  gtmId?: string;
};

export const site = {
  linkedin: '',
  photo: '',
  formEndpoint: '',
  formAccessKey: '',
  bookingUrl: '',
  gtmId: '',
  ...(settings as Settings),
  domain: 'maciejzieciak.com',
  url: 'https://maciejzieciak.com',
};
