#!/usr/bin/env python3
"""Technical SEO self-check of the built site.

Run after `npm run build`:  python3 scripts/seo-audit.py dist
Checks canonical, hreflang reciprocity and x-default, title/description length,
one H1, heading order, JSON-LD parsing and references, internal links and anchors,
image alt text and og:image on every page. Pages marked noindex (404) are expected
to have no canonical/hreflang."""
import os, re, json, sys, html
from html.parser import HTMLParser
ROOT = sys.argv[1]
SITE = 'https://maciejzieciak.com'
pages = {}
for dp, dn, fn in os.walk(ROOT):
    for f in fn:
        if f.endswith('.html'):
            p = os.path.join(dp, f); url = '/' + os.path.relpath(p, ROOT).replace('index.html', '').replace(os.sep, '/')
            url = url.replace('//', '/')
            pages[url] = open(p, encoding='utf-8').read()

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.links=[]; s.meta={}; s.alts=[]; s.h=[]; s.cur=None; s.title=''; s.intitle=False; s.ld=[]; s.inld=False; s.buf=''; s.a=[]; s.imgs=[]; s.lang=None; s.ids=set()
    def handle_starttag(s, t, a):
        a = dict(a)
        if 'id' in a: s.ids.add(a['id'])
        if t == 'html': s.lang = a.get('lang')
        if t == 'link': s.links.append(a)
        if t == 'meta': s.meta[a.get('name') or a.get('property') or a.get('charset') or '?'] = a.get('content')
        if t == 'title': s.intitle = True
        if t in ('h1','h2','h3','h4'): s.cur=[t,'']
        if t == 'script' and a.get('type') == 'application/ld+json': s.inld=True; s.buf=''
        if t == 'a' and 'href' in a: s.a.append(a['href'])
        if t == 'img': s.imgs.append(a)
    def handle_endtag(s, t):
        if t == 'title': s.intitle = False
        if s.cur and t == s.cur[0]: s.h.append((s.cur[0], ' '.join(s.cur[1].split()))); s.cur=None
        if t == 'script' and s.inld: s.inld=False; s.ld.append(s.buf)
    def handle_data(s, d):
        if s.intitle: s.title += d
        if s.cur: s.cur[1] += d
        if s.inld: s.buf += d

issues = []
info = {}
canon = {}
alts = {}
for url, src in sorted(pages.items()):
    p = P(); p.feed(src)
    t = html.unescape(p.title).strip(); d = p.meta.get('description') or ''
    c = [l['href'] for l in p.links if l.get('rel') == 'canonical']
    hl = {l['hreflang']: l['href'] for l in p.links if l.get('rel') == 'alternate' and l.get('hreflang')}
    canon[url] = c[0] if c else None; alts[url] = hl
    h1 = [x for x in p.h if x[0]=='h1']
    info[url] = dict(title=t, tl=len(t), dl=len(d), h1=h1, lang=p.lang, robots=p.meta.get('robots'), og=p.meta.get('og:image'), ogt=p.meta.get('og:title'), tw=p.meta.get('twitter:card'))
    if not c: issues.append((url, 'no canonical'))
    elif c[0] != SITE + url: issues.append((url, f'canonical {c[0]} != self'))
    if len(h1) != 1: issues.append((url, f'h1 count {len(h1)}'))
    if not (30 <= len(t) <= 65): issues.append((url, f'title length {len(t)}: {t}'))
    if not (70 <= len(d) <= 165): issues.append((url, f'description length {len(d)}'))
    if ' ' in t or ' ' in d: issues.append((url, 'nbsp in title/description'))
    if not p.meta.get('og:image'): issues.append((url, 'no og:image'))
    # heading order
    lv = [int(x[0][1]) for x in p.h]
    for a_, b_ in zip(lv, lv[1:]):
        if b_ > a_ + 1: issues.append((url, f'heading skip h{a_}->h{b_}')); break
    # JSON-LD
    for raw in p.ld:
        try: j = json.loads(raw)
        except Exception as e: issues.append((url, f'JSON-LD parse error {e}')); continue
        g = j.get('@graph', [j])
        types = [x.get('@type') for x in g]
        info[url]['ld'] = types
        ids = {x.get('@id') for x in g if x.get('@id')}
        # referenced ids
        refs = set(re.findall(r'"@id":\s*"([^"]+)"', raw))
        for x in g:
            for k, v in x.items():
                if isinstance(v, dict) and set(v) == {'@id'} and v['@id'] not in ids and not v['@id'].startswith(SITE + '/#') :
                    issues.append((url, f'LD ref {k} -> {v["@id"]} not defined on page'))
            if x.get('@type') == 'FAQPage':
                for q in x.get('mainEntity', []):
                    if not q.get('acceptedAnswer', {}).get('text'): issues.append((url, 'FAQ answer missing'))
            if x.get('@type') == 'BreadcrumbList':
                for i, it in enumerate(x.get('itemListElement', [])):
                    if it.get('position') != i + 1: issues.append((url, 'breadcrumb position'))
            if x.get('@type') == 'Person':
                info[url]['person'] = {k: x.get(k) for k in ('name','jobTitle','sameAs','image','worksFor','knowsAbout','url')}
            if x.get('@type') == 'ProfessionalService':
                info[url]['ps'] = {k: x.get(k) for k in ('name','areaServed','address','priceRange','image','telephone','email','url','founder')}
    # internal links
    for h in p.a:
        if h.startswith('http') and not h.startswith(SITE): continue
        if h.startswith(('mailto:','tel:')): continue
        path, _, frag = h.partition('#')
        if path.startswith(SITE): path = path[len(SITE):]
        if not path: target = url
        elif path.startswith('/'): target = path
        else: continue
        if target not in pages: issues.append((url, f'broken link {h}'))
        elif frag:
            tp = P(); tp.feed(pages[target])
            if frag not in tp.ids: issues.append((url, f'missing anchor {h}'))
    for im in p.imgs:
        if 'alt' not in im: issues.append((url, f'img without alt {im.get("src")}'))

# hreflang reciprocity
for url, hl in alts.items():
    for lang, href in hl.items():
        tgt = href.replace(SITE, '')
        if tgt not in alts: issues.append((url, f'hreflang {lang} -> missing page {href}')); continue
        back = alts[tgt]
        if SITE + url not in back.values(): issues.append((url, f'hreflang {lang} not reciprocal from {tgt}'))
    if hl and 'x-default' not in hl: issues.append((url, 'no x-default'))
    if not hl: issues.append((url, 'no hreflang'))

for u, i in info.items():
    print(u, '|', i['tl'], i['title'][:70], '| desc', i['dl'], '| lang', i['lang'], '| LD', i.get('ld'), '| robots', i['robots'])
print()
first = next(iter(info.values()))
for u in ('/', '/en/'):
    print(u, 'PERSON', json.dumps(info[u].get('person'), ensure_ascii=False)[:600])
    print(u, 'PS', json.dumps(info[u].get('ps'), ensure_ascii=False)[:600])
print()
seen=set()
for u, m in issues:
    print('ISSUE', u, '|', m)
print(len(issues), 'issues')
