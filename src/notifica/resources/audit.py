"""Recurso de audit logs do SDK Notifica.

⚠️ **Admin Only**: Este recurso requer autenticação admin (Bearer token do backoffice).
Não está disponível com API keys regulares.

Use audit logs para rastrear ações sensíveis na sua organização:
- Ciclo de vida de API keys (criadas, rotacionadas, revogadas)
- Mudanças de membros do time (convidados, removidos, mudanças de role)
- Eventos de subscription (criada, mudança de plano, cancelamento, falha de pagamento)
- Gerenciamento de domínios (adicionados, verificados, removidos)
- Configuração de webhooks (criados, atualizados, deletados)
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterator

if TYPE_CHECKING:
    from ..client import NotificaClient


class Audit:
    """Recurso de audit logs.
    
    ⚠️ **Admin Only**: Requer autenticação admin.
    
    Example:
        ```python
        # Listar logs recentes
        logs = client.audit.list({"limit": 50})
        
        # Filtrar por ação
        api_key_logs = client.audit.list({
            "action": "api_key.created",
            "limit": 20,
        })
        
        # Filtrar por tipo de recurso
        webhook_logs = client.audit.list({
            "resource_type": "webhook",
        })
        ```
    """

    def __init__(self, client: NotificaClient) -> None:
        self._client = client
        self._base_path = "/internal/audit-logs"

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Lista audit logs com filtros opcionais.
        
        ⚠️ **Admin Only**: Requer autenticação admin.

        Args:
            params: Filtros opcionais:
                - action: Filtrar por ação (ex: 'api_key.created')
                - resource_type: Filtrar por tipo de recurso (ex: 'api_key', 'webhook')
                - resource_id: Filtrar por ID do recurso
                - actor_type: Filtrar por tipo de ator ('user', 'api_key', 'system')
                - actor_id: Filtrar por ID do ator
                - start_date: Data inicial (ISO 8601)
                - end_date: Data final (ISO 8601)
                - limit: Número máximo de resultados
                - cursor: Cursor para paginação
            options: Opções da requisição

        Returns:
            Resposta paginada com lista de audit logs

        Example:
            ```python
            # Listar todos os logs recentes
            result = client.audit.list({"limit": 100})
            for log in result["data"]:
                print(log["action"], log["actor"]["name"])
            
            # Filtrar por período
            logs = client.audit.list({
                "start_date": "2024-01-01T00:00:00Z",
                "end_date": "2024-01-31T23:59:59Z",
            })
            ```
        """
        return self._client.list(self._base_path, params=params, options=options)  # type: ignore[no-any-return]

    def list_auto(self, params: dict[str, Any] | None = None) -> Iterator[dict[str, Any]]:
        """Itera automaticamente por todos os audit logs.
        
        ⚠️ **Admin Only**: Requer autenticação admin.

        Args:
            params: Filtros (mesmos de list())

        Yields:
            Audit logs um por um

        Example:
            ```python
            for log in client.audit.list_auto({"resource_type": "api_key"}):
                print(log["action"], log["resource_id"])
            ```
        """
        return self._client.list_auto(self._base_path, params=params)

    def get(self, id: str, options: dict[str, Any] | None = None) -> dict[str, Any]:
        """Obtém um audit log específico pelo ID.
        
        ⚠️ **Admin Only**: Requer autenticação admin.

        Args:
            id: ID do audit log
            options: Opções da requisição

        Returns:
            O audit log

        Example:
            ```python
            log = client.audit.get("audit_abc123")
            print(log["action"], log["actor"]["name"], log["created_at"])
            ```
        """
        return self._client.get_one(f"{self._base_path}/{id}", options=options)  # type: ignore[no-any-return]
