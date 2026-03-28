"""MCP resources for WhatsApp functionality."""

from typing import Any

from mcp_whatsapp.mcp import get_adapter, mcp


@mcp.resource("whatsapp://status")
def connection_status() -> dict[str, Any]:
    """Get the current connection status of the WhatsApp client.

    Returns:
        dict with connection status information
    """
    adapter = get_adapter()
    result = adapter.get_status()
    return result.to_dict()


@mcp.resource("whatsapp://config")
def config_info() -> dict[str, Any]:
    """Get the current adapter configuration.

    Returns:
        dict with configuration information
    """
    from mcp_whatsapp.mcp import ADAPTER_TYPE

    return {
        "adapter_type": ADAPTER_TYPE,
        "available_adapters": ["whatsapp-business", "pywhatkit"],
    }
