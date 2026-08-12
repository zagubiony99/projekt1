"""Testy klienta: search, paginacja, auto-export >10k, agregacje."""

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
