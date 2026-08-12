"""Testy discovery end-to-end na zamockowanym API (bez sieci, bez quoty)."""

from pathlib import Path

import pytest

from discovery import DiscoveryCollector, render_markdown
from oncrawl.config import Settings
from oncrawl.http import OncrawlSession
from tests.fake_api import TOKEN, make_transport


@pytest.fixture
def session(tmp_path: Path) -> OncrawlSession:
    settings = Settings(
        token=TOKEN,
        base_url="https://app.oncrawl.com/api/v2",
        cache_dir=tmp_path / ".cache",
        max_retries=0,
    )
    with OncrawlSession(settings, transport=make_transport()) as s:
        yield s


@pytest.fixture
def capabilities(session) -> dict:
    return DiscoveryCollector(session, cache=False).collect()


def test_workspaces_and_projects_enumerated(capabilities):
    assert len(capabilities["workspaces"]) == 1
    ws = capabilities["workspaces"][0]
    assert ws["id"] == "ws1"
    assert len(ws["projects"]) == 2


def test_project_detail_and_flags(capabilities):
    p1 = capabilities["workspaces"][0]["projects"][0]
    assert p1["id"] == "p1"
    assert p1["log_monitoring_ready"] is True
    assert p1["crawl_config_ids"] == ["cfg1"]
    assert p1["domain"] == "example.com"
    assert p1["last_crawl_id"] == "c1"
    # crawl do sondowania pól bierze się z last_crawl_id (dane odpytywalne).
    assert p1["last_finished_crawl_id"] == "c1"


def test_crawls_fetched_with_status(capabilities):
    # /projects/{id} zwraca tylko crawl_ids — szczegóły (status) dociągane z /crawls/{id}.
    p1 = capabilities["workspaces"][0]["projects"][0]
    by_id = {c["id"]: c for c in p1["crawls"]}
    assert by_id["c1"]["status"] == "done"
    assert by_id["c1"]["end_reason"] == "success"
    assert by_id["c0"]["status"] == "crawling"


def test_candidate_crawl_ids_ordering():
    from discovery import DiscoveryCollector

    order = DiscoveryCollector._candidate_crawl_ids("c9", ["c1", "c9", "c2"], cap=6)
    assert order[0] == "c9"                 # last_crawl_id zawsze pierwszy
    assert order == ["c9", "c1", "c2"]      # bez duplikatu c9
    assert DiscoveryCollector._candidate_crawl_ids(None, ["a", "b", "c"], cap=2) == ["a", "b"]


def test_pages_fields_come_from_api_not_guessed(capabilities):
    p1 = capabilities["workspaces"][0]["projects"][0]
    pages = p1["data_types"]["pages"]
    assert pages["available"] is True
    names = {f["name"] for f in pages["fields"]}
    assert names == {"url", "status_code", "fetch_date", "depth", "indexable"}


def test_feature_not_available_recorded_gracefully(capabilities):
    p1 = capabilities["workspaces"][0]["projects"][0]
    clusters = p1["data_types"]["clusters"]
    assert clusters["available"] is False
    assert "feature_not_available" in clusters["reason"]
    assert clusters["fields"] == []


def test_quota_error_recorded_gracefully(capabilities):
    p1 = capabilities["workspaces"][0]["projects"][0]
    rp = p1["ranking_performance"]
    assert rp["available"] is False
    assert "quota_error" in rp["reason"]


def test_project_level_forbidden_recorded(capabilities):
    p2 = capabilities["workspaces"][0]["projects"][1]
    assert p2["id"] == "p2"
    assert p2["error"] is not None
    assert "403" in p2["error"]


def test_log_monitoring_fields_and_metadata(capabilities):
    p1 = capabilities["workspaces"][0]["projects"][0]
    lm = p1["log_monitoring"]
    assert lm["available"] is True
    assert {f["name"] for f in lm["events_fields"]["fields"]} == {"bot", "hits", "date"}
    assert lm["events_metadata"]["metadata"]["week_definition"] == "monday"


def test_markdown_renders_and_hides_no_secret(capabilities):
    md = render_markdown(capabilities)
    assert "# CAPABILITIES" in md
    assert "example.com" in md
    assert "`status_code`" in md
    assert "feature_not_available" in md  # powód zapisany, nie wywalony
    assert TOKEN not in md


def test_json_output_has_no_secret(capabilities):
    import json

    dumped = json.dumps(capabilities)
    assert TOKEN not in dumped
    assert "Authorization" not in dumped


def test_targeted_project_mode(session):
    cap = DiscoveryCollector(session, cache=False).collect(project_ids=["p1"])
    assert cap["workspaces"][0]["projects"][0]["id"] == "p1"


def test_probe_falls_back_when_last_crawl_not_ready(tmp_path):
    """last_crawl_id=cA nie ma odpytywalnych stron (404) -> wybór cB."""
    import httpx

    def handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path.replace("/api/v2", "")
        if path == "/projects/pX":
            return httpx.Response(200, json={"project": {
                "id": "pX", "crawl_ids": ["cA", "cB"], "last_crawl_id": "cA",
                "log_monitoring_ready": False,
            }})
        if path in ("/crawls/cA", "/crawls/cB"):
            return httpx.Response(200, json={"crawl": {"id": path.rsplit("/", 1)[1], "status": "done"}})
        if path == "/data/crawl/cA/pages/fields":
            return httpx.Response(404, json={"type": "resource_not_found", "message": "crawl nie gotowy"})
        if path.startswith("/data/crawl/cB/") and path.endswith("/fields"):
            return httpx.Response(200, json={"fields": [{"name": "url", "type": "string", "can_filter": True}]})
        return httpx.Response(404, json={"type": "resource_not_found"})

    settings = Settings(token=TOKEN, base_url="https://app.oncrawl.com/api/v2",
                        cache_dir=tmp_path / ".cache", max_retries=0)
    with OncrawlSession(settings, transport=httpx.MockTransport(handler)) as s:
        cap = DiscoveryCollector(s, cache=False).collect(project_ids=["pX"])
    px = cap["workspaces"][0]["projects"][0]
    assert px["last_finished_crawl_id"] == "cB"           # przeszło z cA na cB
    assert px["data_types"]["pages"]["available"] is True
