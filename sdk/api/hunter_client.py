from typing import Dict
import httpx
from urllib.parse import urljoin


class HunterAPIClient:
    """Hunter.io API client implementation."""

    BASE_URL = 'https://api.hunter.io/v2/'

    def __init__(self, api_key: str) -> None:
        """Initialize Hunter API client.

        Args:
            api_key: Hunter.io API key
        """
        self._api_key = api_key
        self._client = httpx.Client(timeout=30.0)

    def verify_email(self, email: str) -> Dict[str, any]:
        """Verify email address using Hunter.io API.

        Args:
            email: Email address to verify

        Returns:
            API response data

        Raises:
            httpx.HTTPError: If API request fails
        """
        params = {
            'email': email,
            'api_key': self._api_key,
        }
        response = self._client.get(
            url=urljoin(self.BASE_URL, 'email-verifier'),
            params=params,
        )
        response.raise_for_status()
        return response.json()['data']
