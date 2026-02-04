"""Testes dos recursos de inbox embed e inbox público."""

from __future__ import annotations

from pytest_httpx import HTTPXMock

from notifica import Notifica

from conftest import paginated_envelope, single_envelope


class TestInboxEmbed:
    def test_get_settings(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"enabled": True, "theme": "auto"}))
        result = client.inbox_embed.get_settings()
        assert result["enabled"] is True

    def test_update_settings(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"enabled": False}))
        result = client.inbox_embed.update_settings({"enabled": False})
        assert result["enabled"] is False

    def test_rotate_key(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"embed_key": "pk_new_abc"}))
        result = client.inbox_embed.rotate_key()
        assert result["embed_key"] == "pk_new_abc"


class TestInbox:
    def test_list_notifications(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=paginated_envelope([{"id": "n1", "read": False}]))
        result = client.inbox.list_notifications("sub_123")
        assert len(result["data"]) == 1
        # Should pass subscriber_id as param
        request = httpx_mock.get_request()
        assert request is not None
        assert request.url.params["subscriber_id"] == "sub_123"

    def test_get_unread_count(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"count": 3}))
        result = client.inbox.get_unread_count("sub_123")
        assert result == 3

    def test_mark_read(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"success": True, "notification_id": "n1"}))
        result = client.inbox.mark_read("n1")
        assert result["success"] is True

    def test_mark_all_read(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"success": True, "marked_count": 5}))
        result = client.inbox.mark_all_read("sub_123")
        assert result["marked_count"] == 5
