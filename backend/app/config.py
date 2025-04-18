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

# Remove os import, not needed
from typing import Optional, List
from pydantic import (
    HttpUrl,
    SecretStr,
    computed_field,
    Field,
)  # Import Field for default
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or .env file.
    """

    # Environment Identifier
    ENVIRONMENT: str = "development"

    # PoC Required Variables
    DATABASE_URL: str
    REDIS_URL: str
    LOG_LEVEL: str = "INFO"
    LLM_API_KEY: Optional[SecretStr] = None

    # --- SuperTokens Configuration ---
    SUPERTOKENS_CONNECTION_URI: str
    SUPERTOKENS_API_KEY: SecretStr

    # --- Observability (MVP) ---
    SENTRY_DSN: Optional[str] = None
    POSTHOG_API_KEY: Optional[SecretStr] = None
    OTEL_EXPORTER_OTLP_ENDPOINT: Optional[HttpUrl] = None

    # --- CORS Configuration ---
    # Load CORS_ORIGINS from env/.env, default to proxy address if not set
    CORS_ORIGINS: str = Field(default="http://localhost")
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: str = Field(default="GET,POST,PUT,DELETE,OPTIONS")
    CORS_ALLOW_HEADERS: str = Field(default="*")

    # --- Proxy Header Configuration ---
    # Tell Uvicorn/FastAPI which IPs are trusted to send proxy headers (X-Forwarded-*)
    # Load from env/.env, default to '*' for development ease. Restrict in production.
    FORWARDED_ALLOW_IPS: str = Field(default="*")

    # Compute the CORS_ALLOWED_ORIGINS list from the string
    @computed_field
    def CORS_ALLOWED_ORIGINS(self) -> List[str]:
        """Split the CORS_ORIGINS string into a list."""
        # No need for default here as Field provides it
        return [
            origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()
        ]

    # Parse the CORS_ALLOW_METHODS string into a list
    @computed_field
    def CORS_ALLOWED_METHODS(self) -> List[str]:
        """Split the CORS_ALLOW_METHODS string into a list."""
        # No need for default here as Field provides it
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

# Debug print to confirm FORWARDED_ALLOW_IPS value after loading
print(f"DEBUG - FORWARDED_ALLOW_IPS set to: {settings.FORWARDED_ALLOW_IPS}")
print(
    f"DEBUG - CORS_ALLOWED_ORIGINS set to: {settings.CORS_ALLOWED_ORIGINS}"
)  # Also print CORS origins
