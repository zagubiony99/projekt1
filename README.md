# MZ-seo

Strona **maciejzieciak.com**: konsulting Technical SEO & AI Search po polsku i po angielsku.

Zbudowana w [Astro](https://astro.build). Wynikiem jest statyczny HTML z ok. 9 KB JavaScriptu, a fonty są hostowane lokalnie, bez Google Fonts (to ważne pod RODO).

## Uruchomienie

Wymaga Node.js 22.12 lub nowszego.

```bash
npm install
npm run dev       # http://localhost:4321
npm run build     # wynik w dist/
npm run preview   # podgląd wersji produkcyjnej
```

## Edycja treści: CMS

Wszystkie teksty (PL i EN), usługi i ustawienia kontaktowe edytujesz w przeglądarce, w **Pages CMS**: bez serwera, bez bazy danych, za darmo.

1. Wejdź na **https://app.pagescms.org** i zaloguj się kontem GitHub.
2. Zainstaluj aplikację Pages CMS dla repozytorium `zagubiony99/projekt1` (CMS poprowadzi Cię za rękę).
3. Wybierz repozytorium i gałąź, z której publikuje się strona (np. `main`).
4. Po lewej masz menu:
   - **Ustawienia i kontakt**: e-mail, LinkedIn, zdjęcie, formularz, kalendarz, Google Tag Manager,
   - **Strona główna**: wszystkie teksty po polsku i po angielsku,
   - **Usługi**: 6 podstron usług, każda z wersją polską i angielską.
5. Zmieniasz tekst i klikasz **Save**. CMS zapisuje zmianę w repozytorium, a hosting (Cloudflare Pages / Netlify / Vercel) w ok. minutę publikuje nową wersję strony.

Polskich „sierotek” (w, i, z, o, a na końcu linii) nie musisz pilnować: strona poprawia je sama.

**Czego nie ma w CMS (celowo):** adresy URL podstron (`src/data/routes.ts`: zmiana adresu wymaga przekierowania), treść polityki prywatności (`src/components/Privacy.astro`), wygląd i animacje.

### Pliki z treścią

| Co | Plik |
| --- | --- |
| Ustawienia, kontakt | `content/site.json` |
| Teksty PL / EN | `content/pl.json`, `content/en.json` |
| Usługi (PL + EN w jednym pliku) | `content/services/<klucz>.json` |
| Zdjęcia wgrane w CMS (przy buildzie strona sama je przycina i kompresuje) | `src/assets/media/` |
| Konfiguracja CMS (generowana) | `.pages.yml` ← `scripts/cms/build-config.py` |

Pages CMS zapisuje tylko pola opisane w konfiguracji. Jeśli dodasz w kodzie nowe pole tekstowe, dopisz je w `scripts/cms/build-config.py`, a potem uruchom:

```bash
python3 scripts/cms/build-config.py   # generuje .pages.yml
python3 scripts/cms/check.py          # sprawdza, że zapis w CMS niczego nie skasuje
```

## Gdzie co edytować w kodzie

| Co | Plik |
| --- | --- |
| Adresy podstron usług i tematy formularza | `src/data/routes.ts` |
| Szablon podstrony usługi | `src/components/ServicePage.astro` |
| Kolory (paleta Apple: biel, #f5f5f7, czerń, niebieski + gradient AI), font (SF Pro na Apple, Inter Tight gdzie indziej), przyciski | `src/styles/global.css` (zmienne w `:root`) |
| Sekcje strony | `src/components/*.astro` |
| Interakcje (tekst zapalający się przy scrollu, scena z kartą botów, liczby odliczające w górę, formularz) | `src/scripts/main.ts` |
| Grafiki do udostępniania (OG) | `public/og-pl.png`, `public/og-en.png` |

## Formularz kontaktowy i kalendarz (ważne dla sprzedaży)

W CMS (**Ustawienia i kontakt**) albo w `content/site.json`:
- `formEndpoint` (+ opcjonalnie `formAccessKey`): adres darmowego backendu formularzy, np. Formspree (`https://formspree.io/f/xxxx`) albo Web3Forms (`https://api.web3forms.com/submit` + klucz). Wtedy formularz wysyła się bez opuszczania strony i pokazuje potwierdzenie. Bez tego otwiera program pocztowy, co gubi część zapytań.
- `bookingUrl`: link do Cal.com lub Calendly. Pod formularzem pojawi się „Wolisz od razu wybrać termin?”.
- Po udanej wysyłce strona wysyła zdarzenie `generate_lead` do `dataLayer`, jeśli podłączysz Google Tag Managera.

## Pomiar i reklamy

- `gtmId` (CMS: Ustawienia i kontakt → Google Tag Manager ID) włącza Google Tag Managera z Consent Mode v2, baner zgody (PL/EN) i link „Ustawienia cookies” w stopce. Puste = brak GTM, brak banera, brak cookies.
- Polityka prywatności: `/polityka-prywatnosci/` i `/en/privacy-policy/` (`src/components/Privacy.astro`). Przed startem reklam warto ją uzupełnić o dane firmy i dać do przejrzenia prawnikowi.
- Kampanie Google Ads i LinkedIn Ads, konfiguracja GTM krok po kroku i plan optymalizacji: [`marketing/README.md`](marketing/README.md).

## Adresy URL

- `/` to wersja polska (domyślna)
- `/en/` to wersja angielska
- `/uslugi/<slug>/` i `/en/services/<slug>/` to podstrony usług (6 × 2 języki), każda z danymi Service, BreadcrumbList i FAQPage

Strona ma `hreflang` (pl, en, x-default), canonical, sitemapę z alternatywnymi wersjami językowymi, `robots.txt` i dane strukturalne JSON-LD (Person, ProfessionalService, WebSite, WebPage, FAQPage).

## Kontrola SEO

Po `npm run build` uruchom `python3 scripts/seo-audit.py dist`. Skrypt sprawdza na każdej stronie: canonical, hreflang (wzajemność i x-default), długość title i description, jeden H1, kolejność nagłówków, poprawność JSON-LD, linki wewnętrzne i kotwice, alt obrazów i og:image. Jedyne oczekiwane uwagi dotyczą strony 404 (ma `noindex`, więc celowo nie ma canonical ani hreflang).

Pliki dla wyszukiwarek i AI generują się same przy buildzie: `sitemap-index.xml` (z hreflang dla wszystkich par PL/EN), `robots.txt`, `llms.txt` (mapa serwisu dla asystentów AI) i `404.html`.

## Wdrożenie

Folder `dist/` to zwykłe pliki statyczne, więc działa na każdym hostingu: Cloudflare Pages, Netlify, Vercel albo GitHub Pages.
Build command: `npm run build`, output: `dist`.

## Do uzupełnienia przed startem

- [ ] Prawdziwy adres e-mail (teraz: `kontakt@maciejzieciak.com`)
- [ ] Link do LinkedIn (pusty = ukryty)
- [ ] Nazwa agencji z lat 2018–2019 (teraz: „Agencja SEO, Kraków”)
- [ ] Potwierdzić, że wymienianie pracodawców (PMI, Accenture Song) na stronie jest OK
- [ ] `formEndpoint` i `gtmId` (warunek startu kampanii, patrz `marketing/README.md`)
- [ ] Dane firmy w polityce prywatności
