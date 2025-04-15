"""
Main FastAPI application entry point.

This file defines the FastAPI application instance, includes routers,
configures middleware, and potentially handles lifespan events (startup/shutdown).

Application-wide settings or configurations that don't belong in config.py
and are directly related to the FastAPI app instance itself can go here.
Avoid putting business logic or specific endpoint implementations in this file;
keep it focused on application assembly.
"""

from fastapi import FastAPI
from .api.routers import health

app = FastAPI(
    title="AI Video Creation Platform API",
    version="0.1.0",
    description="API for managing AI-powered video script creation.",
)

# Include routers
app.include_router(health.router)

# Logging configuration will be applied here (using logging_config.py)

# Middleware will be added here

# Lifespan events (startup/shutdown) will be defined here

# Configuration settings (from config.py) will be loaded/used here
