"""Testy biblioteki recept SEO.

Najważniejszy test: każde pole użyte w OQL recepty jest zadeklarowane
w `needs` — bez tego recepta mogłaby wygenerować zapytanie o pole, którego
w danym projekcie nie ma (dokładnie ten błąd, którego chcemy uniknąć).
"""

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


# --- AI ------------------------------------------------------------------ #
def test_ai_recipes_exist_per_bot_family():
    """Każda rodzina botów AI ma komplet: crawled / error / status mismatch."""
    from oncrawl.recipes import AI_BOT_FAMILIES

    ids = {r["id"] for r in RECIPES}
    for key, _name in AI_BOT_FAMILIES:
        assert f"ai_crawled_{key}" in ids
        assert f"ai_errors_{key}" in ids, f"brak recepty na błędy dla {key}"
        assert f"ai_status_mismatch_{key}" in ids


def test_ai_answer_sources_have_traffic_and_broken_recipes():
    from oncrawl.recipes import AI_ANSWER_SOURCES

    ids = {r["id"] for r in RECIPES}
    for key, _name in AI_ANSWER_SOURCES:
        assert f"ai_visits_{key}" in ids
        assert f"ai_visits_broken_{key}" in ids


def test_ai_log_recipes_cover_errors_and_kinds():
    ids = {r["id"] for r in RECIPES}
    assert "log_ai_bots_errors" in ids       # boty AI dostające 404 — wprost proszone
    assert "log_ai_bots_redirects" in ids
    assert "log_ai_search_vs_training" in ids
    assert "log_ai_training_bots" in ids
    assert "log_ai_user_fetches" in ids


def test_ai_bot_recipe_degrades_when_family_missing():
    """Brak jednej rodziny botów nie może ukryć recept dla pozostałych."""
    fs = _fieldset_from([
        "url", "status_code",
        "logs_bot_hits_openai_gpt_bot", "logs_bot_status_code_openai_gpt_bot",
        # brak jakichkolwiek pól Claude
    ])
    got = {r["id"] for r in applicable_recipes(fs, "pages")}
    assert "ai_crawled_openai_gpt_bot" in got
    assert "ai_errors_openai_gpt_bot" in got
    assert "ai_crawled_claude_bot" not in got
    assert "ai_errors_claude_bot" not in got


def test_ai_group_is_substantial():
    ai = [r for r in RECIPES if r["group"] == "AI crawlers & answers"]
    assert len(ai) >= 40
