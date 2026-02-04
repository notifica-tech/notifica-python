"""Testes do recurso de templates."""

from __future__ import annotations

from pytest_httpx import HTTPXMock

from notifica import Notifica

from conftest import paginated_envelope, single_envelope


class TestTemplates:
    def test_create(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "t1", "slug": "welcome"}))
        result = client.templates.create({
            "channel": "email",
            "slug": "welcome",
            "name": "Welcome",
            "content": "Hello {{name}}",
        })
        assert result["slug"] == "welcome"

    def test_list(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=paginated_envelope([{"id": "t1"}]))
        result = client.templates.list()
        assert len(result["data"]) == 1

    def test_get(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "t1"}))
        result = client.templates.get("t1")
        assert result["id"] == "t1"

    def test_update(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "t1", "name": "Updated"}))
        result = client.templates.update("t1", {"name": "Updated"})
        assert result["name"] == "Updated"

    def test_delete(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(status_code=204)
        client.templates.delete("t1")

    def test_preview(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"rendered": {"body": "Hello João"}}))
        result = client.templates.preview("t1", {"variables": {"name": "João"}})
        assert result["rendered"]["body"] == "Hello João"

    def test_validate(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"valid": True, "errors": []}))
        result = client.templates.validate("t1")
        assert result["valid"] is True

    def test_preview_content(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"rendered": {"body": "Hi"}}))
        result = client.templates.preview_content({"content": "Hi", "channel": "email"})
        assert "rendered" in result

    def test_validate_content(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"valid": True, "errors": [], "warnings": []}))
        result = client.templates.validate_content({"content": "Hi", "channel": "email"})
        assert result["valid"] is True
