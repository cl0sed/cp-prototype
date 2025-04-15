"""
Core Logic / Service Layer for the Voice DNA Feature.

This file contains the main business logic for the Creator Voice DNA feature.
It acts as a facade, orchestrating interactions between API endpoints/tasks,
data access (repositories/DB), and AI pipelines.

Examples:
- Functions to initiate Voice DNA analysis.
- Functions to retrieve or update Voice DNA profiles.
- Functions to utilize the Voice DNA for content generation tasks.
- Coordination of database operations and calls to AI pipelines (`pipelines.py`).

Implement the core use cases of the feature here.
Keep this layer clean of direct web framework (FastAPI) or database session
management details; inject dependencies (like DB sessions, pipeline runners) instead.
Avoid putting raw AI pipeline definitions here; use `pipelines.py`.
"""
