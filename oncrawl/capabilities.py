"""Ładowanie i odpytywanie capabilities.json wyprodukowanego przez discovery.

Dostarcza FieldSet (per projekt + data_type) używany przez builder OQL,
walidację zapytań i dynamiczny panel filtrów w explorerze.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterator

# Kanoniczne nazwy data_type i gdzie szukać ich pól w capabilities.json.
CRAWL_DATA_TYPES = ("pages", "links", "clusters", "structured_data")
LOG_DATA_TYPE = "logs"
RANKING_DATA_TYPE = "ranking_performance"


class FieldSet:
    """Zbiór pól jednego data_type: szybkie sprawdzenia flag."""

    def __init__(self, fields: list[dict]) -> None:
        self._by_name: dict[str, dict] = {
            f["name"]: f for f in fields if isinstance(f, dict) and f.get("name")
        }

    def __len__(self) -> int:
        return len(self._by_name)

    def names(self) -> list[str]:
        return list(self._by_name.keys())

    def all(self) -> list[dict]:
        return list(self._by_name.values())

    def get(self, name: str) -> dict | None:
        return self._by_name.get(name)

    def exists(self, name: str) -> bool:
        return name in self._by_name

    def _flag(self, name: str, flag: str) -> bool:
        f = self._by_name.get(name)
        return bool(f and f.get(flag))

    def can_filter(self, name: str) -> bool:
        return self._flag(name, "can_filter")

    def can_sort(self, name: str) -> bool:
        return self._flag(name, "can_sort")

    def can_display(self, name: str) -> bool:
        return self._flag(name, "can_display")

    def type(self, name: str) -> str | None:
        f = self._by_name.get(name)
        return f.get("type") if f else None

    def default_display_fields(self, limit: int = 12) -> list[str]:
        return [n for n in self._by_name if self.can_display(n)][:limit]


class Capabilities:
    """Wrapper na capabilities.json."""

    def __init__(self, data: dict) -> None:
        self.data = data

    @classmethod
    def load(cls, path: str | Path = "capabilities.json") -> "Capabilities":
        return cls(json.loads(Path(path).read_text("utf-8")))

    # --- nawigacja -------------------------------------------------------
    def iter_projects(self) -> Iterator[dict]:
        for ws in self.data.get("workspaces", []):
            for proj in ws.get("projects", []):
                yield proj

    def project(self, project_id: str) -> dict | None:
        for proj in self.iter_projects():
            if proj.get("id") == project_id:
                return proj
        return None

    def project_summaries(self) -> list[dict]:
        out = []
        for ws in self.data.get("workspaces", []):
            for proj in ws.get("projects", []):
                out.append(
                    {
                        "id": proj.get("id"),
                        "name": proj.get("name"),
                        "workspace_id": ws.get("id"),
                        "workspace_name": ws.get("name"),
                        "error": proj.get("error"),
                        "available_data_types": self.available_data_types(proj),
                    }
                )
        return out

    # --- data types ------------------------------------------------------
    def available_data_types(self, project_or_id: str | dict) -> dict[str, bool]:
        proj = self._resolve(project_or_id)
        if proj is None:
            return {}
        out: dict[str, bool] = {}
        dts = proj.get("data_types") or {}
        for dt in CRAWL_DATA_TYPES:
            out[dt] = bool((dts.get(dt) or {}).get("available"))
        lm = proj.get("log_monitoring") or {}
        out[LOG_DATA_TYPE] = bool(lm.get("available") and (lm.get("events_fields") or {}).get("available"))
        out[RANKING_DATA_TYPE] = bool((proj.get("ranking_performance") or {}).get("available"))
        return out

    def raw_fields(self, project_or_id: str | dict, data_type: str) -> list[dict]:
        proj = self._resolve(project_or_id)
        if proj is None:
            return []
        if data_type in CRAWL_DATA_TYPES:
            return ((proj.get("data_types") or {}).get(data_type) or {}).get("fields", [])
        if data_type == LOG_DATA_TYPE:
            return ((proj.get("log_monitoring") or {}).get("events_fields") or {}).get("fields", [])
        if data_type == RANKING_DATA_TYPE:
            return (proj.get("ranking_performance") or {}).get("fields", [])
        return []

    def fieldset(self, project_or_id: str | dict, data_type: str) -> FieldSet:
        return FieldSet(self.raw_fields(project_or_id, data_type))

    def _resolve(self, project_or_id: str | dict) -> dict | None:
        if isinstance(project_or_id, dict):
            return project_or_id
        return self.project(project_or_id)
