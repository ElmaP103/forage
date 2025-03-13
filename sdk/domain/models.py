from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class EmailVerificationResult:
    """Email verification result data structure."""

    email: str
    score: float
    status: str
    domain: str
    is_disposable: bool
    is_webmail: bool
    is_deliverable: Optional[bool] = None

    def __post_init__(self) -> None:
        """Validate email verification result data."""
        if not isinstance(self.email, str):
            raise TypeError('Email must be a string')
        if not isinstance(self.score, float):
            raise TypeError('Score must be a float')
        if not isinstance(self.status, str):
            raise TypeError('Status must be a string')
