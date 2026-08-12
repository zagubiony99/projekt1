"""Źródła danych i ich wymagania — dlaczego część analiz bywa pusta.

Crawl Oncrawl sam z siebie wypełnia tylko część pól. Reszta pochodzi
z integracji podpiętych do projektu (analityka, Search Console, logi
serwera). Jeśli integracji nie ma, pola istnieją w /fields, dają się
odpytać i zwracają… zero wierszy. Z punktu widzenia użytkownika wygląda
to jak zepsute narzędzie.

Ten moduł opisuje mapowanie rodzin pól na źródła i pozwala **empirycznie**
sprawdzić, które z nich są w danym crawlu wypełnione — zamiast zgadywać
z konfiguracji konta. Sonda to jedno zapytanie na źródło z filtrem
`has_value` (albo `gt 0` dla liczników) i `limit=1`; liczy się wyłącznie
total_hits.
"""

from __future__ import annotations

from typing import Any

from .capabilities import FieldSet

# Każde źródło: pole-sonda (reprezentatywne dla rodziny), sposób sprawdzenia
# i opis, co odblokowuje. `requires` mówi wprost, czego brakuje.
DATA_SOURCES: list[dict[str, Any]] = [
    {
        "id": "crawl",
        "label": "Crawl data",
        "requires": "a finished crawl",
        "unlocks": "URLs, status codes, titles, headings, content, internal linking, depth",
        "probe_field": "url",
        "probe": "has_value",
        "data_type": "pages",
    },
    {
        "id": "analytics",
        "label": "Analytics (traffic)",
        "requires": "Google Analytics (or another analytics source) connected to the Oncrawl project",
        "unlocks": "seo_visits, seo_visits_per_day — the 'Money pages' recipes",
        "probe_field": "seo_visits",
        "probe": "gt0",
        "data_type": "pages",
    },
    {
        "id": "logs",
        "label": "Log monitoring (Googlebot)",
        "requires": "server log files ingested into the project",
        "unlocks": "googlebot_hits, crawled_by_googlebot — crawl budget analyses",
        "probe_field": "googlebot_hits",
        "probe": "gt0",
        "data_type": "pages",
    },
    {
        "id": "ai_bots",
        "label": "Log monitoring (AI bots)",
        "requires": "server logs, plus AI user agents actually visiting the site",
        "unlocks": "logs_bot_hits_* / logs_bot_status_code_* — the AI crawler recipes",
        "probe_field": "logs_bot_hits_openai_gpt_bot",
        "probe": "gt0",
        "data_type": "pages",
    },
    {
        "id": "ai_answers",
        "label": "Traffic from AI assistants",
        "requires": "server logs with referrers from AI assistants",
        "unlocks": "logs_seo_visits_openai / _perplexity / _gemini / _claude",
        "probe_field": "logs_seo_visits_openai",
        "probe": "gt0",
        "data_type": "pages",
    },
    {
        "id": "cwv",
        "label": "Core Web Vitals",
        "requires": "the CWV/JS feature enabled for the crawl configuration",
        "unlocks": "cwv_lcp, cwv_cls, cwv_performance_score — performance recipes",
        "probe_field": "cwv_lcp",
        "probe": "has_value",
        "data_type": "pages",
    },
    {
        "id": "sitemaps",
        "label": "Sitemaps",
        "requires": "sitemaps discovered or declared in the crawl configuration",
        "unlocks": "sitemaps_file_origin — the Sitemaps recipes",
        "probe_field": "sitemaps_file_origin",
        "probe": "has_value",
        "data_type": "pages",
    },
    {
        "id": "log_events",
        "label": "Raw log events",
        "requires": "log monitoring enabled and processed",
        "unlocks": "the whole 'logs' tab — event_* fields",
        "probe_field": "event_url",
        "probe": "has_value",
        "data_type": "logs",
    },
]


def probe_oql(source: dict) -> dict:
    """Buduje OQL sondy dla danego źródła."""
    field = source["probe_field"]
    if source["probe"] == "gt0":
        return {"field": [field, "gt", 0]}
    return {"field": [field, "has_value"]}


def sources_for(data_type: str) -> list[dict]:
    return [s for s in DATA_SOURCES if s["data_type"] == data_type]


def applicable_sources(fieldset: FieldSet, data_type: str) -> list[dict]:
    """Źródła, których pole-sonda istnieje i da się po nim filtrować."""
    out = []
    for src in sources_for(data_type):
        field = src["probe_field"]
        if fieldset.exists(field) and fieldset.can_filter(field):
            out.append(src)
    return out


def missing_source_for_field(field: str) -> dict | None:
    """Do jakiego źródła należy pole — żeby wyjaśnić puste wyniki.

    Dopasowanie po prefiksach rodzin pól, nie po pojedynczych nazwach.
    """
    prefixes = [
        ("logs_seo_visits_", "ai_answers"),
        ("logs_bot_", "ai_bots"),
        ("googlebot_", "logs"),
        ("crawled_by_googlebot", "logs"),
        ("seo_visits", "analytics"),
        ("cwv_", "cwv"),
        ("sitemaps_", "sitemaps"),
        ("event_", "log_events"),
    ]
    for prefix, source_id in prefixes:
        if field.startswith(prefix):
            return next((s for s in DATA_SOURCES if s["id"] == source_id), None)
    return None
