"""
Global settings instance to be imported and used throughout the application.

Example usage:
```python
from app.config import settings

# Use settings in your code
log_level = settings.LOG_LEVEL
database_url = settings.DATABASE_URL
```

IMPORTANT NOTES:
1. Always use SecretStr for sensitive values to prevent accidental logging
2. For PoC development, only the core variables need to be set
3. Optional MVP variables don't need values during PoC, but the structure is ready
4. For deployed environments (staging/production), all settings MUST be provided
   via environment variables injected securely, NOT from .env files
"""

from typing import Optional
from pydantic import HttpUrl, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or .env file.

    This class defines all configuration parameters used throughout the application.
    Values are loaded with the following precedence:
    1. Environment variables
    2. .env file (for local development)
    3. Default values defined here

    For production deployments, ALL values should be provided via environment
    variables injected securely (e.g., from a secrets manager), NOT from .env files.
    """

    # Environment Identifier
    ENVIRONMENT: str = "development"  # Can be "development", "staging", "production"

    # PoC Required Variables
    DATABASE_URL: str  # PostgreSQL connection string
    REDIS_URL: str  # Redis connection string
    LOG_LEVEL: str = "INFO"  # Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    LLM_API_KEY: Optional[SecretStr] = (
        None  # API key for LLM provider, using SecretStr for security
    )

    # --- Observability (MVP) ---
    # These variables are optional for PoC but will be needed for MVP
    # They are defined here to establish the structure for future expansion
    SENTRY_DSN: Optional[str] = None  # Optional: For Sentry error tracking (MVP)
    POSTHOG_API_KEY: Optional[SecretStr] = None  # Optional: For PostHog analytics (MVP)
    OTEL_EXPORTER_OTLP_ENDPOINT: Optional[HttpUrl] = (
        None  # Optional: For OpenTelemetry Exporter (MVP)
    )

    # --- Add other future settings here ---

    # Configure BaseSettings to load from .env file and ignore extra variables
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


# Create a single instance of Settings to be imported by other modules
settings = Settings()
