class HunterAPIError(Exception):
    """Base exception for Hunter.io API errors."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        """Initialize the exception.

        Args:
            message: Error message
            status_code: HTTP status code if applicable
        """
        super().__init__(message)
        self.status_code = status_code


class APIKeyError(HunterAPIError):
    """Raised when there's an issue with the API key."""
    pass


class RateLimitError(HunterAPIError):
    """Raised when API rate limit is exceeded."""
    pass


class ValidationError(Exception):
    """Raised when there's an issue with input validation."""
    pass
