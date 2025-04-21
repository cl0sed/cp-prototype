# Decision Log

This file records architectural and implementation decisions using a list format.
2025-04-18 09:27:00 - Log of updates made.

*

## Decision

* [2025-04-18 09:27:00] - Rearchitect the React Frontend with React 19.1, Mantine 7.17.4, and SuperTokens Auth React
* [2025-04-17 12:34:00] - Use SuperTokens Managed Service for Authentication
* [2025-04-18 13:00:00] - Use Vite Alias for @tabler/icons-react to Fix Dev Server Performance
* [2025-04-18 13:26:00] - Refine Proxy Strategy: Modify Nginx `/auth/` block for SuperTokens CORS preflight only, use Vite proxy for `/auth` API calls.
* [2025-04-18 15:00:00] - Standardize HTTP Status Code for "User Not Found" Error
* [2025-04-18 15:05:00] - Create `get_required_user_from_session` Dependency
* [2025-04-18 15:10:00] - Centralize `APP_BASE_URL` in `config.py`

* [2025-04-18 15:24:00] - Remove Redundant Frontend Auth Code (Layout, Route, Services)

* [2025-04-18 15:33:00] - Optimize dev workflow: Added `watchfiles` for worker hot-reloading, removed redundant `npm install` from frontend command. Backend dependencies are managed with `uv` and pyproject.toml.
* [2025-04-19 10:39:00] - Update `portkey-ai` dependency version to `1.12.0`.
* [2025-04-19 10:39:00] - Allow access to `.env` files in `.rooignore`.
* [2025-04-19 10:39:00] - Use TypeScript (`.ts`/`.tsx`) for all new frontend files and update existing ones.
* [2025-04-19 10:39:00] - Integrate chat API logic into existing `frontend/src/services/apiService.ts`.
* [2025-04-19 10:39:00] - Configure frontend routing to make `ChatPage` the default landing page for authenticated users.
* [2025-04-19 10:39:00] - Add missing `HealthResponse` schema to `backend/app/api/schemas.py`.
* [2025-04-19 19:15:53] - Decision: Investigate `/api/api/...` routing issue across frontend API client, Vite proxy, and Nginx configuration.
* [2025-04-19 20:11:47] - Decision: Fix `/api/api/...` routing issue by correcting endpoint paths in frontend `apiService.ts` (removed duplicated `/api`).
* [2025-04-19 20:11:47] - Decision: Remove Nginx rewrite rule `rewrite ^/api(.*)$ $1 break;` from `reverse-proxy.conf` as it is no longer needed after fixing frontend routing.
* [2025-04-19 20:11:47] - Decision: Address SQLAlchemy warnings about overlapping relationships by adding `overlaps` parameter to relevant relationships in `backend/app/db/models.py`.
* [2025-04-19 20:11:47] - Decision: Fix `NameError: name 'UUID' is not defined` in `backend/app/features/auth/supertokens_config.py` by adding `from uuid import UUID` import.
* [2025-04-19 20:11:47] - Decision: Attempt to resolve 422 Unprocessable Entity errors by changing `get_required_user_from_session` dependency to return user ID (UUID) instead of full User object and updating chat endpoints accordingly.
* [2025-04-19 20:11:47] - Decision: Add debug logging in `backend/app/services/chat_service.py` and `backend/app/api/routers/chat.py` to inspect data structures during 422 error debugging.
* [2025-04-19 10:39:00] - Integrate chat API logic into existing `frontend/src/services/apiService.ts`.
* [2025-04-19 10:39:00] - Configure frontend routing to make `ChatPage` the default landing page for authenticated users.
* [2025-04-18 09:27:00] - **React 19.1 & Mantine 7.17.4 & SuperTokens Auth React Decision:**
  * React 19.1 provides the latest performance improvements and feature updates for modern web applications.
  * Mantine 7.17.4 offers a comprehensive UI component library with excellent TypeScript support and theming capabilities.
  * Consolidating authentication to use only `supertokens-auth-react` improves maintainability by removing the redundant `supertokens-web-js` dependency.
  * This approach establishes a modern, well-supported tech stack for the React frontend while ensuring consistent authentication implementation.
  * The migration allows for better code organization and follows the best practices documented in the official SuperTokens documentation.

* [2025-04-17 12:34:00] - **SuperTokens Decision:**
  * SuperTokens Managed Service aligns with our "Low-Ops" principle, eliminating the need to run and maintain authentication servers ourselves.
  * It provides a complete authentication solution with pre-built UI components, reducing development time.
  * The SDK offers both backend (FastAPI) and frontend (SvelteKit) integration.
  * The managed service handles security complexities like password storage and session management.
  * SuperTokens supports our core authentication requirements: sign-up, sign-in, sign-out, and session management.
  * The free tier of the managed service is sufficient for our PoC needs.

* [2025-04-18 13:00:00] - **Vite Alias for @tabler/icons-react Rationale:**
  * The `@tabler/icons-react` library uses internal dynamic imports (`dist/esm/dynamic-imports.mjs`) which caused Vite's dev server to generate thousands of requests/chunks, severely impacting performance.
  * Directly excluding the library from `optimizeDeps` prevented a Vite optimization loop but resulted in the browser making thousands of requests.
  * Using a Vite alias forces imports of `@tabler/icons-react` to resolve to the static export file (`dist/esm/icons/index.mjs`), bypassing the problematic dynamic imports during development.
  * This resolves the excessive request issue without reintroducing the Vite optimization loop.

* [2025-04-18 13:26:00] - **Refine Proxy Strategy Rationale:**
  * Initial plan to remove Nginx `location /auth/` block was flawed. While it fixed the 404 issue caused by incorrectly proxying non-OPTIONS requests to the backend, it also removed necessary CORS preflight (OPTIONS) handling.
  * **Critical Context:** This specific Nginx OPTIONS handling for `/auth` was previously implemented to resolve persistent CORS errors encountered when the SuperTokens frontend SDK attempted to communicate with the backend API under the `/auth` path. Standard CORS middleware in the backend or Vite proxy alone was insufficient.
  * **Refined Approach:** Modify Nginx `location /auth/` to *only* handle OPTIONS requests, preserving the critical SuperTokens CORS preflight logic. Remove the `proxy_pass` directive for non-OPTIONS requests within this block.
  * This allows non-OPTIONS `/auth/...` requests (API calls like `/auth/signin` and frontend routes like `/auth/login`) to fall through to the Nginx `location /` block, which correctly proxies them to the Vite dev server.
  * Adding a `/auth` proxy rule to `vite.config.ts` leverages Vite's dev server to correctly forward the SuperTokens API calls (now received via Nginx `location /`) to the backend service (`http://backend:8000`).
  * This maintains the necessary CORS fix while correctly routing frontend pages and backend API calls.


* [2025-04-18 15:24:00] - **Remove Redundant Frontend Auth Code Rationale:**
  * The code review identified several components and service logic (`AuthLayout.tsx`, `ProtectedRoute.tsx`, manual token handling in `apiService.ts`, most of `authService.ts`) that were either unused, non-functional (due to missing dependencies like `useAuth`), or conflicted with the primary authentication patterns established using the SuperTokens React SDK (`<SessionAuth>`, `useSessionContext`, `signIn`, `signUp`, cookie-based sessions).
  * Removing this code simplifies the codebase, eliminates potential confusion, reduces maintenance overhead, and ensures reliance on the recommended SuperTokens SDK integration methods.

* [2025-04-19 10:39:00] - **Update `portkey-ai` dependency version to `1.12.0` Rationale:** To use the latest features and improvements available in version 1.12.0 of the `portkey-ai` library.
* [2025-04-19 10:39:00] - **Allow access to `.env` files in `.rooignore` Rationale:** To enable the AI assistant to read `.env.example` files for configuration context and to add new environment variable placeholders as needed during development tasks.
* [2025-04-19 10:39:00] - **Use TypeScript (`.ts`/`.tsx`) for all new frontend files and update existing ones Rationale:** To maintain consistency with the existing frontend codebase, leverage the benefits of static typing (improved code quality, maintainability, and developer experience), and align with modern React development practices.
* [2025-04-19 10:39:00] - **Integrate chat API logic into existing `frontend/src/services/apiService.ts` Rationale:** To avoid code duplication and centralize API communication logic within the existing service file, adhering to established project patterns.
* [2025-04-19 10:39:00] - **Configure frontend routing to make `ChatPage` the default landing page for authenticated users Rationale:** To fulfill the task requirement of the chat interface being the primary landing page for logged-in users, improving user flow and accessibility to the core functionality.
* [2025-04-19 10:39:00] - **Add missing `HealthResponse` schema to `backend/app/api/schemas.py` Rationale:** To resolve a backend `ImportError` and restore the necessary schema for the health check endpoint, ensuring the backend application can start correctly.
## Implementation Details
* [2025-04-18 13:06:00] - **Nginx Reverse Proxy and CORS Implementation:**
  * Nginx (`reverse-proxy.conf` mounted via Docker Compose) acts as the single entry point for the application.
  * It routes requests to the appropriate service (frontend-react, backend API, backend auth).
  * It handles SSL termination (implicitly, by forwarding as HTTP internally but potentially receiving HTTPS).
  * It explicitly handles CORS preflight (OPTIONS) requests for `/api` and `/auth` locations.
  * It adds necessary CORS headers (`Access-Control-Allow-*`) for requests to `/api` and `/auth`.
  * The backend (FastAPI) also includes `CORSMiddleware` for fine-grained control and to ensure CORS headers are present even if Nginx configuration changes.
  * The backend Uvicorn process uses `--proxy-headers` to correctly interpret `X-Forwarded-*` headers set by Nginx.
* [2025-04-18 09:27:00] - **React 19.1 & Mantine 7.17.4 & SuperTokens Auth React Implementation:**
  * **Package Updates:**
    * Updated React and React DOM to version 19.1.0.
    * Updated Mantine packages to version 7.17.4 (`@mantine/core`, `@mantine/form`, `@mantine/hooks`, `@mantine/notifications`).
    * Removed the redundant `supertokens-web-js` dependency.
    * Updated React type definitions to match React 19.1.
  * **SuperTokens Configuration:**
    * Updated `supertokens.ts` with modern configuration syntax.
    * Enhanced theming to match Mantine 7.17.4 design system.
    * Added proper TypeScript typing for improved type safety.
  * **Authentication Components:**
    * Refactored login and signup pages to use SuperTokens auth-react functions directly.
    * Improved form validation and error handling.
    * Enhanced UI with Mantine 7.17.4 components.
  * **Main Application:**
    * Updated the main entry point with proper Mantine provider configuration.
    * Added TypeScript environment variable declarations for better type safety.
* [2025-04-17 12:34:00] - **SuperTokens Implementation:**
  * **Backend Integration:**
    * Added `supertokens-python-sdk` dependency to the backend.
    * Created configuration module in `backend/app/features/auth/supertokens_config.py`.
    * Implemented async-compatible user linking between SuperTokens and our database.
    * Added session verification middleware to protect the `/agent/interact` endpoint.
    * Modified the `User` model to include a `supertokens_user_id` field.
  * **Frontend Integration:**
    * Added `supertokens-web-js` dependency to the frontend.
    * Created a catch-all route for the pre-built authentication UI.
    * Updated the API client to use SuperTokens session management.
    * Added login/logout functionality to the main layout.
    * Created protected dashboard page that requires authentication.
* [2025-04-18 13:00:00] - **Vite Alias for @tabler/icons-react Implementation:**
  * Added an alias to `frontend-react/vite.config.ts` within `resolve.alias`:
    `'@tabler/icons-react': '@tabler/icons-react/dist/esm/icons/index.mjs'`
  * Ensured `@tabler/icons-react` was *not* present in `optimizeDeps.exclude`.
  * Kept `@tabler/icons-react` in `optimizeDeps.include` (though the alias is the primary mechanism).
* [2025-04-18 13:06:00] - **Nginx Reverse Proxy and CORS Implementation:**
  * Nginx configuration is defined in `reverse-proxy.conf`.
  * Docker Compose (`docker-compose.yaml`) mounts `reverse-proxy.conf` to `/etc/nginx/conf.d/default.conf` in the `nginx` service.
  * CORS headers and OPTIONS handling are configured within `location` blocks in `reverse-proxy.conf`.
  * FastAPI CORS middleware is configured in `backend/app/main.py` using settings from `backend/app/config.py`.
  * Uvicorn `--proxy-headers` flag is set in the `backend` service command in `docker-compose.yaml`.
* [2025-04-18 13:26:00] - **Refine Proxy Strategy Implementation:**
  * In `reverse-proxy.conf`, within the `location /auth/ { ... }` block (lines 40-65):
    * Keep the `if ($request_method = 'OPTIONS') { ... }` block (lines 43-52).
    * Remove the non-OPTIONS `add_header` lines (55-56).
    * Remove the `proxy_pass` directive (line 58) and associated `proxy_*` directives (lines 59-64).
  * Add a `server.proxy` configuration to `frontend-react/vite.config.ts` targeting `http://backend:8000` for the `/auth` path.
* [2025-04-18 13:40:01] - **Signup Form Field Mismatch:** Diagnosed 400 error on signup due to frontend sending 'username' field while backend SuperTokens config only expected 'email' and 'password'. Decided to modify backend config (`backend/app/features/auth/supertokens_config.py`) to accept 'username' using `InputFormField`.
133 | * [2025-04-18 14:30:00] - Fix SQLAlchemy Polymorphic Relationship Errors: Add `foreign()` annotation to `primaryjoin` conditions in relationships linking back to `EvaluationResult` (e.g., `Project.evaluation_results_link`, `AudienceAvatar.evaluation_results`) to resolve `InvalidRequestError` during mapper initialization.
134 | * [2025-04-18 14:30:00] - Fix Missing DB Column Error: Generate and apply Alembic migration to add the `supertokens_user_id` column to the `users` table, resolving `UndefinedColumnError`.
135 | * [2025-04-18 14:30:00] - Fix SuperTokens User Sync (404 Error): Modify SuperTokens `sign_up_post` and `sign_in_post` API overrides to manually create/manage `AsyncSession` using `async_session_factory` instead of relying on context injection, ensuring user records are created/linked in the local DB.
136 | * [2025-04-18 14:30:00] - Enhance User Profile Schema: Add `created_at` field to the `UserProfile` Pydantic schema (`schemas/user.py`) to include the account creation date in the profile endpoint response.
137 | * [2025-04-18 15:00:00] - **Standardize HTTP Status Code for "User Not Found" Error:** The code review identified inconsistent usage of HTTP status codes (404 vs 403) for the scenario where a valid SuperTokens session exists, but the corresponding user record is not found in the local database. We decided to standardize on `403 Forbidden` as it more accurately reflects the situation: the user is authenticated but not authorized to access the resource due to the missing local record. This improves consistency and provides a clearer signal to the client.
138 | * [2025-04-18 15:05:00] - **Create `get_required_user_from_session` Dependency:** The code review identified duplicated logic in the API routers for fetching the user based on the SuperTokens session ID and handling the "user not found" error. To address this, we created a new FastAPI dependency, `get_required_user_from_session`, in `features/auth/supertokens_config.py`. This dependency encapsulates the user fetching logic and raises an `HTTPException(403)` if the user is not found, simplifying the router code and ensuring consistency.
139 | * [2025-04-18 15:10:00] - **Centralize `APP_BASE_URL` in `config.py`:** The code review identified a hardcoded `PROXY_ADDRESS` in `features/auth/supertokens_config.py`. To improve maintainability and configuration management, we moved this value to `config.py` as `APP_BASE_URL` and updated `supertokens_config.py` to use `settings.APP_BASE_URL`.
140 | * [2025-04-18 15:24:00] - **Remove Redundant Frontend Auth Code Implementation:**
141 |   * Deleted `frontend-react/src/layouts/AuthLayout.tsx`.
142 |   * Deleted `frontend-react/src/routes/ProtectedRoute.tsx`.
143 |   * Modified `frontend-react/src/services/apiService.ts` to remove the `authToken` property, `setAuthToken` method, and the logic adding the `Authorization: Bearer` header. Adjusted return types to `Promise<T | null>` to handle empty responses correctly.
144 | * [2025-04-18 16:16:00] - Added `username` field to backend `User` model and API response schema (`UserProfile`). Rationale: Required to display user-provided username on the frontend profile page. Implications: Required database migration and update to SuperTokens signup logic to save the username.
145 |   * Deleted `frontend-react/src/services/authService.ts`.
146 | * [2025-04-20 09:05:37] - **Decision:** Adopted the Python subdirectory/module + `__init__.py` re-export pattern for organizing the `backend/app/shared/` directory.
147 | **Rationale:** This pattern balances internal code organization (keeping code in specific module files like `exceptions.py`) with a clean external import interface (allowing imports directly from `app.shared.<subdirectory>`). It avoids overcrowding `__init__.py` files while providing a stable public API for shared components.
148 | **Implementation Details:** Created `__init__.py` files in `shared/clients/`, `shared/constants/`, `shared/exceptions/`, `shared/schemas/`, and `shared/utils/`. Re-exported relevant items from module files (e.g., `exceptions.py`, `constants.py`) within their respective `__init__.py` files.
149 | * [2025-04-20 09:38:37] - Implemented prompt and tool versioning strategy: hybrid storage, ENV VARs for defaults, optional YAML override, configurable fallback, DB trigger, startup validation.
150 | *   **Prompts/Tools Files:** Stored as versioned files in Git (`features/.../prompts/`, `shared/prompts/`, `features/.../tools.py`, `shared/tools/`).
151 | *   **Default Pipeline Tags:** Configured via required ENV VARs (`DEFAULT__{TYPE}__PIPELINE_TAG`), loaded into Pydantic Settings (e.g., `DEFAULT_CHAT_PIPELINE_TAG`, `DEFAULT_CREATORDNA_PIPELINE_TAG`).
152 | *   **Default Prompt Version (Fallback):** The fallback prompt version is defined by the `DEFAULT_PROMPT_VERSION` ENV VAR (defaulting to "v1" if not set). This version is used if the override config file doesn't exist, doesn't list the active tag, doesn't list the pipeline type for the active tag, or doesn't list a specific prompt for that pipeline type within the active tag.
153 | *   **Override Configuration File:** An optional YAML file (path configurable via `PIPELINE_TAGS_CONFIG` ENV VAR, default e.g., `./pipeline-tags.yaml`) maps pipeline tags to specific prompt versions using a nested structure: `{tag: {pipeline_type: {prompt_name: version_string}}}`.
154 | *   **Override Trigger:** Optional, nullable `pipeline_tag` string column on `background_jobs` table.
155 | *   **Startup Validation:** Checks parse validity of the override file (if present) and existence of all prompt files required by the *default pipeline tags* (using the YAML mapping or the `DEFAULT_PROMPT_VERSION` fallback). Logs effective configuration.
156 | * [2025-04-19 10:39:00] - **Implementation Details:** Implemented the core structure for the minimal chat interface, including backend API endpoint (`backend/app/api/routers/chat_router.py`), service (`backend/app/services/chat_service.py`), basic Haystack/Portkey integration structure (`backend/app/ai/dependencies.py`, `backend/app/ai/chat_pipeline.py`), and frontend UI components (`frontend/src/components/ChatInput.tsx`, `frontend/src/components/MessageList.tsx`, `frontend/src/pages/ChatPage.tsx`) and routing (`frontend/src/routes/index.tsx`). Addressed reported TypeScript errors in frontend components and a backend ImportError related to schemas (`backend/app/api/schemas.py`).
157 | * [2025-04-20 12:20:00] - Decision: Resolve Pydantic `NameError` during chat router startup.
158 | 170 | **Rationale:** A `NameError: Fields must not use names with leading underscores` occurred during application startup when the chat router was loaded. Debugging isolated the issue to the `get_chat_service` dependency function, specifically when injecting the `Settings` `BaseSettings` model using `FastAPI.Depends()`. Further testing showed that `Settings = Depends(get_settings)` worked correctly in other contexts (e.g., `/health/test-settings` endpoint), which lead to the discovery that using get_settings in conjunction with lru_cache instead of referencing `Settings` directly solved the problem.
159 | 171 |
160 | 172 | * [2025-04-20 12:33:27] - Decision: Manually correct Alembic migration script after autogenerate included unintended changes.
161 | 173 | **Rationale:** The `alembic revision --autogenerate` command incorrectly detected a type change on the `chat_messages.session_id` column and included it in the migration script for adding `pipeline_tag` to `background_jobs`. Attempting to apply this script failed due to a `DatatypeMismatchError`. Manually editing the generated script to remove the `chat_messages` alteration was necessary to successfully apply the intended migration.
162 | 174 | **Implementation Details:** Edited `backend/app/db/migrations/versions/d7a0cedf8349_add_pipeline_tag_to_background_jobs.py` to remove the `op.alter_column('chat_messages', ...)` calls in both the `upgrade` and `downgrade` functions.
163 | 175 |
164 | 176 | * [2025-04-20 12:35:30] - Decision: Clarify availability of `pipeline_tag` in background task context.
165 | 177 | **Rationale:** The implementation plan noted that the `pipeline_tag` from the `background_jobs` table needed to be passed to the `PromptService` calls within background tasks. Upon examining the SAQ worker code, it was determined that the `pipeline_tag` is already accessible within the task function's `Context` object via `ctx.get("job").pipeline_tag`. The plan was updated to reflect this, indicating that the implementation involves using this existing context rather than requiring explicit passing from the `before_process` hook.
166 | 178 | **Implementation Details:** Updated the description for Step 7 in `docs/prompt_tool_versioning_plan.md` to clarify that the `pipeline_tag` is available in the task context.
167 | 179 |
168 | 180 | [2025-04-20 12:51:53] - Decision: Standardize test data management using `factory-boy` (version 3.3.3).
169 | 181 | **Rationale:** Provides programmatic generation of test data, reducing boilerplate and promoting consistency
170 | 182 | **Implementation Details:** Will integrate `factory-boy` into the backend test suite, starting with key models like User and ChatMessage
171 | 183 |
172 | 184 | * [2025-04-20 18:43:11] - Decision: Remove the `GeneratedStructure` model and all its references from the codebase and database schema.
173 | 185 |   **Rationale:** The `GeneratedStructure` model was causing persistent `sqlalchemy.exc.InvalidRequestError` during mapper initialization due to complex relationships and foreign key ambiguities after model refactoring. Temporarily removing the model simplifies the schema and allows progress on other tasks.
174 | 186 |   **Implementation Details:** Removed the `GeneratedStructure` class definition from `backend/app/db/models/structure.py`. Removed foreign key columns and relationships referencing `GeneratedStructure` in `backend/app/db/models/project.py`, `backend/app/db/models/job.py`, and `backend/app/db/models/script.py`. Updated `backend/app/db/models/__init__.py` to remove imports and `__all__` entry.
175 | 187 |
176 | 188 | * [2025-04-20 18:43:11] - Decision: Manually create and apply an Alembic migration to drop foreign key constraints and the `generated_structures` table.
177 | 189 |   **Rationale:** Alembic's autogenerate failed to detect the removal of foreign key definitions in the models and did not generate the necessary `drop_constraint` operations, leading to `DependentObjectsStillExistError` when attempting to drop the table. Manual intervention was required to explicitly drop the constraints before the table.
178 | 190 |   **Implementation Details:** Generated an empty migration script (`alembic revision -m "..."`). Manually added `op.drop_constraint('script_sections_generated_structure_id_fkey', 'script_sections', type_='foreignkey')`, `op.drop_constraint('projects_selected_structure_id_fkey', 'projects', type_='foreignkey')`, and `op.drop_table('generated_structures')` to the `upgrade()` function. Applied the migration using `alembic upgrade head` after manually stamping the database to the previous revision.
179 | * [2025-04-20 18:57:00] - Decision: Refactor chat pipeline to use Haystack Agent.
180 |   **Rationale:** To improve pipeline structure, leverage Agent capabilities for managing conversation flow and tools, and prepare for future function calling implementation.
181 |   **Implementation Details:** Modified `backend/app/features/chat/chat_pipeline.py` to instantiate and add a Haystack `Agent` component instead of the `OpenAIChatGenerator` directly. Configured the Agent with the LLM generator and the fetched `system_prompt_content`.
182 | * [2025-04-20 18:57:00] - Decision: Implement LLM-based greeting generation in the `/greeting` endpoint.
183 |   **Rationale:** To provide a dynamic and personalized greeting based on user interaction history, fulfilling a planned feature requirement.
184 |   **Implementation Details:** Modified `backend/app/api/routers/chat.py` to fetch recent user chat history, fetch the `greeting` prompt template via `PromptService`, format the prompt with user details and history, and use an `OpenAIChatGenerator` to generate the greeting text.
185 | * [2025-04-20 19:29:00] - Debugging: Resolved `TypeError: build_chat_pipeline() got an unexpected keyword argument 'override_pipeline_tag'` by correcting the import path for `build_chat_pipeline` in `chat_service.py`.
186 | * [2025-04-20 19:29:00] - Debugging: Resolved `ValidationError` in `/history` endpoint by aligning `ChatMessageResponse` schema types (UUID, datetime) with ORM model types.
187 | * [2025-04-20 19:29:00] - Debugging: Resolved `AttributeError: 'SecretStr' object has no attribute 'resolve_value'` during LLM generator initialization by wrapping the SecretStr API key in Haystack's `Secret.from_token()`.
188 | * [2025-04-20 19:29:00] - Debugging: Resolved `TypeError: Agent.__init__() got an unexpected keyword argument 'llm'` by using the correct keyword argument `chat_generator` when instantiating the Agent.
189 | * [2025-04-20 19:29:00] - Debugging: Resolved `ValueError: ToolInvoker requires at least one tool.` by providing the `general_tools` list to the Agent constructor.
[2025-04-21 14:22:20] - Removed multiple SQLAlchemy models as per user request. This involved deleting model definition files and removing relationships and factory definitions in other files. The removed models include: PromptTemplate, AudienceAvatar, EducationalFramework, ContentSource, SupportingMaterial, RetrievableText, ScriptSection, SafetyAnalysis, DnaDetailedAnalysis, ProjectSettingsTemplate, ProjectSettings, ProjectTopic, ResearchAnalysis, Feedback, ProjectIdeaValidation, ProjectAudienceAvatar, ProjectTopicMaterial.
[2025-04-21 14:25:40] - Removed the CreatorDnaProfile SQLAlchemy model as per user request. This involved deleting the model definition file and removing relationships and factory definitions in other files.
190 | * [2025-04-20 19:29:00] - Debugging: Resolved `TypeError: cannot pickle 'module' object` by removing the unpicklable `UserService` instance from the pipeline input data.
