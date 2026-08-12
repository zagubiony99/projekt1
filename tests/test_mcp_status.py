"""Testy panelu MCP w explorerze (status, konfiguracje, self-test)."""

import json

import pytest
from fastapi.testclient import TestClient

from app import create_app
from oncrawl import mcp_status
from oncrawl.capabilities import Capabilities
from oncrawl.client import OncrawlClient
from oncrawl.config import Settings
from oncrawl.http import OncrawlSession
from discovery import DiscoveryCollector
from tests.fake_api import TOKEN, make_transport as caps_transport
from tests.fake_data import make_transport as data_transport


def _capabilities() -> Capabilities:
    s = Settings(token=TOKEN, base_url="https://app.oncrawl.com/api/v2",
                 cache_dir="/tmp/mcpcaps", max_retries=0)
    with OncrawlSession(s, transport=caps_transport()) as sess:
        return Capabilities(DiscoveryCollector(sess, cache=False).collect())


@pytest.fixture
def client(tmp_path):
    s = Settings(token=TOKEN, base_url="https://app.oncrawl.com/api/v2",
                 cache_dir=tmp_path / ".cache", max_retries=0)
    api_client = OncrawlClient(OncrawlSession(s, transport=data_transport()))
    app = create_app(capabilities=_capabilities(), client=api_client,
                     presets_path=tmp_path / "presets.json", lazy=False)
    yield TestClient(app)
    api_client.close()


def test_status_endpoint_shape(client):
    s = client.get("/api/mcp/status").json()
    assert "ready" in s and isinstance(s["ready"], bool)
    assert s["project_dir"]
    ids = {r["id"] for r in s["requirements"]}
    assert {"mcp_package", "server_file", "env_token", "capabilities"} == ids
    assert {t["name"] for t in s["tools"]} >= {"list_projects", "query_data", "export_data"}


def test_client_configs_are_valid_json_and_tokenless():
    for c in mcp_status.client_configs():
        assert c["name"] and c["steps"] and c["config"]
        # Claude Code to komenda, nie JSON — reszta musi się parsować.
        if c["id"] != "claude_code":
            parsed = json.loads(c["config"])
            assert parsed  # niepusty
        assert TOKEN not in c["config"]
        assert "ONCRAWL_TOKEN" not in c["config"]


def test_vscode_config_uses_workspace_folder():
    cfg = next(c for c in mcp_status.client_configs() if c["id"] == "vscode")
    parsed = json.loads(cfg["config"])
    server = parsed["servers"]["oncrawl"]
    assert server["type"] == "stdio"
    assert server["args"] == ["mcp_server.py"]
    assert server["cwd"] == "${workspaceFolder}"


def test_requirements_flag_missing_token(monkeypatch, tmp_path):
    monkeypatch.delenv("ONCRAWL_TOKEN", raising=False)
    monkeypatch.chdir(tmp_path)  # pusty katalog: brak .env, brak capabilities
    reqs = {r["id"]: r for r in mcp_status.requirements()}
    assert reqs["env_token"]["ok"] is False
    assert reqs["capabilities"]["ok"] is False
    assert reqs["server_file"]["ok"] is False
    assert reqs["env_token"]["hint"]


def test_requirements_detect_env_file(monkeypatch, tmp_path):
    monkeypatch.delenv("ONCRAWL_TOKEN", raising=False)
    (tmp_path / ".env").write_text("ONCRAWL_TOKEN=abc123\n", "utf-8")
    monkeypatch.chdir(tmp_path)
    reqs = {r["id"]: r for r in mcp_status.requirements()}
    assert reqs["env_token"]["ok"] is True


def test_selftest_endpoint_runs(client):
    """Self-test faktycznie startuje serwer i robi handshake."""
    pytest.importorskip("mcp")
    r = client.post("/api/mcp/selftest").json()
    assert r["ok"] is True, r
    assert r["server"]["name"] == "oncrawl"
    assert "query_data" in r["tools"]


def test_selftest_reports_missing_server_file(monkeypatch, tmp_path):
    import asyncio

    monkeypatch.chdir(tmp_path)  # brak mcp_server.py
    out = asyncio.run(mcp_status.run_selftest())
    assert out["ok"] is False
    assert "mcp_server.py" in out["error"]
