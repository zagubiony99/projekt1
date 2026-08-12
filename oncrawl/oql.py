"""Builder OQL (Oncrawl Query Language) z fluent API + walidacja.

OQL to drzewo JSON:

  * liść:     {"field": [nazwa, filtr, wartość]}  (+ opcjonalnie 4. element: opcje)
  * compound: {"and": [...]}  /  {"or": [...]}

Filtry: has_value, has_no_value, contains, startswith, endswith, equals,
gt, gte, lt, lte, between. Prefiks `not_` neguje. Czwarty element liścia to
opcje: {"ci": true, "regex": true}.

Walidacja jest opcjonalna: `field(...)` bez validatora buduje surowe drzewo,
a `OQLBuilder(fieldset)` sprawdza istnienie pola, `can_filter` i dozwolony filtr
względem capabilities.json.
"""

from __future__ import annotations

from typing import Any, Protocol

_UNSET = object()

# Filtry bez wartości (3. elementu liścia brak).
_NO_VALUE_FILTERS = {"has_value", "has_no_value"}

# Bazowe (nienegowane) nazwy filtrów.
_BASE_FILTERS = {
    "has_value",
    "has_no_value",
    "contains",
    "startswith",
    "endswith",
    "equals",
    "gt",
    "gte",
    "lt",
    "lte",
    "between",
}

# Wszystkie dozwolone nazwy filtrów, łącznie z negacjami.
ALLOWED_FILTERS = _BASE_FILTERS | {f"not_{f}" for f in _BASE_FILTERS}


class OQLError(ValueError):
    """Niepoprawne OQL: nieznane pole, niefiltrowalne, zły filtr."""


class FieldSetLike(Protocol):
    def exists(self, name: str) -> bool: ...
    def can_filter(self, name: str) -> bool: ...


class OQLNode:
    def to_tree(self) -> dict:  # pragma: no cover - interfejs
        raise NotImplementedError

    def to_json(self) -> dict:
        return self.to_tree()


class Leaf(OQLNode):
    def __init__(
        self,
        field: str,
        op: str,
        value: Any = _UNSET,
        *,
        ci: bool = False,
        regex: bool = False,
    ) -> None:
        if op not in ALLOWED_FILTERS:
            raise OQLError(f"Nieznany filtr: {op!r}. Dozwolone: {sorted(ALLOWED_FILTERS)}")
        base = op[4:] if op.startswith("not_") else op
        needs_value = base not in _NO_VALUE_FILTERS
        if needs_value and value is _UNSET:
            raise OQLError(f"Filtr {op!r} wymaga wartości.")
        if not needs_value and value is not _UNSET:
            raise OQLError(f"Filtr {op!r} nie przyjmuje wartości.")
        if base == "between":
            if not (isinstance(value, (list, tuple)) and len(value) == 2):
                raise OQLError("between wymaga [dolna, górna].")
        self.field = field
        self.op = op
        self.value = value
        self.ci = ci
        self.regex = regex

    def to_tree(self) -> dict:
        leaf: list[Any] = [self.field, self.op]
        if self.value is not _UNSET:
            leaf.append(list(self.value) if self.op.endswith("between") else self.value)
        opts: dict[str, bool] = {}
        if self.ci:
            opts["ci"] = True
        if self.regex:
            opts["regex"] = True
        if opts:
            # Opcje są 4. elementem; wymagają obecnego 3. (wartości).
            if len(leaf) == 2:
                raise OQLError(f"Opcje (ci/regex) nie mają sensu dla {self.op!r}.")
            leaf.append(opts)
        return {"field": leaf}


class Bool(OQLNode):
    def __init__(self, op: str, nodes: list[OQLNode]) -> None:
        if op not in ("and", "or"):
            raise OQLError(f"Compound musi być 'and'/'or', nie {op!r}.")
        if not nodes:
            raise OQLError(f"{op} wymaga co najmniej jednego węzła.")
        self.op = op
        self.nodes = list(nodes)

    def to_tree(self) -> dict:
        return {self.op: [n.to_tree() for n in self.nodes]}


def and_(*nodes: OQLNode) -> Bool:
    return Bool("and", list(nodes))


def or_(*nodes: OQLNode) -> Bool:
    return Bool("or", list(nodes))


class FieldRef:
    """Fluent budowniczy liścia dla jednego pola.

    Jeśli `fieldset` podany, waliduje istnienie pola i `can_filter` od razu,
    a każdy filtr — przy tworzeniu liścia.
    """

    def __init__(self, name: str, fieldset: FieldSetLike | None = None) -> None:
        if fieldset is not None:
            if not fieldset.exists(name):
                raise OQLError(f"Pole {name!r} nie istnieje w tym data_type.")
            if not fieldset.can_filter(name):
                raise OQLError(f"Pole {name!r} nie jest filtrowalne (can_filter=false).")
        self.name = name
        self._fs = fieldset

    def _leaf(self, op: str, value: Any = _UNSET, *, ci=False, regex=False) -> Leaf:
        return Leaf(self.name, op, value, ci=ci, regex=regex)

    # bez wartości
    def has_value(self) -> Leaf:
        return self._leaf("has_value")

    def has_no_value(self) -> Leaf:
        return self._leaf("has_no_value")

    # równość
    def equals(self, value, *, ci=False, regex=False) -> Leaf:
        return self._leaf("equals", value, ci=ci, regex=regex)

    def not_equals(self, value, *, ci=False, regex=False) -> Leaf:
        return self._leaf("not_equals", value, ci=ci, regex=regex)

    # tekstowe
    def contains(self, value, *, ci=False, regex=False) -> Leaf:
        return self._leaf("contains", value, ci=ci, regex=regex)

    def not_contains(self, value, *, ci=False, regex=False) -> Leaf:
        return self._leaf("not_contains", value, ci=ci, regex=regex)

    def startswith(self, value, *, ci=False, regex=False) -> Leaf:
        return self._leaf("startswith", value, ci=ci, regex=regex)

    def endswith(self, value, *, ci=False, regex=False) -> Leaf:
        return self._leaf("endswith", value, ci=ci, regex=regex)

    # numeryczne / porównania
    def gt(self, value) -> Leaf:
        return self._leaf("gt", value)

    def gte(self, value) -> Leaf:
        return self._leaf("gte", value)

    def lt(self, value) -> Leaf:
        return self._leaf("lt", value)

    def lte(self, value) -> Leaf:
        return self._leaf("lte", value)

    def between(self, low, high) -> Leaf:
        return self._leaf("between", [low, high])


def field(name: str) -> FieldRef:
    """Skrót do budowy liścia bez walidacji (surowe OQL)."""
    return FieldRef(name)


class OQLBuilder:
    """Fluent builder z walidacją względem FieldSet (z capabilities.json)."""

    def __init__(self, fieldset: FieldSetLike) -> None:
        self._fs = fieldset

    def field(self, name: str) -> FieldRef:
        return FieldRef(name, self._fs)

    @staticmethod
    def and_(*nodes: OQLNode) -> Bool:
        return and_(*nodes)

    @staticmethod
    def or_(*nodes: OQLNode) -> Bool:
        return or_(*nodes)


def to_tree(node: OQLNode | dict | None) -> dict | None:
    """Zwraca drzewo JSON z węzła buildera albo przepuszcza gotowy dict."""
    if node is None:
        return None
    if isinstance(node, OQLNode):
        return node.to_tree()
    if isinstance(node, dict):
        return node
    raise OQLError(f"Nie umiem zbudować OQL z {type(node)!r}.")


def validate_tree(tree: Any, fieldset: FieldSetLike, *, path: str = "$") -> None:
    """Waliduje surowe drzewo OQL (np. z frontendu) względem FieldSet.

    Rzuca OQLError przy nieznanym polu, polu niefiltrowalnym lub złym filtrze.
    """
    if tree is None:
        return
    if not isinstance(tree, dict):
        raise OQLError(f"{path}: węzeł OQL musi być obiektem.")

    if "and" in tree or "or" in tree:
        op = "and" if "and" in tree else "or"
        children = tree[op]
        if not isinstance(children, list) or not children:
            raise OQLError(f"{path}.{op}: oczekiwano niepustej listy.")
        for i, child in enumerate(children):
            validate_tree(child, fieldset, path=f"{path}.{op}[{i}]")
        return

    if "field" in tree:
        leaf = tree["field"]
        if not isinstance(leaf, list) or len(leaf) < 2:
            raise OQLError(f"{path}.field: oczekiwano [nazwa, filtr, wartość?].")
        name, op = leaf[0], leaf[1]
        if op not in ALLOWED_FILTERS:
            raise OQLError(f"{path}: nieznany filtr {op!r}.")
        if not fieldset.exists(name):
            raise OQLError(f"{path}: pole {name!r} nie istnieje.")
        if not fieldset.can_filter(name):
            raise OQLError(f"{path}: pole {name!r} nie jest filtrowalne.")
        return

    raise OQLError(f"{path}: węzeł musi mieć klucz 'and', 'or' albo 'field'.")
