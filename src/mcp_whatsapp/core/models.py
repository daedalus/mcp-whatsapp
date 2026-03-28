from dataclasses import dataclass
from typing import Any


@dataclass
class MessageResponse:
    """Response from sending a message."""

    success: bool
    message_id: str | None = None
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "success": self.success,
            "message_id": self.message_id,
            "error": self.error,
        }


@dataclass
class StatusResponse:
    """Response from getting connection status."""

    connected: bool
    adapter: str
    phone: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "connected": self.connected,
            "adapter": self.adapter,
            "phone": self.phone,
        }
