export const pl = {
  lang: 'pl',
  locale: 'pl_PL',
  path: '/',
  meta: {
    title: 'Maciej Zięciak — konsultant Technical SEO i AI Search',
    description:
      'Technical SEO i widoczność w AI search dla dużych serwisów, e-commerce i enterprise. 9 lat doświadczenia: audyty, rendering, indeksacja, migracje, hreflang i dostęp botów AI.',
  },
  ids: { services: 'uslugi', experience: 'doswiadczenie', process: 'proces', faq: 'faq', contact: 'kontakt', gets: 'co-dostajesz' },
  skip: 'Przejdź do treści',
  nav: {
    services: 'Usługi',
    experience: 'Doświadczenie',
    process: 'Proces',
    faq: 'FAQ',
    contact: 'Kontakt',
    cta: 'Umów rozmowę',
    switchLabel: 'English version',
    menu: 'Menu',
    close: 'Zamknij',
  },
  hero: {
    pill: 'Technical SEO & AI Search · 9 lat doświadczenia',
    titleA: 'Widoczność w\u00a0Google.',
    titleB: 'Cytowania w\u00a0AI.',
    lead:
      'Pomagam dużym serwisom, sklepom i firmom enterprise być widocznymi tam, gdzie dziś szuka się odpowiedzi: w Google, AI Overviews, ChatGPT i Perplexity. Zaczynam od techniki, czyli crawlu, renderowania, indeksacji i architektury.',
    ctaPrimary: 'Umów bezpłatną konsultację',
    ctaSecondary: 'Zobacz doświadczenie',
    card: {
      title: 'Kto widzi Twoją stronę?',
      url: 'example.com/kategoria/produkt',
      note: 'Przykładowy wycinek z audytu',
      summary: '3 z 6 botów ma problem z dostępem do treści',
      rows: [
        { bot: 'Googlebot', s: 'ok', t: '200 · renderuje JS · indeksowalna' },
        { bot: 'Bingbot', s: 'ok', t: '200 · indeksowalna' },
        { bot: 'OAI-SearchBot', s: 'warn', t: 'Bez JS widzi 38% treści' },
        { bot: 'PerplexityBot', s: 'err', t: '403 · blokada WAF' },
        { bot: 'ClaudeBot', s: 'err', t: 'Zablokowany w robots.txt' },
        { bot: 'Google-Extended', s: 'ok', t: 'Dozwolony' },
      ],
    },
  },
  statement: {
    label: 'Dlaczego teraz',
    parts: [
      { t: 'Google to już nie jedyne miejsce, w którym szukają Twoi klienci. Pytają ChatGPT, Perplexity i AI Overviews. Pytanie brzmi: ' },
      { t: 'czy Twoja strona jest w odpowiedzi?', mark: true },
    ],
  },
  stage: {
    eyebrow: 'Audyt dostępu botów',
    title: 'Zobacz swoją stronę oczami botów.',
    text: 'Googlebot renderuje JavaScript. Większość crawlerów AI tego nie robi. Sprawdzam, co naprawdę widzi każdy z nich i co po drodze blokuje WAF, CDN albo robots.txt.',
  },
  stats: {
    label: 'W liczbach',
    items: [
      { v: '9 lat', k: 'w SEO: agencja, własny projekt, konsulting, enterprise' },
      { v: '1,1 mln', k: 'podstron w serwisie, który rozwijałem od zera' },
      { v: '670 tys.', k: 'URL-i w indeksie Google w szczycie' },
      { v: '115 tys.', k: 'wizyt organicznych miesięcznie w szczycie' },
    ],
  },
  tools: {
    label: 'Narzędzia, na których pracuję',
    items: ['Botify', 'Lumar', 'OnCrawl', 'Screaming Frog', 'GetBeast'],
  },
  services: {
    label: 'Usługi',
    title: 'W czym pomagam',
    intro:
      'Technical SEO to fundament. Jeśli wyszukiwarki i boty AI nie mogą poprawnie pobrać, wyrenderować i zrozumieć strony, treści i linki nie zadziałają tak, jak powinny.',
    items: [
      {
        name: 'Audyt Technical SEO',
        desc: 'Crawl, renderowanie JavaScriptu, indeksacja, canonicale, przekierowania, Core Web Vitals i logi serwera. Dostajesz listę problemów posortowaną według wpływu na ruch, z gotowymi zadaniami dla developerów.',
        tags: ['Crawl i rendering', 'Indeksacja', 'Logi serwera', 'Core Web Vitals'],
      },
      {
        name: 'AI Search i widoczność w LLM',
        desc: 'Sprawdzam, czy boty AI mają dostęp do treści i czy widzą ją bez JavaScriptu. Porządkuję dane strukturalne i encje, a potem mierzę, jak marka pojawia się w ChatGPT, Perplexity i AI Overviews.',
        tags: ['Dostęp botów AI', 'Schema.org', 'Encje', 'Monitoring cytowań'],
      },
      {
        name: 'Duże serwisy i programmatic SEO',
        desc: 'Setki tysięcy URL-i, nawigacja fasetowa, crawl budget, szablony stron. Sam rozwijałem serwis z ponad milionem podstron, więc wiem, gdzie takie projekty się sypią.',
        tags: ['Crawl budget', 'Nawigacja fasetowa', 'Szablony', 'Skala'],
      },
      {
        name: 'Enterprise i SEO międzynarodowe',
        desc: 'Adobe Experience Manager, wiele rynków i wersji językowych, hreflang. Praca z zespołami developerskimi i w procesach korporacyjnych.',
        tags: ['AEM', 'Hreflang', 'Wiele rynków', 'Procesy dev'],
      },
      {
        name: 'Migracje i relaunche',
        desc: 'Zmiana CMS, domeny albo struktury URL bez utraty ruchu: mapa przekierowań, testy przed startem i monitoring po wdrożeniu.',
        tags: ['Mapa przekierowań', 'Testy przed startem', 'Monitoring'],
      },
      {
        name: 'E-commerce SEO',
        desc: 'Kategorie, filtry, karty produktów i kontrola indeksacji. Doświadczenie z PrestaShop, Magento, WordPress, Shoper, RedCart i systemami autorskimi.',
        tags: ['Kategorie i filtry', 'Karty produktów', 'Rynki PL i CZ'],
      },
    ],
  },
  experience: {
    label: 'Doświadczenie',
    title: '9 lat w SEO',
    intro:
      'Od agencji i własnego projektu, przez konsulting, po zespoły enterprise w Accenture Song i Philip Morris International.',
    items: [
      {
        when: '2026 — obecnie',
        org: 'Philip Morris International',
        role: 'Manager SEO & AI Search Operations',
        desc: 'Wcześniej Tech SEO Operations Senior Specialist.',
      },
      {
        when: '2021 — 2026',
        org: 'Accenture Song',
        role: 'Digital Marketing Senior Strategy Analyst (SEO)',
        desc: 'Wcześniej Senior Technical SEO Expert. Strategie Technical SEO dla odbiorców międzynarodowych, serwisy na Adobe Experience Manager.',
      },
      {
        when: '2020 — 2022',
        org: 'Działalność własna',
        role: 'Konsultant SEO',
        desc: 'Audyty i konsulting: Technical SEO, on-page i off-page.',
      },
      {
        when: '2019 — 2021',
        org: 'IG',
        role: 'Technical SEO Specialist',
        desc: 'Optymalizacja serwisów zbudowanych na Adobe Experience Manager.',
      },
      {
        when: '2018 — 2019',
        org: 'Agencja SEO, Kraków',
        role: 'SEO dla e-commerce, rynki PL i CZ',
        desc: 'Audyty, strategie i wdrożenia na wielu platformach sklepowych, warsztaty dla klientów, koordynacja w 20-osobowym zespole.',
      },
      {
        when: '2017 — 2023',
        org: 'Własny projekt',
        role: 'Współzałożyciel, SEO lead',
        desc: 'Polski katalog firm, w którym byłem jedynym specjalistą SEO: ponad 1,1 mln podstron, 670 tys. URL-i w indeksie i 115 tys. wizyt organicznych miesięcznie w szczycie. Później konsultant nowych właścicieli.',
        highlight: true,
      },
    ],
  },
  process: {
    label: 'Proces',
    title: 'Jak pracuję',
    steps: [
      { name: 'Diagnoza', desc: 'Dostęp do danych, crawl, logi, analiza renderowania i dostępu botów. Ustalam, gdzie serwis naprawdę traci.' },
      { name: 'Priorytety', desc: 'Lista działań ułożona według wpływu i kosztu wdrożenia, z KPI powiązanymi z celami biznesowymi.' },
      { name: 'Wdrożenie', desc: 'Zadania dla developerów, review zmian przed publikacją, wsparcie zespołu, a gdy trzeba, wdrożenie po mojej stronie.' },
      { name: 'Pomiar', desc: 'Monitoring indeksacji, ruchu i obecności w AI search. Priorytety przesuwam tam, gdzie dane pokazują największy zwrot.' },
    ],
  },
  faq: {
    label: 'FAQ',
    title: 'Częste pytania',
    items: [
      {
        q: 'Czym Technical SEO różni się od „zwykłego” SEO?',
        a: 'Technical SEO odpowiada za to, czy wyszukiwarki i boty AI mogą znaleźć, pobrać, wyrenderować i zrozumieć Twoją stronę. Jeśli tu jest problem, treści i linki nie zadziałają w pełni, niezależnie od ich jakości.',
      },
      {
        q: 'Czy da się „wypozycjonować” stronę w ChatGPT?',
        a: 'Nie ma jednego przełącznika. Da się natomiast zadbać o to, żeby boty AI miały dostęp do treści, widziały ją bez JavaScriptu, rozumiały, czym jest Twoja marka (encje, dane strukturalne), i żeby marka pojawiała się w źródłach, z których korzystają modele. Efekty da się mierzyć.',
      },
      {
        q: 'Pracujesz z dużymi serwisami i enterprise?',
        a: 'Tak, to moja specjalność: serwisy z setkami tysięcy URL-i, platformy takie jak Adobe Experience Manager, wiele rynków i wersji językowych, praca w procesach z zespołami dev.',
      },
      {
        q: 'Doradzasz czy też wdrażasz?',
        a: 'Jedno i drugie. Najczęściej piszę zadania dla developerów i robię review zmian, ale część rzeczy mogę wdrożyć samodzielnie.',
      },
      {
        q: 'Ile to kosztuje?',
        a: 'Audyt wyceniam jednorazowo, stałą współpracę miesięcznie. Kwota zależy od skali serwisu i zakresu. Po krótkiej rozmowie dostajesz konkretną wycenę.',
      },
    ],
  },
  contact: {
    label: 'Kontakt',
    title: 'Porozmawiajmy o Twoim serwisie.',
    lead: 'Napisz kilka zdań o projekcie i o tym, co chcesz osiągnąć. Pierwsza konsultacja jest bezpłatna.',
    topicsLabel: 'Czego dotyczy projekt?',
    topics: ['Audyt techniczny', 'AI search', 'Duży serwis', 'Enterprise / AEM', 'Migracja', 'Stała współpraca'],
    urlLabel: 'Adres strony',
    urlPlaceholder: 'https://twojafirma.pl',
    msgLabel: 'Wiadomość',
    msgPlaceholder: 'Czym się zajmujecie i co chcecie osiągnąć?',
    submit: 'Wyślij wiadomość',
    subject: 'Zapytanie SEO — maciejzieciak.com',
    bodyTopics: 'Temat',
    bodyUrl: 'Strona',
    orEmail: 'Albo napisz bezpośrednio',
  },
  footer: {
    rights: 'Wszelkie prawa zastrzeżone.',
    top: 'Do góry',
    built: 'Statyczny HTML, zero trackerów, fonty hostowane lokalnie.',
  },
};

export type Dict = typeof pl;
