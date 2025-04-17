# Product Context

This file provides a high-level overview of the project and the expected product. It synthesizes information from various project documents and should be updated as the project evolves.
2025-04-17 08:59:27 - Log of updates made (Restored original README citations to refined content).

*

## Project Goal

* - **Primary Goal:** Develop an AI-powered platform designed to drastically reduce the pre-production bottleneck (research, structuring, scripting) for educational content creators, enabling sustainable channel growth by transforming hours of manual work into a focused, AI-assisted workflow. [Source: README.md Sec 1]
* - **Core Problem Addressed:** Creators face a significant "Time-Quality Paradox," spending 10-30 hours per video, with 60-70% often consumed by research and scripting. This leads to creator burnout and limits content output. Furthermore, existing AI tools frequently fail to preserve the creator's unique voice and teaching style, which is critical for audience connection and trust. [Source: README.md Sec 2]
* - **Target Audience:** Primarily "Accelerating Creators" – typically solo operators with 25K-50K subscribers generating \$30K-\$75K annually. They are transitioning from passion projects to professional businesses and feel the conflict between their educational mission and the demands of scaling. They seek solutions that save significant time while rigorously preserving their unique voice and authenticity. [Source: README.md Sec 2]

## PoC Scope & Goals

* - **Primary Goal:** Validate the technical feasibility and core value proposition of the research-to-script flow using the chosen tech stack (Python/FastAPI/SAQ backend, Haystack/Portkey AI layer, SvelteKit frontend, PostgreSQL/pgvector DB).
* - **Key PoC Flow:** Minimal Creator DNA Capture -> Basic Automated Research -> Human Review/Approval -> Single Script Section Generation.
* - **Interaction Model:** A minimal conversational web UI built with SvelteKit, enabling users to interact with the backend agent API.
* - **Success Criteria:** Demonstrate a working end-to-end flow; achieve >70% perceived voice authenticity in generated text (via initial user feedback); demonstrate potential for >50% reduction in active research/scripting time; elicit positive qualitative feedback ("Wow" factor) from 3+ friendly testers; establish and validate core architecture patterns.

## Key Features & Value Proposition (Phased View)

* - **Core Value Proposition (The Creator Success Triad):**
    * **1. Creator DNA Technology (Key Differentiator):** Analyzes creator's existing content to capture unique linguistic patterns, terminology, pacing, tone, and teaching style. Aims to move beyond generic AI output. (PoC: Basic pattern capture, MVP: Style fine-tuning controls). [Source: README.md Sec 3]
    * **2. Pre-Production Accelerator:** Automates time-consuming tasks like research, content structuring, and initial script drafting. Targets a 90% reduction in active pre-production time (e.g., 15-30 hours down to 2-3 hours of review & refinement). (PoC: Basic research/scripting, MVP: Enhanced capabilities). [Source: README.md Sec 3]
    * **3. Content Opportunity Engine (Post-MVP Scope):** Future features like data-driven idea validation and knowledge gap analysis to inform content strategy.
* - **Human-in-the-Loop Workflow:** The platform operates as a creator's assistant, guiding them through the pre-production process via a primarily conversational interface. AI generates suggestions (research findings, structure options, script drafts) which the creator reviews, edits, and approves at key decision points. Creator control and oversight are fundamental.
* - **Sustainable Scaling:** Empower creators to significantly increase their content output (potentially doubling it) without a corresponding increase in workload, thus mitigating burnout. [Source: README.md Sec 3]
* - **Educational Effectiveness:** Provide AI-powered suggestions and tools to optimize content structure and clarity, aiming for improved learning outcomes and viewer retention. [Source: README.md Sec 3]
* - **Phased Feature Rollout (Module-Based):** [Source: README.md Sec 3]
    * Module 1: Creator Voice & Identity (PoC/MVP)
    * Module 2: Strategic Content Intelligence (MVP+)
    * Module 3: Research & Knowledge Management (PoC/MVP)
    * Module 4: Content Production Pipeline (PoC/MVP)
    * Module 5: Distribution & Monetization (Post-MVP)
    * Module 6: Creator Workflow System (PoC/MVP)
    * Module 7: Platform Foundation (PoC/MVP)

## Overall Architecture

* - **Structure:** Monorepo containing Backend (Python/FastAPI API & SAQ Worker) and Frontend (SvelteKit). [Source: README.md Sec 5]
* - **Primary User Interface:** Conversational agent interface (driven by Haystack components) complemented by necessary GUI elements built with SvelteKit. Minimal GUI in PoC, evolving for MVP usability.
* - **Core Technologies:** Python 3.11+, FastAPI 0.115.0+, SAQ 0.22.5+ (for background tasks), Haystack v2+ (AI orchestration), Portkey (LLM Gateway - abstraction & observability for PoC/MVP), PostgreSQL 15+ w/ pgvector (vector & relational data), Redis (SAQ Broker), Alembic (DB Migrations), Svelte 5.26.0+, Docker (Containerization), Container PaaS (Target Hosting). [Source: README.md Sec 6.a]
* - **Data Layer:** Utilizes SQLAlchemy 2.0+ ORM models. The `RETRIEVABLE_TEXT` table is central for Retrieval-Augmented Generation (RAG), storing chunked text from various sources (transcripts, personal stories) along with vector embeddings generated via models accessed through Portkey. Embeddings indexed using pgvector (HNSW/IVFFlat). Relational tables provide structure, track workflow state, and enable metadata filtering during retrieval.
* - **Observability Strategy (MVP Target):** Comprehensive monitoring using OpenTelemetry for instrumentation. Deploys a stack combining Grafana Cloud (Infrastructure & System Observability: Logs, Metrics, Traces), Sentry (Application Code Health: Errors, APM), and PostHog (Product Analytics: User Behavior, Events). The LLM Gateway (Portkey) provides specialized observability for AI interactions (costs, latency, quality). PoC phase relies heavily on basic logging and the Portkey dashboard.
* - **Key Architectural Principles:** Minimize direct infrastructure operation ("Low-Ops"); prioritize Async-first design; ensure Modularity for rapid iteration; enforce Idempotency, especially for background tasks; maintain Creator Voice Authenticity as a core product principle; enable Cost-efficient Scaling from the start. [Source: README.md Sec 6.b]
* - **API vs. Worker Design:** The FastAPI API handles synchronous requests (authentication, validation, simple data operations, task initiation). It returns job IDs for long-running operations. For PoC, the frontend polls status endpoints. The SAQ Worker executes asynchronous, long-running, or I/O-bound tasks (e.g., LLM interactions via Haystack/Portkey, data ingestion pipelines, complex analyses) and updates status/results in the database. MVP aims to replace polling with WebSockets/SSE for real-time updates. [Source: README.md Sec 6.d]
* - **Key Consideration (Deferred Technical Debt):** The current architecture (SAQ + background job tracking) is sufficient for PoC/MVP's independent background tasks but does *not* adequately address complex, multi-step, stateful workflow orchestration (e.g., managing the entire video creation lifecycle as a single, resilient process). This capability is intentionally deferred post-MVP and will likely require adopting a dedicated workflow engine (e.g., Temporal, Prefect).
