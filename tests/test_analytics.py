"""Testes do recurso de analytics."""

from __future__ import annotations

from pytest_httpx import HTTPXMock

from notifica import Notifica


class TestAnalytics:
    def test_overview(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json={"data": {"total_sent": 100, "delivery_rate": 98.5}})
        result = client.analytics.overview({"period": "7d"})
        assert result["total_sent"] == 100

    def test_by_channel(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json={"data": [{"channel": "email", "sent": 50}]})
        result = client.analytics.by_channel({"period": "30d"})
        assert len(result) == 1

    def test_timeseries(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json={"data": [{"timestamp": "2024-01-01", "sent": 10}]})
        result = client.analytics.timeseries({"period": "7d", "granularity": "day"})
        assert len(result) == 1

    def test_top_templates(self, client: Notifica, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(json={"data": [{"template_id": "t1", "sent": 100}]})
        result = client.analytics.top_templates({"period": "30d", "limit": 10})
        assert len(result) == 1
