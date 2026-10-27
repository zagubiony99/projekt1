// robots.txt matching as specified in RFC 9309 (and as Google applies it):
// - a crawler obeys the group(s) whose user-agent matches its product token (case-insensitive);
//   several matching groups are merged; with none, the "*" group(s) apply;
// - within those rules the longest matching path wins; on a tie, allow wins;
// - "*" matches any sequence of characters, "$" anchors the end of the path;
// - no matching rule (or no robots.txt rules at all) means the path is allowed.

type Rule = { allow: boolean; path: string };
type Group = { agents: string[]; rules: Rule[] };
export type Verdict = { allowed: boolean; rule: Rule | null; group: string | null };

export function parseRobots(txt: string): Group[] {
  const groups: Group[] = [];
  let cur: Group | null = null;
  let lastWasAgent = false;
  for (const raw of txt.split(/\r\n|\r|\n/)) {
    const line = raw.replace(/#.*$/, '').trim();
    const i = line.indexOf(':');
    if (i < 1) continue;
    const field = line.slice(0, i).trim().toLowerCase();
    const value = line.slice(i + 1).trim();
    if (field === 'user-agent') {
      // consecutive user-agent lines share one group; after rules, a new group starts
      if (!cur || !lastWasAgent) groups.push((cur = { agents: [], rules: [] }));
      cur.agents.push(value.toLowerCase());
      lastWasAgent = true;
    } else if (field === 'allow' || field === 'disallow') {
      lastWasAgent = false;
      if (!cur) continue; // rules before any user-agent line are ignored
      // an empty Disallow means "nothing is disallowed"
      if (value === '') continue;
      cur.rules.push({ allow: field === 'allow', path: value });
    }
    // sitemap, crawl-delay and unknown fields are ignored and don't affect grouping
  }
  return groups;
}

const escape = (s: string) => s.replace(/[.+?^{}()|[\]\\]/g, '\\$&');
function matches(pattern: string, path: string): boolean {
  const anchored = pattern.endsWith('$');
  const body = anchored ? pattern.slice(0, -1) : pattern;
  const re = new RegExp('^' + body.split('*').map(escape).join('.*') + (anchored ? '$' : ''));
  return re.test(path);
}

export function check(groups: Group[], token: string, path: string): Verdict {
  const t = token.toLowerCase();
  let picked = groups.filter((g) => g.agents.includes(t));
  let name = token;
  if (!picked.length) {
    picked = groups.filter((g) => g.agents.includes('*'));
    name = '*';
  }
  if (!picked.length) return { allowed: true, rule: null, group: null };
  let best: Rule | null = null;
  for (const r of picked.flatMap((g) => g.rules)) {
    if (!matches(r.path, path)) continue;
    const len = r.path.length;
    if (!best || len > best.path.length || (len === best.path.length && r.allow && !best.allow)) best = r;
  }
  return { allowed: best ? best.allow : true, rule: best, group: name };
}
