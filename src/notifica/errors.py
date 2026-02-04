"""Classes de erro do SDK Notifica."""

from typing import Any


class NotificaError(Exception):
    """Classe base para todos os erros do SDK Notifica."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class ApiError(NotificaError):
    """Erro retornado pela API.

    Contém status HTTP, código do erro, e request ID para debugging.
    """

    def __init__(
        self,
        message: str,
        status: int,
        code: str,
        details: dict[str, list[str]] | None = None,
        request_id: str | None = None,
    ) -> None:
        super().__init__(message)
        self.status = status
        self.code = code
        self.details = details or {}
        self.request_id = request_id

    def __str__(self) -> str:
        parts = [f"[{self.status}] {self.code}: {self.message}"]
        if self.request_id:
            parts.append(f"(request_id: {self.request_id})")
        return " ".join(parts)


class ValidationError(ApiError):
    """Erro de validação (HTTP 422)."""

    def __init__(
        self,
        message: str,
        details: dict[str, list[str]] | None = None,
        request_id: str | None = None,
    ) -> None:
        super().__init__(message, 422, "validation_failed", details, request_id)


class RateLimitError(ApiError):
    """Rate limit excedido (HTTP 429).

    Inclui o tempo para tentar novamente.
    """

    def __init__(
        self,
        message: str,
        retry_after: int | None = None,
        request_id: str | None = None,
    ) -> None:
        super().__init__(message, 429, "rate_limit_exceeded", {}, request_id)
        self.retry_after = retry_after


class TimeoutError(NotificaError):
    """Timeout de conexão ou request."""

    def __init__(self, timeout_seconds: float) -> None:
        super().__init__(f"Request timed out after {timeout_seconds}s")
        self.timeout_seconds = timeout_seconds
