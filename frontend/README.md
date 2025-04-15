# Frontend README - AI Video Creation Platform

*(Project Status: PoC Phase - As of: April 15, 2025)*

## 1. Overview

This directory houses the frontend application for the AI Video Creation Platform. Built with SvelteKit and Svelte 5, it serves as the primary interface for creators, featuring a conversational agent interaction model alongside essential GUI elements.

**Note:** This README focuses specifically on the frontend. For overall project goals, architecture, monorepo structure, backend details, and shared configurations, refer to the **root `README.txt`**[cite: 4276].

## 2. Getting Started

### Prerequisites

* Node.js & a package manager (npm recommended, pnpm/yarn acceptable)
* Docker & Docker Compose (for the full local stack via root `docker-compose.yml`)

### Local Development

1.  **Run Backend:** Ensure backend services (API, DB, Redis) are running (usually `docker-compose up --build -d` from project root).
2.  **Navigate:** `cd frontend/`
3.  **Install:** `npm install`
4.  **Run Dev Server:** `npm run dev`
5.  **Access:** `http://localhost:5173` (default)

### Building for Production

* Frontend build is integrated into the root `docker-compose.yml` build process.
* Manual Build: `npm run build`
* The production image (`frontend/Dockerfile`) typically serves static assets via Nginx.

## 3. Technology Stack & Key Decisions

* **Framework:** SvelteKit
* **UI Language:** Svelte 5 (**Runes Mode Enabled and Strictly Required**)
* **Build Tool:** Vite
* **Styling:** Standard CSS (scoped), PostCSS/SCSS via `vitePreprocess` if needed. Global styles in `src/app.css`.
* **State Management:** Svelte 5 Runes (`$state`, `$derived`). Shared state via `$state` in `$lib/state/*.svelte.js` preferred.
* **Type Checking:** TypeScript / JSDoc (via `tsconfig.json` / `jsconfig.json`).

## 4. Project Structure

* `src/`: SvelteKit application source.
    * `app.html`: Main HTML template (utilize `%sveltekit.*%` placeholders)[cite: 2024, 2025, 2026].
    * `app.d.ts`: Ambient TypeScript definitions (`App.*` namespace).
    * `app.css`: Global CSS styles.
    * `hooks.client.js`/`hooks.server.js`: Client/Server hooks[cite: 2029, 2030].
    * `lib/`: Reusable modules, accessible via `$lib` alias.
        * `components/`: Svelte UI components.
        * `services/`: API client logic.
        * `state/`: **Preferred location for shared reactive state (`$state` in `.svelte.js/.ts` files)**.
        * `types/`: Frontend-specific type definitions.
        * `utils/`: Utility functions.
    * `routes/`: Filesystem-based application routes[cite: 2023].
* `static/`: Static assets (e.g., favicon).
* `tests/`: Frontend automated tests.
* `svelte.config.js`: SvelteKit & Preprocessor configuration[cite: 2034].
* `vite.config.js`: Vite build tool configuration[cite: 2037].
* `tsconfig.json`: (If using TS) TypeScript configuration.
* `package.json`: Dependencies and scripts.
* `.prettierrc.json`/`.eslintrc.cjs`: Code formatting/linting rules.

(See **root `README.txt`**[cite: 4316] for the complete monorepo layout).

## 5. Core Svelte 5 / SvelteKit Development Practices (**MANDATORY**)

**Adherence to these Svelte 5 practices is required for all frontend development.** Refer to the official [Svelte Documentation (`https://svelte.dev/llms-full.txt`)](https://svelte.dev/llms-full.txt)[cite: 74] for detailed explanations.

* **Runes Mode:** All components **must** operate in Runes mode. Legacy reactivity (`export let` for props, `$:` for reactions) is disallowed.
* **Reactivity (`$state`, `$derived`, `$effect`):**
    * Employ `$state` for all reactive component state[cite: 116].
    * Utilize `$derived` for values computed from other reactive state[cite: 162]. Avoid manual state synchronization.
    * Employ `$effect` strictly for side effects reacting to state changes (e.g., DOM manipulation, third-party library calls)[cite: 186]. Minimize state updates within `$effect`. Use `$effect.pre` for effects requiring execution before DOM updates[cite: 219].
* **Component Props (`$props`, `$bindable`):**
    * Define all component properties using `let { ... } = $props()`[cite: 244, 245]. Use JS destructuring for defaults/renaming/rest.
    * Props are immutable by default. **Do not mutate props** from within a child component.
    * Use **Callback Props** (functions passed as props) for child-to-parent communication instead of `createEventDispatcher`.
    * Enable two-way binding only by marking the specific prop with `$bindable()` in the child component[cite: 275].
    * Strongly type props (TypeScript/JSDoc). Use `svelte/elements` types for HTML attribute typings in wrappers[cite: 762, 763].
* **Bindings (`bind:`):**
    * Use `bind:property={value}` for two-way binding, primarily with form elements (`input`, `select`, `textarea`)[cite: 380, 387, 392, 406, 415].
    * When binding component props, ensure the child uses `$bindable()`[cite: 424].
    * Utilize element dimension bindings (`bind:clientWidth`) and `bind:this` where necessary[cite: 418].
* **Event Handling:**
    * Utilize direct event attributes (`onclick={handler}`, `oninput`, etc.)[cite: 307]. The legacy `on:` directive is disallowed.
    * Handle event logic (like `preventDefault`) within the handler function. For `capture`, use the `on...capture` attribute[cite: 938].
* **State Management (Shared):**
    * **Primary Method:** Define shared, cross-component state using `$state` within dedicated modules in `$lib/state/` (e.g., `user.svelte.js`)[cite: 109, 572]. Import and use this state directly.
    * **Secondary Method:** Reserve `svelte/store` (`writable`, `readable`) only for scenarios demanding complex asynchronous logic, custom subscription mechanisms, or integration with external reactive libraries (e.g., RxJs)[cite: 574]. Minimize use of `$lib/stores/`.
* **Content Projection (Snippets):**
    * Employ snippets (`{#snippet name(params)}...{/snippet}`) and render tags (`{@render snippet(params)}`) for all content projection[cite: 349, 370].
    * Default content projection uses a `children` snippet prop: `let { children } = $props(); {@render children?.()}`[cite: 357].
    * Named content projection uses named snippet props.
    * Legacy `<slot>`, `let:`, and `<svelte:fragment>` are disallowed[cite: 952].
* **Lifecycle:**
    * Use `$effect` for reactions. Use `onMount` for browser-only setup after mount[cite: 650]. Use `onDestroy` for cleanup[cite: 657].
    * Legacy `beforeUpdate`/`afterUpdate` are disallowed[cite: 663, 670].
* **Routing:**
    * Follow SvelteKit's filesystem conventions (`src/routes/`).
    * Use `+page.svelte` (pages), `+layout.svelte` (layouts), `+error.svelte` (error boundaries), `+page.js`/`+layout.js` (universal load), `+page.server.js`/`+layout.server.js` (server load/actions), `+server.js` (API endpoints)[cite: 2071, 2101, 2090, 2078, 2113, 2083, 2118, 2120].
    * Utilize `./$types` for type safety in route files[cite: 2146].
* **Styling:**
    * Leverage default scoped styles within `<style>` tags[cite: 500].
    * Use `:global(...)` explicitly for unscoped CSS when required[cite: 509, 513].
* **Configuration:**
    * `svelte.config.js`: Configure adapter, `vitePreprocess` (if needed), aliases.
    * `vite.config.js`: Ensure `@sveltejs/kit/vite` plugin is included. Add other Vite plugins as needed.
    * `tsconfig.json`/`jsconfig.json`: **Must** extend `./.svelte-kit/tsconfig.json`. Ensure compiler options `verbatimModuleSyntax: true` (or equivalent) and `isolatedModules: true` are set[cite: 750, 751].

## 6. Testing

* Implement tests within the `frontend/tests/` directory.
* Use Vitest (recommended) or similar frameworks.
* **Component Testing:**
    * Instantiate components using `mount` from `svelte`[cite: 677, 716].
    * Use `unmount` for cleanup[cite: 682].
    * Employ `flushSync` from `svelte` after state changes or event triggers before making DOM assertions[cite: 700, 716].
    * Testing logic involving `$effect` or `$derived` may require wrapping in `$effect.root`[cite: 708].
    * Consider `@testing-library/svelte` for user-interaction focused tests[cite: 720].
    * Extract complex logic into testable utility functions outside components where feasible.

## 7. Code Quality

* **Formatting:** Enforced by Prettier (`.prettierrc.json`).
* **Linting:** Enforced by ESLint (`.eslintrc.cjs`) with Svelte plugins.
* **Automation:** Utilize pre-commit hooks (configured at root level) to ensure quality before commits.

## 8. Deployment

* Deployment is handled via the root project setup (Docker, CI/CD workflows).
* The `frontend/Dockerfile` builds the production assets and typically serves them using Nginx.
* Environment-specific configuration is managed via environment variables.

**Adherence to the Svelte 5 practices outlined in Section 5 is crucial for maintaining consistency and leveraging the framework's capabilities effectively.**
