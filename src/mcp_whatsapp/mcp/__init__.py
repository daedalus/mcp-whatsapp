__all__ = ["mcp", "tools", "resources"]

import os

import fastmcp

from mcp_whatsapp.adapters import (
    PyWhatKitAdapter,
    WhatsAppAdapter,
    WhatsAppBusinessAdapter,
)

mcp = fastmcp.FastMCP("mcp-whatsapp")

ADAPTER_TYPE = os.getenv("WHATSAPP_ADAPTER", "pywhatkit")

_adapter: WhatsAppAdapter | None = None


def get_adapter() -> WhatsAppAdapter:
    """Get the configured WhatsApp adapter."""
    global _adapter
    if _adapter is not None:
        return _adapter

    if ADAPTER_TYPE == "whatsapp-business":
        _adapter = WhatsAppBusinessAdapter()
    else:
        _adapter = PyWhatKitAdapter()

    return _adapter


def set_adapter(adapter: WhatsAppAdapter) -> None:
    """Set a custom adapter (useful for testing)."""
    global _adapter
    _adapter = adapter


from mcp_whatsapp.mcp import resources, tools  # noqa: E402, F401
