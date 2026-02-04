"""Recurso de SMS do SDK Notifica (BYOP — Bring Your Own Provider)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterator

if TYPE_CHECKING:
    from ..client import NotificaClient


# ═══════════════════════════════════════════════════
# Providers
# ═══════════════════════════════════════════════════


class SmsProviders:
    """Sub-recurso de provedores SMS."""

    def __init__(self, client: NotificaClient) -> None:
        self._client = client

    def list(self, options: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Lista todos os provedores SMS configurados."""
        return self._client.get("/channels/sms/providers", options=options)["data"]  # type: ignore[no-any-return]

    def create(self, params: dict[str, Any], options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Cria um novo provedor SMS (idempotent)."""
        return self._client.post("/channels/sms/providers", json=params, options=options)["data"]  # type: ignore[no-any-return]

    def get(self, id: str, options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Obtém detalhes de um provedor SMS."""
        return self._client.get_one(f"/channels/sms/providers/{id}", options=options)  # type: ignore[no-any-return]

    def update(self, id: str, params: dict[str, Any], options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Atualiza um provedor SMS (PATCH parcial)."""
        return self._client.patch(f"/channels/sms/providers/{id}", json=params, options=options)["data"]  # type: ignore[no-any-return]

    def activate(self, id: str, options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Ativa um provedor SMS."""
        return self._client.post(f"/channels/sms/providers/{id}/activate", options=options)["data"]  # type: ignore[no-any-return]

    def delete(self, id: str, options: dict[str, Any] | None = None) -> None:
        """Remove um provedor SMS."""
        self._client.delete(f"/channels/sms/providers/{id}", options=options)

    def validate(self, params: dict[str, Any], options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Valida a configuração de um provedor SMS."""
        return self._client.post("/channels/sms/providers/validate", json=params, options=options)["data"]  # type: ignore[no-any-return]

    def test(self, params: dict[str, Any], options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Envia um SMS de teste."""
        return self._client.post("/channels/sms/providers/test", json=params, options=options)["data"]  # type: ignore[no-any-return]


# ═══════════════════════════════════════════════════
# Compliance
# ═══════════════════════════════════════════════════


class SmsCompliance:
    """Sub-recurso de compliance SMS."""

    def __init__(self, client: NotificaClient) -> None:
        self._client = client

    def show(self, options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Obtém as configurações de compliance SMS."""
        return self._client.get_one("/channels/sms/compliance", options=options)  # type: ignore[no-any-return]

    def update(self, params: dict[str, Any], options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Atualiza as configurações de compliance SMS (PATCH parcial)."""
        return self._client.patch("/channels/sms/compliance", json=params, options=options)["data"]  # type: ignore[no-any-return]

    def analytics(self, options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Obtém estatísticas de compliance."""
        return self._client.get_one("/channels/sms/compliance/analytics", options=options)  # type: ignore[no-any-return]

    def logs(
        self, params: dict[str, Any] | None = None, options: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Lista logs de compliance com paginação."""
        return self._client.list("/channels/sms/compliance/logs", params=params, options=options)  # type: ignore[no-any-return]


# ═══════════════════════════════════════════════════
# Consents
# ═══════════════════════════════════════════════════


class SmsConsents:
    """Sub-recurso de consentimentos SMS."""

    def __init__(self, client: NotificaClient) -> None:
        self._client = client

    def list(self, params: dict[str, Any] | None = None, options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Lista consentimentos SMS com paginação."""
        return self._client.list("/channels/sms/consents", params=params, options=options)  # type: ignore[no-any-return]

    def list_auto(self, params: dict[str, Any] | None = None) -> Iterator[dict[str, Any]]:
        """Itera automaticamente por todos os consentimentos."""
        return self._client.list_auto("/channels/sms/consents", params=params)

    def summary(self, options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Obtém resumo estatístico dos consentimentos."""
        return self._client.get_one("/channels/sms/consents/summary", options=options)  # type: ignore[no-any-return]

    def get(self, phone: str, options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Obtém o consentimento de um número específico."""
        return self._client.get_one(f"/channels/sms/consents/{phone}", options=options)  # type: ignore[no-any-return]

    def revoke(self, phone: str, options: dict[str, Any] | None = None) -> None:
        """Revoga o consentimento de um número (DELETE)."""
        self._client.delete(f"/channels/sms/consents/{phone}", options=options)

    def create(self, params: dict[str, Any], options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Cria ou atualiza um consentimento SMS (idempotent)."""
        return self._client.post("/channels/sms/consents", json=params, options=options)["data"]  # type: ignore[no-any-return]

    def import_bulk(self, params: dict[str, Any], options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Importa consentimentos em lote."""
        return self._client.post("/channels/sms/consents/import", json=params, options=options)["data"]  # type: ignore[no-any-return]


# ═══════════════════════════════════════════════════
# Main SMS Resource
# ═══════════════════════════════════════════════════


class Sms:
    """Recurso de SMS com sub-recursos providers, compliance e consents."""

    def __init__(self, client: NotificaClient) -> None:
        self.providers = SmsProviders(client)
        self.compliance = SmsCompliance(client)
        self.consents = SmsConsents(client)
