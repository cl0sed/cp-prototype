"""
FastAPI Dependencies.

This file contains reusable dependencies for FastAPI endpoints, such as:
- Authentication checks (e.g., verifying JWT tokens, API keys).
- Database session management per request.
- Retrieving current user objects.
- Role-based access control.

Keep dependencies concise and focused on a single task (e.g., getting a DB session).
Avoid putting complex business logic directly into dependencies; they should primarily
handle cross-cutting concerns like auth and resource setup/teardown.
"""
