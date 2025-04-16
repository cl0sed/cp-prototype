"""
Background Worker Package.

This package contains the configuration and task definitions for
background processing using SAQ (Simple Async Queue).

The worker runs as a separate service from the API and processes
jobs asynchronously. Task status is tracked in the background_jobs
database table.
"""
