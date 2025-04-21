# Chat Feature Refactoring Plan

## Objective

Refactor the existing chat implementation to utilize a Haystack `Agent` component for improved structure and future function calling capabilities, and implement LLM-based greeting generation using user history and versioned prompts via `PromptService`.

## Current State Analysis

Based on the code review of `backend/app/features/chat/chat_pipeline.py`, `backend/app/api/routers/chat.py`, `backend/app/services/chat_service.py`, and `backend/app/services/prompt_service.py`:

*   Basic chat flow (message processing, history, greeting placeholder) is present.
*   Database interaction for history (`ChatMessage`) is implemented.
*   Prompt versioning via `PromptService` and `pipeline-tags.yaml` is functional.
*   The chat pipeline currently uses `OpenAIChatGenerator` directly instead of a Haystack `Agent`.
*   The `/greeting` endpoint uses placeholder logic for greeting generation.
*   The `system` and `main_chat` prompts fetched in `chat_pipeline.py` are not fully integrated into the current pipeline structure.

## Planned Features (Confirmed)

*   Basic chat interaction
*   Chat history retrieval
*   LLM-based greeting generation using user history
*   Utilization of Haystack `Agent` for pipeline structure (in preparation for function calling)
*   Correct usage of `PromptService` for `system`, `greeting`, and `main_chat` prompts.

## Revised Plan

### 1. Refactor `backend/app/features/chat/chat_pipeline.py`

*   **Goal:** Replace direct `OpenAIChatGenerator` usage with a Haystack `Agent`, utilizing prompts fetched via `PromptService`.
*   **Steps:**
    *   Import the `Agent` component from Haystack (`haystack.components.agents`).
    *   **Fetch Prompts:** Use the injected `PromptService` instance to fetch:
        *   `system_prompt_content = await prompt_service.get_prompt_content(pipeline_type="chat", logical_prompt_name="system", override_pipeline_tag=...)`
        *   `main_chat_template = await prompt_service.get_prompt_content(pipeline_type="chat", logical_prompt_name="main_chat", override_pipeline_tag=...)` (This template will likely define how conversation history and the current query are formatted for the LLM within the agent's turn).
    *   **Instantiate Agent:** Instantiate the `Agent`, providing:
        *   The `OpenAIChatGenerator` instance (`llm_generator`) as the LLM.
        *   The fetched `system_prompt_content` to the `Agent`'s `system_prompt` parameter.
        *   *(Implementation Detail):* The `Agent` component internally manages how the `system_prompt`, conversation history (`messages`), and the current user input are combined. It might use an internal `PromptBuilder` or similar logic. The fetched `main_chat_template` might be needed for this internal templating, potentially passed during `Agent` initialization or configuration depending on the specific Haystack version's `Agent` API. This will be confirmed during implementation based on the `Agent`'s signature.
    *   **Update Pipeline:** Replace `pipeline.add_component("llm_generator", ...)` with `pipeline.add_component("agent", configured_agent_instance)`.
    *   **Adjust Service Call:** Update the `pipeline.run_async` call in `ChatService.interact` to pass the required inputs (`messages`, potentially `query` separately depending on the Agent, `user`, `user_service` for tools etc.) to the `"agent"` component.
*   **Diagram:**

    ```mermaid
    graph TD
        subgraph Build Chat Pipeline
            direction LR
            B_PS[PromptService] --> B_FetchSys(Fetch 'system' prompt);
            B_PS --> B_FetchMain(Fetch 'main_chat' prompt);
            B_LLM[Instantiate OpenAIChatGenerator] --> B_Agent(Instantiate Agent);
            B_FetchSys --> B_Agent;
            B_FetchMain -- Used by Agent's internal templating --> B_Agent;
            B_Tools[Empty Tool List] --> B_Agent;
            B_Agent --> B_Add(Add Agent to AsyncPipeline);
        end
        A[ChatService.interact] --> Build_Chat_Pipeline;
        Build_Chat_Pipeline --> H[Return Pipeline];
        A --> I{Prepare Agent Input (messages, user, etc.)};
        I --> J[pipeline.run_async];
        J --> K[Process Agent Output];
        K --> L[Store Response & Return];
    ```

### 2. Refactor `/greeting` Endpoint (`backend/app/api/routers/chat.py`)

*   **Goal:** Implement LLM-based greeting generation using user history and the correct prompt from `PromptService`.
*   **Steps:**
    *   Modify the endpoint logic to fetch a relevant subset of the user's `ChatMessage` history from the database (e.g., last N interactions).
    *   **Fetch Prompt:** Use the injected `PromptService` to fetch the greeting template: `greeting_template = await prompt_service.get_prompt_content(pipeline_type="chat", logical_prompt_name="greeting", override_pipeline_tag=...)`.
    *   Instantiate an LLM generator (e.g., `OpenAIChatGenerator`) within the endpoint (or use a dedicated small pipeline/service function).
    *   Format the fetched `greeting_template` with user details and the summarized/formatted interaction history.
    *   Call the LLM generator with the formatted prompt.
    *   Return the generated greeting text in the `GreetingResponse`.
*   **Diagram:**

    ```mermaid
    graph TD
        M[GET /greeting Request] --> N{Fetch User History (DB)};
        N --> O{Fetch 'greeting' Prompt (PromptService)};
        O --> P{Instantiate LLM Generator};
        Q[Format Greeting Prompt w/ History & User] --> R[Call LLM Generator];
        N --> Q;
        O --> Q;
        P --> R;
        R --> S[Return Generated Greeting];
    ```

### 3. Update Memory Bank

*   **Goal:** Record the decisions made.
*   **Steps:**
    *   Add/update entries in `memory-bank/decisionLog.md` documenting the decision to use Haystack `Agent`, implement LLM-based greetings, and explicitly use `PromptService` for `system`, `greeting`, and `main_chat` prompts.
    *   Update `memory-bank/activeContext.md` and `memory-bank/progress.md` to reflect the refined refactoring tasks.

### 4. Documentation (Optional)

*   This plan is being written to `docs/chat_refactor_plan.md`.

## Next Steps

Upon user confirmation of successful file writing, request to switch to the `code` mode to begin implementing this plan.
