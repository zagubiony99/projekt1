"""Serwer MCP dla Oncrawl — udostępnia dane crawli/logów jako narzędzia MCP.

Opakowuje istniejący oncrawl/client.py + capabilities.json, więc obowiązują
te same reguły: token wyłącznie z .env, walidacja OQL względem /fields,
automatyczne przejście na export=true powyżej 10 000 wyników.

Uruchomienie (stdio — dla Claude Desktop / Claude Code / Cursor):

    python mcp_server.py

Konfiguracja klienta — patrz README (sekcja MCP) albo mcp_config.example.json.

Wymaga: pip install "mcp>=1.2"
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from oncrawl.capabilities import (
    CRAWL_DATA_TYPES,
    LOG_DATA_TYPE,
    RANKING_DATA_TYPE,
    Capabilities,
)
from oncrawl.client import (
    OncrawlClient,
    crawl_data_path,
    logs_events_path,
    ranking_path,
)
from oncrawl.config import load_settings
from oncrawl.errors import OncrawlAPIError, OncrawlError
from oncrawl.oql import OQLError, validate_tree

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as exc:  # pragma: no cover - zależność opcjonalna
    raise SystemExit(
        "Brak pakietu mcp. Zainstaluj: pip install \"mcp>=1.2\""
    ) from exc

mcp = FastMCP("oncrawl")

CAPABILITIES_PATH = Path("capabilities.json")

# Limity chroniące kontekst modelu — wynik narzędzia MCP trafia w całości do
# kontekstu, więc nie wysyłamy dziesiątek tysięcy wierszy ani setek definicji
# pól. Pełne zbiory idą przez export_data prosto na dysk.
MAX_ROWS = 200
DEFAULT_ROWS = 25
MAX_FIELDS = 80


class _State:
    """Leniwie inicjalizowane zależności (capabilities + klient)."""

    def __init__(self) -> None:
        self._caps: Capabilities | None = None
        self._client: OncrawlClient | None = None

    @property
    def caps(self) -> Capabilities:
        if self._caps is None:
            if not CAPABILITIES_PATH.exists():
                raise RuntimeError(
                    "Brak capabilities.json — uruchom najpierw: python cli.py discover"
                )
            self._caps = Capabilities.load(CAPABILITIES_PATH)
        return self._caps

    @property
    def client(self) -> OncrawlClient:
        if self._client is None:
            self._client = OncrawlClient.from_settings(load_settings())
        return self._client


state = _State()


def _data_path(project_id: str, data_type: str, crawl_id: str | None) -> str:
    if data_type in CRAWL_DATA_TYPES:
        if not crawl_id:
            proj = state.caps.project(project_id) or {}
            crawl_id = proj.get("last_finished_crawl_id") or proj.get("last_crawl_id")
        if not crawl_id:
            raise ValueError(f"data_type={data_type} wymaga crawl_id (brak też ostatniego crawla).")
        return crawl_data_path(crawl_id, data_type)
    if data_type == LOG_DATA_TYPE:
        return logs_events_path(project_id)
    if data_type == RANKING_DATA_TYPE:
        return ranking_path(project_id)
    raise ValueError(f"Nieznany data_type: {data_type}")


def _err(exc: Exception) -> str:
    if isinstance(exc, OncrawlAPIError):
        return f"BŁĄD API: {exc.short_reason()}"
    if isinstance(exc, (OQLError, ValueError)):
        return f"BŁĄD: {exc}"
    if isinstance(exc, OncrawlError):
        return f"BŁĄD: {exc}"
    return f"BŁĄD: {exc!r}"


@mcp.tool()
def list_projects() -> str:
    """Lista projektów Oncrawl wraz z dostępnymi typami danych.

    Zwraca id, nazwę, workspace oraz które data_type są dostępne
    (pages, links, clusters, structured_data, logs, ranking_performance).
    """
    try:
        return json.dumps(state.caps.project_summaries(), ensure_ascii=False, indent=2)
    except Exception as exc:
        return _err(exc)


@mcp.tool()
def list_crawls(project_id: str) -> str:
    """Lista crawli projektu (id, status, end_reason, created_at)."""
    try:
        proj = state.caps.project(project_id)
        if proj is None:
            return f"BŁĄD: nieznany projekt {project_id}"
        return json.dumps(
            {
                "crawls": proj.get("crawls", []),
                "last_crawl_id": proj.get("last_crawl_id"),
                "recommended_crawl_id": proj.get("last_finished_crawl_id"),
            },
            ensure_ascii=False,
            indent=2,
        )
    except Exception as exc:
        return _err(exc)


@mcp.tool()
def list_fields(
    project_id: str,
    data_type: str,
    search: str = "",
    detailed: bool = False,
    limit: int = MAX_FIELDS,
) -> str:
    """Pola dostępne dla data_type. Wywołaj PRZED query_data, by poznać nazwy pól.

    `pages` potrafi mieć 200+ pól, więc domyślnie zwracamy zwięzłą formę
    "nazwa:typ" — to wystarcza do zbudowania zapytania i nie zalewa kontekstu.
    Zawężaj `search` (fragment nazwy), a `detailed=True` włącz tylko dla
    kilku pól, gdy naprawdę potrzebujesz flag i dozwolonych wartości.
    """
    try:
        fs = state.caps.fieldset(project_id, data_type)
        if len(fs) == 0:
            return (
                f"Brak pól dla {data_type} w projekcie {project_id} "
                "(niedostępne w planie albo brak danych). Sprawdź list_projects."
            )

        matched = [
            f for f in fs.all()
            if not search or search.lower() in str(f.get("name", "")).lower()
        ]
        total = len(matched)
        limit = max(1, min(limit, MAX_FIELDS))
        shown = matched[:limit]

        if detailed:
            fields: Any = [
                {
                    "name": f.get("name"),
                    "type": f.get("type"),
                    "can_filter": bool(f.get("can_filter")),
                    "can_sort": bool(f.get("can_sort")),
                    "aggs": f.get("agg_metric_methods") or [],
                    "values": f.get("values") or None,
                }
                for f in shown
            ]
        else:
            # Zwięźle: "nazwa:typ" (+ '-' gdy pole nie jest filtrowalne).
            fields = [
                f"{f.get('name')}:{f.get('type')}" + ("" if f.get("can_filter") else " (no-filter)")
                for f in shown
            ]

        out: dict[str, Any] = {"total_matching": total, "returned": len(shown), "fields": fields}
        if total > len(shown):
            out["hint"] = (
                f"Pokazano {len(shown)} z {total}. Zawęź parametrem search="
                ", np. search='title' albo search='cwv'."
            )
        return json.dumps(out, ensure_ascii=False, indent=2)
    except Exception as exc:
        return _err(exc)


@mcp.tool()
def query_data(
    project_id: str,
    data_type: str,
    fields: list[str],
    crawl_id: str | None = None,
    oql: dict | None = None,
    sort: str | None = None,
    limit: int = DEFAULT_ROWS,
) -> str:
    """Pobiera wiersze danych (strony, linki, logi…) z filtrem OQL.

    OQL to drzewo JSON:
      liść:     {"field": ["status_code", "equals", 404]}
      compound: {"and": [...]} / {"or": [...]}
      filtry:   has_value, has_no_value, contains, startswith, endswith,
                equals, gt, gte, lt, lte, between (prefiks not_ neguje)

    sort ma format "pole:asc" albo "pole:desc".
    Zwraca total_hits oraz wiersze (limit maks. 200 — to podgląd, nie eksport).
    """
    try:
        fs = state.caps.fieldset(project_id, data_type)
        if oql is not None and len(fs) > 0:
            validate_tree(oql, fs)  # rzuci OQLError przy złym polu/filtrze
        path = _data_path(project_id, data_type, crawl_id)
        res = state.client.search(
            path,
            fields=fields,
            oql=oql,
            sort=sort,
            limit=max(1, min(limit, MAX_ROWS)),
        )
        return json.dumps(
            {"total_hits": res["total_hits"], "returned": len(res["rows"]), "rows": res["rows"]},
            ensure_ascii=False,
            indent=2,
            default=str,
        )
    except Exception as exc:
        return _err(exc)


@mcp.tool()
def aggregate_data(
    project_id: str,
    data_type: str,
    value: str,
    crawl_id: str | None = None,
    group_by: list[str] | None = None,
    oql: dict | None = None,
) -> str:
    """Agregacja po stronie API — liczy na całym zbiorze, nie tylko na stronie wyników.

    `value` w formacie "pole:metoda", np. "status_code:value_count",
    "depth:avg", "url:cardinality". Metody: min, max, avg, sum,
    value_count, cardinality (część pól ma też median/percentiles/stddev).
    `group_by` to lista pól wymiarów (np. ["status_code_range"]).
    """
    try:
        fs = state.caps.fieldset(project_id, data_type)
        if oql is not None and len(fs) > 0:
            validate_tree(oql, fs)
        path = _data_path(project_id, data_type, crawl_id)
        agg: dict[str, Any] = {"value": value}
        if group_by:
            agg["fields"] = list(group_by)
        if oql is not None:
            agg["oql"] = oql
        res = state.client.aggregate(path, aggs=[agg])
        return json.dumps(res, ensure_ascii=False, indent=2, default=str)
    except Exception as exc:
        return _err(exc)


@mcp.tool()
def export_data(
    project_id: str,
    data_type: str,
    fields: list[str],
    out_path: str,
    crawl_id: str | None = None,
    oql: dict | None = None,
) -> str:
    """Eksport pełnego wyniku do pliku CSV (obchodzi limit 10 000 wierszy).

    Strumieniuje przez export=true prosto na dysk — nie ładuje całości do
    pamięci ani do kontekstu modelu. `out_path` to ścieżka pliku .csv.
    Zwraca liczbę zapisanych linii.
    """
    try:
        fs = state.caps.fieldset(project_id, data_type)
        if oql is not None and len(fs) > 0:
            validate_tree(oql, fs)
        path = _data_path(project_id, data_type, crawl_id)
        target = Path(out_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        n = 0
        with target.open("w", encoding="utf-8", newline="") as fh:
            for line in state.client.export_lines(path, fields=fields, oql=oql, file_type="csv"):
                fh.write(line + "\n")
                n += 1
        return f"Zapisano {n} linii → {target.resolve()}"
    except Exception as exc:
        return _err(exc)


if __name__ == "__main__":
    mcp.run()
