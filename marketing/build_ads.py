#!/usr/bin/env python3
"""Ad copy source of truth + validator + Google Ads Editor CSV export.

Run:  python3 marketing/build_ads.py
It fails loudly if any asset breaks Google Ads limits (headline 30, description 90,
path 15, sitelink 25/35/35, callout 25, snippet value 25) or policy basics
(no '!' in headlines, no duplicate headlines).
"""
import csv, os, sys

SITE = 'https://maciejzieciak.com'
OUT = os.path.join(os.path.dirname(__file__), 'google-ads')

# ---------------------------------------------------------------------------
# Ad groups: one per service landing page (+ a general consultant group).
# Keywords are proposals: check volumes/CPC in Keyword Planner before launch.
# ---------------------------------------------------------------------------
PL = {
  'campaign': 'PL | Search | Technical SEO',
  'groups': [
    dict(name='Konsultant Technical SEO', url='/', path=('konsultant', 'technical-seo'),
      kw=['konsultant seo', 'konsultant technical seo', 'specjalista technical seo', 'ekspert seo', 'freelancer seo', 'konsultant seo b2b'],
      h=['Konsultant Technical SEO', 'Technical SEO i AI search', '9 lat doświadczenia w SEO', 'Doświadczenie enterprise',
         'Bezpośrednio z ekspertem', 'Bez juniora z agencji', 'Bezpłatna konsultacja 30 min', 'Duże serwisy i e-commerce',
         'Widoczność w Google i AI', 'Gotowe zadania dla devów', 'Priorytety według wpływu', 'Audyty, migracje, AI search',
         'Umów bezpłatną rozmowę', 'Konsultant SEO po polsku i EN', 'SEO, które da się wdrożyć'],
      d=['Technical SEO i AI search dla dużych serwisów, sklepów i marek enterprise. 9 lat w SEO.',
         'Pracujesz bezpośrednio z konsultantem, nie z juniorem z agencji. Umów bezpłatną rozmowę.',
         'Na 30-min konsultacji przejrzę Twoją stronę i wskażę 3 rzeczy do poprawy. Bez zobowiązań.',
         'Audyty, migracje, SEO e-commerce i widoczność w ChatGPT. Zadania gotowe dla Twoich devów.']),
    dict(name='Audyt Technical SEO', url='/uslugi/audyt-technical-seo/', path=('audyt', 'technical-seo'),
      kw=['audyt seo', 'audyt techniczny seo', 'audyt technical seo', 'audyt seo strony', 'audyt seo sklepu internetowego',
          'audyt seo dużego serwisu', 'analiza logów serwera seo', 'audyt indeksacji'],
      h=['Audyt Technical SEO', 'Audyt SEO dużego serwisu', 'Audyt techniczny SEO', 'Spada ruch? Sprawdźmy czemu',
         'Gotowe zadania dla devów', 'Priorytety według wpływu', 'Bez 80-stronicowych PDF-ów', 'Analiza logów i renderingu',
         'Crawl, indeksacja, rendering', 'Audyt sklepu i serwisu JS', '9 lat doświadczenia w SEO', 'Doświadczenie enterprise',
         'Bezpłatna konsultacja 30 min', 'Audyt w 2–3 tygodnie', 'Umów bezpłatną rozmowę'],
      d=['Audyt Technical SEO z priorytetami według wpływu na ruch i gotowymi zadaniami dla devów.',
         'Crawl, rendering JavaScriptu, indeksacja, logi serwera i Core Web Vitals w jednym audycie.',
         'Bezpłatna 30-min konsultacja: przejrzę stronę i wskażę 3 rzeczy, które warto poprawić.',
         'Pracujesz bezpośrednio z konsultantem z 9-letnim doświadczeniem. Umów rozmowę już dziś.']),
    dict(name='AI Search / LLM', url='/uslugi/widocznosc-w-ai-search/', path=('ai-search', 'chatgpt'),
      kw=['seo ai', 'seo pod ai', 'widoczność w chatgpt', 'pozycjonowanie w chatgpt', 'geo seo', 'seo pod ai overviews',
          'seo pod llm', 'optymalizacja pod chatgpt', 'widoczność w ai search'],
      h=['Widoczność w ChatGPT', 'SEO pod AI search', 'Bądź w odpowiedziach AI', 'AI Overviews i Perplexity',
         'Czy boty AI widzą stronę?', 'Audyt dostępu botów AI', 'Encje i dane strukturalne', 'Monitoring cytowań w AI',
         'Konsultant AI Search', 'Technical SEO pod LLM', 'Bez obietnic bez pokrycia', '9 lat doświadczenia w SEO',
         'Bezpłatna konsultacja 30 min', 'GEO: SEO dla modeli AI', 'Umów bezpłatną rozmowę'],
      d=['Sprawdzam, czy ChatGPT, Perplexity i AI Overviews widzą Twoją stronę i ją cytują.',
         'Audyt botów AI, rendering bez JavaScriptu, encje i schema.org oraz monitoring cytowań.',
         'Bez gwarancji „1. miejsca w ChatGPT”. Usuwam bariery techniczne i mierzę realne postępy.',
         'Bezpłatna 30-min konsultacja z konsultantem Technical SEO i AI search. Umów rozmowę.']),
    dict(name='Duże serwisy / programmatic', url='/uslugi/seo-duzych-serwisow/', path=('duze-serwisy', 'seo'),
      kw=['seo dużego serwisu', 'crawl budget', 'optymalizacja crawl budget', 'programmatic seo', 'seo portalu',
          'nawigacja fasetowa seo', 'indeksacja dużego serwisu', 'seo marketplace'],
      h=['SEO dużych serwisów', 'Crawl budget pod kontrolą', 'Programmatic SEO', 'Setki tysięcy URL-i',
         'Nawigacja fasetowa a SEO', 'Kontrola indeksacji', 'Audyt szablonów stron', 'Doświadczenie: 1,1 mln stron',
         'Analiza logów serwera', 'SEO portali i marketplace', '9 lat doświadczenia w SEO', 'Bezpłatna konsultacja 30 min',
         'Jedna poprawka, tysiące stron', 'Konsultant Technical SEO', 'Umów bezpłatną rozmowę'],
      d=['SEO dla serwisów z setkami tysięcy URL-i: crawl budget, filtry, szablony i indeksacja.',
         'Rozwijałem serwis do ponad 1,1 mln podstron i 115 tys. wizyt organicznych miesięcznie.',
         'Analiza logów serwera i zasady indeksacji spisane jako gotowe zadania dla zespołu dev.',
         'Bezpłatna 30-min konsultacja: wskażę, gdzie Twój serwis traci ruch. Umów rozmowę.']),
    dict(name='Enterprise / międzynarodowe', url='/uslugi/seo-enterprise-miedzynarodowe/', path=('enterprise', 'hreflang'),
      kw=['seo międzynarodowe', 'audyt hreflang', 'hreflang', 'seo wielojęzycznej strony', 'seo aem',
          'adobe experience manager seo', 'seo enterprise', 'konsultant seo enterprise'],
      h=['SEO międzynarodowe', 'Audyt hreflang', 'SEO dla AEM', 'SEO enterprise', 'Wiele rynków, jedna marka',
         'SEO wielu wersji językowych', 'Doświadczenie enterprise', 'Standardy SEO dla rynków', 'SEO w procesie wydań',
         'Konsultant SEO po polsku i EN', '9 lat doświadczenia w SEO', 'Bezpłatna konsultacja 30 min',
         'Współpraca z Twoim zespołem', 'Adobe Experience Manager', 'Umów bezpłatną rozmowę'],
      d=['Hreflang, wersje językowe i SEO dla Adobe Experience Manager w firmach enterprise.',
         'Jedne standardy SEO dla wszystkich rynków i agencji, wpisane w proces wydań.',
         'Pracuję z zespołami dev i agencjami w wielu krajach. Po polsku albo po angielsku.',
         'Bezpłatna 30-min konsultacja z konsultantem z doświadczeniem enterprise. Umów rozmowę.']),
    dict(name='Migracje', url='/uslugi/migracja-strony-seo/', path=('migracja', 'seo'),
      kw=['migracja strony seo', 'migracja sklepu seo', 'zmiana domeny seo', 'migracja seo', 'relaunch strony seo',
          'spadek ruchu po migracji', 'przekierowania 301 migracja', 'zmiana platformy sklepu seo'],
      h=['Migracja strony bez spadków', 'Migracja SEO', 'Zmiana domeny bez utraty', 'Nowa strona, ten sam ruch',
         'Mapa przekierowań 301', 'Testy przed startem', 'Monitoring po wdrożeniu', 'Zmiana CMS lub platformy',
         'Spadek ruchu po migracji?', 'Relaunch strony i SEO', '9 lat doświadczenia w SEO', 'Bezpłatna konsultacja 30 min',
         'Konsultant Technical SEO', 'Zaplanuj migrację z SEO', 'Umów bezpłatną rozmowę'],
      d=['Zmiana CMS, domeny albo adresów URL bez utraty ruchu. Plan, testy i monitoring.',
         'Mapa przekierowań 301, testy środowiska testowego i checklista dnia startu.',
         'Ruch spadł po migracji? Znajdę brakujące przekierowania i błędy, które zabrały ruch.',
         'Najlepiej włączyć SEO przed developmentem. Bezpłatna 30-min konsultacja. Umów rozmowę.']),
    dict(name='E-commerce SEO', url='/uslugi/seo-ecommerce/', path=('e-commerce', 'seo'),
      kw=['seo e-commerce', 'seo sklepu internetowego', 'pozycjonowanie sklepu internetowego', 'seo prestashop',
          'seo magento', 'seo kategorii sklepu', 'audyt seo sklepu', 'seo sklepu shoper'],
      h=['SEO dla e-commerce', 'SEO sklepu internetowego', 'Więcej sprzedaży z Google', 'Kategorie, filtry, produkty',
         'SEO PrestaShop i Magento', 'Filtry bez marnowania budżetu', 'Priorytety według przychodu', 'Karty produktów pod SEO',
         'Audyt SEO sklepu', 'Rynki PL i zagraniczne', '9 lat doświadczenia w SEO', 'Bezpłatna konsultacja 30 min',
         'Konsultant Technical SEO', 'Shoper, RedCart, WordPress', 'Umów bezpłatną rozmowę'],
      d=['SEO sklepu: architektura kategorii, filtry, karty produktów i kontrola indeksacji.',
         'PrestaShop, Magento, WordPress, Shoper, RedCart. Priorytety według przychodu.',
         'Więcej sprzedaży z Google, nie tylko więcej wejść. Najpierw kategorie, które zarabiają.',
         'Bezpłatna 30-min konsultacja: wskażę 3 rzeczy do poprawy w Twoim sklepie. Umów rozmowę.']),
  ],
  'sitelinks': [
    ('Audyt Technical SEO', 'Priorytety według wpływu', 'Gotowe zadania dla devów', '/uslugi/audyt-technical-seo/'),
    ('Widoczność w AI search', 'ChatGPT, Perplexity, Overviews', 'Audyt dostępu botów AI', '/uslugi/widocznosc-w-ai-search/'),
    ('SEO dla e-commerce', 'Kategorie, filtry, produkty', 'Priorytety według przychodu', '/uslugi/seo-ecommerce/'),
    ('Migracja bez spadków', 'Mapa przekierowań 301', 'Testy i monitoring po starcie', '/uslugi/migracja-strony-seo/'),
    ('Bezpłatna konsultacja', '30 minut, online', 'Bez zobowiązań', '/#kontakt'),
    ('Doświadczenie', '9 lat w SEO', 'Agencja, konsulting, enterprise', '/#doswiadczenie'),
  ],
  'callouts': ['9 lat doświadczenia', 'Bezpłatna konsultacja', 'Konsultacja online', 'Bezpośrednio z ekspertem',
               'Zadania dla developerów', 'Po polsku i po angielsku', 'Doświadczenie enterprise', 'Bez długich umów'],
  'snippet': ('Usługi', ['Audyt Technical SEO', 'AI search', 'SEO e-commerce', 'Migracje', 'SEO międzynarodowe', 'Duże serwisy']),
  'negatives': ['praca', 'oferty pracy', 'zatrudnię', 'staż', 'praktyki', 'kurs', 'szkolenie', 'studia', 'certyfikat',
                'za darmo', 'darmowy', 'darmowe', 'samodzielnie', 'jak zrobić', 'poradnik', 'co to jest', 'definicja',
                'wikipedia', 'pdf', 'wtyczka', 'plugin', 'szablon', 'forum', 'opinie o pracy', 'zarobki', 'ile zarabia'],
}

EN = {
  'campaign': 'EN | Search | Technical SEO',
  'groups': [
    dict(name='Technical SEO consultant', url='/en/', path=('consultant', 'technical-seo'),
      kw=['technical seo consultant', 'seo consultant', 'freelance technical seo', 'technical seo expert',
          'enterprise seo consultant', 'b2b seo consultant'],
      h=['Technical SEO Consultant', 'Technical SEO & AI Search', '9 Years in SEO', 'Enterprise Experience',
         'Work With a Senior Directly', 'No Juniors, No Middlemen', 'Free 30-Minute Consultation', 'Large Sites & E-commerce',
         'Visible in Google and AI', 'Tickets Your Devs Can Ship', 'Priorities Ranked by Impact', 'Audits, Migrations, AI',
         'Book a Free Call', 'Working in English & Polish', 'SEO Your Team Can Ship'],
      d=['Technical SEO and AI search for large websites, online stores and enterprise brands.',
         'Work directly with a senior consultant, not a junior at an agency. Book a free call.',
         'On a free 30-minute call I review your site and point out the 3 things to fix first.',
         'Audits, migrations, e-commerce SEO and ChatGPT visibility. Tickets your devs can ship.']),
    dict(name='Technical SEO audit', url='/en/services/technical-seo-audit/', path=('services', 'seo-audit'),
      kw=['technical seo audit', 'seo audit service', 'technical seo audit service', 'seo audit large website',
          'log file analysis seo', 'javascript seo audit', 'indexation audit', 'ecommerce seo audit'],
      h=['Technical SEO Audit', 'SEO Audit for Large Sites', 'Traffic Dropping? Find Out', 'Tickets Your Devs Can Ship',
         'Priorities Ranked by Impact', 'No 80-Page PDF Reports', 'Log File & Rendering Audit', 'Crawl, Index, Render',
         'JavaScript SEO Audit', '9 Years in SEO', 'Enterprise Experience', 'Free 30-Minute Consultation',
         'Audit in 2–3 Weeks', 'Technical SEO Consultant', 'Book a Free Call'],
      d=['Technical SEO audit with issues ranked by traffic impact and ready-to-ship dev tickets.',
         'Crawling, JavaScript rendering, indexation, server logs and Core Web Vitals in one audit.',
         'Free 30-minute consultation: I review your site and point out the 3 things to fix first.',
         'Work directly with a consultant with 9 years of SEO experience. Book your call today.']),
    dict(name='AI search / LLM', url='/en/services/ai-search-visibility/', path=('services', 'ai-search'),
      kw=['ai search optimization', 'chatgpt seo', 'generative engine optimization', 'llm seo', 'ai overviews seo',
          'seo for chatgpt', 'perplexity seo', 'geo seo'],
      h=['Get Cited in ChatGPT', 'AI Search Optimisation', 'Be in the AI Answer', 'AI Overviews & Perplexity',
         'Can AI Bots See Your Site?', 'AI Crawler Access Audit', 'Entities & Structured Data', 'AI Citation Tracking',
         'AI Search Consultant', 'Technical SEO for LLMs', 'No Empty Promises', '9 Years in SEO',
         'Free 30-Minute Consultation', 'GEO: SEO for AI Models', 'Book a Free Call'],
      d=['I check whether ChatGPT, Perplexity and AI Overviews can access your site and cite it.',
         'AI crawler audit, no-JS rendering, entities and schema.org, plus citation tracking.',
         'No guaranteed “#1 in ChatGPT”. I remove technical barriers and measure real progress.',
         'Free 30-minute call with a technical SEO and AI search consultant. Book yours today.']),
    dict(name='Large sites / programmatic', url='/en/services/large-website-seo/', path=('services', 'large-sites'),
      kw=['crawl budget optimization', 'programmatic seo consultant', 'enterprise website seo', 'faceted navigation seo',
          'seo for large websites', 'marketplace seo', 'indexation management'],
      h=['SEO for Large Websites', 'Crawl Budget Under Control', 'Programmatic SEO', 'Hundreds of Thousands of URLs',
         'Faceted Navigation SEO', 'Indexation Control', 'Template-Level SEO Audit', 'Grew a Site to 1.1M Pages',
         'Server Log Analysis', 'Marketplace & Directory SEO', '9 Years in SEO', 'Free 30-Minute Consultation',
         'One Fix, Thousands of Pages', 'Technical SEO Consultant', 'Book a Free Call'],
      d=['SEO for sites with 100k+ URLs: crawl budget, filters, templates and indexation.',
         'I grew a site past 1.1M pages and 115k monthly organic visits. I know where scale breaks.',
         'Log file analysis and indexation rules, written up as ready-to-ship tickets for your devs.',
         'Free 30-minute consultation: I show where your site is losing traffic. Book a call.']),
    dict(name='Enterprise / international', url='/en/services/enterprise-international-seo/', path=('services', 'international'),
      kw=['international seo consultant', 'hreflang audit', 'multilingual seo', 'aem seo', 'adobe experience manager seo',
          'enterprise seo', 'multi market seo'],
      h=['International SEO', 'Hreflang Audit', 'SEO for AEM', 'Enterprise SEO', 'Many Markets, One Brand',
         'Multilingual SEO', 'Enterprise Experience', 'SEO Standards for Markets', 'SEO in Your Release Process',
         'English & Polish', '9 Years in SEO', 'Free 30-Minute Consultation', 'Works With Your Dev Team',
         'Adobe Experience Manager', 'Book a Free Call'],
      d=['Hreflang, language versions and Adobe Experience Manager SEO for enterprise brands.',
         'One set of SEO standards across markets and agencies, built into releases and reviews.',
         'I work with dev teams and agencies across countries. Communication in English or Polish.',
         'Free 30-minute call with a consultant with enterprise experience. Book yours today.']),
    dict(name='Migrations', url='/en/services/website-migration-seo/', path=('services', 'migration'),
      kw=['website migration seo', 'seo migration consultant', 'domain migration seo', 'site migration seo',
          'replatforming seo', 'traffic drop after migration', 'redirect mapping'],
      h=['Website Migration SEO', 'Migrate Without Losing SEO', 'Change Domain, Keep Traffic', 'New Site, Same Traffic',
         '301 Redirect Mapping', 'Pre-Launch SEO Testing', 'Post-Launch Monitoring', 'CMS & Platform Changes',
         'Traffic Drop After Launch?', 'Relaunch With SEO in Mind', '9 Years in SEO', 'Free 30-Minute Consultation',
         'Technical SEO Consultant', 'Plan Your Migration', 'Book a Free Call'],
      d=['Change CMS, domain or URL structure without losing organic traffic. Plan, test, monitor.',
         '301 redirect map, staging crawl and a launch-day checklist in one tried process.',
         'Traffic dropped after a migration? I find the missing redirects and errors behind it.',
         'Bring SEO in before development starts. Free 30-minute consultation. Book a call.']),
    dict(name='E-commerce SEO', url='/en/services/ecommerce-seo/', path=('services', 'ecommerce'),
      kw=['ecommerce seo consultant', 'ecommerce seo', 'online store seo', 'magento seo', 'prestashop seo',
          'category page seo', 'ecommerce seo audit'],
      h=['E-commerce SEO', 'SEO for Online Stores', 'More Sales From Google', 'Categories, Filters, Products',
         'Magento & PrestaShop SEO', 'Filters Without Waste', 'Priorities by Revenue', 'Product Page SEO',
         'E-commerce SEO Audit', 'Domestic & Cross-Border', '9 Years in SEO', 'Free 30-Minute Consultation',
         'Technical SEO Consultant', 'Category Architecture', 'Book a Free Call'],
      d=['Store SEO: category architecture, filters, product pages and indexation control.',
         'PrestaShop, Magento, WordPress and custom platforms. Priorities ordered by revenue.',
         'More sales from search, not just more visits. Categories that make money come first.',
         'Free 30-minute consultation: I point out 3 things to fix in your store. Book a call.']),
  ],
  'sitelinks': [
    ('Technical SEO Audit', 'Issues ranked by impact', 'Ready-to-ship dev tickets', '/en/services/technical-seo-audit/'),
    ('AI Search Visibility', 'ChatGPT, Perplexity, Overviews', 'AI crawler access audit', '/en/services/ai-search-visibility/'),
    ('E-commerce SEO', 'Categories, filters, products', 'Priorities ordered by revenue', '/en/services/ecommerce-seo/'),
    ('Website Migrations', '301 redirect mapping', 'Testing and post-launch checks', '/en/services/website-migration-seo/'),
    ('Free Consultation', '30 minutes, online', 'No strings attached', '/en/#contact'),
    ('Experience', '9 years in SEO', 'Agency, consulting, enterprise', '/en/#experience'),
  ],
  'callouts': ['9 Years in SEO', 'Free Consultation', 'Online Consultation', 'Work With a Senior', 'Dev-Ready Tickets',
               'English & Polish', 'Enterprise Experience', 'No Long Contracts'],
  'snippet': ('Services', ['Technical SEO Audit', 'AI Search', 'E-commerce SEO', 'Site Migrations', 'International SEO', 'Large Websites']),
  'negatives': ['jobs', 'job', 'career', 'careers', 'salary', 'hiring', 'internship', 'course', 'training', 'certification',
                'free', 'tutorial', 'how to', 'guide', 'checklist pdf', 'what is', 'definition', 'wiki', 'reddit',
                'plugin', 'template', 'tool free', 'udemy', 'youtube'],
}

# ---------------------------------------------------------------------------
LIM = dict(h=30, d=90, path=15, sl=25, sld=35, co=25, sv=25)
errors = []

def check(kind, text, where):
    if len(text) > LIM[kind]:
        errors.append(f'{where}: "{text}" = {len(text)} > {LIM[kind]}')
    if kind == 'h' and '!' in text:
        errors.append(f'{where}: "!" is not allowed in headlines')

for lang, cfg in (('pl', PL), ('en', EN)):
    for g in cfg['groups']:
        w = f"{lang}/{g['name']}"
        if len(g['h']) != 15: errors.append(f'{w}: needs 15 headlines, has {len(g["h"])}')
        if len(g['d']) != 4: errors.append(f'{w}: needs 4 descriptions, has {len(g["d"])}')
        if len({x.lower() for x in g['h']}) != len(g['h']): errors.append(f'{w}: duplicate headline')
        for x in g['h']: check('h', x, w)
        for x in g['d']: check('d', x, w)
        for x in g['path']: check('path', x, w)
    for t, d1, d2, _ in cfg['sitelinks']:
        check('sl', t, f'{lang}/sitelink'); check('sld', d1, f'{lang}/sitelink'); check('sld', d2, f'{lang}/sitelink')
    for c in cfg['callouts']: check('co', c, f'{lang}/callout')
    for v in cfg['snippet'][1]: check('sv', v, f'{lang}/snippet')

if errors:
    print('\n'.join(errors)); sys.exit(1)

# ---------------------------------------------------------------------------
# Google Ads Editor CSV export (File → Import → From file).
# ---------------------------------------------------------------------------
os.makedirs(OUT, exist_ok=True)
for lang, cfg in (('pl', PL), ('en', EN)):
    camp = cfg['campaign']
    with open(f'{OUT}/{lang}-ads.csv', 'w', newline='', encoding='utf-8') as f:
        cols = ['Campaign', 'Ad Group', 'Ad type'] + [f'Headline {i}' for i in range(1, 16)] + \
               [f'Description {i}' for i in range(1, 5)] + ['Path 1', 'Path 2', 'Final URL']
        wr = csv.writer(f); wr.writerow(cols)
        for g in cfg['groups']:
            wr.writerow([camp, g['name'], 'Responsive search ad'] + g['h'] + g['d'] + list(g['path']) + [SITE + g['url']])
    with open(f'{OUT}/{lang}-keywords.csv', 'w', newline='', encoding='utf-8') as f:
        wr = csv.writer(f); wr.writerow(['Campaign', 'Ad Group', 'Keyword', 'Criterion Type'])
        for g in cfg['groups']:
            for k in g['kw']:
                wr.writerow([camp, g['name'], k, 'Phrase'])
                wr.writerow([camp, g['name'], k, 'Exact'])
    with open(f'{OUT}/{lang}-negatives.csv', 'w', newline='', encoding='utf-8') as f:
        wr = csv.writer(f); wr.writerow(['Campaign', 'Keyword', 'Criterion Type'])
        for k in cfg['negatives']:
            wr.writerow([camp, k, 'Negative Phrase'])
    with open(f'{OUT}/{lang}-sitelinks.csv', 'w', newline='', encoding='utf-8') as f:
        wr = csv.writer(f); wr.writerow(['Campaign', 'Link Text', 'Description Line 1', 'Description Line 2', 'Final URL'])
        for t, d1, d2, u in cfg['sitelinks']:
            wr.writerow([camp, t, d1, d2, SITE + u])
    with open(f'{OUT}/{lang}-callouts.csv', 'w', newline='', encoding='utf-8') as f:
        wr = csv.writer(f); wr.writerow(['Campaign', 'Callout text'])
        for c in cfg['callouts']: wr.writerow([camp, c])
    with open(f'{OUT}/{lang}-snippets.csv', 'w', newline='', encoding='utf-8') as f:
        wr = csv.writer(f); wr.writerow(['Campaign', 'Header', 'Values'])
        wr.writerow([camp, cfg['snippet'][0], ';'.join(cfg['snippet'][1])])

n_ads = sum(len(c['groups']) for c in (PL, EN))
n_kw = sum(len(g['kw']) * 2 for c in (PL, EN) for g in c['groups'])
print(f'OK: {n_ads} ad groups / RSAs, {n_kw} keywords (phrase+exact), all assets within limits.')
