"""Testy narzędzi serwera MCP (na mockach, bez sieci i quoty)."""

import json

import pytest

pytest.importorskip("mcp", reason="pakiet mcp opcjonalny")

import mcp_server
from discovery import DiscoveryCollector
from oncrawl.capabilities import Capabilities
from oncrawl.client import OncrawlClient
from oncrawl.config import Settings
from oncrawl.http import OncrawlSession
from tests.fake_api import TOKEN, make_transport as caps_transport
from tests.fake_data import make_transport as data_transport


@pytest.fixture(autouse=True)
def wired_state(tmp_path, monkeypatch):
    """Podmienia capabilities + klienta na wersje z MockTransport."""
    s = Settings(token=TOKEN, base_url="https://app.oncrawl.com/api/v2",
                 cache_dir=tmp_path / ".caps", max_retries=0)
    with OncrawlSession(s, transport=caps_transport()) as sess:
        caps = Capabilities(DiscoveryCollector(sess, cache=False).collect())

    s2 = Settings(token=TOKEN, base_url="https://app.oncrawl.com/api/v2",
                  cache_dir=tmp_path / ".data", max_retries=0)
    client = OncrawlClient(OncrawlSession(s2, transport=data_transport()))

    monkeypatch.setattr(mcp_server.state, "_caps", caps, raising=False)
    monkeypatch.setattr(mcp_server.state, "_client", client, raising=False)
    yield
    client.close()


def _call(tool, **kwargs):
    """Wywołuje funkcję opakowaną dekoratorem @mcp.tool()."""
    fn = getattr(tool, "fn", tool)
    return fn(**kwargs)


def test_list_projects():
    out = json.loads(_call(mcp_server.list_projects))
    ids = {p["id"] for p in out}
    assert {"p1", "p2"} <= ids


def test_list_crawls():
    out = json.loads(_call(mcp_server.list_crawls, project_id="p1"))
    assert out["last_crawl_id"] == "c1"
    assert any(c["id"] == "c1" for c in out["crawls"])


def test_list_fields_and_search():
    out = json.loads(_call(mcp_server.list_fields, project_id="p1", data_type="pages"))
    assert out["count"] == 5
    names = {f["name"] for f in out["fields"]}
    assert "status_code" in names

    filtered = json.loads(
        _call(mcp_server.list_fields, project_id="p1", data_type="pages", search="status")
    )
    assert filtered["count"] == 1
    assert filtered["fields"][0]["name"] == "status_code"


def test_list_fields_unavailable_data_type():
    out = _call(mcp_server.list_fields, project_id="p1", data_type="clusters")
    assert "Brak pól" in out


def test_query_data_uses_last_crawl_when_no_crawl_id():
    out = json.loads(
        _call(mcp_server.query_data, project_id="p1", data_type="pages", fields=["url"])
    )
    assert out["total_hits"] == 5
    assert out["returned"] == 5


def test_query_data_rejects_bad_oql_field():
    out = _call(
        mcp_server.query_data, project_id="p1", data_type="pages",
        fields=["url"], oql={"field": ["ghost", "equals", 1]},
    )
    assert out.startswith("BŁĄD")
    assert "ghost" in out


def test_query_data_accepts_valid_oql():
    out = json.loads(_call(
        mcp_server.query_data, project_id="p1", data_type="pages",
        fields=["url"], oql={"field": ["status_code", "equals", 200]},
    ))
    assert out["total_hits"] == 5


def test_query_limit_is_capped():
    out = json.loads(_call(
        mcp_server.query_data, project_id="p1", data_type="pages",
        fields=["url"], limit=99999,
    ))
    assert out["returned"] <= mcp_server.MAX_ROWS


def test_aggregate_data():
    out = json.loads(_call(
        mcp_server.aggregate_data, project_id="p1", data_type="pages",
        value="depth:avg", group_by=["status_code"],
    ))
    echo = out["aggs"][0]["echo"]["aggs"][0]
    assert echo["value"] == "depth:avg"
    assert echo["fields"] == ["status_code"]


def test_export_data_writes_file(tmp_path):
    target = tmp_path / "out.csv"
    msg = _call(
        mcp_server.export_data, project_id="p1", data_type="pages",
        fields=["url"], out_path=str(target),
    )
    assert "Zapisano" in msg
    assert target.exists()
    assert target.read_text("utf-8").startswith("url,status_code,depth")


def test_unknown_data_type_is_error_not_crash():
    out = _call(mcp_server.query_data, project_id="p1", data_type="nonsense", fields=["url"])
    assert out.startswith("BŁĄD")
