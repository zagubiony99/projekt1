import { polishTypo } from '../i18n/typo';

// Service landing pages (PL + EN). Each entry is one sales page per language.
// Copy is built only on facts from the profile; no invented client results or prices.

export type ServiceCopy = {
  slug: string;
  name: string;            // short name (nav, cards, breadcrumbs)
  metaTitle: string;
  metaDescription: string;
  eyebrow: string;
  title: string;           // benefit headline (H1)
  lead: string;
  painTitle: string;
  pains: string[];
  getTitle: string;
  gets: { t: string; d: string }[];
  stepsTitle: string;
  steps: { t: string; when: string; d: string }[];
  forTitle: string;
  forYes: string[];
  forNo: string[];
  proof: string;           // one experience line specific to this service
  faq: { q: string; a: string }[];
};

type Pair = { key: string; topic: { pl: string; en: string }; pl: ServiceCopy; en: ServiceCopy };

const raw: Pair[] = [
  {
    key: 'audit',
    topic: { pl: 'Audyt techniczny', en: 'Technical audit' },
    pl: {
      slug: 'audyt-technical-seo',
      name: 'Audyt Technical SEO',
      metaTitle: 'Audyt Technical SEO dużych serwisów | Maciej Zięciak',
      metaDescription:
        'Audyt Technical SEO: crawl, JavaScript, indeksacja, logi serwera i Core Web Vitals. Problemy od najważniejszych i gotowe zadania dla programistów.',
      eyebrow: 'Audyt Technical SEO',
      title: 'Dowiedz się, co naprawdę blokuje Twój ruch.',
      lead:
        'Nie dostaniesz 80-stronicowego PDF-a, którego nikt nie przeczyta. Dostaniesz listę problemów ułożoną według wpływu na ruch i przychód, z gotowymi zadaniami dla programistów.',
      painTitle: 'Brzmi znajomo?',
      pains: [
        'Ruch organiczny spada, a nikt nie potrafi wskazać dlaczego.',
        'Google indeksuje tysiące stron, których nie chcesz w wynikach, a pomija te, które sprzedają.',
        'W Search Console przybywa stron ze statusem „Strona zeskanowana, ale nie zindeksowana”.',
        'Strona stoi na JavaScripcie i nie wiesz, co Googlebot faktycznie widzi.',
        'Poprzedni audyt skończył się listą 300 punktów bez priorytetów.',
        'Programiści pytają „co właściwie mamy zrobić?” i nie dostają jasnej odpowiedzi.',
      ],
      getTitle: 'Co dostajesz',
      gets: [
        { t: 'Listę problemów od najważniejszych', d: 'Każdy problem z oceną wpływu na ruch, kosztem wdrożenia i priorytetem. Najpierw to, co przyniesie najwięcej.' },
        { t: 'Gotowe zadania dla programistów', d: 'Opis problemu, przykładowe adresy, oczekiwany efekt i warunki odbioru. Do wklejenia prosto do Jiry.' },
        { t: 'Analizę renderowania i indeksacji', d: 'Co widzi Googlebot, a co boty AI. Gdzie JavaScript, canonicale, przekierowania albo robots.txt odcinają treść.' },
        { t: 'Analizę logów serwera', d: 'Gdzie Googlebot naprawdę spędza czas, a które sekcje serwisu omija.' },
        { t: 'Omówienie wyników', d: 'Przechodzimy przez wyniki z Tobą i programistami, żeby wszyscy wiedzieli, co robimy i dlaczego.' },
        { t: 'Sprawdzenie po wdrożeniu', d: 'Upewniam się, że poprawki działają tak, jak powinny, zanim uznamy temat za zamknięty.' },
      ],
      stepsTitle: 'Jak to przebiega',
      steps: [
        { t: 'Rozmowa i dostępy', when: 'Dzień 1–3', d: 'Krótka rozmowa o celach i dostęp do Search Console, analityki oraz, jeśli to możliwe, logów serwera.' },
        { t: 'Crawl i analiza', when: 'Tydzień 1–2', d: 'Pełny crawl w Screaming Frogu, Botify, Lumarze albo OnCrawlu oraz analiza renderowania, indeksacji i logów.' },
        { t: 'Priorytety i zadania', when: 'Tydzień 2–3', d: 'Układam problemy od najważniejszych i przygotowuję gotowe zadania dla zespołu.' },
        { t: 'Omówienie i wsparcie', when: 'Tydzień 3', d: 'Spotkanie z zespołem, odpowiedzi na pytania programistów i sprawdzenie pierwszych wdrożeń.' },
      ],
      forTitle: 'Dla kogo to jest',
      forYes: [
        'Serwisy od kilku tysięcy do milionów adresów',
        'Sklepy internetowe i serwisy z nawigacją fasetową',
        'Strony na JavaScripcie (React, Next.js, Angular) i na AEM',
        'Firmy z własnymi programistami albo software housem',
      ],
      forNo: [
        'Wizytówki z kilkoma podstronami',
        'Firmy szukające „pozycjonowania” w pakiecie z linkami',
        'Projekty bez możliwości wdrażania zmian w kodzie',
      ],
      proof: 'Audyty techniczne robię od 2018 roku: dla e-commerce w agencji, dla serwisów na Adobe Experience Manager i dla międzynarodowych marek w Accenture Song i Philip Morris International.',
      faq: [
        { q: 'Ile trwa audyt?', a: 'Zwykle 2–3 tygodnie od otrzymania dostępów. Przy bardzo dużych serwisach albo analizie logów z dłuższego okresu może to potrwać dłużej. Termin ustalamy przed startem.' },
        { q: 'Jakich dostępów potrzebujesz?', a: 'Minimum to Google Search Console i analityka. Bardzo pomagają logi serwera i dostęp do środowiska testowego. Wszystko ustalamy na pierwszej rozmowie.' },
        { q: 'Czy wdrażasz poprawki?', a: 'Zwykle przygotowuję zadania dla Twoich programistów i sprawdzam wdrożenia. Część rzeczy mogę zrobić sam, jeśli to ma sens.' },
        { q: 'Ile kosztuje audyt?', a: 'Audyt wyceniam jednorazowo, w zależności od wielkości serwisu i zakresu (np. czy analizujemy logi). Konkretną kwotę dostajesz po bezpłatnej konsultacji.' },
      ],
    },
    en: {
      slug: 'technical-seo-audit',
      name: 'Technical SEO audit',
      metaTitle: 'Technical SEO Audit for Large Sites | Maciej Zięciak',
      metaDescription:
        'Technical SEO audit: crawling, JavaScript rendering, indexation, server logs and Core Web Vitals. Issues ranked by impact, with dev-ready tickets.',
      eyebrow: 'Technical SEO audit',
      title: 'Find out what is really holding your traffic back.',
      lead:
        'No 80-page PDF that nobody reads. You get a list of issues ranked by impact on traffic and revenue, with ready-to-ship tickets for your developers.',
      painTitle: 'Sound familiar?',
      pains: [
        'Organic traffic is dropping and nobody can say why.',
        'Google indexes thousands of pages you don’t want in search and skips the ones that sell.',
        '“Crawled – currently not indexed” keeps growing in Search Console.',
        'Your site runs on JavaScript and you don’t know what Googlebot actually sees.',
        'Your last audit ended as a 300-point list with no priorities.',
        'Your dev team keeps asking “so what exactly should we do?”',
      ],
      getTitle: 'What you get',
      gets: [
        { t: 'Issues ranked by impact', d: 'Every issue scored for traffic impact, implementation cost and priority. What moves the needle comes first.' },
        { t: 'Ready-to-ship developer tickets', d: 'Tickets with the problem, sample URLs, expected behaviour and acceptance criteria. Paste straight into Jira.' },
        { t: 'Rendering and indexation analysis', d: 'What Googlebot sees versus AI crawlers. Where JavaScript, canonicals, redirects or robots.txt cut content off.' },
        { t: 'Server log analysis', d: 'Where Googlebot actually spends crawl budget, and which sections it ignores.' },
        { t: 'Walkthrough call', d: 'We go through the findings with you and your dev team so everyone knows what to do and why.' },
        { t: 'Post-release verification', d: 'I check the fixes behave as intended before we close the topic.' },
      ],
      stepsTitle: 'How it works',
      steps: [
        { t: 'Kick-off and access', when: 'Day 1–3', d: 'A short call about goals, access to Search Console, analytics and, ideally, server logs.' },
        { t: 'Crawl and analysis', when: 'Week 1–2', d: 'Full crawl (Screaming Frog, Botify, Lumar or OnCrawl), rendering, indexation and log analysis.' },
        { t: 'Priorities and tickets', when: 'Week 2–3', d: 'Issues ranked by impact and turned into ready-to-ship tickets.' },
        { t: 'Walkthrough and support', when: 'Week 3', d: 'Call with the team, answers for developers, verification of the first releases.' },
      ],
      forTitle: 'Who it’s for',
      forYes: [
        'Websites from thousands to millions of URLs',
        'Online stores and sites with faceted navigation',
        'JavaScript sites (React, Next.js, Angular) and AEM',
        'Companies with an in-house dev team or agency',
      ],
      forNo: [
        'Small brochure sites with a handful of pages',
        'Anyone looking for “SEO packages” with links',
        'Projects where code changes can’t be shipped',
      ],
      proof: 'I’ve been running technical audits since 2018: for e-commerce at an agency, for Adobe Experience Manager sites, and for international brands at Accenture Song and Philip Morris International.',
      faq: [
        { q: 'How long does an audit take?', a: 'Usually 2–3 weeks from receiving access. Very large sites or long log periods can take longer. We agree the timeline before we start.' },
        { q: 'What access do you need?', a: 'At minimum Google Search Console and analytics. Server logs and a staging environment help a lot. We settle this on the first call.' },
        { q: 'Do you implement the fixes?', a: 'Usually I write tickets for your dev team and verify the releases. I can implement some things myself when it makes sense.' },
        { q: 'How much does an audit cost?', a: 'Audits are a one-off fee depending on site size and scope (e.g. whether we analyse logs). You get a concrete quote after a free consultation.' },
      ],
    },
  },
  {
    key: 'ai',
    topic: { pl: 'AI search', en: 'AI search' },
    pl: {
      slug: 'widocznosc-w-ai-search',
      name: 'Widoczność w odpowiedziach AI',
      metaTitle: 'Widoczność w ChatGPT i AI Overviews | Maciej Zięciak',
      metaDescription:
        'Sprawdzam, czy ChatGPT, Perplexity i Google AI widzą i cytują Twoją stronę. Dostęp botów AI, dane strukturalne i pomiar obecności marki w AI.',
      eyebrow: 'Widoczność w odpowiedziach AI',
      title: 'Niech AI poleca Ciebie, a nie konkurencję.',
      lead:
        'Coraz więcej klientów pyta ChatGPT, Perplexity albo AI Overviews, zanim kliknie jakikolwiek link. Sprawdzam, czy modele mają dostęp do Twojej strony, czy ją rozumieją i czy ją cytują. Potem usuwam to, co stoi na przeszkodzie.',
      painTitle: 'Brzmi znajomo?',
      pains: [
        'Pytasz ChatGPT o swoją branżę i w odpowiedzi jest konkurencja, a Ciebie nie ma.',
        'Nie wiesz, czy boty OpenAI, Perplexity i Anthropic w ogóle mają dostęp do Twojej strony.',
        'Firewall albo CDN blokuje nieznane boty i nikt tego nie sprawdzał.',
        'Treść ładuje się JavaScriptem, którego większość crawlerów AI nie wykonuje.',
        'AI Overviews odpowiadają na pytania, na które kiedyś klikano w Twoją stronę.',
        'Zarząd pyta o „strategię na AI”, a w SEO nikt nie ma na to planu.',
      ],
      getTitle: 'Co dostajesz',
      gets: [
        { t: 'Audyt dostępu botów AI', d: 'Robots.txt, firewall, CDN i odpowiedzi serwera dla OAI-SearchBot, GPTBot, PerplexityBot, ClaudeBot, Google-Extended i innych.' },
        { t: 'Test strony bez JavaScriptu', d: 'Ile treści widzi bot, który nie uruchamia JavaScriptu, i co trzeba przenieść do HTML-a.' },
        { t: 'Dane strukturalne i informacje o marce', d: 'Schema.org i spójny opis marki w sieci, żeby modele rozumiały, kim jesteś i czym się zajmujesz.' },
        { t: 'Pomiar obecności w AI', d: 'Zestaw pytań typowych dla Twojej branży i regularny pomiar, jak często i w jakim kontekście pojawia się Twoja marka.' },
        { t: 'Plan treści, które AI cytuje', d: 'Które treści mają szansę trafić do odpowiedzi i jak je przygotować, żeby modele chciały z nich korzystać.' },
        { t: 'Decyzję, którym botom dać dostęp', d: 'Które boty wpuścić, a które zablokować, z uwzględnieniem kwestii prawnych i biznesowych.' },
      ],
      stepsTitle: 'Jak to przebiega',
      steps: [
        { t: 'Punkt wyjścia', when: 'Tydzień 1', d: 'Sprawdzam, jak marka wypada dziś w ChatGPT, Perplexity, Gemini i AI Overviews na kluczowe pytania.' },
        { t: 'Dostęp i JavaScript', when: 'Tydzień 1–2', d: 'Audyt dostępu botów, odpowiedzi serwera, firewalla i CDN oraz treści widocznej bez JavaScriptu.' },
        { t: 'Marka i treści', when: 'Tydzień 2–4', d: 'Dane strukturalne, informacje o marce i plan treści, które mają szansę trafić do odpowiedzi.' },
        { t: 'Pomiar', when: 'Co miesiąc', d: 'Regularny pomiar obecności w odpowiedziach AI i korekta działań.' },
      ],
      forTitle: 'Dla kogo to jest',
      forYes: [
        'Marki, których klienci pytają AI o rekomendacje',
        'SaaS, B2B i usługi z długim procesem decyzyjnym',
        'Serwisy z dużą liczbą treści eksperckich',
        'Firmy, które chcą świadomie zdecydować o dostępie botów AI',
      ],
      forNo: [
        'Firmy oczekujące gwarancji „pierwszego miejsca w ChatGPT”',
        'Strony bez treści, które dałoby się zacytować',
      ],
      proof: 'Obecnie pracuję jako Manager SEO & AI Search Operations w Philip Morris International. Wcześniej przez prawie 5 lat zajmowałem się Technical SEO w Accenture Song.',
      faq: [
        { q: 'Czy da się zagwarantować obecność w ChatGPT?', a: 'Nie. Modele działają inaczej niż wyniki Google i nikt uczciwy tego nie obiecuje. Da się za to usunąć bariery techniczne, wzmocnić markę i mierzyć postępy.' },
        { q: 'Czy blokować boty AI?', a: 'To decyzja biznesowa. Część botów zbiera dane do trenowania modeli, a część wyszukuje informacje na bieżąco. Pomagam rozróżnić, które dają widoczność, a które nie.' },
        { q: 'Jak mierzysz widoczność w AI?', a: 'Stałym zestawem pytań dla Twojej branży, sprawdzanym regularnie w kilku modelach, oraz danymi o ruchu z narzędzi AI w analityce.' },
        { q: 'Czy to zastępuje klasyczne SEO?', a: 'Nie, to jego rozszerzenie. Te same fundamenty techniczne decydują o widoczności w Google i w odpowiedziach AI.' },
      ],
    },
    en: {
      slug: 'ai-search-visibility',
      name: 'AI search & LLM visibility',
      metaTitle: 'AI Search Visibility for ChatGPT | Maciej Zięciak',
      metaDescription:
        'Find out whether ChatGPT, Perplexity and Google AI can see and cite your site. AI crawler access, structured data and brand visibility tracking.',
      eyebrow: 'AI search & LLM visibility',
      title: 'Be in the answer, not just below it.',
      lead:
        'More and more buyers ask ChatGPT, Perplexity or AI Overviews before they ever click a link. I check whether models can access your site at all, whether they understand it and whether they cite it, and then I fix what’s missing.',
      painTitle: 'Sound familiar?',
      pains: [
        'You ask ChatGPT about your industry and it recommends competitors, not you.',
        'You don’t know whether OpenAI, Perplexity and Anthropic crawlers can reach your site.',
        'Your WAF or CDN blocks unknown bots and nobody has checked.',
        'Content loads via JavaScript that most AI crawlers don’t execute.',
        'AI Overviews now answer questions that used to send clicks to you.',
        'The board asks for an “AI strategy” and SEO has no plan for it.',
      ],
      getTitle: 'What you get',
      gets: [
        { t: 'AI crawler access audit', d: 'Robots.txt, WAF, CDN and response codes for OAI-SearchBot, GPTBot, PerplexityBot, ClaudeBot, Google-Extended and more.' },
        { t: 'No-JavaScript rendering test', d: 'How much content a non-JS crawler sees, and what needs to move into the HTML.' },
        { t: 'Entities and structured data', d: 'Schema.org and consistent brand information so models understand who you are and what you do.' },
        { t: 'Citation tracking', d: 'A prompt set for your industry and regular measurement of how your brand shows up in AI answers.' },
        { t: 'Answer-ready content strategy', d: 'Which content is likely to be cited and how to shape it so models want to use it.' },
        { t: 'An access decision', d: 'A conscious choice about which bots get your content, balancing legal and business needs.' },
      ],
      stepsTitle: 'How it works',
      steps: [
        { t: 'Baseline', when: 'Week 1', d: 'How your brand shows up today in ChatGPT, Perplexity, Gemini and AI Overviews for key questions.' },
        { t: 'Access and rendering', when: 'Week 1–2', d: 'Bot access, server responses, WAF/CDN and content visible without JavaScript.' },
        { t: 'Entities and content', when: 'Week 2–4', d: 'Structured data, brand information and a plan for citable content.' },
        { t: 'Measurement', when: 'Monthly', d: 'Repeatable measurement of AI answer presence and course correction.' },
      ],
      forTitle: 'Who it’s for',
      forYes: [
        'Brands whose buyers ask AI for recommendations',
        'SaaS, B2B and services with long buying cycles',
        'Sites with a lot of expert content',
        'Companies that want to decide on AI bot access deliberately',
      ],
      forNo: [
        'Anyone expecting a guaranteed “#1 in ChatGPT”',
        'Sites with no content worth citing',
      ],
      proof: 'I currently work as Manager SEO & AI Search Operations at Philip Morris International. Before that I spent almost five years on technical SEO at Accenture Song.',
      faq: [
        { q: 'Can you guarantee a spot in ChatGPT?', a: 'No. Models don’t work like Google rankings and nobody honest guarantees this. What I can do is remove technical barriers, strengthen your brand as an entity and measure progress.' },
        { q: 'Should we block AI bots?', a: 'It’s a business decision. Some bots train models, others fetch pages for live answers. I help you tell apart the ones that bring visibility from the ones that don’t.' },
        { q: 'How do you measure AI visibility?', a: 'With a fixed prompt set for your industry checked regularly across several models, plus AI referral traffic in your analytics.' },
        { q: 'Does this replace classic SEO?', a: 'No, it extends it. The same technical foundations decide visibility in Google and in AI answers.' },
      ],
    },
  },
  {
    key: 'large',
    topic: { pl: 'Duży serwis', en: 'Large website' },
    pl: {
      slug: 'seo-duzych-serwisow',
      name: 'Duże serwisy i programmatic SEO',
      metaTitle: 'SEO dużych serwisów i programmatic SEO | Maciej Zięciak',
      metaDescription:
        'SEO dla serwisów z setkami tysięcy adresów: crawl budget, filtry, szablony i programmatic SEO. Doświadczenie z serwisem, który urósł do 1,1 mln podstron.',
      eyebrow: 'Duże serwisy i programmatic SEO',
      title: 'Milion podstron może pracować na Ciebie. Albo przeciwko Tobie.',
      lead:
        'Przy setkach tysięcy adresów każdy błąd w szablonie powtarza się tysiące razy. Sam rozwijałem serwis do ponad 1,1 mln podstron i 115 tys. wizyt organicznych miesięcznie, więc wiem, gdzie takie projekty się sypią.',
      painTitle: 'Brzmi znajomo?',
      pains: [
        'Googlebot krąży po filtrach i parametrach zamiast po stronach, które mają znaczenie.',
        'W indeksie jest kilka razy więcej stron niż w mapie witryny albo odwrotnie.',
        'Nowe strony czekają tygodniami na zaindeksowanie.',
        'Tysiące podobnych stron konkurują ze sobą o te same frazy.',
        'Po wdrożeniu nowego szablonu ruch się zmienił i nikt nie wie dlaczego.',
        'Programmatic SEO wygenerowało dużo stron i mało ruchu.',
      ],
      getTitle: 'Co dostajesz',
      gets: [
        { t: 'Analizę crawl budgetu', d: 'Na podstawie logów i crawla: gdzie bot marnuje czas i jak skierować go do wartościowych sekcji.' },
        { t: 'Kontrolę indeksacji', d: 'Zasady dla filtrów, parametrów, paginacji i duplikatów: co indeksować, co kanonizować, czego nie crawlować.' },
        { t: 'Audyt szablonów', d: 'Patrzę na szablony, a nie pojedyncze adresy. Jedna poprawka naprawia tysiące stron.' },
        { t: 'Architekturę i linkowanie wewnętrzne', d: 'Struktura, która prowadzi bota i użytkownika do stron z największym potencjałem.' },
        { t: 'Strategię programmatic SEO', d: 'Które strony generować, z jakich danych i jak zapewnić im unikalną wartość.' },
        { t: 'Pomiar po zmianach', d: 'Indeksacja i ruch w każdej sekcji osobno, żeby od razu widzieć efekt wdrożeń.' },
      ],
      stepsTitle: 'Jak to przebiega',
      steps: [
        { t: 'Dane', when: 'Tydzień 1', d: 'Logi serwera, Search Console, mapy witryny i crawl reprezentatywnej części serwisu.' },
        { t: 'Diagnoza sekcji', when: 'Tydzień 1–3', d: 'Analiza szablonów, indeksacji i crawl budgetu w każdej sekcji serwisu.' },
        { t: 'Zasady i architektura', when: 'Tydzień 3–4', d: 'Reguły indeksacji, linkowania i generowania stron spisane jako zadania dla zespołu.' },
        { t: 'Wdrożenie i pomiar', when: 'Kolejne miesiące', d: 'Wsparcie wdrożeń i śledzenie zmian w indeksacji i ruchu.' },
      ],
      forTitle: 'Dla kogo to jest',
      forYes: [
        'Katalogi, portale ogłoszeniowe, marketplace’y',
        'Sklepy z dziesiątkami tysięcy produktów',
        'Serwisy budujące strony z danych (programmatic SEO)',
        'Wydawcy i serwisy z dużym archiwum treści',
      ],
      forNo: ['Serwisy poniżej kilku tysięcy stron, gdzie wystarczy standardowy audyt'],
      proof: 'Przez lata byłem jedynym specjalistą SEO polskiego katalogu firm: ponad 1,1 mln podstron, 670 tys. adresów w indeksie Google i 115 tys. wizyt z wyszukiwarki miesięcznie w szczytowym momencie.',
      faq: [
        { q: 'Od ilu stron serwis jest „duży”?', a: 'Problemy typowe dla dużych serwisów zaczynają się zwykle od kilkudziesięciu tysięcy adresów albo wcześniej, jeśli serwis ma rozbudowane filtry i parametry.' },
        { q: 'Czy potrzebne są logi serwera?', a: 'Bardzo pomagają, bo pokazują, co bot faktycznie robi. Bez nich też da się pracować, ale diagnoza jest mniej precyzyjna.' },
        { q: 'Czy programmatic SEO jeszcze działa?', a: 'Tak, jeśli strony mają realną wartość i unikalne dane. Masowe generowanie podobnych stron dziś raczej szkodzi niż pomaga.' },
      ],
    },
    en: {
      slug: 'large-website-seo',
      name: 'Large sites & programmatic SEO',
      metaTitle: 'SEO for Large Websites & Programmatic SEO | Maciej Zięciak',
      metaDescription:
        'SEO for sites with hundreds of thousands of URLs: crawl budget, faceted navigation, templates and programmatic SEO, from someone who grew a 1.1M-page site.',
      eyebrow: 'Large sites & programmatic SEO',
      title: 'Scale that works for your traffic, not against it.',
      lead:
        'With hundreds of thousands of URLs, every template mistake multiplies at scale. I grew a site to over 1.1M pages and 115k monthly organic visits myself, so I know where these projects break.',
      painTitle: 'Sound familiar?',
      pains: [
        'Googlebot wanders through filters and parameters instead of the pages that matter.',
        'Your index is several times larger than your sitemap, or the other way round.',
        'New pages wait weeks to get indexed.',
        'Thousands of near-identical pages compete for the same queries.',
        'A new template went live, traffic changed, and nobody knows why.',
        'Programmatic SEO produced lots of pages and little traffic.',
      ],
      getTitle: 'What you get',
      gets: [
        { t: 'Crawl budget analysis', d: 'From logs and crawls: where the bot wastes resources and how to point it at valuable sections.' },
        { t: 'Indexation control', d: 'Rules for filters, parameters, pagination and duplicates: what to index, canonicalise or keep out of the crawl.' },
        { t: 'Template audit', d: 'SEO measured per template, not per URL. One fix repairs thousands of pages.' },
        { t: 'Architecture and internal linking', d: 'A structure that leads bots and users to the pages with the most potential.' },
        { t: 'Programmatic SEO strategy', d: 'Which pages to generate, from which data, and how to give them unique value.' },
        { t: 'Post-change monitoring', d: 'Indexation and traffic tracked per section, so you see the effect of every release.' },
      ],
      stepsTitle: 'How it works',
      steps: [
        { t: 'Data', when: 'Week 1', d: 'Server logs, Search Console, sitemaps and a crawl of a representative part of the site.' },
        { t: 'Diagnosis per section', when: 'Week 1–3', d: 'Templates, indexation and crawl budget analysed section by section.' },
        { t: 'Rules and architecture', when: 'Week 3–4', d: 'Indexation, linking and page-generation rules written up as tickets.' },
        { t: 'Rollout and measurement', when: 'Following months', d: 'Release support and monitoring of indexation and traffic.' },
      ],
      forTitle: 'Who it’s for',
      forYes: [
        'Directories, classifieds and marketplaces',
        'Stores with tens of thousands of products',
        'Sites generating pages from data (programmatic SEO)',
        'Publishers with large content archives',
      ],
      forNo: ['Sites under a few thousand pages, where a standard audit is enough'],
      proof: 'For years I was the only SEO behind a Polish business directory: over 1.1M pages, 670k URLs indexed by Google and 115k monthly organic visits at peak.',
      faq: [
        { q: 'When is a site “large”?', a: 'Large-site problems usually start at tens of thousands of URLs, or earlier if the site has heavy filtering and parameters.' },
        { q: 'Do you need server logs?', a: 'They help a lot, because they show what the bot actually does. It’s possible without them, but the diagnosis is less precise.' },
        { q: 'Does programmatic SEO still work?', a: 'Yes, if pages carry real value and unique data. Mass-producing near-identical pages tends to hurt rather than help today.' },
      ],
    },
  },
  {
    key: 'intl',
    topic: { pl: 'Enterprise / AEM', en: 'Enterprise / AEM' },
    pl: {
      slug: 'seo-enterprise-miedzynarodowe',
      name: 'Enterprise i SEO międzynarodowe',
      metaTitle: 'SEO międzynarodowe i enterprise (AEM) | Maciej Zięciak',
      metaDescription:
        'SEO dla marek enterprise i serwisów wielojęzycznych: hreflang, struktura rynków, Adobe Experience Manager i praca z zespołami IT w dużych firmach.',
      eyebrow: 'Enterprise i SEO międzynarodowe',
      title: 'Jedna marka, wiele rynków. Zero chaosu w wynikach.',
      lead:
        'Przy wielu rynkach i językach SEO to przede wszystkim proces: hreflang, szablony, wydania i ludzie w różnych zespołach. Pracuję w takim środowisku na co dzień, od lat na Adobe Experience Manager.',
      painTitle: 'Brzmi znajomo?',
      pains: [
        'Google pokazuje użytkownikom w Niemczech wersję brytyjską albo odwrotnie.',
        'Hreflang niby jest wdrożony, ale crawl pokazuje setki błędów i nikt nie wie, które są ważne.',
        'Każdy rynek robi SEO po swojemu i wyniki są nie do porównania.',
        'Zmiany SEO czekają miesiącami w kolejce wydań.',
        'Globalny szablon psuje lokalne strony, które dobrze radziły sobie w Google.',
        'Agencje na różnych rynkach dostają sprzeczne wytyczne.',
      ],
      getTitle: 'Co dostajesz',
      gets: [
        { t: 'Audyt hreflang i wersji językowych', d: 'Pełna mapa wersji rynkowych, błędy w powiązaniach, x-default i spójność z canonicalami.' },
        { t: 'Strategię struktury rynków', d: 'Domeny, subdomeny czy katalogi, oraz jak to wpływa na SEO, utrzymanie i koszty.' },
        { t: 'Wytyczne SEO dla AEM', d: 'Ustawienia komponentów, szablonów i dyspozytora, które decydują o SEO w Adobe Experience Manager.' },
        { t: 'Standardy dla rynków i agencji', d: 'Jedne zasady SEO dla wszystkich rynków, żeby wyniki dało się porównać, a dobre rozwiązania przenieść dalej.' },
        { t: 'SEO w procesie wydań', d: 'Wymagania SEO w zadaniach i kontrola przed każdym wydaniem, żeby błędy nie trafiały na produkcję.' },
        { t: 'Raporty dla każdego rynku', d: 'Widoczność i ruch w podziale na rynki i wersje językowe.' },
      ],
      stepsTitle: 'Jak to przebiega',
      steps: [
        { t: 'Mapa rynków', when: 'Tydzień 1', d: 'Inwentaryzacja domen, wersji językowych i zespołów odpowiedzialnych za każdy rynek.' },
        { t: 'Audyt', when: 'Tydzień 1–3', d: 'Hreflang, canonicale, szablony i konfiguracja CMS na reprezentatywnych rynkach.' },
        { t: 'Standardy', when: 'Tydzień 3–4', d: 'Wytyczne i wymagania SEO dla zespołów i agencji.' },
        { t: 'Stała opieka', when: 'Kolejne miesiące', d: 'Kontrola wydań, wsparcie rynków i raporty.' },
      ],
      forTitle: 'Dla kogo to jest',
      forYes: [
        'Marki działające na wielu rynkach i w wielu językach',
        'Serwisy na Adobe Experience Manager i innych CMS-ach enterprise',
        'Organizacje z kilkoma zespołami IT i agencjami',
        'Firmy wchodzące na nowe rynki',
      ],
      forNo: ['Firmy działające na jednym rynku, w jednym języku'],
      proof: 'Od 2019 roku pracuję przy serwisach na Adobe Experience Manager: w IG, potem w Accenture Song (strategie Technical SEO dla odbiorców międzynarodowych), dziś w Philip Morris International.',
      faq: [
        { q: 'Czy pracujesz z naszą agencją i programistami?', a: 'Tak, w dużych firmach to standard. Przygotowuję wytyczne i zadania, sprawdzam wdrożenia i wspieram zespoły w różnych krajach.' },
        { q: 'Czy znasz tylko AEM?', a: 'AEM znam najlepiej, ale zasady SEO międzynarodowego są uniwersalne. Pracowałem też z WordPressem, platformami e-commerce i systemami autorskimi.' },
        { q: 'W jakich językach pracujesz?', a: 'Komunikacja i dokumentacja po polsku albo po angielsku.' },
      ],
    },
    en: {
      slug: 'enterprise-international-seo',
      name: 'Enterprise & international SEO',
      metaTitle: 'Enterprise & International SEO (AEM) | Maciej Zięciak',
      metaDescription:
        'SEO for enterprise brands and multilingual sites: hreflang, market structure, Adobe Experience Manager and work with dev teams in large organisations.',
      eyebrow: 'Enterprise & international SEO',
      title: 'One brand, many markets. No chaos in search.',
      lead:
        'With many markets and languages, SEO is mostly process: hreflang, templates, releases and people across teams. That’s my daily environment, on Adobe Experience Manager for years.',
      painTitle: 'Sound familiar?',
      pains: [
        'Google shows German users the UK version, or the other way round.',
        'Hreflang is in place, but Search Console shows errors and nobody knows which matter.',
        'Every market does SEO its own way and results can’t be compared.',
        'SEO fixes wait months in the release queue.',
        'A global template breaks local pages that used to rank well.',
        'Agencies in different markets get conflicting guidelines.',
      ],
      getTitle: 'What you get',
      gets: [
        { t: 'Hreflang and language version audit', d: 'A full map of market versions, broken links between them, x-default and consistency with canonicals.' },
        { t: 'Market structure strategy', d: 'Domains, subdomains or folders, and what that means for SEO, maintenance and cost.' },
        { t: 'SEO guidelines for AEM', d: 'Component, template and dispatcher settings that decide SEO in Adobe Experience Manager.' },
        { t: 'Standards for markets and agencies', d: 'One set of SEO rules across markets, so results are comparable and scalable.' },
        { t: 'SEO in the release process', d: 'SEO acceptance criteria in tickets and pre-release review, so errors never reach production.' },
        { t: 'Reporting per market', d: 'Visibility and traffic split by market and language version.' },
      ],
      stepsTitle: 'How it works',
      steps: [
        { t: 'Market map', when: 'Week 1', d: 'An inventory of domains, language versions and the teams behind each market.' },
        { t: 'Audit', when: 'Week 1–3', d: 'Hreflang, canonicals, templates and CMS configuration on representative markets.' },
        { t: 'Standards', when: 'Week 3–4', d: 'Guidelines and SEO acceptance criteria for teams and agencies.' },
        { t: 'Ongoing support', when: 'Following months', d: 'Release reviews, market support and reporting.' },
      ],
      forTitle: 'Who it’s for',
      forYes: [
        'Brands operating in many markets and languages',
        'Sites on Adobe Experience Manager and other enterprise CMSs',
        'Organisations with several dev teams and agencies',
        'Companies entering new markets',
      ],
      forNo: ['Single-market, single-language businesses'],
      proof: 'Since 2019 I’ve worked on Adobe Experience Manager sites: at IG, then at Accenture Song (technical SEO strategy for international audiences), and today at Philip Morris International.',
      faq: [
        { q: 'Will you work with our agency and dev team?', a: 'Yes, that’s standard on enterprise projects. I write guidelines and tickets, review releases and support teams across countries.' },
        { q: 'Do you only know AEM?', a: 'AEM is where I’m strongest, but international SEO principles are universal. I’ve also worked with WordPress, e-commerce platforms and custom systems.' },
        { q: 'Which languages do you work in?', a: 'Communication and documentation in English or Polish.' },
      ],
    },
  },
  {
    key: 'migration',
    topic: { pl: 'Migracja', en: 'Migration' },
    pl: {
      slug: 'migracja-strony-seo',
      name: 'Migracje i przebudowy stron',
      metaTitle: 'Migracja strony bez utraty ruchu SEO | Maciej Zięciak',
      metaDescription:
        'Migracja strony bez utraty ruchu: zmiana CMS, domeny albo adresów URL. Mapa przekierowań, testy przed startem i opieka po wdrożeniu.',
      eyebrow: 'Migracje i przebudowy stron',
      title: 'Nowa strona. Ten sam ruch. Albo większy.',
      lead:
        'Migracja to najszybszy sposób, żeby w tydzień stracić połowę ruchu. Pilnuję, żeby tak się nie stało: przygotowuję mapę przekierowań, testuję nową wersję przed startem i obserwuję ruch przez kilka tygodni po nim.',
      painTitle: 'Brzmi znajomo?',
      pains: [
        'Zmieniacie CMS, domenę albo strukturę URL i nikt nie odpowiada za SEO.',
        'Agencja robiąca nową stronę mówi, że „przekierowania się dorobi”.',
        'Po poprzedniej przebudowie strony ruch spadł i nigdy w pełni nie wrócił.',
        'Nie wiesz, które stare adresy mają linki i ruch, a które można spokojnie pominąć.',
        'Termin startu jest ustalony, a SEO jest na końcu listy.',
      ],
      getTitle: 'Co dostajesz',
      gets: [
        { t: 'Spis starych adresów', d: 'Wszystkie adresy, które mają ruch, linki albo są w indeksie. Nic wartościowego nie zginie po drodze.' },
        { t: 'Mapę przekierowań 301', d: 'Stary adres → nowy adres, bez łańcuchów i przekierowań na stronę główną.' },
        { t: 'Testy przed startem', d: 'Crawl wersji testowej: przekierowania, canonicale, meta robots, hreflang, mapy witryny i renderowanie.' },
        { t: 'Listę kontrolną na dzień startu', d: 'Co sprawdzić w pierwszej godzinie, pierwszym dniu i pierwszym tygodniu po starcie.' },
        { t: 'Opiekę po wdrożeniu', d: 'Przez kilka tygodni po starcie pilnuję indeksacji, błędów 404, ruchu i pozycji i szybko reaguję na problemy.' },
        { t: 'Raport porównawczy', d: 'Ruch i widoczność przed migracją i po niej, w czytelnej formie dla zarządu.' },
      ],
      stepsTitle: 'Jak to przebiega',
      steps: [
        { t: 'Planowanie', when: 'Jak najwcześniej', d: 'Dołączam na etapie projektu, żeby SEO trafiło do wymagań, a nie do poprawek.' },
        { t: 'Mapa i wymagania', when: 'Przed pracami programistycznymi', d: 'Spis adresów, mapa przekierowań i wymagania SEO dla nowej strony.' },
        { t: 'Testy', when: 'Przed startem', d: 'Crawl i testy wersji testowej oraz lista poprawek przed publikacją.' },
        { t: 'Start i obserwacja', when: 'Start + kilka tygodni', d: 'Kontrola w dniu startu i obserwacja, aż ruch się ustabilizuje.' },
      ],
      forTitle: 'Dla kogo to jest',
      forYes: [
        'Zmiana CMS albo platformy sklepu',
        'Zmiana domeny lub połączenie kilku domen',
        'Nowa struktura adresów albo nowy układ serwisu',
        'Redesign z przebudową szablonów',
      ],
      forNo: ['Zmiana samej grafiki bez zmian w adresach i szablonach'],
      proof: 'Pracowałem z e-commerce na wielu platformach sklepowych i z serwisami enterprise na Adobe Experience Manager, czyli w środowiskach, gdzie zmiany szablonów, struktur i platform to codzienność.',
      faq: [
        { q: 'Kiedy najlepiej się zgłosić?', a: 'Zanim programiści zaczną budować nową stronę. Im później, tym więcej trzeba poprawiać, zamiast od razu zrobić dobrze.' },
        { q: 'Czy da się przeprowadzić migrację bez żadnego spadku?', a: 'Krótkie wahania są normalne, bo Google musi przetworzyć zmiany. Celem jest uniknięcie trwałego spadku i jak najszybszy powrót ruchu.' },
        { q: 'A jeśli migracja już była i ruch spadł?', a: 'Też pomogę. Odtwarzam stare adresy, znajduję brakujące przekierowania i inne błędy, które zabrały ruch.' },
      ],
    },
    en: {
      slug: 'website-migration-seo',
      name: 'Migrations & relaunches',
      metaTitle: 'Website Migration Without Losing Traffic | Maciej Zięciak',
      metaDescription:
        'Website migration without losing organic traffic: a new CMS, domain or URL structure. Redirect mapping, pre-launch testing and post-launch monitoring.',
      eyebrow: 'Migrations & relaunches',
      title: 'New website. Same traffic. Or more.',
      lead:
        'A migration is the fastest way to lose half your traffic in a week. I make sure that doesn’t happen: from the redirect map, through staging tests, to weeks of monitoring after launch.',
      painTitle: 'Sound familiar?',
      pains: [
        'You’re changing CMS, domain or URL structure and nobody owns SEO.',
        'The agency building the new site says “we’ll add redirects later”.',
        'After the last relaunch traffic dropped and never fully came back.',
        'You don’t know which old URLs have links and traffic and which can go.',
        'The launch date is fixed and SEO is at the bottom of the list.',
      ],
      getTitle: 'What you get',
      gets: [
        { t: 'Old URL inventory', d: 'Every URL with traffic, links or index presence. Nothing valuable gets lost.' },
        { t: '301 redirect map', d: 'Old URL → new URL, with no chains and no redirects to the homepage.' },
        { t: 'Pre-launch testing', d: 'A staging crawl: redirects, canonicals, meta robots, hreflang, sitemaps, rendering.' },
        { t: 'Launch-day checklist', d: 'What to check in the first hour, first day and first week after launch.' },
        { t: 'Post-launch monitoring', d: 'Indexation, 404s, traffic and rankings for several weeks, with fast reaction to problems.' },
        { t: 'Before/after report', d: 'Traffic and visibility before and after the migration, in a format the board can read.' },
      ],
      stepsTitle: 'How it works',
      steps: [
        { t: 'Planning', when: 'As early as possible', d: 'I join at the design stage so SEO is in the requirements, not the bug list.' },
        { t: 'Map and requirements', when: 'Before development', d: 'URL inventory, redirect map and SEO requirements for the new site.' },
        { t: 'Testing', when: 'Before launch', d: 'Staging crawl and tests, a fix list before going live.' },
        { t: 'Launch and monitoring', when: 'Launch + several weeks', d: 'Launch-day checks and monitoring until traffic settles.' },
      ],
      forTitle: 'Who it’s for',
      forYes: [
        'Changing CMS or e-commerce platform',
        'Changing domain or merging several domains',
        'New URL structure or information architecture',
        'Redesigns that rebuild templates',
      ],
      forNo: ['Purely visual changes with no URL or template changes'],
      proof: 'I’ve worked with e-commerce on many store platforms and with enterprise sites on Adobe Experience Manager, environments where template, structure and platform changes are part of everyday life.',
      faq: [
        { q: 'When should I get in touch?', a: 'Ideally before development of the new site starts. The later it is, the more has to be fixed instead of designed right from the start.' },
        { q: 'Can a migration happen with no dip at all?', a: 'Short fluctuations are normal while Google processes the changes. The goal is to avoid a lasting drop and recover traffic as fast as possible.' },
        { q: 'What if the migration already happened and traffic dropped?', a: 'I help with that too: recovering old URLs, finding missing redirects and the other errors that took the traffic.' },
      ],
    },
  },
  {
    key: 'ecom',
    topic: { pl: 'E-commerce', en: 'E-commerce' },
    pl: {
      slug: 'seo-ecommerce',
      name: 'SEO dla e-commerce',
      metaTitle: 'SEO dla e-commerce: kategorie i filtry | Maciej Zięciak',
      metaDescription:
        'SEO dla sklepów internetowych: kategorie, filtry, karty produktów i indeksacja. PrestaShop, Magento, WordPress, Shoper, RedCart i systemy autorskie.',
      eyebrow: 'SEO dla e-commerce',
      title: 'Więcej sprzedaży z wyszukiwarki, nie tylko więcej wejść.',
      lead:
        'W sklepie liczy się ruch na kategoriach i produktach, które sprzedają. Porządkuję strukturę, filtry i indeksację tak, żeby Google trafiał tam, gdzie są pieniądze.',
      painTitle: 'Brzmi znajomo?',
      pains: [
        'Filtry tworzą tysiące adresów, które zjadają crawl budget.',
        'Kategorie nie pojawiają się w Google na frazy, na których zarabiasz.',
        'Karty produktów mają opisy od producenta, takie same jak u konkurencji.',
        'Produkty niedostępne zostawiają po sobie 404 albo puste strony.',
        'Platforma sklepu robi z SEO rzeczy, nad którymi nie panujesz.',
      ],
      getTitle: 'Co dostajesz',
      gets: [
        { t: 'Architekturę kategorii', d: 'Struktura kategorii i podkategorii oparta na tym, czego klienci faktycznie szukają.' },
        { t: 'Zasady dla filtrów', d: 'Które kombinacje filtrów indeksować jako strony docelowe, a które ukryć przed botem.' },
        { t: 'Szablony kart produktów', d: 'Tytuły, opisy, dane strukturalne Product i elementy, które pomagają w wynikach.' },
        { t: 'Obsługę niedostępnych produktów', d: 'Zasady dla produktów wycofanych, sezonowych i chwilowo niedostępnych.' },
        { t: 'Wytyczne dla Twojej platformy', d: 'Konkretne ustawienia dla PrestaShop, Magento, WordPressa, Shopera, RedCart albo systemu autorskiego.' },
        { t: 'Priorytety według przychodu', d: 'Najpierw kategorie i produkty z największym potencjałem sprzedaży.' },
      ],
      stepsTitle: 'Jak to przebiega',
      steps: [
        { t: 'Dane sprzedażowe', when: 'Tydzień 1', d: 'Które kategorie i produkty zarabiają, a które mają potencjał.' },
        { t: 'Audyt sklepu', when: 'Tydzień 1–3', d: 'Struktura, filtry, indeksacja, szablony i konfiguracja platformy.' },
        { t: 'Plan', when: 'Tydzień 3–4', d: 'Zadania dla zespołu i treści priorytetowe, ułożone według przychodu.' },
        { t: 'Wdrożenie i pomiar', when: 'Kolejne miesiące', d: 'Wsparcie wdrożeń i pomiar ruchu oraz sprzedaży z wyszukiwarki.' },
      ],
      forTitle: 'Dla kogo to jest',
      forYes: [
        'Sklepy od kilkuset do dziesiątek tysięcy produktów',
        'Sklepy na rynku polskim i zagranicznym',
        'Sklepy z rozbudowanymi filtrami',
        'Marki planujące zmianę platformy',
      ],
      forNo: ['Sklepy z kilkunastoma produktami, gdzie lepiej sprawdzi się kampania płatna'],
      proof: 'W agencji SEO w Krakowie odpowiadałem za SEO sklepów na rynkach polskim i czeskim: audyty, strategie i wdrożenia na PrestaShop, Magento, WordPress, Shoper, RedCart i systemach autorskich.',
      faq: [
        { q: 'Z jakimi platformami pracujesz?', a: 'PrestaShop, Magento, WordPress, Shoper, RedCart i systemy autorskie.' },
        { q: 'Czy piszesz opisy produktów?', a: 'Przygotowuję szablony, wytyczne i priorytety. Same treści mogą pisać Twoi copywriterzy albo wspólnie dobierzemy wykonawcę.' },
        { q: 'Kiedy zobaczę efekty w sprzedaży?', a: 'Poprawki techniczne potrafią zadziałać w kilka tygodni. Na stabilny wzrost ruchu i sprzedaży z wyszukiwarki zwykle czeka się kilka miesięcy.' },
      ],
    },
    en: {
      slug: 'ecommerce-seo',
      name: 'E-commerce SEO',
      metaTitle: 'E-commerce SEO: Categories & Filters | Maciej Zięciak',
      metaDescription:
        'SEO for online stores: categories, faceted navigation, product pages and indexation. PrestaShop, Magento, WordPress, Shoper, RedCart and custom builds.',
      eyebrow: 'E-commerce SEO',
      title: 'More sales from search, not just more visits.',
      lead:
        'In a store what counts is traffic to the categories and products that sell. I fix structure, filters and indexation so Google goes where the money is.',
      painTitle: 'Sound familiar?',
      pains: [
        'Filters generate thousands of URLs that eat your crawl budget.',
        'Categories don’t rank for the queries you sell on.',
        'Product pages use manufacturer copy, identical to your competitors’.',
        'Out-of-stock products leave behind 404s or empty pages.',
        'Your store platform does things to SEO you can’t control.',
      ],
      getTitle: 'What you get',
      gets: [
        { t: 'Category architecture', d: 'A category and subcategory structure based on what customers actually search for.' },
        { t: 'Filter rules', d: 'Which filter combinations become indexable landing pages and which stay hidden from bots.' },
        { t: 'Product page templates', d: 'Titles, descriptions, Product structured data and elements that help in search.' },
        { t: 'Out-of-stock handling', d: 'Rules for discontinued, seasonal and temporarily unavailable products.' },
        { t: 'Guidelines for your platform', d: 'Concrete settings for PrestaShop, Magento, WordPress, Shoper, RedCart or a custom system.' },
        { t: 'Priorities by revenue', d: 'Categories and products with the most sales potential come first.' },
      ],
      stepsTitle: 'How it works',
      steps: [
        { t: 'Sales data', when: 'Week 1', d: 'Which categories and products make money and which have potential.' },
        { t: 'Store audit', when: 'Week 1–3', d: 'Structure, filters, indexation, templates and platform configuration.' },
        { t: 'Plan', when: 'Week 3–4', d: 'Tickets for the team and priority content, ordered by revenue.' },
        { t: 'Rollout and measurement', when: 'Following months', d: 'Release support and measurement of organic traffic and sales.' },
      ],
      forTitle: 'Who it’s for',
      forYes: [
        'Stores with hundreds to tens of thousands of products',
        'Stores selling domestically and abroad',
        'Stores with complex filtering',
        'Brands planning a platform change',
      ],
      forNo: ['Stores with a dozen products, where paid campaigns will do better'],
      proof: 'At an SEO agency in Kraków I ran SEO for online stores in the Polish and Czech markets: audits, strategy and implementation on PrestaShop, Magento, WordPress, Shoper, RedCart and custom platforms.',
      faq: [
        { q: 'Which platforms do you work with?', a: 'PrestaShop, Magento, WordPress, Shoper, RedCart and custom systems.' },
        { q: 'Do you write product descriptions?', a: 'I prepare templates, guidelines and priorities. Your copywriters can write the content, or we can pick someone together.' },
        { q: 'When will I see an effect on sales?', a: 'Technical fixes can show impact within weeks. Sustained growth in organic traffic and sales usually takes a few months.' },
      ],
    },
  },
];

// Polish copy gets Polish typography (no one-letter words at line ends)
export const services: Pair[] = raw.map((p) => ({ ...p, pl: polishTypo(p.pl) }));

export const ui = {
  pl: {
    base: '/uslugi/',
    home: 'Strona główna',
    services: 'Usługi',
    cta: 'Umów bezpłatną konsultację',
    seeWhat: 'Zobacz, co dostajesz',
    more: 'Dowiedz się więcej',
    yes: 'Tak, jeśli',
    no: 'Raczej nie, jeśli',
    proofTitle: 'Dlaczego ja',
    faqTitle: 'Pytania o tę usługę',
    other: 'Pozostałe usługi',
    nextTitle: 'Co się stanie, gdy napiszesz',
    next: [
      { t: 'Krótka rozmowa', d: 'Bezpłatnie, ok. 30 minut. Opowiadasz o serwisie i celach.' },
      { t: 'Propozycja zakresu', d: 'Dostajesz konkretny zakres, termin i wycenę.' },
      { t: 'Start', d: 'Ustalamy dostępy i zaczynam pracę.' },
    ],
  },
  en: {
    base: '/en/services/',
    home: 'Home',
    services: 'Services',
    cta: 'Book a free consultation',
    seeWhat: 'See what you get',
    more: 'Learn more',
    yes: 'A good fit if',
    no: 'Probably not if',
    proofTitle: 'Why me',
    faqTitle: 'Questions about this service',
    other: 'Other services',
    nextTitle: 'What happens when you get in touch',
    next: [
      { t: 'A short call', d: 'Free, about 30 minutes. You tell me about the site and your goals.' },
      { t: 'Scope proposal', d: 'You get a concrete scope, timeline and quote.' },
      { t: 'Kick-off', d: 'We set up access and I start work.' },
    ],
  },
} as const;
