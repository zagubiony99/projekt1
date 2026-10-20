#!/usr/bin/env python3
"""Generates .pages.yml (the Pages CMS configuration) from the field spec below.

Run:  python3 scripts/cms/build-config.py && python3 scripts/cms/check.py

Pages CMS saves ONLY the fields listed in its config (and drops empty values), so the
spec must describe every key in content/*.json. scripts/cms/check.py verifies that by
simulating a save of every content file.
"""
import os
import yaml

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')


# ---- tiny field helpers ---------------------------------------------------------
def s(name, label, desc=None, **kw):  # one-line text
    f = {'name': name, 'label': label, 'type': 'string', **kw}
    if desc: f['description'] = desc
    return f

def t(name, label, desc=None, **kw):  # multi-line text
    f = {'name': name, 'label': label, 'type': 'text', **kw}
    if desc: f['description'] = desc
    return f

def b(name, label, desc=None):
    f = {'name': name, 'label': label, 'type': 'boolean'}
    if desc: f['description'] = desc
    return f

def strings(name, label, desc=None):  # list of one-line texts
    f = {'name': name, 'label': label, 'type': 'string', 'list': True}
    if desc: f['description'] = desc
    return f

def obj(name, label, fields, desc=None):
    f = {'name': name, 'label': label, 'type': 'object', 'fields': fields}
    if desc: f['description'] = desc
    return f

def items(name, label, fields, desc=None):  # list of objects
    f = obj(name, label, fields, desc)
    f['list'] = True
    return f


# ---- site settings (content/site.json) -----------------------------------------
SITE = [
    s('name', 'Imię i nazwisko', 'Pojawia się w menu, stopce, tytułach stron i danych strukturalnych.', required=True),
    s('email', 'E-mail kontaktowy', 'Adres w stopce, formularzu i polityce prywatności.', required=True),
    s('linkedin', 'Profil LinkedIn', 'Pełny adres, np. https://www.linkedin.com/in/… Puste = ukryty. Trafia też do schema (sameAs).'),
    {'name': 'photo', 'label': 'Zdjęcie', 'type': 'image',
     'description': 'Portret: pokazuje się w sekcji Doświadczenie, przy formularzu kontaktowym i w „Dlaczego ja” na podstronach usług, trafia też do schema. Najlepiej min. 1000×1000 px, twarz w górnej części kadru. Strona sama przytnie i odchudzi plik.'},
    s('formEndpoint', 'Adres formularza (Formspree / Web3Forms)',
      'Np. https://formspree.io/f/xxxx albo https://api.web3forms.com/submit. Puste = formularz otwiera program pocztowy.'),
    s('formAccessKey', 'Klucz Web3Forms', 'Tylko dla Web3Forms. Dla Formspree zostaw puste.'),
    s('bookingUrl', 'Link do kalendarza', 'Cal.com albo Calendly. Gdy jest ustawiony, przy formularzu pojawia się „Wolisz od razu wybrać termin?”.'),
    s('gtmId', 'Google Tag Manager ID', 'Np. GTM-XXXXXXX. Puste = brak analityki, brak banera cookies.'),
]

# ---- one language of the site (content/pl.json, content/en.json) ---------------
COPY = [
    obj('meta', 'SEO strony głównej', [
        s('title', 'Tytuł (title)', 'Do 60 znaków. Widoczny w Google i na karcie przeglądarki.'),
        t('description', 'Opis (meta description)', 'Do 155 znaków. Widoczny pod tytułem w Google.'),
    ]),
    obj('hero', 'Hero (pierwszy ekran)', [
        s('pill', 'Linijka nad nagłówkiem'),
        s('titleA', 'Nagłówek, linia 1'),
        s('titleB', 'Nagłówek, linia 2 (kolorowa)'),
        t('lead', 'Tekst pod nagłówkiem'),
        s('ctaPrimary', 'Przycisk główny'),
        s('ctaSecondary', 'Link obok przycisku'),
        s('ctaNote', 'Dopisek pod przyciskiem'),
        s('trustLabel', 'Podpis przed nazwami firm'),
        obj('demo', 'Okno „Odpowiedź AI”', [
            s('app', 'Nazwa okna'),
            s('note', 'Dopisek w rogu okna'),
            s('q', 'Pytanie'),
            s('think', 'Komunikat „szukam”'),
            t('answer', 'Odpowiedź', 'Przypisy wpisuj jako [1], [2], [3]: numer = pozycja na liście źródeł.'),
            s('sourcesLabel', 'Nagłówek listy źródeł'),
            items('sources', 'Źródła', [
                s('d', 'Domena'),
                s('t', 'Tytuł strony'),
                b('you', 'To „Twoja strona”', 'Zaznacz przy jednym źródle: dostanie kolorową ramkę i plakietkę.'),
            ]),
            s('you', 'Napis na plakietce'),
        ]),
        obj('card', 'Karta „Kto widzi Twoją stronę?” (sekcja z botami)', [
            s('title', 'Tytuł karty'),
            s('url', 'Przykładowy adres'),
            s('note', 'Dopisek w rogu'),
            s('summary', 'Podsumowanie pod listą'),
            items('rows', 'Boty', [
                s('bot', 'Nazwa bota'),
                {'name': 's', 'label': 'Status', 'type': 'select',
                 'options': {'values': [{'value': 'ok', 'label': 'OK (zielony)'},
                                        {'value': 'warn', 'label': 'Uwaga (pomarańczowy)'},
                                        {'value': 'err', 'label': 'Błąd (czerwony)'}]}},
                s('t', 'Opis'),
            ]),
        ]),
    ]),
    obj('statement', 'Czarna sekcja z dużym zdaniem', [
        s('label', 'Etykieta (dla czytników ekranu)'),
        items('parts', 'Fragmenty zdania', [
            t('t', 'Tekst'),
            b('mark', 'Wyróżnij kolorem'),
        ], 'Zdanie składa się z fragmentów; wyróżniony fragment jest w gradiencie.'),
    ]),
    obj('stage', 'Sekcja „oczami botów”', [
        s('eyebrow', 'Nadtytuł'),
        s('title', 'Nagłówek'),
        t('text', 'Tekst'),
    ]),
    obj('stats', 'Liczby', [
        s('label', 'Etykieta sekcji'),
        items('items', 'Liczby', [s('v', 'Wartość', 'Np. 9 lat albo 1,1 mln. Liczba odlicza się przy przewijaniu.'), s('k', 'Opis')]),
    ]),
    obj('tools', 'Narzędzia', [
        s('label', 'Nagłówek'),
        strings('items', 'Narzędzia'),
    ]),
    obj('bands', 'Paski z wezwaniem do kontaktu', [
        obj('afterServices', 'Po usługach', [s('title', 'Nagłówek'), t('text', 'Tekst'), s('btn', 'Przycisk')]),
    ]),
    obj('compare', 'Porównanie z agencją', [
        s('label', 'Nadtytuł'),
        s('title', 'Nagłówek'),
        s('me', 'Nazwa kolumny „ja”'),
        s('them', 'Nazwa kolumny „agencja”'),
        items('rows', 'Wiersze', [s('k', 'Temat'), t('me', 'Ja'), t('them', 'Agencja')]),
    ]),
    obj('services', 'Usługi (nagłówek sekcji)', [
        s('label', 'Nadtytuł'),
        s('title', 'Nagłówek'),
        t('intro', 'Wstęp'),
    ], 'Treść kart usług edytujesz w sekcji „Usługi”.'),
    obj('experience', 'Doświadczenie', [
        s('label', 'Nadtytuł'),
        s('title', 'Nagłówek'),
        t('intro', 'Wstęp'),
        s('more', 'Link „więcej o mnie” (strona główna)'),
        s('industriesLabel', 'Nagłówek listy branż'),
        strings('industries', 'Branże'),
        items('items', 'Etapy kariery', [
            s('when', 'Lata', 'Np. 2021 — 2026 albo 2026 — obecnie.'),
            s('org', 'Firma'),
            s('role', 'Stanowisko'),
            t('desc', 'Opis'),
            b('highlight', 'Wyróżnij (kolorowa nazwa)'),
        ]),
    ]),
    obj('process', 'Proces', [
        s('label', 'Nadtytuł'),
        s('title', 'Nagłówek'),
        items('steps', 'Kroki', [s('name', 'Nazwa'), t('desc', 'Opis')]),
    ]),
    obj('engage', 'Formy współpracy', [
        s('label', 'Nadtytuł'),
        s('title', 'Nagłówek'),
        t('lead', 'Tekst pod nagłówkiem'),
        s('priceFallback', 'Tekst, gdy nie podasz ceny', 'Np. „Wycena po rozmowie”.'),
        items('models', 'Formy współpracy', [
            s('name', 'Nazwa'),
            s('kind', 'Etykieta nad nazwą', 'Np. „Jednorazowo”.'),
            s('price', 'Cena', 'Np. „od 600 zł netto”. Puste = tekst zastępczy powyżej.'),
            t('desc', 'Opis'),
            strings('points', 'Punkty'),
            s('cta', 'Przycisk'),
            s('topic', 'Temat w formularzu', 'Musi być identyczny z jednym z tematów formularza kontaktowego. Puste = żaden.'),
            b('featured', 'Wyróżnij (ciemna karta)'),
        ]),
    ]),
    obj('faq', 'FAQ', [
        s('label', 'Nadtytuł'),
        s('title', 'Nagłówek'),
        items('items', 'Pytania', [s('q', 'Pytanie'), t('a', 'Odpowiedź')]),
    ]),
    obj('contact', 'Kontakt i formularz', [
        s('label', 'Nadtytuł'),
        s('title', 'Nagłówek'),
        t('lead', 'Tekst pod nagłówkiem'),
        s('topicsLabel', 'Pytanie o temat'),
        strings('topics', 'Tematy do wyboru', 'Nie zmieniaj nazw tematów usług: podstrona usługi sama zaznacza swój temat.'),
        s('urlLabel', 'Etykieta pola „adres strony”'),
        s('urlPlaceholder', 'Podpowiedź w polu „adres strony”'),
        s('msgLabel', 'Etykieta pola „wiadomość”'),
        s('msgPlaceholder', 'Podpowiedź w polu „wiadomość”'),
        s('submit', 'Przycisk wysyłki'),
        t('note', 'Dopisek pod formularzem'),
        s('booking', 'Pytanie o kalendarz'),
        s('bookingBtn', 'Link do kalendarza'),
        s('sending', 'Napis podczas wysyłania'),
        t('success', 'Komunikat po wysłaniu'),
        s('error', 'Komunikat błędu (przed adresem e-mail)'),
        s('subject', 'Temat e-maila'),
        s('bodyTopics', 'E-mail: etykieta tematów'),
        s('bodyUrl', 'E-mail: etykieta strony'),
        s('orEmail', 'Tekst „albo napisz bezpośrednio”'),
    ]),
    obj('sticky', 'Pływający pasek na telefonie', [s('text', 'Tekst'), s('btn', 'Przycisk')]),
    obj('serviceUi', 'Podstrony usług: stałe napisy', [
        s('home', 'Okruszki: strona główna'),
        s('services', 'Okruszki: usługi'),
        s('cta', 'Przycisk główny'),
        s('seeWhat', 'Link „zobacz, co dostajesz”'),
        s('more', 'Link „dowiedz się więcej”'),
        s('yes', 'Nagłówek „dla kogo tak”'),
        s('no', 'Nagłówek „dla kogo nie”'),
        s('proofTitle', 'Nagłówek „dlaczego ja”'),
        s('faqTitle', 'Nagłówek FAQ'),
        s('other', 'Nagłówek „pozostałe usługi”'),
        s('nextTitle', 'Nagłówek „co dalej”'),
        items('next', 'Co dalej (kroki)', [s('t', 'Krok'), t('d', 'Opis')]),
    ]),
    obj('guidesUi', 'Poradniki: lista i stałe napisy', [
        s('metaTitle', 'SEO: tytuł listy poradników', 'Do 60 znaków.'),
        t('metaDescription', 'SEO: opis listy poradników', 'Do 155 znaków.'),
        s('eyebrow', 'Nadtytuł'),
        s('title', 'Nagłówek listy poradników'),
        t('lead', 'Tekst pod nagłówkiem'),
        s('toolEyebrow', 'Etykieta karty narzędzia'),
        s('toc', 'Spis treści'),
        s('updated', 'Aktualizacja'),
        s('readTime', 'Min czytania'),
        s('by', 'Autor'),
        s('read', 'Link „czytaj poradnik”'),
        s('all', 'Link „wszystkie poradniki”'),
        s('others', 'Nagłówek „inne poradniki”'),
        s('faqTitle', 'Nagłówek FAQ'),
        s('serviceTitle', 'Ramka usługi: nagłówek'),
        s('serviceCta', 'Ramka usługi: przycisk'),
    ]),
    obj('nav', 'Menu', [
        s('services', 'Usługi'), s('about', 'O mnie'), s('guides', 'Poradniki'), s('experience', 'Doświadczenie'), s('process', 'Proces'), s('faq', 'FAQ'),
        s('contact', 'Kontakt'), s('cta', 'Przycisk w menu'), s('switchLabel', 'Link do drugiej wersji językowej'),
        s('menu', 'Przycisk menu (telefon)'), s('close', 'Zamknij menu (telefon)'),
    ]),
    obj('consent', 'Baner cookies', [
        t('text', 'Tekst'), s('accept', 'Akceptuj'), s('reject', 'Odrzuć'), s('more', 'Link do polityki'), s('settings', 'Ustawienia cookies'),
    ], 'Widoczny tylko, gdy w ustawieniach jest Google Tag Manager ID.'),
    obj('privacy', 'Polityka prywatności (SEO)', [
        s('label', 'Tytuł strony'),
        t('description', 'Opis (meta description)', 'Do 155 znaków.'),
    ], 'Treść samej polityki jest w kodzie (src/components/Privacy.astro).'),
    obj('footer', 'Stopka', [s('rights', 'Prawa zastrzeżone'), s('top', 'Link „do góry”'), s('built', 'Dopisek techniczny')]),
    s('skip', 'Link „przejdź do treści” (dla klawiatury)'),
]

# ---- one language of a service page (content/services/<key>.json) --------------
SERVICE = [
    s('name', 'Nazwa usługi', 'Menu, karty, okruszki. Zmieniaj w obu językach.'),
    obj('card', 'Karta na stronie głównej', [t('desc', 'Opis na karcie'), strings('tags', 'Tagi')]),
    s('metaTitle', 'SEO: tytuł', 'Do 60 znaków.'),
    t('metaDescription', 'SEO: opis', 'Do 155 znaków.'),
    s('eyebrow', 'Nadtytuł'),
    s('title', 'Nagłówek (H1)'),
    t('lead', 'Tekst pod nagłówkiem'),
    s('painTitle', 'Nagłówek „brzmi znajomo?”'),
    strings('pains', 'Problemy klienta'),
    s('getTitle', 'Nagłówek „co dostajesz”'),
    items('gets', 'Co dostajesz', [s('t', 'Nazwa'), t('d', 'Opis')]),
    s('stepsTitle', 'Nagłówek „jak to przebiega”'),
    items('steps', 'Etapy', [s('t', 'Nazwa'), s('when', 'Kiedy'), t('d', 'Opis')]),
    s('forTitle', 'Nagłówek „dla kogo”'),
    strings('forYes', 'Dla kogo tak'),
    strings('forNo', 'Dla kogo nie'),
    t('proof', 'Dlaczego ja (doświadczenie)'),
    items('faq', 'FAQ usługi', [s('q', 'Pytanie'), t('a', 'Odpowiedź')]),
]

# ---- About page (content/about.json) --------------------------------------------
ABOUT = [
    s('metaTitle', 'SEO: tytuł', 'Do 60 znaków.'),
    t('metaDescription', 'SEO: opis', 'Do 155 znaków.'),
    s('eyebrow', 'Nadtytuł (część H1)'),
    s('title', 'Nagłówek (H1)'),
    t('lead', 'Tekst pod nagłówkiem'),
    s('ctaPrimary', 'Przycisk główny'),
    s('ctaSecondary', 'Link do usług'),
    s('storyTitle', 'Nagłówek historii'),
    {'name': 'story', 'label': 'Historia (akapity)', 'type': 'text', 'list': True},
    s('approachTitle', 'Nagłówek „jak pracuję”'),
    items('approach', 'Jak pracuję', [s('t', 'Nazwa'), t('d', 'Opis')]),
    s('kitTitle', 'Nagłówek „platformy i narzędzia”'),
    s('platformsLabel', 'Nagłówek listy platform'),
    strings('platforms', 'Platformy'),
    s('languagesLabel', 'Nagłówek listy języków'),
    strings('languages', 'Języki'),
    s('guidesTitle', 'Nagłówek sekcji poradników'),
    t('guidesLead', 'Tekst sekcji poradników'),
]

# ---- one language of a guide (content/guides/<key>.json) ----------------------------
GUIDE = [
    s('metaTitle', 'SEO: tytuł', 'Do 60 znaków.'),
    t('metaDescription', 'SEO: opis', 'Do 155 znaków.'),
    s('title', 'Tytuł (H1)'),
    t('lead', 'Wstęp'),
    items('sections', 'Rozdziały', [
        s('h', 'Nagłówek rozdziału (H2)', 'Trafia też do spisu treści.'),
        # HTML in a code editor rather than rich text: tables and code blocks survive every save
        {'name': 'body', 'label': 'Treść (HTML)', 'type': 'code', 'options': {'format': 'html'},
         'description': 'Akapity <p>, listy <ul>/<ol>, pogrubienie <strong>, linki <a href=\'/…\'>, tabele <table>.'},
    ]),
    items('faq', 'FAQ', [s('q', 'Pytanie'), t('a', 'Odpowiedź')]),
]

GUIDES = [  # key, label in the CMS menu
    ('ai-overviews', 'AI Overviews i ChatGPT: jak przygotować stronę'),
    ('ai-bots', 'Boty AI w robots.txt'),
    ('audit-cost', 'Audyt SEO: od czego zależy cena'),
    ('audit', 'Audyt techniczny: checklista'),
    ('migration', 'Migracja strony: checklista'),
    ('release', 'SEO przed wdrożeniem: checklista'),
    ('hreflang', 'Hreflang: najczęstsze błędy'),
    ('facets', 'Filtry w sklepie a SEO'),
]

# ---- robots.txt tool (content/tools/robots-ai.json) ---------------------------------
TOOL = [
    s('metaTitle', 'SEO: tytuł', 'Do 60 znaków.'),
    t('metaDescription', 'SEO: opis', 'Do 155 znaków.'),
    s('eyebrow', 'Nadtytuł'),
    s('title', 'Nagłówek (H1)'),
    t('lead', 'Tekst pod nagłówkiem'),
    s('inputLabel', 'Pole robots.txt: etykieta'),
    s('inputHint', 'Pole robots.txt: podpowiedź'),
    s('pathLabel', 'Pole ścieżki: etykieta'),
    s('pathHint', 'Pole ścieżki: podpowiedź'),
    s('check', 'Przycisk „sprawdź”'),
    s('example', 'Przycisk „wstaw przykład”'),
    s('colBot', 'Kolumna: bot'),
    s('colPurpose', 'Kolumna: do czego służy'),
    s('colStatus', 'Kolumna: dostęp'),
    s('colRule', 'Kolumna: reguła'),
    s('allowed', 'Status: ma dostęp'),
    s('blocked', 'Status: zablokowany'),
    s('noRule', 'Brak reguły'),
    s('fromGroup', 'Słowo „grupa”'),
    s('summary', 'Podsumowanie', 'Zostaw {blocked} i {total}: w ich miejsce wstawiają się liczby.'),
    s('empty', 'Komunikat przed sprawdzeniem'),
    obj('groups', 'Nazwy grup botów', [s('search', 'Wyszukiwarki'), s('aiSearch', 'Wyszukiwanie w AI'), s('training', 'Trening modeli'), s('user', 'Na prośbę użytkownika')]),
    t('userNote', 'Uwaga przy botach „na prośbę użytkownika”'),
    s('howTitle', 'Nagłówek „jak czytać wynik”'),
    {'name': 'how', 'label': 'Jak czytać wynik (punkty)', 'type': 'text', 'list': True},
    items('faq', 'FAQ', [s('q', 'Pytanie'), t('a', 'Odpowiedź')]),
    s('guideCta', 'Link do poradnika'),
    s('serviceTitle', 'Ramka usługi: nagłówek'),
    t('serviceText', 'Ramka usługi: tekst'),
    s('serviceCta', 'Ramka usługi: przycisk'),
]

SERVICES = [  # key, label in the CMS menu
    ('audit', 'Technical SEO (audyty)'),
    ('ai', 'Widoczność w odpowiedziach AI'),
    ('schema', 'Dane strukturalne'),
    ('webops', 'WebOps i SEO Operations'),
    ('content', 'Planowanie treści'),
    ('large', 'Duże serwisy i programmatic SEO'),
    ('intl', 'Enterprise i SEO międzynarodowe'),
    ('migration', 'Migracje i przebudowy stron'),
    ('ecom', 'SEO dla e-commerce'),
]

config = {
    # photos go to src/assets so Astro can crop/resize/convert them at build time
    'media': {'input': 'src/assets/media', 'output': '/media', 'categories': ['image']},
    'content': [
        {'name': 'settings', 'label': 'Ustawienia i kontakt', 'type': 'file', 'path': 'content/site.json', 'format': 'json',
         'description': 'Dane kontaktowe, formularz, kalendarz, analityka.', 'fields': SITE},
        {'name': 'pages', 'label': 'Strona główna', 'type': 'group', 'items': [
            {'name': 'pl', 'label': 'Po polsku', 'type': 'file', 'path': 'content/pl.json', 'format': 'json', 'fields': COPY},
            {'name': 'en', 'label': 'Po angielsku', 'type': 'file', 'path': 'content/en.json', 'format': 'json', 'fields': COPY},
        ]},
        {'name': 'services', 'label': 'Usługi', 'type': 'group', 'items': [
            {'name': f'service-{key}', 'label': label, 'type': 'file', 'path': f'content/services/{key}.json', 'format': 'json',
             'description': 'Adres podstrony jest stały (src/data/routes.ts), zmieniasz tylko treść.',
             'fields': [obj('pl', 'Po polsku', SERVICE), obj('en', 'Po angielsku', SERVICE)]}
            for key, label in SERVICES
        ]},
        {'name': 'more-pages', 'label': 'Inne strony', 'type': 'group', 'items': [
            {'name': 'about', 'label': 'O mnie', 'type': 'file', 'path': 'content/about.json', 'format': 'json',
             'fields': [obj('pl', 'Po polsku', ABOUT), obj('en', 'Po angielsku', ABOUT)]},
            {'name': 'tool-robots', 'label': 'Narzędzie: robots.txt dla botów AI', 'type': 'file', 'path': 'content/tools/robots-ai.json', 'format': 'json',
             'description': 'Lista botów i logika sprawdzania są w kodzie (src/data/ai-bots.ts, src/lib/robots.ts).',
             'fields': [obj('pl', 'Po polsku', TOOL), obj('en', 'Po angielsku', TOOL)]},
        ]},
        {'name': 'guides', 'label': 'Poradniki', 'type': 'group', 'items': [
            {'name': f'guide-{key}', 'label': label, 'type': 'file', 'path': f'content/guides/{key}.json', 'format': 'json',
             'description': 'Adres poradnika jest stały (src/data/routes.ts). Po zmianie treści zaktualizuj datę aktualizacji.',
             'fields': [
                 {'name': 'published', 'label': 'Data publikacji', 'type': 'date'},
                 {'name': 'updated', 'label': 'Data aktualizacji', 'type': 'date'},
                 obj('pl', 'Po polsku', GUIDE), obj('en', 'Po angielsku', GUIDE),
             ]}
            for key, label in GUIDES
        ]},
    ],
}


class NoAliases(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


header = (
    '# Pages CMS configuration (https://pagescms.org). Generated by scripts/cms/build-config.py:\n'
    '# edit the spec there, then run: python3 scripts/cms/build-config.py && python3 scripts/cms/check.py\n'
)
with open(os.path.join(ROOT, '.pages.yml'), 'w', encoding='utf-8') as f:
    f.write(header)
    yaml.dump(config, f, Dumper=NoAliases, allow_unicode=True, sort_keys=False, width=200)
print('wrote .pages.yml')
