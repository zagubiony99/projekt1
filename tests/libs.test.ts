// Unit tests for the robots.txt matcher, the robots.txt generator and the hreflang checker.
// Run: npm test (Node 22+, no dependencies).
import { parseRobots, check } from '../src/lib/robots.ts';
import { generateRobots } from '../src/lib/robots-gen.ts';
import { parseInput, checkHreflang, codeProblem } from '../src/lib/hreflang.ts';
let pass = 0, fail = 0;
const eq = (name: string, got: unknown, want: unknown) => {
  const ok = JSON.stringify(got) === JSON.stringify(want);
  ok ? pass++ : fail++;
  if (!ok) console.log('FAIL', name, 'got', JSON.stringify(got), 'want', JSON.stringify(want));
};
// robots.txt (RFC 9309)
const g = parseRobots('User-agent: GPTBot\nDisallow: /\n\nUser-agent: *\nDisallow: /cart/\nAllow: /cart/public\n\nUser-agent: googlebot\nDisallow: /*.pdf$\n');
eq('gptbot blocked', check(g, 'GPTBot', '/').allowed, false);
eq('star cart blocked', check(g, 'ClaudeBot', '/cart/x').allowed, false);
eq('longest allow wins', check(g, 'ClaudeBot', '/cart/public/a').allowed, true);
eq('root allowed', check(g, 'ClaudeBot', '/').allowed, true);
eq('case-insensitive UA', check(g, 'Googlebot', '/a.pdf').allowed, false);
eq('$ anchor', check(g, 'Googlebot', '/a.pdf?x').allowed, true);
eq('own group ignores *', check(g, 'Googlebot', '/cart/').allowed, true);
eq('empty file allows', check(parseRobots(''), 'GPTBot', '/x').allowed, true);
eq('tie allow wins', check(parseRobots('User-agent: *\nDisallow: /a\nAllow: /a'), 'X', '/a').allowed, true);
eq('merged groups', check(parseRobots('User-agent: A\nDisallow: /x\n\nUser-agent: A\nDisallow: /y'), 'A', '/y').allowed, false);
eq('empty disallow', check(parseRobots('User-agent: *\nDisallow:'), 'X', '/').allowed, true);
// generator round-trip
const out = generateRobots({ allow: ['OAI-SearchBot'], block: ['GPTBot'], disallow: ['/cart/', 'admin/'], sitemap: 'https://x.pl/s.xml' });
const gg = parseRobots(out);
eq('gen allowed bot root', check(gg, 'OAI-SearchBot', '/').allowed, true);
eq('gen allowed bot cart', check(gg, 'OAI-SearchBot', '/cart/a').allowed, false);
eq('gen path normalised', check(gg, 'Other', '/admin/').allowed, false);
eq('gen blocked bot', check(gg, 'GPTBot', '/').allowed, false);
eq('gen sitemap', out.includes('Sitemap: https://x.pl/s.xml'), true);
eq('gen no paths -> Allow', generateRobots({ allow: ['A'], block: [], disallow: [] }).includes('Allow: /'), true);
// hreflang codes
for (const [c, want] of [['pl', null], ['en-GB', null], ['x-default', null], ['zh-Hant-TW', null], ['en-UK', 'uk'], ['en_GB', 'underscore'], ['GB', 'regionOnly'], ['xx', 'language'], ['en-XX', 'region'], ['es-419', 'regionFormat'], ['en-EU', 'region'], ['fil', 'threeLetter']] as const)
  eq(`code ${c}`, codeProblem(c)?.key ?? null, want);
// hreflang pages
const html = parseInput('<link rel="alternate" hreflang="pl" href="https://x.pl/"><link rel="alternate" hreflang="en" href="/en/">', 'https://x.pl/');
eq('html mode', html.mode, 'html');
eq('html issues', checkHreflang(html.pages).map((i) => i.code).sort(), ['noXDefault', 'relative']);
const sm = parseInput(`<urlset><url><loc>https://x.pl/</loc><xhtml:link rel="alternate" hreflang="pl" href="https://x.pl/"/><xhtml:link rel="alternate" hreflang="en" href="https://x.pl/en/"/><xhtml:link rel="alternate" hreflang="x-default" href="https://x.pl/"/></url><url><loc>https://x.pl/en/</loc><xhtml:link rel="alternate" hreflang="en" href="https://x.pl/en/"/><xhtml:link rel="alternate" hreflang="x-default" href="https://x.pl/"/></url></urlset>`);
eq('sitemap pages', sm.pages.length, 2);
eq('sitemap noReturn', checkHreflang(sm.pages).filter((i) => i.code === 'noReturn').map((i) => i.page), ['https://x.pl/']);
eq('dup code', checkHreflang([{ url: '', alts: [{ code: 'pl', href: 'https://a/' }, { code: 'PL', href: 'https://b/' }] }]).some((i) => i.code === 'duplicate'), true);
eq('none', checkHreflang(parseInput('<p>x</p>').pages)[0].code, 'none');
console.log(`unit: ${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
