# Frontend React Rearchitecture Plan (React 19.1 / Mantine 7.17.4)

**Objective:** Rearchitect the `frontend-react` application to use React 19.1 and Mantine 7.17.4, update dependencies, remove the unused `supertokens-web-js` package, and verify the existing `supertokens-auth-react` implementation against official documentation.

---

## Phase 1: Dependency Management

1.  **Update Core Libraries:**
    *   Modify `frontend-react/package.json` to specify React `19.1.0` and React DOM `19.1.0`.
    *   Modify `frontend-react/package.json` to specify Mantine packages (`@mantine/core`, `@mantine/hooks`, `@mantine/form`, `@mantine/notifications`, etc.) version `7.17.4`.
2.  **Remove Unused SuperTokens:**
    *   Remove the `supertokens-web-js` dependency from `frontend-react/package.json`.
3.  **Review & Update Other Dependencies:**
    *   Analyze other dependencies (e.g., `@vitejs/plugin-react`, testing libraries like `@testing-library/react`, `vitest`, `@playwright/test`, ESLint plugins) for compatibility with React 19.1. Update as necessary based on their respective documentation/changelogs.
4.  **Install Updated Dependencies:**
    *   Run `npm install` (or equivalent package manager command like `pnpm install` or `yarn install`) within the `frontend-react` directory to install the updated versions and remove the old ones. Resolve any peer dependency conflicts.

## Phase 2: Code Adaptation & Verification

1.  **Address React 19 Changes:**
    *   Review the React 19.1 documentation (https://react.dev/reference/react) for breaking changes or new patterns (e.g., ref handling, context API changes, potential hooks behavior adjustments).
    *   Refactor components as needed to align with React 19.1 standards.
2.  **Address Mantine 7.17.4 Changes:**
    *   Review the Mantine changelogs between the current version (`^7.4.0`) and `7.17.4` for any breaking changes or deprecated components/props.
    *   Update component usage as required.
3.  **Verify SuperTokens Implementation:**
    *   Review the existing SuperTokens integration (`config/supertokens.ts`, `contexts/AuthContext.tsx`, `hooks/useAuth.ts`, `services/authService.ts`, `routes/ProtectedRoute.tsx`, `pages/auth/`) against the official `supertokens-auth-react` documentation (https://supertokens.com/docs/auth-react/modules.html).
    *   Ensure all necessary modules are imported correctly and best practices are followed. Make minor adjustments if needed for alignment.
4.  **Static Analysis & Linting:**
    *   Run `npm run lint` to catch any syntax errors or style issues introduced during the refactoring. Fix any reported problems.

## Phase 3: Testing

1.  **Unit/Integration Tests:**
    *   Run the existing test suite using `npm run test`. Address any failures caused by the dependency updates or code changes.
2.  **End-to-End Tests:**
    *   Run the Playwright tests using `npm run test:e2e`. Debug and fix any failing E2E tests.
3.  **Manual Testing:**
    *   Manually test the core application flows, focusing on:
        *   Login and Signup functionality.
        *   Navigation between public and protected routes.
        *   Profile page access.
        *   Overall UI rendering and responsiveness with the updated Mantine components.

## Phase 4: Documentation (Memory Bank Update)

1.  **Update `decisionLog.md`:** Add an entry detailing the decision to upgrade to React 19.1/Mantine 7.17.4 and remove `supertokens-web-js`.
2.  **Update `progress.md`:** Add a new task tracking the completion of this rearchitecture effort.
3.  **Update `systemPatterns.md`:** Update the React and Mantine versions listed. Confirm the SuperTokens pattern reflects the sole use of `supertokens-auth-react`.
4.  **Update `activeContext.md`:** Reflect that the current focus is on the React frontend and the completion of this task.

## Plan Visualization

```mermaid
sequenceDiagram
    participant Arch as Architect
    participant User
    participant Code as Code Mode
    participant MB as Memory Bank

    Arch->>User: Present Plan
    User->>Arch: Approve Plan
    Arch->>User: Offer to save plan?
    User->>Arch: Confirm save/skip
    Arch->>MB: (Optional) Write plan to file
    Arch->>User: Request switch to Code Mode
    User->>Code: Approve switch

    Code->>Code: Phase 1: Dependency Management (Update package.json, npm install)
    Code->>Code: Phase 2: Code Adaptation (Refactor for React 19/Mantine, Verify SuperTokens)
    Code->>Code: Phase 3: Testing (Unit, E2E, Manual)
    Code->>MB: Phase 4: Update Memory Bank Files
    Code->>User: Report Completion / Request Review
