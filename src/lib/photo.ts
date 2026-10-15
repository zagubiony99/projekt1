// The portrait uploaded in the CMS ("Ustawienia i kontakt" → "Zdjęcie").
// The CMS stores "/media/<file>"; the file itself lives in src/assets/media, so Astro can
// crop, resize and convert it at build time. No photo (or a missing file) = null, and every
// place that shows the portrait simply renders nothing.
import type { ImageMetadata } from 'astro';
import { site } from '../config';

const files = import.meta.glob<{ default: ImageMetadata }>('../assets/media/*.{jpg,jpeg,png,webp,avif,JPG,JPEG,PNG,WEBP}', { eager: true });
const name = site.photo ? decodeURIComponent(site.photo.split('/').pop() ?? '') : '';

export const photo: ImageMetadata | null = name
  ? (Object.entries(files).find(([path]) => path.split('/').pop() === name)?.[1].default ?? null)
  : null;
