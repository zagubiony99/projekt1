import { pl } from './pl';
import { en } from './en';
import { polishTypo } from './typo';

export const dicts = { pl: polishTypo(pl), en };
export type Lang = keyof typeof dicts;
export const getDict = (lang: Lang) => dicts[lang];
export const otherLang = (lang: Lang): Lang => (lang === 'pl' ? 'en' : 'pl');
