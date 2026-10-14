# Marketing: Google Ads, LinkedIn Ads, pomiar

Wszystko, co potrzebne do płatnej promocji maciejzieciak.com: reklamy, słowa kluczowe, rozszerzenia, targetowanie i konfiguracja pomiaru leadów.

| Plik | Co to jest |
|---|---|
| `build_ads.py` | Źródło prawdy dla Google Ads. Waliduje limity znaków i generuje pliki CSV. |
| `google-ads/{pl,en}-ads.csv` | Reklamy elastyczne (RSA): 7 grup reklam na język, po 15 nagłówków i 4 opisy. |
| `google-ads/{pl,en}-keywords.csv` | Słowa kluczowe w dopasowaniu do wyrażenia i ścisłym. |
| `google-ads/{pl,en}-negatives.csv` | Wykluczające słowa kluczowe (praca, kursy, darmowe, „jak zrobić” itd.). |
| `google-ads/{pl,en}-sitelinks.csv` | Linki do podstron (6 usług). |
| `google-ads/{pl,en}-callouts.csv` | Rozszerzenia objaśnień. |
| `google-ads/{pl,en}-snippets.csv` | Rozszerzenie informacji o usługach. |
| `linkedin-ads.md` | Teksty LinkedIn Ads (PL + EN, warianty A/B), targetowanie, Lead Gen Form. |

---

## 0. Zanim wydasz pierwszą złotówkę

Bez tych punktów kampania będzie wydawać pieniądze bez pomiaru albo bez możliwości odpowiedzi na leady.

### Uzupełnij `src/config.ts`

- **`formEndpoint`:**
  - formularz musi wysyłać się bez programu pocztowego (Formspree albo Web3Forms, instrukcja w głównym README);
  - przy `mailto:` część leadów z reklam przepadnie.
- **`gtmId`:**
  - ID kontenera Google Tag Manager, na przykład `GTM-XXXXXXX`;
  - bez niego nie ma pomiaru konwersji ani banera zgody.
- **`email`:** prawdziwy adres. Obecny `kontakt@maciejzieciak.com` to założenie.
- **`bookingUrl` (opcjonalnie):**
  - link do Calendly lub Cal.com;
  - część osób woli od razu wybrać termin.

### Potwierdź obietnice użyte w reklamach

Reklamy obiecują to samo co strona. Jeśli czegoś nie chcesz obiecywać, usuń to w `build_ads.py` **i** na stronie.

- **„Bezpłatna konsultacja 30 min” oraz „3 rzeczy do poprawy”.**
- **„Audyt w 2–3 tygodnie”:** nagłówek w grupie Audyt.
- **„Bez długich umów” / „No Long Contracts”:** callout. Usuń go, jeśli pracujesz na umowach z okresem wypowiedzenia.
- **NDA:** obecne w FAQ na stronie.

### Sprawdź słowa kluczowe w Planerze słów kluczowych Google Ads

To są propozycje oparte na wiedzy branżowej, nie na danych o wolumenie. Usuń frazy z zerowym wolumenem; dodaj te, które Planer podpowie, a które pasują do usług.

### Opublikuj stronę

Kampanie odpalaj dopiero, gdy domena działa po HTTPS, a formularz jest przetestowany prawdziwym wysłaniem.

---

## 1. Pomiar (Google Tag Manager + Consent Mode v2)

### Co już jest na stronie

Działa automatycznie, gdy ustawisz `gtmId`.

- **GTM w trybie „Advanced Consent Mode”.**
  - Domyślnie wszystkie zgody są `denied`.
  - Po kliknięciu „Akceptuję” baner wysyła `consent update = granted`.
  - Wybór zapisuje się w `localStorage`, a przy kolejnej wizycie zgoda jest odtwarzana przed startem GTM.
- **Baner zgody (PL/EN), link „Ustawienia cookies” w stopce i polityka prywatności.**
  - PL: `/polityka-prywatnosci/`, EN: `/en/privacy-policy/`.
- **Zdarzenia w `dataLayer`:**

  | Zdarzenie | Kiedy | Parametry |
  |---|---|---|
  | `generate_lead` | formularz został faktycznie wysłany (odpowiedź 200 z backendu) | `lead_topic`, `language`, `page_path` |
  | `book_call_click` | kliknięcie linku do kalendarza | `page_path` |
  | `email_click` | kliknięcie adresu e-mail albo wysyłka formularza przez program pocztowy | `page_path` |
  | `consent_update` | wybór w banerze | `consent` |

- **Źródło leada w treści zgłoszenia.**
  - Parametry `utm_*`, `gclid` i `li_fat_id` z pierwszego wejścia w sesji oraz strona wejścia dopinają się do formularza jako pole `source`.
  - Dzięki temu w każdym mailu z leadem widać, z jakiej kampanii przyszedł.

### Konfiguracja w GTM (jednorazowo, ok. 30 minut)

1. **Zmienne.** Utwórz 3 zmienne typu „Zmienna warstwy danych”: `lead_topic`, `language` i `page_path`.
2. **Reguły** (typ „Zdarzenie niestandardowe”):
   - `generate_lead`;
   - `book_call_click`.
3. **Tagi:**
   - **Tag Google (GA4):**
     - ID pomiaru `G-…`;
     - reguła: Initialization – All Pages.
   - **GA4 – Zdarzenie `generate_lead`:**
     - parametry: `lead_topic`, `language`, `page_path`;
     - reguła: `generate_lead`;
     - w GA4 oznacz `generate_lead` jako **kluczowe zdarzenie**.
   - **Tag łączący konwersje (Conversion Linker):** reguła All Pages.
   - **Google Ads – Śledzenie konwersji „Lead – formularz”:**
     - identyfikator i etykieta z Google Ads;
     - reguła: `generate_lead`;
     - w Google Ads: kategoria „Przesłanie formularza potencjalnego klienta”, liczenie „Jedna”, **konwersja główna**.
   - **(opcjonalnie) Google Ads – „Klik w kalendarz”:**
     - reguła: `book_call_click`;
     - ustaw jako **konwersję dodatkową**, żeby nie myliła algorytmu stawek.
   - **LinkedIn Insight Tag:**
     - Partner ID z Campaign Manager;
     - reguła: All Pages;
     - w ustawieniach zgody tagu wymagaj zgody `ad_storage`.
   - **LinkedIn – konwersja:**
     - Custom HTML: `<script>window.lintrk && window.lintrk('track', { conversion_id: 1234567 });</script>`;
     - reguła: `generate_lead`;
     - ten sam wymóg zgody `ad_storage`.
4. **Ustawienia zgody.** Włącz „Przegląd zgody” (Consent Overview) w ustawieniach kontenera i sprawdź, że każdy tag ma przypisane wymagania.
   - Tagi Google mają wbudowaną obsługę Consent Mode.
5. **Test:**
   - w trybie podglądu GTM (Tag Assistant) wyślij formularz;
   - tag `generate_lead` musi odpalić się **tylko** po komunikacie o sukcesie;
   - po 24–48 h status konwersji w Google Ads powinien zmienić się na „Rejestruje konwersje”.
6. **Opublikuj kontener.**

### Uwagi

- **Formularz bez `formEndpoint` (`mailto:`) nie wywołuje `generate_lead`.** Nie da się sprawdzić, czy ktoś faktycznie wysłał maila. Dlatego backend formularza to warunek startu kampanii.
- **Enhanced Conversions** (przesyłanie zahaszowanego e-maila leada) to dobry krok na później. Zwiększa liczbę przypisanych konwersji, ale wymaga dopisania tego w polityce prywatności.

---

## 2. Google Ads: struktura i ustawienia

### Struktura

```
PL | Search | Technical SEO        EN | Search | Technical SEO
├─ Konsultant Technical SEO  → /   ├─ Technical SEO Consultant → /en/
├─ Audyt Technical SEO       → /uslugi/audyt-technical-seo/
├─ AI Search                 → /uslugi/widocznosc-w-ai-search/
├─ Duże serwisy              → /uslugi/seo-duzych-serwisow/
├─ Enterprise / międzynarodowe → /uslugi/seo-enterprise-miedzynarodowe/
├─ Migracje                  → /uslugi/migracja-strony-seo/
└─ E-commerce SEO            → /uslugi/seo-ecommerce/        (EN analogicznie: /en/services/…)
```

Każda grupa reklam prowadzi na dedykowaną stronę usługi, a nie na stronę główną. Nagłówek H1 strony odpowiada obietnicy z reklamy, co poprawia Wynik Jakości i współczynnik konwersji.

### Ustawienia kampanii

Te ustawienia nie są w plikach CSV; ustaw je ręcznie w Google Ads Editor lub w panelu.

| Ustawienie | PL | EN |
|---|---|---|
| Typ | Sieć wyszukiwania | Sieć wyszukiwania |
| Partnerzy wyszukiwania / sieć reklamowa | **wyłączone** | **wyłączone** |
| Lokalizacje | Polska | UK, Irlandia, Niemcy, Austria, Szwajcaria, Holandia, Belgia, kraje nordyckie (możesz zacząć od UK + IE) |
| Opcja lokalizacji | „Obecność: osoby znajdujące się w wybranych lokalizacjach lub regularnie w nich przebywające” | to samo |
| Język | polski | angielski |
| Harmonogram | pon–pt 7:00–20:00 (B2B); po miesiącu zweryfikuj w raporcie godzin | jak PL, w strefie czasowej konta |
| Rotacja reklam | „Optymalizuj” | „Optymalizuj” |
| Status przy imporcie | **Wstrzymana**, dopóki pomiar konwersji nie jest sprawdzony | to samo |

### Strategia stawek

1. **Tygodnie 1–4: „Maksymalizacja liczby kliknięć” z limitem maksymalnego CPC.**
   - Limit ustaw na podstawie górnego zakresu stawek z Planera.
   - Cel: zebrać dane i pierwsze konwersje.
2. **Od ~15 konwersji w 30 dniach: „Maksymalizacja liczby konwersji”.**
3. **Od ~30 konwersji w 30 dniach: docelowy CPA (tCPA).**
   - Ustaw go na poziomie realnego kosztu leada z ostatnich 30 dni.
   - Nie obniżaj go o więcej niż 15–20% naraz.

### Budżet i dopasowania

- **Budżet dzienny.** Kampania powinna dostawać co najmniej ~10 kliknięć dziennie, czyli budżet ≈ 10 × średni CPC z Planera. Przy mniejszym budżecie zostaw mniej grup reklam (np. Konsultant, Audyt, Migracje), zamiast rozcieńczać go na 7.
- **Dopasowania.** Tylko do wyrażenia i ścisłe. Dopasowanie przybliżone włącz najwcześniej przy „Maksymalizacji konwersji” i z dobrą listą wykluczeń.

### Rozszerzenia

Są w plikach CSV: linki do podstron, objaśnienia i informacje o usługach. Dodatkowo w panelu:

- **nazwa firmy:** „Maciej Zięciak”;
- **formularz kontaktowy (lead form asset):** dopiero po teście; leady z niego nie przechodzą przez stronę, więc trzeba je pobierać z panelu.

---

## 3. Import do Google Ads Editor

1. Pobierz i zaloguj się do [Google Ads Editor](https://ads.google.com/intl/pl_pl/home/tools/ads-editor/), a potem pobierz konto.
2. **Konto → Importuj → Z pliku.** Importuj w tej kolejności, osobno dla PL i EN:
   1. `*-keywords.csv`: tworzy kampanię i grupy reklam.
   2. `*-ads.csv`.
   3. `*-negatives.csv`.
   4. `*-sitelinks.csv`, `*-callouts.csv`, `*-snippets.csv`.
3. Po imporcie ustaw w kampanii budżet, lokalizacje, język, stawki i harmonogram (tabela wyżej) oraz status **Wstrzymana**.
4. **Sprawdź zmiany → Opublikuj.**
5. Włącz kampanię dopiero, gdy konwersja „Lead – formularz” jest przetestowana.

Jeśli Editor nie przyjmie nagłówka informacji o usługach „Usługi”, wybierz nagłówek „Services”. Wartości w języku polskim zostają.

### Zmiana reklam

1. Edytuj `marketing/build_ads.py`.
2. Uruchom `python3 marketing/build_ads.py`.
3. Skrypt przerywa działanie, jeśli coś przekracza limity, na przykład nagłówek ponad 30 znaków, opis ponad 90 znaków, „!” w nagłówku albo duplikaty.
4. Zaimportuj ponownie zmienione pliki.

---

## 4. LinkedIn Ads

Teksty i targetowanie są w `linkedin-ads.md`. Najważniejsze zasady:

- **Rola LinkedIn.** Docierasz tam do konkretnych stanowisk (Head of SEO, e-commerce, marketing) w firmach o konkretnej wielkości. Kliknięcie jest wyraźnie droższe niż w Google, więc LinkedIn traktuj jako uzupełnienie: budowanie rozpoznawalności, retargeting, ABM.
- **Start.** Jedna kampania PL i jedna EN. Po 2 warianty reklamy na usługę, zaczynając od 2–3 usług z największym potencjałem.
- **Stawki.** „Maksymalna liczba dostarczeń” z limitem kosztu albo ręczne CPC. Nie podnoś budżetu, dopóki koszt leada nie jest znany.
- **UTM-y.** Każdy link musi je mieć (wzór w `linkedin-ads.md`). Pole `source` w zgłoszeniu pokaże wtedy, która reklama przyniosła leada.

---

## 5. Rytm optymalizacji

| Kiedy | Co |
|---|---|
| Codziennie przez pierwszy tydzień | Czy są kliknięcia i wyświetlenia, czy reklamy nie są odrzucone, czy formularz działa. |
| Co tydzień | **Raport wyszukiwanych haseł:** nietrafione hasła dodaj do wykluczeń, dobre do słów kluczowych. Ocena jakości leadów: które grupy dają rozmowy, a które spam. |
| Co 2 tygodnie | Skuteczność komponentów RSA: zamień nagłówki z oceną „Niska” na nowe warianty (w `build_ads.py`). LinkedIn: wyłącz słabszy wariant A/B. |
| Co miesiąc | Przesunięcie budżetu do grup z najniższym kosztem **rozmowy** (nie kliknięcia), przejście na kolejny etap strategii stawek, przegląd harmonogramu i lokalizacji. |

### Wskaźniki, które mają znaczenie

- koszt leada (CPL);
- odsetek leadów, które zamieniają się w rozmowę;
- odsetek rozmów, które zamieniają się w klienta.

Prowadź prostą tabelę leadów z kolumną `source` z maila i notuj, czy z rozmowy był projekt. Po kilku tygodniach zobaczysz, która usługa i który kanał zarabiają, a nie tylko generują kliknięcia.
