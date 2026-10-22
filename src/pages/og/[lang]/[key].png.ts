import type { APIRoute } from 'astro';
import { site } from '../../../config';
import { ogCards, type OgCard } from '../../../data/og';
import { renderOg } from '../../../lib/og';

export function getStaticPaths() {
  return ogCards.map((c) => ({ params: { lang: c.lang, key: c.key }, props: { card: c } }));
}

export const GET: APIRoute = async ({ props }) => {
  const { card } = props as { card: OgCard };
  const png = await renderOg({ eyebrow: card.eyebrow, title: card.title, name: site.name, site: new URL(site.url).host });
  return new Response(png, { headers: { 'Content-Type': 'image/png' } });
};
