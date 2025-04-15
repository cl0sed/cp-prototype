"""
Alembic Migration Environment Configuration.

This script is run by Alembic to configure the migration environment.
It typically:
- Loads database connection details (often from app config).
- Sets up the SQLAlchemy metadata object (`target_metadata`) to be used for
  autogenerate diffs.
- Configures logging for Alembic operations.

Customize this file to control how Alembic connects to your database and detects
schema changes. Avoid putting application-specific setup here unless it's
directly required for Alembic to function.
"""
