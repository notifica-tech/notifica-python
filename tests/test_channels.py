"""Testes do recurso de canais."""

from __future__ import annotations

from pytest_httpx import HTTPXMock

from notifica import Notifica

from conftest import single_envelope


class TestChannels:
    def test_create(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "ch1", "channel": "email"}))
        result = client.channels.create({"channel": "email", "provider": "aws_ses", "credentials": {}})
        assert result["channel"] == "email"

    def test_list(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json={"data": [{"id": "ch1"}]})
        result = client.channels.list()
        assert len(result) == 1

    def test_get(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "ch1", "channel": "email"}))
        assert client.channels.get("email")["channel"] == "email"

    def test_update(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "ch1"}))
        client.channels.update("email", {"provider": "resend"})

    def test_delete(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(status_code=204)
        client.channels.delete("email")
