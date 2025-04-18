# Frontend Rewrite Plan: SvelteKit + Flowbite Svelte + Custom Auth

This document outlines the plan to rewrite the existing SvelteKit frontend application using the Flowbite Svelte component library and implement custom authentication UI integrated with SuperTokens.

**Goal:** Replace the current UI implementation (including SuperTokens pre-built UI) with a consistent, modern interface built with Flowbite Svelte components.

## Phase 1: Setup & Core Authentication Refactor

1.  **Install & Configure Flowbite Svelte:** Add Flowbite Svelte and its dependencies (including Tailwind CSS) to the `frontend/` project and configure them according to the Flowbite Svelte documentation.
2.  **Remove SuperTokens Pre-built UI:** Delete the catch-all route currently handling the SuperTokens UI (`frontend/src/routes/auth/[[...path]]/+page.svelte`).
3.  **Create Custom Auth Routes & Components:**
    *   Define new routes (e.g., `/auth/signup`, `/auth/signin`).
    *   Build custom `SignUp.svelte` and `SignIn.svelte` components using Flowbite Svelte form elements (Inputs, Buttons, Labels, Alerts for validation/errors).
4.  **Integrate Custom Auth UI with SuperTokens SDK:** Connect the new Flowbite-based Sign Up and Sign In forms to the corresponding SuperTokens client SDK functions (`signUp`, `signIn`). Handle loading states and display errors using Flowbite components (e.g., Spinners, Alerts).
5.  **Refactor Layout & Navigation:** Update the main layout (`+layout.svelte`) to use Flowbite components (e.g., Navbar, Dropdown for user menu) and manage the display of Login/Logout options based on the SuperTokens session state.

## Phase 2: Protected Routes & Dashboard

6.  **Implement Authentication Guards:** Ensure existing or create new mechanisms (e.g., in `+layout.server.js` or `hooks.server.js`) to check the SuperTokens session and protect routes that require authentication. Redirect unauthenticated users to the new Sign In page.
7.  **Create User Profile Dashboard:**
    *   Create a new route for the dashboard (e.g., `/dashboard`).
    *   Build a skeleton `Dashboard.svelte` component using Flowbite layout elements (e.g., Cards, Grid).
    *   Initially, fetch and display the authenticated user's email address (obtained via SuperTokens session info).
    *   Ensure this route is protected by the authentication guard.

## Phase 3: General UI Refactoring & Polish

8.  **Refactor Existing Components:** Gradually refactor other existing UI components (like the chat interface mentioned in `progress.md` Task 6a-3) to use Flowbite Svelte components for consistency.
9.  **Implement Loading/Error States:** Systematically add loading indicators (e.g., Flowbite Spinners) and user-friendly error messages (e.g., Flowbite Alerts, Toasts) throughout the application for API calls and other asynchronous operations.
10. **Ensure Responsiveness:** Leverage Flowbite's utility classes and responsive component variants to ensure the application looks and works well on different screen sizes.
11. **Documentation & Memory Bank:** Update `systemPatterns.md` and `decisionLog.md` in the Memory Bank to reflect the use of Flowbite Svelte and the custom authentication UI approach. Update `progress.md` with new/refined tasks.

## Authentication Flow Diagram

```mermaid
graph TD
    subgraph "Frontend (SvelteKit + Flowbite Svelte)"
        A[User visits /auth/signin] --> B(SignIn.svelte Component);
        B -- Enters Credentials --> C{Submit Form};
        C -- Calls --> D[SuperTokens Client SDK: signIn()];
        D -- Success --> E[Redirect to /dashboard];
        D -- Failure --> F[Display Error in SignIn.svelte (Flowbite Alert)];

        G[User visits /auth/signup] --> H(SignUp.svelte Component);
        H -- Enters Details --> I{Submit Form};
        I -- Calls --> J[SuperTokens Client SDK: signUp()];
        J -- Success --> K[Redirect to /dashboard or /auth/signin];
        J -- Failure --> L[Display Error in SignUp.svelte (Flowbite Alert)];

        M[User visits /dashboard] --> N{Auth Guard Check};
        N -- Authenticated --> O(Dashboard.svelte Component);
        N -- Not Authenticated --> P[Redirect to /auth/signin];

        Q[User clicks Logout (Flowbite Button/Dropdown)] --> R[SuperTokens Client SDK: signOut()];
        R --> S[Redirect to /auth/signin or /];
    end

    subgraph "Backend (FastAPI + SuperTokens)"
        D --> T(SuperTokens Core: Verify Credentials);
        J --> U(SuperTokens Core: Create User);
        N --> V(SuperTokens Core: Verify Session);
        R --> W(SuperTokens Core: Revoke Session);
    end

    T --> D;
    U --> J;
    V --> N;
    W --> R;

    style F fill:#f99,stroke:#333,stroke-width:2px;
    style L fill:#f99,stroke:#333,stroke-width:2px;
    style P fill:#f99,stroke:#333,stroke-width:2px;
