"""
Main FastAPI application entry point.
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

# Import router modules directly
from .api.routers import health
from .api.routers import tasks
from .api.routers import agent
from .api.routers import user
from .api.routers import chat  # Import the new chat router
from .config import get_settings  # Import get_settings()
import logging  # Import logging
from .features.auth import init_supertokens  # Import SuperTokens initialization
from .lifecycle import lifespan  # Import the lifespan context manager
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session

logging.basicConfig(level=get_settings().LOG_LEVEL.upper())

# Create FastAPI app instance and register lifespan
app = FastAPI(
    title="AI Video Creation Platform API",
    version="0.1.0",
    description="API for managing AI-powered video script creation.",
    lifespan=lifespan,
)

# ----------------
# MIDDLEWARE SETUP - Order is important
# ----------------

logging.debug("CORS get_settings():")
logging.debug(f"CORS_ALLOWED_ORIGINS: {get_settings().CORS_ALLOWED_ORIGINS}")
logging.debug(f"CORS_ALLOW_CREDENTIALS: {get_settings().CORS_ALLOW_CREDENTIALS}")
logging.debug(f"CORS_ALLOW_METHODS: {get_settings().CORS_ALLOW_METHODS}")
logging.debug(f"CORS_ALLOW_HEADERS: {get_settings().CORS_ALLOW_HEADERS}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().CORS_ALLOWED_ORIGINS,
    allow_credentials=get_settings().CORS_ALLOW_CREDENTIALS,
    allow_methods=get_settings().CORS_ALLOWED_METHODS,
    allow_headers=get_settings().CORS_ALLOWED_HEADERS,
    expose_headers=[
        "Content-Type",
        "Content-Length",
        "Authorization",
        "sFrontToken",  # Added sFrontToken for SuperTokens
    ],
    max_age=86400,
)
logging.info(
    f"CORS configured to allow origins: {get_settings().CORS_ALLOWED_ORIGINS}"
)  # Replaced print with logging

# ----------------
# AUTHENTICATION SETUP - Initialize SuperTokens AFTER CORS middleware
# ----------------

# Initialize SuperTokens with our FastAPI app (this adds SuperTokens middleware internally)
init_supertokens(app)

# ----------------
# ROUTER INCLUSION - After middleware setup
# ----------------

app.include_router(health.router)
app.include_router(tasks.router)
app.include_router(agent.router)
app.include_router(user.router, prefix="/api")
app.include_router(chat.router, prefix="/api")


# Add a test route to verify session
@app.get(
    "/auth/sessioninfo"
)  # Changed path slightly to avoid conflict if ST uses /auth/session
async def session_info(session: SessionContainer = Depends(verify_session())):
    return {
        "userId": session.get_user_id(),
        "accessTokenPayload": session.get_access_token_payload(),
    }


# ----------------
# LOGGING CONFIGURATION
# ----------------
# (Logging setup is typically done early, potentially before FastAPI app creation,
# but can also be managed within the lifespan or separate config files.)
# The lifespan handles specific startup logging and validation.
