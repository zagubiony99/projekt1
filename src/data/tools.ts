import type { ImageMetadata } from 'astro';

// Tool logos for the "Tools I work with" strip. Drop a file into src/assets/tools/ named
// after the tool (lowercase, letters and digits only), e.g. screamingfrog.svg, botify.png,
// adobeanalytics.svg. Tools without a file are shown as text.
const files = import.meta.glob<ImageMetadata>('../assets/tools/*.{svg,png,webp,jpg}', { eager: true, import: 'default' });
const byKey = new Map(Object.entries(files).map(([p, img]) => [p.split('/').pop()!.replace(/\.\w+$/, ''), img]));

export const toolKey = (name: string) => name.toLowerCase().replace(/[^a-z0-9]/g, '');
export const toolLogo = (name: string): ImageMetadata | undefined => byKey.get(toolKey(name));
