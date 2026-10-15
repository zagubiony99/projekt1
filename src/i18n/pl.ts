export const pl = {
  lang: 'pl',
  locale: 'pl_PL',
  path: '/',
  meta: {
    title: 'Konsultant Technical SEO i AI search | Maciej Zięciak',
    description:
      'Konsultant Technical SEO z 9-letnim doświadczeniem. Audyty, migracje i widoczność w ChatGPT dla dużych serwisów, sklepów internetowych i marek enterprise.',
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
    pill: 'Technical SEO i AI search · 9\u00a0lat w\u00a0branży',
    titleA: 'Widoczna w\u00a0Google.',
    titleB: 'Cytowana przez\u00a0AI.',
    lead:
      'Pomagam dużym serwisom, sklepom i markom enterprise rosnąć w Google i w odpowiedziach ChatGPT. Znajduję to, co blokuje ruch, i zamieniam to w konkretne zadania dla Twoich programistów.',
    ctaPrimary: 'Umów bezpłatną konsultację',
    ctaSecondary: 'Zobacz doświadczenie',
    ctaNote: '30 minut · online · bez zobowiązań',
    trustLabel: 'Pracowałem m.in. w',
    // Hero demo: an AI answer that cites "your" site. Illustrative, fictional domains.
    // Citations in the answer are written as [n] and refer to sources[n - 1].
    demo: {
      app: 'Odpowiedź AI',
      note: 'Przykład poglądowy',
      q: 'Jakie buty do biegania wybrać na pierwszy maraton?',
      think: 'Przeszukuję 14 stron',
      answer:
        'Na pierwszy maraton wybierz buty z dobrą amortyzacją i stabilnym prowadzeniem stopy [1][3]. Dobierz je do typu stopy i przebiegnij w nich co najmniej 50 km przed startem [2]. Porównanie modeli i tabelę rozmiarów znajdziesz w poradniku sklepu [2].',
      sourcesLabel: 'Źródła',
      sources: [
        { d: 'biegowy-blog.pl', t: 'Jak wybrać buty na maraton' },
        { d: 'twojsklep.pl', t: 'Buty do biegania na maraton: poradnik', you: true },
        { d: 'forum-biegaczy.pl', t: 'Pierwszy maraton: jakie buty?' },
      ],
      you: 'Twoja strona',
    },
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
      { t: 'Twoi klienci nie szukają już tylko w Google. Pytają ChatGPT, Perplexity i AI Overviews. Liczy się jedno: ' },
      { t: 'czy w odpowiedzi pada nazwa Twojej firmy?', mark: true },
    ],
  },
  stage: {
    eyebrow: 'Audyt dostępu botów',
    title: 'Zobacz swoją stronę oczami botów.',
    text: 'Googlebot radzi sobie z JavaScriptem. Większość botów AI już nie. Sprawdzam, co naprawdę widzi każdy z nich i co po drodze odcinają firewall, CDN albo robots.txt.',
  },
  stats: {
    label: 'W liczbach',
    items: [
      { v: '9 lat', k: 'w SEO: agencja, własny serwis, doradztwo i korporacje' },
      { v: '1,1 mln', k: 'podstron w serwisie, który rozwijałem od zera' },
      { v: '670 tys.', k: 'adresów w indeksie Google w szczytowym momencie' },
      { v: '115 tys.', k: 'wizyt z wyszukiwarki miesięcznie w szczytowym momencie' },
    ],
  },
  tools: {
    label: 'Narzędzia, z których korzystam',
    items: ['Botify', 'Lumar', 'OnCrawl', 'Screaming Frog', 'GetBeast'],
  },
  bands: {
    afterServices: {
      title: 'Nie wiesz, od czego zacząć?',
      text: 'Na bezpłatnej konsultacji przejrzę Twoją stronę i wskażę 3 rzeczy, które warto poprawić w pierwszej kolejności.',
      btn: 'Umów bezpłatną konsultację',
    },
    afterProcess: {
      title: 'Pierwszy krok zajmuje 30 minut.',
      text: 'Krótka rozmowa, konkretne wnioski, zero zobowiązań.',
      btn: 'Umów rozmowę',
    },
  },
  compare: {
    label: 'Dlaczego konsultant, a nie agencja',
    title: 'Twoim projektem zajmuje się ekspert. Od początku do końca.',
    me: 'Ze mną',
    them: 'Typowa agencja',
    rows: [
      { k: 'Kto pracuje nad projektem', me: 'Ja, osobiście: od audytu po odbiór wdrożenia', them: 'Często junior, a ekspert pojawia się tylko na spotkaniach' },
      { k: 'Specjalizacja', me: 'Technical SEO i AI search', them: 'Wszystkiego po trochu: SEO, Google Ads, social media' },
      { k: 'Doświadczenie', me: '9 lat, w tym w PMI i Accenture Song', them: 'Zależy, komu przypadnie Twój projekt' },
      { k: 'Co dostajesz', me: 'Konkretne zadania dla programistów, od najważniejszych', them: 'Raport w PDF i tabelkę z pozycjami' },
      { k: 'Kontakt', me: 'Bezpośrednio ze mną', them: 'Przez opiekuna klienta' },
      { k: 'Forma współpracy', me: 'Jednorazowy audyt albo stała współpraca. Ty decydujesz.', them: 'Często abonament z minimalnym okresem umowy' },
    ],
  },
  sticky: { text: 'Bezpłatna konsultacja · 30 min', btn: 'Umów' },
  services: {
    label: 'Usługi',
    title: 'W czym pomagam',
    intro:
      'Technical SEO to fundament. Jeśli Google i boty AI nie potrafią poprawnie odczytać Twojej strony, nawet najlepsze treści i linki nie przyniosą efektów.',
    items: [
      {
        name: 'Audyt Technical SEO',
        desc: 'Sprawdzam wszystko, co decyduje o tym, jak Google czyta Twoją stronę: indeksację, JavaScript, przekierowania, szybkość i logi serwera. Dostajesz listę problemów od najważniejszych, z gotowymi zadaniami dla programistów.',
        tags: ['Indeksacja', 'JavaScript', 'Logi serwera', 'Core Web Vitals'],
      },
      {
        name: 'Widoczność w odpowiedziach AI',
        desc: 'Sprawdzam, czy ChatGPT, Perplexity i Google AI mają dostęp do Twojej strony i czy ją rozumieją. Porządkuję dane strukturalne i informacje o marce, a potem mierzę, jak często pojawiasz się w odpowiedziach.',
        tags: ['Dostęp botów AI', 'Dane strukturalne', 'Informacje o marce', 'Pomiar obecności w AI'],
      },
      {
        name: 'Duże serwisy i programmatic SEO',
        desc: 'Setki tysięcy adresów, filtry, crawl budget i szablony stron. Sam rozwijałem serwis z ponad milionem podstron, więc wiem, gdzie takie projekty się sypią.',
        tags: ['Crawl budget', 'Filtry i parametry', 'Szablony', 'Skala'],
      },
      {
        name: 'Enterprise i SEO międzynarodowe',
        desc: 'Wiele rynków, języków i zespołów, często na Adobe Experience Manager. Pilnuję hreflangów i wpisuję SEO w procesy firmy tak, żeby poprawki naprawdę trafiały na produkcję.',
        tags: ['AEM', 'Hreflang', 'Wiele rynków', 'Procesy wdrożeń'],
      },
      {
        name: 'Migracje i przebudowy stron',
        desc: 'Zmieniasz CMS, domenę albo adresy stron? Przygotuję przekierowania, przetestuję nową wersję przed startem i będę pilnował ruchu po wdrożeniu.',
        tags: ['Mapa przekierowań', 'Testy przed startem', 'Opieka po starcie'],
      },
      {
        name: 'SEO dla e-commerce',
        desc: 'Kategorie, filtry i karty produktów ułożone tak, żeby Google trafiał tam, gdzie sprzedajesz. Znam PrestaShop, Magento, WordPressa, Shopera, RedCart i systemy autorskie.',
        tags: ['Kategorie i filtry', 'Karty produktów', 'Rynki PL i CZ'],
      },
    ],
  },
  experience: {
    label: 'Doświadczenie',
    title: '9 lat w SEO',
    intro:
      'Od agencji i własnego serwisu, przez własną działalność, po zespoły w Accenture Song i Philip Morris International.',
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
        desc: 'Wcześniej Senior Technical SEO Expert. Strategie SEO dla marek międzynarodowych i serwisów na Adobe Experience Manager.',
      },
      {
        when: '2020 — 2022',
        org: 'Działalność własna',
        role: 'Konsultant SEO',
        desc: 'Audyty i doradztwo: SEO techniczne, treści i linki.',
      },
      {
        when: '2019 — 2021',
        org: 'IG',
        role: 'Technical SEO Specialist',
        desc: 'Optymalizacja serwisów na Adobe Experience Manager.',
      },
      {
        when: '2018 — 2019',
        org: 'Agencja SEO, Kraków',
        role: 'SEO dla e-commerce, rynki PL i CZ',
        desc: 'Audyty, strategie i wdrożenia na wielu platformach sklepowych, warsztaty dla klientów i koordynacja pracy w 20-osobowym zespole.',
      },
      {
        when: '2017 — 2023',
        org: 'Własny projekt',
        role: 'Współzałożyciel, SEO lead',
        desc: 'Polski katalog firm, w którym byłem jedynym specjalistą SEO: ponad 1,1 mln podstron, 670 tys. adresów w indeksie i 115 tys. wizyt z wyszukiwarki miesięcznie w szczytowym momencie. Po zmianie właściciela zostałem jego doradcą.',
        highlight: true,
      },
    ],
  },
  process: {
    label: 'Proces',
    title: 'Jak pracuję',
    steps: [
      { name: 'Diagnoza', desc: 'Zbieram dane, crawluję serwis, analizuję logi i to, co widzą boty. Ustalam, gdzie naprawdę uciekają ruch i pieniądze.' },
      { name: 'Priorytety', desc: 'Układam działania według tego, ile dadzą i ile kosztują. Każde ma mierzalny cel powiązany z wynikami firmy.' },
      { name: 'Wdrożenie', desc: 'Piszę zadania dla programistów, sprawdzam zmiany przed publikacją i odpowiadam na pytania zespołu. Część rzeczy wdrażam sam.' },
      { name: 'Pomiar', desc: 'Śledzę indeksację, ruch i obecność w odpowiedziach AI. Przesuwam siły tam, gdzie dane pokazują największy zwrot.' },
    ],
  },
  faq: {
    label: 'FAQ',
    title: 'Częste pytania',
    items: [
      {
        q: 'Jak wygląda bezpłatna konsultacja?',
        a: '30 minut online. Opowiadasz o serwisie i celach, a ja przeglądam stronę na żywo i wskazuję 3 rzeczy, które warto poprawić w pierwszej kolejności. Bez zobowiązań: po rozmowie sam decydujesz, czy idziemy dalej.',
      },
      {
        q: 'Czym Technical SEO różni się od „zwykłego” SEO?',
        a: 'Technical SEO sprawia, że Google i boty AI mogą znaleźć, odczytać i zrozumieć Twoją stronę. Jeśli tu są błędy, nawet świetne treści i linki nie dadzą pełnych efektów.',
      },
      {
        q: 'Czy da się „wypozycjonować” stronę w ChatGPT?',
        a: 'Nie ma jednego przycisku. Da się za to zadbać, żeby boty AI miały dostęp do treści i widziały ją bez JavaScriptu, żeby rozumiały, czym zajmuje się Twoja firma, i żeby marka pojawiała się w źródłach, z których korzystają modele. Efekty da się mierzyć.',
      },
      {
        q: 'Pracujesz z dużymi serwisami i korporacjami?',
        a: 'Tak, to moja specjalność: serwisy z setkami tysięcy adresów, Adobe Experience Manager, wiele rynków i języków oraz praca w procesach z zespołami IT.',
      },
      {
        q: 'Tylko doradzasz, czy też wdrażasz?',
        a: 'Jedno i drugie. Najczęściej piszę zadania dla programistów i sprawdzam ich wdrożenie, ale część rzeczy robię sam.',
      },
      {
        q: 'Współpracujesz z naszą agencją albo software housem?',
        a: 'Tak, to częsty układ. Przygotowuję dla nich zadania, sprawdzam zmiany i odpowiadam na pytania techniczne.',
      },
      {
        q: 'Czy podpisujesz NDA?',
        a: 'Tak. Jeśli projekt wymaga dostępu do danych, logów albo kodu, NDA podpisujemy przed startem.',
      },
      {
        q: 'Ile to kosztuje?',
        a: 'Audyt wyceniam jednorazowo, stałą współpracę miesięcznie. Kwota zależy od wielkości serwisu i zakresu prac. Konkretną wycenę dostajesz po krótkiej rozmowie.',
      },
    ],
  },
  contact: {
    label: 'Kontakt',
    title: 'Porozmawiajmy o Twoim serwisie.',
    lead: 'Na bezpłatnej, 30-minutowej rozmowie przejrzę Twoją stronę i wskażę 3 rzeczy, które warto poprawić w pierwszej kolejności. Bez zobowiązań.',
    topicsLabel: 'Czego dotyczy projekt?',
    topics: ['Audyt techniczny', 'AI search', 'Duży serwis', 'E-commerce', 'Enterprise / AEM', 'Migracja', 'Stała współpraca'],
    urlLabel: 'Adres strony',
    urlPlaceholder: 'https://twojafirma.pl',
    msgLabel: 'Wiadomość',
    msgPlaceholder: 'Czym się zajmujecie i co chcecie osiągnąć?',
    submit: 'Umów bezpłatną konsultację',
    note: 'Odpowiadam osobiście. Dane z formularza wykorzystam wyłącznie do odpowiedzi na Twoje zapytanie.',
    booking: 'Wolisz od razu wybrać termin?',
    bookingBtn: 'Otwórz kalendarz',
    sending: 'Wysyłam…',
    success: 'Dzięki! Wiadomość dotarła. Odezwę się z propozycją terminu rozmowy.',
    error: 'Coś poszło nie tak. Napisz bezpośrednio na',
    subject: 'Zapytanie SEO — maciejzieciak.com',
    bodyTopics: 'Temat',
    bodyUrl: 'Strona',
    orEmail: 'Albo napisz bezpośrednio',
  },
  consent: {
    text: 'Używam plików cookies do analityki i mierzenia skuteczności reklam. Włączę je tylko za Twoją zgodą.',
    accept: 'Akceptuję',
    reject: 'Tylko niezbędne',
    more: 'Polityka prywatności',
    settings: 'Ustawienia cookies',
  },
  privacy: {
    path: '/polityka-prywatnosci/',
    label: 'Polityka prywatności',
    description: 'Jak maciejzieciak.com przetwarza Twoje dane: co zbiera formularz kontaktowy, w jakim celu i jak długo, jakie są pliki cookies i jakie masz prawa.',
  },
  footer: {
    rights: 'Wszelkie prawa zastrzeżone.',
    top: 'Do góry',
    built: 'Statyczny HTML, fonty hostowane lokalnie, cookies tylko za zgodą.',
  },
};

export type Dict = typeof pl;
