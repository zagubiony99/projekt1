#!/usr/bin/env python3
"""Etap 1 — discovery.

Mapuje wszystko, do czego token ma dostęp, i zapisuje:

  * capabilities.json  — pełny, maszynowy zrzut,
  * CAPABILITIES.md    — czytelne tabele pól per projekt i data_type.

Nic nie zgadujemy: listy pól pochodzą wyłącznie z /fields. Brak uprawnień,
brak feature'a albo wyczerpane quota są zapisywane jako powód, a nie
wywalają skryptu.

Użycie:
    python discovery.py                       # całe konto
    python discovery.py --project P1 --project P2   # wybrane projekty
    python discovery.py --no-cache            # pomiń cache na dysku
    python discovery.py --from capabilities.json    # tylko przerenderuj MD

Token: wyłącznie z .env (ONCRAWL_TOKEN). Nigdy w kodzie ani w logach.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from oncrawl.config import MissingTokenError, load_settings
from oncrawl.errors import (
    ACCESS_DENIED_ERRORS,
    OncrawlAPIError,
    OncrawlError,
    OncrawlNetworkError,
)
from oncrawl.http import OncrawlSession

logger = logging.getLogger("discovery")

# Data-type'y crawla, o których pola pytamy (dopisując /fields do ścieżki danych).
CRAWL_DATA_TYPES = ["pages", "links", "clusters", "structured_data"]

# --------------------------------------------------------------------------- #
# Pomocnicze wyciąganie kształtów odpowiedzi (API bywa opakowane różnie)
# --------------------------------------------------------------------------- #
def _as_list(data: Any, *keys: str) -> list:
    """Zwraca listę: albo bezpośrednio, albo spod jednego z kluczy koperty."""
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in keys:
            val = data.get(key)
            if isinstance(val, list):
                return val
    return []


def _as_obj(data: Any, key: str) -> dict:
    """Zwraca obiekt spod klucza koperty, albo samo `data` jeśli to już dict."""
    if isinstance(data, dict):
        if isinstance(data.get(key), dict):
            return data[key]
        return data
    return {}


def _fields_from(data: Any) -> list[dict]:
    """Normalizuje odpowiedź /fields do listy dictów pól."""
    fields = _as_list(data, "fields", "columns")
    return [f for f in fields if isinstance(f, dict)]


# --------------------------------------------------------------------------- #
# Kolektor — używa wyłącznie session.get_json; testowalny przez MockTransport
# --------------------------------------------------------------------------- #
class DiscoveryCollector:
    def __init__(self, session: OncrawlSession, *, cache: bool = True) -> None:
        self._s = session
        self._cache = cache

    def _get(self, path: str, **params) -> Any:
        return self._s.get_json(path, params=params or None, cache=self._cache)

    def _probe_fields(self, path: str) -> dict:
        """Odpytuje /fields pod ścieżką danych; zwraca {fields|reason}."""
        try:
            data = self._get(path)
        except ACCESS_DENIED_ERRORS as exc:
            return {"available": False, "reason": exc.short_reason(), "fields": []}
        except OncrawlAPIError as exc:
            return {"available": False, "reason": exc.short_reason(), "fields": []}
        except OncrawlNetworkError as exc:
            return {"available": False, "reason": f"network: {exc}", "fields": []}
        return {"available": True, "reason": None, "fields": _fields_from(data)}

    # --- najwyższy poziom ------------------------------------------------
    def collect(
        self,
        *,
        workspace_ids: list[str] | None = None,
        project_ids: list[str] | None = None,
    ) -> dict:
        result: dict[str, Any] = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "base_url": self._s._settings.base_url,  # bez tokena
            "workspaces": [],
            "errors": [],
        }

        if project_ids:
            # Tryb celowany: pomijamy enumerację workspace'ów.
            ws_entry = {"id": None, "name": "(explicit projects)", "projects": []}
            for pid in project_ids:
                ws_entry["projects"].append(self._collect_project(pid))
            result["workspaces"].append(ws_entry)
            return result

        workspaces = self._list_workspaces(workspace_ids)
        if isinstance(workspaces, dict) and "error" in workspaces:
            result["errors"].append(workspaces["error"])
            return result

        for ws in workspaces:
            result["workspaces"].append(self._collect_workspace(ws))
        return result

    def _list_workspaces(self, workspace_ids: list[str] | None) -> list[dict] | dict:
        if workspace_ids:
            return [{"id": wid, "name": None} for wid in workspace_ids]
        try:
            data = self._get("/workspaces")
        except OncrawlError as exc:
            reason = exc.short_reason() if isinstance(exc, OncrawlAPIError) else str(exc)
            return {"error": f"nie udało się pobrać /workspaces: {reason}"}
        return _as_list(data, "workspaces")

    def _collect_workspace(self, ws: dict) -> dict:
        wid = ws.get("id") or ws.get("workspace_id")
        entry: dict[str, Any] = {
            "id": wid,
            "name": ws.get("name"),
            "raw": {k: v for k, v in ws.items() if k not in ("projects",)},
            "projects": [],
            "error": None,
        }
        try:
            data = self._get(f"/workspaces/{wid}/projects")
        except OncrawlAPIError as exc:
            entry["error"] = exc.short_reason()
            return entry
        except OncrawlNetworkError as exc:
            entry["error"] = f"network: {exc}"
            return entry

        for proj in _as_list(data, "projects"):
            pid = proj.get("id") or proj.get("project_id")
            if pid:
                entry["projects"].append(self._collect_project(pid, summary=proj))
        return entry

    def _collect_project(self, project_id: str, *, summary: dict | None = None) -> dict:
        entry: dict[str, Any] = {
            "id": project_id,
            "name": (summary or {}).get("name"),
            "error": None,
        }
        try:
            data = self._get(f"/projects/{project_id}")
        except OncrawlAPIError as exc:
            entry["error"] = exc.short_reason()
            return entry
        except OncrawlNetworkError as exc:
            entry["error"] = f"network: {exc}"
            return entry

        # Odpowiedź /projects/{id} ma jeden klucz najwyższego poziomu: "project".
        # Crawle NIE są tu jako pełne obiekty — jest tylko lista crawl_ids oraz
        # last_crawl_id. Szczegóły crawli dociągamy osobno (GET /crawls/{id}).
        project = _as_obj(data, "project")
        crawl_configs = _as_list(data, "crawl_configs") or _as_list(project, "crawl_configs")

        entry["name"] = project.get("name") or entry["name"]
        entry["domain"] = project.get("domain")
        entry["start_url"] = project.get("start_url")
        entry["features"] = project.get("features")
        entry["limits"] = project.get("limits")
        entry["log_monitoring_ready"] = project.get("log_monitoring_ready")
        entry["log_monitoring_data_ready"] = project.get("log_monitoring_data_ready")
        entry["crawl_config_ids"] = project.get("crawl_config_ids") or []
        entry["crawl_ids"] = project.get("crawl_ids") or []
        entry["crawl_over_crawl_ids"] = project.get("crawl_over_crawl_ids") or []
        entry["last_crawl_id"] = project.get("last_crawl_id")
        entry["last_crawl_created_at"] = project.get("last_crawl_created_at")

        entry["crawl_configs"] = [
            {"id": c.get("id"), "name": c.get("name"), "user_agent": c.get("user_agent")}
            for c in crawl_configs
            if isinstance(c, dict)
        ]

        # Dociągnij realne crawle (status/end_reason wg specyfikacji Oncrawl).
        entry["crawls"], entry["crawls_truncated"] = self._collect_crawls(entry["crawl_ids"])

        # Wybór crawla do sondowania pól: last_crawl_id, potem crawl_ids (od
        # najnowszego), aż /pages/fields odpowie 200.
        candidates = self._candidate_crawl_ids(entry["last_crawl_id"], entry["crawl_ids"])
        probed_id, data_types = self._collect_crawl_data_types(candidates)
        entry["last_finished_crawl_id"] = probed_id  # crawl, po którym pobrano pola
        entry["data_types"] = data_types

        entry["log_monitoring"] = self._collect_log_monitoring(project_id, project)
        entry["ranking_performance"] = self._probe_fields(
            f"/data/project/{project_id}/ranking_performance/fields"
        )
        return entry

    @staticmethod
    def _candidate_crawl_ids(
        last_crawl_id: str | None, crawl_ids: list[str], *, cap: int = 6
    ) -> list[str]:
        order: list[str] = []
        if last_crawl_id:
            order.append(last_crawl_id)
        for cid in crawl_ids or []:
            if cid and cid not in order:
                order.append(cid)
        return order[:cap]

    def _collect_crawls(self, crawl_ids: list[str], *, cap: int = 15) -> tuple[list[dict], bool]:
        """Dociąga szczegóły crawli (GET /crawls/{id}) do selektora w explorerze."""
        out: list[dict] = []
        ids = crawl_ids or []
        for cid in ids[:cap]:
            try:
                data = self._get(f"/crawls/{cid}")
            except OncrawlAPIError as exc:
                out.append({"id": cid, "status": None, "error": exc.short_reason()})
                continue
            except OncrawlNetworkError as exc:
                out.append({"id": cid, "status": None, "error": f"network: {exc}"})
                continue
            crawl = _as_obj(data, "crawl")
            out.append(
                {
                    "id": crawl.get("id") or cid,
                    "status": crawl.get("status"),
                    "end_reason": crawl.get("end_reason"),
                    "created_at": crawl.get("created_at"),
                }
            )
        return out, len(ids) > cap

    def _collect_crawl_data_types(self, candidate_ids: list[str]) -> tuple[str | None, dict]:
        """Znajduje pierwszy crawl z odpytywalnymi danymi i sonduje wszystkie data_type."""
        if not candidate_ids:
            empty = {
                dt: {"available": False, "reason": "brak crawli w projekcie", "fields": []}
                for dt in CRAWL_DATA_TYPES
            }
            return None, empty

        chosen: str | None = None
        pages_probe: dict | None = None
        for cid in candidate_ids:
            probe = self._probe_fields(f"/data/crawl/{cid}/pages/fields")
            if probe["available"]:
                chosen, pages_probe = cid, probe
                break

        if chosen is None:
            # Żaden crawl nie ma odpytywalnych stron — raportujemy powód per data_type
            # na najnowszym kandydacie (najczęściej ten sam powód: crawl nie gotowy).
            cid = candidate_ids[0]
            return cid, {
                dt: self._probe_fields(f"/data/crawl/{cid}/{dt}/fields")
                for dt in CRAWL_DATA_TYPES
            }

        out = {"pages": pages_probe}
        for dt in CRAWL_DATA_TYPES:
            if dt == "pages":
                continue
            out[dt] = self._probe_fields(f"/data/crawl/{chosen}/{dt}/fields")
        return chosen, out

    def _collect_log_monitoring(self, project_id: str, project: dict) -> dict:
        ready = project.get("log_monitoring_ready")
        block: dict[str, Any] = {
            "log_monitoring_ready": ready,
            "log_monitoring_data_ready": project.get("log_monitoring_data_ready"),
        }
        if ready is False:
            block["available"] = False
            block["reason"] = "log_monitoring_ready=false"
            return block

        block["available"] = True
        block["events_fields"] = self._probe_fields(
            f"/data/project/{project_id}/log_monitoring/events/fields"
        )
        block["events_metadata"] = self._probe_metadata(
            f"/data/project/{project_id}/log_monitoring/events/metadata"
        )
        return block

    def _probe_metadata(self, path: str) -> dict:
        try:
            data = self._get(path)
        except OncrawlAPIError as exc:
            return {"available": False, "reason": exc.short_reason()}
        except OncrawlNetworkError as exc:
            return {"available": False, "reason": f"network: {exc}"}
        return {"available": True, "reason": None, "metadata": data}


# --------------------------------------------------------------------------- #
# Renderowanie CAPABILITIES.md
# --------------------------------------------------------------------------- #
def _bool_cell(v: Any) -> str:
    if v is True:
        return "✅"
    if v is False:
        return "—"
    return "?"


def _aggs_cell(field: dict) -> str:
    methods = field.get("agg_metric_methods")
    if isinstance(methods, list) and methods:
        return ", ".join(str(m) for m in methods)
    return "—"


def _values_cell(field: dict) -> str:
    values = field.get("values")
    if isinstance(values, list) and values:
        shown = ", ".join(str(v) for v in values[:6])
        if len(values) > 6:
            shown += f" … (+{len(values) - 6})"
        return shown
    return ""


def _fields_table(fields: list[dict]) -> str:
    if not fields:
        return "_Brak pól._\n"
    lines = [
        "| pole | typ | arity | filtr | sort | display | agregacje | wartości |",
        "|------|-----|-------|:-----:|:----:|:-------:|-----------|----------|",
    ]
    for f in sorted(fields, key=lambda x: str(x.get("name", ""))):
        lines.append(
            "| `{name}` | {type} | {arity} | {flt} | {srt} | {disp} | {agg} | {vals} |".format(
                name=f.get("name", "?"),
                type=f.get("type", ""),
                arity=f.get("arity", ""),
                flt=_bool_cell(f.get("can_filter")),
                srt=_bool_cell(f.get("can_sort")),
                disp=_bool_cell(f.get("can_display")),
                agg=_aggs_cell(f),
                vals=_values_cell(f).replace("|", "\\|"),
            )
        )
    return "\n".join(lines) + "\n"


def _data_type_section(title: str, block: dict) -> str:
    out = [f"##### {title}\n"]
    if not block.get("available"):
        out.append(f"> ⛔ Niedostępne — {block.get('reason', 'nieznany powód')}\n")
        return "\n".join(out) + "\n"
    fields = block.get("fields", [])
    out.append(f"_{len(fields)} pól_\n")
    out.append(_fields_table(fields))
    return "\n".join(out) + "\n"


def render_markdown(cap: dict) -> str:
    out: list[str] = []
    out.append("# CAPABILITIES — Oncrawl API discovery\n")
    out.append(f"_Wygenerowano: {cap.get('generated_at', '?')}_")
    out.append(f"_Baza API: {cap.get('base_url', '?')}_\n")

    if cap.get("errors"):
        out.append("## ⚠️ Błędy globalne\n")
        for err in cap["errors"]:
            out.append(f"- {err}")
        out.append("")

    # Spis treści per projekt.
    all_projects = [
        (ws, p)
        for ws in cap.get("workspaces", [])
        for p in ws.get("projects", [])
    ]
    out.append("## Podsumowanie\n")
    out.append(f"- Workspace'ów: {len(cap.get('workspaces', []))}")
    out.append(f"- Projektów: {len(all_projects)}\n")

    for ws in cap.get("workspaces", []):
        ws_name = ws.get("name") or ws.get("id") or "(workspace)"
        out.append(f"## Workspace: {ws_name}  \n`id={ws.get('id')}`\n")
        if ws.get("error"):
            out.append(f"> ⛔ {ws['error']}\n")
        for proj in ws.get("projects", []):
            out.append(_project_section(proj))
    return "\n".join(out).rstrip() + "\n"


def _project_section(proj: dict) -> str:
    out: list[str] = []
    name = proj.get("name") or proj.get("id")
    out.append(f"### 📦 Projekt: {name}\n")
    out.append(f"`id={proj.get('id')}`\n")
    if proj.get("error"):
        out.append(f"> ⛔ {proj['error']}\n")
        return "\n".join(out) + "\n"

    lm_ready = proj.get("log_monitoring_ready")
    out.append("| właściwość | wartość |")
    out.append("|------------|---------|")
    out.append(f"| domain | {proj.get('domain') or '—'} |")
    out.append(f"| start_url | {proj.get('start_url') or '—'} |")
    out.append(f"| features | {_compact(proj.get('features'))} |")
    out.append(f"| limits | {_compact(proj.get('limits'))} |")
    out.append(f"| log_monitoring_ready | {_bool_cell(lm_ready)} |")
    out.append(f"| log_monitoring_data_ready | {_bool_cell(proj.get('log_monitoring_data_ready'))} |")
    out.append(f"| crawl_config_ids | {_count(proj.get('crawl_config_ids'))} |")
    out.append(f"| crawl_ids | {_count(proj.get('crawl_ids'))} |")
    out.append(f"| crawl_over_crawl_ids | {_count(proj.get('crawl_over_crawl_ids'))} |")
    out.append(f"| last_crawl_id | `{proj.get('last_crawl_id')}` |")
    out.append(f"| crawl użyty do pól | `{proj.get('last_finished_crawl_id')}` |")
    out.append("")

    crawls = proj.get("crawls") or []
    if crawls:
        extra = " (pierwsze 15)" if proj.get("crawls_truncated") else ""
        out.append(f"<details><summary>Crawle{extra} (status / end_reason)</summary>\n")
        out.append("| crawl_id | status | end_reason | created_at |")
        out.append("|----------|--------|-----------|-----------|")
        for c in crawls[:20]:
            out.append(
                f"| `{c.get('id')}` | {c.get('status') or ''} | {c.get('end_reason') or ''} | {c.get('created_at') or ''} |"
            )
        out.append("\n</details>\n")

    out.append("#### Dane crawla\n")
    for dt in CRAWL_DATA_TYPES:
        block = (proj.get("data_types") or {}).get(dt, {"available": False, "reason": "brak danych"})
        out.append(_data_type_section(dt, block))

    lm = proj.get("log_monitoring") or {}
    out.append("#### Log monitoring\n")
    if not lm.get("available"):
        out.append(f"> ⛔ {lm.get('reason', 'niedostępne')}\n")
    else:
        out.append(_data_type_section("events (fields)", lm.get("events_fields", {})))
        meta = lm.get("events_metadata", {})
        if meta.get("available"):
            out.append("<details><summary>events metadata</summary>\n")
            out.append("```json")
            out.append(_compact(meta.get("metadata"), limit=2000))
            out.append("```\n</details>\n")
        else:
            out.append(f"> metadata: {meta.get('reason', 'niedostępne')}\n")

    out.append("#### Ranking Performance\n")
    out.append(_data_type_section("ranking_performance", proj.get("ranking_performance", {})))

    return "\n".join(out) + "\n"


def _compact(obj: Any, *, limit: int = 300) -> str:
    if obj is None:
        return "—"
    try:
        s = json.dumps(obj, ensure_ascii=False)
    except (TypeError, ValueError):
        s = str(obj)
    if len(s) > limit:
        s = s[: limit - 1] + "…"
    return s


def _count(obj: Any) -> str:
    if isinstance(obj, list):
        return str(len(obj))
    if obj is None:
        return "—"
    return str(obj)


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Oncrawl API discovery (Etap 1)")
    p.add_argument("--workspace", action="append", dest="workspaces", default=None,
                   help="Ogranicz do konkretnego workspace_id (można powtórzyć).")
    p.add_argument("--project", action="append", dest="projects", default=None,
                   help="Ogranicz do konkretnego project_id (można powtórzyć).")
    p.add_argument("--out-json", default="capabilities.json")
    p.add_argument("--out-md", default="CAPABILITIES.md")
    p.add_argument("--no-cache", action="store_true", help="Nie czytaj/nie zapisuj .cache")
    p.add_argument("--from", dest="from_json", default=None,
                   help="Pomiń API i tylko przerenderuj MD z istniejącego capabilities.json")
    p.add_argument("-v", "--verbose", action="store_true")
    return p.parse_args(argv)


def _write_outputs(cap: dict, out_json: str, out_md: str) -> None:
    Path(out_json).write_text(json.dumps(cap, ensure_ascii=False, indent=2), "utf-8")
    Path(out_md).write_text(render_markdown(cap), "utf-8")
    logger.info("zapisano %s oraz %s", out_json, out_md)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )

    if args.from_json:
        cap = json.loads(Path(args.from_json).read_text("utf-8"))
        Path(args.out_md).write_text(render_markdown(cap), "utf-8")
        logger.info("przerenderowano %s z %s", args.out_md, args.from_json)
        return 0

    try:
        settings = load_settings()
    except MissingTokenError as exc:
        print(f"BŁĄD: {exc}", file=sys.stderr)
        return 2

    logger.info("konfiguracja: %s", settings.redacted())

    try:
        with OncrawlSession(settings) as session:
            collector = DiscoveryCollector(session, cache=not args.no_cache)
            cap = collector.collect(
                workspace_ids=args.workspaces,
                project_ids=args.projects,
            )
    except OncrawlNetworkError as exc:
        print(f"BŁĄD SIECI: {exc}", file=sys.stderr)
        return 1

    _write_outputs(cap, args.out_json, args.out_md)
    print(f"\n✔ Gotowe. Zajrzyj do {args.out_md}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
