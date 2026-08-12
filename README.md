# Oncrawl API Explorer

Lokalne narzędzie do przeglądania i eksportu danych z crawli Oncrawl (REST API v2) —
w stylu Screaming Froga, ale na danych, które Oncrawl już policzył. Plus podgląd tego,
co API w ogóle udostępnia na Twoim koncie.

Stack: Python 3.11+, httpx, pydantic, typer (CLI), FastAPI + uvicorn (backend),
frontend to pojedynczy plik HTML + vanilla JS + Tabulator.js z CDN (bez Reacta, bez builda).
Bez Streamlita/Gradio.

> Status: **Etap 1 (discovery) gotowy.** Etapy 2 (klient) i 3 (explorer) — po akceptacji.

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

### Graceful degradation

Brak uprawnień, brak feature'a w planie albo wyczerpane dzienne quota **nie wywalają
skryptu** — powód jest zapisywany przy danym zasobie, np.:

```
> ⛔ Niedostępne — HTTP 403 · forbidden · feature_not_available · Clusters niedostępne w tym planie
> ⛔ Niedostępne — HTTP 403 · quota_error · Dzienne quota wyczerpane
```

---

## Bezpieczeństwo tokena

- Token czytany **tylko** z `ONCRAWL_TOKEN` (env / `.env`).
- `.env`, `.cache/`, `capabilities.json` i `CAPABILITIES.md` są w `.gitignore`.
- Token trafia wyłącznie do nagłówka `Authorization: Bearer …`. Nie jest logowany
  (logi pokazują zamaskowaną formę `abcd…wxyz`) ani zapisywany w wynikach.
  Testy pilnują, że token nie wycieka do `capabilities.json` / `CAPABILITIES.md`.

---

## Architektura (na teraz)

```
discovery.py            # Etap 1 — kolektor + renderer CAPABILITIES.md
oncrawl/
  config.py             # ładowanie tokena/ustawień z .env, maskowanie sekretu
  errors.py             # typowane wyjątki mapujące formaty błędów Oncrawl
  http.py               # sesja httpx: auth, retry/backoff (429/5xx), cache GET na dysku
tests/
  fake_api.py           # zamockowane API (httpx.MockTransport) — zero sieci, zero quoty
  test_errors.py        # mapowanie błędów
  test_discovery.py     # discovery end-to-end na mockach + brak wycieku tokena
```

Warstwa `oncrawl/http.py` + `oncrawl/errors.py` to fundament, na którym w Etapie 2
powstanie pełny `oncrawl/client.py` (iteratory paginacji, `fetch_data()` z auto-przełączaniem
na `export=true` powyżej 10k, builder OQL walidujący pola względem `capabilities.json`,
helper agregacji z osobną ścieżką dla `ranking_performance`).

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
