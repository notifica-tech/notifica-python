"""Fixtures compartilhadas para testes do SDK Notifica."""

from __future__ import annotations

from typing import Any

import pytest
from pytest_httpx import HTTPXMock

from notifica import Notifica


BASE_URL = "https://api.test.local/v1"
TEST_API_KEY = "nk_test_abc123"


@pytest.fixture
def client() -> Notifica:
    """Cria um cliente Notifica configurado para testes."""
    return Notifica(
        TEST_API_KEY,
        base_url=BASE_URL,
        timeout=5.0,
        max_retries=0,
    )


@pytest.fixture
def retrying_client() -> Notifica:
    """Cria um cliente Notifica com retries habilitados."""
    return Notifica(
        TEST_API_KEY,
        base_url=BASE_URL,
        timeout=5.0,
        max_retries=2,
    )


@pytest.fixture
def no_idempotency_client() -> Notifica:
    """Cria um cliente sem auto-idempotency."""
    return Notifica(
        TEST_API_KEY,
        base_url=BASE_URL,
        timeout=5.0,
        max_retries=0,
        auto_idempotency=False,
    )


def paginated_envelope(
    data: list[Any],
    cursor: str | None = None,
    has_more: bool = False,
) -> dict[str, Any]:
    """Constrói envelope de resposta paginada."""
    return {
        "data": data,
        "meta": {
            "cursor": cursor,
            "has_more": has_more,
        },
    }


def single_envelope(data: Any) -> dict[str, Any]:
    """Constrói envelope de resposta singular."""
    return {"data": data}


def error_body(
    code: str = "api_error",
    message: str = "Error",
    details: dict[str, list[str]] | None = None,
) -> dict[str, Any]:
    """Constrói corpo de erro da API."""
    body: dict[str, Any] = {
        "error": {
            "code": code,
            "message": message,
        }
    }
    if details:
        body["error"]["details"] = details
    return body
