"""Recurso de inbox público do SDK Notifica.

Usa publishable key (pk_*). Ideal para integração direta no frontend.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..client import NotificaClient


class Inbox:
    """Recurso de inbox público."""

    def __init__(self, client: NotificaClient) -> None:
        self._client = client

    def list_notifications(
        self,
        subscriber_id: str,
        params: dict[str, Any] | None = None,
        options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Lista notificações do inbox."""
        query = {**(params or {}), "subscriber_id": subscriber_id}
        return self._client.list("/inbox/notifications", params=query, options=options)  # type: ignore[no-any-return]

    def get_unread_count(self, subscriber_id: str, options: dict[str, Any] | None = None) -> int:
        """Obtém a contagem de notificações não lidas."""
        response = self._client.get(
            "/inbox/notifications/unread-count",
            params={"subscriber_id": subscriber_id},
            options=options,
        )
        return response["data"]["count"]  # type: ignore[no-any-return]

    def mark_read(self, notification_id: str, options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Marca uma notificação como lida."""
        return self._client.post(f"/inbox/notifications/{notification_id}/read", options=options)["data"]  # type: ignore[no-any-return]

    def mark_all_read(self, subscriber_id: str, options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Marca todas as notificações como lidas."""
        return self._client.post(
            "/inbox/notifications/read-all",
            json={"subscriber_id": subscriber_id},
            options=options,
        )["data"]  # type: ignore[no-any-return]
