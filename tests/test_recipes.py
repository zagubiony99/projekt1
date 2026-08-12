"""Testy biblioteki recept SEO.

Najważniejszy test: każde pole użyte w OQL recepty jest zadeklarowane
w `needs` — bez tego recepta mogłaby wygenerować zapytanie o pole, którego
w danym projekcie nie ma (dokładnie ten błąd, którego chcemy uniknąć).
"""

import pytest

from oncrawl.capabilities import FieldSet
from oncrawl.oql import validate_tree
from oncrawl.recipes import GROUPS, RECIPES, _fields_in_oql, applicable_recipes


def _fieldset_from(names, **flags):
    base = {"can_filter": True, "can_sort": True, "can_display": True}
    base.update(flags)
    return FieldSet([{"name": n, "type": "string", **base} for n in names])


def test_recipe_ids_unique():
    ids = [r["id"] for r in RECIPES]
    assert len(ids) == len(set(ids))


def test_every_oql_field_is_declared_in_needs():
    for rec in RECIPES:
        used = set(_fields_in_oql(rec["oql"]))
        declared = set(rec["needs"])
        missing = used - declared
        assert not missing, f"{rec['id']}: OQL używa pól spoza needs: {missing}"


def test_every_recipe_oql_is_structurally_valid():
    for rec in RECIPES:
        fs = _fieldset_from(rec["needs"])
        validate_tree(rec["oql"], fs)  # rzuci OQLError przy złym filtrze/kształcie


def test_every_recipe_has_url_like_column():
    for rec in RECIPES:
        assert rec["columns"], f"{rec['id']}: brak kolumn"
        assert any(c in ("url", "event_url") for c in rec["columns"]), rec["id"]


def test_every_group_is_known():
    for rec in RECIPES:
        assert rec["group"] in GROUPS, f"{rec['id']}: nieznana grupa {rec['group']}"


def test_sort_field_is_in_columns_or_needs():
    for rec in RECIPES:
        if not rec.get("sort"):
            continue
        field = rec["sort"].split(":")[0]
        assert field in rec["columns"] or field in rec["needs"], f"{rec['id']}: sort po {field}"


def test_recipe_descriptions_present():
    for rec in RECIPES:
        assert rec["why"].strip(), f"{rec['id']}: brak opisu"
        assert rec["label"].strip()


# --- filtrowanie względem realnych pól ---------------------------------- #
def test_applicable_hides_recipes_with_missing_fields():
    fs = _fieldset_from(["url", "status_code"])
    got = {r["id"] for r in applicable_recipes(fs, "pages")}
    assert "errors_4xx_5xx" in got            # ma url + status_code
    assert "money_pages" not in got           # brak seo_visits
    assert "sitemap_errors" not in got        # brak sitemaps_file_origin


def test_applicable_filters_columns_to_existing_fields():
    fs = _fieldset_from(["url", "status_code", "depth"])
    rec = next(r for r in applicable_recipes(fs, "pages") if r["id"] == "errors_4xx_5xx")
    assert set(rec["columns"]) <= {"url", "status_code", "depth"}
    assert "nb_inlinks" not in rec["columns"]  # nie istnieje -> przycięte


def test_applicable_drops_sort_when_field_not_sortable():
    fs = FieldSet([
        {"name": "url", "can_filter": True, "can_sort": True, "can_display": True},
        {"name": "status_code", "can_filter": True, "can_sort": True, "can_display": True},
        {"name": "nb_inlinks", "can_filter": True, "can_sort": False, "can_display": True},
    ])
    rec = next(r for r in applicable_recipes(fs, "pages") if r["id"] == "errors_4xx_5xx")
    assert rec["sort"] is None                 # nb_inlinks nie jest sortowalne


def test_applicable_skips_non_filterable_oql_field():
    fs = FieldSet([
        {"name": "url", "can_filter": True, "can_sort": True, "can_display": True},
        {"name": "status_code", "can_filter": False, "can_sort": True, "can_display": True},
    ])
    got = {r["id"] for r in applicable_recipes(fs, "pages")}
    assert "errors_4xx_5xx" not in got


def test_data_type_separation():
    log_fields = _fieldset_from(["event_url", "event_status_code", "event_is_bot_hit"])
    got = {r["id"] for r in applicable_recipes(log_fields, "logs")}
    assert "log_bot_errors" in got
    assert "errors_4xx_5xx" not in got         # to recepta dla 'pages'


def test_pages_recipes_cover_key_scenarios():
    """Scenariusze, o które prosił użytkownik, faktycznie istnieją."""
    ids = {r["id"] for r in RECIPES}
    assert "money_pages" in ids                # najwięcej ruchu
    assert "sitemap_errors" in ids             # 404 w sitemapie
    assert "errors_with_inlinks" in ids        # odniesienia do 404
    assert len(RECIPES) >= 20                  # "takie nie wiem 20 przykładów"


def test_recipes_have_reasonable_coverage_per_group():
    groups = {r["group"] for r in RECIPES}
    assert len(groups) >= 7
