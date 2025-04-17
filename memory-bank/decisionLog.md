# Decision Log

This file records architectural and implementation decisions using a list format.
2025-04-17 08:43:45 - Log of updates made.

*

## Decision

* [2025-04-17 12:34:00] - Use SuperTokens Managed Service for Authentication

## Rationale

* SuperTokens Managed Service aligns with our "Low-Ops" principle, eliminating the need to run and maintain authentication servers ourselves.
* It provides a complete authentication solution with pre-built UI components, reducing development time.
* The SDK offers both backend (FastAPI) and frontend (SvelteKit) integration.
* The managed service handles security complexities like password storage and session management.
* SuperTokens supports our core authentication requirements: sign-up, sign-in, sign-out, and session management.
* The free tier of the managed service is sufficient for our PoC needs.

## Implementation Details

* **Backend Integration:**
  * Added `supertokens-python-sdk` dependency to the backend.
  * Created configuration module in `backend/app/features/auth/supertokens_config.py`.
  * Implemented async-compatible user linking between SuperTokens and our database.
  * Added session verification middleware to protect the `/agent/interact` endpoint.
  * Modified the `User` model to include a `supertokens_user_id` field.

* **Frontend Integration:**
  * Added `supertokens-web-js` dependency to the frontend.
  * Created a catch-all route for the pre-built authentication UI.
  * Updated the API client to use SuperTokens session management.
  * Added login/logout functionality to the main layout.
  * Created protected dashboard page that requires authentication.
