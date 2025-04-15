"""
Custom Application Exceptions.

This file defines custom exception classes specific to the application domain.
These exceptions help in handling specific error conditions gracefully and
can be caught by FastAPI exception handlers to return appropriate HTTP responses.

Examples:
- `ResourceNotFoundError`, `InvalidInputError`, `AuthenticationError`.
- Exceptions related to specific business rules.

Define clear, specific exception types. Avoid creating overly generic exceptions.
These classes should generally inherit from Python's built-in `Exception`.
"""
