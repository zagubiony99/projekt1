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
            "label": "'mcp' package installed",
            "ok": mcp_installed,
            "hint": 'pip install "mcp>=1.2"',
        },
        {
            "id": "server_file",
            "label": f"{SERVER_FILE} present",
            "ok": (root / SERVER_FILE).exists(),
            "hint": "Unzip the full project archive.",
        },
        {
            "id": "env_token",
            "label": "Token in .env (ONCRAWL_TOKEN)",
            "ok": bool(os.environ.get("ONCRAWL_TOKEN")) or _env_has_token(root),
            "hint": "Copy .env.example to .env and set ONCRAWL_TOKEN.",
        },
        {
            "id": "capabilities",
            "label": "capabilities.json generated",
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
            "path": ".vscode/mcp.json  (in the project folder)",
            "steps": [
                "Open this folder in VS Code.",
                "Ctrl+Shift+P -> 'MCP: List Servers' -> oncrawl -> Start.",
                "Switch Copilot Chat to Agent mode.",
            ],
            "note": "Requires VS Code 1.102+ and GitHub Copilot. The file already ships with this project.",
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
                "Paste the block below into the config file.",
                "Restart Claude Desktop.",
                "The Oncrawl tools will appear in the conversation.",
            ],
            "note": "Requires the Claude Desktop app to be installed.",
            "config": json.dumps(
                {"mcpServers": {"oncrawl": {
                    "command": python, "args": [server_abs], "cwd": root_str}}},
                indent=2,
            ),
        },
        {
            "id": "cursor",
            "name": "Cursor",
            "path": ".cursor/mcp.json  (in the project folder)",
            "steps": ["Create the file with the content below.", "Restart Cursor."],
            "note": "Also works globally: ~/.cursor/mcp.json",
            "config": json.dumps(
                {"mcpServers": {"oncrawl": {
                    "command": python, "args": [SERVER_FILE], "cwd": root_str}}},
                indent=2,
            ),
        },
        {
            "id": "claude_code",
            "name": "Claude Code (CLI)",
            "path": "- (a command, not a file)",
            "steps": ["Run this in a terminal, in this folder:"],
            "note": "The configuration is saved automatically.",
            "config": f"claude mcp add oncrawl -- {python} {SERVER_FILE}",
        },
    ]


def tools_reference() -> list[dict]:
    """Opis narzędzi wystawianych przez serwer (do panelu)."""
    return [
        {"name": "list_projects", "desc": "List of projects and their available data types."},
        {"name": "list_crawls", "desc": "Crawls of a project together with their status."},
        {"name": "list_fields", "desc": "Fields of a data_type, searchable; flags and aggregations on demand."},
        {"name": "query_data", "desc": "Data rows with an OQL filter (up to 200 rows)."},
        {"name": "aggregate_data", "desc": "Aggregations computed API-side over the whole data set."},
        {"name": "export_data", "desc": "Export the full result to a CSV file (bypasses the 10k limit)."},
    ]


async def run_selftest() -> dict:
    """Uruchamia mcp_server.py i wykonuje handshake + tools/list po stdio."""
    root = _project_dir()
    if not (root / SERVER_FILE).exists():
        return {"ok": False, "error": f"{SERVER_FILE} not found in {root}"}
    if find_spec("mcp") is None:
        return {"ok": False, "error": 'The mcp package is missing. Install it: pip install "mcp>=1.2"'}

    try:
        proc = await asyncio.create_subprocess_exec(
            sys.executable, SERVER_FILE,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(root),
        )
    except OSError as exc:
        return {"ok": False, "error": f"Could not start the server: {exc}"}

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
        return {"ok": False, "error": "The server did not respond in time.",
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
