"""
Core Internal Data Shapes (Pydantic Models).

This file defines Pydantic models representing core data structures used
internally within the backend, potentially across different features or layers,
but NOT directly exposed via the API.

Examples:
- Internal representations of data retrieved from multiple sources.
- Standardized structures passed between services or components.
- Data shapes used before being mapped to API responses or database models.

Distinguish these from API schemas (`app/api/schemas.py`) which define the
external contract, and DB models (`app/db/models.py`) which define the
database structure. These are for internal data transfer and consistency.
"""
