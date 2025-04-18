"""
SuperTokens configuration and initialization.

This module handles the setup and configuration of SuperTokens authentication,
following the project's async-first architecture.
"""

from typing import Dict, Any, List, Optional, Union

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select  # Import select
from supertokens_python import init, InputAppInfo, SupertokensConfig
from supertokens_python.framework.fastapi import get_middleware
from supertokens_python.recipe import session, emailpassword
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.emailpassword.interfaces import APIInterface, APIOptions
from supertokens_python.recipe.emailpassword.types import (
    FormField,
    InputFormField,
)  # Import InputFormField

from app.config import settings
from app.db.session import (
    get_db_session,
    async_session_factory,
)  # Ensure async_session_factory is imported
from app.db.models import User

# Use APP_BASE_URL from settings instead of hardcoding the proxy address


def get_api_domain() -> str:
    """Get the API domain from settings."""
    return settings.APP_BASE_URL


def get_website_domain() -> str:
    """Get the website domain from settings."""
    return settings.APP_BASE_URL


def get_app_name() -> str:
    """Get the app name from settings."""
    return settings.APP_NAME if hasattr(settings, "APP_NAME") else "AI Video Platform"


def override_email_password_apis(original_implementation: APIInterface) -> APIInterface:
    """
    Override the default SuperTokens EmailPassword APIs to integrate with our User model.
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
        # Call original implementation first
        response = await original_sign_up_post(
            form_fields,
            tenant_id,
            session,
            should_try_linking_with_session_user,
            api_options,
            user_context,
        )

        # If signup was successful, sync with our DB
        if response.status == "OK":
            email = next((f.value for f in form_fields if f.id == "email"), None)
            if email:
                supertokens_user_id = response.user.id
                # Manually create session scope for DB operations
                async with async_session_factory() as db_session:
                    try:
                        # Use ORM select
                        stmt = select(User).where(User.email == email)
                        result = await db_session.execute(stmt)
                        existing_user = result.scalar_one_or_none()
                        if existing_user:
                            # Link existing user if found by email
                            if existing_user.supertokens_user_id is None:
                                existing_user.supertokens_user_id = supertokens_user_id
                                await db_session.commit()
                                print(
                                    f"Linked existing user {email} to SuperTokens ID {supertokens_user_id}"
                                )
                            elif (
                                existing_user.supertokens_user_id != supertokens_user_id
                            ):
                                # Handle potential conflict - should ideally not happen if ST handles email uniqueness
                                print(
                                    f"Warning: User {email} already linked to a different SuperTokens ID."
                                )
                                await db_session.rollback()  # Rollback to be safe
                            # else: user already correctly linked, do nothing
                        else:
                            # Create new user if not found
                            new_user = User(
                                email=email, supertokens_user_id=supertokens_user_id
                            )
                            db_session.add(new_user)
                            await db_session.commit()
                            print(
                                f"Created new user {email} with SuperTokens ID {supertokens_user_id}"
                            )
                    except Exception as e:
                        await db_session.rollback()
                        print(f"Error syncing user after sign-up: {e}")
                        # Optionally re-raise or handle the error to inform SuperTokens/user
                        # For now, just log and return original response
        return response

    async def sign_in_post(
        form_fields: List[FormField],
        tenant_id: str,
        session: Union[SessionContainer, None],
        should_try_linking_with_session_user: Union[bool, None],
        api_options: APIOptions,
        user_context: Dict[str, Any],
    ):
        # Call original implementation first
        response = await original_sign_in_post(
            form_fields,
            tenant_id,
            session,
            should_try_linking_with_session_user,
            api_options,
            user_context,
        )

        # If sign-in was successful, ensure user exists in our DB
        if response.status == "OK":
            email = next((f.value for f in form_fields if f.id == "email"), None)
            if email:
                supertokens_user_id = response.user.id
                # Manually create session scope for DB operations
                async with async_session_factory() as db_session:
                    try:
                        # Use ORM select
                        stmt = select(User).where(
                            User.supertokens_user_id == supertokens_user_id
                        )
                        result = await db_session.execute(stmt)
                        existing_user = result.scalar_one_or_none()
                        if not existing_user:
                            # Attempt to link by email if ST ID match failed
                            # Use ORM select
                            stmt_email = select(User).where(
                                User.email == email,
                                User.supertokens_user_id.is_(None),
                            )
                            result_email = await db_session.execute(stmt_email)
                            email_user = result_email.scalar_one_or_none()
                            if email_user:
                                email_user.supertokens_user_id = supertokens_user_id
                                await db_session.commit()
                                print(
                                    f"Linked existing user {email} to SuperTokens ID {supertokens_user_id} during sign-in"
                                )
                            else:
                                # User exists in SuperTokens but not in our DB - this indicates an inconsistency
                                # Log a warning, maybe create the user? Depends on desired behavior.
                                print(
                                    f"Warning: User {email} (ST ID: {supertokens_user_id}) signed in but not found or already linked in local DB."
                                )
                                # Optionally create user if missing:
                                # new_user = User(email=email, supertokens_user_id=supertokens_user_id)
                                # db_session.add(new_user)
                                # await db_session.commit()
                                # print(f"Created missing user record for {email} during sign-in.")
                    except Exception as e:
                        # Avoid rollback here unless absolutely necessary, as sign-in was successful
                        print(f"Error checking/syncing user after sign-in: {e}")
                        # Do not interfere with the successful sign-in response
        return response

    original_implementation.sign_up_post = sign_up_post
    original_implementation.sign_in_post = sign_in_post
    return original_implementation


def init_supertokens(app: FastAPI) -> None:
    """
    Initialize SuperTokens with the FastAPI app.
    """
    init(
        app_info=InputAppInfo(
            app_name=get_app_name(),
            api_domain=get_api_domain(),  # Use APP_BASE_URL from settings
            website_domain=get_website_domain(),  # Use APP_BASE_URL from settings
            api_base_path="/auth",  # Reverted base path
            website_base_path="/auth",  # Reverted base path
        ),
        supertokens_config=SupertokensConfig(
            connection_uri=settings.SUPERTOKENS_CONNECTION_URI,
            api_key=settings.SUPERTOKENS_API_KEY.get_secret_value(),
        ),
        framework="fastapi",
        recipe_list=[
            session.init(
                cookie_secure=True,
                cookie_same_site="none",
                cookie_domain=None,  # Keep None for localhost proxy
                get_token_transfer_method=lambda _, __, ___: "cookie",
            ),
            emailpassword.init(
                sign_up_feature=emailpassword.InputSignUpFeature(
                    form_fields=[
                        InputFormField(id="email"),
                        InputFormField(id="password"),
                        InputFormField(id="username"),  # Use InputFormField
                    ]
                ),
                override=emailpassword.InputOverrideConfig(
                    apis=override_email_password_apis
                ),
            ),
        ],
        mode="asgi",
    )
    app.add_middleware(get_middleware())


session_verifier = verify_session()


async def get_user_id(session_container: SessionContainer) -> str:
    """Extract the user ID from a session container."""
    return session_container.get_user_id()


async def get_user_from_session(
    session_container: SessionContainer = Depends(
        session_verifier
    ),  # Added Depends here for clarity
    db_session: AsyncSession = Depends(get_db_session),
) -> Optional[User]:
    """Get the User model instance associated with the current session."""
    supertokens_user_id = session_container.get_user_id()
    # Use ORM select
    stmt = select(User).where(User.supertokens_user_id == supertokens_user_id)
    result = await db_session.execute(stmt)
    return result.scalar_one_or_none()


async def add_db_context_to_request(db_session: AsyncSession = Depends(get_db_session)):
    """A FastAPI dependency that adds the database session to the user_context."""
    return {"db_session": db_session}


# Corrected implementation: Depends directly on session_verifier and get_db_session
async def get_required_user_from_session(
    session_container: SessionContainer = Depends(session_verifier),
    db_session: AsyncSession = Depends(get_db_session),
) -> User:
    """
    Get the User model instance associated with the current session.
    Raises HTTPException(403) if user is not found in the database.

    This dependency combines fetching the user and handling the common error case
    where a valid session exists but no corresponding user record is found in the DB.

    Usage in FastAPI:
    ```
    @app.get("/protected-endpoint")
    async def protected_endpoint(user: User = Depends(get_required_user_from_session)):
        # No need to check if user exists - it's guaranteed or an exception is raised
        return {"user_id": str(user.id)}
    ```
    """
    supertokens_user_id = session_container.get_user_id()
    # Use ORM select
    stmt = select(User).where(User.supertokens_user_id == supertokens_user_id)
    result = await db_session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        # Log the warning as well
        print(
            f"WARNING: Valid session for ST ID {supertokens_user_id} but no matching user in DB."
        )
        raise HTTPException(status_code=403, detail="User not found in database")
    return user
