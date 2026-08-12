"""Zamockowane API Oncrawl dla testów — httpx.MockTransport, zero sieci.

Kształty odpowiedzi odwzorowują dokumentację: koperty (workspaces/projects/
project/crawls), /fields z pełnym zestawem flag, błędy {type,code,message}.
Scenariusze braku dostępu są celowo wplecione, by testować graceful degradation:

  * projekt p2  -> 403 forbidden na GET /projects/p2
  * clusters    -> 403 feature_not_available (feature niedostępny)
  * ranking_perf-> 403 quota_error (wyczerpane quota)
"""

from __future__ import annotations

import json

import httpx

TOKEN = "SECRET-TEST-TOKEN-should-never-leak"

PREFIX = "/api/v2"


def _fields(*names_with_flags) -> dict:
    fields = []
    for spec in names_with_flags:
        fields.append(
            {
                "name": spec["name"],
                "type": spec.get("type", "string"),
                "arity": spec.get("arity", "one"),
                "values": spec.get("values"),
                "actions": spec.get("actions", []),
                "agg_dimension": spec.get("agg_dimension", False),
                "agg_metric_methods": spec.get("agg_metric_methods", []),
                "can_display": spec.get("can_display", True),
                "can_filter": spec.get("can_filter", True),
                "can_sort": spec.get("can_sort", True),
            }
        )
    return {"fields": fields}


PAGES_FIELDS = _fields(
    {"name": "url", "type": "string"},
    {"name": "status_code", "type": "int", "agg_metric_methods": ["min", "max", "avg"], "values": [200, 301, 404]},
    {"name": "fetch_date", "type": "date", "can_filter": True, "can_sort": True},
    {"name": "depth", "type": "int", "agg_metric_methods": ["min", "max", "avg", "sum"]},
    {"name": "indexable", "type": "bool", "values": [True, False]},
)
LINKS_FIELDS = _fields(
    {"name": "source", "type": "string"},
    {"name": "target", "type": "string"},
    {"name": "follow", "type": "bool"},
)
STRUCTURED_FIELDS = _fields(
    {"name": "type", "type": "string"},
    {"name": "url", "type": "string"},
)
LOG_EVENTS_FIELDS = _fields(
    {"name": "bot", "type": "string", "values": ["googlebot", "bingbot"]},
    {"name": "hits", "type": "int", "agg_metric_methods": ["sum", "avg"]},
    {"name": "date", "type": "date"},
)
LOG_METADATA = {
    "bot_kinds": ["googlebot", "bingbot"],
    "dates": {"first": "2026-01-01", "last": "2026-08-01"},
    "search_engines": ["google", "bing"],
    "week_definition": "monday",
}

PROJECT_P1 = {
    "project": {
        "id": "p1",
        "name": "example.com",
        "features": {"crawl": True, "log_monitoring": True, "ranking_performance": True},
        "limits": {"max_urls": 500000},
        "log_monitoring_ready": True,
        "log_monitoring_data_ready": True,
        "crawl_config_ids": ["cfg1"],
        "crawl_ids": ["c1", "c0"],
        "crawl_over_crawl_ids": ["coc1"],
    },
    "crawl_configs": [{"id": "cfg1", "name": "Full crawl", "user_agent": "Oncrawl"}],
    "crawls": [
        {"id": "c1", "status": "done", "end_reason": "success", "created_at": "2026-08-01", "ready": True},
        {"id": "c0", "status": "crawling", "end_reason": None, "created_at": "2026-08-10", "ready": False},
    ],
}


def _err(status: int, type_: str, code: str | None, message: str) -> httpx.Response:
    body = {"type": type_, "code": code, "message": message, "fields": None}
    return httpx.Response(status, json=body)


def handler(request: httpx.Request) -> httpx.Response:
    # Twarda asercja: token dociera w nagłówku i nigdzie indziej.
    assert request.headers.get("Authorization") == f"Bearer {TOKEN}"
    path = request.url.path
    if path.startswith(PREFIX):
        path = path[len(PREFIX):]

    routes = {
        "/workspaces": lambda: httpx.Response(200, json={"workspaces": [{"id": "ws1", "name": "Main"}]}),
        "/workspaces/ws1/projects": lambda: httpx.Response(
            200, json={"projects": [{"id": "p1", "name": "example.com"}, {"id": "p2", "name": "locked.com"}]}
        ),
        "/projects/p1": lambda: httpx.Response(200, json=PROJECT_P1),
        "/projects/p2": lambda: _err(403, "forbidden", "unauthorized", "Brak dostępu do projektu"),
        "/data/crawl/c1/pages/fields": lambda: httpx.Response(200, json=PAGES_FIELDS),
        "/data/crawl/c1/links/fields": lambda: httpx.Response(200, json=LINKS_FIELDS),
        "/data/crawl/c1/clusters/fields": lambda: _err(
            403, "forbidden", "feature_not_available", "Clusters niedostępne w tym planie"
        ),
        "/data/crawl/c1/structured_data/fields": lambda: httpx.Response(200, json=STRUCTURED_FIELDS),
        "/data/project/p1/ranking_performance/fields": lambda: _err(
            403, "quota_error", None, "Dzienne quota wyczerpane"
        ),
        "/data/project/p1/log_monitoring/events/fields": lambda: httpx.Response(200, json=LOG_EVENTS_FIELDS),
        "/data/project/p1/log_monitoring/events/metadata": lambda: httpx.Response(200, json=LOG_METADATA),
    }

    route = routes.get(path)
    if route is None:
        return _err(404, "resource_not_found", None, f"Nieznana ścieżka: {path}")
    return route()


def make_transport() -> httpx.MockTransport:
    return httpx.MockTransport(handler)
