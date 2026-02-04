"""Recurso de notificações do SDK Notifica."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterator

if TYPE_CHECKING:
    from ..client import NotificaClient


class Notifications:
    """Recurso de notificações."""

    def __init__(self, client: NotificaClient) -> None:
        self._client = client

    def send(
        self,
        params: dict[str, Any],
        options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Envia uma notificação.

        A notificação é enfileirada para entrega assíncrona.

        Example:
            ```python
            notification = client.notifications.send({
                "channel": "whatsapp",
                "to": "+5511999999999",
                "template": "welcome",
                "data": {"name": "João"},
            })
            ```
        """
        response = self._client.post("/notifications", json=params, options=options)
        return response["data"]  # type: ignore[no-any-return]

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Lista notificações com paginação manual.

        Retorna ``{data: [...], meta: {cursor, has_more}}``.
        """
        return self._client.list("/notifications", params=params, options=options)  # type: ignore[no-any-return]

    def list_auto(
        self,
        params: dict[str, Any] | None = None,
    ) -> Iterator[dict[str, Any]]:
        """Itera automaticamente por todas as notificações.

        Example:
            ```python
            for notification in client.notifications.list_auto({"channel": "email"}):
                print(notification["id"])
            ```
        """
        return self._client.list_auto("/notifications", params=params)

    def get(
        self,
        id: str,
        options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Obtém detalhes de uma notificação."""
        return self._client.get_one(f"/notifications/{id}", options=options)  # type: ignore[no-any-return]

    def list_attempts(
        self,
        notification_id: str,
        options: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Lista tentativas de entrega de uma notificação."""
        response = self._client.get(
            f"/notifications/{notification_id}/attempts", options=options
        )
        return response["data"]  # type: ignore[no-any-return]
