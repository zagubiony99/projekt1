"""Testy backendu explorera (FastAPI TestClient, bez sieci)."""

import pytest
from fastapi.testclient import TestClient

from app import create_app
from oncrawl.capabilities import Capabilities
from oncrawl.client import OncrawlClient
from oncrawl.config import Settings
from oncrawl.http import OncrawlSession
from discovery import DiscoveryCollector
from tests.fake_api import TOKEN, make_transport as caps_transport
from tests.fake_data import make_transport as data_transport


def _capabilities() -> Capabilities:
    s = Settings(token=TOKEN, base_url="https://app.oncrawl.com/api/v2", cache_dir="/tmp/x", max_retries=0)
    with OncrawlSession(s, transport=caps_transport()) as sess:
        return Capabilities(DiscoveryCollector(sess, cache=False).collect())


@pytest.fixture
def client(tmp_path):
    s = Settings(token=TOKEN, base_url="https://app.oncrawl.com/api/v2",
                 cache_dir=tmp_path / ".cache", max_retries=0)
    api_client = OncrawlClient(OncrawlSession(s, transport=data_transport()))
    app = create_app(
        capabilities=_capabilities(),
        client=api_client,
        presets_path=tmp_path / "presets.json",
        lazy=False,
    )
    return TestClient(app)


def test_projects_endpoint(client):
    r = client.get("/api/projects").json()
    ids = {p["id"] for p in r["projects"]}
    assert {"p1", "p2"} <= ids
    p1 = next(p for p in r["projects"] if p["id"] == "p1")
    assert p1["available_data_types"]["pages"] is True
    assert p1["available_data_types"]["clusters"] is False


def test_crawls_endpoint(client):
    r = client.get("/api/projects/p1/crawls").json()
    assert r["last_finished_crawl_id"] == "c1"
    assert any(c["id"] == "c1" for c in r["crawls"])


def test_fields_endpoint(client):
    r = client.get("/api/fields", params={"project_id": "p1", "data_type": "pages"}).json()
    names = {f["name"] for f in r["fields"]}
    assert "status_code" in names
    assert r["default_display"]


def test_query_ok(client):
    r = client.post("/api/query", json={
        "project_id": "p1", "data_type": "pages", "crawl_id": "c1",
        "fields": ["url", "depth"], "limit": 100,
    })
    assert r.status_code == 200
    body = r.json()
    assert body["total_hits"] == 5
    assert len(body["rows"]) == 5


def test_query_requires_crawl_for_pages(client):
    r = client.post("/api/query", json={"project_id": "p1", "data_type": "pages", "fields": ["url"]})
    assert r.status_code == 400


def test_query_rejects_invalid_oql(client):
    r = client.post("/api/query", json={
        "project_id": "p1", "data_type": "pages", "crawl_id": "c1",
        "fields": ["url"], "oql": {"field": ["ghost_field", "equals", 1]},
    })
    assert r.status_code == 422
    assert "OQL" in r.json()["detail"]


def test_query_accepts_valid_oql(client):
    r = client.post("/api/query", json={
        "project_id": "p1", "data_type": "pages", "crawl_id": "c1",
        "fields": ["url"], "oql": {"field": ["status_code", "equals", 200]},
    })
    assert r.status_code == 200


def test_export_csv(client):
    r = client.post("/api/export", json={
        "project_id": "p1", "data_type": "pages", "crawl_id": "c1",
        "fields": ["url", "depth"], "file_type": "csv",
    })
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("text/csv")
    assert "url,status_code,depth" in r.text


def test_export_xlsx(client):
    r = client.post("/api/export", json={
        "project_id": "p1", "data_type": "pages", "crawl_id": "c1",
        "fields": ["url", "depth"], "file_type": "xlsx",
    })
    assert r.status_code == 200
    assert "spreadsheetml" in r.headers["content-type"]
    assert r.content[:2] == b"PK"  # zip/xlsx magic


def test_presets_crud(client):
    assert client.get("/api/presets").json()["presets"] == []
    q = {"project_id": "p1", "data_type": "pages", "fields": ["url"]}
    r = client.post("/api/presets", json={"name": "moj", "query": q}).json()
    assert len(r["presets"]) == 1
    assert client.get("/api/presets").json()["presets"][0]["name"] == "moj"
    r2 = client.delete("/api/presets/moj").json()
    assert r2["presets"] == []


def test_index_served(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "Oncrawl API Explorer" in r.text


def test_api_error_surfaces_reason_not_generic_500(tmp_path):
    """Błąd z Oncrawl musi dotrzeć z powodem, a nie jako gołe 500."""
    import httpx

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(400, json={
            "type": "invalid_request_parameters",
            "code": None,
            "message": "field sitemaps_file_origin cannot be displayed",
            "fields": ["sitemaps_file_origin"],
        })

    s = Settings(token=TOKEN, base_url="https://app.oncrawl.com/api/v2",
                 cache_dir=tmp_path / ".c", max_retries=0)
    api_client = OncrawlClient(OncrawlSession(s, transport=httpx.MockTransport(handler)))
    app = create_app(capabilities=_capabilities(), client=api_client,
                     presets_path=tmp_path / "p.json", lazy=False)
    c = TestClient(app, raise_server_exceptions=False)

    r = c.post("/api/query", json={
        "project_id": "p1", "data_type": "pages", "crawl_id": "c1",
        "fields": ["url", "sitemaps_file_origin"],
    })
    assert r.status_code == 400                      # nie 500
    body = r.json()
    assert "cannot be displayed" in body["detail"]   # realny powód z API
    assert body["fields"] == ["sitemaps_file_origin"]
    api_client.close()
