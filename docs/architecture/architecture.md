# Application Architecture

The application follows a monorepo structure, housing both the backend and frontend components. It is designed as a multi-component system orchestrated using Docker and Nginx as a reverse proxy.

## Primary Components and Functions

1.  **Frontend:**
    *   **Function:** Provides the user interface for interacting with the application. Currently focuses on a conversational chat interface, authentication flows, and basic profile management.
    *   **Technologies:** React 19.1, Mantine 7.17.4 (UI components), SuperTokens Auth React SDK (authentication), Vite (build tool/dev server).
    *   **Communication:** Communicates with the Backend API via HTTP requests, managed by a fetch-based API service that relies on browser cookie handling for sessions. Interacts directly with the SuperTokens Managed Service for authentication state management via the SDK.

2.  **Backend API (FastAPI):**
    *   **Function:** Acts as the main entry point for synchronous requests from the frontend. It handles user authentication, session management, basic data retrieval/storage, and triggers asynchronous tasks via the job queue.
    *   **Technologies:** Python 3.11+, FastAPI 0.115.0+, SQLAlchemy 2.0+ (ORM), SuperTokens Python SDK (authentication), Pydantic (data validation), `uv` (dependency management), SAQ (for enqueueing jobs).
    *   **Key Features Hosted/Initiated Here:**
        *   **Authentication (`backend/app/features/auth/`):** Manages user sign-up, sign-in, and session verification using the SuperTokens Python SDK, linking SuperTokens users to local database records. Includes dependencies (`get_required_user_from_session`) to protect API routes.
        *   **Chat API Endpoints (`backend/app/api/routers/chat.py`):** Exposes endpoints for `/interact` (handling new user messages), `/history` (retrieving previous messages for a session), and `/greeting` (generating a dynamic initial message). The `/interact` endpoint receives the user's message and session ID, validates the request, and then enqueues a corresponding chat processing job with the SAQ worker.
        *   **User Management (`backend/app/api/routers/user.py`):** Provides endpoints for retrieving user profile information.
        *   **Health Checks (`backend/app/api/routers/health.py`):** Provides endpoints to verify service health and configuration.
    *   **Communication:** Receives HTTP requests routed by Nginx. Interacts with the PostgreSQL database via SQLAlchemy for user data, chat history retrieval, and job status updates. Sends jobs to the Redis queue used by the Backend Worker via SAQ. Communicates with the SuperTokens Managed Service for authentication validation and user linking.

3.  **Backend Worker (SAQ):**
    *   **Function:** Processes long-running, resource-intensive, or I/O-bound tasks asynchronously, decoupling them from the synchronous API request flow. It is the primary execution environment for the AI-driven chat logic.
    *   **Technologies:** Python 3.11+, SAQ 0.22.5+ (background task queue consumer), SQLAlchemy 2.0+ (ORM), Haystack v2+ (AI orchestration), `uv`.
    *   **Key Features Implemented/Executed Here:**
        *   **Chat Processing (`backend/app/features/chat/chat_pipeline.py`):** Contains the definition and execution logic for the Haystack Pipeline that handles user messages. This pipeline is designed to process incoming messages, manage conversational state, and generate responses.
        *   **AI Orchestration (`backend/app/ai/`):** Houses the Haystack components and pipeline definitions. The chat pipeline specifically utilizes a Haystack `Agent`. The Agent is configured with an LLM generator (accessed via Portkey) and potentially a set of `Tools` that the Agent can decide to use based on the user's query.
        *   **Prompt Management (`backend/app/shared/prompts/`, `backend/app/features/.../prompts/`):** The chat pipeline (or components within it, like the Agent) utilizes the PromptService to fetch appropriate prompt templates (e.g., the system prompt, potentially specific prompts for tools or tasks) based on the configured pipeline tag and versioning strategy.
        *   **Tool Implementation (`backend/app/shared/tools/`, `backend/app/features/.../tools.py`):** Contains the implementations of specific tools that the Haystack Agent can call upon. While the specific tools for features like Creator DNA or Research are under development, the architecture supports the Agent invoking these tools during the chat flow.
        *   **Background Processing Tasks:** Executes specific tasks like the chat pipeline, and is the intended environment for future tasks such as data ingestion (e.g., YouTube ingestion).
    *   **Communication:** Polls the Redis queue for new jobs. Interacts with the PostgreSQL database via SQLAlchemy to retrieve chat history (for context), store new chat messages, and update job status. Uses Haystack to orchestrate interactions with LLMs via Portkey.

4.  **Database (PostgreSQL + pgvector):**
    *   **Function:** Stores both relational data (user information, chat history, project metadata, background job status) and vector embeddings for Retrieval-Augmented Generation (RAG). The chat history for each user/session is persisted here, providing conversational memory.
    *   **Technologies:** PostgreSQL 15+, pgvector extension (vector storage and indexing), Alembic (database migrations).
    *   **Communication:** Accessed by the Backend API (for history retrieval) and Backend Worker (for history retrieval, new message storage, job status updates) via SQLAlchemy using standard database protocols.

5.  **Redis:**
    *   **Function:** Serves as the message broker for the SAQ background task queue, facilitating communication between the Backend API (enqueueing chat processing tasks) and the Backend Worker (processing chat tasks).
    *   **Technologies:** Redis.
    *   **Communication:** Accessed by the Backend API and Backend Worker using the Redis protocol.

6.  **Nginx Reverse Proxy:**
    *   **Function:** Acts as the single entry point, routing incoming requests to the appropriate internal service (Frontend or Backend API). Handles SSL termination (in deployment) and manages specific CORS preflight requests.
    *   **Technologies:** Nginx.
    *   **Communication:** Routes HTTP traffic between the user's browser and the internal Docker services.

7.  **SuperTokens Managed Service:**
    *   **Function:** Provides core user authentication management (sign-up, sign-in, session handling).
    *   **Technologies:** SuperTokens Managed Service.
    *   **Communication:** Interacts with the Frontend SDK for UI flows and the Backend SDK for session verification and user linking.

8.  **Portkey (LLM Gateway):**
    *   **Function:** Acts as an abstraction layer and observability tool for interacting with various external LLMs. Used by the Haystack pipeline within the Backend Worker.
    *   **Technologies:** Portkey.
    *   **Communication:** Accessed by the Backend Worker (via Haystack) to make calls to External LLMs.

9.  **External LLMs:**
    *   **Function:** Provide large language model capabilities for tasks like text generation, summarization, etc., orchestrated by Haystack for the chat responses.
    *   **Technologies:** Various LLM providers (e.g., OpenAI, Anthropic) accessed via Portkey.
    *   **Communication:** Accessed by Portkey via their respective APIs.

## Detailed Chat Feature Flow:

1.  **User Input:** The user sends a message via the Frontend chat interface.
2.  **API Request:** The Frontend's `apiService` sends an HTTP POST request to the Backend API's `/api/v1/chat/interact` endpoint, including the user's message and session ID.
3.  **API Processing:**
    *   The FastAPI endpoint receives the request.
    *   Authentication dependencies (`get_required_user_from_session`) verify the user's session.
    *   The request data is validated using Pydantic schemas.
    *   The Backend API uses SAQ to enqueue a new job named `process_chat_message` (or similar) into the Redis queue. This job includes necessary context such as the user ID, session ID, and the user's message content.
    *   The API immediately returns a response to the Frontend, likely indicating that the message was received and a job was queued (e.g., returning a job ID).
4.  **Worker Processing:**
    *   The Backend Worker, continuously polling the Redis queue, picks up the `process_chat_message` job.
    *   The worker function retrieves the job details (user ID, session ID, message content).
    *   It uses SQLAlchemy to interact with the PostgreSQL database:
        *   Retrieving previous chat messages for the given session ID to provide conversation history to the LLM.
        *   Storing the user's incoming message in the database.
        *   Storing the AI's response in the PostgreSQL database, linking it to the same session ID.
        *   Updating the job status in Redis and PostgreSQL (e.g., to 'completed').
    *   The worker initializes and runs the Haystack Pipeline defined in `backend/app/features/chat/chat_pipeline.py`.
    *   Inside the pipeline, the configured Haystack `Agent` takes the user's message and chat history as input.
    *   The Agent uses the PromptService to fetch the appropriate system prompt and potentially other prompts based on the configured pipeline tag.
    *   Based on the prompt, input, and available tools, the Agent decides the next step: either directly generate a response using the LLM via Portkey or invoke one or more configured Tools.
    *   If a Tool is invoked, the worker executes the Python function corresponding to the tool, which might perform actions like data retrieval (potentially from PostgreSQL via RAG), external API calls (though none are fully implemented for chat yet), etc. The tool's result is returned to the Agent.
    *   The Agent continues its process (potentially invoking more tools or generating a final response) based on the tool outputs and the conversation goal.
    *   Once the Agent determines the final response, the worker receives this response.
5.  **Frontend Update:** The Frontend, which is likely polling a status endpoint or will eventually use WebSockets/SSE (as per the plan in `productContext.md`), detects that the job for the sent message is complete. It then retrieves the updated chat history (including the AI's response) from the Backend API's `/api/v1/chat/history` endpoint and updates the UI.

## Architectural Diagram:

```mermaid
graph TD
    User --> Nginx
    Nginx --> Frontend
    Nginx --> BackendAPI
    Frontend --> SuperTokensMS
    BackendAPI --> PostgreSQL
    BackendAPI --> Redis
    BackendAPI --> SuperTokensMS
    BackendWorker --> Redis
    BackendWorker --> PostgreSQL
    BackendWorker --> Haystack
    Haystack --> Portkey
    Portkey --> ExternalLLMs

    subgraph User Interface
        Frontend
    end

    subgraph Backend Services
        BackendAPI[Backend API (FastAPI)]
        BackendWorker[Backend Worker (SAQ)]
        Haystack[AI Orchestration (Haystack)]
    end

    subgraph Data Stores
        PostgreSQL[PostgreSQL + pgvector]
        Redis[Redis]
    end

    subgraph Infrastructure
        Nginx[Nginx Reverse Proxy]
    end

    subgraph External Services
        SuperTokensMS[SuperTokens Managed Service]
        Portkey[LLM Gateway (Portkey)]
        ExternalLLMs[External LLMs]
    end

    classDef default fill:#f9f,stroke:#333,stroke-width:2px;
    classDef infrastructure fill:#ccf,stroke:#333,stroke-width:2px;
    classDef datastore fill:#cfc,stroke:#333,stroke-width:2px;
    classDef external fill:#ffc,stroke:#333,stroke-width:2px;

    class Nginx infrastructure;
    class PostgreSQL,Redis datastore;
    class SuperTokensMS,Portkey,ExternalLLMs external;

    linkStyle 0 stroke:#555,stroke-width:1.5px,color:#555;
    linkStyle 1 stroke:#555,stroke-width:1.5px,color:#555;
    linkStyle 2 stroke:#555,stroke-width:1.5px,color:#555;
    linkStyle 3 stroke:#555,stroke-width:1.5px,color:#555;
    linkStyle 4 stroke:#555,stroke-width:1.5px,color:#555;
    linkStyle 5 stroke:#555,stroke-width:1.5px,color:#555;
    linkStyle 6 stroke:#555,stroke-width:1.5px,color:#555;
    linkStyle 7 stroke:#555,stroke-width:1.5px,color:#555;
    linkStyle 8 stroke:#555,stroke-width:1.5px,color:#555;
    linkStyle 9 stroke:#555,stroke-width:1.5px,color:#555;
    linkStyle 10 stroke:#555,stroke-width:1.5px,color:#555;
    linkStyle 11 stroke:#555,stroke-width:1.5px,color:#555;
```
