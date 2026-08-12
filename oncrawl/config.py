"""Konfiguracja ładowana ze środowiska / .env.

Token żyje wyłącznie tutaj i w nagłówku Authorization. Nigdy nie jest
logowany ani serializowany do capabilities.json / cache.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

DEFAULT_BASE_URL = "https://app.oncrawl.com/api/v2"


class MissingTokenError(RuntimeError):
    """Brak ONCRAWL_TOKEN w środowisku/.env."""


@dataclass(frozen=True)
class Settings:
    token: str
    base_url: str = DEFAULT_BASE_URL
    cache_dir: Path = Path(".cache")
    timeout: float = 30.0
    max_retries: int = 5
    concurrency: int = 4

    def redacted(self) -> dict:
        """Reprezentacja bez sekretu — do logów i debugowania."""
        return {
            "base_url": self.base_url,
            "cache_dir": str(self.cache_dir),
            "timeout": self.timeout,
            "max_retries": self.max_retries,
            "concurrency": self.concurrency,
            "token": _mask(self.token),
        }


def _mask(token: str) -> str:
    if not token:
        return "<empty>"
    if len(token) <= 8:
        return "*" * len(token)
    return f"{token[:4]}…{token[-4:]}"


def _get_float(name: str, default: float) -> float:
    raw = os.environ.get(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return float(raw)
    except ValueError:
        return default


def _get_int(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def load_settings(*, dotenv_path: str | os.PathLike | None = None) -> Settings:
    """Wczytuje ustawienia z .env i zmiennych środowiskowych.

    Zmienne środowiskowe mają pierwszeństwo nad .env (override=False).
    """
    load_dotenv(dotenv_path=dotenv_path, override=False)

    token = os.environ.get("ONCRAWL_TOKEN", "").strip()
    if not token:
        raise MissingTokenError(
            "Brak ONCRAWL_TOKEN. Skopiuj .env.example do .env i wstaw token "
            "(scope'y: account:read, projects:read do samego discovery)."
        )

    return Settings(
        token=token,
        base_url=os.environ.get("ONCRAWL_BASE_URL", DEFAULT_BASE_URL).rstrip("/"),
        cache_dir=Path(os.environ.get("ONCRAWL_CACHE_DIR", ".cache")),
        timeout=_get_float("ONCRAWL_TIMEOUT", 30.0),
        max_retries=_get_int("ONCRAWL_MAX_RETRIES", 5),
        concurrency=_get_int("ONCRAWL_CONCURRENCY", 4),
    )
