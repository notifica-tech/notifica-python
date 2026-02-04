"""Testes do recurso de SMS."""

from __future__ import annotations

from pytest_httpx import HTTPXMock

from notifica import Notifica

from conftest import paginated_envelope, single_envelope


class TestSmsProviders:
    def test_list(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json={"data": [{"id": "p1", "type": "twilio"}]})
        result = client.sms.providers.list()
        assert len(result) == 1

    def test_create(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "p1", "type": "twilio"}))
        result = client.sms.providers.create({
            "type": "twilio",
            "name": "Meu Twilio",
            "config": {"account_sid": "AC...", "auth_token": "...", "phone_number": "+1"},
        })
        assert result["type"] == "twilio"

    def test_get(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "p1"}))
        assert client.sms.providers.get("p1")["id"] == "p1"

    def test_update(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "p1", "name": "Updated"}))
        result = client.sms.providers.update("p1", {"name": "Updated"})
        assert result["name"] == "Updated"
        # PATCH method
        request = httpx_mock.get_request()
        assert request is not None
        assert request.method == "PATCH"

    def test_activate(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"id": "p1", "active": True}))
        result = client.sms.providers.activate("p1")
        assert result["active"] is True

    def test_delete(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(status_code=204)
        client.sms.providers.delete("p1")

    def test_validate(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"valid": True}))
        result = client.sms.providers.validate({"type": "twilio", "config": {}})
        assert result["valid"] is True

    def test_test(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"success": True, "message": "Sent"}))
        result = client.sms.providers.test({"to": "+5511999999999"})
        assert result["success"] is True


class TestSmsCompliance:
    def test_show(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"respect_national_holidays": True}))
        result = client.sms.compliance.show()
        assert result["respect_national_holidays"] is True

    def test_update(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"allowed_hours_start": "08:00"}))
        result = client.sms.compliance.update({"allowed_hours_start": "08:00"})
        assert result["allowed_hours_start"] == "08:00"

    def test_analytics(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"total_messages": 1000}))
        result = client.sms.compliance.analytics()
        assert result["total_messages"] == 1000

    def test_logs(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=paginated_envelope([{"id": "log1"}]))
        result = client.sms.compliance.logs()
        assert len(result["data"]) == 1


class TestSmsConsents:
    def test_list(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=paginated_envelope([{"phone": "+5511999999999"}]))
        result = client.sms.consents.list()
        assert len(result["data"]) == 1

    def test_summary(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"total": 100, "opted_in": 80}))
        result = client.sms.consents.summary()
        assert result["total"] == 100

    def test_get(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"phone": "+5511999999999"}))
        assert client.sms.consents.get("+5511999999999")["phone"] == "+5511999999999"

    def test_create(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"phone": "+5511999999999", "status": "opted_in"}))
        result = client.sms.consents.create({"phone": "+5511999999999", "status": "opted_in"})
        assert result["status"] == "opted_in"

    def test_revoke(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(status_code=204)
        client.sms.consents.revoke("+5511999999999")

    def test_import_bulk(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json=single_envelope({"imported": 5}))
        result = client.sms.consents.import_bulk({"consents": []})
        assert result["imported"] == 5
