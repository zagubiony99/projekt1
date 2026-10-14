// Polish typography: a one-letter word (a, i, o, u, w, z) must not be left at the end of a line,
// so it is glued to the next word with a non-breaking space. Applied to all Polish copy at build time.
const glue = (s: string) => s.replace(/(?<![^\s(„])([aiouwzAIOUWZ])[ \t\n]+/g, '$1 ');

export const polishTypo = <T>(v: T): T => {
  if (typeof v === 'string') return glue(v) as T;
  if (Array.isArray(v)) return v.map(polishTypo) as T;
  if (v && typeof v === 'object') return Object.fromEntries(Object.entries(v).map(([k, x]) => [k, polishTypo(x)])) as T;
  return v;
};
