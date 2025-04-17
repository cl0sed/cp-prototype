"""
Main FastAPI application entry point.

This file defines the FastAPI application instance, includes routers,
configures middleware, and potentially handles lifespan events (startup/shutdown).

Application-wide settings or configurations that don't belong in config.py
and are directly related to the FastAPI app instance itself can go here.
Avoid putting business logic or specific endpoint implementations in this file;
keep it focused on application assembly.
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .api.routers import health, tasks, agent
from .config import settings  # Import centralized settings
from .features.auth import init_supertokens  # Import SuperTokens initialization
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session

# Create FastAPI app instance
app = FastAPI(
    title="AI Video Creation Platform API",
    version="0.1.0",
    description="API for managing AI-powered video script creation.",
)

# ----------------
# MIDDLEWARE SETUP - Order is important (last registered = first executed)
# ----------------

# 1. Add CORS middleware first (to handle preflight requests before any other processing)
# Debug: Print CORS settings being used
print("DEBUG - CORS settings:")
print(f"CORS_ALLOWED_ORIGINS: {settings.CORS_ALLOWED_ORIGINS}")
print(f"CORS_ALLOW_CREDENTIALS: {settings.CORS_ALLOW_CREDENTIALS}")
print(f"CORS_ALLOW_METHODS: {settings.CORS_ALLOW_METHODS}")
print(f"CORS_ALLOW_HEADERS: {settings.CORS_ALLOW_HEADERS}")

# Try more permissive CORS settings for debugging
app.add_middleware(
    CORSMiddleware,
    # Use explicit wildcard for debugging
    allow_origins=["*"],
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
    expose_headers=["*"],
    max_age=86400,  # 24 hours in seconds
)
print(f"CORS configured to allow these origins: {settings.CORS_ALLOWED_ORIGINS}")

# ----------------
# AUTHENTICATION SETUP - Initialize SuperTokens AFTER CORS middleware
# ----------------

# Initialize SuperTokens with our FastAPI app
init_supertokens(app)

# 2. Add any other middleware here (they will execute after CORS)
# Example: app.add_middleware(SomeOtherMiddleware, ...)

# ----------------
# ROUTER INCLUSION - After middleware setup
# ----------------

# Include routers after middleware configuration
app.include_router(health.router)
app.include_router(tasks.router)  # Include the tasks router
app.include_router(agent.router)  # Include the agent router with protected endpoints


# Add a test route to verify session
@app.get("/auth/session")
async def session_info(session: SessionContainer = Depends(verify_session())):
    return {"user_id": session.get_user_id()}


# ----------------
# LOGGING CONFIGURATION
# ----------------

# Logging configuration will be applied here (using logging_config.py)

# ----------------
# LIFESPAN EVENTS
# ----------------

# Lifespan events (startup/shutdown) will be defined here
