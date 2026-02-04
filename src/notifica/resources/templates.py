"""Recurso de templates do SDK Notifica."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterator

if TYPE_CHECKING:
    from ..client import NotificaClient


class Templates:
    """Recurso de templates."""

    def __init__(self, client: NotificaClient) -> None:
        self._client = client

    def create(
        self,
        params: dict[str, Any],
        options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Cria um novo template.

        Example:
            ```python
            template = client.templates.create({
                "channel": "email",
                "slug": "welcome-email",
                "name": "Email de Boas-Vindas",
                "content": "Olá {{name}}, bem-vindo!",
            })
            ```
        """
        return self._client.post("/templates", json=params, options=options)["data"]  # type: ignore[no-any-return]

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Lista templates com paginação."""
        return self._client.list("/templates", params=params, options=options)  # type: ignore[no-any-return]

    def list_auto(
        self,
        params: dict[str, Any] | None = None,
    ) -> Iterator[dict[str, Any]]:
        """Itera automaticamente por todos os templates."""
        return self._client.list_auto("/templates", params=params)

    def get(
        self,
        id: str,
        options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Obtém detalhes de um template."""
        return self._client.get_one(f"/templates/{id}", options=options)  # type: ignore[no-any-return]

    def update(
        self,
        id: str,
        params: dict[str, Any],
        options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Atualiza um template."""
        return self._client.put(f"/templates/{id}", json=params, options=options)["data"]  # type: ignore[no-any-return]

    def delete(
        self,
        id: str,
        options: dict[str, Any] | None = None,
    ) -> None:
        """Deleta um template."""
        self._client.delete(f"/templates/{id}", options=options)

    def preview(
        self,
        id: str,
        params: dict[str, Any],
        options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Preview de um template salvo com variáveis."""
        return self._client.post(f"/templates/{id}/preview", json=params, options=options)["data"]  # type: ignore[no-any-return]

    def preview_content(
        self,
        params: dict[str, Any],
        options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Preview de conteúdo arbitrário (útil para editor em tempo real)."""
        return self._client.post("/templates/preview", json=params, options=options)["data"]  # type: ignore[no-any-return]

    def validate(
        self,
        id: str,
        options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Valida um template salvo."""
        return self._client.post(f"/templates/{id}/validate", options=options)["data"]  # type: ignore[no-any-return]

    def validate_content(
        self,
        params: dict[str, Any],
        options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Valida conteúdo arbitrário."""
        return self._client.post("/templates/validate", json=params, options=options)["data"]  # type: ignore[no-any-return]
