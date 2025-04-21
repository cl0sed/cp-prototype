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
from pydantic import (
    HttpUrl,
    SecretStr,
    computed_field,
    Field,
)  # Import Field for default
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache  # Import lru_cache


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
    LLM_MODEL: str = "google/gemini-2.5-flash-preview"  # Default LLM model
    LLM_API_URL: Optional[HttpUrl] = None  # Optional custom API URL

    # --- SuperTokens Configuration ---
    SUPERTOKENS_CONNECTION_URI: str
    SUPERTOKENS_API_KEY: SecretStr

    # --- LLM Configuration (Haystack) ---

    # --- Chat Configuration ---
    CHAT_PIPELINE_TAG: str = "chat_v1"  # Default pipeline version tag

    # --- Prompt and Tool Versioning Configuration ---
    DEFAULT_CHAT_PIPELINE_TAG: str = Field(
        default="dev"
    )  # Required default tag for the chat pipeline
    PIPELINE_TAGS_CONFIG_PATH: str = Field(
        default="./pipeline-tags.yaml"
    )  # Path to the pipeline tags override YAML file
    DEFAULT_PROMPT_VERSION: str = Field(
        default="v1"
    )  # Default prompt version to use if no override is found

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

    # --- Application URLs ---
    # Base URL for the application (used for SuperTokens configuration)
    APP_BASE_URL: str = Field(default="http://localhost")

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

    # Method to load prompt configuration
    @computed_field
    def PROMPT_CONFIG(self) -> dict:
        """Loads the prompt configuration from prompts.yaml."""
        # NOTE: This requires PyYAML dependency
        import yaml
        import logging  # Added logging import

        try:
            with open("prompts.yaml", "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logging.warning(
                "prompts.yaml not found. Using empty prompt config."
            )  # Replaced print with logging
            return {}
        except yaml.YAMLError as e:
            logging.error(
                f"Failed to parse prompts.yaml: {e}"
            )  # Replaced print with logging
            return {}


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Cached dependency for getting settings."""
    # Instantiate Settings directly here, relying on lru_cache for singleton behavior
    return Settings()
