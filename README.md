# AI Video Creation Platform - Project README

*(As of: April 15, 2025)*

This README provides a central hub for understanding the project's goals, structure, architecture, development workflow, and current status. It aims to be a self-contained context source for team members and AI agents working on the project.

## 1. High-Level Overview

This project is an AI-powered platform designed to drastically reduce pre-production time (aiming for 90% reduction) for educational content creators by automating research, structuring, and scripting while preserving the creator's unique voice and teaching style. It addresses critical bottlenecks that lead to creator burnout and limit sustainable channel growth.

The primary user interaction model is conversational, driven by AI agents orchestrated via the Haystack framework, guiding creators through a human-in-the-loop pre-production pipeline.

## 2. Problem Space & Target Audience

* **Problem:** Educational creators invest significant time (10-30 hours/video) in pre-production, with research/scripting being the major bottleneck (60-70%). This limits output, creates stress, and risks burnout. Existing AI tools often lack the ability to maintain the creator's unique voice and teaching style, a critical factor for audience connection.
* **Primary Target Audience:** "Accelerating Creators" - typically solo creators with 25K-50K subscribers, generating $30K-$75K annually. They are transitioning from passion projects to businesses, feeling the conflict between creative goals and scaling demands, and are highly receptive to solutions that save time while preserving authenticity.
* **Key Pain Points:** Time-Quality Paradox (scaling vs. quality), Creator Burnout, Voice & Authenticity Concerns with AI, Structuring complex educational content effectively.

## 3. Vision & Core Features

* **Vision:** To be the essential pre-production partner for educational creators, enabling them to "Create more without burnout - reclaim your creative passion".
* **Core Value Proposition:**
    * **Time Reduction:** Transform 15-30 hours of research/scripting into 2-3 hours of focused effort.
    * **Voice Preservation ("Creator DNA"):** Analyze existing content to capture and replicate unique linguistic patterns, terminology, pacing, and teaching style, avoiding generic AI output.
    * **Sustainable Scaling:** Allow creators to potentially double content output without increasing stress.
    * **Educational Effectiveness:** Help optimize content structure and clarity for better learning outcomes and viewer retention.
* **Key Feature Modules & Phased Rollout:**
    * **Module 1: Creator Voice & Identity**
        * **Creator DNA System:** Captures linguistic patterns/style from creator content. *(PoC: Basic pattern capture; MVP: Style fine-tuning controls)*
        * **Personal Stories Database:** Stores and retrieves creator anecdotes for integration. *(Post-MVP)*
    * **Module 2: Strategic Content Intelligence**
        * **Idea Validation:** Assesses topic viability and potential performance. *(MVP: Basic viability; Post-MVP: Performance prediction)*
        * **Knowledge Gap Detector:** Identifies underserved areas in the creator's content or niche. *(Post-MVP)*
    * **Module 3: Research & Knowledge Management**
        * **Deep Research Automation:** Gathers and synthesizes information from multiple sources. *(PoC: Basic info gathering; MVP: Multi-source synthesis)*
        * **Factual Authority Verification:** Checks information accuracy against sources. *(PoC: Basic verification; MVP: Source credibility assessment)*
        * **Audience Research:** Analyzes audience demographics, interests, and questions. *(PoC: Basic profiling; MVP: Enhanced mapping, pain points)*
    * **Module 4: Content Production Pipeline**
        * **Structure Optimization:** Suggests effective content outlines based on educational frameworks. *(PoC: Basic organization; MVP: Educational framework templates)*
        * **Script Coherence Engine:** Ensures logical flow and conceptual connections. *(PoC: Basic flow check; MVP: Conceptual connection tools)*
        * **Concept Simplification Engine:** Helps explain complex topics clearly. *(PoC: Basic explanation tools; MVP: Multiple explanation approaches)*
        * **Hook Development:** Generates engaging intro hooks. *(PoC: Basic options; MVP: Enhanced options/prediction)*
        * **Script Generation:** Creates full scripts in the creator's voice. *(PoC: Basic generation; MVP: Enhanced personalization, dynamic examples)*
        * **Content Safety:** Checks for compliance and brand safety. *(PoC: Basic policy check; MVP: Enhanced detection)*
    * **Module 5: Content Distribution & Monetization**
        * **Content Repurposing:** Adapts video scripts for other formats (shorts, blogs). *(Post-MVP)*
        * **Monetization Strategy:** Suggests relevant CTAs based on content. *(Post-MVP)*
    * **Module 6: Creator Workflow System**
        * **Streaming Save / Version Management:** Preserves work continuously and allows reverting. *(PoC: Critical point saves, basic version retrieval; MVP: Continuous save, enhanced version control)*
        * **Feedback System:** Allows creators to provide feedback at any stage to improve AI outputs. *(PoC: Basic correction system; MVP: Preference tracking)*
    * **Module 7: Platform Foundation**
        * **Processing Infrastructure:** Manages underlying compute for AI tasks. *(PoC/MVP)*
        * **Data Security:** Ensures protection of creator data and content. *(PoC/MVP)*

## 4. Roadmap & Current Status

* **Phased Approach:** Development follows an iterative plan: **PoC -> Early MVP -> MVP -> Post-MVP**. This allows for validation and refinement at each stage.
* **Current Phase:** **Proof of Concept (PoC)** *(Target Completion: See internal plan)*
    * **Goal:** Validate the core technical feasibility of the research-to-script flow using basic versions of key features (DNA capture, research, verification, structuring, scripting) via a conversational agent (Haystack) interacting with an LLM Gateway (Portkey). Establish core backend/frontend architecture patterns.
    * **Key PoC Deliverables:** Basic voice pattern capture, basic research automation & fact verification, basic script generation in creator's voice, minimal interactive frontend/agent interface.
* **Next Phases:**
    * **Early MVP:** Stabilize PoC flow, deploy to cloud, add foundational CI/CD and basic observability (logging, error tracking).
    * **MVP:** Deliver core value prop reliably with enhanced AI quality (fine-tuning, multi-source research), improved usability, full observability integration, and readiness for initial paying customers. Replace PoC polling with real-time status updates (WebSockets/SSE).
* **Remaining Decisions / Active Design Areas:** Specific PaaS/DB/Redis provider selection, final data schema details, detailed data ingestion pipelines, specific Haystack pipeline implementations, detailed observability configuration (dashboards/alerts), advanced caching strategies, **Workflow Orchestration Strategy (Post-MVP)**.

## 5. Project Structure (Monorepo)

This project uses a monorepo to manage the frontend, backend, and configurations together, simplifying local development while maintaining separation.

*(Structure diagram retained from previous version)*

```plaintext
cp-prototype/
├── .github/                  # CI/CD Automation (e.g., GitHub Actions)
│   └── workflows/
│       ├── ci-backend.yml
│       └── ci-frontend.yml
│       └── deploy-staging.yml # Example deployment workflow
│       └── deploy-production.yml # Example deployment workflow
├── .gitignore                # Files/folders for Git to ignore
├── docker-compose.yml        # Local development environment setup
├── .env.example              # --- KEY: Example env vars for LOCAL development ---
├── .env.staging.example      # --- KEY: Example env vars for STAGING environment ---
├── .env.production.example   # --- KEY: Example env vars for PRODUCTION (excluding secrets!) ---
├── README.md                 # --- KEY: High-level overview, Arch decisions, Setup, How to Run ---
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI app definition, middleware, lifespan events
│   │   ├── config.py         # --- KEY: Pydantic settings loading from ENV variables ---
│   │   ├── logging_config.py # --- KEY ADDITION: Configure application logging (levels, formats) ---
│   │   │
│   │   ├── api/              # FastAPI specifics
│   │   │   ├── __init__.py
│   │   │   ├── dependencies.py # Auth checks, DB sessions per request
│   │   │   ├── middleware/   # Custom middleware (e.g., request timing)
│   │   │   │   └── ...
│   │   │   ├── routers/      # Endpoint definitions, grouped by feature
│   │   │   │   └── ...
│   │   │   └── schemas.py    # API request/response data shapes (Pydantic)
│   │   │
│   │   ├── worker/           # SAQ Worker specifics
│   │   │   ├── __init__.py
│   │   │   └── settings.py   # SAQ Queue definition, task imports/discovery
│   │   │
│   │   ├── db/               # Database specifics
│   │   │   ├── __init__.py
│   │   │   ├── models.py     # SQLAlchemy table definitions
│   │   │   ├── migrations/   # --- KEY: Alembic DB schema change scripts ---
│   │   │   │   └── versions/
│   │   │   │       └── ...py # Individual migration files generated by Alembic
│   │   │   │   └── env.py    # Alembic runtime environment
│   │   │   │   └── script.py.mako # Migration file template
│   │   │   └── session.py    # DB connection/session logic
│   │   │
│   │   ├── shared/           # Code shared across backend features
│   │   │   ├── __init__.py
│   │   │   ├── clients/      # Clients for 3rd party APIs (YouTube, etc.)
│   │   │   │   └── ...
│   │   │   ├── constants.py  # Shared Enums and constant values
│   │   │   ├── exceptions.py # Custom error classes
│   │   │   ├── schemas.py    # Core internal data shapes (Pydantic)
│   │   │   └── utils.py      # Common helper functions
│   │   │
│   │   └── features/         # Business Logic / Domain Features
│   │       ├── __init__.py
│   │       │
│   │       ├── auth/         # Example user/auth feature logic
│   │       │   └── ...
│   │       │
│   │       ├── voice_dna/    # Example Creator DNA feature logic
│   │       │   ├── __init__.py
│   │       │   ├── pipelines.py  # Haystack/AI pipeline definitions
│   │       │   ├── prompts/      # Prompt templates
│   │       │   ├── service.py    # Core logic / Facade for this feature
│   │       │   └── tasks.py      # Background tasks for this feature
│   │       │
│   │       └── # ... (research/, scripting/, etc.)
│   │
│   ├── tests/                # Backend automated tests
│   │   ├── __init__.py
│   │   └── # (Mirror app structure: api/, features/, shared/, etc.)
│   │
│   ├── models/               # --- KEY ADDITION (Optional): For downloaded AI models (if self-hosting later) ---
│   │   └── .gitkeep
│   │
│   ├── Dockerfile            # Builds the common backend image (API + Worker code)
│   ├── pyproject.toml        # Python dependencies (Poetry/PDM)
│   ├── alembic.ini           # Alembic configuration file
│   ├── ruff.toml             # --- KEY ADDITION: Example Linter/Formatter config ---
│   └── README.md             # --- KEY: Backend setup, running locally, migration cmd, testing cmd ---
│
├── frontend/
│   ├── src/                  # SvelteKit source code
│   │   ├── app.html
│   │   ├── app.d.ts
│   │   ├── app.css           # Global styles
│   │   ├── hooks.server.js   # Server-side hooks
│   │   ├── hooks.client.js   # Client-side hooks
│   │   │
│   │   ├── lib/              # Reusable frontend modules
│   │   │   ├── components/   # UI Components
│   │   │   ├── services/     # API Client (handles requests/responses/errors)
│   │   │   ├── stores/       # Global state management
│   │   │   ├── types/        # TypeScript definitions
│   │   │   └── utils/        # Helper functions
│   │   │
│   │   └── routes/           # Application pages and layouts
│   │       └── ...
│   │
│   ├── static/               # Static assets (favicon, images)
│   ├── tests/                # Frontend automated tests
│   ├── Dockerfile            # --- KEY: Builds PRODUCTION frontend image (often serves static files via Nginx) ---
│   ├── package.json          # Node.js dependencies
│   ├── svelte.config.js
│   ├── vite.config.js
│   ├── .prettierrc.json      # --- KEY ADDITION: Example Formatter config ---
│   ├── .eslintrc.cjs         # --- KEY ADDITION: Example Linter config ---
│   └── README.md             # --- KEY: Frontend setup, running dev server, building for prod ---
│
├── e2e_tests/                # --- KEY ADDITION (Optional): End-to-end tests (e.g., Playwright/Cypress) ---
│   └── .gitkeep
│
├── infra/                    # Optional: Infrastructure-as-Code (Terraform, Pulumi)
│   └── .gitkeep
│
└── scripts/                  # Optional: Helper scripts (e.g., db reset, run linters)
    └── .gitkeep
```

* **`backend/`:** Python API (FastAPI) & Background Task Worker (SAQ). See `backend/README.md`.
* **`frontend/`:** SvelteKit User Interface. See `frontend/README.md`.
* **Root:** Shared configurations, local development setup (`docker-compose.yml`), CI/CD workflows.

## 6. Architecture

Architecture choices prioritize developer velocity (solopreneur focus), low operational overhead ("Low-Ops"), cost-efficient scaling, and creator voice authenticity.

### 6.a. Core Technology Stack

* Backend Language/Framework: Python / FastAPI
* AI Orchestration: Haystack Framework (v2+)
* Frontend Framework: Svelte / SvelteKit
* Database: Managed PostgreSQL + `pgvector` extension (for relational & vector data)
* DB Migrations: Alembic
* Background Tasks: SAQ (Simple Async Queue) library
* Task Queue Broker: Managed Redis
* Hosting: Container-based PaaS (e.g., Cloud Run, App Runner, Render)
* LLM Interaction (PoC): Via managed LLM Gateway (Portkey) for abstraction, monitoring, caching. Architecture allows for future self-hosted/fine-tuned models.

### 6.b. Guiding Principles

* Minimize direct infrastructure operation ("Low-Ops").
* Minimize vendor lock-in (prefer managed open-source/standards where feasible).
* Prioritize creator voice authenticity.
* Async-first design.
* Modularity & Rapid Iteration.
* **Design for Idempotency:** Especially for background tasks, ensure operations can be safely retried.

### 6.c. Key Patterns

* Async-first design (Python `async`/`await`).
* Dependency Injection (FastAPI `Depends`, SAQ context/hooks).
* Single Backend Docker Image: Builds API + Worker code; run with different commands.
* Conversational Agent primary interface via Haystack Tool/Function calling.

### 6.d. API vs. Worker Design Strategy (PoC)

This strategy outlines the division of logic between the synchronous API Process (FastAPI) and the asynchronous Worker Process (SAQ) for the PoC, acknowledging areas needing evolution.

* **Guiding Principles:** API Responsiveness (< 500ms target), Background Processing for long tasks (> 500ms, I/O, CPU-heavy), Independent Scalability, Reliability via background retries, Maintainability via shared code.
* **Core Responsibilities:**
    * **API (FastAPI):** Handles HTTP requests, quick validation/auth, simple/fast DB ops, *triggers* background tasks, provides *polling endpoints* for job status/results (PoC limitation).
    * **Worker (SAQ):** Executes longer tasks (>500ms), I/O-bound calls (LLM Gateway, external APIs), CPU-intensive work, tasks needing retries. Updates status/results in DB. Must be designed for **idempotency** where possible.
* **Communication Patterns (PoC Scope):**
    1.  **Triggering:** API validates, generates `job_id`, calls `await queue.enqueue("task_name", job_id=job_id, ...)`, returns `job_id` (e.g., 202 Accepted).
    2.  **Status Reporting:** Worker updates job status (`PROCESSING`, `COMPLETED`, `FAILED`) and results in DB, keyed by `job_id`.
    3.  **Status Retrieval (PoC Limitation):** Client **polls** API endpoint (`GET /jobs/{job_id}/status`), which reads status/results from DB. (*Note: This polling approach is for PoC simplicity and is expected to be replaced by real-time updates like WebSockets/SSE in MVP for better UX and efficiency.*)
* **Shared Code Strategy:**
    * Reusable logic (business rules, DB interactions, clients) in `app/features/.../service.py` or `app/shared/`.
    * Services accept dependencies (e.g., DB session) explicitly, usable by both API (via `Depends`) and Worker (via explicit setup/context). Avoid FastAPI-specific objects in shared services.
* **Error Handling (PoC Scope):**
    * **Worker:** Use `try...except`, log errors thoroughly, update job status to `FAILED`. Use basic SAQ retries for transient issues.
    * **API:** Return standard HTTP 4xx/5xx errors with JSON bodies.
* **Application to Key PoC Features:**
    * **Worker Tasks:** Content Ingestion, Creator DNA Analysis, Research Topic, Verify Fact, Generate Script Section.
    * **API Tasks:** Auth, Agent Interaction (triggers workers), Job Status Endpoint.
* **Future Considerations & Challenges (MVP+):**
    * **Real-time Updates:** Replace PoC polling with WebSockets/SSE.
    * **Workflow Orchestration:** **CRITICAL CHALLENGE.** Managing complex, multi-step, conditional background processes (required for advanced Post-MVP features) will necessitate a robust orchestration strategy beyond simple SAQ enqueueing. Options include dedicated workflow engines (Temporal, Prefect, etc.) or custom state machines. This requires dedicated design effort post-PoC (See Section 4).
    * **Advanced Error Handling:** Implement dead-letter queues, more sophisticated retry logic, and potentially compensation logic for multi-step failures.
    * **Observability:** Implement distributed tracing (OpenTelemetry) to track requests across API -> Queue -> Worker boundaries.
    * **Resource Management:** More granular concurrency controls might be needed for resource-intensive tasks.

### 6.e. Observability Strategy (MVP Target)

* Instrumentation: OpenTelemetry SDK (standard for traces, metrics, logs).
* Backend - Grafana Cloud: Centralized Logs (Loki), Metrics (Mimir), Traces (Tempo). Infrastructure & System view.
* Backend - Sentry: Application Error Tracking & Performance Monitoring (APM). Application Code view.
* Frontend/Backend - PostHog: Product Analytics, User Behavior Tracking, Feature Flags, Session Replay. User Interaction & Product view.
* Supplemented by LLM Gateway (Portkey) for monitoring LLM calls, costs, latency, prompts.

## 7. Development Workflow

This section outlines the process for setting up the local environment, running services, testing, and managing code quality. **See `backend/README.md` and `frontend/README.md` for detailed commands.**

* **Prerequisites:**
    * Docker & Docker Compose
    * Git
    * Python environment management (e.g., Poetry or PDM recommended)
    * Node.js & package manager (npm/yarn/pnpm recommended)

* **Local Setup:**
    1.  Clone repository.
    2.  Copy `.env.example` (from root) to `backend/.env`.
    3.  Fill in necessary local configuration values in `backend/.env`. **CRITICAL: Never commit your actual `.env` file to Git! Ensure `backend/.env` is in `.gitignore`.**
    4.  (Recommended) Set up pre-commit hooks for automated code checks/formatting.

* **Running Services:**
    1.  Build & Start Services:
        ```bash
        docker-compose up --build -d
        ```
        * This command builds the Docker images and starts all services defined in `docker-compose.yml` (db, redis, api, worker, frontend) in the background.
    2.  Access Services (Default Ports):
        * Frontend: `http://localhost:5173`
        * Backend API: `http://localhost:8000` (API Docs: `http://localhost:8000/docs`)
    3.  View Logs: `docker-compose logs -f <service_name>` (e.g., `backend`, `frontend`, `worker`).
    4.  Stopping Services:
        ```bash
        docker-compose down
        ```

* **Database Migrations:**
    * **CRITICAL:** If you pull changes that include database schema modifications (`backend/db/migrations/`), you MUST apply them *before* running the application code that depends on them.
    * **Apply Migrations:** Run the migration command (detailed in `backend/README.md`), typically:
        ```bash
        docker-compose exec backend alembic upgrade head
        ```
    * **Generate Migrations:** After changing SQLAlchemy models in `backend/app/db/models.py`, generate a new migration script:
        ```bash
        docker-compose exec backend alembic revision --autogenerate -m "Brief description of changes"
        ```
        Review the generated script in `backend/db/migrations/versions/` before applying.

* **Testing:**
    * Backend: Run `pytest` within the backend container (see `backend/README.md`), typically:
        ```bash
        docker-compose exec backend pytest
        ```
    * Frontend: Run tests using commands defined in `frontend/package.json` (see `frontend/README.md`).
    * CI pipelines automatically run tests (`.github/workflows/`).

* **Code Quality:**
    * Linters (Ruff for Python, ESLint for JS/TS) and Formatters (Black for Python, Prettier for JS/TS/CSS/etc.) are configured (`ruff.toml`, `pyproject.toml`, `.prettierrc.json`).
    * Pre-commit hooks should be set up locally to automatically run these tools before committing.

* **Configuration & Secrets:**
    * **Local:** Uses `backend/.env` file (ignored by Git). Loaded via Pydantic `BaseSettings` in `backend/app/config.py`. Frontend config managed via build/runtime variables.
    * **Staging/Production:** Configuration MUST be injected via environment variables (set in PaaS).
    * **Secrets Management:** **CRITICAL:** Sensitive data (API keys, database passwords) for deployed environments MUST use a proper secrets management system (e.g., AWS Secrets Manager, Google Secret Manager, HashiCorp Vault) and injected as environment variables at runtime, **not** stored in `.env` files or code.

*(Refer to the README files inside the `backend/` and `frontend/` directories for more detailed development workflows.)*
