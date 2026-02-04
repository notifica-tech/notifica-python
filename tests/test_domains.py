"""Testes do recurso de domínios."""

from __future__ import annotations

from pytest_httpx import HTTPXMock

from notifica import Notifica

from conftest import paginated_envelope, single_envelope


class TestDomains:
    def test_create(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "d1", "domain": "test.com.br"}))
        result = client.domains.create({"domain": "test.com.br"})
        assert result["domain"] == "test.com.br"

    def test_list(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=paginated_envelope([{"id": "d1"}]))
        result = client.domains.list()
        assert len(result["data"]) == 1

    def test_get(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "d1"}))
        assert client.domains.get("d1")["id"] == "d1"

    def test_delete(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(status_code=204)
        client.domains.delete("d1")

    def test_get_health(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"dns_valid": True}))
        result = client.domains.get_health("d1")
        assert result["dns_valid"] is True
