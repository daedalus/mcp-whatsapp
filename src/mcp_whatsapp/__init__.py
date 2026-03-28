__version__ = "0.1.0"
__all__ = ["mcp", "WhatsAppAdapter", "WhatsAppBusinessAdapter", "PyWhatKitAdapter"]

from typing import TYPE_CHECKING

from .adapters.base import WhatsAppAdapter
from .adapters.pywhatkit import PyWhatKitAdapter
from .adapters.whatsapp_business import WhatsAppBusinessAdapter
from .core.models import MessageResponse, StatusResponse

if TYPE_CHECKING:
    from .mcp import resources, tools
