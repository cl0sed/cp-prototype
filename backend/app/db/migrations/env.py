import os
import sys
import asyncio
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context

# --- Project-specific Setup ---
# Add the 'backend' directory to sys.path to allow importing 'app' package
sys.path.insert(
    0, os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
)

try:
    # Import your SQLAlchemy Base from models.py
    # Ensure 'backend/app/db/models.py' exists and defines 'Base'
    from app.db.models import Base

    # Import your Pydantic BaseSettings configuration object
    # Ensure 'backend/app/config.py' exists and defines 'settings'
    from app.config import settings
except ImportError as e:
    print("FATAL: Could not import Base or settings in Alembic env.py.")
    print("       Ensure backend/app/db/models.py defines 'Base'.")
    print("       Ensure backend/app/config.py defines 'settings'.")
    print("       Ensure the script is run from the project root or paths are correct.")
    print(f"       Import Error: {e}")
    sys.exit(1)  # Stop if essential imports fail

# --- Alembic Configuration ---
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata for 'autogenerate' support
target_metadata = Base.metadata


# --- Database URL Configuration ---
def get_url_from_settings():
    """Constructs the database URL from the application settings object."""
    try:
        # Assumes settings.DATABASE_URL is available (e.g., from .env)
        # Handles potential Pydantic SecretStr
        db_url = getattr(settings, "DATABASE_URL", None)
        if db_url is None:
            raise ValueError(
                "DATABASE_URL not found in the settings object (app.config.settings). Check your .env file and config.py."
            )

        url_str = (
            db_url.get_secret_value()
            if hasattr(db_url, "get_secret_value")
            else str(db_url)
        )

        if not url_str:
            raise ValueError("DATABASE_URL is empty in the application settings.")
        return url_str
    except (AttributeError, ValueError) as e:
        print(f"FATAL Error configuring database URL in Alembic env.py: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"FATAL: An unexpected error occurred getting the database URL: {e}")
        sys.exit(1)


# --- Migration Execution Functions ---
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = get_url_from_settings()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # include_object=include_object # Add if using include_object filter
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        # compare_type=True, # Optional: Check column types too
        # include_schemas=True, # If using schemas
        # include_object=include_object # Add if using include_object filter
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online_async() -> None:
    """Run migrations in 'online' mode using async engine."""
    # Get the database URL
    db_url = get_url_from_settings()

    # Create async engine
    connectable = create_async_engine(db_url)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_migrations_online_async())


# --- Main Execution Logic ---
try:
    if context.is_offline_mode():
        print("Running migrations in offline mode...")
        run_migrations_offline()
    else:
        print("Running migrations in online mode...")
        run_migrations_online()
    print("Migrations execution finished.")
except SystemExit:
    # Allow SystemExit to propagate to indicate failure
    raise
except Exception as e:
    print(f"FATAL: An error occurred during migration execution: {e}")
    # Consider logging traceback here
    sys.exit(1)  # Ensure script exits with error code
