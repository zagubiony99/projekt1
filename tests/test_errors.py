"""Testy mapowania formatów błędów Oncrawl na typowane wyjątki."""

from oncrawl.errors import (
    DuplicateEntryError,
    FeatureNotAvailableError,
    ForbiddenError,
    InternalServerError,
    InvalidRequestError,
    InvalidStateError,
    NoActiveSubscriptionError,
    QuotaError,
    ResourceNotFoundError,
    UnauthorizedError,
    api_error_from_body,
)


def test_unauthorized():
    e = api_error_from_body(401, {"type": "unauthorized", "message": "bad token"})
    assert isinstance(e, UnauthorizedError)
    assert e.status == 401


def test_forbidden_feature_not_available():
    e = api_error_from_body(403, {"type": "forbidden", "code": "feature_not_available"})
    assert isinstance(e, FeatureNotAvailableError)
    assert isinstance(e, ForbiddenError)


def test_forbidden_no_subscription():
    e = api_error_from_body(403, {"type": "forbidden", "code": "no_active_subscription"})
    assert isinstance(e, NoActiveSubscriptionError)


def test_quota_error_is_not_generic_forbidden():
    e = api_error_from_body(403, {"type": "quota_error", "message": "daily limit"})
    assert isinstance(e, QuotaError)
    assert not isinstance(e, ForbiddenError)


def test_resource_not_found():
    assert isinstance(api_error_from_body(404, {"type": "resource_not_found"}), ResourceNotFoundError)


def test_duplicate_entry():
    assert isinstance(api_error_from_body(400, {"type": "duplicate_entry"}), DuplicateEntryError)


def test_invalid_state():
    assert isinstance(api_error_from_body(409, {"type": "invalid_state_for_request"}), InvalidStateError)


def test_invalid_request_variants():
    assert isinstance(api_error_from_body(400, {"type": "invalid_request"}), InvalidRequestError)
    assert isinstance(api_error_from_body(400, {"type": "invalid_request_parameters"}), InvalidRequestError)


def test_internal_error():
    assert isinstance(api_error_from_body(500, {"type": "internal_error"}), InternalServerError)


def test_non_json_body_is_tolerated():
    e = api_error_from_body(500, "<html>Bad Gateway</html>")
    assert e.status == 500
    assert e.raw == "<html>Bad Gateway</html>"


def test_short_reason_has_no_secret():
    e = api_error_from_body(403, {"type": "quota_error", "code": None, "message": "limit"})
    reason = e.short_reason()
    assert "403" in reason and "quota_error" in reason and "limit" in reason
