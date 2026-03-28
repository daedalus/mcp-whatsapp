import os
import re
from typing import Any

from mcp_whatsapp.core.exceptions import (
    EmptyMessageError,
    InvalidMediaTypeError,
    InvalidPhoneNumberError,
    MediaNotFoundError,
)
from mcp_whatsapp.core.models import MessageResponse, StatusResponse

PHONE_REGEX = re.compile(r"^\+?[1-9]\d{6,14}$")
VALID_MEDIA_TYPES = {"image", "audio", "video", "document"}


def _validate_phone(phone: str) -> None:
    """Validate phone number format."""
    if not phone:
        raise InvalidPhoneNumberError("Phone number cannot be empty")
    cleaned = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    if not PHONE_REGEX.match(cleaned):
        raise InvalidPhoneNumberError(
            f"Invalid phone number format: {phone}. "
            "Use international format (e.g., +1234567890)"
        )


def _validate_message(message: str) -> None:
    """Validate message content."""
    if not message or not message.strip():
        raise EmptyMessageError("Message content cannot be empty")


def _validate_media_path(media_path: str) -> None:
    """Validate media file exists and has valid extension."""
    if not os.path.exists(media_path):
        raise MediaNotFoundError(f"Media file not found: {media_path}")

    ext = os.path.splitext(media_path)[1].lower().lstrip(".")
    allowed_extensions = {
        "image": ["jpg", "jpeg", "png", "gif", "webp"],
        "audio": ["mp3", "ogg", "aac", "wav"],
        "video": ["mp4", "3gp", "avi"],
        "document": ["pdf", "doc", "docx", "txt"],
    }

    for media_type, extensions in allowed_extensions.items():
        if ext in extensions:
            return

    raise InvalidMediaTypeError(
        f"Unsupported media type: .{ext}. "
        f"Supported: {', '.join(f'.{e}' for e in sum(allowed_extensions.values(), []))}"
    )


class WhatsAppBusinessAdapter:
    """Adapter for WhatsApp Business API."""

    def __init__(
        self,
        phone_number_id: str | None = None,
        access_token: str | None = None,
        verify_token: str | None = None,
    ) -> None:
        """Initialize the WhatsApp Business API adapter.

        Args:
            phone_number_id: WhatsApp Business phone number ID
            access_token: Facebook access token
            verify_token: Webhook verification token
        """
        self._phone_number_id = phone_number_id or os.getenv("WHATSAPP_PHONE_NUMBER_ID")
        self._access_token = access_token or os.getenv("WHATSAPP_ACCESS_TOKEN")
        self._verify_token = verify_token or os.getenv("WHATSAPP_VERIFY_TOKEN")
        self._client: Any = None
        self._connected = False

    @property
    def is_configured(self) -> bool:
        """Check if adapter is properly configured."""
        return bool(self._phone_number_id and self._access_token)

    def connect(self) -> None:
        """Connect to WhatsApp Business API."""
        if not self.is_configured:
            from mcp_whatsapp.core.exceptions import AdapterNotConfiguredError

            raise AdapterNotConfiguredError(
                "WhatsApp Business adapter not configured. "
                "Set WHATSAPP_PHONE_NUMBER_ID and WHATSAPP_ACCESS_TOKEN environment variables "
                "or pass them to the adapter constructor."
            )

        try:
            from whatsapp_business import WhatsAppBusiness

            self._client = WhatsAppBusiness(
                phone_number_id=self._phone_number_id,
                access_token=self._access_token,
            )
            self._connected = True
        except ImportError:
            from mcp_whatsapp.core.exceptions import WhatsAppError

            raise WhatsAppError(
                "whatsapp-business package not installed. "
                "Install with: pip install mcp-whatsapp[whatsapp-business]"
            )

    def disconnect(self) -> None:
        """Disconnect from WhatsApp Business API."""
        self._client = None
        self._connected = False

    def send_message(self, phone: str, message: str) -> MessageResponse:
        """Send a text message using WhatsApp Business API."""
        _validate_phone(phone)
        _validate_message(message)

        if not self._connected:
            self.connect()

        try:
            result = self._client.send_message(
                recipient=phone,
                message=message,
            )
            return MessageResponse(
                success=True,
                message_id=result.get("messages", [{}])[0].get("id"),
            )
        except Exception as e:  # noqa: BLE001
            return MessageResponse(success=False, error=str(e))

    def send_media(
        self, phone: str, media_path: str, caption: str | None = None
    ) -> MessageResponse:
        """Send media using WhatsApp Business API."""
        _validate_phone(phone)
        _validate_media_path(media_path)

        if not self._connected:
            self.connect()

        try:
            media_type = self._get_media_type(media_path)
            result = self._client.send_media(
                recipient=phone,
                media_path=media_path,
                media_type=media_type,
                caption=caption,
            )
            return MessageResponse(
                success=True,
                message_id=result.get("messages", [{}])[0].get("id"),
            )
        except Exception as e:  # noqa: BLE001
            return MessageResponse(success=False, error=str(e))

    def send_location(
        self,
        phone: str,
        latitude: float,
        longitude: float,
        title: str | None = None,
    ) -> MessageResponse:
        """Send a location using WhatsApp Business API."""
        _validate_phone(phone)

        if not self._connected:
            self.connect()

        try:
            location_data: dict[str, float | str] = {
                "latitude": latitude,
                "longitude": longitude,
            }
            if title:
                location_data["name"] = title

            result = self._client.send_message(
                recipient=phone,
                message_type="location",
                location=location_data,
            )
            return MessageResponse(
                success=True,
                message_id=result.get("messages", [{}])[0].get("id"),
            )
        except Exception as e:  # noqa: BLE001
            return MessageResponse(success=False, error=str(e))

    def get_status(self) -> StatusResponse:
        """Get connection status."""
        return StatusResponse(
            connected=self._connected,
            adapter="whatsapp-business",
            phone=self._phone_number_id,
        )

    def _get_media_type(self, media_path: str) -> str:
        """Determine media type from file extension."""
        ext = os.path.splitext(media_path)[1].lower().lstrip(".")
        if ext in ["jpg", "jpeg", "png", "gif", "webp"]:
            return "image"
        if ext in ["mp3", "ogg", "aac", "wav"]:
            return "audio"
        if ext in ["mp4", "3gp", "avi"]:
            return "video"
        return "document"
