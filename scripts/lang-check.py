"""PL/EN linking audit over the built site: html lang, canonical, hreflang pairs and return links,
x-default, language switch target, links in the wrong language and sitemap alternates.
Usage: python3 scripts/lang-check.py dist"""
import glob, os, re, sys
from html.parser import HTMLParser

D = sys.argv[1]
SITE = 'https://maciejzieciak.com'

class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.alts = {}; self.canon = None; self.lang = None; self.links = []; self.stack = []; self.switch = []
    def handle_starttag(self, tag, a):
        a = dict(a)
        if tag == 'html': self.lang = a.get('lang')
        if tag == 'link' and a.get('rel') == 'alternate' and a.get('hreflang'): self.alts[a['hreflang']] = a['href']
        if tag == 'link' and a.get('rel') == 'canonical': self.canon = a['href']
        if tag == 'a' and a.get('href'):
            self.links.append((a['href'], a.get('hreflang'), a.get('lang'), a.get('class', '')))

def path_of(f):
    r = '/' + os.path.relpath(f, D).replace(os.sep, '/')
    return r[:-len('index.html')] if r.endswith('index.html') else r

pages = {}
for f in glob.glob(f'{D}/**/index.html', recursive=True):
    p = P(); p.feed(open(f, encoding='utf-8').read()); pages[path_of(f)] = p
is_en = lambda u: u.startswith('/en/') or u == '/en'
issues = []
for path, p in sorted(pages.items()):
    if path.startswith('/404'): continue
    want_lang = 'en' if is_en(path) else 'pl'
    if not (p.lang or '').startswith(want_lang): issues.append((path, f'html lang={p.lang}'))
    if p.canon != SITE + path: issues.append((path, f'canonical {p.canon}'))
    pl, en, xd = p.alts.get('pl'), p.alts.get('en'), p.alts.get('x-default')
    if not (pl and en and xd): issues.append((path, f'missing hreflang {sorted(p.alts)}')); continue
    self_alt = pl if want_lang == 'pl' else en
    other = (en if want_lang == 'pl' else pl).replace(SITE, '')
    if self_alt != SITE + path: issues.append((path, f'hreflang self {self_alt}'))
    if other not in pages: issues.append((path, f'hreflang target missing {other}'))
    else:
        q = pages[other]
        back = (q.alts.get('pl') if want_lang == 'pl' else q.alts.get('en'))
        if back != SITE + path: issues.append((path, f'no return link from {other} (points to {back})'))
    if xd != pl: issues.append((path, f'x-default {xd} != pl'))
    # internal links in the wrong language (language switch and hreflang-tagged links excepted)
    for href, hl, la, cls in p.links:
        if not href.startswith('/') or href.startswith('//'): continue
        h = href.split('#')[0].split('?')[0]
        if h in ('', '/favicon.svg') or h.endswith(('.xml', '.txt', '.png', '.json', '.svg', '.woff2')): continue
        if hl or la: continue  # the language switch is marked with hreflang/lang
        if is_en(h) != is_en(path):
            issues.append((path, f'cross-language link {href}'))
    # the language switch must go to the equivalent page, not the other home page
    sw = [href for href, hl, la, cls in p.links if (hl or la) and href.startswith('/')]
    for s in sw:
        h = s.split('#')[0]
        if h != other and not (h in ('/', '/en/') and other in ('/', '/en/')):
            issues.append((path, f'language switch -> {s}, expected {other}'))
    if not sw: issues.append((path, 'no language switch link found'))
# sitemap alternates match the pages
sm = open(f'{D}/sitemap-0.xml', encoding='utf-8').read()
for block in re.findall(r'<url>(.*?)</url>', sm, re.S):
    loc = re.search(r'<loc>(.*?)</loc>', block).group(1).replace(SITE, '')
    alts = dict(re.findall(r'hreflang="([^"]+)" href="([^"]+)"', block))
    p = pages.get(loc)
    if not p: issues.append((loc, 'in sitemap but no page')); continue
    for k in ('pl', 'en'):
        if alts.get(k) != p.alts.get(k): issues.append((loc, f'sitemap {k} {alts.get(k)} != page {p.alts.get(k)}'))
print('pages checked:', len([x for x in pages if not x.startswith('/404')]))
print('issues:', len(issues))
for i in issues[:80]: print(' ', i)
