// Polish typography: a one-letter word (a, i, o, u, w, z) must not be left at the end of a line,
// so it is glued to the next word with a non-breaking space. Applied to all Polish copy at build time.
const glue = (s: string) => s.replace(/(?<![^\s(„])([aiouwzAIOUWZ])[ \t\n]+/g, '$1 ');

// Meta strings (<title>, meta description) are left alone: they are not laid out in lines.
const SKIP = new Set(['meta', 'metaTitle', 'metaDescription', 'description', 'path', 'slug', 'ids', 'code']);

export const polishTypo = <T>(v: T, key = ''): T => {
  if (SKIP.has(key)) return v;
  if (typeof v === 'string') return glue(v) as T;
  if (Array.isArray(v)) return v.map((x) => polishTypo(x)) as T;
  if (v && typeof v === 'object') return Object.fromEntries(Object.entries(v).map(([k, x]) => [k, polishTypo(x, k)])) as T;
  return v;
};
