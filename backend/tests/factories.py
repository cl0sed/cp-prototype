"""
Test factories for the AI Video Creation Platform.
"""

import factory
import uuid
import datetime
from pydantic import SecretStr  # Import SecretStr for optional secret fields

from app.db.models import (
    User,
    ChatMessage,
    Video,
    EvaluationResult,
    BackgroundJob,
)
from app.config import Settings  # Import Settings model


class UserFactory(factory.Factory):
    class Meta:
        model = User  # Associate with the User model

    id = factory.LazyFunction(uuid.uuid4)
    email = factory.Sequence(lambda n: f"testuser{n}@example.com")
    role = "user"  # Default role


class ChatMessageFactory(factory.Factory):
    class Meta:
        model = ChatMessage  # Associate with the ChatMessage model

    id = factory.LazyFunction(uuid.uuid4)
    user_id = factory.LazyFunction(uuid.uuid4)  # Default, can be overridden
    session_id = factory.LazyFunction(uuid.uuid4)  # Default, can be overridden
    role = "user"  # Default role
    content = factory.Sequence(lambda n: f"Test message {n}")
    timestamp = factory.LazyFunction(datetime.datetime.now)


class SettingsFactory(factory.Factory):
    class Meta:
        model = Settings  # Associate with the Settings model

    # Provide default test values for required settings
    # Use an in-memory SQLite database for faster and simpler tests
    DATABASE_URL = "sqlite+aiosqlite:///./test.db"
    REDIS_URL = "redis://localhost:6379/0"
    LOG_LEVEL = "INFO"
    LLM_API_KEY = SecretStr("fake-llm-api-key")
    LLM_MODEL = "fake-llm-model"
    LLM_API_URL = "http://localhost:8000/test-llm"

    # SuperTokens Configuration
    SUPERTOKENS_CONNECTION_URI = "http://localhost:3567"
    SUPERTOKENS_API_KEY = SecretStr("testapikey")

    # Chat Configuration
    CHAT_PIPELINE_TAG = "chat_v1"
    DEFAULT_CHAT_PIPELINE_TAG = "dev"

    # Prompt and Tool Versioning Configuration
    PIPELINE_TAGS_CONFIG_PATH = (
        "./test-pipeline-tags.yaml"  # Use a test specific config path
    )
    DEFAULT_PROMPT_VERSION = "v1"

    # Observability (Optional for tests, provide defaults)
    SENTRY_DSN = None
    POSTHOG_API_KEY = None
    OTEL_EXPORTER_OTLP_ENDPOINT = None

    # CORS Configuration (Provide defaults matching app.config)
    CORS_ORIGINS = "http://localhost:5173,http://127.0.0.1:5173"
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOW_METHODS = "GET,POST,PUT,DELETE,OPTIONS"
    CORS_ALLOW_HEADERS = "*"

    # Proxy Header Configuration (Provide defaults matching app.config)
    FORWARDED_ALLOW_IPS = "*"

    # Application URLs (Provide defaults matching app.config)
    APP_BASE_URL = "http://localhost"

    # Note: Computed fields like CORS_ALLOWED_ORIGINS are handled by Pydantic
    # when SettingsFactory.build() creates a real Settings instance.
    # PROMPT_CONFIG computed field will attempt to load the test config file.


class VideoFactory(factory.Factory):
    class Meta:
        model = Video

    id = factory.LazyFunction(uuid.uuid4)
    user_id = factory.LazyFunction(
        uuid.uuid4
    )  # Needs a UserFactory later, but define FK here
    educational_framework_id = None  # Optional FK
    active_dna_profile_id = None  # Optional FK
    title = factory.Sequence(lambda n: f"Video {n}")
    status = "active"
    creative_brief = factory.Faker("text")  # Assuming Faker is available
    created_at = factory.LazyFunction(datetime.datetime.now)
    updated_at = factory.LazyFunction(datetime.datetime.now)


class EvaluationResultFactory(factory.Factory):
    class Meta:
        model = EvaluationResult

    id = factory.LazyFunction(uuid.uuid4)
    video_id = factory.LazyFunction(uuid.uuid4)  # Needs a VideoFactory later
    evaluating_user_id = None  # Optional FK, needs UserFactory
    target_entity_id = factory.LazyFunction(
        uuid.uuid4
    )  # Generic FK, needs ID of target entity
    target_entity_type = "PROJECTS"  # Needs type of target entity
    evaluation_type = "quality"
    evaluation_result = {}
    created_at = factory.LazyFunction(datetime.datetime.now)


class BackgroundJobFactory(factory.Factory):
    class Meta:
        model = BackgroundJob

    id = factory.LazyFunction(uuid.uuid4)
    job_type = "ingest_content"
    status = "pending"
    video_id = None  # Optional FK, needs VideoFactory
    user_id = None  # Optional FK, needs UserFactory
    parameters = {}
    result = {}
    error = None
    created_at = factory.LazyFunction(datetime.datetime.now)
    updated_at = factory.LazyFunction(datetime.datetime.now)
    completed_at = None
