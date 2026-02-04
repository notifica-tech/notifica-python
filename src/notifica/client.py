"""Cliente HTTP do SDK Notifica."""

from __future__ import annotations

import random
import time
import uuid
from typing import Any, AsyncIterator, Iterator

import httpx

from .errors import ApiError, NotificaError, RateLimitError, TimeoutError, ValidationError

DEFAULT_BASE_URL = "https://app.usenotifica.com.br/v1"
DEFAULT_TIMEOUT = 30.0
DEFAULT_MAX_RETRIES = 3
SDK_VERSION = "0.1.0"

RETRYABLE_STATUS_CODES = frozenset({429, 500, 502, 503, 504})


def _clean_params(params: dict[str, Any] | None) -> dict[str, Any] | None:
    """Remove chaves com valor None de query params."""
    if params is None:
        return None
    return {k: v for k, v in params.items() if v is not None}


def _parse_error_body(response: httpx.Response) -> dict[str, Any]:
    """Extrai corpo de erro JSON de forma segura."""
    try:
        if response.content:
            return response.json()  # type: ignore[no-any-return]
    except Exception:
        pass
    return {}


def _parse_retry_after(response: httpx.Response) -> int | None:
    """Extrai o tempo de retry do header Retry-After."""
    header = response.headers.get("retry-after")
    if not header:
        return None
    try:
        return int(header)
    except ValueError:
        try:
            import email.utils

            date = email.utils.parsedate_to_datetime(header)
            return max(0, int(date.timestamp() - time.time()))
        except Exception:
            return None


def _raise_for_error(response: httpx.Response) -> None:
    """Lança exceção apropriada com base no status HTTP."""
    error_data = _parse_error_body(response)
    error_info = error_data.get("error", {})
    message = error_info.get("message", f"API error ({response.status_code})")
    code = error_info.get("code", "api_error")
    details = error_info.get("details", {})
    request_id = response.headers.get("x-request-id")

    if response.status_code == 422:
        raise ValidationError(message, details=details, request_id=request_id)

    if response.status_code == 429:
        retry_after = _parse_retry_after(response)
        raise RateLimitError(message, retry_after=retry_after, request_id=request_id)

    raise ApiError(
        message,
        status=response.status_code,
        code=code,
        details=details,
        request_id=request_id,
    )


class NotificaClient:
    """Cliente HTTP síncrono para a API Notifica.

    Implementa retry com exponential backoff, idempotency keys automáticas,
    paginação manual e auto-paginação.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        auto_idempotency: bool = True,
    ) -> None:
        if not api_key:
            raise NotificaError(
                "API key é obrigatória. Passe via: Notifica('nk_live_...')"
            )

        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries
        self._auto_idempotency = auto_idempotency

        self._client = httpx.Client(
            base_url=self._base_url,
            timeout=httpx.Timeout(timeout),
            headers=self._default_headers(),
        )

    def _default_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": f"notifica-python/{SDK_VERSION}",
        }

    # ── Core request ────────────────────────────────────

    def _request(
        self,
        method: str,
        path: str,
        json: Any | None = None,
        params: dict[str, Any] | None = None,
        options: dict[str, Any] | None = None,
    ) -> Any:
        """Faz uma requisição HTTP com retry e backoff."""
        options = options or {}
        headers = self._build_headers(method, options)
        req_timeout = options.get("timeout", self._timeout)
        clean = _clean_params(params)

        last_error: Exception | None = None

        for attempt in range(self._max_retries + 1):
            if attempt > 0:
                self._backoff(attempt, last_error)

            try:
                response = self._client.request(
                    method=method,
                    url=path,
                    json=json,
                    params=clean,
                    headers=headers,
                    timeout=req_timeout,
                )
            except httpx.TimeoutException as exc:
                last_error = TimeoutError(req_timeout)
                if attempt < self._max_retries:
                    continue
                raise last_error from exc
            except httpx.HTTPError as exc:
                last_error = NotificaError(f"Erro de rede: {exc}")
                if attempt < self._max_retries:
                    continue
                raise last_error from exc

            # 2xx — sucesso
            if response.is_success:
                if response.status_code == 204:
                    return None
                return response.json()

            # 429 — rate limit (retryable)
            if response.status_code == 429:
                error_data = _parse_error_body(response)
                retry_after = _parse_retry_after(response)
                err = RateLimitError(
                    error_data.get("error", {}).get("message", "Rate limit exceeded"),
                    retry_after=retry_after,
                    request_id=response.headers.get("x-request-id"),
                )
                if attempt < self._max_retries:
                    last_error = err
                    continue
                raise err

            # 5xx — server error (retryable)
            if response.status_code in RETRYABLE_STATUS_CODES and attempt < self._max_retries:
                error_data = _parse_error_body(response)
                last_error = ApiError(
                    error_data.get("error", {}).get(
                        "message", f"Server error ({response.status_code})"
                    ),
                    status=response.status_code,
                    code=error_data.get("error", {}).get("code", "server_error"),
                    details=error_data.get("error", {}).get("details", {}),
                    request_id=response.headers.get("x-request-id"),
                )
                continue

            # 4xx / demais erros — não retryable
            _raise_for_error(response)

        raise last_error or NotificaError("Request failed after max retries")

    def _build_headers(
        self, method: str, options: dict[str, Any]
    ) -> dict[str, str]:
        headers: dict[str, str] = {}
        if method == "POST":
            idem = options.get("idempotency_key")
            if idem:
                headers["Idempotency-Key"] = idem
            elif self._auto_idempotency:
                headers["Idempotency-Key"] = str(uuid.uuid4())
        return headers

    def _backoff(self, attempt: int, last_error: Exception | None) -> None:
        if isinstance(last_error, RateLimitError) and last_error.retry_after is not None:
            delay = float(last_error.retry_after)
        else:
            base = 0.5 * (2 ** (attempt - 1))
            jitter = random.random() * base * 0.5  # noqa: S311
            delay = base + jitter
        time.sleep(delay)

    # ── HTTP verbs ──────────────────────────────────────

    def get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: dict[str, Any] | None = None,
    ) -> Any:
        """GET request."""
        return self._request("GET", path, params=params, options=options)

    def post(
        self,
        path: str,
        json: Any | None = None,
        options: dict[str, Any] | None = None,
    ) -> Any:
        """POST request."""
        return self._request("POST", path, json=json, options=options)

    def put(
        self,
        path: str,
        json: Any | None = None,
        options: dict[str, Any] | None = None,
    ) -> Any:
        """PUT request."""
        return self._request("PUT", path, json=json, options=options)

    def patch(
        self,
        path: str,
        json: Any | None = None,
        options: dict[str, Any] | None = None,
    ) -> Any:
        """PATCH request."""
        return self._request("PATCH", path, json=json, options=options)

    def delete(
        self,
        path: str,
        options: dict[str, Any] | None = None,
    ) -> Any:
        """DELETE request."""
        return self._request("DELETE", path, options=options)

    # ── Pagination helpers ──────────────────────────────

    def list(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Lista com paginação manual — retorna ``{data, meta}``."""
        return self.get(path, params=params, options=options)

    def get_one(
        self,
        path: str,
        options: dict[str, Any] | None = None,
    ) -> Any:
        """Obtém um objeto único, extraindo de ``{data: T}``."""
        response = self.get(path, options=options)
        return response["data"]

    def list_auto(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> Iterator[Any]:
        """Auto-paginação via iterator síncrono."""
        cursor: str | None = None
        while True:
            query = {**(params or {})}
            if cursor:
                query["cursor"] = cursor
            response = self.list(path, params=query)
            yield from response["data"]
            meta = response.get("meta", {})
            if not meta.get("has_more"):
                break
            cursor = meta.get("cursor")

    # ── Lifecycle ───────────────────────────────────────

    def close(self) -> None:
        """Fecha o cliente HTTP."""
        self._client.close()

    def __enter__(self) -> NotificaClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


# ═══════════════════════════════════════════════════════
# Async Client
# ═══════════════════════════════════════════════════════


class AsyncNotificaClient:
    """Cliente HTTP assíncrono para a API Notifica.

    Mesma API que ``NotificaClient``, porém com ``await``.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        auto_idempotency: bool = True,
    ) -> None:
        if not api_key:
            raise NotificaError(
                "API key é obrigatória. Passe via: AsyncNotifica('nk_live_...')"
            )

        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries
        self._auto_idempotency = auto_idempotency

        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            timeout=httpx.Timeout(timeout),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": f"notifica-python/{SDK_VERSION}",
            },
        )

    # ── Core request ────────────────────────────────────

    async def _request(
        self,
        method: str,
        path: str,
        json: Any | None = None,
        params: dict[str, Any] | None = None,
        options: dict[str, Any] | None = None,
    ) -> Any:
        """Faz uma requisição HTTP assíncrona com retry e backoff."""
        import asyncio

        options = options or {}
        headers = self._build_headers(method, options)
        req_timeout = options.get("timeout", self._timeout)
        clean = _clean_params(params)

        last_error: Exception | None = None

        for attempt in range(self._max_retries + 1):
            if attempt > 0:
                await self._backoff(attempt, last_error)

            try:
                response = await self._client.request(
                    method=method,
                    url=path,
                    json=json,
                    params=clean,
                    headers=headers,
                    timeout=req_timeout,
                )
            except httpx.TimeoutException as exc:
                last_error = TimeoutError(req_timeout)
                if attempt < self._max_retries:
                    continue
                raise last_error from exc
            except httpx.HTTPError as exc:
                last_error = NotificaError(f"Erro de rede: {exc}")
                if attempt < self._max_retries:
                    continue
                raise last_error from exc

            if response.is_success:
                if response.status_code == 204:
                    return None
                return response.json()

            if response.status_code == 429:
                error_data = _parse_error_body(response)
                retry_after = _parse_retry_after(response)
                err = RateLimitError(
                    error_data.get("error", {}).get("message", "Rate limit exceeded"),
                    retry_after=retry_after,
                    request_id=response.headers.get("x-request-id"),
                )
                if attempt < self._max_retries:
                    last_error = err
                    continue
                raise err

            if response.status_code in RETRYABLE_STATUS_CODES and attempt < self._max_retries:
                error_data = _parse_error_body(response)
                last_error = ApiError(
                    error_data.get("error", {}).get(
                        "message", f"Server error ({response.status_code})"
                    ),
                    status=response.status_code,
                    code=error_data.get("error", {}).get("code", "server_error"),
                    details=error_data.get("error", {}).get("details", {}),
                    request_id=response.headers.get("x-request-id"),
                )
                continue

            _raise_for_error(response)

        raise last_error or NotificaError("Request failed after max retries")

    def _build_headers(
        self, method: str, options: dict[str, Any]
    ) -> dict[str, str]:
        headers: dict[str, str] = {}
        if method == "POST":
            idem = options.get("idempotency_key")
            if idem:
                headers["Idempotency-Key"] = idem
            elif self._auto_idempotency:
                headers["Idempotency-Key"] = str(uuid.uuid4())
        return headers

    async def _backoff(self, attempt: int, last_error: Exception | None) -> None:
        import asyncio

        if isinstance(last_error, RateLimitError) and last_error.retry_after is not None:
            delay = float(last_error.retry_after)
        else:
            base = 0.5 * (2 ** (attempt - 1))
            jitter = random.random() * base * 0.5  # noqa: S311
            delay = base + jitter
        await asyncio.sleep(delay)

    # ── HTTP verbs ──────────────────────────────────────

    async def get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: dict[str, Any] | None = None,
    ) -> Any:
        """GET request."""
        return await self._request("GET", path, params=params, options=options)

    async def post(
        self,
        path: str,
        json: Any | None = None,
        options: dict[str, Any] | None = None,
    ) -> Any:
        """POST request."""
        return await self._request("POST", path, json=json, options=options)

    async def put(
        self,
        path: str,
        json: Any | None = None,
        options: dict[str, Any] | None = None,
    ) -> Any:
        """PUT request."""
        return await self._request("PUT", path, json=json, options=options)

    async def patch(
        self,
        path: str,
        json: Any | None = None,
        options: dict[str, Any] | None = None,
    ) -> Any:
        """PATCH request."""
        return await self._request("PATCH", path, json=json, options=options)

    async def delete(
        self,
        path: str,
        options: dict[str, Any] | None = None,
    ) -> Any:
        """DELETE request."""
        return await self._request("DELETE", path, options=options)

    # ── Pagination helpers ──────────────────────────────

    async def list(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Lista com paginação manual — retorna ``{data, meta}``."""
        return await self.get(path, params=params, options=options)

    async def get_one(
        self,
        path: str,
        options: dict[str, Any] | None = None,
    ) -> Any:
        """Obtém um objeto único, extraindo de ``{data: T}``."""
        response = await self.get(path, options=options)
        return response["data"]

    async def list_auto(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> AsyncIterator[Any]:
        """Auto-paginação via async iterator."""
        cursor: str | None = None
        while True:
            query = {**(params or {})}
            if cursor:
                query["cursor"] = cursor
            response = await self.list(path, params=query)
            for item in response["data"]:
                yield item
            meta = response.get("meta", {})
            if not meta.get("has_more"):
                break
            cursor = meta.get("cursor")

    # ── Lifecycle ───────────────────────────────────────

    async def close(self) -> None:
        """Fecha o cliente HTTP."""
        await self._client.aclose()

    async def __aenter__(self) -> AsyncNotificaClient:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()
