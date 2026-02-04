"""Recurso de workflows do SDK Notifica."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterator

if TYPE_CHECKING:
    from ..client import NotificaClient


class Workflows:
    """Recurso de workflows."""

    def __init__(self, client: NotificaClient) -> None:
        self._client = client

    def create(
        self,
        params: dict[str, Any],
        options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Cria um novo workflow.

        Example:
            ```python
            workflow = client.workflows.create({
                "slug": "welcome-flow",
                "name": "Fluxo de Boas-Vindas",
                "steps": [
                    {"type": "send", "channel": "email", "template": "welcome-email"},
                    {"type": "delay", "duration": "1h"},
                    {"type": "send", "channel": "whatsapp", "template": "welcome-whatsapp"},
                ],
            })
            ```
        """
        return self._client.post("/workflows", json=params, options=options)["data"]  # type: ignore[no-any-return]

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Lista workflows com paginação."""
        return self._client.list("/workflows", params=params, options=options)  # type: ignore[no-any-return]

    def list_auto(
        self,
        params: dict[str, Any] | None = None,
    ) -> Iterator[dict[str, Any]]:
        """Itera automaticamente por todos os workflows."""
        return self._client.list_auto("/workflows", params=params)

    def get(self, id: str, options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Obtém detalhes de um workflow."""
        return self._client.get_one(f"/workflows/{id}", options=options)  # type: ignore[no-any-return]

    def update(
        self,
        id: str,
        params: dict[str, Any],
        options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Atualiza um workflow (cria nova versão)."""
        return self._client.put(f"/workflows/{id}", json=params, options=options)["data"]  # type: ignore[no-any-return]

    def delete(self, id: str, options: dict[str, Any] | None = None) -> None:
        """Deleta um workflow (soft delete)."""
        self._client.delete(f"/workflows/{id}", options=options)

    def trigger(
        self,
        slug: str,
        params: dict[str, Any],
        options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Dispara a execução de um workflow.

        Example:
            ```python
            run = client.workflows.trigger("welcome-flow", {
                "recipient": "+5511999999999",
                "data": {"name": "João", "plan": "pro"},
            })
            ```
        """
        return self._client.post(f"/workflows/{slug}/trigger", json=params, options=options)["data"]  # type: ignore[no-any-return]

    # ── Workflow Runs ───────────────────────────────────

    def list_runs(
        self,
        params: dict[str, Any] | None = None,
        options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Lista execuções de workflows."""
        return self._client.list("/workflow-runs", params=params, options=options)  # type: ignore[no-any-return]

    def get_run(self, id: str, options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Obtém detalhes de uma execução (incluindo step_results)."""
        return self._client.get_one(f"/workflow-runs/{id}", options=options)  # type: ignore[no-any-return]

    def cancel_run(self, id: str, options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Cancela uma execução em andamento."""
        return self._client.post(f"/workflow-runs/{id}/cancel", options=options)["data"]  # type: ignore[no-any-return]
