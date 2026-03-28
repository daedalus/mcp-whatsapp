import os
from unittest.mock import MagicMock, patch

import pytest

from mcp_whatsapp.adapters.pywhatkit import PyWhatKitAdapter
from mcp_whatsapp.adapters.whatsapp_business import WhatsAppBusinessAdapter
from mcp_whatsapp.core.exceptions import (
    AdapterNotConfiguredError,
    EmptyMessageError,
    InvalidPhoneNumberError,
)


class TestPyWhatKitAdapter:
    """Tests for PyWhatKitAdapter."""

    def test_is_configured(self):
        """Test adapter is always configured."""
        adapter = PyWhatKitAdapter()
        assert adapter.is_configured is True

    def test_connect(self):
        """Test connect method."""
        adapter = PyWhatKitAdapter()
        with patch.dict("sys.modules", {"pywhatkit": MagicMock()}):
            adapter.connect()
            assert adapter._connected is True

    def test_send_message_invalid_phone(self):
        """Test sending message with invalid phone."""
        adapter = PyWhatKitAdapter()
        with pytest.raises(InvalidPhoneNumberError):
            adapter.send_message("invalid", "Hello!")

    def test_send_message_empty_message(self):
        """Test sending empty message."""
        adapter = PyWhatKitAdapter()
        with pytest.raises(EmptyMessageError):
            adapter.send_message("+1234567890", "")

    def test_send_message_success(self):
        """Test successful message sending."""
        adapter = PyWhatKitAdapter()
        with patch.dict("sys.modules", {"pywhatkit": MagicMock()}):
            adapter.connect()
            adapter._connected = True
            with patch("mcp_whatsapp.adapters.pywhatkit.pywhatkit"):
                result = adapter.send_message("+1234567890", "Test message")
                assert result.success is True


class TestWhatsAppBusinessAdapter:
    """Tests for WhatsAppBusinessAdapter."""

    def test_is_not_configured_without_env(self):
        """Test adapter is not configured without env vars."""
        adapter = WhatsAppBusinessAdapter()
        assert adapter.is_configured is False

    def test_is_configured_with_env(self):
        """Test adapter is configured with env vars."""
        with patch.dict(
            os.environ,
            {
                "WHATSAPP_PHONE_NUMBER_ID": "12345",
                "WHATSAPP_ACCESS_TOKEN": "token123",
            },
        ):
            adapter = WhatsAppBusinessAdapter()
            assert adapter.is_configured is True

    def test_connect_not_configured(self):
        """Test connect raises when not configured."""
        adapter = WhatsAppBusinessAdapter()
        with pytest.raises(AdapterNotConfiguredError):
            adapter.connect()

    def test_send_message_invalid_phone(self):
        """Test sending message with invalid phone."""
        adapter = WhatsAppBusinessAdapter()
        with pytest.raises(InvalidPhoneNumberError):
            adapter.send_message("invalid", "Hello!")

    def test_send_message_empty_message(self):
        """Test sending empty message."""
        adapter = WhatsAppBusinessAdapter()
        with pytest.raises(EmptyMessageError):
            adapter.send_message("+1234567890", "")

    def test_get_status(self):
        """Test get_status returns correct info."""
        adapter = WhatsAppBusinessAdapter()
        adapter._connected = True
        status = adapter.get_status()
        assert status.connected is True
        assert status.adapter == "whatsapp-business"
