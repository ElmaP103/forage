import time
from datetime import datetime, timedelta


class RateLimiter:
    """Rate limiter implementation."""

    def __init__(
        self,
        max_requests: int,
        time_window: int,
    ) -> None:
        """Initialize rate limiter.

        Args:
            max_requests: Maximum number of requests allowed
            time_window: Time window in seconds
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests: list[datetime] = []

    def acquire(self) -> bool:
        """Try to acquire a request slot.

        Returns:
            True if request is allowed, False otherwise
        """
        now = datetime.now()
        self.requests = [
            req_time for req_time in self.requests
            if now - req_time < timedelta(seconds=self.time_window)
        ]

        if len(self.requests) >= self.max_requests:
            return False

        self.requests.append(now)
        return True

    def wait(self) -> None:
        """Wait until a request slot is available."""
        while not self.acquire():
            time.sleep(0.1)
