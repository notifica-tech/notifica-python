"""Recurso de domínios do SDK Notifica."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterator

if TYPE_CHECKING:
    from ..client import NotificaClient


class Domains:
    """Recurso de domínios."""

    def __init__(self, client: NotificaClient) -> None:
        self._client = client

    def create(self, params: dict[str, Any], options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Registra um novo domínio de envio."""
        return self._client.post("/domains", json=params, options=options)["data"]  # type: ignore[no-any-return]

    def list(self, params: dict[str, Any] | None = None, options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Lista domínios registrados."""
        return self._client.list("/domains", params=params, options=options)  # type: ignore[no-any-return]

    def list_auto(self, params: dict[str, Any] | None = None) -> Iterator[dict[str, Any]]:
        """Itera automaticamente por todos os domínios."""
        return self._client.list_auto("/domains", params=params)

    def get(self, id: str, options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Obtém detalhes de um domínio."""
        return self._client.get_one(f"/domains/{id}", options=options)  # type: ignore[no-any-return]

    def delete(self, id: str, options: dict[str, Any] | None = None) -> None:
        """Remove um domínio."""
        self._client.delete(f"/domains/{id}", options=options)

    def get_health(self, domain_id: str, options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Obtém status de saúde do domínio."""
        return self._client.get_one(f"/domains/{domain_id}/health", options=options)  # type: ignore[no-any-return]
