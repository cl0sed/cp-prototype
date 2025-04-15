# AI Video Creation Platform - Project README

*(As of: April 15, 2025)*

This README provides a central hub for understanding the project's goals, structure, architecture, development workflow, and current status. It aims to be a self-contained context source for team members and AI agents working on the project.

## 1. High-Level Overview

This project is an AI-powered platform designed to drastically reduce pre-production time (aiming for 90% reduction) for educational content creators by automating research, structuring, and scripting while preserving the creator's unique voice and teaching style[cite: 19, 69]. It addresses critical bottlenecks that lead to creator burnout and limit sustainable channel growth[cite: 18, 68].

The primary user interaction model is conversational, driven by AI agents orchestrated via the Haystack framework[cite: 2], guiding creators through a human-in-the-loop pre-production pipeline[cite: 20].

## 2. Problem Space & Target Audience

* **Problem:** Educational creators invest significant time (10-30 hours/video) in pre-production, with research/scripting being the major bottleneck (60-70%)[cite: 18, 68]. This limits output, creates stress, and risks burnout[cite: 25]. Existing AI tools often lack the ability to maintain the creator's unique voice and teaching style, a critical factor for audience connection[cite: 25, 68].
* **Primary Target Audience:** "Accelerating Creators" [cite: 20] - typically solo creators with 25K-50K subscribers, generating \$30K-\$75K annually[cite: 20, 41]. They are transitioning from passion projects to businesses, feeling the conflict between creative goals and scaling demands[cite: 21, 69], and are highly receptive to solutions that save time while preserving authenticity[cite: 22].
* **Key Pain Points:** Time-Quality Paradox (scaling vs. quality)[cite: 25, 44], Creator Burnout[cite: 25, 44], Voice & Authenticity Concerns with AI[cite: 25, 44], Structuring complex educational content effectively[cite: 26, 44].

## 3. Vision & Core Features

* **Vision:** To be the essential pre-production partner for educational creators, enabling them to "Create more without burnout - reclaim your creative passion"[cite: 34].
* **Core Value Proposition:**
    * **Time Reduction:** Transform 15-30 hours of research/scripting into 2-3 hours of focused effort[cite: 69].
    * **Voice Preservation ("Creator DNA"):** Analyze existing content to capture and replicate unique linguistic patterns, terminology, pacing, and teaching style, avoiding generic AI output[cite: 28, 36, 49, 70].
    * **Sustainable Scaling:** Allow creators to potentially double content output without increasing stress[cite: 25, 69].
    * **Educational Effectiveness:** Help optimize content structure and clarity for better learning outcomes and viewer retention[cite: 26, 55, 70].
* **Key Feature Modules & Phased Rollout:**
    * **Module 1: Creator Voice & Identity** [cite: 48]
        * **Creator DNA System:** Captures linguistic patterns/style from creator content. *(PoC: Basic pattern capture[cite: 49, 64]; MVP: Style fine-tuning controls [cite: 49, 64])*
        * **Personal Stories Database:** Stores and retrieves creator anecdotes for integration. *(Post-MVP [cite: 49])*
    * **Module 2: Strategic Content Intelligence** [cite: 50]
        * **Idea Validation:** Assesses topic viability and potential performance. *(MVP: Basic viability[cite: 51, 64]; Post-MVP: Performance prediction [cite: 51, 65])*
        * **Knowledge Gap Detector:** Identifies underserved areas in the creator's content or niche. *(Post-MVP [cite: 51])*
    * **Module 3: Research & Knowledge Management** [cite: 52]
        * **Deep Research Automation:** Gathers and synthesizes information from multiple sources. *(PoC: Basic info gathering[cite: 53, 64]; MVP: Multi-source synthesis [cite: 53, 64])*
        * **Factual Authority Verification:** Checks information accuracy against sources. *(PoC: Basic verification[cite: 53, 64]; MVP: Source credibility assessment [cite: 53, 64])*
        * **Audience Research:** Analyzes audience demographics, interests, and questions. *(PoC: Basic profiling[cite: 53, 64]; MVP: Enhanced mapping, pain points [cite: 53, 64])*
    * **Module 4: Content Production Pipeline** [cite: 54]
        * **Structure Optimization:** Suggests effective content outlines based on educational frameworks. *(PoC: Basic organization[cite: 55, 64]; MVP: Educational framework templates [cite: 55, 64])*
        * **Script Coherence Engine:** Ensures logical flow and conceptual connections. *(PoC: Basic flow check[cite: 55, 64]; MVP: Conceptual connection tools [cite: 55, 64])*
        * **Concept Simplification Engine:** Helps explain complex topics clearly. *(PoC: Basic explanation tools[cite: 55, 64]; MVP: Multiple explanation approaches [cite: 55, 64])*
        * **Hook Development:** Generates engaging intro hooks. *(PoC: Basic options[cite: 56, 64]; MVP: Enhanced options/prediction [cite: 56, 64])*
        * **Script Generation:** Creates full scripts in the creator's voice. *(PoC: Basic generation[cite: 56, 64]; MVP: Enhanced personalization, dynamic examples [cite: 56, 64])*
        * **Content Safety:** Checks for compliance and brand safety. *(PoC: Basic policy check[cite: 56, 64]; MVP: Enhanced detection [cite: 56, 64])*
    * **Module 5: Content Distribution & Monetization** [cite: 57]
        * **Content Repurposing:** Adapts video scripts for other formats (shorts, blogs). *(Post-MVP [cite: 58])*
        * **Monetization Strategy:** Suggests relevant CTAs based on content. *(Post-MVP [cite: 58])*
    * **Module 6: Creator Workflow System** [cite: 59]
        * **Streaming Save / Version Management:** Preserves work continuously and allows reverting. *(PoC: Critical point saves, basic version retrieval[cite: 60, 64]; MVP: Continuous save, enhanced version control [cite: 60, 64])*
        * **Feedback System:** Allows creators to provide feedback at any stage to improve AI outputs. *(PoC: Basic correction system[cite: 60, 64]; MVP: Preference tracking [cite: 60, 64])*
    * **Module 7: Platform Foundation** [cite: 61]
        * **Processing Infrastructure:** Manages underlying compute for AI tasks. *(PoC/MVP [cite: 62])*
        * **Data Security:** Ensures protection of creator data and content. *(PoC/MVP [cite: 62])*

## 4. Roadmap & Current Status

* **Phased Approach:** Development follows an iterative plan: **PoC -> Early MVP -> MVP -> Post-MVP**[cite: 74]. This allows for validation and refinement at each stage.
* **Current Phase:** **Proof of Concept (PoC)** *(Target Completion: See internal plan)* [cite: 76]
    * **Goal:** Validate the core technical feasibility of the research-to-script flow using basic versions of key features (DNA capture, research, verification, structuring, scripting) via a conversational agent (Haystack) interacting with an LLM Gateway (Portkey)[cite: 76, 83, 84]. Establish core backend/frontend architecture patterns[cite: 77].
    * **Key PoC Deliverables:** Basic voice pattern capture, basic research automation & fact verification, basic script generation in creator's voice, minimal interactive frontend/agent interface[cite: 64, 76, 84].
* **Next Phases:**
    * **Early MVP:** Stabilize PoC flow, deploy to cloud, add foundational CI/CD and basic observability (logging, error tracking)[cite: 86, 88, 90].
    * **MVP:** Deliver core value prop reliably with enhanced AI quality (fine-tuning, multi-source research), improved usability, full observability integration, and readiness for initial paying customers[cite: 91, 93, 95].
* **Remaining Decisions / Active Design Areas:** Specific PaaS/DB/Redis provider selection, final data schema details, detailed data ingestion pipelines, specific Haystack pipeline implementations, detailed observability configuration (dashboards/alerts), advanced caching strategies[cite: 7, 8, 9, 10, 11, 12, 13, 16].

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

Architecture choices prioritize developer velocity (solopreneur focus), low operational overhead ("Low-Ops"), cost-efficient scaling, and creator voice authenticity[cite: 7, 68].

* **Core Technology Stack**[cite: 2, 3, 4, 5]:
    * Backend Language/Framework: Python / FastAPI
    * AI Orchestration: Haystack Framework (v2+)
    * Frontend Framework: Svelte / SvelteKit
    * Database: Managed PostgreSQL + `pgvector` extension (for relational & vector data)
    * DB Migrations: Alembic
    * Background Tasks: SAQ (Simple Async Queue) library
    * Task Queue Broker: Managed Redis
    * Hosting: Container-based PaaS (e.g., Cloud Run, App Runner, Render)
    * LLM Interaction (PoC): Via managed LLM Gateway (Portkey) [cite: 83] for abstraction, monitoring, caching. Architecture allows for future self-hosted/fine-tuned models.
* **Guiding Principles**[cite: 6, 7]:
    * Minimize direct infrastructure operation ("Low-Ops").
    * Minimize vendor lock-in (prefer managed open-source/standards where feasible).
    * Prioritize creator voice authenticity[cite: 68].
    * Async-first design.
    * Modularity & Rapid Iteration.
* **Key Patterns**[cite: 6]:
    * Async-first design (Python `async`/`await`).
    * Dependency Injection (FastAPI `Depends`, SAQ context/hooks).
    * Single Backend Docker Image: Builds API + Worker code; run with different commands.
    * Conversational Agent primary interface via Haystack Tool/Function calling.
* **Observability Strategy (MVP Target)**[cite: 5, 95]:
    * Instrumentation: OpenTelemetry SDK (standard for traces, metrics, logs).
    * Backend - Grafana Cloud: Centralized Logs (Loki), Metrics (Mimir), Traces (Tempo). Infrastructure & System view.
    * Backend - Sentry: Application Error Tracking & Performance Monitoring (APM). Application Code view.
    * Frontend/Backend - PostHog: Product Analytics, User Behavior Tracking, Feature Flags, Session Replay. User Interaction & Product view.
    * Supplemented by LLM Gateway (Portkey) for monitoring LLM calls, costs, latency, prompts[cite: 85, 90, 92].
