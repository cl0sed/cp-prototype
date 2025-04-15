# Frontend README - AI Video Creation Platform

*(Project Status: PoC Phase - As of: April 15, 2025)*

## 1. Overview

This directory houses the frontend application for the AI Video Creation Platform. Built with SvelteKit and Svelte 5, it provides the user interface for creators to interact with the platform's AI capabilities, primarily through a conversational agent interface complemented by necessary GUI elements.

**Note:** This README focuses specifically on the frontend. For overall project goals, architecture, monorepo structure, backend details, and shared configurations, please refer to the **root `README.txt`**.

## 2. Getting Started

### Prerequisites

* Node.js & a package manager (npm recommended, pnpm/yarn acceptable)
* Docker & Docker Compose (for running the full stack locally via the root `docker-compose.yml`)

### Creating the Project (If starting fresh)

If you haven't initialized the project in this directory yet:

    # Navigate to the frontend/ directory
    cd path/to/cp-prototype/frontend

    # Create a new project in the current directory
    npx sv create .

Follow the prompts: Choose the "SvelteKit App (skeleton)" template, select "Yes, using TypeScript syntax", and **skip** adding extra tools like ESLint, Prettier, etc. (we'll configure those manually based on project standards).

### Installing Dependencies

Once the project files exist, install dependencies:

    npm install

(Or `pnpm install` / `yarn install`)

### Running the Development Server

To start the Vite development server:

    npm run dev

To start the server and automatically open the app in a new browser tab:

    npm run dev -- --open

Access the frontend at `http://localhost:5173` (default port).

### Building for Production

To create a production version of the frontend app:

    npm run build

You can preview the production build locally with `npm run preview`. Actual deployment uses the `frontend/Dockerfile` and is typically managed via the root project's CI/CD or Docker Compose setup.

## 3. Technology Stack & Key Decisions

* **Framework:** SvelteKit
* **UI Language:** Svelte 5 (**Runes Mode Enabled and Strictly Required**)
* **Build Tool:** Vite
* **Styling:** Standard CSS (scoped), PostCSS/SCSS via `vitePreprocess` if needed. Global styles in `src/app.css`.
* **State Management:** Primarily Svelte 5 Runes (`$state`, `$derived`). Shared state via `$state` in `$lib/state/*.svelte.js` preferred. Traditional stores (`svelte/store`) reserved for complex cases.
* **Type Checking:** TypeScript / JSDoc (via `tsconfig.json` / `jsconfig.json`).

## 4. Project Structure Overview

```plaintext
frontend/
├── src/                  # SvelteKit source code
│   ├── app.html          # Main HTML template
│   ├── app.d.ts          # Ambient TypeScript definitions
│   ├── app.css           # Global styles
│   ├── hooks.server.js   # Server-side hooks
│   ├── hooks.client.js   # Client-side hooks
│   │
│   ├── lib/              # Reusable frontend modules ($lib alias)
│   │   ├── components/   # UI Components
│   │   ├── services/     # API Client
│   │   ├── state/        # Preferred: Shared reactive state modules (.svelte.js/.ts)
│   │   ├── types/        # TypeScript definitions
│   │   └── utils/        # Helper functions
│   │
│   └── routes/           # Application pages and layouts
│       └── ...
│
├── static/               # Static assets (favicon, images)
├── tests/                # Frontend automated tests
├── Dockerfile            # Builds PRODUCTION frontend image
├── package.json          # Node.js dependencies
├── svelte.config.js      # SvelteKit configuration
├── vite.config.js        # Vite configuration
├── tsconfig.json         # (If using TS) TypeScript configuration
├── .prettierrc.json      # Formatter config
├── .eslintrc.cjs         # Linter config
└── README.md             # This file
```

(Refer to the **root `README.txt`** for the full monorepo layout).

## 5. Configuration

This SvelteKit application uses Vite's environment variables system to manage environment-specific configuration:

### API Configuration

The application requires the following environment variable to connect to the backend API:

* `PUBLIC_API_BASE_URL`: Base URL for the backend API.

These are configured in different ways depending on the environment:

* **Development**: Values in `.env.development` are used when running `npm run dev`. Set this to `http://localhost:8000` to connect to the local backend via Docker Compose.
* **Production**: Values must be provided via environment variables in the deployment environment (e.g., PaaS settings, Docker environment variables). Use `.env.production` for reference or non-sensitive defaults only.
* **Example Config**: See `.env.example` for required variables.

### How to Access Environment Variables

Within the application code (client-side safe), access these variables using Vite's `import.meta.env`:

    // Example from src/lib/services/apiClient.ts (or .js)
    const baseApiUrl = import.meta.env.PUBLIC_API_BASE_URL;

    async function someApiCall() {
      const response = await fetch(`${baseApiUrl}/some-endpoint`);
      // ...
    }

**Note**: Only variables prefixed with `PUBLIC_` (the default in SvelteKit's config) are accessible in client-side code. Ensure `app.d.ts` is updated for TypeScript type safety if using TS.

## 6. Core Svelte 5 / SvelteKit Development Practices (**MANDATORY**)

**Adherence to these Svelte 5 practices is required for all frontend development.** Refer to the official [Svelte Documentation (`https://svelte.dev/llms-full.txt`)](https://svelte.dev/llms-full.txt) and the root `README.txt` for context.

* **Runes Mode:** All components **must** operate in Runes mode. Legacy reactivity (`export let` for props, `$:` for reactions) is disallowed.
* **Reactivity (`$state`, `$derived`, `$effect`):**
    * Employ `$state` for all reactive component state.
    * Utilize `$derived` for values computed from other reactive state. Avoid manual state synchronization.
    * Employ `$effect` strictly for side effects reacting to state changes (e.g., DOM manipulation, third-party library calls). Minimize state updates within `$effect`. Use `$effect.pre` for effects requiring execution before DOM updates.
* **Component Props (`$props`, `$bindable`):**
    * Define all component properties using `let { ... } = $props()`. Use JS destructuring for defaults/renaming/rest.
    * Props are immutable by default. **Do not mutate props** from within a child component.
    * Use **Callback Props** (functions passed as props) for child-to-parent communication instead of `createEventDispatcher`.
    * Enable two-way binding only by marking the specific prop with `$bindable()` in the child component.
    * Strongly type props (TypeScript/JSDoc). Use `svelte/elements` types for HTML attribute typings in wrappers.
* **Bindings (`bind:`):**
    * Use `bind:property={value}` for two-way data binding, primarily with form elements (`input`, `select`, `textarea`).
    * When binding component props, ensure the child uses `$bindable()`.
    * Utilize element dimension bindings (`bind:clientWidth`) and `bind:this` where necessary.
* **Event Handling:**
    * Utilize direct event attributes (`onclick={handler}`, `oninput`, etc.). The legacy `on:` directive is disallowed.
    * Handle event logic (like `preventDefault`) within the handler function itself. For `capture`, use the `on...capture` attribute.
* **State Management (Shared):**
    * **Primary Method:** Define shared, cross-component state using `$state` within dedicated modules in `$lib/state/` (e.g., `user.svelte.js`). Import and use this state directly.
    * **Secondary Method:** Reserve `svelte/store` (`writable`, `readable`) only for scenarios demanding complex asynchronous logic, custom subscription mechanisms, or integration with external reactive libraries (e.g., RxJs).
* **Content Projection (Snippets):**
    * Employ snippets (`{#snippet name(params)}...{/snippet}`) and render tags (`{@render snippet(params)}`) exclusively for content projection.
    * Default content projection uses a `children` snippet prop: `let { children } = $props(); {@render children?.()}`.
    * Named content projection uses named snippet props.
    * Legacy `<slot>`, `let:`, and `<svelte:fragment>` are disallowed.
* **Lifecycle:**
    * Use `$effect` for reactions. Use `onMount` for browser-only setup after mount. Use `onDestroy` for cleanup.
    * Legacy `beforeUpdate`/`afterUpdate` are disallowed.
* **Routing:**
    * Follow SvelteKit's filesystem conventions (`src/routes/`).
    * Use `+page.svelte` (pages), `+layout.svelte` (layouts), `+error.svelte` (error boundaries), `+page.js`/`+layout.js` (universal load), `+page.server.js`/`+layout.server.js` (server load/actions), `+server.js` (API endpoints).
    * Utilize `./$types` imports for type safety in route files.
* **Styling:**
    * Leverage default scoped styles within `<style>` tags.
    * Use `:global(...)` explicitly for unscoped CSS when required.
* **Configuration:**
    * `svelte.config.js`: Configure adapter, `vitePreprocess` (if needed for SCSS/advanced TS), aliases.
    * `vite.config.js`: Ensure `@sveltejs/kit/vite` plugin is included. Add other Vite plugins as needed.
    * `tsconfig.json`/`jsconfig.json`: **Must** extend `./.svelte-kit/tsconfig.json`. Ensure compiler options `verbatimModuleSyntax: true` (or equivalent) and `isolatedModules: true` are effectively set.

## 7. Testing

* Implement tests within the `frontend/tests/` directory.
* Use testing frameworks like Vitest (recommended) or Playwright (for E2E).
* **Component Testing:**
    * Instantiate components using `mount` from `svelte`.
    * Use `unmount` for cleanup.
    * Employ `flushSync` from `svelte` after triggering state changes or events before making DOM assertions.
    * Testing logic involving `$effect` or `$derived` may require wrapping in `$effect.root`.
    * Consider `@testing-library/svelte` for user-interaction focused tests.
    * Extract complex logic into testable utility functions outside components where feasible.

## 8. Code Quality

* **Formatting:** Enforced by Prettier (`.prettierrc.json`).
* **Linting:** Enforced by ESLint (`.eslintrc.cjs`) with Svelte plugins.
* **Automation:** Utilize pre-commit hooks (configured at root level) to ensure quality before commits.

## 9. Deployment

* Deployment is handled via the root project setup (Docker, CI/CD workflows).
* The `frontend/Dockerfile` builds the production assets and typically serves them using Nginx.
* Environment-specific configuration (like `PUBLIC_API_BASE_URL`) is managed via runtime environment variables.

**Adherence to the Svelte 5 practices outlined in Section 6 is crucial for maintaining consistency and leveraging the framework's capabilities effectively.**
