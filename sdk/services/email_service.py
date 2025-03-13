import re
from typing import Optional

from sdk.api.exceptions import ValidationError
from sdk.api.hunter_client import HunterAPIClient
from sdk.domain.models import EmailVerificationResult
from sdk.storage.memory_storage import MemoryStorage


class EmailVerificationService:

    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

    def __init__(
        self,
        api_client: HunterAPIClient,
        storage: MemoryStorage[EmailVerificationResult],
    ) -> None:
        """Initialize email verification service.

        Args:
            api_client: Hunter API client instance
            storage: Storage instance for verification results
        """
        self._api_client = api_client
        self._storage = storage

    def _validate_email(self, email: str) -> None:
        """Validate email format.

        Args:
            email: Email address to validate

        Raises:
            ValidationError: If email format is invalid
        """
        if not isinstance(email, str):
            raise ValidationError('Email must be a string')
        if not email:
            raise ValidationError('Email cannot be empty')
        if not self.EMAIL_PATTERN.match(email):
            raise ValidationError('Invalid email format')

    def verify_email(self, email: str) -> EmailVerificationResult:
        """Verify email and store result.

        Args:
            email: Email address to verify

        Returns:
            Email verification result

        Raises:
            ValidationError: If email format is invalid
        """
        self._validate_email(email)
        
        cached_result = self._storage.get(email)
        if cached_result is not None:
            return cached_result

        api_result = self._api_client.verify_email(email)
        verification_result = EmailVerificationResult(
            email=api_result.get('email', email),
            score=float(api_result.get('score', 0)),
            status=api_result.get('status', 'unknown'),
            domain=api_result.get('domain', email.split('@')[-1]),
            is_disposable=api_result.get('disposable', False),
            is_webmail=api_result.get('webmail', False),
            is_deliverable=api_result.get('deliverable'),
        )
        
        self._storage.save(email, verification_result)
        return verification_result

    def get_verification_result(
        self,
        email: str,
    ) -> Optional[EmailVerificationResult]:
        """Retrieve stored verification result.

        Args:
            email: Email address to look up

        Returns:
            Stored verification result or None if not found

        Raises:
            ValidationError: If email format is invalid
        """
        self._validate_email(email)
        return self._storage.get(email)