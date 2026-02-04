"""Testes do recurso de notificações."""

from __future__ import annotations

from pytest_httpx import HTTPXMock

from notifica import Notifica

from conftest import paginated_envelope, single_envelope


class TestNotifications:
    def test_send(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "n1", "status": "pending"}))
        result = client.notifications.send({"channel": "whatsapp", "to": "+5511999999999"})
        assert result["id"] == "n1"

    def test_list(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=paginated_envelope([{"id": "n1"}]))
        result = client.notifications.list({"limit": 10})
        assert len(result["data"]) == 1

    def test_get(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "n1", "channel": "email"}))
        result = client.notifications.get("n1")
        assert result["id"] == "n1"

    def test_list_attempts(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json={"data": [{"id": "a1", "attempt_number": 1}]})
        result = client.notifications.list_attempts("n1")
        assert len(result) == 1
        assert result[0]["attempt_number"] == 1

    def test_list_auto(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=paginated_envelope([{"id": "n1"}], "c2", True))
        httpx_mock.add_response(json=paginated_envelope([{"id": "n2"}], None, False))
        items = list(client.notifications.list_auto())
        assert [i["id"] for i in items] == ["n1", "n2"]
