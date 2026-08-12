"""Wysokopoziomowy klient Oncrawl API v2 (Etap 2).

Buduje na oncrawl/http.py (sesja z retry/backoff/cache) i errors.py.
Zawiera:

  * metody zasobów + iteratory paginujące (offset/limit/sort/filters),
  * search() — pojedyncza strona danych (rows + total_hits + columns),
  * iter_data() — pełny przebieg, sam wykrywa próg 10 000 i przełącza się na
    export=true ze strumieniowym parsowaniem JSONL (bez całości w pamięci),
  * export_lines() — surowy strumień CSV/JSONL do przekazania dalej,
  * aggregate() oraz aggregate_ranking_performance() (inny format body).

Limit paginacji danych = 10 000 wyników; powyżej wymuszamy export
(bez sort i offset, zgodnie z API).
"""

from __future__ import annotations

import json
from typing import Any, Iterator

from .config import Settings
from .http import OncrawlSession

# Twardy limit paginacji danych po stronie Oncrawl.
PAGINATION_LIMIT = 10_000


# --- budowa ścieżek danych ------------------------------------------------- #
def crawl_data_path(crawl_id: str, data_type: str) -> str:
    return f"/data/crawl/{crawl_id}/{data_type}"


def coc_data_path(coc_id: str, data_type: str) -> str:
    return f"/data/crawl_over_crawl/{coc_id}/{data_type}"


def logs_events_path(project_id: str) -> str:
    return f"/data/project/{project_id}/log_monitoring/events"


def logs_pages_path(project_id: str, granularity: str) -> str:
    return f"/data/project/{project_id}/log_monitoring/pages/{granularity}"


def ranking_path(project_id: str) -> str:
    return f"/data/project/{project_id}/ranking_performance"


def _clean_body(**kwargs) -> dict:
    return {k: v for k, v in kwargs.items() if v is not None}


class OncrawlClient:
    """Fasada nad OncrawlSession z metodami zasobów i danych."""

    def __init__(self, session: OncrawlSession) -> None:
        self.session = session

    @classmethod
    def from_settings(cls, settings: Settings, **kwargs) -> "OncrawlClient":
        return cls(OncrawlSession(settings, **kwargs))

    def close(self) -> None:
        self.session.close()

    def __enter__(self) -> "OncrawlClient":
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    # --- zasoby ----------------------------------------------------------
    def list_workspaces(self) -> list[dict]:
        data = self.session.get_json("/workspaces")
        return _envelope_list(data, "workspaces")

    def list_projects(self, workspace_id: str, **page) -> list[dict]:
        data = self.session.get_json(f"/workspaces/{workspace_id}/projects", params=page or None)
        return _envelope_list(data, "projects")

    def get_project(self, project_id: str) -> dict:
        return self.session.get_json(f"/projects/{project_id}")

    def list_crawls(self, workspace_id: str, **page) -> list[dict]:
        data = self.session.get_json(f"/workspaces/{workspace_id}/crawls", params=page or None)
        return _envelope_list(data, "crawls")

    def get_crawl(self, crawl_id: str) -> dict:
        return self.session.get_json(f"/crawls/{crawl_id}")

    def get_crawl_progress(self, crawl_id: str) -> dict:
        return self.session.get_json(f"/crawls/{crawl_id}/progress", cache=False)

    def get_fields(self, data_path: str) -> list[dict]:
        """GET {data_path}/fields — lista definicji pól."""
        data = self.session.get_json(f"{data_path}/fields")
        return _envelope_list(data, "fields", "columns")

    def iter_resource(
        self,
        path: str,
        key: str,
        *,
        page_size: int = 100,
        sort: str | None = None,
        filters: str | None = None,
    ) -> Iterator[dict]:
        """Iteruje po stronicowanym zasobie (offset/limit)."""
        offset = 0
        while True:
            params = _clean_body(limit=page_size, offset=offset, sort=sort, filters=filters)
            data = self.session.get_json(path, params=params, cache=False)
            items = _envelope_list(data, key)
            if not items:
                return
            yield from items
            if len(items) < page_size:
                return
            offset += page_size

    # --- dane: pojedyncza strona ----------------------------------------
    def search(
        self,
        data_path: str,
        *,
        fields: list[str],
        oql: dict | None = None,
        sort: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """POST search na ścieżce danych. Zwraca {rows, total_hits, columns, oql}."""
        if offset + limit > PAGINATION_LIMIT:
            raise ValueError(
                f"offset+limit={offset + limit} przekracza próg {PAGINATION_LIMIT}. "
                "Użyj iter_data()/export_lines() dla większych zbiorów."
            )
        body = _clean_body(limit=limit, offset=offset, fields=fields, sort=sort, oql=oql)
        data = self.session.post_json(data_path, json_body=body)
        meta = data.get("meta", {}) if isinstance(data, dict) else {}
        return {
            "rows": data.get("urls", []) if isinstance(data, dict) else [],
            "total_hits": meta.get("total_hits"),
            "columns": meta.get("columns"),
            "oql": data.get("oql") if isinstance(data, dict) else None,
        }

    # --- dane: pełny przebieg z auto-eksportem --------------------------
    def iter_data(
        self,
        data_path: str,
        *,
        fields: list[str],
        oql: dict | None = None,
        sort: str | None = None,
        max_rows: int | None = None,
        page_size: int = 1000,
    ) -> Iterator[dict]:
        """Zwraca wiersze. Sam decyduje: paginacja (<=10k) albo export (>10k).

        Nigdy nie ładuje całości do pamięci — eksport jest strumieniowany.
        """
        page_size = min(page_size, PAGINATION_LIMIT)
        first = self.search(data_path, fields=fields, oql=oql, sort=sort, limit=page_size, offset=0)
        total = first.get("total_hits") or 0
        target = total if max_rows is None else min(max_rows, total)

        if target <= PAGINATION_LIMIT:
            yield from self._iter_paged(
                data_path, first=first, fields=fields, oql=oql, sort=sort,
                target=target, page_size=page_size,
            )
        else:
            # Powyżej progu: eksport strumieniowy (bez sort/offset).
            count = 0
            for row in self.iter_export(data_path, fields=fields, oql=oql, file_type="json"):
                yield row
                count += 1
                if count >= target:
                    return

    def _iter_paged(self, data_path, *, first, fields, oql, sort, target, page_size):
        emitted = 0
        for row in first["rows"]:
            if emitted >= target:
                return
            yield row
            emitted += 1
        offset = page_size
        while emitted < target and offset < PAGINATION_LIMIT:
            page = self.search(
                data_path, fields=fields, oql=oql, sort=sort,
                limit=min(page_size, PAGINATION_LIMIT - offset), offset=offset,
            )
            rows = page["rows"]
            if not rows:
                return
            for row in rows:
                if emitted >= target:
                    return
                yield row
                emitted += 1
            offset += page_size

    # --- eksport strumieniowy -------------------------------------------
    def export_lines(
        self,
        data_path: str,
        *,
        fields: list[str],
        oql: dict | None = None,
        file_type: str = "csv",
    ) -> Iterator[str]:
        """Surowe linie eksportu (CSV/JSONL) — do przekazania do pliku/streamu.

        W eksporcie nie podajemy sort ani offset (wymóg API).
        """
        params = {"export": "true", "file_type": file_type}
        body = _clean_body(fields=fields, oql=oql)
        yield from self.session.stream_lines("POST", data_path, params=params, json_body=body)

    def iter_export(
        self,
        data_path: str,
        *,
        fields: list[str],
        oql: dict | None = None,
        file_type: str = "json",
    ) -> Iterator[dict]:
        """Eksport JSONL sparsowany do wierszy (dict), linia po linii."""
        for line in self.export_lines(data_path, fields=fields, oql=oql, file_type=file_type):
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                # Pierwsza linia CSV/nagłówek albo śmieć — pomijamy.
                continue

    # --- agregacje -------------------------------------------------------
    def aggregate(self, data_path: str, aggs: list[dict]) -> Any:
        """Standardowe agregacje: POST {data_path}/aggs, body {aggs:[...]}.

        Każdy agg: {oql?, fields?, value}. value = "field:method"
        (min|max|avg|sum|value_count|cardinality). fields może mieć ranges.
        """
        return self.session.post_json(f"{data_path}/aggs", json_body={"aggs": aggs})

    def aggregate_ranking_performance(
        self,
        project_id: str,
        *,
        value: list[dict],
        oql: dict | None = None,
        fields: list[dict] | None = None,
        sort: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        post_aggs_oql: dict | None = None,
    ) -> Any:
        """Agregacje Ranking Performance — inny format niż standardowy.

        value to lista {field, method, alias}; dostępne sort/limit/offset oraz
        post_aggs_oql (filtrowanie po aliasach agregacji).
        """
        body = _clean_body(
            oql=oql,
            fields=fields,
            value=value,
            sort=sort,
            limit=limit,
            offset=offset,
            post_aggs_oql=post_aggs_oql,
        )
        return self.session.post_json(f"{ranking_path(project_id)}/aggs", json_body=body)


def _envelope_list(data: Any, *keys: str) -> list:
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in keys:
            val = data.get(key)
            if isinstance(val, list):
                return val
    return []
