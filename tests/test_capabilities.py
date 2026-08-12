"""Testy loadera/validatora capabilities.json."""

import json

from oncrawl.capabilities import Capabilities, FieldSet
from discovery import DiscoveryCollector
from oncrawl.config import Settings
from oncrawl.http import OncrawlSession
from tests.fake_api import TOKEN, make_transport


def _capabilities_dict() -> dict:
    s = Settings(token=TOKEN, base_url="https://app.oncrawl.com/api/v2", cache_dir="/tmp/x", max_retries=0)
    with OncrawlSession(s, transport=make_transport()) as sess:
        return DiscoveryCollector(sess, cache=False).collect()


def test_fieldset_flags():
    fs = FieldSet([{"name": "a", "can_filter": True, "can_sort": False, "can_display": True, "type": "int"}])
    assert fs.exists("a")
    assert fs.can_filter("a")
    assert not fs.can_sort("a")
    assert fs.can_display("a")
    assert fs.type("a") == "int"
    assert not fs.exists("z")


def test_available_data_types_from_real_discovery():
    cap = Capabilities(_capabilities_dict())
    dts = cap.available_data_types("p1")
    assert dts["pages"] is True
    assert dts["links"] is True
    assert dts["clusters"] is False          # feature_not_available
    assert dts["structured_data"] is True
    assert dts["logs"] is True
    assert dts["ranking_performance"] is False  # quota_error


def test_fieldset_for_pages():
    cap = Capabilities(_capabilities_dict())
    fs = cap.fieldset("p1", "pages")
    assert set(fs.names()) == {"url", "status_code", "fetch_date", "depth", "indexable"}
    assert fs.can_filter("status_code")


def test_fieldset_for_logs():
    cap = Capabilities(_capabilities_dict())
    fs = cap.fieldset("p1", "logs")
    assert "bot" in fs.names()


def test_default_display_prioritizes_common_fields():
    # url/status_code powinny wyprzedzić rzadkie pola alfabetyczne.
    fs = FieldSet([
        {"name": "aaa_rare", "can_display": True},
        {"name": "url", "can_display": True},
        {"name": "status_code", "can_display": True},
        {"name": "zzz_rare", "can_display": True},
    ])
    top = fs.default_display_fields(limit=3)
    assert top[0] == "url"
    assert "status_code" in top
    assert "zzz_rare" not in top


def test_project_summaries():
    cap = Capabilities(_capabilities_dict())
    summaries = cap.project_summaries()
    ids = {s["id"] for s in summaries}
    assert {"p1", "p2"} <= ids
    p1 = next(s for s in summaries if s["id"] == "p1")
    assert p1["available_data_types"]["pages"] is True


def test_load_from_file(tmp_path):
    cap_data = _capabilities_dict()
    fp = tmp_path / "capabilities.json"
    fp.write_text(json.dumps(cap_data), "utf-8")
    cap = Capabilities.load(fp)
    assert cap.project("p1") is not None
