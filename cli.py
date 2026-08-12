"""CLI spinający całość (typer).

    python cli.py discover [--project ID]        # Etap 1
    python cli.py serve [--port 8000]            # Etap 3 (explorer)
    python cli.py projects                       # z capabilities.json (offline)
    python cli.py fields PROJECT DATA_TYPE       # tabela pól (offline)
    python cli.py query PROJECT DATA_TYPE ...    # strzał do API
    python cli.py export PROJECT DATA_TYPE OUT   # eksport CSV/XLSX
"""

from __future__ import annotations

import json
from pathlib import Path

import typer

from oncrawl.capabilities import CRAWL_DATA_TYPES, Capabilities
from oncrawl.client import (
    OncrawlClient,
    crawl_data_path,
    logs_events_path,
    ranking_path,
)
from oncrawl.config import load_settings

cli = typer.Typer(add_completion=False, help="Oncrawl API Explorer")


def _load_caps(path: str) -> Capabilities:
    p = Path(path)
    if not p.exists():
        typer.secho(f"Brak {path}. Uruchom: python cli.py discover", fg="red")
        raise typer.Exit(2)
    return Capabilities.load(p)


def _data_path(caps: Capabilities, project: str, data_type: str, crawl_id: str | None) -> str:
    if data_type in CRAWL_DATA_TYPES:
        if not crawl_id:
            proj = caps.project(project) or {}
            crawl_id = proj.get("last_finished_crawl_id")
        if not crawl_id:
            typer.secho("Ten data_type wymaga --crawl-id (brak też ostatniego crawla).", fg="red")
            raise typer.Exit(2)
        return crawl_data_path(crawl_id, data_type)
    if data_type == "logs":
        return logs_events_path(project)
    if data_type == "ranking_performance":
        return ranking_path(project)
    typer.secho(f"Nieznany data_type: {data_type}", fg="red")
    raise typer.Exit(2)


@cli.command()
def discover(
    project: list[str] = typer.Option(None, "--project", help="Ogranicz do project_id."),
    no_cache: bool = typer.Option(False, "--no-cache"),
):
    """Etap 1 — zmapuj konto do capabilities.json / CAPABILITIES.md."""
    import discovery

    argv = []
    for pid in project or []:
        argv += ["--project", pid]
    if no_cache:
        argv.append("--no-cache")
    raise typer.Exit(discovery.main(argv))


@cli.command()
def serve(host: str = "127.0.0.1", port: int = 8000):
    """Etap 3 — uruchom explorer (FastAPI + frontend)."""
    import uvicorn

    typer.secho(f"→ http://{host}:{port}", fg="green")
    uvicorn.run("app:app", host=host, port=port, reload=False)


@cli.command()
def projects(capabilities: str = "capabilities.json"):
    """Wypisz projekty i dostępne data_type (offline, z capabilities.json)."""
    caps = _load_caps(capabilities)
    for p in caps.project_summaries():
        avail = ", ".join(dt for dt, on in p["available_data_types"].items() if on) or "—"
        flag = " ⛔" + (p["error"] or "") if p["error"] else ""
        typer.echo(f"{p['id']}  {p['name'] or ''}{flag}")
        typer.echo(f"    data_type: {avail}")


@cli.command()
def fields(project: str, data_type: str, capabilities: str = "capabilities.json"):
    """Wypisz pola data_type (offline)."""
    caps = _load_caps(capabilities)
    fs = caps.fieldset(project, data_type)
    if len(fs) == 0:
        typer.secho("Brak pól (niedostępne albo zły data_type). Sprawdź `projects`.", fg="yellow")
        raise typer.Exit(1)
    typer.echo(f"{'pole':30} {'typ':10} filtr sort disp  agregacje")
    for f in fs.all():
        typer.echo(
            f"{f.get('name',''):30} {str(f.get('type','')):10} "
            f"{'T' if f.get('can_filter') else '-':5} "
            f"{'T' if f.get('can_sort') else '-':4} "
            f"{'T' if f.get('can_display') else '-':4}  "
            f"{','.join(f.get('agg_metric_methods') or []) or '-'}"
        )


@cli.command()
def query(
    project: str,
    data_type: str,
    crawl_id: str = typer.Option(None, "--crawl-id"),
    field: list[str] = typer.Option(None, "--field", help="Kolumna (powtarzalne)."),
    oql_json: str = typer.Option(None, "--oql", help="OQL jako JSON."),
    sort: str = typer.Option(None, "--sort", help="field:asc|desc"),
    limit: int = 20,
    capabilities: str = "capabilities.json",
):
    """Strzał do API — pojedyncza strona danych."""
    caps = _load_caps(capabilities)
    path = _data_path(caps, project, data_type, crawl_id)
    oql = json.loads(oql_json) if oql_json else None
    with OncrawlClient.from_settings(load_settings()) as client:
        res = client.search(path, fields=field or [], oql=oql, sort=sort, limit=limit)
    typer.echo(f"total_hits: {res['total_hits']}")
    for row in res["rows"]:
        typer.echo(json.dumps(row, ensure_ascii=False))


@cli.command()
def export(
    project: str,
    data_type: str,
    out: str,
    crawl_id: str = typer.Option(None, "--crawl-id"),
    field: list[str] = typer.Option(None, "--field"),
    oql_json: str = typer.Option(None, "--oql"),
    capabilities: str = "capabilities.json",
):
    """Eksport do pliku (CSV wg rozszerzenia; .jsonl = JSONL) strumieniowo."""
    caps = _load_caps(capabilities)
    path = _data_path(caps, project, data_type, crawl_id)
    oql = json.loads(oql_json) if oql_json else None
    file_type = "json" if out.endswith(".jsonl") else "csv"
    n = 0
    with OncrawlClient.from_settings(load_settings()) as client, open(out, "w", encoding="utf-8") as fh:
        for line in client.export_lines(path, fields=field or [], oql=oql, file_type=file_type):
            fh.write(line + "\n")
            n += 1
    typer.secho(f"Zapisano {n} linii → {out}", fg="green")


if __name__ == "__main__":
    cli()
