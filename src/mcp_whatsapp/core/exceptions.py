class WhatsAppError(Exception):
    """Base exception for WhatsApp-related errors."""

    pass


class InvalidPhoneNumberError(WhatsAppError):
    """Raised when a phone number is invalid."""

    pass


class MediaNotFoundError(WhatsAppError, FileNotFoundError):
    """Raised when a media file is not found."""

    pass


class ConnectionError(WhatsAppError):
    """Raised when connection to WhatsApp fails."""

    pass


class RateLimitError(WhatsAppError):
    """Raised when rate limit is exceeded."""

    pass


class InvalidMediaTypeError(WhatsAppError):
    """Raised when media type is invalid."""

    pass


class AdapterNotConfiguredError(WhatsAppError, RuntimeError):
    """Raised when adapter is not configured."""

    pass


class EmptyMessageError(WhatsAppError, ValueError):
    """Raised when message content is empty."""

    pass
