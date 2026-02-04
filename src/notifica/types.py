"""Tipos da API Notifica.

Todos os tipos usam TypedDict para compatibilidade com dict literal.
"""

from __future__ import annotations

from typing import Any, Literal, NotRequired, TypedDict

# ═══════════════════════════════════════════════════
# Tipos comuns
# ═══════════════════════════════════════════════════

Channel = Literal["email", "whatsapp", "sms", "in_app", "push"]
NotificationStatus = Literal[
    "pending", "processing", "delivered", "failed", "bounced", "rejected"
]
TemplateStatus = Literal["draft", "active"]
Environment = Literal["production", "sandbox"]
ApiKeyType = Literal["secret", "public"]


class PaginationMeta(TypedDict):
    """Metadados de paginação."""

    cursor: str | None
    has_more: bool


class PaginatedResponse(TypedDict):
    """Resposta paginada genérica."""

    data: list[Any]
    meta: PaginationMeta


class SingleResponse(TypedDict):
    """Resposta com objeto único."""

    data: Any


# ═══════════════════════════════════════════════════
# Notificações
# ═══════════════════════════════════════════════════


class SendNotificationParams(TypedDict):
    """Parâmetros para enviar notificação."""

    channel: Channel
    to: str
    template: NotRequired[str]
    data: NotRequired[dict[str, Any]]
    metadata: NotRequired[dict[str, Any]]


class Notification(TypedDict):
    """Objeto de notificação."""

    id: str
    channel: Channel
    recipient: str
    status: NotificationStatus
    template_id: NotRequired[str]
    metadata: NotRequired[dict[str, Any]]
    created_at: str
    updated_at: NotRequired[str]


class MessageAttempt(TypedDict):
    """Tentativa de entrega de mensagem."""

    id: str
    attempt_number: int
    status: str
    provider_response: NotRequired[dict[str, Any]]
    created_at: str


class ListNotificationsParams(TypedDict):
    """Parâmetros para listar notificações."""

    limit: NotRequired[int]
    cursor: NotRequired[str]
    status: NotRequired[NotificationStatus]
    channel: NotRequired[Channel]


# ═══════════════════════════════════════════════════
# Templates
# ═══════════════════════════════════════════════════


class CreateTemplateParams(TypedDict):
    """Parâmetros para criar template."""

    channel: Channel
    slug: str
    name: str
    content: str
    variables: NotRequired[list[str]]
    variants: NotRequired[dict[str, str]]
    language: NotRequired[str]
    status: NotRequired[TemplateStatus]
    metadata: NotRequired[dict[str, Any]]
    provider_template_id: NotRequired[str]


class UpdateTemplateParams(TypedDict):
    """Parâmetros para atualizar template."""

    name: NotRequired[str]
    content: NotRequired[str]
    variables: NotRequired[list[str]]
    variants: NotRequired[dict[str, str]]
    language: NotRequired[str]
    status: NotRequired[TemplateStatus]
    metadata: NotRequired[dict[str, Any]]
    provider_template_id: NotRequired[str]


class Template(TypedDict):
    """Objeto de template."""

    id: str
    slug: str
    name: str
    channel: Channel
    content: str
    variables: list[str]
    variants: NotRequired[dict[str, str]]
    language: str
    status: TemplateStatus
    metadata: NotRequired[dict[str, Any]]
    provider_template_id: NotRequired[str]
    created_at: str
    updated_at: str


class PreviewTemplateParams(TypedDict):
    """Parâmetros para preview de template."""

    variables: dict[str, Any]


class PreviewContentParams(TypedDict):
    """Parâmetros para preview de conteúdo."""

    content: str
    channel: Channel
    variables: NotRequired[dict[str, Any]]
    variants: NotRequired[dict[str, str]]


class ValidationResult(TypedDict):
    """Resultado de validação."""

    valid: bool
    errors: list[str]
    warnings: list[str]
    variables: NotRequired[list[str]]


class PreviewResult(TypedDict):
    """Resultado de preview."""

    rendered: dict[str, str]
    variables: list[str]
    validation: ValidationResult


class ValidateContentParams(TypedDict):
    """Parâmetros para validação de conteúdo."""

    content: str
    channel: Channel
    variants: NotRequired[dict[str, str]]


class ListTemplatesParams(TypedDict):
    """Parâmetros para listar templates."""

    limit: NotRequired[int]
    cursor: NotRequired[str]
    channel: NotRequired[Channel]
    status: NotRequired[TemplateStatus]


# ═══════════════════════════════════════════════════
# Workflows
# ═══════════════════════════════════════════════════


class SendStep(TypedDict):
    """Passo de envio em workflow."""

    type: Literal["send"]
    channel: Channel
    template: str


class DelayStep(TypedDict):
    """Passo de delay em workflow."""

    type: Literal["delay"]
    duration: str


class FallbackStep(TypedDict):
    """Passo de fallback em workflow."""

    type: Literal["fallback"]
    channels: list[Channel]
    template: str


WorkflowStep = SendStep | DelayStep | FallbackStep


class CreateWorkflowParams(TypedDict):
    """Parâmetros para criar workflow."""

    slug: str
    name: str
    steps: list[WorkflowStep]


class UpdateWorkflowParams(TypedDict):
    """Parâmetros para atualizar workflow."""

    name: NotRequired[str]
    steps: NotRequired[list[WorkflowStep]]


class Workflow(TypedDict):
    """Objeto de workflow."""

    id: str
    slug: str
    name: str
    steps: list[WorkflowStep]
    version: int
    active: bool
    created_at: str
    updated_at: str


class TriggerWorkflowParams(TypedDict):
    """Parâmetros para disparar workflow."""

    recipient: str
    data: NotRequired[dict[str, Any]]


WorkflowRunStatus = Literal[
    "pending", "running", "completed", "failed", "cancelled"
]


class StepResult(TypedDict):
    """Resultado de um passo do workflow."""

    step_index: int
    step_type: str
    status: str
    result: NotRequired[dict[str, Any]]
    executed_at: str


class WorkflowRun(TypedDict):
    """Execução de workflow."""

    id: str
    workflow_id: str
    workflow_slug: str
    workflow_version: int
    status: WorkflowRunStatus
    recipient: str
    data: NotRequired[dict[str, Any]]
    step_results: NotRequired[list[StepResult]]
    created_at: str
    updated_at: str


class ListWorkflowsParams(TypedDict):
    """Parâmetros para listar workflows."""

    limit: NotRequired[int]
    cursor: NotRequired[str]


class ListWorkflowRunsParams(TypedDict):
    """Parâmetros para listar execuções de workflow."""

    limit: NotRequired[int]
    cursor: NotRequired[str]
    workflow_id: NotRequired[str]
    status: NotRequired[WorkflowRunStatus]


# ═══════════════════════════════════════════════════
# Subscribers
# ═══════════════════════════════════════════════════


class CreateSubscriberParams(TypedDict):
    """Parâmetros para criar subscriber."""

    external_id: str
    email: NotRequired[str]
    phone: NotRequired[str]
    name: NotRequired[str]
    locale: NotRequired[str]
    timezone: NotRequired[str]
    custom_properties: NotRequired[dict[str, Any]]


class UpdateSubscriberParams(TypedDict):
    """Parâmetros para atualizar subscriber."""

    email: NotRequired[str]
    phone: NotRequired[str]
    name: NotRequired[str]
    locale: NotRequired[str]
    timezone: NotRequired[str]
    custom_properties: NotRequired[dict[str, Any]]


class Subscriber(TypedDict):
    """Objeto de subscriber."""

    id: str
    external_id: str
    email: NotRequired[str]
    phone: NotRequired[str]
    name: NotRequired[str]
    locale: NotRequired[str]
    timezone: NotRequired[str]
    custom_properties: NotRequired[dict[str, Any]]
    created_at: str
    updated_at: str


class NotificationPreference(TypedDict):
    """Preferência de notificação."""

    category: str
    channel: str
    enabled: bool


class UpdatePreferencesParams(TypedDict):
    """Parâmetros para atualizar preferências."""

    preferences: list[NotificationPreference]


class SubscriberPreferences(TypedDict):
    """Preferências de subscriber."""

    preferences: list[NotificationPreference]


class BulkImportParams(TypedDict):
    """Parâmetros para importação em lote."""

    subscribers: list[CreateSubscriberParams]


class BulkImportResult(TypedDict):
    """Resultado de importação em lote."""

    imported: int
    subscribers: list[Subscriber]


class InAppNotification(TypedDict):
    """Notificação in-app."""

    id: str
    title: NotRequired[str]
    body: NotRequired[str]
    action_url: NotRequired[str]
    read: bool
    created_at: str


class ListInAppParams(TypedDict):
    """Parâmetros para listar notificações in-app."""

    limit: NotRequired[int]
    offset: NotRequired[int]
    unread_only: NotRequired[bool]


class UnreadCountResult(TypedDict):
    """Resultado de contagem de não lidas."""

    count: int


class ListSubscribersParams(TypedDict):
    """Parâmetros para listar subscribers."""

    limit: NotRequired[int]
    cursor: NotRequired[str]
    search: NotRequired[str]
    offset: NotRequired[int]


# ═══════════════════════════════════════════════════
# Channels
# ═══════════════════════════════════════════════════


class CreateChannelParams(TypedDict):
    """Parâmetros para criar configuração de canal."""

    channel: Channel
    provider: str
    credentials: dict[str, Any]
    settings: NotRequired[dict[str, Any]]


class UpdateChannelParams(TypedDict):
    """Parâmetros para atualizar configuração de canal."""

    provider: NotRequired[str]
    credentials: NotRequired[dict[str, Any]]
    settings: NotRequired[dict[str, Any]]


class ChannelConfiguration(TypedDict):
    """Configuração de canal."""

    id: str
    channel: Channel
    provider: str
    settings: NotRequired[dict[str, Any]]
    created_at: str
    updated_at: str


class TestChannelResult(TypedDict):
    """Resultado de teste de canal."""

    success: bool
    message: str


# ═══════════════════════════════════════════════════
# Domains
# ═══════════════════════════════════════════════════


class CreateDomainParams(TypedDict):
    """Parâmetros para criar domínio."""

    domain: str


DomainStatus = Literal["pending", "verified", "failed"]


class DnsRecord(TypedDict):
    """Registro DNS."""

    name: str
    type: str
    value: str


class DomainDnsRecords(TypedDict):
    """Registros DNS de domínio."""

    txt: NotRequired[DnsRecord]
    dkim: NotRequired[list[DnsRecord]]
    spf: NotRequired[DnsRecord]


class Domain(TypedDict):
    """Objeto de domínio."""

    id: str
    domain: str
    status: DomainStatus
    dns_records: NotRequired[DomainDnsRecords]
    verified_at: NotRequired[str]
    created_at: str
    updated_at: str


class DomainHealth(TypedDict):
    """Saúde do domínio."""

    domain_id: str
    dns_valid: bool
    dkim_valid: bool
    spf_valid: bool
    last_checked_at: str
    issues: NotRequired[list[str]]


class DomainAlert(TypedDict):
    """Alerta de domínio."""

    id: str
    domain_id: str
    alert_type: str
    message: str
    severity: str
    created_at: str


class ListDomainsParams(TypedDict):
    """Parâmetros para listar domínios."""

    limit: NotRequired[int]
    cursor: NotRequired[str]


# ═══════════════════════════════════════════════════
# Webhooks
# ═══════════════════════════════════════════════════


class CreateWebhookParams(TypedDict):
    """Parâmetros para criar webhook."""

    url: str
    events: list[str]


class UpdateWebhookParams(TypedDict):
    """Parâmetros para atualizar webhook."""

    url: NotRequired[str]
    events: NotRequired[list[str]]
    active: NotRequired[bool]


class Webhook(TypedDict):
    """Objeto de webhook."""

    id: str
    url: str
    events: list[str]
    active: bool
    signing_secret: NotRequired[str]
    created_at: str
    updated_at: str


class WebhookDelivery(TypedDict):
    """Entrega de webhook."""

    id: str
    event: str
    status: str
    status_code: NotRequired[int]
    response_body: NotRequired[str]
    created_at: str


class ListWebhooksParams(TypedDict):
    """Parâmetros para listar webhooks."""

    limit: NotRequired[int]
    cursor: NotRequired[str]


class ListDeliveriesParams(TypedDict):
    """Parâmetros para listar entregas."""

    limit: NotRequired[int]


# ═══════════════════════════════════════════════════
# API Keys
# ═══════════════════════════════════════════════════


class CreateApiKeyParams(TypedDict):
    """Parâmetros para criar API key."""

    key_type: ApiKeyType
    label: str
    environment: Environment


class ApiKey(TypedDict):
    """Objeto de API key."""

    id: str
    key_type: ApiKeyType
    label: str
    prefix: str
    environment: Environment
    raw_key: NotRequired[str]
    created_at: str


# ═══════════════════════════════════════════════════
# Analytics
# ═══════════════════════════════════════════════════

AnalyticsPeriod = Literal["1h", "24h", "7d", "30d"]
Granularity = Literal["hour", "day"]


class AnalyticsParams(TypedDict):
    """Parâmetros de analytics."""

    period: NotRequired[AnalyticsPeriod]


class TimeseriesParams(TypedDict):
    """Parâmetros de série temporal."""

    period: NotRequired[AnalyticsPeriod]
    granularity: NotRequired[Granularity]


class TopTemplatesParams(TypedDict):
    """Parâmetros para templates mais usados."""

    period: NotRequired[AnalyticsPeriod]
    limit: NotRequired[int]


class AnalyticsOverview(TypedDict):
    """Visão geral de analytics."""

    total_sent: int
    total_delivered: int
    total_failed: int
    delivery_rate: float
    period: AnalyticsPeriod


class ChannelAnalytics(TypedDict):
    """Analytics por canal."""

    channel: str
    sent: int
    delivered: int
    failed: int
    delivery_rate: float


class TimeseriesPoint(TypedDict):
    """Ponto de série temporal."""

    timestamp: str
    sent: int
    delivered: int
    failed: int


class TemplateAnalytics(TypedDict):
    """Analytics de template."""

    template_id: str
    template_name: str
    sent: int
    delivered: int
    delivery_rate: float


# ═══════════════════════════════════════════════════
# SMS Provider Types
# ═══════════════════════════════════════════════════

SmsProviderType = Literal["twilio", "zenvia", "custom"]


class TwilioConfig(TypedDict):
    """Configuração da Twilio."""

    account_sid: str
    auth_token: str
    phone_number: str
    messaging_service_sid: NotRequired[str]


class ZenviaConfig(TypedDict):
    """Configuração da Zenvia."""

    api_key: str
    from_: NotRequired[str]


class CustomSmsConfig(TypedDict):
    """Configuração de SMS customizado."""

    webhook_url: str
    headers: NotRequired[dict[str, str]]
    timeout: NotRequired[int]


SmsProviderConfig = TwilioConfig | ZenviaConfig | CustomSmsConfig


class CreateSmsProviderParams(TypedDict):
    """Parâmetros para criar provedor SMS."""

    type: SmsProviderType
    name: str
    config: SmsProviderConfig
    active: NotRequired[bool]
    allowed_regions: NotRequired[list[str]]
    rate_limit_per_minute: NotRequired[int]


class UpdateSmsProviderParams(TypedDict):
    """Parâmetros para atualizar provedor SMS."""

    name: NotRequired[str]
    config: NotRequired[SmsProviderConfig]
    active: NotRequired[bool]
    allowed_regions: NotRequired[list[str]]
    rate_limit_per_minute: NotRequired[int]


class SmsProvider(TypedDict):
    """Objeto de provedor SMS."""

    id: str
    type: SmsProviderType
    name: str
    config_mask: NotRequired[str]
    active: bool
    is_default: bool
    allowed_regions: list[str] | None
    rate_limit_per_minute: int | None
    created_at: str
    updated_at: str


class ValidateSmsProviderParams(TypedDict):
    """Parâmetros para validar provedor SMS."""

    type: SmsProviderType
    config: SmsProviderConfig


class ValidateSmsProviderResult(TypedDict):
    """Resultado de validação de provedor SMS."""

    valid: bool
    message: NotRequired[str]
    errors: NotRequired[dict[str, list[str]]]


class TestSmsProviderParams(TypedDict):
    """Parâmetros para testar provedor SMS."""

    provider_id: NotRequired[str]
    config: NotRequired[CreateSmsProviderParams]
    to: str
    message: NotRequired[str]


class TestSmsProviderResult(TypedDict):
    """Resultado de teste de provedor SMS."""

    success: bool
    message: str
    message_id: NotRequired[str]


# ═══════════════════════════════════════════════════
# SMS Compliance Types
# ═══════════════════════════════════════════════════


class SmsComplianceSettings(TypedDict):
    """Configurações de compliance SMS."""

    allowed_hours_start: str | None
    allowed_hours_end: str | None
    allowed_weekdays: list[int] | None
    respect_national_holidays: bool
    custom_holidays: list[str] | None
    opt_out_message: str | None
    opt_out_keywords: list[str] | None
    opt_out_cooldown_hours: int | None
    opt_in_confirmation_message: str | None


class UpdateSmsComplianceParams(TypedDict):
    """Parâmetros para atualizar compliance SMS."""

    allowed_hours_start: NotRequired[str]
    allowed_hours_end: NotRequired[str]
    allowed_weekdays: NotRequired[list[int]]
    respect_national_holidays: NotRequired[bool]
    custom_holidays: NotRequired[list[str]]
    opt_out_message: NotRequired[str]
    opt_out_keywords: NotRequired[list[str]]
    opt_out_cooldown_hours: NotRequired[int]
    opt_in_confirmation_message: NotRequired[str]


class SmsComplianceAnalytics(TypedDict):
    """Analytics de compliance SMS."""

    period_start: str
    period_end: str
    total_messages: int
    messages_blocked_by_compliance: int
    opt_outs_received: int
    opt_ins_received: int
    violations_by_type: dict[str, int]


SmsComplianceAction = Literal["blocked", "allowed", "opt_out", "opt_in"]


class SmsComplianceLog(TypedDict):
    """Log de compliance SMS."""

    id: str
    message_id: str
    phone: str
    action: SmsComplianceAction
    reason: NotRequired[str]
    created_at: str


class ListComplianceLogsParams(TypedDict):
    """Parâmetros para listar logs de compliance."""

    limit: NotRequired[int]
    cursor: NotRequired[str]
    phone: NotRequired[str]
    action: NotRequired[SmsComplianceAction]
    start_date: NotRequired[str]
    end_date: NotRequired[str]


# ═══════════════════════════════════════════════════
# SMS Consent Types
# ═══════════════════════════════════════════════════

SmsConsentStatus = Literal["opted_in", "opted_out", "pending"]
SmsConsentSource = Literal[
    "manual", "import", "api", "webhook", "opt_out_reply", "opt_in_reply"
]


class SmsConsent(TypedDict):
    """Consentimento SMS."""

    phone: str
    status: SmsConsentStatus
    source: SmsConsentSource
    metadata: NotRequired[dict[str, Any]]
    opted_in_at: str | None
    opted_out_at: str | None
    created_at: str
    updated_at: str


class CreateSmsConsentParams(TypedDict):
    """Parâmetros para criar consentimento SMS."""

    phone: str
    status: NotRequired[SmsConsentStatus]
    source: NotRequired[SmsConsentSource]
    metadata: NotRequired[dict[str, Any]]


class BulkImportSmsConsentParams(TypedDict):
    """Parâmetros para importação em lote de consentimentos."""

    consents: list[CreateSmsConsentParams]


class BulkImportSmsConsentError(TypedDict):
    """Erro individual na importação de consentimento."""

    phone: str
    error: str


class BulkImportSmsConsentResult(TypedDict):
    """Resultado de importação em lote de consentimentos."""

    imported: int
    errors: NotRequired[list[BulkImportSmsConsentError]]


class SmsConsentSummary(TypedDict):
    """Resumo de consentimentos SMS."""

    total: int
    opted_in: int
    opted_out: int
    pending: int
    by_source: dict[str, int]


class ListSmsConsentsParams(TypedDict):
    """Parâmetros para listar consentimentos SMS."""

    limit: NotRequired[int]
    cursor: NotRequired[str]
    phone: NotRequired[str]
    status: NotRequired[SmsConsentStatus]
    source: NotRequired[SmsConsentSource]


# ═══════════════════════════════════════════════════
# Billing Plans
# ═══════════════════════════════════════════════════


class BillingQuotas(TypedDict):
    """Quotas de faturamento."""

    notifications_per_month: int | None
    emails_per_month: int | None
    sms_per_month: int | None
    whatsapp_per_month: int | None
    subscribers_limit: int | None
    templates_limit: int | None
    workflows_limit: int | None
    team_members_limit: int | None


class BillingFeatures(TypedDict):
    """Recursos de faturamento."""

    multi_channel: bool
    advanced_workflows: bool
    custom_webhooks: bool
    dedicated_api: bool
    priority_support: bool
    sla_guarantee: bool
    advanced_lgpd: bool
    sso: bool
    audit_logs: bool


class BillingPlan(TypedDict):
    """Plano de faturamento."""

    name: str
    display_name: str
    description: str | None
    monthly_price_cents: int
    yearly_price_cents: int
    trial_days: int
    quotas: BillingQuotas
    features: BillingFeatures
    available: bool
    sort_order: int


# ═══════════════════════════════════════════════════
# Billing Settings
# ═══════════════════════════════════════════════════

BillingGatewayType = Literal["asaas", "efi"]


class BillingAddress(TypedDict):
    """Endereço de faturamento."""

    street: str
    number: str
    complement: NotRequired[str]
    neighborhood: str
    city: str
    state: str
    zip_code: str
    country: str


class BillingTaxInfo(TypedDict):
    """Informações fiscais."""

    person_type: Literal["individual", "company"]
    document: str
    legal_name: str
    billing_email: str
    address: NotRequired[BillingAddress]


class BillingSettings(TypedDict):
    """Configurações de faturamento."""

    gateway: BillingGatewayType | None
    currency: str
    timezone: str
    due_day: int | None
    tax_info: BillingTaxInfo | None


# ═══════════════════════════════════════════════════
# Subscription
# ═══════════════════════════════════════════════════

SubscriptionStatus = Literal[
    "trial", "active", "past_due", "canceled", "paused", "expired"
]
SubscriptionPeriod = Literal["monthly", "yearly"]


class Subscription(TypedDict):
    """Assinatura."""

    id: str
    plan_name: str
    status: SubscriptionStatus
    period: SubscriptionPeriod
    starts_at: str
    current_period_ends_at: str
    ends_at: str | None
    trial_days_remaining: int | None
    in_trial: bool
    auto_renew: bool
    current_price_cents: int
    created_at: str
    updated_at: str


class SubscribeParams(TypedDict):
    """Parâmetros para assinar."""

    plan_name: str
    period: NotRequired[SubscriptionPeriod]
    payment_method_id: NotRequired[str]
    coupon_code: NotRequired[str]


class ChangePlanParams(TypedDict):
    """Parâmetros para mudar de plano."""

    plan_name: str
    period: NotRequired[SubscriptionPeriod]
    effective_immediately: NotRequired[bool]


class CancelSubscriptionParams(TypedDict):
    """Parâmetros para cancelar assinatura."""

    at_period_end: NotRequired[bool]
    reason: NotRequired[str]


class ReactivateSubscriptionParams(TypedDict):
    """Parâmetros para reativar assinatura."""

    payment_method_id: NotRequired[str]


class CalculateProrationParams(TypedDict):
    """Parâmetros para calcular proration."""

    plan_name: str
    period: NotRequired[SubscriptionPeriod]


class CalculateProrationResult(TypedDict):
    """Resultado de cálculo de proration."""

    current_plan_credit_cents: int
    new_plan_debit_cents: int
    proration_amount_cents: int
    next_billing_date: str


# ═══════════════════════════════════════════════════
# Usage & Quotas
# ═══════════════════════════════════════════════════


class BillingUsageMetrics(TypedDict):
    """Métricas de uso."""

    notifications: int
    emails: int
    sms: int
    whatsapp: int
    subscribers: int
    templates: int
    workflows: int
    team_members: int


class BillingUsagePercentages(TypedDict):
    """Percentuais de uso."""

    notifications: float | None
    emails: float | None
    sms: float | None
    whatsapp: float | None
    subscribers: float | None
    templates: float | None
    workflows: float | None
    team_members: float | None


class BillingUsage(TypedDict):
    """Uso e quotas."""

    period_start: str
    period_end: str
    current: BillingUsageMetrics
    quotas: BillingQuotas
    percentages: BillingUsagePercentages


# ═══════════════════════════════════════════════════
# Invoices
# ═══════════════════════════════════════════════════

InvoiceStatus = Literal[
    "pending", "paid", "overdue", "canceled", "refunded", "processing"
]
PaymentMethodType = Literal["credit_card", "pix", "boleto"]


class Invoice(TypedDict):
    """Fatura."""

    id: str
    subscription_id: str
    status: InvoiceStatus
    amount_cents: int
    amount_paid_cents: int
    currency: str
    description: str
    payment_method: PaymentMethodType | None
    due_date: str
    paid_at: str | None
    boleto_url: str | None
    pix_code: str | None
    pix_qr_code: str | None
    boleto_line: str | None
    boleto_pdf_url: str | None
    created_at: str
    updated_at: str


class ListInvoicesParams(TypedDict):
    """Parâmetros para listar faturas."""

    limit: NotRequired[int]
    cursor: NotRequired[str]
    status: NotRequired[InvoiceStatus]
    start_date: NotRequired[str]
    end_date: NotRequired[str]


# ═══════════════════════════════════════════════════
# Payment Methods
# ═══════════════════════════════════════════════════

CardBrand = Literal[
    "visa",
    "mastercard",
    "amex",
    "elo",
    "hipercard",
    "diners",
    "discover",
    "jcb",
    "aura",
    "unknown",
]
PixKeyType = Literal["cpf", "cnpj", "email", "phone", "random"]


class PaymentMethodCard(TypedDict):
    """Cartão de método de pagamento."""

    brand: CardBrand
    last_four: str
    exp_month: int
    exp_year: int
    holder_name: str


class PaymentMethod(TypedDict):
    """Método de pagamento."""

    id: str
    type: PaymentMethodType
    is_default: bool
    card: PaymentMethodCard | None
    pix_key: str | None
    pix_key_type: PixKeyType | None
    nickname: str | None
    created_at: str
    updated_at: str


class CreateCardParams(TypedDict):
    """Parâmetros para criar cartão."""

    number: str
    holder_name: str
    exp_month: int
    exp_year: int
    cvv: str


class CreatePaymentMethodParams(TypedDict):
    """Parâmetros para criar método de pagamento."""

    type: PaymentMethodType
    card_token: NotRequired[str]
    card: NotRequired[CreateCardParams]
    pix_key: NotRequired[str]
    pix_key_type: NotRequired[PixKeyType]
    nickname: NotRequired[str]
    set_as_default: NotRequired[bool]


class UpdatePaymentMethodParams(TypedDict):
    """Parâmetros para atualizar método de pagamento."""

    nickname: NotRequired[str]
    exp_month: NotRequired[int]
    exp_year: NotRequired[int]


# ═══════════════════════════════════════════════════
# Inbox Embed
# ═══════════════════════════════════════════════════

InboxEmbedTheme = Literal["light", "dark", "auto"]
InboxEmbedPosition = Literal[
    "bottom-right", "bottom-left", "top-right", "top-left"
]
InboxDateFormat = Literal["relative", "absolute", "both"]


class InboxEmbedSettings(TypedDict):
    """Configurações do Inbox Embed."""

    enabled: bool
    theme: InboxEmbedTheme
    position: InboxEmbedPosition
    title: str | None
    primary_color: str | None
    background_color: str | None
    unread_badge_text: str | None
    show_sender_avatar: bool
    show_timestamp: bool
    date_format: InboxDateFormat
    max_notifications: int
    empty_state_text: str | None
    custom_logo_url: str | None
    custom_css: str | None
    embed_key: str
    allowed_domains: list[str]
    created_at: str
    updated_at: str


class UpdateInboxEmbedSettingsParams(TypedDict):
    """Parâmetros para atualizar configurações do Inbox Embed."""

    enabled: NotRequired[bool]
    theme: NotRequired[InboxEmbedTheme]
    position: NotRequired[InboxEmbedPosition]
    title: NotRequired[str]
    primary_color: NotRequired[str]
    background_color: NotRequired[str]
    unread_badge_text: NotRequired[str]
    show_sender_avatar: NotRequired[bool]
    show_timestamp: NotRequired[bool]
    date_format: NotRequired[InboxDateFormat]
    max_notifications: NotRequired[int]
    empty_state_text: NotRequired[str]
    custom_logo_url: NotRequired[str]
    custom_css: NotRequired[str]
    allowed_domains: NotRequired[list[str]]


class RotateEmbedKeyResult(TypedDict):
    """Resultado de rotação de chave de embed."""

    embed_key: str
    old_key_expires_at: str


# ═══════════════════════════════════════════════════
# Public Inbox
# ═══════════════════════════════════════════════════


class InboxNotification(TypedDict):
    """Notificação do inbox público."""

    id: str
    title: str | None
    body: str | None
    action_url: str | None
    read: bool
    image_url: str | None
    category: str | None
    metadata: dict[str, Any] | None
    sent_at: str
    created_at: str


class ListInboxNotificationsParams(TypedDict):
    """Parâmetros para listar notificações do inbox."""

    limit: NotRequired[int]
    cursor: NotRequired[str]
    unread_only: NotRequired[bool]
    category: NotRequired[str]
    start_date: NotRequired[str]
    end_date: NotRequired[str]


class InboxUnreadCountResult(TypedDict):
    """Resultado de contagem de não lidas do inbox."""

    count: int


class MarkInboxReadResult(TypedDict):
    """Resultado de marcar notificação como lida."""

    success: bool
    notification_id: NotRequired[str]


class MarkInboxReadAllResult(TypedDict):
    """Resultado de marcar todas como lidas."""

    success: bool
    marked_count: int
