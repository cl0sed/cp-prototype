# AI Video Creation Platform - Project README

*(As of: April 16, 2025)*

This README provides a central hub for understanding the project's goals, structure, architecture, development workflow, and current status. It aims to be a self-contained context source for team members and AI agents working on the project.

## 1. High-Level Overview

This project is an AI-powered platform designed to drastically reduce pre-production time (aiming for 90% reduction) for educational content creators by automating research, structuring, and scripting while preserving the creator's unique voice and teaching style[cite: 19, 4278]. It addresses critical bottlenecks that lead to creator burnout and limit sustainable channel growth[cite: 4282].

The primary user interaction model is conversational, driven by AI agents orchestrated via the Haystack framework, guiding creators through a human-in-the-loop pre-production pipeline[cite: 4280, 4304].

## 2. Problem Space & Target Audience

* **Problem:** Educational creators invest significant time (10-30 hours/video) in pre-production, with research/scripting being the major bottleneck (60-70%)[cite: 18, 25, 4281]. This limits output, creates stress, and risks burnout[cite: 4282]. Existing AI tools often lack the ability to maintain the creator's unique voice and teaching style, a critical factor for audience connection[cite: 26, 4282].
* **Primary Target Audience:** "Accelerating Creators" - typically solo creators with 25K-50K subscribers, generating $30K-$75K annually[cite: 18, 41, 4283]. They are transitioning from passion projects to businesses, feeling the conflict between creative goals and scaling demands, and are highly receptive to solutions that save time while preserving authenticity[cite: 21, 4284].
* **Key Pain Points:** Time-Quality Paradox (scaling vs. quality), Creator Burnout, Voice & Authenticity Concerns with AI, Structuring complex educational content effectively[cite: 25, 26, 4285].

## 3. Vision & Core Features

* **Vision:** To be the essential pre-production partner for educational creators, enabling them to "Create more without burnout - reclaim your creative passion"[cite: 4286].
* **Core Value Proposition:**
    * **Time Reduction:** Transform 15-30 hours of research/scripting into 2-3 hours of focused effort[cite: 69, 4287].
    * **Voice Preservation ("Creator DNA"):** Analyze existing content to capture and replicate unique linguistic patterns, terminology, pacing, and teaching style, avoiding generic AI output[cite: 28, 49, 4288].
    * **Sustainable Scaling:** Allow creators to potentially double content output without increasing stress[cite: 70, 4289].
    * **Educational Effectiveness:** Help optimize content structure and clarity for better learning outcomes and viewer retention[cite: 70, 4290].
* **Key Feature Modules & Phased Rollout[cite: 48, 64, 65, 4291]:**
    * **Module 1: Creator Voice & Identity:** Creator DNA System[cite: 49], Personal Stories DB (Post-MVP)[cite: 49].
    * **Module 2: Strategic Content Intelligence:** Idea Validation (MVP)[cite: 51], Knowledge Gap Detector (Post-MVP)[cite: 51].
    * **Module 3: Research & Knowledge Management:** Deep Research Automation (PoC/MVP)[cite: 53], Factual Verification (PoC/MVP)[cite: 53], Audience Research (PoC/MVP)[cite: 53].
    * **Module 4: Content Production Pipeline:** Structure Optimization (PoC/MVP)[cite: 55], Script Coherence (PoC/MVP)[cite: 55], Concept Simplification (PoC/MVP)[cite: 55], Hook Development (PoC/MVP)[cite: 56], Script Generation (PoC/MVP)[cite: 56], Content Safety (PoC/MVP)[cite: 56].
    * **Module 5: Content Distribution & Monetization:** Repurposing, Monetization Strategy (Post-MVP)[cite: 58].
    * **Module 6: Creator Workflow System:** Streaming Save/Versioning (PoC basic save, MVP simplified versioning)[cite: 60], Feedback System (PoC/MVP)[cite: 60].
    * **Module 7: Platform Foundation:** Processing Infra, Data Security (PoC/MVP)[cite: 62].

## 4. Roadmap & Current Status

* **Phased Approach:** PoC -> Early MVP -> MVP -> Post-MVP[cite: 4310].
* **Current Phase:** Proof of Concept (PoC)[cite: 4311].
    * **Goal:** Validate core research-to-script flow via conversational agent and LLM Gateway (Portkey)[cite: 4285, 4311]. Establish core architecture.
    * **Key PoC Deliverables:** Basic DNA capture, basic research/verification, basic script generation, minimal UI[cite: 64, 4312].
* **Next Phases:**
    * **Early MVP:** Cloud deployment, CI/CD, basic observability (logging, Sentry)[cite: 4313, 4397].
    * **MVP:** Reliable core value prop, enhanced AI quality, improved usability, full observability integration, initial customer readiness, real-time updates (WebSockets/SSE instead of polling)[cite: 4314, 4315, 4402, 4403].
* **Remaining Decisions / Active Design Areas:** Specific PaaS/DB/Redis provider selection[cite: 4393], detailed data ingestion pipelines[cite: 10, 4393], specific Haystack pipeline implementations[cite: 11, 4393], detailed observability config (dashboards/alerts)[cite: 16, 4393], advanced caching[cite: 13], **Workflow Orchestration Strategy (Post-MVP)**[cite: 4315, 4360].

## 5. Project Structure (Monorepo)

This project uses a monorepo to manage the frontend, backend, and configurations together[cite: 4316].

(Structure diagram retained from previous version)
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
* **`backend/`:** Python API (FastAPI) & Background Task Worker (SAQ)[cite: 4334]. See `backend/README.md`.
* **`frontend/`:** SvelteKit User Interface[cite: 4335]. See `frontend/README.md`.
* **Root:** Shared configurations, local development setup (`docker-compose.yml`)[cite: 4317], CI/CD workflows.

## 6. Architecture

Architecture choices prioritize developer velocity (solopreneur focus)[cite: 4336], low operational overhead ("Low-Ops")[cite: 4338], cost-efficient scaling, and creator voice authenticity[cite: 4336].

### 6.a. Core Technology Stack [cite: 4337, 4361]

* Backend Language/Framework: Python / FastAPI
* AI Orchestration: Haystack Framework (v2+)
* Frontend Framework: Svelte / SvelteKit
* Database: Managed PostgreSQL + `pgvector` extension for vector embeddings
* DB Migrations: Alembic (configured for automated database schema management)
* Background Tasks: SAQ (Simple Async Queue) library
* Task Queue Broker: Managed Redis
* Hosting: Container-based PaaS
* LLM Interaction (PoC/MVP): Via managed LLM Gateway (Portkey)

### 6.b. Guiding Principles [cite: 4338, 4339, 4340]

* Minimize direct infrastructure operation ("Low-Ops").
* Minimize vendor lock-in.
* Prioritize creator voice authenticity.
* Async-first design.
* Modularity & Rapid Iteration.
* Design for Idempotency (especially background tasks).

### 6.c. Key Patterns [cite: 4341, 4342, 4343]

* Async-first design.
* Dependency Injection.
* Single Backend Docker Image (API + Worker).
* Conversational Agent primary interface.

### 6.d. API vs. Worker Design Strategy [cite: 4344]

* **API (FastAPI):** Handles synchronous requests, validation, auth, simple DB ops, triggers background tasks[cite: 4346]. For PoC, provides polling endpoints for job status[cite: 4346, 4351].
* **Worker (SAQ):** Executes long-running (>500ms), I/O-bound (LLM calls), or retryable tasks[cite: 4347]. Updates status/results in DB. Designed for idempotency[cite: 4348].
* **PoC Communication:** API enqueues job -> returns `job_id`[cite: 4349]. Worker updates status in `background_jobs` table[cite: 4350]. Client polls API for status[cite: 4351]. (Polling replaced by WebSockets/SSE in MVP [cite: 4352, 4358]).
* **MVP+ Challenges:** Real-time updates, Workflow Orchestration, Advanced Error Handling[cite: 4358, 4359, 4360, 4361].

### 6.e. Data Layer Details

The database schema is designed to support the application's features from PoC through MVP, balancing normalization with practical needs for AI processing and retrieval.

* **Core Entities:** `users`, `projects` (stores title, topic, `creative_brief`, links to active DNA profile & selected structure), `content_sources`.
* **User Assets (Reusable):** `creator_dna_profiles` (stores DNA analysis config/summary), `audience_avatars` (user-defined personas), `supporting_materials` (user-provided links, images, etc.). These are linked to projects via join tables (`project_audience_avatars`, `project_topic_materials`).
* **Project Context:** `project_settings` (references optional `project_settings_templates`), `project_topics` (stores project-specific outline with user `selection_status`), `generated_structures` (stores AI-generated structure options for user selection).
* **Content & Generation:**
    * `RETRIEVABLE_TEXT`: **Key table for Haystack RAG.** Stores chunked text from `content_sources` AND `personal_stories` (now centralized here), along with their vector embeddings (`pgvector`). Includes metadata for filtering (e.g., `origin_type`).
    * `script_sections`: Acts as a header for script components (type, order, parent link, link to chosen structure). Stores the current `content` and `previous_content` (for simple MVP versioning/revert).
    * `dna_detailed_analysis`, `research_analysis`, `safety_analysis`, `project_idea_validation`: Store structured results from specific AI analysis tasks, linked to their respective sources/projects/sections. Includes `initiating_job_id` for tracing.
* **Supporting Tables:** `background_jobs` (tracks SAQ tasks, includes `initiating_job_id`), `feedback` (polymorphic link to various entities), `evaluation_results` (simplified, polymorphic storage for AI/user evaluations), `educational_frameworks`, join tables.
* **Vector Data Strategy:** Uses `pgvector` extension within PostgreSQL. Embeddings for semantic search reside primarily in `RETRIEVABLE_TEXT` with 1536-dimensional vectors corresponding to AI model embedding output. Queries combine vector similarity search (IVFFLAT index on `embedding` with vector_l2_ops) with metadata filtering (on FKs or `basic_metadata` JSONB) for efficient semantic retrieval.

### 6.f. Architecture Considerations & Technical Debt

* **Workflow Orchestration:** The current SAQ + `background_jobs` approach is sufficient for PoC/early MVP but does **not** solve complex, multi-step workflow orchestration[cite: 4360]. This remains the most significant piece of **deferred technical debt**, requiring a dedicated solution (e.g., Temporal, Prefect) Post-MVP.
* **Simplified Script Versioning:** Using `previous_content` avoids the complexity of a separate versions table for MVP but limits history to one step back. Full versioning can be added later if needed.
* **Simplified AI Evaluation:** The polymorphic `evaluation_results` table allows storing basic evaluation data but lacks structure for complex metric analysis[cite: 14]. The mechanism for *processing* these results for meaningful insights is deferred.
* **Polymorphic Links:** `feedback` and `evaluation_results` use polymorphism. This provides flexibility but increases query complexity and reduces DB-level referential integrity compared to dedicated tables or FKs per type. Requires careful handling in application code.
* **Join Complexity:** Linking reusable assets (`supporting_materials`) through `project_topics` adds join complexity to retrieve all materials for a project outline.
* **Unified Retrieval Index:** Storing source text and story chunks in `RETRIEVABLE_TEXT` simplifies vector indexing but requires the AI retrieval logic (Haystack) to handle filtering and potentially different ranking for these distinct content types.
* **External Prompt Tracking:** Removal of the `prompts` table relies on the external LLM Gateway (Portkey) [cite: 4285] for prompt logging and traceability.

### 6.g. Observability Strategy (MVP Target)

* Instrumentation: OpenTelemetry SDK.
* Platforms: Grafana Cloud (Logs, Metrics, Traces - Infra/System), Sentry (Errors, APM - App Code), PostHog (Product Analytics - User/Product).
* LLM Gateway (Portkey) provides LLM-specific monitoring.

## 7. Development Workflow

This section outlines the process for setting up the local environment, running services, testing, and managing code quality. **See `backend/README.md` and `frontend/README.md` for detailed commands.** [cite: 4369]

* **Prerequisites:** Docker, Git, Python env management, Node.js[cite: 4370].
* **Local Setup:** Clone, configure `backend/.env` (from root `.env.example`, keep secrets out of Git)[cite: 4371, 4372]. Use pre-commit hooks[cite: 4372].
* **Running Services:** `docker-compose up --build -d`. Access via standard ports. Logs via `docker-compose logs -f`. Stop via `docker-compose down`[cite: 4373, 4374, 4375].
* **Database Migrations (Alembic):** Apply migrations *before* running app code (`docker-compose exec backend alembic upgrade head`). Generate migrations after model changes (`docker-compose exec backend alembic revision --autogenerate -m "Description of changes"`). Migration configuration in `backend/alembic.ini` and `backend/app/db/migrations/env.py` loads database settings from application config[cite: 4375, 4376, 4377].
* **Testing:** Use commands defined in backend/frontend READMEs. CI runs tests automatically[cite: 4377, 4378].
* **Code Quality:** Linters (Ruff, ESLint) & Formatters (Black, Prettier) configured. Use pre-commit hooks[cite: 4378, 4379].
* **Configuration & Secrets:** Local via `backend/.env`[cite: 4380]. Deployed via environment variables[cite: 4382]. **CRITICAL:** Use secrets management service for deployed secrets, inject as env vars[cite: 4383].

*(Refer to the README files inside the `backend/` and `frontend/` directories for more detailed development workflows.)* [cite: 4384]
