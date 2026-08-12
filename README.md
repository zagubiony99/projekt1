# Oncrawl API Explorer

Lokalne narzędzie do przeglądania i eksportu danych z crawli Oncrawl (REST API v2) —
w stylu Screaming Froga, ale na danych, które Oncrawl już policzył. Plus podgląd tego,
co API w ogóle udostępnia na Twoim koncie.

Stack: Python 3.11+, httpx, pydantic, typer (CLI), FastAPI + uvicorn (backend),
frontend to pojedynczy plik HTML + vanilla JS + Tabulator.js z CDN (bez Reacta, bez builda).
Bez Streamlita/Gradio.

> Status: **Etapy 1–3 gotowe** (discovery, klient, explorer). Live discovery/query
> wymaga dostępu do `app.oncrawl.com` — patrz uwaga o środowisku na końcu.

---

## Szybki start (Etap 1: discovery)

```bash
# 1. Zależności
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Token — wyłącznie w .env, nigdy w kodzie ani w logach
cp .env.example .env
#   ...i wpisz ONCRAWL_TOKEN=... (scope'y do discovery: account:read, projects:read)

# 3. Mapowanie całego konta
python discovery.py

# ...albo tylko wybrany projekt (np. z URL-a w panelu Oncrawl)
python discovery.py --project 690323076e6bbec8f8be7790
```

Wynik:

| plik | co zawiera |
|------|------------|
| `capabilities.json` | pełny, maszynowy zrzut wszystkiego, do czego token ma dostęp |
| `CAPABILITIES.md`   | czytelne tabele pól per projekt i data_type |

Podgląd docelowego kształtu bez uruchamiania (z fixtur): [`CAPABILITIES.sample.md`](CAPABILITIES.sample.md).

### Przydatne flagi

```bash
python discovery.py --workspace WS_ID        # ogranicz do workspace'a
python discovery.py --project P1 --project P2 # kilka konkretnych projektów
python discovery.py --no-cache               # pomiń cache (.cache/)
python discovery.py --from capabilities.json # tylko przerenderuj MD z JSON-a
python discovery.py -v                        # logi DEBUG (bez tokena!)
```

---

## Co robi discovery

Dla wszystkiego, do czego sięga token, zapisuje:

- **workspace'y i projekty** z polami `features`, `limits`, `log_monitoring_ready`,
  `log_monitoring_data_ready`, `crawl_config_ids`, `crawl_ids`, `crawl_over_crawl_ids`;
- **crawl_configs** i ostatnie crawle wraz ze `status` i `end_reason`;
- **`/fields`** dla każdego dostępnego `data_type` ostatniego zakończonego crawla
  (`pages`, `links`, `clusters`, `structured_data`);
- **`/fields` + `/metadata`** dla log monitoringu tam, gdzie `log_monitoring_ready`;
- **`/fields`** dla `ranking_performance` tam, gdzie dostępny.

Każda tabela pól ma kolumny: nazwa, typ, arity, **filtrowalne** (`can_filter`),
**sortowalne** (`can_sort`), **wyświetlalne** (`can_display`), **agregacje**
(`agg_metric_methods`), przykładowe wartości.

**Nic nie jest zgadywane** — listy pól pochodzą wyłącznie z odpowiedzi `/fields`.
Wszystko, co budujemy w Etapach 2–3, opiera się o `capabilities.json`.

> Uwaga o crawlach: `GET /projects/{id}` zwraca tylko `crawl_ids` + `last_crawl_id`
> (nie pełne obiekty crawli). Discovery dociąga szczegóły przez `GET /crawls/{id}`
> i sonduje pola crawla zaczynając od `last_crawl_id`; jeśli jego dane nie są jeszcze
> odpytywalne, przechodzi po `crawl_ids` (od najnowszego) aż `/pages/fields` odpowie 200.

### Graceful degradation

Brak uprawnień, brak feature'a w planie albo wyczerpane dzienne quota **nie wywalają
skryptu** — powód jest zapisywany przy danym zasobie, np.:

```
> ⛔ Niedostępne — HTTP 403 · forbidden · feature_not_available · Clusters niedostępne w tym planie
> ⛔ Niedostępne — HTTP 403 · quota_error · Dzienne quota wyczerpane
```

---

## Etap 2 — klient (`oncrawl/`)

Moduły, na których stoi CLI i explorer:

- **`oncrawl/http.py`** — sesja httpx: `Authorization: Bearer`, retry z backoffem na
  429/5xx (szanuje `Retry-After`), timeouty, cache GET-ów na dysku.
- **`oncrawl/errors.py`** — typowane wyjątki mapujące formaty błędów Oncrawl
  (`unauthorized`, `forbidden`/`feature_not_available`/`no_active_subscription`,
  `quota_error`, `invalid_request`, `resource_not_found`, `duplicate_entry`,
  `invalid_state_for_request`, `internal_error`).
- **`oncrawl/oql.py`** — builder OQL z fluent API + walidacja:
  ```python
  from oncrawl.oql import OQLBuilder
  b = OQLBuilder(fieldset)                       # fieldset z capabilities.json
  oql = b.and_(
      b.field("status_code").equals(200),
      b.field("url").contains("blog", ci=True),
  ).to_tree()
  # -> {"and": [{"field": ["status_code","equals",200]},
  #             {"field": ["url","contains","blog",{"ci":true}]}]}
  ```
  `validate_tree(tree, fieldset)` sprawdza też drzewa przysłane z frontendu
  (istnienie pola, `can_filter`, dozwolony filtr).
- **`oncrawl/capabilities.py`** — `Capabilities.load("capabilities.json")` +
  `FieldSet` (per projekt/data_type) używany do walidacji i budowy panelu filtrów.
- **`oncrawl/client.py`** — `OncrawlClient`:
  - `search(...)` — pojedyncza strona (`rows`, `total_hits`, `columns`);
  - `iter_data(...)` — **sam wykrywa próg 10 000** i przełącza się na
    `export=true` ze strumieniowym parsowaniem JSONL (bez całości w pamięci);
  - `export_lines(...)` — surowy strumień CSV/JSONL;
  - `aggregate(...)` oraz `aggregate_ranking_performance(...)` (osobny format body).

> **Format `sort` w body zapytania o dane.** Dokumentacja precyzuje
> `{name}:{asc|desc}` dla paginacji *zasobów*, ale nie dla search body.
> Klient wysyła więc formę listową `[{"field": …, "order": …}]`, a jeśli API
> odrzuci ją jako niepoprawny parametr (400/422) — automatycznie ponawia
> z formą tekstową i zapamiętuje, który wariant działa. Błędy inne niż
> walidacyjne (np. `quota_error`) nie powodują ponowienia.

## Etap 3 — explorer

Backend FastAPI (`app.py`) + frontend to **jeden plik** `web/index.html`
(vanilla JS + Tabulator.js z CDN, bez Reacta, bez builda).

```bash
python cli.py serve            # -> http://127.0.0.1:8000
# albo:  uvicorn app:app --reload
```

Funkcje UI:

- zakładki **Pages / Links / Clusters / Structured Data / Logs / Ranking Performance**,
  widoczne tylko gdy dostępne w `capabilities.json`;
- **panel filtrów generowany dynamicznie z `/fields`** — kontrolki dobierane do typu
  pola (tekst + operator + `ci`, zakresy numeryczne/dat, bool, enum jako multiselect,
  `ma wartość`/`brak wartości`) i mapowane na OQL;
- wybór kolumn, **sortowanie i paginacja po stronie API**, licznik `total_hits`;
- eksport widocznego zapytania do **CSV i XLSX** przez `export=true`;
- **zapisywane presety** zapytań w lokalnym `presets.json`.

Endpointy backendu: `GET /api/projects`, `GET /api/projects/{id}/crawls`,
`GET /api/fields`, `POST /api/query` (waliduje OQL wzgl. capabilities),
`POST /api/export`, `GET|POST|DELETE /api/presets`.

### 📋 Recipes — gotowe analizy SEO

Przycisk **Recipes** nad tabelą otwiera bibliotekę **92 gotowych analiz**.
Klik = gotowe OQL + właściwe kolumny + sortowanie. Grupy:

| grupa | przykłady |
|-------|-----------|
| **Money pages** | strony z największym ruchem SEO, money pages z błędami, wysoki InRank bez ruchu |
| **Status & redirects** | błędy 4xx/5xx, **404-ki linkowane wewnętrznie**, łańcuchy i pętle przekierowań |
| **Indexability** | noindex, blokada robots.txt, skanonikalizowane, problemy canonical, błędy hreflang |
| **Sitemaps** | **błędy w sitemapie**, przekierowania w sitemapie, noindex w sitemapie, sieroty w sitemapie, indeksowalne strony spoza sitemapy |
| **Content quality** | brak title/description/H1, duplikaty, thin content, near-duplicates, brakujące alty |
| **Internal linking** | strony osierocone, głębokie strony, tylko linki nofollow |
| **Performance** | wolne strony, słabe LCP/CLS, niski performance score |
| **AI crawlers & answers** | 50 analiz — patrz niżej |
| **Googlebot & crawl budget** | nieodwiedzone przez Googlebota, rozbieżny status, gdzie idzie budżet |
| **Logs** | boty trafiające na błędy, wizyty SEO, wolne odpowiedzi serwera |

#### AI crawlers & answers — 50 analiz

Oncrawl wzbogaca dane crawla o pola per bot AI (`logs_bot_hits_*`,
`logs_bot_status_code_*`, `logs_seo_visits_*`), a logi mają `event_bot_kind`
z wartościami `ai search` / `ai training` / `ai user`. To pozwala odpowiedzieć
na pytania, których klasyczne narzędzia SEO nie zadają:

- **`{Bot}` received an error** — bot AI dostał 4xx/5xx zamiast treści.
  Ta strona nigdy nie trafi do odpowiedzi AI. *(per bot: GPTBot, SearchBot,
  ChatGPT-User, ClaudeBot, Claude-SearchBot, Claude-User, PerplexityBot,
  Perplexity-User, Gemini Deep Research, Mistral-User)*
- **`{Bot}` sees a different status than the crawl** — crawl widzi 200,
  a bot AI błąd. Typowo rate limiting albo ochrona antybotowa uderzająca w AI.
- **AI bots hitting errors / redirects** (logi) — to samo od strony zdarzeń;
  część botów AI w ogóle nie podąża za przekierowaniami.
- **`{Źródło}` sends users to a broken page** — asystent cytuje URL, który
  zwraca błąd. Najgorszy scenariusz: AI Cię poleca, użytkownik trafia na 404.
- **Crawled by AI bots but not by Googlebot** oraz odwrotnie — gdzie AI już
  Cię czyta, a klasyczne wyszukiwanie nie (i vice versa).
- **AI bots crawling thin content / noindex pages** — na co boty AI marnują
  budżet; `noindex` ich nie zatrzymuje, potrzeba reguł robots.txt dla ich UA.
- **AI search bots only** vs **AI training crawlers only** — rozdzielenie
  botów zasilających odpowiedzi na żywo od tych zbierających dane treningowe.
- **Live fetches triggered by AI users** — ktoś zapytał asystenta o Twoją
  stronę, a ten pobrał ją na żywo.
- **Traffic arriving from `{Źródło}`** — realne wizyty z ChatGPT / Perplexity /
  Gemini / Claude / Mistral.

Recepty są definiowane w [`oncrawl/recipes.py`](oncrawl/recipes.py) i filtrowane
po stronie API: **pokazują się tylko te, których pola faktycznie istnieją**
w `/fields` danego projektu i `data_type`. Kolumny są przycinane do istniejących,
a sortowanie odpada, gdy pole nie jest sortowalne. Na koncie z pełnym crawlem
+ logami i pełnym zestawem botów AI dostępne są zwykle **63 recepty dla
`pages` (w tym 44 AI) i 10 dla `logs`**.

Testy pilnują niezmiennika: **każde pole użyte w OQL recepty musi być
zadeklarowane w `needs`** — inaczej recepta mogłaby wygenerować zapytanie
o nieistniejące pole (ten test od razu wyłapał dwa takie przypadki).

### Szukanie i filtry

- **🔎 search in URLs…** (pasek narzędzi) — szuka **w danych**, po URL-ach;
  buduje `{"field":["url","contains",…,{"ci":true}]}` i łączy się (AND)
  z filtrami oraz receptą.
- **FILTERS → OQL** (panel po lewej) — filtr po dowolnym polu, kontrolki
  dobierane do typu (tekst + operator, zakresy liczbowe i dat, bool, enum).
- **filter fields…** (pod COLUMNS) — to tylko wyszukiwarka **nazw pól**,
  nie szuka w danych.

## MCP — dane Oncrawl jako narzędzia dla asystenta

`mcp_server.py` wystawia dane przez [Model Context Protocol](https://modelcontextprotocol.io),
więc klient MCP (Claude Desktop, Claude Code, Cursor) może **sam** odpytywać
Oncrawl — np. „ile stron IQOS ma status 404 i jaki mają depth".

Narzędzia: `list_projects`, `list_crawls`, `list_fields`, `query_data`,
`aggregate_data`, `export_data`.

```bash
pip install "mcp>=1.2"
python mcp_server.py          # transport stdio
```

Konfiguracja klienta — skopiuj blok z [`mcp_config.example.json`](mcp_config.example.json):

```json
{
  "mcpServers": {
    "oncrawl": {
      "command": "python",
      "args": ["C:\\sciezka\\do\\OnCrawl\\mcp_server.py"],
      "cwd": "C:\\sciezka\\do\\OnCrawl"
    }
  }
}
```

- Claude Desktop (Windows): `%APPDATA%\Claude\claude_desktop_config.json`
- Claude Desktop (macOS): `~/Library/Application Support/Claude/claude_desktop_config.json`
- Claude Code: `claude mcp add oncrawl -- python /sciezka/do/mcp_server.py`
- Cursor: `.cursor/mcp.json` w projekcie

`cwd` musi wskazywać folder z `.env` i `capabilities.json`. **Tokena nie wpisuje
się do configu** — jest czytany z `.env`, tak jak w reszcie narzędzia.
`query_data` zwraca maks. 200 wierszy (to podgląd dla modelu); pełne zbiory
idą przez `export_data`, które strumieniuje CSV prosto na dysk.

> Uwaga: MCP wymaga **klienta MCP zainstalowanego lokalnie**. Jeśli polityka
> firmowa na to nie pozwala, używaj web explorera (`python cli.py serve`) —
> działa w przeglądarce, bez instalacji. Alternatywa dla zespołów: wystawić
> serwer po HTTP i dodać go w claude.ai jako custom connector (wymaga admina).

## CLI (`cli.py`, typer)

```bash
python cli.py discover [--project ID]          # Etap 1
python cli.py serve --port 8000                # Etap 3
python cli.py projects                          # offline, z capabilities.json
python cli.py fields PROJECT DATA_TYPE          # offline: tabela pól
python cli.py query PROJECT pages --crawl-id C --field url --field status_code \
             --oql '{"field":["status_code","equals",200]}' --limit 20
python cli.py export PROJECT pages out.csv --crawl-id C --field url   # .jsonl = JSONL
```

## Bezpieczeństwo tokena

- Token czytany **tylko** z `ONCRAWL_TOKEN` (env / `.env`).
- `.env`, `.cache/`, `capabilities.json` i `CAPABILITIES.md` są w `.gitignore`.
- Token trafia wyłącznie do nagłówka `Authorization: Bearer …`. Nie jest logowany
  (logi pokazują zamaskowaną formę `abcd…wxyz`) ani zapisywany w wynikach.
  Testy pilnują, że token nie wycieka do `capabilities.json` / `CAPABILITIES.md`.

---

## Architektura

```
discovery.py            # Etap 1 — kolektor + renderer CAPABILITIES.md
cli.py                  # CLI (typer): discover / serve / projects / fields / query / export
app.py                  # Etap 3 — backend FastAPI
web/index.html          # Etap 3 — frontend (jeden plik, Tabulator z CDN)
mcp_server.py           # serwer MCP (opcjonalny) — dane jako narzędzia asystenta
oncrawl/
  config.py             # ładowanie tokena/ustawień z .env, maskowanie sekretu
  errors.py             # typowane wyjątki mapujące formaty błędów Oncrawl
  http.py               # sesja httpx: auth, retry/backoff (429/5xx), cache GET na dysku
  capabilities.py       # loader capabilities.json + FieldSet (walidacja/panel filtrów)
  oql.py                # builder OQL (fluent) + validate_tree
  client.py             # OncrawlClient: search / iter_data(auto-export) / aggregate / ...
tests/
  fake_api.py           # zamockowane API zasobów (httpx.MockTransport) — zero sieci
  fake_data.py          # zamockowane endpointy danych (search/export/aggs)
  test_errors.py test_discovery.py test_oql.py
  test_capabilities.py test_client.py test_app.py test_cli.py
```

---

## Testy

```bash
python -m pytest -q
```

Wszystkie testy działają na **zamockowanych** odpowiedziach (`httpx.MockTransport`),
więc nie zużywają quoty API.

---

## Uwaga o środowisku zdalnym

Jeśli uruchamiasz to w środowisku Claude Code on the web: wychodzące połączenia do
`app.oncrawl.com` mogą być **zablokowane przez politykę egress** — wtedy live discovery
trzeba odpalić lokalnie. Kod, testy i budowa działają w obu miejscach; różnica dotyczy
wyłącznie faktycznego strzału do API.
