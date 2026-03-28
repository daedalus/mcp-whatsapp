from typing import Protocol

from mcp_whatsapp.core.models import MessageResponse, StatusResponse


class WhatsAppAdapter(Protocol):
    """Protocol defining the interface for WhatsApp adapters."""

    def send_message(self, phone: str, message: str) -> MessageResponse:
        """Send a text message to a phone number.

        Args:
            phone: Phone number in international format (e.g., "+1234567890")
            message: Text message to send

        Returns:
            MessageResponse with success status and message_id or error
        """
        ...

    def send_media(
        self, phone: str, media_path: str, caption: str | None = None
    ) -> MessageResponse:
        """Send media (image, document) to a phone number.

        Args:
            phone: Phone number in international format
            media_path: Path to the media file
            caption: Optional caption for the media

        Returns:
            MessageResponse with success status and message_id or error
        """
        ...

    def send_location(
        self,
        phone: str,
        latitude: float,
        longitude: float,
        title: str | None = None,
    ) -> MessageResponse:
        """Send a location to a phone number.

        Args:
            phone: Phone number in international format
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            title: Optional title for the location

        Returns:
            MessageResponse with success status and message_id or error
        """
        ...

    def get_status(self) -> StatusResponse:
        """Get the current connection status.

        Returns:
            StatusResponse with connection status information
        """
        ...

    def connect(self) -> None:
        """Connect to WhatsApp service."""
        ...

    def disconnect(self) -> None:
        """Disconnect from WhatsApp service."""
        ...
