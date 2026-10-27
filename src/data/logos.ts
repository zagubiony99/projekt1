import type { ImageMetadata } from 'astro';
import ig from '../assets/logos/ig.png';
import igMono from '../assets/logos/ig-mono.png';
import accenture from '../assets/logos/accenture.png';
import accentureMono from '../assets/logos/accenture-mono.png';
import googleAds from '../assets/logos/google-ads.png';
import googleAdsMono from '../assets/logos/google-ads-mono.png';
import euvic from '../assets/logos/euvic.png';
import euvicMono from '../assets/logos/euvic-mono.png';
import digitree from '../assets/logos/digitree.png';
import digitreeMono from '../assets/logos/digitree-mono.png';

// Logos in the hero trust row. Each has a grey version (shown) and the brand colours (on hover).
// Width follows the logo's shape so a square mark and a long wordmark look the same size:
// width = base * aspect^0.55, with a per-logo nudge for marks that look heavier or lighter.
const base = 44;
const make = (name: string, color: ImageMetadata, mono: ImageMetadata, nudge = 1) => ({
  name,
  color,
  mono,
  w: Math.round(base * (color.width / color.height) ** 0.55 * nudge),
});

export const logos = [
  make('Accenture', accenture, accentureMono),
  make('IG', ig, igMono, 0.72),
  make('Google Ads', googleAds, googleAdsMono, 1.15),
  make('Euvic', euvic, euvicMono, 0.8),
  make('Digitree', digitree, digitreeMono),
];
