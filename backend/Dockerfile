# Dockerfile for the Backend (API + Worker)
#
# This file defines the steps to build the Docker image containing the Python
# backend application code (FastAPI API and SAQ Worker).
#
# Responsibilities:
# - Specify the base Python image.
# - Install system dependencies (if any).
# - Install Python dependencies (using pyproject.toml via Poetry/PDM).
# - Copy application code into the image.
# - Set environment variables (non-secret defaults).
# - Define the default command/entrypoint (or allow overriding via docker run/compose).
#
# Keep this focused on creating a reproducible image. Avoid environment-specific
# configurations (like secrets) here; inject those at runtime.
# Optimize for layer caching (e.g., copy dependency file and install before copying code).
