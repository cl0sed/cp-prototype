# Plan: Integrate SuperTokens Frontend SDK

**Goal:** Resolve CORS issues and simplify frontend authentication by integrating the official SuperTokens frontend SDK.

**Steps:**

1.  **Install Frontend Dependencies:**
    *   Add `supertokens-auth-react` to `frontend-react/package.json`. Adjust version based on React 18 compatibility.

2.  **Configure SuperTokens Frontend:**
    *   Modify `frontend-react/src/main.tsx` to initialize SuperTokens:
        *   Use correct `appInfo` (matching backend `apiDomain`, `websiteDomain`, `apiBasePath`, `websiteBasePath`).
        *   Configure `recipeList` (EmailPassword, Session).

3.  **Refactor Routing and Authentication:**
    *   Update `frontend-react/src/routes/index.tsx`:
        *   Wrap the application with `SuperTokensWrapper`.
        *   Use `getSuperTokensRoutesForReactRouterDom` (from `supertokens-auth-react/recipe/session/prebuiltui`) to handle auth routes and UIs.
    *   Replace custom `ProtectedRoute.tsx` with SuperTokens' `SessionAuth` component.

4.  **Remove Custom Auth Implementation:**
    *   Remove `AuthContext.tsx` and `useAuth.ts`.
    *   Remove `authService.ts`.
    *   Simplify `apiService.ts` if only needed for non-auth API calls.

5.  **Update Pages:**
    *   Remove custom `LoginPage.tsx` and `SignupPage.tsx`.
    *   Update `ProfilePage.tsx` to use SuperTokens session hooks (e.g., `useSessionContext`) for user data.

6.  **Verify Backend Configuration:**
    *   Ensure `backend/app/features/auth/supertokens_config.py` `InputAppInfo` settings match the frontend.
    *   Keep the main FastAPI CORS middleware in `backend/app/main.py` correctly configured for any non-SuperTokens API endpoints.

**Rationale:**

*   Aligns with the recommended SuperTokens integration pattern.
*   Delegates complex auth flows, session management, and API communication (including CORS for auth routes) to the SDK.
*   Simplifies frontend code by removing custom authentication logic.
