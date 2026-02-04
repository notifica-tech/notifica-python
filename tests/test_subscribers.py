"""Testes do recurso de subscribers."""

from __future__ import annotations

from pytest_httpx import HTTPXMock

from notifica import Notifica

from conftest import paginated_envelope, single_envelope


class TestSubscribers:
    def test_create(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "s1", "external_id": "user-123"}))
        result = client.subscribers.create({"external_id": "user-123", "email": "a@b.com"})
        assert result["external_id"] == "user-123"

    def test_list(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=paginated_envelope([{"id": "s1"}]))
        result = client.subscribers.list()
        assert len(result["data"]) == 1

    def test_get(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "s1"}))
        assert client.subscribers.get("s1")["id"] == "s1"

    def test_update(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "s1", "name": "João"}))
        result = client.subscribers.update("s1", {"name": "João"})
        assert result["name"] == "João"

    def test_delete(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(status_code=204)
        client.subscribers.delete("s1")

    def test_get_preferences(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"preferences": []}))
        result = client.subscribers.get_preferences("s1")
        assert "preferences" in result

    def test_update_preferences(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        prefs = [{"category": "marketing", "channel": "email", "enabled": False}]
        httpx_mock.add_response(json=single_envelope({"preferences": prefs}))
        result = client.subscribers.update_preferences("s1", {"preferences": prefs})
        assert len(result["preferences"]) == 1

    def test_bulk_import(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"imported": 2, "subscribers": []}))
        result = client.subscribers.bulk_import({
            "subscribers": [
                {"external_id": "u1", "email": "a@b.com"},
                {"external_id": "u2", "email": "c@d.com"},
            ]
        })
        assert result["imported"] == 2

    def test_list_notifications(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json={"data": [{"id": "n1", "read": False}]})
        result = client.subscribers.list_notifications("s1")
        assert len(result) == 1

    def test_mark_read(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(status_code=204)
        client.subscribers.mark_read("s1", "n1")

    def test_mark_all_read(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(status_code=204)
        client.subscribers.mark_all_read("s1")

    def test_get_unread_count(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"count": 5}))
        result = client.subscribers.get_unread_count("s1")
        assert result == 5
