"""
SuperTokens configuration and initialization.

This module handles the setup and configuration of SuperTokens authentication,
following the project's async-first architecture.
"""

from typing import Dict, Any, List, Optional, Union

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from supertokens_python import init, InputAppInfo, SupertokensConfig
from supertokens_python.framework.fastapi import get_middleware
from supertokens_python.recipe import session, emailpassword
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.emailpassword.interfaces import APIInterface, APIOptions
from supertokens_python.recipe.emailpassword.types import FormField

from app.config import settings
from app.db.session import get_db_session
from app.db.models import User


def get_api_domain() -> str:
    """Get the API domain from settings."""
    return (
        settings.API_DOMAIN
        if hasattr(settings, "API_DOMAIN")
        else "http://localhost:8000"
    )


def get_website_domain() -> str:
    """Get the website domain from settings."""
    return (
        settings.WEBSITE_DOMAIN
        if hasattr(settings, "WEBSITE_DOMAIN")
        else "http://localhost:5173"
    )


def get_app_name() -> str:
    """Get the app name from settings."""
    return settings.APP_NAME if hasattr(settings, "APP_NAME") else "AI Video Platform"


def override_email_password_apis(original_implementation: APIInterface) -> APIInterface:
    """
    Override the default SuperTokens EmailPassword APIs to integrate with our User model.

    This ensures that when users sign up or sign in through SuperTokens, their information
    is properly synchronized with our application's User table, using async operations.
    """
    original_sign_up_post = original_implementation.sign_up_post
    original_sign_in_post = original_implementation.sign_in_post

    async def sign_up_post(
        form_fields: List[FormField],
        tenant_id: str,
        session: Union[SessionContainer, None],
        should_try_linking_with_session_user: Union[bool, None],
        api_options: APIOptions,
        user_context: Dict[str, Any],
    ):
        # Defensive check - ensure user_context is a dictionary
        # This follows the SuperTokens pattern - keep type signature but check inside
        if user_context is None or not isinstance(user_context, dict):
            user_context = {}

        # First, let SuperTokens handle the sign-up
        response = await original_sign_up_post(
            form_fields,
            tenant_id,
            session,
            should_try_linking_with_session_user,
            api_options,
            user_context,
        )

        # If sign-up was successful, create or update our User record
        if response.status == "OK":
            # Extract email from form fields
            email = next(
                (field.value for field in form_fields if field.id == "email"), None
            )

            if email:
                # Get SuperTokens user ID
                supertokens_user_id = response.user.id

                # Get database session from user_context if available
                db_session = user_context.get("db_session")

                if db_session:
                    try:
                        # Check if user with this email already exists
                        result = await db_session.execute(
                            User.__table__.select().where(User.email == email)
                        )
                        existing_user = result.scalar_one_or_none()

                        if existing_user:
                            # Update existing user with SuperTokens ID
                            existing_user.supertokens_user_id = supertokens_user_id
                            await db_session.commit()
                        else:
                            # Create new user
                            new_user = User(
                                email=email, supertokens_user_id=supertokens_user_id
                            )
                            db_session.add(new_user)
                            await db_session.commit()
                    except Exception as e:
                        await db_session.rollback()
                        # Log the error but don't fail the sign-up
                        print(f"Error syncing user after sign-up: {e}")

        return response

    async def sign_in_post(
        form_fields: List[FormField],
        tenant_id: str,
        session: Union[SessionContainer, None],
        should_try_linking_with_session_user: Union[bool, None],
        api_options: APIOptions,
        user_context: Dict[str, Any],
    ):
        # Defensive check - ensure user_context is a dictionary
        # This follows the SuperTokens pattern - keep type signature but check inside
        if user_context is None or not isinstance(user_context, dict):
            user_context = {}

        # First, let SuperTokens handle the sign-in
        response = await original_sign_in_post(
            form_fields,
            tenant_id,
            session,
            should_try_linking_with_session_user,
            api_options,
            user_context,
        )

        # If sign-in was successful, ensure our User record is properly linked
        if response.status == "OK":
            # Extract email from form fields
            email = next(
                (field.value for field in form_fields if field.id == "email"), None
            )

            if email:
                # Get SuperTokens user ID
                supertokens_user_id = response.user.id

                # Get database session from user_context if available
                db_session = user_context.get("db_session")

                if db_session:
                    try:
                        # Check if user with this SuperTokens ID already exists
                        result = await db_session.execute(
                            User.__table__.select().where(
                                User.supertokens_user_id == supertokens_user_id
                            )
                        )
                        existing_user = result.scalar_one_or_none()

                        if not existing_user:
                            # Check if user exists with this email but no SuperTokens ID
                            result = await db_session.execute(
                                User.__table__.select().where(
                                    User.email == email,
                                    User.supertokens_user_id.is_(None),
                                )
                            )
                            email_user = result.scalar_one_or_none()

                            if email_user:
                                # Update existing user with SuperTokens ID
                                email_user.supertokens_user_id = supertokens_user_id
                                await db_session.commit()
                            else:
                                # This is an edge case - user exists in SuperTokens but not in our DB
                                # Create new user instead of just logging a warning
                                new_user = User(
                                    email=email, supertokens_user_id=supertokens_user_id
                                )
                                db_session.add(new_user)
                                await db_session.commit()
                                print(
                                    f"Created new user record for existing SuperTokens user: {email}"
                                )
                    except Exception as e:
                        await db_session.rollback()
                        # Log the error but don't fail the sign-in
                        print(f"Error syncing user after sign-in: {e}")

        return response

    # Override the original implementation
    original_implementation.sign_up_post = sign_up_post
    original_implementation.sign_in_post = sign_in_post

    return original_implementation


def init_supertokens(app: FastAPI) -> None:
    """
    Initialize SuperTokens with the FastAPI app.

    This function configures SuperTokens with our application settings and
    adds the necessary middleware to the FastAPI app.
    """
    # Initialize SuperTokens
    init(
        app_info=InputAppInfo(
            app_name=get_app_name(),
            api_domain=get_api_domain(),
            website_domain=get_website_domain(),
            api_base_path="/auth",  # Explicitly set the API base path
            website_base_path="/auth",  # Explicitly set the website base path
        ),
        supertokens_config=SupertokensConfig(
            connection_uri=settings.SUPERTOKENS_CONNECTION_URI,
            api_key=settings.SUPERTOKENS_API_KEY.get_secret_value(),
        ),
        framework="fastapi",
        recipe_list=[
            session.init(
                cookie_secure=False,  # For development, set to True in production
                cookie_same_site="lax",  # For development, use "none" for cross-origin requests
            ),
            emailpassword.init(
                override=emailpassword.InputOverrideConfig(
                    apis=override_email_password_apis
                )
            ),
        ],
        mode="asgi",  # Use ASGI mode for FastAPI
    )

    # Add SuperTokens middleware
    app.add_middleware(get_middleware())


# Export session verification function for use in protected routes
session_verifier = verify_session()


async def get_user_id(session_container: SessionContainer) -> str:
    """
    Extract the user ID from a session container.

    This is a helper function to use in route dependencies.
    """
    return session_container.get_user_id()


async def get_user_from_session(
    session_container: SessionContainer,
    db_session: AsyncSession = Depends(get_db_session),
) -> Optional[User]:
    """
    Get the User model instance associated with the current session.

    Args:
        session_container: The SuperTokens session container
        db_session: SQLAlchemy async database session

    Returns:
        User instance or None if not found
    """
    supertokens_user_id = session_container.get_user_id()
    result = await db_session.execute(
        User.__table__.select().where(User.supertokens_user_id == supertokens_user_id)
    )
    return result.scalar_one_or_none()


# Create a dependency that injects the db_session into the user_context for SuperTokens
async def add_db_context_to_request(db_session: AsyncSession = Depends(get_db_session)):
    """
    A FastAPI dependency that adds the database session to the user_context.

    This should be used as a dependency in routes that need to access the database
    during SuperTokens authentication operations.
    """
    # This will be available in the user_context parameter of SuperTokens API overrides
    return {"db_session": db_session}
