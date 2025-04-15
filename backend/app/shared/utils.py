"""
Common Utility Functions.

This file contains general-purpose helper functions that don't belong to a
specific feature but are used across multiple parts of the backend.

Examples:
- Data formatting functions (e.g., date formatting, string manipulation).
- Simple validation helpers (that don't warrant a full Pydantic model).
- Functions for interacting with common external libraries in a standardized way.

Keep functions small, pure (if possible), and well-documented.
Avoid putting business logic or feature-specific code here. If a utility grows
complex or becomes tightly coupled to a feature, consider moving it.
"""
