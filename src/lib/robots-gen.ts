// Builds a robots.txt from a simple policy. Each bot obeys only the most specific group
// (RFC 9309), so paths disallowed for everyone are repeated in the allowed bots' group.
export type RobotsPolicy = {
  allow: string[]; // bot tokens that may crawl (except the paths below)
  block: string[]; // bot tokens blocked from the whole site
  disallow: string[]; // paths closed to every bot, e.g. /cart/
  sitemap?: string;
  comments?: { allow: string; block: string; rest: string };
};

const clean = (paths: string[]) =>
  [...new Set(paths.map((p) => p.trim()).filter(Boolean).map((p) => (p.startsWith('/') || p.startsWith('*') ? p : `/${p}`)))];

export function generateRobots(p: RobotsPolicy): string {
  const paths = clean(p.disallow);
  const rules = paths.length ? paths.map((x) => `Disallow: ${x}`) : ['Allow: /'];
  const out: string[] = [];
  if (p.allow.length) {
    if (p.comments) out.push(`# ${p.comments.allow}`);
    out.push(...p.allow.map((b) => `User-agent: ${b}`), ...rules, '');
  }
  if (p.block.length) {
    if (p.comments) out.push(`# ${p.comments.block}`);
    out.push(...p.block.map((b) => `User-agent: ${b}`), 'Disallow: /', '');
  }
  if (p.comments) out.push(`# ${p.comments.rest}`);
  out.push('User-agent: *', ...rules);
  if (p.sitemap?.trim()) out.push('', `Sitemap: ${p.sitemap.trim()}`);
  return out.join('\n') + '\n';
}
