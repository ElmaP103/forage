from typing import Dict, Optional, TypeVar, Generic

T = TypeVar('T')

class MemoryStorage(Generic[T]):
    """In-memory storage implementation."""

    def __init__(self) -> None:
        """Initialize empty storage."""
        self._storage: Dict[str, T] = {}

    def save(self, key: str, value: T) -> None:
        """Save value to storage.

        Args:
            key: Unique identifier for the value
            value: Data to store
        """
        self._storage[key] = value

    def get(self, key: str) -> Optional[T]:
        """Retrieve value from storage.

        Args:
            key: Unique identifier for the value

        Returns:
            Stored value or None if not found
        """
        return self._storage.get(key)

    def delete(self, key: str) -> None:
        """Remove value from storage.

        Args:
            key: Unique identifier for the value
        """
        self._storage.pop(key, None)

    def list_all(self) -> Dict[str, T]:
        """Get all stored values.

        Returns:
            Dictionary of all stored key-value pairs
        """
        return self._storage.copy()