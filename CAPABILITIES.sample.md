# CAPABILITIES — Oncrawl API discovery

_Wygenerowano: (PRZYKŁAD z fixtur — nie z żywego konta)_
_Baza API: https://app.oncrawl.com/api/v2_

## Podsumowanie

- Workspace'ów: 1
- Projektów: 2

## Workspace: Main  
`id=ws1`

### 📦 Projekt: example.com

`id=p1`

| właściwość | wartość |
|------------|---------|
| features | {"crawl": true, "log_monitoring": true, "ranking_performance": true} |
| limits | {"max_urls": 500000} |
| log_monitoring_ready | ✅ |
| log_monitoring_data_ready | ✅ |
| crawl_config_ids | 1 |
| crawl_ids | 2 |
| crawl_over_crawl_ids | 1 |
| ostatni zakończony crawl | `c1` |

<details><summary>Crawle (status / end_reason)</summary>

| crawl_id | status | end_reason | ready |
|----------|--------|-----------|:-----:|
| `c1` | done | success | ✅ |
| `c0` | crawling |  | — |

</details>

#### Dane crawla

##### pages

_5 pól_

| pole | typ | arity | filtr | sort | display | agregacje | wartości |
|------|-----|-------|:-----:|:----:|:-------:|-----------|----------|
| `depth` | int | one | ✅ | ✅ | ✅ | min, max, avg, sum |  |
| `fetch_date` | date | one | ✅ | ✅ | ✅ | — |  |
| `indexable` | bool | one | ✅ | ✅ | ✅ | — | True, False |
| `status_code` | int | one | ✅ | ✅ | ✅ | min, max, avg | 200, 301, 404 |
| `url` | string | one | ✅ | ✅ | ✅ | — |  |


##### links

_3 pól_

| pole | typ | arity | filtr | sort | display | agregacje | wartości |
|------|-----|-------|:-----:|:----:|:-------:|-----------|----------|
| `follow` | bool | one | ✅ | ✅ | ✅ | — |  |
| `source` | string | one | ✅ | ✅ | ✅ | — |  |
| `target` | string | one | ✅ | ✅ | ✅ | — |  |


##### clusters

> ⛔ Niedostępne — HTTP 403 · forbidden · feature_not_available · Clusters niedostępne w tym planie


##### structured_data

_2 pól_

| pole | typ | arity | filtr | sort | display | agregacje | wartości |
|------|-----|-------|:-----:|:----:|:-------:|-----------|----------|
| `type` | string | one | ✅ | ✅ | ✅ | — |  |
| `url` | string | one | ✅ | ✅ | ✅ | — |  |


#### Log monitoring

##### events (fields)

_3 pól_

| pole | typ | arity | filtr | sort | display | agregacje | wartości |
|------|-----|-------|:-----:|:----:|:-------:|-----------|----------|
| `bot` | string | one | ✅ | ✅ | ✅ | — | googlebot, bingbot |
| `date` | date | one | ✅ | ✅ | ✅ | — |  |
| `hits` | int | one | ✅ | ✅ | ✅ | sum, avg |  |


<details><summary>events metadata</summary>

```json
{"bot_kinds": ["googlebot", "bingbot"], "dates": {"first": "2026-01-01", "last": "2026-08-01"}, "search_engines": ["google", "bing"], "week_definition": "monday"}
```
</details>

#### Ranking Performance

##### ranking_performance

> ⛔ Niedostępne — HTTP 403 · quota_error · Dzienne quota wyczerpane



### 📦 Projekt: locked.com

`id=p2`

> ⛔ HTTP 403 · forbidden · unauthorized · Brak dostępu do projektu
