"""Zamockowane endpointy danych (search/export/aggs) dla testów klienta."""

from __future__ import annotations

import json

import httpx

from tests.fake_api import TOKEN

PREFIX = "/api/v2"


def _row(i: int) -> dict:
    return {"url": f"https://ex/{i}", "status_code": 200, "depth": i}


def _search_response(total: int, limit: int, offset: int) -> dict:
    end = min(offset + limit, total)
    rows = [_row(i) for i in range(offset, max(offset, end))]
    return {
        "urls": rows,
        "oql": None,
        "meta": {"columns": ["url", "status_code", "depth"], "total_hits": total},
    }


# Ile wierszy zwraca strumień eksportu (celowo krótki — i tak stopujemy wcześniej).
EXPORT_ROWS = 25


def handler(request: httpx.Request) -> httpx.Response:
    assert request.headers.get("Authorization") == f"Bearer {TOKEN}"
    path = request.url.path
    if path.startswith(PREFIX):
        path = path[len(PREFIX):]
    params = dict(request.url.params)
    body = json.loads(request.content) if request.content else {}

    # Agregacje standardowe.
    if path.endswith("/aggs") and "ranking_performance" not in path:
        return httpx.Response(200, json={"aggs": [{"value": 42, "echo": body}]})

    # Agregacje ranking performance — echo body, by przetestować format.
    if path == "/data/project/p1/ranking_performance/aggs":
        return httpx.Response(200, json={"ranking": True, "echo": body})

    # Eksport strumieniowy (JSONL/CSV).
    if params.get("export") == "true":
        file_type = params.get("file_type", "csv")
        if file_type == "json":
            text = "\n".join(json.dumps(_row(i)) for i in range(EXPORT_ROWS))
        else:
            text = "url,status_code,depth\n" + "\n".join(
                f"https://ex/{i},200,{i}" for i in range(EXPORT_ROWS)
            )
        return httpx.Response(200, text=text)

    # Search — total_hits zależny od crawl_id w ścieżce.
    total = 15000 if "/cbig/" in path else 5
    return httpx.Response(
        200,
        json=_search_response(total, limit=body.get("limit", 100), offset=body.get("offset", 0)),
    )


def make_transport() -> httpx.MockTransport:
    return httpx.MockTransport(handler)
