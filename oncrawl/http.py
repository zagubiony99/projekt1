"""Cienka sesja HTTP nad httpx: auth, retry/backoff, cache GET-ów na dysku.

To fundament wspólny dla discovery (Etap 1) i pełnego klienta (Etap 2).
Świadomie trzymamy to małe i przewidywalne:

- Authorization: Bearer {token} dodawany raz, nigdy nie logowany.
- Retry z wykładniczym backoffem na 429 i 5xx; szanuje Retry-After.
- Cache tylko dla GET (część endpointów ma dzienne quota) — klucz z
  metody+ścieżki+parametrów, treść zapisywana jako JSON w cache_dir.
- Błędy odpowiedzi mapowane na typowane wyjątki z errors.py.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from pathlib import Path
from typing import Any, Iterator, Mapping
from urllib.parse import urlencode

import httpx

from .config import Settings
from .errors import OncrawlNetworkError, api_error_from_body

logger = logging.getLogger("oncrawl.http")

_RETRY_STATUSES = frozenset({429, 500, 502, 503, 504})


def _cache_key(method: str, path: str, params: Mapping[str, Any] | None) -> str:
    norm_params = ""
    if params:
        # Sortujemy, by klucz był deterministyczny niezależnie od kolejności.
        items = sorted((str(k), str(v)) for k, v in params.items())
        norm_params = urlencode(items)
    payload = f"{method.upper()} {path}?{norm_params}"
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]
    # Czytelny prefiks z ostatniego segmentu ścieżki ułatwia grzebanie w .cache.
    slug = path.strip("/").replace("/", "_")[-60:] or "root"
    return f"{slug}.{digest}"


class OncrawlSession:
    """Synchronincza sesja z retry, backoffem i cache GET-ów.

    Parametry sieciowe pochodzą z Settings. `transport` pozwala wstrzyknąć
    httpx.MockTransport w testach, bez ruszania sieci.
    """

    def __init__(
        self,
        settings: Settings,
        *,
        transport: httpx.BaseTransport | None = None,
        sleep=time.sleep,
    ) -> None:
        self._settings = settings
        self._sleep = sleep
        self._cache_dir = Path(settings.cache_dir)
        self._client = httpx.Client(
            base_url=settings.base_url,
            headers={
                "Authorization": f"Bearer {settings.token}",
                "Accept": "application/json",
            },
            timeout=settings.timeout,
            transport=transport,
        )

    # --- lifecycle -------------------------------------------------------
    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "OncrawlSession":
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    # --- niskopoziomowe --------------------------------------------------
    def request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json_body: Any = None,
        stream: bool = False,
    ) -> httpx.Response:
        """Wykonuje żądanie z retry. Zwraca surową odpowiedź (2xx) lub rzuca.

        `stream=True` zwraca otwartą odpowiedź do strumieniowego czytania —
        wywołujący odpowiada za jej zamknięcie (eksporty > 10k).
        """
        attempt = 0
        while True:
            attempt += 1
            try:
                req = self._client.build_request(
                    method, path, params=params, json=json_body
                )
                response = self._client.send(req, stream=stream)
            except httpx.TimeoutException as exc:
                if attempt <= self._settings.max_retries:
                    self._backoff(attempt, reason=f"timeout: {exc!s}")
                    continue
                raise OncrawlNetworkError(f"Timeout po {attempt} próbach: {exc}") from exc
            except httpx.TransportError as exc:
                if attempt <= self._settings.max_retries:
                    self._backoff(attempt, reason=f"transport: {exc!s}")
                    continue
                raise OncrawlNetworkError(str(exc)) from exc

            if response.status_code in _RETRY_STATUSES and attempt <= self._settings.max_retries:
                if stream:
                    response.close()
                self._backoff(
                    attempt,
                    reason=f"HTTP {response.status_code}",
                    retry_after=response.headers.get("Retry-After"),
                )
                continue

            if response.status_code >= 400:
                self._raise_for_error(response, stream=stream)

            return response

    def get_json(
        self,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        cache: bool = True,
    ) -> Any:
        """GET zwracający sparsowany JSON, z opcjonalnym cache na dysku."""
        if cache:
            cached = self._read_cache("GET", path, params)
            if cached is not None:
                logger.debug("cache hit: %s", path)
                return cached

        response = self.request("GET", path, params=params)
        data = response.json()
        if cache:
            self._write_cache("GET", path, params, data)
        return data

    def post_json(
        self,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json_body: Any = None,
    ) -> Any:
        """POST zwracający sparsowany JSON (bez cache — zapytania mutują/są zmienne)."""
        response = self.request("POST", path, params=params, json_body=json_body)
        return response.json()

    def stream_lines(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json_body: Any = None,
    ) -> Iterator[str]:
        """Strumień linii (eksport JSONL/CSV) bez ładowania całości do pamięci."""
        response = self.request(
            method, path, params=params, json_body=json_body, stream=True
        )
        try:
            yield from response.iter_lines()
        finally:
            response.close()

    # --- wewnętrzne ------------------------------------------------------
    def _raise_for_error(self, response: httpx.Response, *, stream: bool) -> None:
        if stream:
            response.read()
        try:
            body: Any = response.json()
        except (json.JSONDecodeError, ValueError):
            body = response.text
        raise api_error_from_body(response.status_code, body)

    def _backoff(self, attempt: int, *, reason: str, retry_after: str | None = None) -> None:
        delay = self._compute_delay(attempt, retry_after)
        logger.warning(
            "retry %d/%d za %.1fs (%s)",
            attempt,
            self._settings.max_retries,
            delay,
            reason,
        )
        self._sleep(delay)

    def _compute_delay(self, attempt: int, retry_after: str | None) -> float:
        if retry_after:
            try:
                return max(0.0, float(retry_after))
            except ValueError:
                pass  # Retry-After jako data HTTP — pomijamy, użyjemy backoffu.
        # Wykładniczo: 1, 2, 4, 8, 16 ... z górnym limitem.
        return float(min(2 ** (attempt - 1), 30))

    def _cache_path(self, method: str, path: str, params: Mapping[str, Any] | None) -> Path:
        return self._cache_dir / f"{_cache_key(method, path, params)}.json"

    def _read_cache(self, method: str, path: str, params) -> Any:
        fp = self._cache_path(method, path, params)
        if not fp.exists():
            return None
        try:
            return json.loads(fp.read_text("utf-8"))
        except (OSError, json.JSONDecodeError):
            return None

    def _write_cache(self, method: str, path: str, params, data: Any) -> None:
        try:
            self._cache_dir.mkdir(parents=True, exist_ok=True)
            fp = self._cache_path(method, path, params)
            fp.write_text(json.dumps(data, ensure_ascii=False), "utf-8")
        except OSError as exc:  # cache to optymalizacja, nie krytyczna ścieżka
            logger.debug("nie udało się zapisać cache: %s", exc)
