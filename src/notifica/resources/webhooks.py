"""Recurso de webhooks do SDK Notifica."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterator

if TYPE_CHECKING:
    from ..client import NotificaClient


class Webhooks:
    """Recurso de webhooks."""

    def __init__(self, client: NotificaClient) -> None:
        self._client = client

    def create(self, params: dict[str, Any], options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Cria um novo webhook. ⚠️ signing_secret só retorna na criação!"""
        return self._client.post("/webhooks", json=params, options=options)["data"]  # type: ignore[no-any-return]

    def list(self, params: dict[str, Any] | None = None, options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Lista webhooks com paginação."""
        return self._client.list("/webhooks", params=params, options=options)  # type: ignore[no-any-return]

    def list_auto(self, params: dict[str, Any] | None = None) -> Iterator[dict[str, Any]]:
        """Itera automaticamente por todos os webhooks."""
        return self._client.list_auto("/webhooks", params=params)

    def get(self, id: str, options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Obtém detalhes de um webhook."""
        return self._client.get_one(f"/webhooks/{id}", options=options)  # type: ignore[no-any-return]

    def update(self, id: str, params: dict[str, Any], options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Atualiza um webhook."""
        return self._client.put(f"/webhooks/{id}", json=params, options=options)["data"]  # type: ignore[no-any-return]

    def delete(self, id: str, options: dict[str, Any] | None = None) -> None:
        """Deleta um webhook."""
        self._client.delete(f"/webhooks/{id}", options=options)

    def test(self, id: str, options: dict[str, Any] | None = None) -> None:
        """Envia um evento de teste para o webhook."""
        self._client.post(f"/webhooks/{id}/test", options=options)

    def list_deliveries(
        self, id: str, params: dict[str, Any] | None = None, options: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """Lista entregas recentes de um webhook."""
        return self._client.get(f"/webhooks/{id}/deliveries", params=params, options=options)["data"]  # type: ignore[no-any-return]
