"""Testes do recurso de workflows."""

from __future__ import annotations

from pytest_httpx import HTTPXMock

from notifica import Notifica

from conftest import paginated_envelope, single_envelope


class TestWorkflows:
    def test_create(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "w1", "slug": "welcome"}))
        result = client.workflows.create({
            "slug": "welcome",
            "name": "Welcome Flow",
            "steps": [{"type": "send", "channel": "email", "template": "welcome"}],
        })
        assert result["slug"] == "welcome"

    def test_list(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=paginated_envelope([{"id": "w1"}]))
        result = client.workflows.list()
        assert len(result["data"]) == 1

    def test_get(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "w1"}))
        assert client.workflows.get("w1")["id"] == "w1"

    def test_update(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "w1", "name": "Updated"}))
        result = client.workflows.update("w1", {"name": "Updated"})
        assert result["name"] == "Updated"

    def test_delete(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(status_code=204)
        client.workflows.delete("w1")

    def test_trigger(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "run1", "status": "pending"}))
        result = client.workflows.trigger("welcome", {"recipient": "+5511999999999"})
        assert result["status"] == "pending"

    def test_list_runs(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=paginated_envelope([{"id": "run1"}]))
        result = client.workflows.list_runs()
        assert len(result["data"]) == 1

    def test_get_run(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "run1", "status": "completed"}))
        assert client.workflows.get_run("run1")["status"] == "completed"

    def test_cancel_run(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "run1", "status": "cancelled"}))
        result = client.workflows.cancel_run("run1")
        assert result["status"] == "cancelled"
