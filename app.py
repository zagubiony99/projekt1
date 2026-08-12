"""Etap 3 — backend explorera (FastAPI).

Endpointy:
  GET  /api/projects                     lista projektów + dostępne data_type (z capabilities.json)
  GET  /api/projects/{pid}/crawls        crawle projektu (z capabilities.json)
  GET  /api/fields                       pola data_type (do panelu filtrów/kolumn)
  POST /api/query                        strona danych (waliduje OQL wzgl. capabilities)
  POST /api/export                       eksport CSV/XLSX (export=true, streaming)
  GET/POST/DELETE /api/presets           zapisane presety zapytań (lokalny JSON)
  GET  /                                 frontend (web/index.html)

Zależności (capabilities, klient) są wstrzykiwalne przez create_app(...),
dzięki czemu testy jadą bez sieci i bez quoty.
"""

from __future__ import annotations

import csv
import io
import json
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    JSONResponse,
    StreamingResponse,
)
from pydantic import BaseModel, Field

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
from oncrawl import mcp_status as mcp_status_mod
from oncrawl.config import load_settings
from oncrawl.errors import OncrawlAPIError, OncrawlError, OncrawlNetworkError
from oncrawl.oql import OQLError, validate_tree
from oncrawl.recipes import applicable_recipes

WEB_DIR = Path(__file__).parent / "web"
DEFAULT_PRESETS_PATH = Path("presets.json")


# --- modele żądań ---------------------------------------------------------- #
class QueryRequest(BaseModel):
    project_id: str
    data_type: str
    crawl_id: str | None = None
    fields: list[str] = Field(default_factory=list)
    oql: dict | None = None
    sort: str | None = None
    limit: int = 100
    offset: int = 0


class ExportRequest(BaseModel):
    project_id: str
    data_type: str
    crawl_id: str | None = None
    fields: list[str] = Field(default_factory=list)
    oql: dict | None = None
    file_type: str = "csv"  # csv | xlsx


class Preset(BaseModel):
    name: str
    query: dict


# --- budowa ścieżki danych ------------------------------------------------- #
def _data_path(req: QueryRequest | ExportRequest) -> str:
    dt = req.data_type
    if dt in CRAWL_DATA_TYPES:
        if not req.crawl_id:
            raise HTTPException(400, f"data_type={dt} requires a crawl_id.")
        return crawl_data_path(req.crawl_id, dt)
    if dt == LOG_DATA_TYPE:
        return logs_events_path(req.project_id)
    if dt == RANKING_DATA_TYPE:
        return ranking_path(req.project_id)
    raise HTTPException(400, f"Unknown data_type: {dt}")


def _validate_oql(app: FastAPI, req: QueryRequest | ExportRequest) -> None:
    caps: Capabilities | None = app.state.capabilities
    if caps is None or req.oql is None:
        return
    fs = caps.fieldset(req.project_id, req.data_type)
    if len(fs) == 0:
        return  # brak schematu w capabilities — best effort, nie blokujemy
    try:
        validate_tree(req.oql, fs)
    except OQLError as exc:
        raise HTTPException(422, f"Invalid OQL: {exc}") from exc


# --- fabryka aplikacji ----------------------------------------------------- #
def create_app(
    *,
    capabilities: Capabilities | None = None,
    client: OncrawlClient | None = None,
    presets_path: Path | str = DEFAULT_PRESETS_PATH,
    lazy: bool = True,
) -> FastAPI:
    app = FastAPI(title="Oncrawl API Explorer")
    app.state.capabilities = capabilities
    app.state.client = client
    app.state.presets_path = Path(presets_path)
    app.state.lazy = lazy

    # Błędy Oncrawl mają czytelny powód (np. "field X cannot be displayed") —
    # bez tych handlerów wypadały jako gołe 500 "Internal Server Error".
    @app.exception_handler(OncrawlAPIError)
    async def _api_error(request: Request, exc: OncrawlAPIError):
        status = exc.status if 400 <= exc.status < 600 else 502
        return JSONResponse(
            status_code=status,
            content={
                "detail": exc.short_reason(),
                "type": exc.type,
                "code": exc.code,
                "fields": exc.fields,
            },
        )

    @app.exception_handler(OncrawlNetworkError)
    async def _net_error(request: Request, exc: OncrawlNetworkError):
        return JSONResponse(status_code=504, content={"detail": f"Network error: {exc}"})

    @app.exception_handler(OncrawlError)
    async def _generic_error(request: Request, exc: OncrawlError):
        return JSONResponse(status_code=502, content={"detail": str(exc)})

    def get_caps() -> Capabilities:
        if app.state.capabilities is None and app.state.lazy:
            if Path("capabilities.json").exists():
                app.state.capabilities = Capabilities.load("capabilities.json")
        if app.state.capabilities is None:
            raise HTTPException(
                503,
                "capabilities.json is missing - run `python cli.py discover` first.",
            )
        return app.state.capabilities

    def get_client() -> OncrawlClient:
        if app.state.client is None and app.state.lazy:
            app.state.client = OncrawlClient.from_settings(load_settings())
        if app.state.client is None:
            raise HTTPException(503, "Oncrawl API client is not available.")
        return app.state.client

    # --- statyka ---------------------------------------------------------
    @app.get("/", response_class=HTMLResponse)
    def index() -> str:
        html = WEB_DIR / "index.html"
        if not html.exists():
            raise HTTPException(404, "web/index.html not found.")
        return html.read_text("utf-8")

    # --- metadane --------------------------------------------------------
    @app.get("/api/projects")
    def projects() -> dict:
        return {"projects": get_caps().project_summaries()}

    @app.get("/api/projects/{project_id}/crawls")
    def crawls(project_id: str) -> dict:
        proj = get_caps().project(project_id)
        if proj is None:
            raise HTTPException(404, f"Unknown project: {project_id}")
        return {
            "crawls": proj.get("crawls", []),
            "last_finished_crawl_id": proj.get("last_finished_crawl_id"),
        }

    # --- MCP: status, konfiguracja, self-test ---------------------------
    @app.get("/api/mcp/status")
    def mcp_status() -> dict:
        """Czy MCP jest gotowy + gotowe wpisy konfiguracyjne per klient."""
        return mcp_status_mod.status()

    @app.post("/api/mcp/selftest")
    async def mcp_selftest() -> dict:
        """Uruchamia serwer MCP i sprawdza handshake — bez żadnego klienta."""
        return await mcp_status_mod.run_selftest()

    @app.get("/api/recipes")
    def recipes(project_id: str, data_type: str) -> dict:
        """Gotowe recepty SEO wykonalne dla tego projektu i data_type."""
        fs = get_caps().fieldset(project_id, data_type)
        return {"recipes": applicable_recipes(fs, data_type)}

    @app.get("/api/fields")
    def fields(project_id: str, data_type: str) -> dict:
        fs = get_caps().fieldset(project_id, data_type)
        return {
            "project_id": project_id,
            "data_type": data_type,
            "fields": fs.all(),
            "default_display": fs.default_display_fields(),
        }

    # --- dane ------------------------------------------------------------
    @app.post("/api/query")
    def query(req: QueryRequest) -> dict:
        _validate_oql(app, req)
        path = _data_path(req)
        res = get_client().search(
            path,
            fields=req.fields,
            oql=req.oql,
            sort=req.sort,
            limit=req.limit,
            offset=req.offset,
        )
        return res

    @app.post("/api/export")
    def export(req: ExportRequest):
        _validate_oql(app, req)
        path = _data_path(req)
        cli = get_client()
        fname = f"{req.data_type}_{req.crawl_id or req.project_id}"

        if req.file_type == "xlsx":
            data = _build_xlsx(cli, path, req)
            return StreamingResponse(
                io.BytesIO(data),
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={"Content-Disposition": f'attachment; filename="{fname}.xlsx"'},
            )

        # CSV — prawdziwy streaming z API.
        def gen():
            for line in cli.export_lines(path, fields=req.fields, oql=req.oql, file_type="csv"):
                yield line + "\n"

        return StreamingResponse(
            gen(),
            media_type="text/csv",
            headers={"Content-Disposition": f'attachment; filename="{fname}.csv"'},
        )

    # --- presety ---------------------------------------------------------
    @app.get("/api/presets")
    def list_presets() -> dict:
        return {"presets": _load_presets(app.state.presets_path)}

    @app.post("/api/presets")
    def save_preset(preset: Preset) -> dict:
        presets = _load_presets(app.state.presets_path)
        presets = [p for p in presets if p.get("name") != preset.name]
        presets.append(preset.model_dump())
        _save_presets(app.state.presets_path, presets)
        return {"presets": presets}

    @app.delete("/api/presets/{name}")
    def delete_preset(name: str) -> dict:
        presets = [p for p in _load_presets(app.state.presets_path) if p.get("name") != name]
        _save_presets(app.state.presets_path, presets)
        return {"presets": presets}

    return app


# --- pomocnicze eksportu/presetów ----------------------------------------- #
def _build_xlsx(client: OncrawlClient, path: str, req: ExportRequest) -> bytes:
    """Buduje XLSX z eksportu (write_only, oszczędnie pamięciowo)."""
    from openpyxl import Workbook

    wb = Workbook(write_only=True)
    ws = wb.create_sheet(req.data_type[:31] or "data")
    header_written = False
    header = list(req.fields)
    for row in client.iter_export(path, fields=req.fields, oql=req.oql, file_type="json"):
        if not header_written:
            header = header or list(row.keys())
            ws.append(header)
            header_written = True
        ws.append([row.get(col) for col in header])
    if not header_written:
        ws.append(header or ["(brak danych)"])
    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


def _load_presets(path: Path) -> list[dict]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text("utf-8"))
        return data if isinstance(data, list) else []
    except (OSError, json.JSONDecodeError):
        return []


def _save_presets(path: Path, presets: list[dict]) -> None:
    path.write_text(json.dumps(presets, ensure_ascii=False, indent=2), "utf-8")


# Instancja dla `uvicorn app:app`.
app = create_app()


def main() -> None:
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=False)


if __name__ == "__main__":
    main()
