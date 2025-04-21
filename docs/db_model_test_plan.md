# Plan: Database Model Unit Test Suite

## Problem Context

Following the refactoring of the database models from a monolithic `models.py` to individual files in `backend/app/db/models/`, a dedicated unit test suite is required for the models layer. The existing test suite primarily focuses on API and service layers and lacks comprehensive coverage for fundamental database interactions at the model level.

## Goal

Design and implement a comprehensive, yet simple and maintainable, unit test suite for the database models layer (`backend/app/db/models/`). The suite should prioritize covering fundamental CRUD operations, data validation, and essential relationships to establish a strong testing foundation and prevent the accumulation of technical debt.

## Plan

### Phase 1: Investigation & Setup Verification (Completed)

1.  **Analyze `conftest.py`:** Reviewed `backend/tests/conftest.py`. It focuses on API testing setup and lacks a database session fixture for model tests.
2.  **Analyze `factories.py`:** Reviewed `backend/tests/factories.py`. It contains factories for `User` and `ChatMessage` but needs factories for all other refactored models.

### Phase 2: Test Suite Design & Structure (Completed)

1.  **Create New Test Directory:** Establish a dedicated directory for database model tests: `backend/tests/models/`.
2.  **Mirror Model Structure:** Inside `backend/tests/models/`, create test files corresponding to each model file in `backend/app/db/models/`. For example:
    *   `backend/app/db/models/user.py` -> `backend/tests/models/test_user.py`
    *   `backend/app/db/models/project.py` -> `backend/tests/models/test_project.py`
    *   ... and so on for all refactored model files.
3.  **Define Standard Test File Structure:** Each `test_*.py` file will follow a consistent pattern:
    *   **Imports:** Import `pytest`, the SQLAlchemy session fixture (e.g., `db_session`), the model(s) being tested, relevant factories, and any necessary exceptions (e.g., `IntegrityError`).
    *   **Test Class:** Define a test class (e.g., `TestUserModel`).
    *   **Test Methods:** Implement methods within the class for testing:
        *   `test_create_<model>`: Verify successful creation and persistence of a valid model instance using a factory. Assert attributes are set correctly.
        *   `test_retrieve_<model>`: Verify fetching the created instance from the DB.
        *   `test_update_<model>`: Verify updating attributes of the model instance and persisting changes.
        *   `test_delete_<model>`: Verify deleting the model instance.
        *   `test_<model>_<attribute>_not_nullable` (if applicable): Verify `IntegrityError` is raised when trying to commit `None` to a non-nullable field.
        *   `test_<model>_<attribute>_unique` (if applicable): Verify `IntegrityError` is raised when trying to commit a duplicate value for a unique field.
        *   `test_<model>_<attribute>_length_limit` (if applicable): Verify constraints on string lengths, potentially checking for validation errors or database errors depending on implementation.
        *   `test_<model>_<relationship>` (for essential relationships): Verify basic relationship functionality (e.g., creating a `User` and a `Project` and asserting `project.owner == user`).

### Phase 3: Implementation (In Progress - Writing Tests Postponed)

1.  **Setup Test Environment:**
    *   Add `db_session` fixture to `backend/tests/conftest.py`. **(Completed)**
    *   Create `factory-boy` factories for all models in `backend/tests/factories.py`. **(Completed - Manually by User)**
2.  **Create Test File Structure:**
    *   Create the `backend/tests/models/` directory. **(Completed)**
    *   Create empty `test_*.py` files mirroring model structure. **(Completed)**
3.  **Write Unit Tests:** Implement tests covering CRUD, validation, and relationships in `test_*.py` files. **(Pending - Postponed)**

#### Recent Related Work & Status

*   **Database Migration Issues:** Resolved issues preventing database upgrades, including manually dropping foreign key constraints and the `generated_structures` table.
*   **Model Removal:** The `GeneratedStructure` model and all its references have been successfully removed from the codebase and database schema.
*   **Application Debugging:** Fixed a `TypeError` in `chat_service.py` related to the Haystack `ChatMessage` constructor. A potential user lookup issue was noted but not fully debugged; its status after recent fixes is pending verification.

#### Next Steps (Postponed Implementation)

*   Implement unit tests in `backend/tests/models/`.
*   Verify overall application functionality.
*   Run the test suite (`pytest backend/tests/models/`).

## Proposed Test Directory Structure

```mermaid
graph TD
    subgraph backend
        subgraph tests
            direction LR
            A[tests] --> C(conftest.py);
            A --> F(factories.py);
            A --> M(models/);
            M --> T1(test_user.py);
            M --> T2(test_project.py);
            M --> T3(test_chat.py);
            M --> T4(test_audience.py);
            M --> TN(...);
            A --> API(api/);
            A --> AI(ai/);
            A --> SVC(services/);
        end
        subgraph app
            direction LR
            subgraph db
               direction LR
               DB[db] --> Models(models/);
               Models --> M1(user.py);
               Models --> M2(project.py);
               Models --> M3(chat.py);
               Models --> M4(audience.py);
               Models --> MN(...);
            end
        end
    end

    style M fill:#ccf,stroke:#333,stroke-width:2px
    style T1 fill:#ccf,stroke:#333,stroke-width:1px
    style T2 fill:#ccf,stroke:#333,stroke-width:1px
    style T3 fill:#ccf,stroke:#333,stroke-width:1px
    style T4 fill:#ccf,stroke:#333,stroke-width:1px
    style TN fill:#ccf,stroke:#333,stroke-width:1px
