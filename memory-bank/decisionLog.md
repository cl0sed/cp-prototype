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
## Rationale
* [2025-04-18 13:06:00] - Confirm Nginx Reverse Proxy and CORS Configuration

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

## Implementation Details

* [2025-04-18 13:06:00] - **Nginx Reverse Proxy and CORS Rationale:**
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

[2025-04-18 13:40:01] - **Signup Form Field Mismatch:** Diagnosed 400 error on signup due to frontend sending 'username' field while backend SuperTokens config only expected 'email' and 'password'. Decided to modify backend config (`backend/app/features/auth/supertokens_config.py`) to accept 'username' using `InputFormField`.

* [2025-04-18 14:30:00] - Fix SQLAlchemy Polymorphic Relationship Errors: Add `foreign()` annotation to `primaryjoin` conditions in relationships linking back to `EvaluationResult` (e.g., `Project.evaluation_results_link`, `AudienceAvatar.evaluation_results`) to resolve `InvalidRequestError` during mapper initialization.
* [2025-04-18 14:30:00] - Fix Missing DB Column Error: Generate and apply Alembic migration to add the `supertokens_user_id` column to the `users` table, resolving `UndefinedColumnError`.
* [2025-04-18 14:30:00] - Fix SuperTokens User Sync (404 Error): Modify SuperTokens `sign_up_post` and `sign_in_post` API overrides to manually create/manage `AsyncSession` using `async_session_factory` instead of relying on context injection, ensuring user records are created/linked in the local DB.
* [2025-04-18 14:30:00] - Enhance User Profile Schema: Add `created_at` field to the `UserProfile` Pydantic schema (`schemas/user.py`) to include the account creation date in the profile endpoint response.
* [2025-04-18 15:00:00] - **Standardize HTTP Status Code for "User Not Found" Error:** The code review identified inconsistent usage of HTTP status codes (404 vs 403) for the scenario where a valid SuperTokens session exists, but the corresponding user record is not found in the local database. We decided to standardize on `403 Forbidden` as it more accurately reflects the situation: the user is authenticated but not authorized to access the resource due to the missing local record. This improves consistency and provides a clearer signal to the client.
* [2025-04-18 15:05:00] - **Create `get_required_user_from_session` Dependency:** The code review identified duplicated logic in the API routers for fetching the user based on the SuperTokens session ID and handling the "user not found" error. To address this, we created a new FastAPI dependency, `get_required_user_from_session`, in `features/auth/supertokens_config.py`. This dependency encapsulates the user fetching logic and raises an `HTTPException(403)` if the user is not found, simplifying the router code and ensuring consistency.
* [2025-04-18 15:10:00] - **Centralize `APP_BASE_URL` in `config.py`:** The code review identified a hardcoded `PROXY_ADDRESS` in `features/auth/supertokens_config.py`. To improve maintainability and configuration management, we moved this value to `config.py` as `APP_BASE_URL` and updated `supertokens_config.py` to use `settings.APP_BASE_URL`.

* [2025-04-18 15:24:00] - **Remove Redundant Frontend Auth Code Implementation:**
  * Deleted `frontend-react/src/layouts/AuthLayout.tsx`.
  * Deleted `frontend-react/src/routes/ProtectedRoute.tsx`.
  * Modified `frontend-react/src/services/apiService.ts` to remove the `authToken` property, `setAuthToken` method, and the logic adding the `Authorization: Bearer` header. Adjusted return types to `Promise<T | null>` to handle empty responses correctly.

[2025-04-18 16:16:00] - Added `username` field to backend `User` model and API response schema (`UserProfile`). Rationale: Required to display user-provided username on the frontend profile page. Implications: Required database migration and update to SuperTokens signup logic to save the username.
  * Deleted `frontend-react/src/services/authService.ts`.
