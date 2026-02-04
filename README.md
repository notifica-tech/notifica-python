# Notifica Python SDK

SDK Python oficial para a API do [Notifica](https://usenotifica.com.br) — plataforma de notificações multicanal (WhatsApp, SMS, Email, Push, In-App).

## Instalação

```bash
pip install notifica
```

## Uso Rápido

```python
from notifica import Notifica

client = Notifica("nk_live_...")

# Enviar notificação
notification = client.notifications.send(
    channel="whatsapp",
    to="+5511999999999",
    template="welcome",
    data={"name": "João"},
)
print(f"Notificação enviada: {notification['id']}")
```

## Autenticação

O SDK aceita sua API key diretamente ou via objeto de configuração:

```python
# Simples
client = Notifica("nk_live_...")

# Com configurações adicionais
client = Notifica(
    api_key="nk_live_...",
    base_url="https://app.usenotifica.com.br/v1",
    timeout=30.0,
    max_retries=3,
)
```

## Recursos

### Notificações

```python
# Enviar
notification = client.notifications.send(
    channel="email",
    to="joao@empresa.com.br",
    template="welcome",
    data={"name": "João"},
)

# Listar com paginação manual
result = client.notifications.list(limit=50)
for n in result["data"]:
    print(n["id"])

# Auto-paginação (iterator)
for notification in client.notifications.list_auto(channel="email"):
    print(notification["id"])

# Obter detalhes
notification = client.notifications.get("not_abc123")

# Listar tentativas de entrega
attempts = client.notifications.list_attempts("not_abc123")
```

### Templates

```python
# Criar
template = client.templates.create(
    channel="email",
    slug="welcome-email",
    name="Email de Boas-Vindas",
    content="Olá {{name}}, bem-vindo!",
)

# Listar, obter, atualizar, deletar
templates = client.templates.list()
template = client.templates.get("tpl_abc123")
updated = client.templates.update("tpl_abc123", {"name": "Novo Nome"})
client.templates.delete("tpl_abc123")

# Preview e validação
preview = client.templates.preview("tpl_abc123", variables={"name": "Teste"})
validation = client.templates.validate("tpl_abc123")
```

### Workflows

```python
# Criar workflow
workflow = client.workflows.create(
    slug="welcome-flow",
    name="Fluxo de Boas-Vindas",
    steps=[
        {"type": "send", "channel": "email", "template": "welcome-email"},
        {"type": "delay", "duration": "1h"},
        {"type": "send", "channel": "whatsapp", "template": "welcome-whatsapp"},
    ],
)

# Disparar workflow
run = client.workflows.trigger("welcome-flow", recipient="+5511999999999")

# Gerenciar execuções
runs = client.workflows.list_runs()
run = client.workflows.get_run("run_abc123")
cancelled = client.workflows.cancel_run("run_abc123")
```

### Subscribers

```python
# Criar (upsert por external_id)
subscriber = client.subscribers.create(
    external_id="user-123",
    email="joao@empresa.com.br",
    phone="+5511999998888",
    name="João Silva",
)

# Auto-paginação
for sub in client.subscribers.list_auto():
    print(sub["external_id"])

# Preferências
prefs = client.subscribers.get_preferences("sub_abc123")
client.subscribers.update_preferences("sub_abc123", {
    "preferences": [
        {"category": "marketing", "channel": "email", "enabled": False},
    ]
})

# Notificações in-app
notifications = client.subscribers.list_notifications("sub_abc123")
client.subscribers.mark_read("sub_abc123", "not_abc123")
count = client.subscribers.get_unread_count("sub_abc123")

# Importação em lote
result = client.subscribers.bulk_import([
    {"external_id": "user-1", "email": "a@b.com"},
    {"external_id": "user-2", "email": "c@d.com"},
])
```

### SMS (BYOP - Bring Your Own Provider)

```python
# Provedores
provider = client.sms.providers.create(
    type="twilio",
    name="Meu Twilio",
    config={
        "account_sid": "AC...",
        "auth_token": "...",
        "phone_number": "+1234567890",
    },
)
client.sms.providers.activate("sms_abc123")

# Compliance
settings = client.sms.compliance.show()
client.sms.compliance.update(allowed_hours_start="08:00", allowed_hours_end="20:00")

# Consentimentos
consent = client.sms.consents.create(phone="+5511999999999", status="opted_in")
summary = client.sms.consents.summary()
```

### Billing

```python
# Planos
plans = client.billing.plans.list()
plan = client.billing.plans.get("startup")

# Assinatura
subscription = client.billing.subscription.get()
client.billing.subscription.subscribe(plan_name="startup", period="monthly")
client.billing.subscription.change_plan(plan_name="pro")
proration = client.billing.subscription.calculate_proration(plan_name="pro")

# Faturas
invoices = client.billing.invoices.list()
invoice = client.billing.invoices.get("inv_abc123")

# Métodos de pagamento
methods = client.billing.payment_methods.list()
method = client.billing.payment_methods.create(
    type="credit_card",
    card_token="tok_...",
)
client.billing.payment_methods.set_default("pm_abc123")

# Uso
usage = client.billing.usage.get()
```

### Webhooks

```python
# Criar (salve o signing_secret!)
webhook = client.webhooks.create(
    url="https://meuapp.com.br/webhooks/notifica",
    events=["notification.delivered", "notification.failed"],
)
print(f"Secret: {webhook['signing_secret']}")  # ⚠️ Só disponível na criação

# Verificar assinatura
import hmac
import hashlib

def verify_webhook(payload: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
```

### Analytics

```python
overview = client.analytics.overview(period="7d")
channels = client.analytics.by_channel(period="30d")
timeseries = client.analytics.timeseries(period="7d", granularity="day")
top_templates = client.analytics.top_templates(period="30d", limit=10)
```

## Async/Await

O SDK também oferece cliente assíncrono:

```python
import asyncio
from notifica import AsyncNotifica

async def main():
    async with AsyncNotifica("nk_live_...") as client:
        notification = await client.notifications.send(
            channel="whatsapp",
            to="+5511999999999",
            template="welcome",
            data={"name": "João"},
        )
        print(notification["id"])

asyncio.run(main())
```

## Tratamento de Erros

```python
from notifica import Notifica
from notifica.errors import (
    NotificaError,
    ApiError,
    ValidationError,
    RateLimitError,
)

client = Notifica("nk_live_...")

try:
    client.notifications.send(channel="email", to="invalid", template="test")
except ValidationError as e:
    print(f"Erro de validação: {e.message}")
    print(f"Detalhes: {e.details}")
except RateLimitError as e:
    print(f"Rate limit. Tente novamente em {e.retry_after}s")
except ApiError as e:
    print(f"Erro da API: {e.status} - {e.code}")
    print(f"Request ID: {e.request_id}")
except NotificaError as e:
    print(f"Erro do SDK: {e}")
```

## Configuração

| Opção | Descrição | Padrão |
|-------|-----------|--------|
| `api_key` | Sua API key (obrigatória) | - |
| `base_url` | URL base da API | `https://app.usenotifica.com.br/v1` |
| `timeout` | Timeout em segundos | `30.0` |
| `max_retries` | Máximo de retries | `3` |
| `auto_idempotency` | Gerar idempotency key automaticamente | `True` |

## Requisitos

- Python 3.10+
- httpx 0.27+

## Licença

MIT
