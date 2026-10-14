# MZ-seo

Strona **maciejzieciak.com**: konsulting Technical SEO & AI Search po polsku i po angielsku.

Zbudowana w [Astro](https://astro.build). Wynikiem jest statyczny HTML z ok. 4 KB JavaScriptu, a fonty są hostowane lokalnie, bez Google Fonts (to ważne pod RODO).

## Uruchomienie

```bash
npm install
npm run dev       # http://localhost:4321
npm run build     # wynik w dist/
npm run preview   # podgląd wersji produkcyjnej
```

## Gdzie co edytować

| Co | Plik |
| --- | --- |
| Imię, e-mail, LinkedIn, zdjęcie | `src/config.ts` |
| Wszystkie teksty PL | `src/i18n/pl.ts` |
| Wszystkie teksty EN | `src/i18n/en.ts` |
| Kolory, font (Geist), przyciski | `src/styles/global.css` (zmienne w `:root`) |
| Sekcje strony | `src/components/*.astro` |
| Interakcje (karta dostępu botów w hero, formularz) | `src/scripts/main.ts` |
| Grafiki do udostępniania (OG) | `public/og-pl.png`, `public/og-en.png` |

## Adresy URL

- `/` to wersja polska (domyślna)
- `/en/` to wersja angielska

Strona ma `hreflang` (pl, en, x-default), canonical, sitemapę z alternatywnymi wersjami językowymi, `robots.txt` i dane strukturalne JSON-LD (Person, ProfessionalService, WebSite, WebPage, FAQPage).

## Wdrożenie

Folder `dist/` to zwykłe pliki statyczne, więc działa na każdym hostingu: Cloudflare Pages, Netlify, Vercel albo GitHub Pages.
Build command: `npm run build`, output: `dist`.

## Do uzupełnienia przed startem

- [ ] Prawdziwy adres e-mail (teraz: `kontakt@maciejzieciak.com`)
- [ ] Link do LinkedIn (pusty = ukryty)
- [ ] Nazwa agencji z lat 2018–2019 (teraz: „Agencja SEO, Kraków”)
- [ ] Potwierdzić, że wymienianie pracodawców (PMI, Accenture Song) na stronie jest OK
