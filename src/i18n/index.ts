import { pl } from './pl';
import { en } from './en';

export const dicts = { pl, en };
export type Lang = keyof typeof dicts;
export const getDict = (lang: Lang) => dicts[lang];
export const otherLang = (lang: Lang): Lang => (lang === 'pl' ? 'en' : 'pl');
