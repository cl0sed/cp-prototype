|
# Chat Interface Enhancements Plan

## Overall Goal
Resolve critical issues (automatic reloads, lack of persistence) and enhance the user experience (responsiveness, visibility, initial state) for the Haystack/Portkey integrated chat interface, which serves as the user's home page upon login.

## Requirements Addressed
1.  **Prevent Automatic Page Reloads & Ensure Chat Persistence:** Diagnose and fix the cause of the ~30-second page reload. Implement state management to preserve the visible chat session without page refreshes and ensure previous chat history is loaded and displayed upon user login or page visit.
2.  **Implement Responsive Chat UI:** Ensure the chat window container, message display area, and text input field dynamically resize to fit entirely within the browser's viewport across different screen sizes, preventing overflow.
3.  **Enhance Chat Window Visibility:** Apply subtle styling (e.g., borders, shadows, slight background contrast) to make the chat window visually distinct from the main page background while maintaining a clean aesthetic.
4.  **Establish Initial Login State:** Upon user login, either display their existing chat history or, if none exists, initiate the chat with a default greeting message from the backend model.

## Plan

### Phase 1: Stability & Persistence

1.  **Investigate Page Reload (External Factors):**
    *   **Goal:** Identify the root cause of the ~30s reload. Since no console errors are present and it happens even when idle, investigate external factors.
    *   **Actions:**
        *   Review SuperTokens session configuration (`backend/app/features/auth/supertokens_config.py`, `frontend/src/config/supertokens.ts`) for session lifetime, refresh mechanisms, or potential conflicts causing forced reloads.
        *   Examine Nginx configuration (`reverse-proxy.conf`) for proxy timeouts (`proxy_read_timeout`, `proxy_send_timeout`) that might be closing connections prematurely.
        *   Check Docker Compose (`docker-compose.yaml`) logs for any container restarts or health check failures that might coincide with the reloads.
        *   *Contingency:* If the cause remains elusive, consider adding frontend logging to track component lifecycle events or network requests around the time of the reload.
    *   **Mode:** Debug (for investigation), then potentially Code/Architect for fixes.

2.  **Implement Chat History Persistence (Backend):**
    *   **Goal:** Store chat messages persistently in the PostgreSQL database.
    *   **Actions:**
        *   Define a new SQLAlchemy model (`ChatMessageHistory`?) in `backend/app/models/` linked to the `User` model (one-to-many). Include fields for `user_id`, `sender` (user/agent), `text`, and `timestamp`.
        *   Generate and apply an Alembic migration to create the new table.
        *   Modify `ChatService.interact` (`backend/app/services/chat_service.py`) to save both the user message and the agent's response to the new database table after successful interaction, associating them with the `user.id`.
    *   **Mode:** Code

3.  **Implement Chat History Retrieval (Backend):**
    *   **Goal:** Create an API endpoint to fetch the last 20 messages for a user.
    *   **Actions:**
        *   Add a new GET endpoint (e.g., `/api/v1/chat/history`) to `chat_router.py`. Protect it using `get_required_user_from_session`.
        *   Add a new method `get_chat_history(user_id: int, limit: int = 20)` to `ChatService`. This method will query the `ChatMessageHistory` table, order by timestamp descending, limit the results to 20, and then reverse the list to maintain chronological order for the frontend.
        *   Implement the logic in the new router endpoint to call `chat_service.get_chat_history`.
    *   **Mode:** Code

4.  **Implement Initial Greeting Logic (Backend):**
    *   **Goal:** Send a default greeting only on the user's very first interaction.
    *   **Actions:**
        *   Modify the `/api/v1/chat/history` endpoint logic:
            *   When fetching history, if the query returns *no messages* for the user, call a new `ChatService` method `get_initial_greeting()`.
            *   `get_initial_greeting()` can return a hardcoded greeting string or potentially make a simple LLM call via a dedicated minimal pipeline/service method if dynamic greetings are desired later.
            *   The endpoint should return either the list of historical messages or a list containing just the single greeting message.
    *   **Mode:** Code

5.  **Implement Chat History Loading (Frontend):**
    *   **Goal:** Load and display chat history or the initial greeting when the chat page loads.
    *   **Actions:**
        *   Add a new method `getChatHistory()` to `apiService.ts` to call the new `/api/v1/chat/history` backend endpoint.
        *   In `ChatPage.tsx`, use a `useEffect` hook that runs once on component mount.
        *   Inside the `useEffect`, call `apiService.getChatHistory()`.
        *   On success, update the `conversationHistory` state with the messages received from the backend. Handle potential errors.
    *   **Mode:** Code

6.  **Update Frontend State Management (Optional but Recommended):**
    *   **Goal:** Improve state management robustness, especially if the reload issue persists or complexity increases.
    *   **Actions:**
        *   Consider replacing `useState` in `ChatPage.tsx` with a more robust state management library (like Zustand or React Context API) for managing `conversationHistory`, `isLoading`, and `error`. This makes state logic more centralized and easier to manage, especially if other components need access to it later.
    *   **Mode:** Code

### Phase 2: UI Enhancements

7.  **Implement Responsive Chat UI:**
    *   **Goal:** Ensure chat elements fit within the viewport on all screen sizes.
    *   **Actions:**
        *   Review the layout of `ChatPage.tsx`, `MessageList.tsx`, and `ChatInput.tsx`.
        *   Utilize Mantine's responsive style props (e.g., `<Box h={{ base: 'calc(100vh - 120px)', sm: 'calc(100vh - 60px)' }}>`) or `useMediaQuery` hook to adjust heights, padding, margins, and potentially font sizes based on viewport width.
        *   Ensure the `MessageList` (`overflowY: 'auto'`) correctly handles scrolling within its container without causing page overflow.
        *   Test thoroughly using browser developer tools in responsive mode.
    *   **Mode:** Code

8.  **Enhance Chat Window Visibility:**
    *   **Goal:** Make the chat window visually distinct.
    *   **Actions:**
        *   In `ChatPage.tsx`, modify the main `Paper` component (line 57) props:
            *   Add `withBorder` for a subtle border.
            *   Adjust `shadow="sm"` (or `md`) as needed.
            *   Consider a slightly different background color using Mantine theme variables if desired (e.g., `bg="var(--mantine-color-gray-0)"` if the main page background is pure white).
    *   **Mode:** Code

## Diagrams

### Initial Load Sequence

```mermaid
sequenceDiagram
    participant User
    participant Frontend (ChatPage)
    participant Frontend (apiService)
    participant Backend (chat_router)
    participant Backend (chat_service)
    participant Database

    User->>Frontend (ChatPage): Loads Chat Page
    Frontend (ChatPage)->>Frontend (apiService): useEffect -> getChatHistory()
    Frontend (apiService)->>Backend (chat_router): GET /api/v1/chat/history
    Backend (chat_router)->>Backend (chat_service): get_chat_history(user_id, limit=20)
    Backend (chat_service)->>Database: Query ChatMessageHistory (user_id, ORDER BY timestamp DESC, LIMIT 20)
    Database-->>Backend (chat_service): Return messages (or empty list)
    alt History Exists (Messages Found)
        Backend (chat_service)->>Backend (chat_service): Reverse message list (chronological)
        Backend (chat_service)-->>Backend (chat_router): Return history (List[ChatMessage])
    else No History (Empty List)
        Backend (chat_service)->>Backend (chat_service): get_initial_greeting()
        Backend (chat_service)-->>Backend (chat_router): Return greeting (List[ChatMessage])
    end
    Backend (chat_router)-->>Frontend (apiService): Return history or greeting
    Frontend (apiService)-->>Frontend (ChatPage): Provide history/greeting
    Frontend (ChatPage)->>Frontend (ChatPage): setConversationHistory(messages)
