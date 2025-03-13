import time
from typing import Dict, Generic, Optional, TypeVar

T = TypeVar('T')


class TTLStorage(Generic[T]):
    """Storage with Time-To-Live support."""

    def __init__(
        self,
        ttl: int,
        storage: Optional[Dict[str, tuple[T, float]]] = None,
    ) -> None:
        """Initialize TTL storage.

        Args:
            ttl: Time-to-live in seconds
            storage: Optional initial storage dictionary
        """
        self.ttl = ttl
        self._storage: Dict[str, tuple[T, float]] = storage or {}

    def save(self, key: str, value: T) -> None:
        """Save value with current timestamp.

        Args:
            key: Unique identifier
            value: Value to store
        """
        self._storage[key] = (value, time.time())

    def get(self, key: str) -> Optional[T]:
        """Get value if not expired.

        Args:
            key: Unique identifier

        Returns:
            Stored value or None if not found or expired
        """
        if key not in self._storage:
            return None

        value, timestamp = self._storage[key]
        if time.time() - timestamp > self.ttl:
            del self._storage[key]
            return None

        return value

    def delete(self, key: str) -> None:
        """Delete value from storage.

        Args:
            key: Unique identifier
        """
        self._storage.pop(key, None)

    def clear_expired(self) -> None:
        """Remove all expired entries."""
        current_time = time.time()
        self._storage = {
            k: v for k, v in self._storage.items()
            if current_time - v[1] <= self.ttl
        }

    def get_all(self) -> Dict[str, T]:
        """Get all non-expired values.

        Returns:
            Dictionary of all valid key-value pairs
        """
        self.clear_expired()
        return {k: v[0] for k, v in self._storage.items()}
