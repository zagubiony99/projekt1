"""Typowane wyjątki mapujące formaty błędów Oncrawl API.

Błąd API to JSON: {type, code, message, fields}. Mapowanie statusów/typów
wg dokumentacji (developer.oncrawl.com):

    unauthorized                401
    forbidden                   403  (code: no_active_subscription |
                                       feature_not_available | unauthorized)
    quota_error                 403
    invalid_request             400
    invalid_request_parameters  400
    resource_not_found          404
    duplicate_entry             400
    invalid_state_for_request   409
    internal_error              500
"""

from __future__ import annotations

from typing import Any


class OncrawlError(Exception):
    """Bazowy wyjątek biblioteki."""


class OncrawlNetworkError(OncrawlError):
    """Błąd transportu (timeout, DNS, zerwane połączenie) — nie odpowiedź API."""


class OncrawlAPIError(OncrawlError):
    """Ustrukturyzowany błąd zwrócony przez API."""

    def __init__(
        self,
        *,
        status: int,
        type: str | None = None,
        code: str | None = None,
        message: str | None = None,
        fields: Any = None,
        raw: Any = None,
    ) -> None:
        self.status = status
        self.type = type
        self.code = code
        self.message = message or ""
        self.fields = fields
        self.raw = raw
        summary = message or type or f"HTTP {status}"
        detail = f" (code={code})" if code else ""
        super().__init__(f"[{status}] {type or 'error'}: {summary}{detail}")

    def short_reason(self) -> str:
        """Jednolinijkowy powód do zapisania w capabilities (bez sekretów)."""
        parts = [f"HTTP {self.status}"]
        if self.type:
            parts.append(self.type)
        if self.code:
            parts.append(self.code)
        if self.message:
            parts.append(self.message)
        return " · ".join(parts)


class UnauthorizedError(OncrawlAPIError):
    """401 — brak/niepoprawny token albo zły scope."""


class ForbiddenError(OncrawlAPIError):
    """403 forbidden — brak subskrypcji, feature niedostępny, brak uprawnień."""


class FeatureNotAvailableError(ForbiddenError):
    """403 forbidden, code=feature_not_available."""


class NoActiveSubscriptionError(ForbiddenError):
    """403 forbidden, code=no_active_subscription."""


class QuotaError(OncrawlAPIError):
    """403 quota_error — wyczerpane dzienne quota endpointu."""


class InvalidRequestError(OncrawlAPIError):
    """400 invalid_request / invalid_request_parameters."""


class ResourceNotFoundError(OncrawlAPIError):
    """404 — zasób nie istnieje."""


class DuplicateEntryError(OncrawlAPIError):
    """400 duplicate_entry."""


class InvalidStateError(OncrawlAPIError):
    """409 invalid_state_for_request."""


class InternalServerError(OncrawlAPIError):
    """500 internal_error."""


# Grupy pomocnicze dla discovery — te wyjątki oznaczają "brak dostępu",
# a nie "coś się zepsuło": zapisujemy powód i idziemy dalej.
ACCESS_DENIED_ERRORS = (
    ForbiddenError,
    FeatureNotAvailableError,
    NoActiveSubscriptionError,
    QuotaError,
    ResourceNotFoundError,
    UnauthorizedError,
)


def _classify(status: int, type_: str | None, code: str | None) -> type[OncrawlAPIError]:
    if type_ == "quota_error":
        return QuotaError
    if type_ == "forbidden" or status == 403:
        if code == "feature_not_available":
            return FeatureNotAvailableError
        if code == "no_active_subscription":
            return NoActiveSubscriptionError
        return ForbiddenError
    if type_ == "unauthorized" or status == 401:
        return UnauthorizedError
    if type_ == "resource_not_found" or status == 404:
        return ResourceNotFoundError
    if type_ == "duplicate_entry":
        return DuplicateEntryError
    if type_ == "invalid_state_for_request" or status == 409:
        return InvalidStateError
    if type_ in ("invalid_request", "invalid_request_parameters") or status == 400:
        return InvalidRequestError
    if type_ == "internal_error" or status >= 500:
        return InternalServerError
    return OncrawlAPIError


def api_error_from_body(status: int, body: Any) -> OncrawlAPIError:
    """Buduje właściwy podtyp wyjątku z ciała odpowiedzi błędu.

    Odporne na nie-JSON i nietypowe kształty — wtedy zwraca ogólny
    OncrawlAPIError z surową treścią.
    """
    type_ = code = message = None
    fields = None
    if isinstance(body, dict):
        type_ = body.get("type")
        code = body.get("code")
        message = body.get("message")
        fields = body.get("fields")

    cls = _classify(status, type_, code)
    return cls(
        status=status,
        type=type_,
        code=code,
        message=message,
        fields=fields,
        raw=body,
    )
