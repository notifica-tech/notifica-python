"""Recurso de analytics do SDK Notifica."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..client import NotificaClient


class Analytics:
    """Recurso de analytics."""

    def __init__(self, client: NotificaClient) -> None:
        self._client = client

    def overview(self, params: dict[str, Any] | None = None, options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Métricas gerais (total enviado, entregue, falhas, taxa de entrega)."""
        return self._client.get("/analytics/overview", params=params, options=options)["data"]  # type: ignore[no-any-return]

    def by_channel(self, params: dict[str, Any] | None = None, options: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Métricas por canal."""
        return self._client.get("/analytics/channels", params=params, options=options)["data"]  # type: ignore[no-any-return]

    def timeseries(self, params: dict[str, Any] | None = None, options: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Série temporal de envios."""
        return self._client.get("/analytics/timeseries", params=params, options=options)["data"]  # type: ignore[no-any-return]

    def top_templates(self, params: dict[str, Any] | None = None, options: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Templates mais utilizados."""
        return self._client.get("/analytics/templates", params=params, options=options)["data"]  # type: ignore[no-any-return]
