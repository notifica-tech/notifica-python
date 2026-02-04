"""Testes do recurso de webhooks."""

from __future__ import annotations

from pytest_httpx import HTTPXMock

from notifica import Notifica

from conftest import paginated_envelope, single_envelope


class TestWebhooks:
    def test_create(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({
            "id": "wh1",
            "url": "https://test.com/hook",
            "signing_secret": "whsec_abc",
        }))
        result = client.webhooks.create({"url": "https://test.com/hook", "events": ["notification.delivered"]})
        assert result["signing_secret"] == "whsec_abc"

    def test_list(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=paginated_envelope([{"id": "wh1"}]))
        result = client.webhooks.list()
        assert len(result["data"]) == 1

    def test_get(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "wh1"}))
        assert client.webhooks.get("wh1")["id"] == "wh1"

    def test_update(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "wh1", "active": False}))
        result = client.webhooks.update("wh1", {"active": False})
        assert result["active"] is False

    def test_delete(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(status_code=204)
        client.webhooks.delete("wh1")

    def test_test(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(status_code=204)
        client.webhooks.test("wh1")

    def test_list_deliveries(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json={"data": [{"id": "del1", "status": "success"}]})
        result = client.webhooks.list_deliveries("wh1")
        assert len(result) == 1
