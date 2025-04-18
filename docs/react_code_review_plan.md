# React Frontend Code Review Plan

**1. Objective & Scope:**

*   **Goal:** Conduct a detailed code review of the `frontend-react/src` directory, focusing on adherence to team standards, React 19.1 best practices, consistency, performance, accessibility, and the DRY principle.
*   **Key Technologies:** React 19.1, Mantine 7.17.4, SuperTokens (`supertokens-auth-react`), Vite, TypeScript.
*   **Primary Focus Areas:** Code Consistency, React Best Practices (incl. 19.1 features like `use`), State Management, Performance, Accessibility, Reusability (DRY).
*   **Target Directory:** `frontend-react/src` (with specific attention to `pages/auth/` for authentication components as confirmed).

**2. Information Gathering & Context Refinement:**

*   **(Done)** Review Memory Bank files (`productContext.md`, `activeContext.md`, `systemPatterns.md`, `decisionLog.md`, `progress.md`).
*   **(Done)** Analyze high-level project structure (`list_files`).
*   **(Next Steps)** Examine key configuration files using `read_file`:
    *   `frontend-react/package.json` (Verify dependencies, scripts)
    *   `frontend-react/.eslintrc.cjs` (Check linting rules)
    *   `frontend-react/tsconfig.json` (Check TypeScript configuration)
    *   `frontend-react/vite.config.ts` (Check build/dev setup, aliases, proxy)
*   **(Next Steps)** Review core application setup files using `read_file`:
    *   `frontend-react/src/main.tsx` (Root component, providers)
    *   `frontend-react/src/App.tsx` (Main application component, layout structure)
    *   `frontend-react/src/routes/index.tsx` (Routing setup)
*   **(Next Steps)** Review established pattern implementations using `read_file`:
    *   `frontend-react/src/config/supertokens.ts` (Authentication config)
    *   `frontend-react/src/layouts/MainLayout.tsx` & `AuthLayout.tsx` (Layout structure)
    *   `frontend-react/src/services/apiService.ts` & `authService.ts` (API interaction)
    *   `frontend-react/src/routes/ProtectedRoute.tsx` (Route protection mechanism)

**3. Code Review Execution (Iterative Process):**

This phase involves reading and analyzing the codebase component by component, guided by the following checklist:

```mermaid
graph TD
    A[Start Review] --> B{Consistency & Standards};
    B --> B1[Naming Conventions];
    B --> B2[File Structure];
    B --> B3[Styling (Mantine)];
    B --> B4[Linting/Formatting];
    B --> C{React Core & Modern Practices};
    C --> C1[Component Design];
    C --> C2[Hook Usage (Standard)];
    C --> C3[use Hook (React 19.1)];
    C --> C4[Custom Hooks];
    C --> C5[State Management (Context/Actions)];
    C --> C6[Performance Opt.];
    C --> C7[Accessibility (a11y)];
    C --> D{Code Reusability (DRY)};
    D --> D1[Identify Duplication];
    D --> D2[Suggest Abstractions];
    D --> E[Collate Findings];
    E --> F[End Review];

    subgraph "Consistency & Standards"
        B1
        B2
        B3
        B4
    end

    subgraph "React Core & Modern Practices"
        C1
        C2
        C3
        C4
        C5
        C6
        C7
    end

     subgraph "Code Reusability (DRY)"
        D1
        D2
    end
```

*   **Consistency & Standards:**
    *   **Naming:** Check file names (`PascalCase` for components), component names (`PascalCase`), variables/functions (`camelCase`), constants (`UPPER_SNAKE_CASE`).
    *   **Structure:** Verify logical grouping within `src/` (e.g., `components`, `hooks`, `utils`, `pages`, `layouts`, `services`, `config`). Check for misplaced files or unclear organization. Identify potential cleanup (e.g., unused `pages/LoginPage.tsx`).
    *   **Styling:** Ensure consistent use of Mantine components and styling system (`sx` prop, `createStyles`, theme tokens). Look for inline styles or deviations.
    *   **Linting/Formatting:** Confirm ESLint/Prettier rules (from `.eslintrc.cjs`) are being followed. Look for code sections that violate configured rules.
*   **React Core & Modern Practices (incl. React 19.1):**
    *   **Component Design:** Evaluate component size, readability, and composition. Check for prop drilling and suggest Context API or other solutions if needed.
    *   **Hook Usage:** Review `useEffect` dependencies for correctness and potential infinite loops. Assess appropriate use of `useState`, `useContext`, `useReducer`, `useCallback`, `useMemo`, `useRef`.
    *   **`use` Hook:** Specifically look for opportunities or existing implementations using the `use` hook for async operations (e.g., data fetching) or reading context.
    *   **Custom Hooks:** Identify custom hooks, evaluate their necessity, reusability, and adherence to hook rules.
    *   **State Management:** Analyze the current Context API usage (`AuthContext.tsx` mentioned in patterns). Assess its suitability for the application's complexity. Check for potential use or need for React Actions.
    *   **Performance:** Look for unnecessary re-renders. Evaluate the use of `React.memo`, `useMemo`, `useCallback`. Check for large component bundles and opportunities for code splitting (leveraging Vite's capabilities).
    *   **Accessibility (a11y):** Check for semantic HTML usage (e.g., `<button>` vs. styled `<div>`), appropriate ARIA roles/attributes where needed, basic keyboard navigation support, and focus management hints.
*   **Code Reusability & DRY Principle:**
    *   **Identify Duplication:** Look for repeated code blocks, logic, or UI elements across components/pages.
    *   **Suggest Abstractions:** Propose creating reusable components, custom hooks, or utility functions to eliminate redundancy.

**4. Reporting & Deliverables:**

*   The final output will be a detailed code review report (likely in Markdown format).
*   Feedback will be specific, actionable, and include code snippets where necessary to illustrate points. Findings will be categorized according to the areas above (Consistency, React Practices, DRY).

**5. Tooling Strategy:**

*   `read_file`: To examine specific configuration files and source code files (`.tsx`, `.ts`, `.cjs`, `.json`).
*   `search_files`: Potentially used to find specific patterns or anti-patterns across multiple files (e.g., searching for `// eslint-disable`, specific hook usage, inline styles).
*   `list_code_definition_names`: To get a quick overview of functions/components within files if needed.

**6. Plan Confirmation:**

*   **(Done)** Plan approved by user.

**7. Plan Persistence (Optional):**

*   **(Done)** Saving plan to `docs/react_code_review_plan.md`.

**8. Next Steps:**

*   After saving the plan, suggest switching to the appropriate mode (likely `Ask` or `Code`) to perform the review.
