"""Diagnostyka i konfiguracja serwera MCP — dla panelu w explorerze.

Wszystko lokalne: sprawdza wymagania (pakiet mcp, .env, capabilities.json),
generuje gotowe wpisy konfiguracyjne dla klientów MCP i potrafi uruchomić
self-test (handshake po stdio), ten sam, co `python cli.py mcp-test`.

Token nigdy nie trafia do generowanej konfiguracji — klient czyta go z .env.
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from importlib.util import find_spec
from pathlib import Path

SERVER_FILE = "mcp_server.py"
HANDSHAKE_TIMEOUT = 25.0


def _project_dir() -> Path:
    return Path.cwd().resolve()


def requirements() -> list[dict]:
    """Lista warunków, które muszą być spełnione, by MCP działał."""
    root = _project_dir()
    mcp_installed = find_spec("mcp") is not None
    return [
        {
            "id": "mcp_package",
            "label": "Pakiet 'mcp' zainstalowany",
            "ok": mcp_installed,
            "hint": 'pip install "mcp>=1.2"',
        },
        {
            "id": "server_file",
            "label": f"Plik {SERVER_FILE} obecny",
            "ok": (root / SERVER_FILE).exists(),
            "hint": "Rozpakuj pełne archiwum projektu.",
        },
        {
            "id": "env_token",
            "label": "Token w .env (ONCRAWL_TOKEN)",
            "ok": bool(os.environ.get("ONCRAWL_TOKEN")) or _env_has_token(root),
            "hint": "Skopiuj .env.example do .env i wpisz ONCRAWL_TOKEN.",
        },
        {
            "id": "capabilities",
            "label": "capabilities.json wygenerowany",
            "ok": (root / "capabilities.json").exists(),
            "hint": "python cli.py discover",
        },
    ]


def _env_has_token(root: Path) -> bool:
    env = root / ".env"
    if not env.exists():
        return False
    try:
        for line in env.read_text("utf-8").splitlines():
            key, _, value = line.partition("=")
            if key.strip() == "ONCRAWL_TOKEN" and value.strip():
                return True
    except OSError:
        return False
    return False


def client_configs() -> list[dict]:
    """Gotowe wpisy konfiguracyjne per klient MCP (bez tokena)."""
    root = _project_dir()
    root_str = str(root)
    python = sys.executable or "python"
    server_abs = str(root / SERVER_FILE)

    return [
        {
            "id": "vscode",
            "name": "VS Code",
            "path": ".vscode/mcp.json  (w folderze projektu)",
            "steps": [
                "Otwórz ten folder w VS Code.",
                "Ctrl+Shift+P → 'MCP: List Servers' → oncrawl → Start.",
                "W Copilot Chat przełącz na tryb Agent.",
            ],
            "note": "Wymaga VS Code 1.102+ i GitHub Copilot. Plik jest już w projekcie.",
            "config": json.dumps(
                {"servers": {"oncrawl": {
                    "type": "stdio", "command": "python",
                    "args": [SERVER_FILE], "cwd": "${workspaceFolder}"}}},
                indent=2,
            ),
        },
        {
            "id": "claude_desktop",
            "name": "Claude Desktop",
            "path": (
                r"%APPDATA%\Claude\claude_desktop_config.json"
                if os.name == "nt"
                else "~/Library/Application Support/Claude/claude_desktop_config.json"
            ),
            "steps": [
                "Wklej poniższy blok do pliku konfiguracyjnego.",
                "Zrestartuj Claude Desktop.",
                "Narzędzia Oncrawl pojawią się w rozmowie.",
            ],
            "note": "Wymaga zainstalowanej aplikacji Claude Desktop.",
            "config": json.dumps(
                {"mcpServers": {"oncrawl": {
                    "command": python, "args": [server_abs], "cwd": root_str}}},
                indent=2,
            ),
        },
        {
            "id": "cursor",
            "name": "Cursor",
            "path": ".cursor/mcp.json  (w folderze projektu)",
            "steps": ["Utwórz plik z poniższą treścią.", "Zrestartuj Cursor."],
            "note": "Działa też globalnie: ~/.cursor/mcp.json",
            "config": json.dumps(
                {"mcpServers": {"oncrawl": {
                    "command": python, "args": [SERVER_FILE], "cwd": root_str}}},
                indent=2,
            ),
        },
        {
            "id": "claude_code",
            "name": "Claude Code (CLI)",
            "path": "— (komenda, nie plik)",
            "steps": ["Uruchom w terminalu, w tym folderze:"],
            "note": "Konfiguracja zapisuje się automatycznie.",
            "config": f"claude mcp add oncrawl -- {python} {SERVER_FILE}",
        },
    ]


def tools_reference() -> list[dict]:
    """Opis narzędzi wystawianych przez serwer (do panelu)."""
    return [
        {"name": "list_projects", "desc": "Lista projektów i dostępnych typów danych."},
        {"name": "list_crawls", "desc": "Crawle projektu wraz ze statusem."},
        {"name": "list_fields", "desc": "Pola data_type z flagami i agregacjami (z wyszukiwaniem)."},
        {"name": "query_data", "desc": "Wiersze danych z filtrem OQL (do 200 wierszy)."},
        {"name": "aggregate_data", "desc": "Agregacje liczone po stronie API na całym zbiorze."},
        {"name": "export_data", "desc": "Eksport pełnego wyniku do pliku CSV (omija limit 10k)."},
    ]


async def run_selftest() -> dict:
    """Uruchamia mcp_server.py i wykonuje handshake + tools/list po stdio."""
    root = _project_dir()
    if not (root / SERVER_FILE).exists():
        return {"ok": False, "error": f"Brak pliku {SERVER_FILE} w {root}"}
    if find_spec("mcp") is None:
        return {"ok": False, "error": 'Brak pakietu mcp. Zainstaluj: pip install "mcp>=1.2"'}

    try:
        proc = await asyncio.create_subprocess_exec(
            sys.executable, SERVER_FILE,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(root),
        )
    except OSError as exc:
        return {"ok": False, "error": f"Nie udało się uruchomić serwera: {exc}"}

    def send(obj):
        proc.stdin.write((json.dumps(obj) + "\n").encode())

    try:
        send({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
            "protocolVersion": "2024-11-05", "capabilities": {},
            "clientInfo": {"name": "explorer-selftest", "version": "1"}}})
        await proc.stdin.drain()
        line = await asyncio.wait_for(proc.stdout.readline(), HANDSHAKE_TIMEOUT)
        server_info = json.loads(line)["result"]["serverInfo"]

        send({"jsonrpc": "2.0", "method": "notifications/initialized"})
        send({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        await proc.stdin.drain()
        line = await asyncio.wait_for(proc.stdout.readline(), HANDSHAKE_TIMEOUT)
        tools = [t["name"] for t in json.loads(line)["result"]["tools"]]

        return {"ok": True, "server": server_info, "tools": tools}
    except asyncio.TimeoutError:
        return {"ok": False, "error": "Serwer nie odpowiedział w czasie.",
                "stderr": await _drain(proc.stderr)}
    except Exception as exc:
        return {"ok": False, "error": f"{type(exc).__name__}: {exc}",
                "stderr": await _drain(proc.stderr)}
    finally:
        # Domknij podproces do końca — inaczej asyncio zgłasza
        # "Event loop is closed" przy zbieraniu transportu.
        try:
            if proc.returncode is None:
                proc.terminate()
                try:
                    await asyncio.wait_for(proc.wait(), 5.0)
                except asyncio.TimeoutError:
                    proc.kill()
                    await proc.wait()
        except ProcessLookupError:
            pass


async def _drain(stream) -> str:
    try:
        data = await asyncio.wait_for(stream.read(), 2.0)
        return data.decode(errors="replace")[-1200:]
    except Exception:
        return ""


def status() -> dict:
    reqs = requirements()
    return {
        "project_dir": str(_project_dir()),
        "python": sys.executable,
        "ready": all(r["ok"] for r in reqs),
        "requirements": reqs,
        "clients": client_configs(),
        "tools": tools_reference(),
    }
