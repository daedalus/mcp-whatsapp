import os
import re

from mcp_whatsapp.core.exceptions import (
    EmptyMessageError,
    InvalidPhoneNumberError,
    WhatsAppError,
)
from mcp_whatsapp.core.models import MessageResponse, StatusResponse

PHONE_REGEX = re.compile(r"^\+?[1-9]\d{6,14}$")


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


class PyWhatKitAdapter:
    """Adapter for pywhatkit (WhatsApp Web)."""

    def __init__(self, wait_time: int = 20, tab_close: bool = False) -> None:
        """Initialize the pywhatkit adapter.

        Args:
            wait_time: Time to wait for WhatsApp Web to load (seconds)
            tab_close: Whether to close the tab after sending
        """
        self._wait_time = wait_time
        self._tab_close = tab_close
        self._connected = False

    @property
    def is_configured(self) -> bool:
        """Check if adapter is configured (always true for pywhatkit)."""
        return True

    def connect(self) -> None:
        """Initialize pywhatkit."""
        try:
            import pywhatkit  # noqa: F401

            self._connected = True
        except ImportError:
            raise WhatsAppError(
                "pywhatkit package not installed. "
                "Install with: pip install mcp-whatsapp[pywhatkit]"
            )

    def disconnect(self) -> None:
        """Disconnect (no-op for pywhatkit)."""
        self._connected = False

    def send_message(self, phone: str, message: str) -> MessageResponse:
        """Send a text message using pywhatkit."""
        _validate_phone(phone)
        _validate_message(message)

        if not self._connected:
            self.connect()

        try:
            import pywhatkit

            cleaned_phone = phone.replace("+", "").replace(" ", "")
            pywhatkit.sendwhatmsg_instantly(
                phone_no=cleaned_phone,
                message=message,
                wait_time=self._wait_time,
                tab_close=self._tab_close,
            )
            return MessageResponse(
                success=True,
                message_id=f"pywhatkit-{cleaned_phone}-{hash(message)}",
            )
        except Exception as e:  # noqa: BLE001
            return MessageResponse(success=False, error=str(e))

    def send_media(
        self, phone: str, media_path: str, caption: str | None = None
    ) -> MessageResponse:
        """Send media using pywhatkit.

        Note: pywhatkit has limited media support. This sends the caption as a text
        message first, then attempts to send media.
        """

        _validate_phone(phone)

        if not os.path.exists(media_path):
            return MessageResponse(
                success=False, error=f"Media file not found: {media_path}"
            )

        if not self._connected:
            self.connect()

        try:
            import pywhatkit

            cleaned_phone = phone.replace("+", "").replace(" ", "")

            if caption:
                pywhatkit.sendwhatmsg_instantly(
                    phone_no=cleaned_phone,
                    message=caption,
                    wait_time=self._wait_time,
                    tab_close=self._tab_close,
                )

            pywhatkit.send_media(
                phone_no=cleaned_phone,
                media_path=media_path,
            )
            return MessageResponse(
                success=True,
                message_id=f"pywhatkit-media-{cleaned_phone}-{hash(media_path)}",
            )
        except AttributeError:
            return MessageResponse(
                success=False,
                error="pywhatkit does not support send_media. "
                "Consider using whatsapp-business for media sending.",
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
        """Send a location using pywhatkit.

        Note: pywhatkit does not natively support location. This sends a Google Maps
        link as a text message.
        """
        _validate_phone(phone)

        if not self._connected:
            self.connect()

        maps_url = f"https://maps.google.com/?q={latitude},{longitude}"
        message = maps_url
        if title:
            message = f"{title}\n{maps_url}"

        return self.send_message(phone, message)

    def get_status(self) -> StatusResponse:
        """Get connection status."""
        return StatusResponse(
            connected=self._connected,
            adapter="pywhatkit",
            phone=None,
        )
