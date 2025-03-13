

from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel, Field


class APIConfig(BaseModel):
    """API configuration."""

    base_url: str = Field(
        default='https://api.hunter.io/v2/',
        description='Base URL for the API',
    )
    timeout: float = Field(
        default=30.0,
        description='Request timeout in seconds',
    )
    max_retries: int = Field(
        default=3,
        description='Maximum number of retry attempts',
    )
    retry_delay: float = Field(
        default=1.0,
        description='Initial delay between retries in seconds',
    )
    retry_backoff: float = Field(
        default=2.0,
        description='Multiplier for delay after each retry',
    )


class RateLimitConfig(BaseModel):
    """Rate limiting configuration."""

    max_requests: int = Field(
        default=100,
        description='Maximum number of requests allowed',
    )
    time_window: int = Field(
        default=60,
        description='Time window in seconds',
    )


class StorageConfig(BaseModel):
    """Storage configuration."""

    ttl: int = Field(
        default=3600,
        description='Time-to-live for cached results in seconds',
    )


@dataclass
class Config:
    """Main configuration class."""

    api: APIConfig = APIConfig()
    rate_limit: RateLimitConfig = RateLimitConfig()
    storage: StorageConfig = StorageConfig()
    api_key: Optional[str] = None

    @classmethod
    def from_env(cls) -> 'Config':
        """Create configuration from environment variables.

        Returns:
            Config instance
        """
        import os
        from dotenv import load_dotenv

        load_dotenv()
        return cls(
            api_key=os.getenv('HUNTER_API_KEY'),
        ) 