"""SDK Python oficial para o Notifica — plataforma de notificações multicanal.

Exemplo de uso:

    from notifica import Notifica

    client = Notifica("nk_live_...")

    notification = client.notifications.send({
        "channel": "whatsapp",
        "to": "+5511999999999",
        "template": "welcome",
        "data": {"name": "João"},
    })

Async:

    from notifica import AsyncNotifica

    async with AsyncNotifica("nk_live_...") as client:
        await client.notifications.send(...)
"""

from __future__ import annotations

from .client import AsyncNotificaClient, NotificaClient
from .errors import ApiError, NotificaError, RateLimitError, TimeoutError, ValidationError
from .resources.analytics import Analytics
from .resources.api_keys import ApiKeys
from .resources.billing import Billing
from .resources.channels import Channels
from .resources.domains import Domains
from .resources.inbox import Inbox
from .resources.inbox_embed import InboxEmbed
from .resources.notifications import Notifications
from .resources.sms import Sms
from .resources.subscribers import Subscribers
from .resources.templates import Templates
from .resources.webhooks import Webhooks
from .resources.workflows import Workflows

__version__ = "0.1.0"

__all__ = [
    # Clientes
    "Notifica",
    "AsyncNotifica",
    # Erros
    "NotificaError",
    "ApiError",
    "ValidationError",
    "RateLimitError",
    "TimeoutError",
    # Recursos (para uso avançado)
    "Notifications",
    "Templates",
    "Workflows",
    "Subscribers",
    "Channels",
    "Domains",
    "Webhooks",
    "ApiKeys",
    "Analytics",
    "Sms",
    "Billing",
    "InboxEmbed",
    "Inbox",
]


class Notifica:
    """Cliente oficial do Notifica para Python (síncrono).

    Args:
        api_key: API key (``nk_live_...``, ``nk_test_...``, etc.)
        base_url: URL base da API (default: ``https://app.usenotifica.com.br/v1``)
        timeout: Timeout padrão em segundos (default: 30.0)
        max_retries: Máximo de retries em 429/5xx (default: 3)
        auto_idempotency: Gerar idempotency key automaticamente para POSTs (default: True)

    Example:
        ```python
        from notifica import Notifica

        # Simples — apenas API key
        client = Notifica("nk_live_...")

        # Configuração completa
        client = Notifica(
            "nk_live_...",
            base_url="https://app.usenotifica.com.br/v1",
            timeout=15.0,
            max_retries=5,
        )

        # Context manager (fecha automaticamente)
        with Notifica("nk_live_...") as client:
            client.notifications.send(...)
        ```
    """

    notifications: Notifications
    templates: Templates
    workflows: Workflows
    subscribers: Subscribers
    channels: Channels
    domains: Domains
    webhooks: Webhooks
    api_keys: ApiKeys
    analytics: Analytics
    sms: Sms
    billing: Billing
    inbox_embed: InboxEmbed
    inbox: Inbox

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = "https://app.usenotifica.com.br/v1",
        timeout: float = 30.0,
        max_retries: int = 3,
        auto_idempotency: bool = True,
    ) -> None:
        self._client = NotificaClient(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            auto_idempotency=auto_idempotency,
        )

        self.notifications = Notifications(self._client)
        self.templates = Templates(self._client)
        self.workflows = Workflows(self._client)
        self.subscribers = Subscribers(self._client)
        self.channels = Channels(self._client)
        self.domains = Domains(self._client)
        self.webhooks = Webhooks(self._client)
        self.api_keys = ApiKeys(self._client)
        self.analytics = Analytics(self._client)
        self.sms = Sms(self._client)
        self.billing = Billing(self._client)
        self.inbox_embed = InboxEmbed(self._client)
        self.inbox = Inbox(self._client)

    def close(self) -> None:
        """Fecha o cliente HTTP."""
        self._client.close()

    def __enter__(self) -> Notifica:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


class AsyncNotifica:
    """Cliente oficial do Notifica para Python (assíncrono).

    Mesma API que ``Notifica``, porém todos os métodos são ``async``.

    Example:
        ```python
        from notifica import AsyncNotifica

        async with AsyncNotifica("nk_live_...") as client:
            notification = await client.notifications.send({
                "channel": "whatsapp",
                "to": "+5511999999999",
                "template": "welcome",
            })
        ```
    """

    # Async resources reuse the same resource classes — the async client
    # has the same method signatures (get/post/etc) but returns coroutines.
    # Since resource methods call client.post(...) etc., in async mode we
    # need async resource wrappers. For now we expose the sync resource
    # classes — the user should use the sync client for sync and the
    # AsyncNotifica provides direct async methods via _client.

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = "https://app.usenotifica.com.br/v1",
        timeout: float = 30.0,
        max_retries: int = 3,
        auto_idempotency: bool = True,
    ) -> None:
        self._client = AsyncNotificaClient(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            auto_idempotency=auto_idempotency,
        )

    async def close(self) -> None:
        """Fecha o cliente HTTP."""
        await self._client.close()

    async def __aenter__(self) -> AsyncNotifica:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()
