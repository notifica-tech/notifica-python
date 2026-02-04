"""Recurso de canais do SDK Notifica."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..client import NotificaClient


class Channels:
    """Recurso de canais."""

    def __init__(self, client: NotificaClient) -> None:
        self._client = client

    def create(self, params: dict[str, Any], options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Configura um canal de notificação."""
        return self._client.post("/channels", json=params, options=options)["data"]  # type: ignore[no-any-return]

    def list(self, options: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Lista todas as configurações de canal."""
        return self._client.get("/channels", options=options)["data"]  # type: ignore[no-any-return]

    def get(self, channel: str, options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Obtém a configuração de um canal específico."""
        return self._client.get_one(f"/channels/{channel}", options=options)  # type: ignore[no-any-return]

    def update(self, channel: str, params: dict[str, Any], options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Atualiza a configuração de um canal."""
        return self._client.put(f"/channels/{channel}", json=params, options=options)["data"]  # type: ignore[no-any-return]

    def delete(self, channel: str, options: dict[str, Any] | None = None) -> None:
        """Remove a configuração de um canal."""
        self._client.delete(f"/channels/{channel}", options=options)
