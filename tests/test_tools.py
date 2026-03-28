
from mcp_whatsapp.core.exceptions import (
    EmptyMessageError,
    InvalidPhoneNumberError,
    MediaNotFoundError,
)
from mcp_whatsapp.mcp import tools


class TestSendMessage:
    """Tests for send_message tool."""

    def test_send_message_success(self, set_mock_adapter, mock_adapter):
        """Test successful message sending."""
        result = tools.send_message("+1234567890", "Hello!")
        assert result["success"] is True
        assert result["message_id"] == "test-123"

    def test_send_message_invalid_phone(self, set_mock_adapter, mock_adapter):
        """Test sending to invalid phone number."""
        mock_adapter.send_message.side_effect = InvalidPhoneNumberError(
            "Invalid phone number"
        )
        result = tools.send_message("invalid", "Hello!")
        assert result["success"] is False
        assert "Invalid phone number" in result["error"]

    def test_send_message_empty_message(self, set_mock_adapter, mock_adapter):
        """Test sending empty message."""
        mock_adapter.send_message.side_effect = EmptyMessageError(
            "Message cannot be empty"
        )
        result = tools.send_message("+1234567890", "")
        assert result["success"] is False
        assert "empty" in result["error"].lower()


class TestSendMedia:
    """Tests for send_media tool."""

    def test_send_media_success(self, set_mock_adapter, mock_adapter):
        """Test successful media sending."""
        result = tools.send_media("+1234567890", "/path/to/image.jpg", "Caption")
        assert result["success"] is True
        assert result["message_id"] == "media-123"

    def test_send_media_not_found(self, set_mock_adapter, mock_adapter):
        """Test sending non-existent media."""
        mock_adapter.send_media.side_effect = MediaNotFoundError("File not found")
        result = tools.send_media("+1234567890", "/nonexistent/file.jpg")
        assert result["success"] is False
        assert "not found" in result["error"].lower()


class TestSendLocation:
    """Tests for send_location tool."""

    def test_send_location_success(self, set_mock_adapter, mock_adapter):
        """Test successful location sending."""
        result = tools.send_location("+1234567890", 40.7128, -74.006, "NYC")
        assert result["success"] is True
        assert result["message_id"] == "loc-123"


class TestConnectWhatsApp:
    """Tests for connect_whatsapp tool."""

    def test_connect_success(self, set_mock_adapter, mock_adapter):
        """Test successful connection."""
        result = tools.connect_whatsapp()
        assert result["success"] is True


class TestDisconnectWhatsApp:
    """Tests for disconnect_whatsapp tool."""

    def test_disconnect_success(self, set_mock_adapter, mock_adapter):
        """Test successful disconnection."""
        result = tools.disconnect_whatsapp()
        assert result["success"] is True
