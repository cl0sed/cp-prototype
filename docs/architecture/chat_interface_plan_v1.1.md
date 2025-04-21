# Architecture Plan: Minimal React/FastAPI Chat Interface with Haystack/Portkey

**Version:** 1.1 (Incorporating Evaluation Recommendations)
**Date:** 2025-04-19

## 1. Overview

This document outlines the architecture and implementation plan for a minimal chat interface. The interface will use a React 19 frontend and a FastAPI backend. The backend integrates with Haystack 2.x and Portkey to provide conversational AI responses based on user input and conversation history. This interface will serve as the default landing page for logged-in users, separate from the user profile section.

**Project Context:** This builds upon an existing monorepo structure with FastAPI, React (recently re-architected with React 19, Mantine, SuperTokens), Haystack, Portkey, Docker, and PostgreSQL.

## 2. Architecture

### 2.1. Components

*   **Frontend (React 19):**
    *   `ChatPage.jsx`: Main component managing state (`useState` for history, input, loading, error; potentially `useOptimistic` for user messages). Orchestrates child components.
    *   `ChatInput.jsx`: Handles user text input and submission (potentially using React Actions / `useFormState`).
    *   `MessageList.jsx`: Renders the conversation history array.
    *   `apiService.js` / `useChatApi.js`: Handles API communication (fetching data, managing errors).
*   **Backend (FastAPI):**
    *   `chat_router.py`: Defines `/api/v1/chat/interact` endpoint (POST).
    *   `schemas.py`: Pydantic models (`ChatMessageRequest`, `ChatMessageResponse`). Ensure strict validation on input size.
    *   `chat_service.py`: Core logic interacting with Haystack.
    *   `config.py`: Loads environment variables, including Portkey API Key/Virtual Key.
*   **AI Core (Haystack 2.x):**
    *   `ai/chat_pipeline.py` (Preferred location): Defines the pipeline.
    *   Minimal Pipeline Components:
        *   `Input`: Receives user message and history.
        *   `PromptBuilder`: Formats input/history for the LLM, considering specific role tags and separators.
        *   `CustomPortkeyGenerator`: **(Key Implementation)** A custom Haystack component (`@component`, subclassing `haystack.core.component.Component`) wrapping the `portkey-ai` *async* client. Uses `InputSocket` for prompt, `OutputSocket` for response. Handles async calls and errors correctly within Haystack.
        *   `Output`: Returns the final response.
*   **LLM Gateway (Portkey):**
    *   `portkey-ai` Python library (async client).
    *   **Configuration:** Use Portkey **Virtual Keys** (configured via `config.py`).
    *   **Metadata:** Pass `user_id` (from SuperTokens session) as metadata in Portkey calls.
    *   **Observability:** Rely on Portkey dashboard for PoC monitoring.
*   **LLM:** External Language Model configured via Portkey dashboard.

### 2.2. Data Flow

1.  User interacts with `ChatInput` on `ChatPage`.
2.  On submit, `ChatPage` (potentially using `useOptimistic`) immediately adds the user message to local state.
3.  `ChatPage` calls `apiService.sendMessage`, sending the current user message and the full `conversationHistory` array (from `useState`).
4.  FastAPI `/api/v1/chat/interact` receives the request, validates via `ChatMessageRequest` (Pydantic).
5.  Protected by `get_required_user_from_session` dependency, providing `user_id`.
6.  `ChatService` is injected via `Depends`.
7.  `ChatService.interact` method is called with validated data and `user_id`.
8.  `ChatService` runs the Haystack pipeline defined in `ai/chat_pipeline.py`.
9.  Pipeline Execution:
    *   `PromptBuilder` formats the prompt.
    *   `CustomPortkeyGenerator` receives the prompt, uses the async `portkey-ai` client to call Portkey, passing the prompt and `user_id` as metadata, using the configured Virtual Key.
    *   Portkey routes to LLM, logs, and returns the response.
    *   `CustomPortkeyGenerator` receives the response and passes it through the output socket.
10. Pipeline returns the `agent_response` to `ChatService`.
11. `ChatService` returns the response to the FastAPI router.
12. FastAPI formats the response using `ChatMessageResponse` and sends JSON back to the frontend.
13. Frontend `apiService` receives the response.
14. `ChatPage` updates `conversationHistory` state with the agent's response, clears loading/error states.
15. `MessageList` re-renders with the new message.

### 2.3. Mermaid Diagram

```mermaid
graph TD
    A[User] --> B(React Frontend);
    B --> C{ChatPage.jsx};
    C --> D[ChatInput.jsx];
    D --> C;
    C --> E[MessageList.jsx];
    C --> F[apiService.js / useChatApi.js];
    F --> G(FastAPI Backend);
    G --> H[chat_router.py];
    H --> I{/api/v1/chat/interact};
    I --> J[API schemas.py];
    J --> I;
    I --> K[chat_service.py];
    K --> L(Haystack Pipeline);
    subgraph Haystack Pipeline (ai/chat_pipeline.py)
        M[Input] --> N[PromptBuilder];
        N --> O[CustomPortkeyGenerator];
        O --> P[Output];
    end
    L --> K;
    O --> Q(Portkey Service);
    Q --> R(LLM);
    R --> Q;
    Q --> O;
    K --> I;
    I --> G;
    G --> F;
    F --> C;

    style O fill:#f9f,stroke:#333,stroke-width:2px
```

## 3. Implementation Plan

*(Assumes frontend rearchitecture tasks 11a-9, 11a-10 are complete)*

1.  **Backend: API Endpoint Structure (Task 4b):**
    *   Create `backend/app/api/routers/chat_router.py`.
    *   Define `/api/v1/chat/interact` (POST) with `ChatMessageRequest` and `ChatMessageResponse` models (from `schemas.py`). Ensure strict validation.
    *   Protect with `get_required_user_from_session`.
    *   Register router in `main.py`. Confirm CORS.
2.  **Backend: Portkey Setup (Task 5a - Enhanced):**
    *   Add `portkey-ai` to `pyproject.toml`.
    *   Add `PORTKEY_API_KEY` and `PORTKEY_CHAT_VIRTUAL_KEY` placeholders to `.env.example`.
    *   Update `config.py` to load these keys.
    *   Implement dependency (`Depends`) to provide an initialized *async* Portkey client configured with the Virtual Key.
3.  **Backend: Chat Service (Task 5c, 5f):**
    *   Create `backend/app/services/chat_service.py` with `ChatService` class.
    *   Implement `async interact(self, user_message: str, conversation_history: List, user: User)` method.
    *   Include try/except for error handling and logging.
4.  **Backend: Haystack Pipeline & Custom Component (Task 5b - Enhanced):**
    *   Add `haystack-ai` to `pyproject.toml`.
    *   Create `backend/app/ai/chat_pipeline.py`.
    *   Define the minimal Haystack pipeline (`Input -> PromptBuilder -> CustomPortkeyGenerator -> Output`).
    *   **Implement `CustomPortkeyGenerator`:** Create a custom Haystack component wrapping the async `portkey-ai` client. Ensure it handles async calls correctly, accepts prompt via `InputSocket`, returns response via `OutputSocket`, and passes `user_id` metadata.
    *   Integrate pipeline execution into `ChatService.interact`.
5.  **Frontend: Chat Interface UI (Task 6a-3):**
    *   Create `ChatInput.jsx` (consider React Actions / `useFormState`).
    *   Create `MessageList.jsx`.
    *   Create `ChatPage.jsx`: Manage state (`useState`, consider `useOptimistic`), implement `handleSendMessage`, render children.
    *   Configure routing: Make `ChatPage` the default for authenticated users at `/` or a dedicated route.
6.  **Frontend: API Connection (Task 6a-4):**
    *   Update `apiService.js`: Add `async sendMessage(userMessage, conversationHistory)` function using `fetch` (POST to `/api/v1/chat/interact`, `credentials: 'include'`). Handle errors.
7.  **Frontend: Connect UI to API (Task 6a-6):**
    *   Wire `ChatPage.handleSendMessage` to call `apiService.sendMessage`. Update state based on response/errors.
8.  **Observability & Testing:**
    *   Ensure backend logging to stdout. Rely on Portkey dashboard. (Task 9a)
    *   Add basic backend integration tests (mocking pipeline/Portkey).
    *   Add basic frontend component tests (RTL).

## 4. Considerations & Future Work

*   **State Management:** `useState` for history is PoC-specific. MVP+ will require server-side history or a more scalable frontend approach.
*   **Streaming:** Not included in PoC. Consider for MVP+ for better UX.
*   **Error Handling:** Requires careful implementation across the stack for user-friendly feedback.
*   **Complex Pipelines:** PoC uses a minimal pipeline. Future work involves adding Haystack tools (`research_topic`, etc.) and potentially Human-in-the-Loop steps.
