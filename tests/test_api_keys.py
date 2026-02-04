"""Testes do recurso de API keys."""

from __future__ import annotations

from pytest_httpx import HTTPXMock

from notifica import Notifica

from conftest import single_envelope


class TestApiKeys:
    def test_create(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({
            "id": "k1",
            "key_type": "secret",
            "raw_key": "nk_live_abc123",
        }))
        result = client.api_keys.create({
            "key_type": "secret",
            "label": "Backend",
            "environment": "production",
        })
        assert result["raw_key"] == "nk_live_abc123"

    def test_list(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json={"data": [{"id": "k1", "prefix": "nk_live_"}]})
        result = client.api_keys.list()
        assert len(result) == 1

    def test_revoke(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(status_code=204)
        client.api_keys.revoke("k1")
