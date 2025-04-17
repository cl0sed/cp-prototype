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

from typing import Optional, List
from pydantic import HttpUrl, SecretStr, computed_field
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

    # --- SuperTokens Configuration ---
    SUPERTOKENS_CONNECTION_URI: str  # Connection URI for the SuperTokens core
    SUPERTOKENS_API_KEY: SecretStr  # API key for the SuperTokens core

    # --- Observability (MVP) ---
    # These variables are optional for PoC but will be needed for MVP
    # They are defined here to establish the structure for future expansion
    SENTRY_DSN: Optional[str] = None  # Optional: For Sentry error tracking (MVP)
    POSTHOG_API_KEY: Optional[SecretStr] = None  # Optional: For PostHog analytics (MVP)
    OTEL_EXPORTER_OTLP_ENDPOINT: Optional[HttpUrl] = (
        None  # Optional: For OpenTelemetry Exporter (MVP)
    )

    # --- CORS Configuration ---
    # Use a plain string field for CORS origins to avoid Pydantic JSON parsing issues
    CORS_ORIGINS: str = "http://localhost:5173"
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: str = "GET,POST,PUT,DELETE,OPTIONS"
    CORS_ALLOW_HEADERS: str = "*"

    # Compute the CORS_ALLOWED_ORIGINS list from the string
    @computed_field
    def CORS_ALLOWED_ORIGINS(self) -> List[str]:
        """Split the CORS_ORIGINS string into a list."""
        if not self.CORS_ORIGINS:
            return ["http://localhost:5173"]
        return [
            origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()
        ]

    # Parse the CORS_ALLOW_METHODS string into a list
    @computed_field
    def CORS_ALLOWED_METHODS(self) -> List[str]:
        """Split the CORS_ALLOW_METHODS string into a list."""
        if not self.CORS_ALLOW_METHODS:
            return ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
        return [
            method.strip()
            for method in self.CORS_ALLOW_METHODS.split(",")
            if method.strip()
        ]

    # Parse the CORS_ALLOW_HEADERS string into a list
    @computed_field
    def CORS_ALLOWED_HEADERS(self) -> List[str]:
        """Convert the CORS_ALLOW_HEADERS string to a list."""
        if self.CORS_ALLOW_HEADERS == "*":
            return ["*"]
        return [
            header.strip()
            for header in self.CORS_ALLOW_HEADERS.split(",")
            if header.strip()
        ]

    # --- Add other future settings here ---

    # Configure BaseSettings to load from .env file and ignore extra variables
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


# Create a single instance of Settings to be imported by other modules
settings = Settings()
