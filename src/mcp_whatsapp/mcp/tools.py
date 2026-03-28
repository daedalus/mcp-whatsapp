"""MCP tools for WhatsApp functionality."""

from typing import Any

from mcp_whatsapp.core.exceptions import (
    AdapterNotConfiguredError,
    EmptyMessageError,
    InvalidPhoneNumberError,
    MediaNotFoundError,
    WhatsAppError,
)
from mcp_whatsapp.mcp import get_adapter, mcp


@mcp.tool()
def send_message(phone: str, message: str) -> dict[str, Any]:
    """Send a text message to a phone number.

    Args:
        phone: Phone number in international format (e.g., "+1234567890")
        message: Text message to send

    Returns:
        dict with success status, message_id, and optional error
    """
    try:
        adapter = get_adapter()
        result = adapter.send_message(phone, message)
        return result.to_dict()
    except (InvalidPhoneNumberError, EmptyMessageError) as e:
        return {"success": False, "error": str(e)}
    except AdapterNotConfiguredError as e:
        return {"success": False, "error": str(e)}
    except WhatsAppError as e:
        return {"success": False, "error": f"WhatsApp error: {e}"}
    except Exception as e:  # noqa: BLE001
        return {"success": False, "error": f"Unexpected error: {e}"}


@mcp.tool()
def send_media(
    phone: str, media_path: str, caption: str | None = None
) -> dict[str, Any]:
    """Send media (image, document) to a phone number.

    Args:
        phone: Phone number in international format (e.g., "+1234567890")
        media_path: Path to the media file
        caption: Optional caption for the media

    Returns:
        dict with success status, message_id, and optional error
    """
    try:
        adapter = get_adapter()
        result = adapter.send_media(phone, media_path, caption)
        return result.to_dict()
    except InvalidPhoneNumberError as e:
        return {"success": False, "error": str(e)}
    except MediaNotFoundError as e:
        return {"success": False, "error": str(e)}
    except AdapterNotConfiguredError as e:
        return {"success": False, "error": str(e)}
    except WhatsAppError as e:
        return {"success": False, "error": f"WhatsApp error: {e}"}
    except Exception as e:  # noqa: BLE001
        return {"success": False, "error": f"Unexpected error: {e}"}


@mcp.tool()
def send_location(
    phone: str, latitude: float, longitude: float, title: str | None = None
) -> dict[str, Any]:
    """Send a location to a phone number.

    Args:
        phone: Phone number in international format (e.g., "+1234567890")
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        title: Optional title for the location

    Returns:
        dict with success status, message_id, and optional error
    """
    try:
        adapter = get_adapter()
        result = adapter.send_location(phone, latitude, longitude, title)
        return result.to_dict()
    except InvalidPhoneNumberError as e:
        return {"success": False, "error": str(e)}
    except AdapterNotConfiguredError as e:
        return {"success": False, "error": str(e)}
    except WhatsAppError as e:
        return {"success": False, "error": f"WhatsApp error: {e}"}
    except Exception as e:  # noqa: BLE001
        return {"success": False, "error": f"Unexpected error: {e}"}


@mcp.tool()
def connect_whatsapp() -> dict[str, Any]:
    """Connect to the WhatsApp service.

    Returns:
        dict with success status and optional error
    """
    try:
        adapter = get_adapter()
        adapter.connect()
        return {"success": True}
    except AdapterNotConfiguredError as e:
        return {"success": False, "error": str(e)}
    except WhatsAppError as e:
        return {"success": False, "error": f"WhatsApp error: {e}"}
    except Exception as e:  # noqa: BLE001
        return {"success": False, "error": f"Unexpected error: {e}"}


@mcp.tool()
def disconnect_whatsapp() -> dict[str, Any]:
    """Disconnect from the WhatsApp service.

    Returns:
        dict with success status and optional error
    """
    try:
        adapter = get_adapter()
        adapter.disconnect()
        return {"success": True}
    except WhatsAppError as e:
        return {"success": False, "error": f"WhatsApp error: {e}"}
    except Exception as e:  # noqa: BLE001
        return {"success": False, "error": f"Unexpected error: {e}"}
