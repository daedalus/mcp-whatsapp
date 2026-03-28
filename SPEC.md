# SPEC.md — mcp-whatsapp

## Purpose

An MCP (Model Context Protocol) server that exposes WhatsApp bot functionality, supporting multiple WhatsApp client libraries (whatsapp-business-python and pywhatkit) through a unified adapter interface.

## Scope

### In Scope
- MCP server exposing WhatsApp messaging tools
- Support for whatsapp-business-python (WhatsApp Business API)
- Support for pywhatkit (WhatsApp Web)
- Send text messages
- Send media (images, documents)
- Receive and process incoming messages
- Unified adapter pattern for library-agnostic operations

### Not In Scope
- Message history persistence (external DB required)
- WhatsApp Business API account setup
- Browser automation for pywhatkit
- Voice/video calling
- Group management

## Public API / Interface

### MCP Tools

```python
@mcp.tool()
def send_message(phone: str, message: str) -> dict:
    """Send a text message to a phone number."""
    ...

@mcp.tool()
def send_media(phone: str, media_path: str, caption: str | None = None) -> dict:
    """Send media (image, document) to a phone number."""
    ...

@mcp.tool()
def send_location(phone: str, latitude: float, longitude: float, title: str | None = None) -> dict:
    """Send a location to a phone number."""
    ...

@mcp.resource("whatsapp://status")
def connection_status() -> dict:
    """Get the current connection status of the WhatsApp client."""
    ...
```

### Adapter Interface

```python
class WhatsAppAdapter(Protocol):
    def send_message(self, phone: str, message: str) -> dict: ...
    def send_media(self, phone: str, media_path: str, caption: str | None = None) -> dict: ...
    def send_location(self, phone: str, latitude: float, longitude: float, title: str | None = None) -> dict: ...
    def get_status(self) -> dict: ...
    def connect(self) -> None: ...
    def disconnect(self) -> None: ...
```

## Data Formats

### Phone Numbers
- Format: International format with country code (e.g., "+1234567890")
- Must not include special characters or spaces

### Message Response
```python
{
    "success": bool,
    "message_id": str | None,
    "error": str | None
}
```

### Status Response
```python
{
    "connected": bool,
    "adapter": str,
    "phone": str | None
}
```

## Edge Cases

1. Invalid phone number format - raise ValueError
2. Media file not found - raise FileNotFoundError
3. Network timeout - raise ConnectionError with retry option
4. WhatsApp API rate limiting - raise RateLimitError
5. Invalid media type - raise ValueError
6. Adapter not configured - raise RuntimeError
7. Empty message content - raise ValueError
8. Phone number too long/short - raise ValueError

## Performance & Constraints

- Async operations for non-blocking message sending
- Maximum media file size: 16MB (WhatsApp Business API limit)
- Connection timeout: 30 seconds
- Request timeout: 60 seconds
