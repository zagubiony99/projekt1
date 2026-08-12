"""Testy wykrywania źródeł danych (dlaczego część analiz jest pusta)."""

import httpx
import pytest
from fastapi.testclient import TestClient

from app import create_app
from discovery import DiscoveryCollector
from oncrawl.capabilities import Capabilities, FieldSet
from oncrawl.client import OncrawlClient
from oncrawl.config import Settings
from oncrawl.datasources import (
    DATA_SOURCES,
    applicable_sources,
    missing_source_for_field,
    probe_oql,
    sources_for,
)
from oncrawl.http import OncrawlSession
from tests.fake_api import TOKEN, make_transport as caps_transport


def _capabilities() -> Capabilities:
    s = Settings(token=TOKEN, base_url="https://app.oncrawl.com/api/v2",
                 cache_dir="/tmp/dscaps", max_retries=0)
    with OncrawlSession(s, transport=caps_transport()) as sess:
        return Capabilities(DiscoveryCollector(sess, cache=False).collect())


def _fieldset(names):
    return FieldSet([{"name": n, "can_filter": True, "can_sort": True, "can_display": True}
                     for n in names])


def test_every_source_is_well_formed():
    for src in DATA_SOURCES:
        assert src["id"] and src["label"] and src["requires"] and src["unlocks"]
        assert src["probe_field"]
        assert src["probe"] in ("has_value", "gt0")
        assert src["data_type"] in ("pages", "logs")


def test_probe_oql_shapes():
    counter = next(s for s in DATA_SOURCES if s["probe"] == "gt0")
    assert probe_oql(counter)["field"][1] == "gt"
    presence = next(s for s in DATA_SOURCES if s["probe"] == "has_value")
    assert probe_oql(presence)["field"][1] == "has_value"


def test_applicable_sources_needs_the_probe_field():
    fs = _fieldset(["url", "seo_visits"])
    ids = {s["id"] for s in applicable_sources(fs, "pages")}
    assert "crawl" in ids and "analytics" in ids
    assert "cwv" not in ids               # brak cwv_lcp
    assert "log_events" not in ids        # to źródło dla data_type=logs


def test_sources_are_split_by_data_type():
    assert {s["id"] for s in sources_for("logs")} == {"log_events"}
    assert "analytics" in {s["id"] for s in sources_for("pages")}


@pytest.mark.parametrize("field,expected", [
    ("seo_visits", "analytics"),
    ("seo_visits_per_day", "analytics"),
    ("googlebot_hits", "logs"),
    ("crawled_by_googlebot", "logs"),
    ("logs_bot_hits_openai_gpt_bot", "ai_bots"),
    ("logs_bot_status_code_claude_bot", "ai_bots"),
    ("logs_seo_visits_openai", "ai_answers"),
    ("cwv_lcp", "cwv"),
    ("sitemaps_file_origin", "sitemaps"),
    ("event_url", "log_events"),
    ("title", None),
])
def test_field_maps_to_its_source(field, expected):
    got = missing_source_for_field(field)
    assert (got["id"] if got else None) == expected


def test_ai_answers_prefix_wins_over_logs_bot():
    """logs_seo_visits_* to ruch z AI, nie odwiedziny bota — kolejność ma znaczenie."""
    assert missing_source_for_field("logs_seo_visits_openai")["id"] == "ai_answers"
    assert missing_source_for_field("logs_bot_hits_openai_gpt_bot")["id"] == "ai_bots"


# --- endpoint ----------------------------------------------------------- #
def _app_with(handler, tmp_path):
    s = Settings(token=TOKEN, base_url="https://app.oncrawl.com/api/v2",
                 cache_dir=tmp_path / ".c", max_retries=0)
    cli = OncrawlClient(OncrawlSession(s, transport=httpx.MockTransport(handler)))
    app = create_app(capabilities=_capabilities(), client=cli,
                     presets_path=tmp_path / "p.json", lazy=False)
    return TestClient(app), cli


def test_endpoint_reports_populated_and_empty(tmp_path):
    """Pole z danymi -> available; pole puste -> available=False + 'requires'."""
    def handler(request: httpx.Request) -> httpx.Response:
        import json as _json
        body = _json.loads(request.content)
        field = body["oql"]["field"][0]
        # url ma dane, reszta nie
        total = 5 if field == "url" else 0
        return httpx.Response(200, json={"urls": [], "meta": {"columns": [], "total_hits": total}})

    client, cli = _app_with(handler, tmp_path)
    sources = client.post("/api/datasources", json={
        "project_id": "p1", "data_type": "pages", "crawl_id": "c1",
    }).json()["sources"]

    by_id = {s["id"]: s for s in sources}
    assert by_id["crawl"]["available"] is True
    assert by_id["crawl"]["rows"] == 5
    # analytics niedostępne — i musi tłumaczyć czego brakuje
    assert by_id["analytics"]["available"] is False
    assert "Analytics" in by_id["analytics"]["requires"]
    assert by_id["analytics"]["unlocks"]
    cli.close()


def test_endpoint_marks_fields_absent_from_schema(tmp_path):
    """Mock ma tylko 5 pól — źródła bez swojego pola są oznaczone, nie pominięte."""
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"urls": [], "meta": {"columns": [], "total_hits": 0}})

    client, cli = _app_with(handler, tmp_path)
    sources = client.post("/api/datasources", json={
        "project_id": "p1", "data_type": "pages", "crawl_id": "c1",
    }).json()["sources"]
    ids = {s["id"] for s in sources}
    assert ids == {s["id"] for s in sources_for("pages")}   # komplet, nic nie zgubione
    missing = [s for s in sources if s.get("missing_field")]
    assert missing and all(s["available"] is False for s in missing)
    cli.close()


def test_endpoint_survives_api_errors(tmp_path):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(403, json={"type": "quota_error", "message": "limit"})

    client, cli = _app_with(handler, tmp_path)
    sources = client.post("/api/datasources", json={
        "project_id": "p1", "data_type": "pages", "crawl_id": "c1",
    }).json()["sources"]
    probed = [s for s in sources if not s.get("missing_field")]
    assert probed and all(s["available"] is False and "error" in s for s in probed)
    cli.close()
