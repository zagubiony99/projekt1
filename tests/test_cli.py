"""Testy CLI (typer) — komendy offline czytające capabilities.json."""

import json

from typer.testing import CliRunner

from cli import cli
from oncrawl.config import Settings
from oncrawl.http import OncrawlSession
from discovery import DiscoveryCollector
from tests.fake_api import TOKEN, make_transport

runner = CliRunner()


def _write_caps(tmp_path):
    s = Settings(token=TOKEN, base_url="https://app.oncrawl.com/api/v2", cache_dir="/tmp/x", max_retries=0)
    with OncrawlSession(s, transport=make_transport()) as sess:
        cap = DiscoveryCollector(sess, cache=False).collect()
    fp = tmp_path / "capabilities.json"
    fp.write_text(json.dumps(cap), "utf-8")
    return str(fp)


def test_projects_command(tmp_path):
    caps = _write_caps(tmp_path)
    r = runner.invoke(cli, ["projects", "--capabilities", caps])
    assert r.exit_code == 0
    assert "p1" in r.stdout
    assert "pages" in r.stdout


def test_fields_command(tmp_path):
    caps = _write_caps(tmp_path)
    r = runner.invoke(cli, ["fields", "p1", "pages", "--capabilities", caps])
    assert r.exit_code == 0
    assert "status_code" in r.stdout


def test_fields_command_missing_data_type(tmp_path):
    caps = _write_caps(tmp_path)
    r = runner.invoke(cli, ["fields", "p1", "clusters", "--capabilities", caps])
    # clusters niedostępne (feature_not_available) -> brak pól
    assert r.exit_code == 1


def test_missing_capabilities_file():
    r = runner.invoke(cli, ["projects", "--capabilities", "/nope/capabilities.json"])
    assert r.exit_code == 2
