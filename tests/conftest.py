from unittest.mock import MagicMock

import pytest

from mcp_whatsapp import mcp as mcp_module
from mcp_whatsapp.adapters.base import WhatsAppAdapter
from mcp_whatsapp.core.models import MessageResponse, StatusResponse


@pytest.fixture
def mock_adapter():
    """Create a mock WhatsApp adapter."""
    adapter = MagicMock(spec=WhatsAppAdapter)
    adapter.send_message.return_value = MessageResponse(
        success=True, message_id="test-123"
    )
    adapter.send_media.return_value = MessageResponse(
        success=True, message_id="media-123"
    )
    adapter.send_location.return_value = MessageResponse(
        success=True, message_id="loc-123"
    )
    adapter.get_status.return_value = StatusResponse(
        connected=True, adapter="test", phone="+1234567890"
    )
    return adapter


@pytest.fixture
def set_mock_adapter(mock_adapter):
    """Set the mock adapter for tests."""
    mcp_module.set_adapter(mock_adapter)
    yield
    mcp_module._adapter = None
