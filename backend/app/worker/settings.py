"""
SAQ (Simple Async Queue) Worker Configuration.

This file defines the SAQ Queue instance, imports task functions, and
configures worker settings (e.g., concurrency, connection details).

It serves as the entry point for discovering and registering background tasks
that the SAQ worker process will execute.

Keep this focused on queue definition and task discovery. Task implementation
logic should reside in feature-specific `tasks.py` files (e.g., `app/features/voice_dna/tasks.py`).
"""
