"""Testes do recurso de billing."""

from __future__ import annotations

from pytest_httpx import HTTPXMock

from notifica import Notifica

from conftest import paginated_envelope, single_envelope


class TestBillingPlans:
    def test_list(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json={"data": [{"name": "startup"}, {"name": "pro"}]})
        result = client.billing.plans.list()
        assert len(result) == 2

    def test_get(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"name": "startup", "monthly_price_cents": 9900}))
        result = client.billing.plans.get("startup")
        assert result["monthly_price_cents"] == 9900


class TestBillingSettings:
    def test_get(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"currency": "BRL", "gateway": "asaas"}))
        result = client.billing.settings.get()
        assert result["currency"] == "BRL"


class TestBillingSubscription:
    def test_get(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "sub1", "status": "active"}))
        result = client.billing.subscription.get()
        assert result["status"] == "active"

    def test_subscribe(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "sub1", "plan_name": "startup"}))
        result = client.billing.subscription.subscribe({"plan_name": "startup"})
        assert result["plan_name"] == "startup"

    def test_change_plan(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "sub1", "plan_name": "pro"}))
        result = client.billing.subscription.change_plan({"plan_name": "pro"})
        assert result["plan_name"] == "pro"

    def test_cancel(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "sub1", "status": "canceled"}))
        result = client.billing.subscription.cancel({"at_period_end": True})
        assert result["status"] == "canceled"

    def test_calculate_proration(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"proration_amount_cents": 1500}))
        result = client.billing.subscription.calculate_proration({"plan_name": "pro"})
        assert result["proration_amount_cents"] == 1500

    def test_reactivate(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "sub1", "status": "active"}))
        result = client.billing.subscription.reactivate()
        assert result["status"] == "active"


class TestBillingUsage:
    def test_get(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"current": {"notifications": 500}}))
        result = client.billing.usage.get()
        assert result["current"]["notifications"] == 500


class TestBillingInvoices:
    def test_list(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=paginated_envelope([{"id": "inv1"}]))
        result = client.billing.invoices.list()
        assert len(result["data"]) == 1

    def test_get(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "inv1", "amount_cents": 9900}))
        result = client.billing.invoices.get("inv1")
        assert result["amount_cents"] == 9900


class TestBillingPaymentMethods:
    def test_list(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json={"data": [{"id": "pm1"}]})
        result = client.billing.payment_methods.list()
        assert len(result) == 1

    def test_create(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "pm1", "type": "credit_card"}))
        result = client.billing.payment_methods.create({"type": "credit_card", "card_token": "tok"})
        assert result["type"] == "credit_card"

    def test_get(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "pm1"}))
        assert client.billing.payment_methods.get("pm1")["id"] == "pm1"

    def test_update(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "pm1", "nickname": "Personal"}))
        result = client.billing.payment_methods.update("pm1", {"nickname": "Personal"})
        assert result["nickname"] == "Personal"

    def test_delete(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(status_code=204)
        client.billing.payment_methods.delete("pm1")

    def test_set_default(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "pm1", "is_default": True}))
        result = client.billing.payment_methods.set_default("pm1")
        assert result["is_default"] is True
