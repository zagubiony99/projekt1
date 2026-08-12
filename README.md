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
