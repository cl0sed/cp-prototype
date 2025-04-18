"""
Main FastAPI application entry point.
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
# Import middleware for handling proxy headers
# Use starlette's middleware as uvicorn's is deprecated/internal
# It seems Uvicorn's --proxy-headers flag implicitly adds 'uvicorn.middleware.proxy_headers.ProxyHeadersMiddleware'.
# Let's rely on that for now and ensure FORWARDED_ALLOW_IPS is set in config.
# If issues persist, we might need to add it manually here using starlette's version.

from .api.routers import health, tasks, agent, user  # Add user router import
from .config import settings  # Import centralized settings
from .features.auth import init_supertokens  # Import SuperTokens initialization
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session

# Create FastAPI app instance
# Pass middleware list if adding ProxyHeadersMiddleware manually, otherwise rely on Uvicorn flag
app = FastAPI(
    title="AI Video Creation Platform API",
    version="0.1.0",
    description="API for managing AI-powered video script creation.",
    # Example if adding manually:
    # middleware=[
    #     Middleware(ProxyHeadersMiddleware, trusted_hosts=settings.FORWARDED_ALLOW_IPS)
    # ]
)

# ----------------
# MIDDLEWARE SETUP - Order is important
# ----------------

# 1. Proxy Headers Middleware (Handled by Uvicorn --proxy-headers flag using settings.FORWARDED_ALLOW_IPS)
#    If issues persist, uncomment the manual addition in FastAPI constructor above.

# 2. Add CORS middleware *after* proxy headers are processed
print("DEBUG - CORS settings:")
print(f"CORS_ALLOWED_ORIGINS: {settings.CORS_ALLOWED_ORIGINS}")
print(f"CORS_ALLOW_CREDENTIALS: {settings.CORS_ALLOW_CREDENTIALS}")
print(f"CORS_ALLOW_METHODS: {settings.CORS_ALLOW_METHODS}")
print(f"CORS_ALLOW_HEADERS: {settings.CORS_ALLOW_HEADERS}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,  # Use computed list
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOWED_METHODS,  # Use computed list
    allow_headers=settings.CORS_ALLOWED_HEADERS,  # Use computed list
    expose_headers=[
        "Content-Type",
        "Content-Length",
        "Authorization",
        "sFrontToken",
    ],  # Added sFrontToken for SuperTokens
    max_age=86400,
)
print(f"CORS configured to allow origins: {settings.CORS_ALLOWED_ORIGINS}")

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
# Include the user router with /api prefix to match Nginx and frontend calls
app.include_router(user.router, prefix="/api")


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
# LOGGING CONFIGURATION / LIFESPAN EVENTS
# ----------------
# (Add logging/lifespan setup here if needed)
