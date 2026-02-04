"""Testes do cliente HTTP e do facade Notifica."""

from __future__ import annotations

import pytest
from pytest_httpx import HTTPXMock

from notifica import Notifica, AsyncNotifica
from notifica.client import NotificaClient
from notifica.errors import (
    ApiError,
    NotificaError,
    RateLimitError,
    TimeoutError,
    ValidationError,
)

from conftest import (
    BASE_URL,
    TEST_API_KEY,
    error_body,
    paginated_envelope,
    single_envelope,
)


# ── Constructor ──────────────────────────────────────


class TestConstructor:
    def test_throws_when_api_key_is_empty(self) -> None:
        with pytest.raises(NotificaError, match="API key"):
            Notifica("")

    def test_creates_all_resources(self) -> None:
        n = Notifica(TEST_API_KEY)
        assert n.notifications is not None
        assert n.templates is not None
        assert n.workflows is not None
        assert n.subscribers is not None
        assert n.channels is not None
        assert n.domains is not None
        assert n.webhooks is not None
        assert n.api_keys is not None
        assert n.analytics is not None
        assert n.sms is not None
        assert n.billing is not None
        assert n.inbox_embed is not None
        assert n.inbox is not None

    def test_accepts_kwargs(self) -> None:
        n = Notifica(
            TEST_API_KEY,
            base_url="https://custom.api/v1",
            timeout=5.0,
            max_retries=1,
            auto_idempotency=False,
        )
        assert n._client._base_url == "https://custom.api/v1"

    def test_strips_trailing_slashes(self) -> None:
        n = Notifica(TEST_API_KEY, base_url="https://api.local/v1///")
        assert n._client._base_url == "https://api.local/v1"


# ── Auth / Headers ───────────────────────────────────


class TestHeaders:
    def test_sends_bearer_token(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=paginated_envelope([]))
        client.notifications.list()
        request = httpx_mock.get_request()
        assert request is not None
        assert request.headers["authorization"] == f"Bearer {TEST_API_KEY}"

    def test_sends_user_agent(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=paginated_envelope([]))
        client.notifications.list()
        request = httpx_mock.get_request()
        assert request is not None
        assert "notifica-python/" in request.headers["user-agent"]

    def test_sends_json_content_type(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=paginated_envelope([]))
        client.notifications.list()
        request = httpx_mock.get_request()
        assert request is not None
        assert request.headers["content-type"] == "application/json"


# ── GET requests ─────────────────────────────────────


class TestGetRequests:
    def test_builds_url_with_path(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=paginated_envelope([]))
        client.notifications.list()
        request = httpx_mock.get_request()
        assert request is not None
        assert str(request.url).startswith(f"{BASE_URL}/notifications")

    def test_appends_query_parameters(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=paginated_envelope([]))
        client.notifications.list({"channel": "email", "limit": 50})
        request = httpx_mock.get_request()
        assert request is not None
        assert request.url.params["channel"] == "email"
        assert request.url.params["limit"] == "50"

    def test_omits_none_query_params(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=paginated_envelope([]))
        client.notifications.list({"channel": "email", "status": None})
        request = httpx_mock.get_request()
        assert request is not None
        assert "status" not in request.url.params


# ── POST requests ────────────────────────────────────


class TestPostRequests:
    def test_sends_post_with_json_body(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "n1"}))
        client.notifications.send({"channel": "email", "to": "a@b.com"})
        request = httpx_mock.get_request()
        assert request is not None
        assert request.method == "POST"
        import json
        body = json.loads(request.content)
        assert body == {"channel": "email", "to": "a@b.com"}


# ── PUT requests ─────────────────────────────────────


class TestPutRequests:
    def test_sends_put(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "t1"}))
        client.templates.update("tpl-1", {"name": "Updated"})
        request = httpx_mock.get_request()
        assert request is not None
        assert request.method == "PUT"


# ── DELETE requests ──────────────────────────────────


class TestDeleteRequests:
    def test_sends_delete_handles_204(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(status_code=204)
        client.templates.delete("tpl-1")
        request = httpx_mock.get_request()
        assert request is not None
        assert request.method == "DELETE"


# ── Idempotency ─────────────────────────────────────


class TestIdempotency:
    def test_auto_generates_idempotency_key_for_post(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "n1"}))
        client.notifications.send({"channel": "email", "to": "a@b.com"})
        request = httpx_mock.get_request()
        assert request is not None
        key = request.headers.get("idempotency-key")
        assert key is not None
        assert len(key) > 10

    def test_uses_custom_idempotency_key(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "n1"}))
        client.notifications.send(
            {"channel": "email", "to": "a@b.com"},
            options={"idempotency_key": "my-custom-key"},
        )
        request = httpx_mock.get_request()
        assert request is not None
        assert request.headers.get("idempotency-key") == "my-custom-key"

    def test_no_idempotency_key_when_disabled(
        self, no_idempotency_client: Notifica, httpx_mock: HTTPXMock
    ) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "n1"}))
        no_idempotency_client.notifications.send({"channel": "email", "to": "a@b.com"})
        request = httpx_mock.get_request()
        assert request is not None
        assert "idempotency-key" not in request.headers

    def test_no_idempotency_key_for_get(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=paginated_envelope([]))
        client.notifications.list()
        request = httpx_mock.get_request()
        assert request is not None
        assert "idempotency-key" not in request.headers

    def test_no_idempotency_key_for_put(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "t1"}))
        client.templates.update("tpl-1", {"name": "x"})
        request = httpx_mock.get_request()
        assert request is not None
        assert "idempotency-key" not in request.headers

    def test_unique_keys_per_request(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "n1"}))
        httpx_mock.add_response(json=single_envelope({"id": "n2"}))
        client.notifications.send({"channel": "email", "to": "a@b.com"})
        client.notifications.send({"channel": "email", "to": "b@c.com"})
        requests = httpx_mock.get_requests()
        key1 = requests[0].headers.get("idempotency-key")
        key2 = requests[1].headers.get("idempotency-key")
        assert key1 != key2


# ── Error handling ───────────────────────────────────


class TestErrorHandling:
    def test_validation_error_on_422(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            status_code=422,
            json=error_body("validation_failed", "Email inválido", {"email": ["is invalid"]}),
        )
        with pytest.raises(ValidationError) as exc_info:
            client.subscribers.create({"external_id": "x"})
        err = exc_info.value
        assert err.status == 422
        assert err.code == "validation_failed"
        assert err.details == {"email": ["is invalid"]}

    def test_rate_limit_error_on_429(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            status_code=429,
            json=error_body("rate_limit_exceeded", "Too many requests"),
            headers={"retry-after": "30"},
        )
        with pytest.raises(RateLimitError) as exc_info:
            client.notifications.list()
        err = exc_info.value
        assert err.status == 429
        assert err.retry_after == 30

    def test_api_error_on_401(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            status_code=401,
            json=error_body("unauthorized", "Invalid API key"),
        )
        with pytest.raises(ApiError) as exc_info:
            client.notifications.list()
        assert exc_info.value.status == 401
        assert exc_info.value.code == "unauthorized"

    def test_api_error_on_404(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            status_code=404,
            json=error_body("not_found", "Not found"),
        )
        with pytest.raises(ApiError) as exc_info:
            client.notifications.get("nonexistent")
        assert exc_info.value.status == 404

    def test_includes_request_id(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            status_code=500,
            json=error_body("internal", "Oops"),
            headers={"x-request-id": "req-abc-123"},
        )
        with pytest.raises(ApiError) as exc_info:
            client.notifications.list()
        assert exc_info.value.request_id == "req-abc-123"

    def test_error_hierarchy(self) -> None:
        v = ValidationError("test")
        assert isinstance(v, ValidationError)
        assert isinstance(v, ApiError)
        assert isinstance(v, NotificaError)
        assert isinstance(v, Exception)

        r = RateLimitError("test", 10)
        assert isinstance(r, RateLimitError)
        assert isinstance(r, ApiError)

        t = TimeoutError(5.0)
        assert isinstance(t, TimeoutError)
        assert isinstance(t, NotificaError)
        assert "5.0s" in str(t)


# ── Retries ──────────────────────────────────────────


class TestRetries:
    def test_retries_on_500(self, retrying_client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(status_code=500, json=error_body("internal", "err"))
        httpx_mock.add_response(status_code=500, json=error_body("internal", "err"))
        httpx_mock.add_response(status_code=500, json=error_body("internal", "err"))
        with pytest.raises(ApiError):
            retrying_client.notifications.list()
        # 1 initial + 2 retries = 3 total
        assert len(httpx_mock.get_requests()) == 3

    def test_succeeds_after_transient_500(self, retrying_client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(status_code=502, json=error_body("bad_gateway", "err"))
        httpx_mock.add_response(json=paginated_envelope([{"id": "n1"}]))
        result = retrying_client.notifications.list()
        assert len(result["data"]) == 1
        assert len(httpx_mock.get_requests()) == 2

    def test_does_not_retry_4xx(self, retrying_client: Notifica, httpx_mock: HTTPXMock) -> None:
        for status in [400, 401, 403, 404]:
            httpx_mock.reset()
            httpx_mock.add_response(status_code=status, json=error_body("err", "err"))
            with pytest.raises(ApiError):
                retrying_client.notifications.list()
            assert len(httpx_mock.get_requests()) == 1

    def test_no_retry_when_max_retries_0(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(status_code=500, json=error_body("internal", "err"))
        with pytest.raises(ApiError):
            client.notifications.list()
        assert len(httpx_mock.get_requests()) == 1


# ── Pagination ───────────────────────────────────────


class TestPagination:
    def test_manual_cursor_pagination(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=paginated_envelope([{"id": "1"}], "cursor-2", True))
        httpx_mock.add_response(json=paginated_envelope([{"id": "2"}], None, False))

        page1 = client.notifications.list()
        assert len(page1["data"]) == 1
        assert page1["meta"]["has_more"] is True
        assert page1["meta"]["cursor"] == "cursor-2"

        page2 = client.notifications.list({"cursor": page1["meta"]["cursor"]})
        assert len(page2["data"]) == 1
        assert page2["meta"]["has_more"] is False

    def test_auto_pagination_across_pages(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=paginated_envelope([{"id": "1"}, {"id": "2"}], "page2", True))
        httpx_mock.add_response(json=paginated_envelope([{"id": "3"}], None, False))

        items = list(client.notifications.list_auto())
        assert len(items) == 3
        assert [i["id"] for i in items] == ["1", "2", "3"]
        assert len(httpx_mock.get_requests()) == 2

    def test_auto_pagination_stops_when_no_more(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=paginated_envelope([{"id": "1"}], None, False))
        items = list(client.notifications.list_auto())
        assert len(items) == 1
        assert len(httpx_mock.get_requests()) == 1

    def test_auto_pagination_empty(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=paginated_envelope([], None, False))
        items = list(client.notifications.list_auto())
        assert len(items) == 0

    def test_auto_pagination_passes_filter_params(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=paginated_envelope([], None, False))
        list(client.notifications.list_auto({"channel": "email", "limit": 10}))
        request = httpx_mock.get_request()
        assert request is not None
        assert request.url.params["channel"] == "email"
        assert request.url.params["limit"] == "10"


# ── Context Manager ──────────────────────────────────


class TestContextManager:
    def test_sync_context_manager(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=paginated_envelope([]))
        with Notifica(TEST_API_KEY, base_url=BASE_URL, max_retries=0) as client:
            client.notifications.list()
