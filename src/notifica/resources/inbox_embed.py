"""Recurso de inbox embed do SDK Notifica."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..client import NotificaClient


class InboxEmbed:
    """Recurso de inbox embed."""

    def __init__(self, client: NotificaClient) -> None:
        self._client = client

    def get_settings(self, options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Obtém as configurações do inbox embed."""
        return self._client.get_one("/inbox-embed/settings", options=options)  # type: ignore[no-any-return]

    def update_settings(self, params: dict[str, Any], options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Atualiza as configurações do inbox embed."""
        return self._client.put("/inbox-embed/settings", json=params, options=options)["data"]  # type: ignore[no-any-return]

    def rotate_key(self, options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Rotaciona a chave de embed. A chave antiga continua por um grace period."""
        return self._client.post("/inbox-embed/keys/rotate", options=options)["data"]  # type: ignore[no-any-return]
