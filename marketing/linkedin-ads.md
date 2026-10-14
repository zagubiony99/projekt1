# LinkedIn Ads: teksty i targetowanie (PL + EN)

Format: **Single Image Ad** (Sponsored Content) w feedzie. Na start kieruj ruch na stronę usługi.
Gdy będzie dane, przetestuj obok **Lead Gen Form** (formularz w LinkedIn).

## Limity i zasady

- **Tekst wprowadzający (intro).** Limit to 600 znaków. Przed „…więcej” widać około 150, więc hak musi być w pierwszym zdaniu.
- **Nagłówek.** Trzymamy się ≤ 70 znaków, bo dłuższy jest ucinany na mobile.
- **Opis.** Wyświetla się tylko w LinkedIn Audience Network, którą zostawiamy wyłączoną.
- **Przycisk.** „Learn more” / „Dowiedz się więcej” albo „Register” / „Zarejestruj się”. LinkedIn tłumaczy przycisk na język odbiorcy.
- **Grafika.** 1200×1200 (feed mobile) albo 1200×627. Konwencja jak na stronie:
  - czarne albo białe tło;
  - jedno duże zdanie z nagłówka H1 usługi;
  - bez stockowych zdjęć, bez logo klientów.
- **Bez nazw pracodawców w reklamach.** Na stronie są w sekcji doświadczenia, ale w reklamie mogą sugerować rekomendację lub naruszać NDA. Piszemy „doświadczenie enterprise”.
- **Testy A/B.** Każda usługa ma 2 warianty:
  - **A:** hak na problem;
  - **B:** oferta i dowód.

  Po ~2 tygodniach (albo ~1000 wyświetleniach na wariant) wyłącz słabszy według CTR i kosztu leada.

### Linki z UTM

Strona to statyczny HTML, więc UTM-y są jedynym źródłem informacji, skąd przyszedł lead.

```
?utm_source=linkedin&utm_medium=paid_social&utm_campaign=<kampania>&utm_content=<usluga>-<a|b>
```

Przykład:
`https://maciejzieciak.com/uslugi/audyt-technical-seo/?utm_source=linkedin&utm_medium=paid_social&utm_campaign=pl-li-uslugi&utm_content=audyt-a`

---

## Targetowanie

### Kampania PL: `PL | LinkedIn | Technical SEO`

- **Lokalizacja:** Polska (tylko „stała lub niedawna lokalizacja”).
- **Język profilu:** polski.
- **Stanowiska (Job titles):**
  - Head of SEO, SEO Manager, SEO Lead, Kierownik SEO;
  - Head of E-commerce, E-commerce Manager, Dyrektor e-commerce;
  - Head of Digital, Digital Marketing Manager;
  - Marketing Director, Dyrektor marketingu, CMO;
  - Head of Growth;
  - Product Owner (e-commerce / web).
- **Migracje (dodatkowo):** CTO, Head of Product, Web Development Manager.
- **Wielkość firmy:** 51–200, 201–500, 501–1000, 1001–5000, 5001–10 000, 10 001+.
- **Branże:**
  - Retail;
  - Retail Apparel and Fashion;
  - Consumer Services;
  - Software Development;
  - Technology, Information and Internet;
  - Travel Arrangements;
  - Real Estate;
  - Financial Services;
  - Online Audio and Video Media;
  - Book and Periodical Publishing.
- **Wykluczenia:**
  - branże: Marketing Services, Advertising Services (agencje to konkurencja, nie klienci);
  - seniority: Entry, Training;
  - lista firm-konkurentów, wgrana jako Matched Audience.
- **Rozmiar grupy.** Celuj w 20–80 tys. osób. Jeśli wyjdzie mniej, dołóż stanowiska albo zdejmij filtr branż.
- **Audience Expansion i LinkedIn Audience Network:** wyłączone.

### Kampania EN: `EN | LinkedIn | Technical SEO`

- **Lokalizacja:**
  - Wielka Brytania, Irlandia;
  - Niemcy, Austria, Szwajcaria;
  - Holandia, Belgia;
  - Szwecja, Dania, Norwegia, Finlandia;
  - Czechy, Rumunia, kraje bałtyckie.

  Dobrze rozdzielić na 2 kampanie: UK/IE oraz EU, bo mają inne stawki.
- **Język profilu:** angielski.
- **Stanowiska:** jak w PL, w wersji angielskiej, plus:
  - VP Marketing;
  - VP E-commerce;
  - Director of SEO;
  - International SEO Manager.
- **Wielkość firmy:** 201+. Za granicą sprzedajemy przede wszystkim enterprise i projekty wielorynkowe.
- **Branże i wykluczenia:** jak w PL.

### Retargeting

Uruchom dopiero po włączeniu Insight Tag i zgromadzeniu ~300 osób w grupie.

- **Grupy odbiorców:**
  - osoby, które odwiedziły dowolną stronę usługi w ostatnich 90 dniach;
  - z wykluczeniem osób, które wysłały formularz.
- **Reklama:** wariant B danej usługi, bo te osoby znają już problem i potrzebują oferty i dowodu.
- **ABM (opcjonalnie).** Wgraj listę 100–300 firm, z którymi chcesz pracować (Company list), i targetuj tylko stanowiska z listy wyżej.

---

## Teksty: PL

Linki docelowe: `https://maciejzieciak.com/uslugi/<slug>/` + UTM.

### Konsultant Technical SEO (strona główna `/`)

**A**

- **Intro:**
  > Google to już nie jedyne miejsce, w którym szukają Twoi klienci. Pytają też ChatGPT, Perplexity i AI Overviews. Czy Twoja strona jest w odpowiedzi?
  >
  > Pomagam dużym serwisom i sklepom znaleźć i usunąć to, co blokuje ruch z Google i z AI. 9 lat w SEO, doświadczenie enterprise.
- **Nagłówek:** Technical SEO i AI search. Bezpłatna konsultacja 30 min

**B**

- **Intro:**
  > Bez juniora z agencji. Bez 80-stronicowych PDF-ów.
  >
  > Na 30-minutowej konsultacji przejrzę Twoją stronę i wskażę 3 rzeczy, które warto poprawić w pierwszej kolejności. Bez zobowiązań.
- **Nagłówek:** Umów bezpłatną konsultację z konsultantem Technical SEO

### Audyt Technical SEO (`audyt-technical-seo`)

**A**

- **Intro:**
  > Ruch organiczny spada, a nikt nie wie dlaczego?
  >
  > Audyt Technical SEO pokazuje, co naprawdę blokuje Twoją stronę: crawl, rendering JavaScriptu, indeksację, logi serwera. Do tego priorytety według wpływu na ruch i zadania gotowe do wrzucenia w sprint.
- **Nagłówek:** Dowiedz się, co naprawdę blokuje Twój ruch

**B**

- **Intro:**
  > Audyt, który Twój zespół faktycznie wdroży. Zamiast raportu do szuflady dostajesz listę zadań dla devów, ułożoną od największego wpływu na ruch.
  >
  > Zwykle 2–3 tygodnie od otrzymania dostępów.
- **Nagłówek:** Audyt Technical SEO z gotowymi zadaniami dla devów

### AI Search i widoczność w LLM (`widocznosc-w-ai-search`)

**A**

- **Intro:**
  > Twoi klienci pytają ChatGPT, zanim wejdą do Google. Kogo im poleca?
  >
  > Sprawdzam, czy boty AI mogą czytać Twoją stronę, jak AI opisuje Twoją markę i co zmienić, żeby to Ty pojawiał się w odpowiedziach.
- **Nagłówek:** Bądź w odpowiedzi AI, a nie tylko pod nią

**B**

- **Intro:**
  > AI search bez czarów i obietnic „pozycji nr 1 w ChatGPT”.
  >
  > Zaczynam od twardych rzeczy: dostęp botów (GPTBot, OAI-SearchBot, PerplexityBot), renderowanie, dane strukturalne i treści, które modele mogą zacytować.
- **Nagłówek:** Widoczność w ChatGPT, Perplexity i AI Overviews

### Duże serwisy i programmatic SEO (`seo-duzych-serwisow`)

**A**

- **Intro:**
  > Masz setki tysięcy URL-i, a Google indeksuje ułamek?
  >
  > Przy dużej skali problemem nie jest pojedyncza podstrona, tylko szablony, filtry i budżet crawlowania. Rozwijałem serwis do 1,1 mln podstron, więc wiem, gdzie to pęka.
- **Nagłówek:** Skala, która pracuje na ruch, a nie przeciwko niemu

**B**

- **Intro:**
  > Programmatic SEO bez śmieciowych podstron.
  >
  > Pomagam zaplanować i uporządkować szablony, linkowanie wewnętrzne i indeksację tak, żeby każda podstrona miała powód istnieć. Pracuję na danych z crawla i logów serwera.
- **Nagłówek:** SEO dużych serwisów i programmatic SEO

### Enterprise i SEO międzynarodowe (`seo-enterprise-miedzynarodowe`)

**A**

- **Intro:**
  > Jedna marka, kilkanaście rynków i strony, które konkurują ze sobą w Google?
  >
  > Porządkuję hreflang, strukturę domen i procesy wdrożeń w organizacjach, w których SEO dotyka wielu zespołów.
- **Nagłówek:** Jedna marka, wiele rynków. Zero chaosu w wynikach

**B**

- **Intro:**
  > SEO w enterprise to nie tylko technika, to też ludzie i procesy.
  >
  > Mam doświadczenie w dużych organizacjach. Mówię językiem devów, produktu i marketingu, po polsku i po angielsku.
- **Nagłówek:** Konsultant SEO dla marek enterprise

### Migracje i relaunche (`migracja-strony-seo`)

**A**

- **Intro:**
  > Planujesz nową stronę, zmianę CMS-u albo domeny?
  >
  > Większość spadków ruchu po migracji da się przewidzieć i im zapobiec. Plan przekierowań, testy na stagingu, kontrola w dniu startu i monitoring po nim.
- **Nagłówek:** Nowa strona. Ten sam ruch. Albo większy

**B**

- **Intro:**
  > Najtańszy moment na SEO przy migracji to przed startem.
  >
  > Dołączam do projektu na etapie planowania, żeby nowa strona nie zaczynała od zera w Google.
- **Nagłówek:** Migracja strony bez utraty ruchu z Google

### E-commerce SEO (`seo-ecommerce`)

**A**

- **Intro:**
  > Filtry, warianty, paginacja: w sklepie internetowym łatwo wygenerować tysiące podstron, które zjadają budżet crawlowania i nie sprzedają.
  >
  > Porządkuję to tak, żeby Google trafiał na kategorie i produkty, które zarabiają.
- **Nagłówek:** Więcej sprzedaży z wyszukiwarki, nie tylko więcej wejść

**B**

- **Intro:**
  > SEO sklepu liczone w sprzedaży, nie w pozycjach.
  >
  > Technical SEO, architektura kategorii i widoczność produktów w Google i w AI. Zadania gotowe dla Twojego zespołu.
- **Nagłówek:** E-commerce SEO dla dużych sklepów

---

## Teksty: EN (British English)

Linki docelowe: `https://maciejzieciak.com/en/services/<slug>/` + UTM (homepage: `/en/`).

### Technical SEO consultant (`/en/`)

**A**

- **Intro:**
  > Google is no longer the only place your customers search. They ask ChatGPT, Perplexity and AI Overviews too. Is your website in the answer?
  >
  > I help large websites and online shops find and fix what blocks traffic from Google and AI. 9 years in SEO, enterprise experience.
- **Headline:** Technical SEO & AI search. Free 30-min consultation

**B**

- **Intro:**
  > No agency juniors. No 80-page PDFs.
  >
  > In a free 30-minute call I'll review your website and point out the 3 things worth fixing first. No strings attached.
- **Headline:** Book a free call with a senior Technical SEO consultant

### Technical SEO audit (`technical-seo-audit`)

**A**

- **Intro:**
  > Organic traffic dropping and nobody knows why?
  >
  > A Technical SEO audit shows what is really holding your site back: crawling, JavaScript rendering, indexing and server logs. You get priorities by traffic impact and tickets ready for your next sprint.
- **Headline:** Find out what is really holding your traffic back

**B**

- **Intro:**
  > An audit your team will actually implement. Instead of a report that gathers dust, you get dev-ready tickets ordered by impact on traffic.
  >
  > Usually 2–3 weeks from receiving access.
- **Headline:** Technical SEO audit with dev-ready tickets

### AI search & LLM visibility (`ai-search-visibility`)

**A**

- **Intro:**
  > Your customers ask ChatGPT before they ever open Google. Who does it recommend?
  >
  > I check whether AI crawlers can read your site, how AI describes your brand and what to change so you show up in the answers.
- **Headline:** Be in the AI answer, not just below it

**B**

- **Intro:**
  > AI search without the magic tricks or "rank #1 in ChatGPT" promises.
  >
  > I start with the hard stuff: crawler access (GPTBot, OAI-SearchBot, PerplexityBot), rendering, structured data and content that models can cite.
- **Headline:** Visibility in ChatGPT, Perplexity and AI Overviews

### Large sites & programmatic SEO (`large-website-seo`)

**A**

- **Intro:**
  > Hundreds of thousands of URLs, and Google indexes a fraction?
  >
  > At scale the problem is rarely a single page. It's templates, facets and crawl budget. I grew a site to 1.1 million pages, so I know where it breaks.
- **Headline:** Scale that works for your traffic, not against it

**B**

- **Intro:**
  > Programmatic SEO without thin, useless pages.
  >
  > I help you plan and clean up templates, internal linking and indexing so every page has a reason to exist. Based on crawl and server log data.
- **Headline:** SEO for large websites and programmatic SEO

### Enterprise & international SEO (`enterprise-international-seo`)

**A**

- **Intro:**
  > One brand, a dozen markets, and pages competing against each other in Google?
  >
  > I sort out hreflang, domain structure and release processes in organisations where SEO touches many teams.
- **Headline:** One brand, many markets. No chaos in search

**B**

- **Intro:**
  > Enterprise SEO isn't just technical. It's people and processes too.
  >
  > I bring experience from large organisations and speak the language of developers, product and marketing.
- **Headline:** Technical SEO consultant for enterprise brands

### Migrations & relaunches (`website-migration-seo`)

**A**

- **Intro:**
  > Planning a new website, a CMS change or a domain move?
  >
  > Most post-migration traffic drops are predictable and preventable: a redirect plan, staging tests, launch-day checks and monitoring afterwards.
- **Headline:** New website. Same traffic. Or more

**B**

- **Intro:**
  > The cheapest time to think about SEO in a migration is before launch.
  >
  > I join at the planning stage so your new site doesn't start from zero in Google.
- **Headline:** Website migration without losing Google traffic

### E-commerce SEO (`ecommerce-seo`)

**A**

- **Intro:**
  > Filters, variants, pagination: an online shop can easily generate thousands of pages that eat crawl budget and sell nothing.
  >
  > I clean that up so Google lands on the categories and products that make money.
- **Headline:** More sales from search, not just more visits

**B**

- **Intro:**
  > E-commerce SEO measured in revenue, not rankings.
  >
  > Technical SEO, category architecture and product visibility in Google and AI, with tasks ready for your team.
- **Headline:** E-commerce SEO for large online shops

---

## Lead Gen Form (test po pierwszych 2–4 tygodniach)

- **Nagłówek formularza:**
  - PL: „Bezpłatna konsultacja SEO, 30 minut”;
  - EN: „Free 30-minute SEO consultation”.
- **Pola:**
  - z profilu: imię, nazwisko, e-mail służbowy, firma, stanowisko;
  - własne: „Adres strony” / „Website URL” oraz pole wyboru tematu (te same tematy co w formularzu na stronie).
- **Polityka prywatności:**
  - PL: `https://maciejzieciak.com/polityka-prywatnosci/`;
  - EN: `https://maciejzieciak.com/en/privacy-policy/`.
- **Podziękowanie:** link do strony usługi albo do kalendarza (`bookingUrl`).
- **Pobieranie leadów.** Ustaw powiadomienia e-mail o nowych leadach albo podłącz LinkedIn do CRM / Zapier. Lead z LinkedIn trzeba obsłużyć w ciągu kilku godzin, bo później szybko stygnie.
