"""Recursos do SDK Notifica."""

from .analytics import Analytics
from .api_keys import ApiKeys
from .audit import Audit
from .billing import Billing
from .channels import Channels
from .domains import Domains
from .inbox import Inbox
from .inbox_embed import InboxEmbed
from .notifications import Notifications
from .sms import Sms
from .subscribers import Subscribers
from .templates import Templates
from .webhooks import Webhooks
from .workflows import Workflows

__all__ = [
    "Analytics",
    "ApiKeys",
    "Audit",
    "Billing",
    "Channels",
    "Domains",
    "Inbox",
    "InboxEmbed",
    "Notifications",
    "Sms",
    "Subscribers",
    "Templates",
    "Webhooks",
    "Workflows",
]
