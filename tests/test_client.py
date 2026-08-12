"""Testy klienta: search, paginacja, auto-export >10k, agregacje."""

import json

import pytest

from oncrawl.client import OncrawlClient, crawl_data_path, ranking_path
from oncrawl.config import Settings
from oncrawl.http import OncrawlSession
from tests.fake_data import make_transport
from tests.fake_api import TOKEN


@pytest.fixture
def client(tmp_path):
    s = Settings(token=TOKEN, base_url="https://app.oncrawl.com/api/v2",
                 cache_dir=tmp_path / ".cache", max_retries=0)
    with OncrawlClient(OncrawlSession(s, transport=make_transport())) as c:
        yield c


def test_search_single_page(client):
    res = client.search(crawl_data_path("csmall", "pages"), fields=["url", "depth"], limit=100)
    assert res["total_hits"] == 5
    assert len(res["rows"]) == 5
    assert res["columns"] == ["url", "status_code", "depth"]


def test_search_guards_pagination_limit(client):
    with pytest.raises(ValueError):
        client.search(crawl_data_path("csmall", "pages"), fields=["url"], limit=1000, offset=9999)


def test_iter_data_pages_under_10k(client):
    rows = list(client.iter_data(crawl_data_path("csmall", "pages"), fields=["url"], page_size=2))
    assert len(rows) == 5                       # 2 + 2 + 1
    assert rows[0]["url"] == "https://ex/0"
    assert rows[-1]["url"] == "https://ex/4"


def test_iter_data_switches_to_export_above_10k(client):
    # total_hits=15000 dla crawl 'cbig' -> ścieżka eksportu; stopujemy na max_rows.
    rows = list(client.iter_data(crawl_data_path("cbig", "pages"), fields=["url"], max_rows=3))
    assert len(rows) == 3
    assert rows[0] == {"url": "https://ex/0", "status_code": 200, "depth": 0}


def test_export_lines_raw_csv(client):
    lines = list(client.export_lines(crawl_data_path("csmall", "pages"), fields=["url"], file_type="csv"))
    assert lines[0].startswith("url,status_code,depth")
    assert len(lines) == 26                      # nagłówek + 25 wierszy


def test_iter_export_parses_jsonl(client):
    rows = list(client.iter_export(crawl_data_path("csmall", "pages"), fields=["url"], file_type="json"))
    assert len(rows) == 25
    assert all("url" in r for r in rows)


def test_aggregate_standard(client):
    res = client.aggregate(crawl_data_path("csmall", "pages"),
                           aggs=[{"oql": None, "fields": ["status_code"], "value": "depth:avg"}])
    assert res["aggs"][0]["value"] == 42
    assert res["aggs"][0]["echo"]["aggs"][0]["value"] == "depth:avg"


def test_aggregate_ranking_performance_format(client):
    res = client.aggregate_ranking_performance(
        "p1",
        value=[{"field": "clicks", "method": "sum", "alias": "total_clicks"}],
        sort="total_clicks:desc",
        limit=10,
        post_aggs_oql={"field": ["total_clicks", "gt", 100]},
    )
    assert res["ranking"] is True
    echo = res["echo"]
    assert echo["value"][0]["alias"] == "total_clicks"
    assert echo["sort"] == "total_clicks:desc"
    assert echo["post_aggs_oql"] == {"field": ["total_clicks", "gt", 100]}
    # sort/offset nie powinny wyciekać jako None
    assert "offset" not in echo


def test_ranking_path_builder():
    assert ranking_path("p1") == "/data/project/p1/ranking_performance"


# --- format `sort` w body search --------------------------------------- #
def _sort_probe_transport(accepted_style):
    """Mock akceptujący tylko jeden format `sort`; zapisuje otrzymane body."""
    import httpx
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        seen.append(body)
        sort = body.get("sort")
        style = "list" if isinstance(sort, list) else "string" if isinstance(sort, str) else None
        if style is not None and style != accepted_style:
            return httpx.Response(422, json={
                "type": "invalid_request_parameters",
                "message": f"sort: expected {accepted_style} form",
                "fields": ["sort"],
            })
        return httpx.Response(200, json={
            "urls": [{"url": "https://ex/0"}],
            "meta": {"columns": ["url"], "total_hits": 1},
        })

    return httpx.MockTransport(handler), seen


def _client_with(transport, tmp_path):
    s = Settings(token=TOKEN, base_url="https://app.oncrawl.com/api/v2",
                 cache_dir=tmp_path / ".c", max_retries=0)
    return OncrawlClient(OncrawlSession(s, transport=transport))


def test_sort_uses_list_form_when_api_accepts_it(tmp_path):
    transport, seen = _sort_probe_transport("list")
    with _client_with(transport, tmp_path) as c:
        res = c.search(crawl_data_path("c1", "pages"), fields=["url"], sort="depth:desc")
    assert res["total_hits"] == 1
    assert seen[0]["sort"] == [{"field": "depth", "order": "desc"}]
    assert len(seen) == 1                      # bez zbędnego retry


def test_sort_falls_back_to_string_form(tmp_path):
    transport, seen = _sort_probe_transport("string")
    with _client_with(transport, tmp_path) as c:
        res = c.search(crawl_data_path("c1", "pages"), fields=["url"], sort="depth:desc")
    assert res["total_hits"] == 1
    assert isinstance(seen[0]["sort"], list)   # najpierw lista
    assert seen[1]["sort"] == "depth:desc"     # potem fallback
    assert c._sort_style == "string"


def test_sort_style_is_remembered_after_fallback(tmp_path):
    transport, seen = _sort_probe_transport("string")
    with _client_with(transport, tmp_path) as c:
        c.search(crawl_data_path("c1", "pages"), fields=["url"], sort="depth:desc")
        seen.clear()
        c.search(crawl_data_path("c1", "pages"), fields=["url"], sort="inrank:asc")
    assert len(seen) == 1                      # drugi raz już bez próbowania listy
    assert seen[0]["sort"] == "inrank:asc"


def test_no_sort_means_no_sort_key(tmp_path):
    transport, seen = _sort_probe_transport("list")
    with _client_with(transport, tmp_path) as c:
        c.search(crawl_data_path("c1", "pages"), fields=["url"])
    assert "sort" not in seen[0]


def test_non_validation_error_is_not_retried(tmp_path):
    import httpx
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(1)
        return httpx.Response(403, json={"type": "quota_error", "message": "daily limit"})

    with _client_with(httpx.MockTransport(handler), tmp_path) as c:
        with pytest.raises(Exception):
            c.search(crawl_data_path("c1", "pages"), fields=["url"], sort="depth:desc")
    assert len(calls) == 1                     # 403 nie uzasadnia zmiany formatu


def test_parse_sort_variants():
    from oncrawl.client import parse_sort
    assert parse_sort("depth:desc") == ("depth", "desc")
    assert parse_sort("depth") == ("depth", "asc")
    assert parse_sort("depth:bogus") == ("depth", "asc")
