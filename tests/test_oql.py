"""Testy buildera OQL i walidacji względem FieldSet."""

import pytest

from oncrawl.capabilities import FieldSet
from oncrawl.oql import (
    OQLBuilder,
    OQLError,
    and_,
    field,
    or_,
    to_tree,
    validate_tree,
)

FIELDS = FieldSet(
    [
        {"name": "url", "type": "string", "can_filter": True, "can_sort": True},
        {"name": "status_code", "type": "int", "can_filter": True, "can_sort": True},
        {"name": "title", "type": "string", "can_filter": True},
        {"name": "internal_only", "type": "string", "can_filter": False},
    ]
)


def test_leaf_equals():
    assert field("status_code").equals(200).to_tree() == {"field": ["status_code", "equals", 200]}


def test_leaf_has_value_no_third_element():
    assert field("title").has_value().to_tree() == {"field": ["title", "has_value"]}


def test_leaf_between_normalizes_to_list():
    tree = field("status_code").between(200, 299).to_tree()
    assert tree == {"field": ["status_code", "between", [200, 299]]}


def test_leaf_ci_option_is_fourth_element():
    tree = field("url").contains("Blog", ci=True).to_tree()
    assert tree == {"field": ["url", "contains", "Blog", {"ci": True}]}


def test_regex_option():
    tree = field("url").contains("^/blog", regex=True).to_tree()
    assert tree["field"][3] == {"regex": True}


def test_not_prefix_negation():
    assert field("status_code").not_equals(404).to_tree()["field"][1] == "not_equals"


def test_compound_and_or():
    tree = and_(field("status_code").equals(200), field("title").has_value()).to_tree()
    assert set(tree.keys()) == {"and"}
    assert len(tree["and"]) == 2

    tree2 = or_(field("status_code").equals(200), field("status_code").equals(301)).to_tree()
    assert set(tree2.keys()) == {"or"}


def test_between_requires_pair():
    # Poprawne użycie nie rzuca.
    field("status_code").between(200, 299)
    # Skalar zamiast pary — błąd.
    from oncrawl.oql import Leaf

    with pytest.raises(OQLError):
        Leaf("status_code", "between", 200)


def test_unknown_filter_rejected():
    from oncrawl.oql import Leaf

    with pytest.raises(OQLError):
        Leaf("url", "matches", "x")


def test_builder_validates_unknown_field():
    b = OQLBuilder(FIELDS)
    with pytest.raises(OQLError):
        b.field("nonexistent")


def test_builder_validates_non_filterable_field():
    b = OQLBuilder(FIELDS)
    with pytest.raises(OQLError):
        b.field("internal_only")


def test_builder_ok_path():
    b = OQLBuilder(FIELDS)
    tree = b.and_(
        b.field("status_code").equals(200),
        b.field("url").contains("blog", ci=True),
    ).to_tree()
    assert tree["and"][0]["field"] == ["status_code", "equals", 200]


def test_validate_tree_accepts_valid_frontend_tree():
    tree = {"and": [{"field": ["status_code", "gte", 400]}, {"field": ["title", "has_value"]}]}
    validate_tree(tree, FIELDS)  # nie rzuca


def test_validate_tree_rejects_unknown_field():
    with pytest.raises(OQLError):
        validate_tree({"field": ["ghost", "equals", 1]}, FIELDS)


def test_validate_tree_rejects_non_filterable():
    with pytest.raises(OQLError):
        validate_tree({"field": ["internal_only", "equals", "x"]}, FIELDS)


def test_validate_tree_rejects_bad_structure():
    with pytest.raises(OQLError):
        validate_tree({"nonsense": []}, FIELDS)


def test_to_tree_passthrough_dict():
    d = {"field": ["url", "has_value"]}
    assert to_tree(d) is d
    assert to_tree(None) is None
