"""Recurso de billing do SDK Notifica."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterator

if TYPE_CHECKING:
    from ..client import NotificaClient


# ═══════════════════════════════════════════════════
# Plans
# ═══════════════════════════════════════════════════


class BillingPlans:
    """Sub-recurso de planos."""

    def __init__(self, client: NotificaClient) -> None:
        self._client = client

    def list(self, options: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Lista todos os planos disponíveis."""
        return self._client.get("/billing/plans", options=options)["data"]  # type: ignore[no-any-return]

    def get(self, name: str, options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Obtém detalhes de um plano específico."""
        return self._client.get_one(f"/billing/plans/{name}", options=options)  # type: ignore[no-any-return]


# ═══════════════════════════════════════════════════
# Settings
# ═══════════════════════════════════════════════════


class BillingSettingsResource:
    """Sub-recurso de configurações de billing."""

    def __init__(self, client: NotificaClient) -> None:
        self._client = client

    def get(self, options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Obtém as configurações de faturamento do tenant."""
        return self._client.get_one("/billing/settings", options=options)  # type: ignore[no-any-return]


# ═══════════════════════════════════════════════════
# Subscription
# ═══════════════════════════════════════════════════


class BillingSubscription:
    """Sub-recurso de assinatura."""

    def __init__(self, client: NotificaClient) -> None:
        self._client = client

    def get(self, options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Obtém a assinatura atual."""
        return self._client.get_one("/billing/subscription", options=options)  # type: ignore[no-any-return]

    def subscribe(self, params: dict[str, Any], options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Cria uma nova assinatura (idempotent)."""
        return self._client.post("/billing/subscribe", json=params, options=options)["data"]  # type: ignore[no-any-return]

    def change_plan(self, params: dict[str, Any], options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Altera o plano da assinatura (idempotent)."""
        return self._client.post("/billing/change-plan", json=params, options=options)["data"]  # type: ignore[no-any-return]

    def cancel(self, params: dict[str, Any] | None = None, options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Cancela a assinatura (idempotent)."""
        return self._client.post("/billing/cancel", json=params, options=options)["data"]  # type: ignore[no-any-return]

    def calculate_proration(self, params: dict[str, Any], options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Calcula o valor de proration para mudança de plano."""
        return self._client.post("/billing/calculate-proration", json=params, options=options)["data"]  # type: ignore[no-any-return]

    def reactivate(self, params: dict[str, Any] | None = None, options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Reativa uma assinatura cancelada (idempotent)."""
        return self._client.post("/billing/reactivate", json=params, options=options)["data"]  # type: ignore[no-any-return]


# ═══════════════════════════════════════════════════
# Usage
# ═══════════════════════════════════════════════════


class BillingUsageResource:
    """Sub-recurso de uso."""

    def __init__(self, client: NotificaClient) -> None:
        self._client = client

    def get(self, options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Obtém o uso atual e quotas do tenant."""
        return self._client.get_one("/billing/usage", options=options)  # type: ignore[no-any-return]


# ═══════════════════════════════════════════════════
# Invoices
# ═══════════════════════════════════════════════════


class BillingInvoices:
    """Sub-recurso de faturas."""

    def __init__(self, client: NotificaClient) -> None:
        self._client = client

    def list(self, params: dict[str, Any] | None = None, options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Lista faturas com paginação."""
        return self._client.list("/billing/invoices", params=params, options=options)  # type: ignore[no-any-return]

    def list_auto(self, params: dict[str, Any] | None = None) -> Iterator[dict[str, Any]]:
        """Itera automaticamente por todas as faturas."""
        return self._client.list_auto("/billing/invoices", params=params)

    def get(self, id: str, options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Obtém detalhes de uma fatura."""
        return self._client.get_one(f"/billing/invoices/{id}", options=options)  # type: ignore[no-any-return]


# ═══════════════════════════════════════════════════
# Payment Methods
# ═══════════════════════════════════════════════════


class BillingPaymentMethods:
    """Sub-recurso de métodos de pagamento."""

    def __init__(self, client: NotificaClient) -> None:
        self._client = client

    def list(self, options: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Lista métodos de pagamento."""
        return self._client.get("/billing/payment-methods", options=options)["data"]  # type: ignore[no-any-return]

    def create(self, params: dict[str, Any], options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Cria um novo método de pagamento (idempotent)."""
        return self._client.post("/billing/payment-methods", json=params, options=options)["data"]  # type: ignore[no-any-return]

    def get(self, id: str, options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Obtém detalhes de um método de pagamento."""
        return self._client.get_one(f"/billing/payment-methods/{id}", options=options)  # type: ignore[no-any-return]

    def update(self, id: str, params: dict[str, Any], options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Atualiza um método de pagamento."""
        return self._client.put(f"/billing/payment-methods/{id}", json=params, options=options)["data"]  # type: ignore[no-any-return]

    def delete(self, id: str, options: dict[str, Any] | None = None) -> None:
        """Remove um método de pagamento."""
        self._client.delete(f"/billing/payment-methods/{id}", options=options)

    def set_default(self, id: str, options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Define um método de pagamento como padrão."""
        return self._client.post(f"/billing/payment-methods/{id}/set-default", options=options)["data"]  # type: ignore[no-any-return]


# ═══════════════════════════════════════════════════
# Main Billing Resource
# ═══════════════════════════════════════════════════


class Billing:
    """Recurso de billing com sub-recursos plans, settings, subscription, usage, invoices, payment_methods."""

    def __init__(self, client: NotificaClient) -> None:
        self.plans = BillingPlans(client)
        self.settings = BillingSettingsResource(client)
        self.subscription = BillingSubscription(client)
        self.usage = BillingUsageResource(client)
        self.invoices = BillingInvoices(client)
        self.payment_methods = BillingPaymentMethods(client)
