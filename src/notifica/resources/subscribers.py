"""Recurso de subscribers do SDK Notifica."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterator

if TYPE_CHECKING:
    from ..client import NotificaClient


class Subscribers:
    """Recurso de subscribers."""

    def __init__(self, client: NotificaClient) -> None:
        self._client = client

    def create(self, params: dict[str, Any], options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Cria ou atualiza um subscriber (upsert por external_id).

        LGPD: registra consentimento automaticamente.
        """
        return self._client.post("/subscribers", json=params, options=options)["data"]  # type: ignore[no-any-return]

    def list(self, params: dict[str, Any] | None = None, options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Lista subscribers com paginação."""
        return self._client.list("/subscribers", params=params, options=options)  # type: ignore[no-any-return]

    def list_auto(self, params: dict[str, Any] | None = None) -> Iterator[dict[str, Any]]:
        """Itera automaticamente por todos os subscribers."""
        return self._client.list_auto("/subscribers", params=params)

    def get(self, id: str, options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Obtém detalhes de um subscriber."""
        return self._client.get_one(f"/subscribers/{id}", options=options)  # type: ignore[no-any-return]

    def update(self, id: str, params: dict[str, Any], options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Atualiza um subscriber."""
        return self._client.put(f"/subscribers/{id}", json=params, options=options)["data"]  # type: ignore[no-any-return]

    def delete(self, id: str, options: dict[str, Any] | None = None) -> None:
        """Deleta um subscriber (soft delete com nullificação de PII — LGPD).

        ⚠️ Irreversível: email, telefone e nome são removidos.
        """
        self._client.delete(f"/subscribers/{id}", options=options)

    # ── Preferences ─────────────────────────────────────

    def get_preferences(self, id: str, options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Obtém preferências de notificação do subscriber."""
        return self._client.get_one(f"/subscribers/{id}/preferences", options=options)  # type: ignore[no-any-return]

    def update_preferences(self, id: str, params: dict[str, Any], options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Atualiza preferências de notificação do subscriber."""
        return self._client.put(f"/subscribers/{id}/preferences", json=params, options=options)["data"]  # type: ignore[no-any-return]

    # ── Bulk import ─────────────────────────────────────

    def bulk_import(self, params: dict[str, Any], options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Importa subscribers em lote (upsert transacional)."""
        return self._client.post("/subscribers/import", json=params, options=options)["data"]  # type: ignore[no-any-return]

    # ── In-App Notifications ────────────────────────────

    def list_notifications(
        self,
        subscriber_id: str,
        params: dict[str, Any] | None = None,
        options: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Lista notificações in-app de um subscriber."""
        response = self._client.get(
            f"/subscribers/{subscriber_id}/notifications",
            params=params,
            options=options,
        )
        return response["data"]  # type: ignore[no-any-return]

    def mark_read(
        self,
        subscriber_id: str,
        notification_id: str,
        options: dict[str, Any] | None = None,
    ) -> None:
        """Marca uma notificação in-app como lida."""
        self._client.post(
            f"/subscribers/{subscriber_id}/notifications/{notification_id}/read",
            options=options,
        )

    def mark_all_read(self, subscriber_id: str, options: dict[str, Any] | None = None) -> None:
        """Marca todas as notificações in-app como lidas."""
        self._client.post(
            f"/subscribers/{subscriber_id}/notifications/read-all",
            options=options,
        )

    def get_unread_count(self, subscriber_id: str, options: dict[str, Any] | None = None) -> int:
        """Obtém contagem de notificações não lidas."""
        response = self._client.get(
            f"/subscribers/{subscriber_id}/notifications/unread-count",
            options=options,
        )
        return response["data"]["count"]  # type: ignore[no-any-return]
