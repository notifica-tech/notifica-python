"""Recurso de API keys do SDK Notifica."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..client import NotificaClient


class ApiKeys:
    """Recurso de API keys."""

    def __init__(self, client: NotificaClient) -> None:
        self._client = client

    def create(self, params: dict[str, Any], options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Cria uma nova API key. ⚠️ raw_key só retorna na criação!"""
        return self._client.post("/api-keys", json=params, options=options)["data"]  # type: ignore[no-any-return]

    def list(self, options: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Lista API keys (sem raw_key)."""
        return self._client.get("/api-keys", options=options)["data"]  # type: ignore[no-any-return]

    def revoke(self, id: str, options: dict[str, Any] | None = None) -> None:
        """Revoga (deleta) uma API key."""
        self._client.delete(f"/api-keys/{id}", options=options)
