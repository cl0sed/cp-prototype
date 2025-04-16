# SAQ Worker Implementation

This directory contains the implementation of the SAQ (Simple Async Queue) worker for background job processing.

## Overview

The SAQ worker system is used to offload long-running tasks from the API service to background workers, ensuring responsive API endpoints while handling resource-intensive operations asynchronously.

## Components

- `settings.py`: Contains the queue configuration, task registration, and lifecycle hooks
- `tasks.py`: Defines the actual task functions that will be executed by the worker
- The lifecycle hooks (before_process, after_process) track job status in the `background_jobs` table

## Key Features

1. **Task Tracking**: Every task is tracked in the database with a unique job ID
2. **Lifecycle Hooks**: Automatic job status updates before and after task execution
3. **Error Handling**: Failed tasks are properly tracked with error messages
4. **Redis Integration**: Uses Redis as the message broker for job queuing

## Testing the Implementation

To test the SAQ worker implementation:

1. Start all services using Docker Compose:
   ```
   docker-compose up --build
   ```

2. Trigger a test task using the API endpoint:
   ```
   curl -X POST http://localhost:8000/api/v1/tasks/trigger-test \
     -H "Content-Type: application/json" \
     -d '{"message": "Test message", "user_id": null, "project_id": null}'
   ```

3. You should receive a response with a job ID:
   ```json
   {
     "message": "Test task accepted and queued for processing",
     "job_id": "some-unique-id"
   }
   ```

4. Monitor the worker logs to see the job processing:
   ```
   docker-compose logs -f worker
   ```

5. Verify the job record in the database:
   ```
   docker-compose exec db psql -U user -d app_db -c "SELECT * FROM background_jobs ORDER BY created_at DESC LIMIT 1;"
   ```

## Notes on Scaling

This implementation is designed for PoC validation. For production, consider:

1. Increasing the concurrency parameter in settings.py
2. Adding more worker instances for horizontal scaling
3. Implementing more robust error handling and retry strategies
