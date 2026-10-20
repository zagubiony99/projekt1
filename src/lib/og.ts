// Share images (Open Graph, 1200×630 PNG) rendered at build time from page copy,
// so every page gets its own card and a title changed in the CMS updates the image too.
import satori from 'satori';
import { Resvg } from '@resvg/resvg-js';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';

const font = (name: string) => readFileSync(join(process.cwd(), 'node_modules/@fontsource/inter-tight/files', name));
// The latin subset lacks Polish letters (ę, ł, ż…), so latin-ext is registered as a second family
// and listed as the fallback in font-family.
const fonts = [
  { name: 'Inter Tight', data: font('inter-tight-latin-700-normal.woff'), weight: 700 as const, style: 'normal' as const },
  { name: 'Inter Tight', data: font('inter-tight-latin-500-normal.woff'), weight: 500 as const, style: 'normal' as const },
  { name: 'Inter Tight Ext', data: font('inter-tight-latin-ext-700-normal.woff'), weight: 700 as const, style: 'normal' as const },
  { name: 'Inter Tight Ext', data: font('inter-tight-latin-ext-500-normal.woff'), weight: 500 as const, style: 'normal' as const },
];

// Same stops as --a1..--a4 in src/styles/global.css
const A = ['#2f5bff', '#0096d6', '#00a87e', '#3a9e00'];

type Node = { type: string; props: Record<string, unknown> & { children?: unknown } };
const h = (type: string, style: Record<string, unknown>, children?: unknown): Node => ({ type, props: { style, children } });

export async function renderOg({ eyebrow, title, name, site }: { eyebrow: string; title: string; name: string; site: string }) {
  // long titles step down so they always fit in three lines
  const size = title.length > 70 ? 54 : title.length > 46 ? 62 : 72;
  const tree = h(
    'div',
    {
      width: '100%',
      height: '100%',
      display: 'flex',
      position: 'relative',
      backgroundColor: '#ffffff',
      backgroundImage: `radial-gradient(60% 70% at 100% 0%, ${A[1]}22, transparent 70%), radial-gradient(55% 60% at 0% 100%, ${A[3]}1f, transparent 70%)`,
      fontFamily: 'Inter Tight, Inter Tight Ext',
      color: '#1d1d1f',
    },
    // content sits in an absolutely placed box: satori miscounts root padding with space-between
    h('div', { position: 'absolute', top: 64, left: 72, right: 72, bottom: 60, display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }, [
      h('div', { display: 'flex', alignItems: 'center', gap: 16 }, [
        h('div', { display: 'flex', alignItems: 'center', justifyContent: 'center', width: 52, height: 52, borderRadius: 13, backgroundColor: '#000', color: '#fff', fontSize: 22, fontWeight: 700, letterSpacing: -1 }, 'MZ'),
        h('div', { fontSize: 28, fontWeight: 700, letterSpacing: -0.6 }, name),
      ]),
      h('div', { display: 'flex', flexDirection: 'column', gap: 22 }, [
        h('div', { fontSize: 28, fontWeight: 500, color: '#6e6e73' }, eyebrow),
        h('div', { fontSize: size, fontWeight: 700, lineHeight: 1.05, letterSpacing: size * -0.035, maxWidth: 1000 }, title),
      ]),
      h('div', { display: 'flex', alignItems: 'center', justifyContent: 'space-between' }, [
        h('div', { fontSize: 24, fontWeight: 500, color: '#6e6e73' }, site),
        h('div', { display: 'flex', width: 280, height: 8, borderRadius: 8, backgroundImage: `linear-gradient(90deg, ${A.join(', ')})` }),
      ]),
    ]),
  );
  const svg = await satori(tree as never, { width: 1200, height: 630, fonts });
  return new Resvg(svg, { fitTo: { mode: 'width', value: 1200 } }).render().asPng();
}
